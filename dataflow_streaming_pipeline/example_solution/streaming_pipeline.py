import logging
import json
import itertools

from typing import Dict, List

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions, StandardOptions

BQ_SCHEMA = ",".join(
    [
        "Product_ID:STRING",
        "Gender:STRING",
        "Age:STRING",
        "Occupation:INTEGER",
        "City_Category:STRING",
        "Stay_In_Current_City_Years:FLOAT64",
        "Marital_Status:INTEGER",
        "Product_Category_1:INTEGER",
        "Value:FLOAT64",
        "Lower_bound:FLOAT64",
        "Upper_bound:FLOAT64",
        "Class_of_spend:STRING"
    ]
)


# ParDo example:
# A ParDo can have a one-to-many relationship between in and output -> 1 event in, N events out
# This is the reason why we use 'yield' and not 'return'
class ModelInvoker(beam.DoFn):
    def __init__(self, project, location, endpoint_name, *unused_args, **unused_kwargs):
        self.project = project
        self.location = location
        self.endpoint_name = endpoint_name
        self.endpoint = None

    def setup(self):
        from google.cloud import aiplatform
        aiplatform.init(project=self.project.get(), location=self.location.get())
        self.endpoint = aiplatform.Endpoint(self.endpoint_name.get())

    def process(self, instances: List[Dict]):
        response = self.endpoint.predict(instances=instances)
        predictions = response.predictions
        for instance, prediction in zip(instances, predictions):
            result = dict(itertools.chain(instance.items(), prediction.items()))
            result["Class_of_spend"] = "Medium"

            #TODO
            # Add additional logic so that the 'Class_of_spend' is low when the 'Value' is <= 5000
            # Medium when 5000 - 10000
            # High when > 1000
            spend_class = "Low"
            if result["Value"] > 5000:
                spend_class = "Medium"
            if result["Value"] > 10000:
                spend_class = "High"
            result["Class_of_spend"] = spend_class

            yield result

# Map examples:
# A map is a one-to-one relationship between events and their result -> 1 event in is 1 event out
def decode(event):
    event_decoded = event.decode('utf-8')
    return event_decoded

def classify_age_group(event):

    #TODO
    # Downstream applications can not know how old a person is because it can be considered PII, therefore we will map
    # it to lettered age groups.
    # Please implement this function so that it maps the age groups '26-35' and '36-45' to 'A'
    # '46-55' and '56-65' to 'B'
    # The rest to 'C'
    age = event["Age"]
    if age == "26-35" or age == "36-45":
        event["Age"] = "A"
    if age == "46-55" or age == "56-65":
        event["Age"] = "B"
    else:
        event["Age"] = "C"

    return event

class PubsubPredBqOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            "--input_topic",
            default="projects/data-night-2022/topics/streaming-data",
            help=(
                "Input Pub/Sub topic of the form "
                '"projects/<PROJECT>/topics/<TOPIC>".'
            )
        )
        parser.add_value_provider_argument(
            "--output_table",
            help=(
                "Output BigQuery table of the form "
                '"<PROJECT>:<DATASET>.<TABLE> or <DATASET>.<TABLE>".'
            )
        )
        parser.add_value_provider_argument(
            "--model_project",
            help="Project of the endpoint of the Vertex AI model"
        )
        parser.add_value_provider_argument(
            "--model_location",
            help="Location of the endpoint of the Vertex AI model"
        )
        parser.add_value_provider_argument(
            "--model_endpoint_id",
            help="ID of the endpoint of the Vertex AI model"
        )

def run(save_main_session: bool = True):
    pipeline_options = PubsubPredBqOptions()
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session
    pipeline_options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=pipeline_options) as p:
        _ = (
            p
            | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(topic=pipeline_options.input_topic).with_output_types(bytes)
            | "UTF-8 bytes to string" >> beam.Map(decode)
            | "Parse input" >> beam.Map(lambda msg: json.loads(msg)["instances"])
            | "Make prediction" >> beam.ParDo(ModelInvoker(pipeline_options.model_project,
                                                           pipeline_options.model_location,
                                                           pipeline_options.model_endpoint_id))
            | "Bucketize age" >> beam.Map(classify_age_group)
            | "Write to BigQuery" >> beam.io.WriteToBigQuery(pipeline_options.output_table,
                                                             schema=BQ_SCHEMA,
                                                             create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
