import os
import asyncio
from aws_resources.s3 import S3Buckets
from aws_resources.glue import Glue

async def ingestion_to_source():
    pass

# Upload Glue Jobs Scripts to S3 Bucket to be Accessed by Glue during Job Run
def upload_scripts(folder_name, bucket_name):
    """Uploads all Python script files (.py) from a specified folder to an S3 bucket.

    Args:
        folder_name (str): The name of the local folder containing the scripts.
        bucket_name (str): The name of the S3 bucket to upload the scripts to.

    Returns:
        str: A message indicating successful upload or an error message.

    Raises:
        ValueError: If the provided folder name or bucket name is empty or invalid.
        FileNotFoundError: If the specified folder does not exist.
        Exception: If an unexpected error occurs during the upload process.
        """
    # Make Connection to S3 Resource vis Boto3 for Python SDK
    s3 = S3Buckets.credentials('us-east-2')

    # Go through Files on Local Folder Containing Scripts and Upload files except the Package Constructor
    for file in os.listdir(f'{folder_name}/'):
        if file.endswith(".py") and not file.startswith("__init__"):
            s3.upload_file(file_name=f"{folder_name}/{file}", bucket_name=bucket_name, object_name=f"{folder_name}/{file}")

    # Return a Success Message if Successful
    return f"The files in {folder_name} have been uploaded to the bucket: {bucket_name}"

def remove_scripts(folder_name, bucket_name):
    s3 = S3Buckets.credentials('us-east-2')
    for file in os.listdir(f'{folder_name}/'):
        if file.endswith(".py"):
            s3.delete_file(bucket_name=bucket_name, file_name=f"{folder_name}/{file}")

    return f"The files in {folder_name} have been removed from the bucket: {bucket_name}"

# print(upload_scripts("glue_job_scripts/bronze", "tickit-project-bucket"))
#print(remove_scripts("glue_job_scripts", "tickit-project-bucket"))

# glue = Glue.credentials('us-east-2')

# glue.create_job(name="tester-job",
#                 description="Testing glue for the first time",
#                 role_arn="arn:aws:iam::851725307232:role/jibbs-glue-role",
#                 script_location='s3://tickit-project-bucket/glue_job_scripts/bronze_to_silver.py'
#                 )

# glue.delete_job(job_name="tester-job")
