import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from app.main import logger
BUCKET_NAME = os.getenv("BUCKET_NAME") #'terraform-20210416111327492600000001'
# BUCKET_NAME = 'terraform-20210416111327492600000001'

def _get_s3_client():
    return boto3.client(
    "s3",
    config=boto3.session.Config(
        signature_version="s3v4", retries={"max_attempts": 10, "mode": "standard"}
    ),
)

def _get_s3_resource():
    return boto3.resource(
    "s3",
    config=boto3.session.Config(
        signature_version="s3v4", retries={"max_attempts": 10, "mode": "standard"}
    ),
)

def upload_file(file):
    logger.info("File API called")
    object_name = datetime.now().year + "/" + datetime.now().month + "/" + datetime.now().day + "/" + file.filename.replace(" ", "").split('/')[-1]
    # Upload the file
    try:
        s3 = _get_s3_client()
        response = s3.upload_fileobj(file, BUCKET_NAME, object_name)
        return {"status": object_name}, 201
    except ClientError as e:
        logger.error(e)
        return {"status": "Error occurred while uploading file"}, 500
