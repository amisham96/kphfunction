import logging
import os

import azure.functions as func
from azure.storage.blob import *

app= func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="container1/{name}.txt",
                               connection="AzureWebJobsStorage") 
def BlobTrigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")

    Connectionstring= os.getenv("AzureWebJobsStorage")

    client = BlobServiceClient.from_connection_string(Connectionstring)
    container_client = client.get_container_client("container1")
    blob_client = container_client.get_blob_client(myblob.name)
    blob_client.delete_blob()
    logging.info(f"Blob {myblob.name} deleted successfully")   
