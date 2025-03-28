import datetime
import logging

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient

app = func.FunctionApp()

def upload_blob_data(blob_service_client: BlobServiceClient, container_name: str):

     time_now  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 
     blob_client = blob_service_client.get_blob_client(container=container_name, blob=f"{time_now}.txt")
     data = b"Sample data for blob"

     # Upload the blob data - default blob type is BlockBlob    
     blob_client.upload_blob(data, blob_type="BlockBlob")

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:

     account_url = "https://kprg950f.blob.core.windows.net"
     credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
     blob_service_client = BlobServiceClient(account_url, credential=credential)
     upload_blob_data(blob_service_client, "container1")
     logging.info('Python timer trigger function executed.')
