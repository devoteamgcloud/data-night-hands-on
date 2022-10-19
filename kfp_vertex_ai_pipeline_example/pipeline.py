"""Creates example pipeline for regression training using AutoML."""
import kfp
import argparse

from kfp.registry import RegistryClient
from kfp.v2 import compiler
from google_cloud_pipeline_components import aiplatform as gcc_aip

parser = argparse.ArgumentParser()
parser.add_argument(
    "--project",
    help="the project ID",
    type=str,
)
parser.add_argument(
    "--region",
    help="the region to deploy everything in",
    type=str,
    default="us-central1",
)
parser.add_argument(
    "--training-data-uri",
    help="the GCS uri of the training data",
    type=str,
)
parser.add_argument(
    "--output-prefix",
    help="the output prefix",
    type=str,
)
parser.add_argument(
    "--pipeline-name",
    help="the name of the pipeline",
    type=str,
    default="kfp-black-friday-demo",
)
parser.add_argument(
    "--pipeline-file",
    help="the location to write the pipeline JSON to",
    type=str,
    default="pipeline.json",
)
parser.add_argument("-t", "--tags", nargs="*", help="Extra tags to set on the image.")

args = parser.parse_args()

automl_location = "us-central1"
if args.region.startswith("eu"):
    automl_location = "eu"


@kfp.dsl.pipeline(name=args.pipeline_name)
def pipeline(
    project: str = args.project,
    location: str = automl_location,
    training_data_path: str = args.training_data_uri,
):
    """
    Create pipeline for training using AutoML.

    :param project: project ID of project
    :param location: desired region
    :param training_data_path: the path to the training data on GCS
    """
    dataset_create_op = gcc_aip.TabularDatasetCreateOp(
        project=project,
        display_name=args.pipeline_name,
        location=location,
        gcs_source=training_data_path,
        labels={"environment": "dev"},
    )

    # TODO: fill in the column_spec
    #
    # The column spec will tell our AutoML model which input columns to use.
    # You can decide for yourself which columns to use, but at the very least is should include
    # the Purchase column and one other
    # column_spec = {
    #     "COLUMN_NAME": "categorical/numeric",
    #     "Purchase": "numeric",
    # }

    # TODO: change
    column_spec = {
        "Purchase": "numeric",
    }

    training_op = gcc_aip.AutoMLTabularTrainingJobRunOp(
        project=project,
        display_name=args.pipeline_name,
        optimization_prediction_type="regression",
        optimization_objective="minimize-rmse",
        column_specs=column_spec,
        dataset=dataset_create_op.outputs["dataset"],
        target_column="Purchase",
        location=location,
        budget_milli_node_hours=1000,
        labels={"environment": "dev"},
        model_labels={"environment": "dev"},
        disable_early_stopping=False,
        export_evaluated_data_items=False,
        export_evaluated_data_items_override_destination=False,
    )

    endpoint_op = gcc_aip.EndpointCreateOp(
        project=project,
        location=location,
        display_name=args.pipeline_name,
    )

    gcc_aip.ModelDeployOp(
        model=training_op.outputs["model"],
        endpoint=endpoint_op.outputs["endpoint"],
        dedicated_resources_machine_type="n1-standard-4",
        dedicated_resources_min_replica_count=1,
        dedicated_resources_max_replica_count=1,
    )


# Compile the pipeline to YAML format
compiler.Compiler().compile(
    pipeline_func=pipeline,
    package_path=args.pipeline_file,
)

# Push the template to artifact registry
client = RegistryClient(
    host=f"https://europe-west1-kfp.pkg.dev/{args.project}/pipeline-templates"
)
templateName, versionName = client.upload_pipeline(
    file_name=args.pipeline_file,
    tags=["v1", "latest"] + [t.replace("/", "-").replace("_", "-") for t in args.tags],
    extra_headers={"description": "Basic vertex AI regression pipeline template."},
)
