"""Example code for running a built pipeline."""
import google.cloud.aiplatform as aip
import argparse

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
    "--bucket",
    help="the bucket to use for staging files",
    type=str,
)
parser.add_argument(
    "--service-account",
    help="the service account used to run the pipeline",
    type=str,
)
parser.add_argument(
    "--pipeline-name",
    help="the name of the pipeline",
    type=str,
    default="kfp-black-friday-demo",
)

pipeline_version = "latest"
args = parser.parse_args()

aip.init(project=args.project, staging_bucket=args.bucket)

display_name = args.pipeline_name
pipeline_root = "gs://{}/{}".format(args.bucket, args.pipeline_name)

job = aip.PipelineJob(
    display_name=display_name,
    template_path=f"https://europe-west1-kfp.pkg.dev/{args.project}/pipeline-templates/{args.pipeline_name}/{pipeline_version}",
    pipeline_root=pipeline_root,
    project=args.project,
    location=args.region,
    parameter_values={
        "location": args.region,
        "project": args.project,
        "training_data_path": args.training_data_uri,
    },
)

job.submit(service_account=args.service_account)
