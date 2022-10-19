# data-night
## Install pip packages on cloud editor if you have not done this before
pip install -r ./requirements_cloud_shell.txt

## Go into the dataflow folder
cd dataflow_streaming_pipeline

## Upload dataflow template
gsutil cp data-night-template_metadata <change_to_your_own_template_bucket_location e.g. gs://test-apache-beam-data-night/templates/>

## Build pipeline
python streaming_pipeline.py \
  --runner=DataflowRunner \
  --project=<change_to_your_own_project_id> \
  --staging_location=<change_to_your_own_staging_bucket_location e.g. gs://test-apache-beam-data-night/staging> \
  --temp_location=<change_to_your_own_staging_bucket_location e.g. gs://test-apache-beam-data-night/temp> \
  --template_location=<change_to_your_own_template_bucket_location e.g. gs://test-apache-beam-data-night/templates/>/data-night-template \
  --region=europe-west1 \
  --requirements_file=requirements.txt \
  --input_topic=projects/data-night-2022/topics/streaming-data

## Run Pipeline
gcloud dataflow jobs run data-night-test \
  --gcs-location=<change_to_your_own_template_bucket_location e.g. gs://test-apache-beam-data-night/templates/>/data-night-template \
  --staging-location=<change_to_your_own_staging_bucket_location e.g. gs://test-apache-beam-data-night/staging> \
  --region=europe-west1 \
  --project=<change_to_your_own_project_id> \
  --parameters=output_table=data-night-2022:datanight.pred4,model_project=data-night-2022,model_location=us-central1,model_endpoint_id=8730935963145994240