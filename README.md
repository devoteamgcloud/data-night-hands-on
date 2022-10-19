# Data Night

Welcome to the data night!

In this repository, you will find the code for two sessions:

## Building an ML model using Vertex AI pipelines
In this session we will develop and deploy a Vertex AI Pipeline that will train a regression model using AutoML.
You can find this code in the kfp_vertex_ai_pipeline_example folder.

## Building a Datflow pipeline for ML Inference
In this session we will develop and depoy a Dataflow pipeline that will call the model we just built to perform
ML inference. You can find the code in the dataflow_streaming_pipeline folder.

## Get all the code and packages in Cloud Shell Editor
Both sessions will use the Cloud Shell Editor to adapt, build and deploy code.

To start, please go to console.cloud.google.com, select the project "Devoteam G Cloud Data Night" with ID "dt-dn-<first_part_your_email>" in the dropdown 
right next to the "Google Cloud" logo, which you can find in the top left corner of the screen.

When the project is selected please search for 'Cloud Shell Editor' in the searchbar and go to this service.
You should now see a blank page with on the left side some files and folders.

Go to 'Terminal' on the top left of the screen and press 'New Terminal' to open a new terminal, so you can get all the 
required code for both sessions.

Run the command "git clone https://github.com/devoteamgcloud/data-night-hands-on" to get the code in your cloud editor.
You should now see a folder called "data-night-hands-on" which contains the code.

When you have the code, please run "pip install -r ./data-night-hands-on/requirements_cloud_shell.txt" to install all 
the required packages in your cloud shell instance.

You are now ready to start coding, good luck!


