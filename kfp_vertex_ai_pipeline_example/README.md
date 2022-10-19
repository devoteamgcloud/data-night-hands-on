# Kubeflow Pipelines Vertex AI AutoML Example

This folder contains sample code for getting up and running with Vertex AI Pipelines on GCP.
The goal of this pipeline is to build a simple regression model that predicts the amount
a customer will spend on a specific project.

## Dataset info

Data used comes from [Kaggle](https://www.kaggle.com/datasets/sdolezel/black-friday). The columns available are:

**User info**:
* **User_ID**: a numeric ID of the customer
* **Gender**: the gender of the person represented as M or F (only values present in dataset)
* **Age**: the age group of the user as a range, e.g. "26-35"
* **Occupation**: a number indicating the occupation of the user
* **City_Category**: a letter indicating the type of city the user lives in
* **Stay_In_Current_City_Years**: a number indicating the amount of years the user has been living in this city
* **Marital_Status**: a number indicating if a user is married (0 or 1)

**Product info**:
* **Product_ID**: the ID of the product
* **Product_Category_1**: a number representing the top level category of the product (example: 1 could represent "electronics")
* **Product_Category_2**: a number representing the second level category of the product (example: 1 could represent "mobile phones")
* **Product_Category_3**: a number representing the third level category of the product (example: 1 could represent "Samsung S22 Ultra")

Target Column:
* **Purchase**: the amount a user spent on this item. This is what we want to predict

You can find the training data on GCS at:
```
gs://data-night-2022-pipelines-demo/data/black-friday-demo/train.csv
```

## Initial command line setup

### If you are NOT working in Cloud Shell
To make sure you can work with GCP through the command line, you need to have **gcloud** installed.
If you are using the Cloud Shell integrated in GCP, you can skip this step. If you are using your local machine,
installation instructions can be found [here](https://cloud.google.com/sdk/docs/install).

Now authenticate your local CLI with your Google account by running:
```commandline
gcloud auth login
```
And log in with your Google account.

Then to make sure your Python environment can use your Google credentials, you need to run:
```commandline
gcloud auth application-default login
```
And log in with your Google account.

Then make sure to set your project ID to the project that was created for you:
```commandline
gcloud config set project [YOUR_PROJECT_ID]
```

### Inspecting the training dataset
Now that gcloud is set up, we can have a look at our training data:
```commandline
# Copy the training dataset to your local machinge
gsutil -m  cp gs://data-night-2022-pipelines-demo/data/black-friday-demo/train.csv train.csv

# Inspect the training dataset
head train.csv
```
This gives us an idea of what columns we have available in the training dataset and what the data looks like.
Notice that in some cases, Product_Category_2 and Product_Category_3 can be empty.

This training dataset will be reachable from within our Vertex Pipeline, so we can leave it on GCS
where it already is.

## Building the pipeline
The code for this pipeline is built using Kubeflow. The template can be found in **pipeline.py**.
Before working on the code, make sure to install all the requirements.
```commandline
pip install -r requirements.txt
```

Now go into the pipeline.py file and resolve all the TODOs. If you have any questions, please
reach out to the Devoteam people in the room!

Once the TODOs are resolved, you are ready to build your pipeline. You can do this by running the command below:

```commandline
python3 pipeline.py \
      --project [PROJECT_ID] \
      --region us-central1 \
      --training-data-uri gs://data-night-2022-pipelines-demo/data/black-friday-demo/train.csv \
      --pipeline-name kfp-vertex-ai-automl-regression \
      --pipeline-file pipeline.yaml \
      --output-prefix gs://[OUTPUT_BUCKET]/output \
      --tags [YOUR_NAME]
```

You should now be able to find your pipeline on the Artifact Registry of your Google project!
If you want, you can also have a look at the pipeline.yaml file that was created in your local environment.
This means we are ready to run our pipeline. We can do this through the UI or by running the **run_pipeline.py** script.

To run the pipeline, you need to look for the vertex ai service account which should be called:
sa-vertex-pipeline...

```commandline
python3 run_pipeline.py \
      --project [PROJECT_ID] \
      --region us-central1 \
      --training-data-uri gs://data-night-2022-pipelines-demo/data/black-friday-demo/train.csv \
      --pipeline-name kfp-vertex-ai-automl-regression \
      --bucket [OUTPUT_BUCKET] \
      --service-account [SERVICE_ACCOUNT]
```
Congrats your pipeline is now running and your model will be ready in the next hour!
