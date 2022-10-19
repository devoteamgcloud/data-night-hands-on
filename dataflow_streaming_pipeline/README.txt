# data-night
## Install pip packages on cloud editor
pip install -r ./requirements_cloud_shell.txt

## Go into the streaming pipeline folders
cd streaming_pipeline

## Upload dataflow template
gsutil cp data-night-template_metadata gs://test-apache-beam-data-night/templates/

## Build pipeline
python streaming_pipeline.py \
  --runner=DataflowRunner \
  --project=data-night-2022 \
  --staging_location=gs://test-apache-beam-data-night/staging \
  --temp_location=gs://test-apache-beam-data-night/temp \
  --template_location=gs://test-apache-beam-data-night/templates/data-night-template \
  --region=europe-west1 \
  --requirements_file=requirements.txt \
  --input_topic=projects/data-night-2022/topics/streaming-data

## Run Pipeline
gcloud dataflow jobs run data-night-test \
  --gcs-location=gs://test-apache-beam-data-night/templates/data-night-template \
  --staging-location=gs://test-apache-beam-data-night/staging \
  --region=europe-west1 \
  --project=data-night-2022 \
  --parameters=output_table=data-night-2022:datanight.pred4,model_project=data-night-2022,model_location=us-central1,model_endpoint_id=8730935963145994240