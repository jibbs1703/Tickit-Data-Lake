import os
import configparser
import sqlite3
import pandas as pd
from aws_resources.s3 import S3Buckets
from aws_resources.glue import Glue

# Connect to Config File to Access Needed Environment Variables
config = configparser.ConfigParser()
config.read('config.ini')

def extract_tables(db_path=config['DATABASE']['PATH'],
                     tables =eval(config.get('DATABASE', 'TABLES'))):

    """ Extracts tables from a SQLite database and uploads them to an S3 bucket as CSV files.
    This function connects to a specified SQLite database, extracts specified tables into
    Pandas DataFrames, and uploads the data as CSV files to an AWS S3 bucket. The function uses
    an imported S3Buckets class to handle S3 operations.

    :param db_path: Path to the SQLite database file
    :param tables: List of table names to extract from the database
    :return: A success message indicating that the tables were uploaded to the S3 bucket """

    for table in tables:
        # Connect to the SQLite database
        with sqlite3.connect(db_path) as connection:
            # Create a cursor to execute SQL commands
            cursor = connection.cursor()
            # Execute Query to Extract All Rows from Table
            query = f"SELECT * FROM {table}"
            cursor.execute(query)

            # Extract Query Results into Pandas DataFrame
            df = pd.read_sql_query(query, connection)

        # Connect to AWS S3 and upload Extracted Dataframe as CSV file
        s3_conn = S3Buckets.credentials(config['AWS_ACCESS']['REGION'])
        s3_conn.upload_dataframe_to_s3(df = df,
                                       bucket_name=config['AWS_ACCESS']['PROJECT_BUCKET'],
                                       object_name=f'source/source_{table}.csv')
        print(f"The {table} table was uploaded")

    return f'The tables were was uploaded to the S3 Bucket'

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