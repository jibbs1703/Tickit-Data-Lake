import configparser
import sqlite3
import pandas as pd
from aws_resources.s3 import S3Buckets

# Connect to Config File to Access Needed Variables
config = configparser.ConfigParser()
config.read('../config.ini')

def extract_venue(db_path=config['DATABASE']['PATH'], table_name=None):
    # Connect to the SQLite database
    connection = sqlite3.connect(db_path)

    # Create a cursor to execute SQL commands
    cursor = connection.cursor()

    # Execute Query to Extract All Rows from Venue Table
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)

    # Extract Query Results into Pandas DataFrame
    df = pd.read_sql_query(query, connection)

    # Connect to AWS S3 and upload Extracted Dataframe as CSV file
    s3_conn = S3Buckets.credentials(config['AWS_ACCESS']['REGION'])
    s3_conn.upload_dataframe_to_s3(df = df,
                                   bucket_name=config['AWS_ACCESS']['PROJECT_BUCKET'],
                                   object_name=f'source/{table_name}.csv')

    return f'The {table_name} table was uploaded to the S3 Bucket'

print(extract_venue(table_name='listing'))