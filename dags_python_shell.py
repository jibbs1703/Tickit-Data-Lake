import configparser
import sqlite3
import pandas as pd
from aws_resources.s3 import S3Buckets

# Connect to Config File to Access Needed Environment Variables
config = configparser.ConfigParser()
config.read('config.ini')

# Extract tables from Source to Bronze Bucket
def extract_to_source(db_path=config['DATABASE']['PATH'],
                     tables=eval(config.get('DATABASE', 'TABLES'))):

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
                                       object_name=f'source/{table}.csv')
        print(f"The {table} table was uploaded")

    return f'The tables were was uploaded to the S3 Bucket'


# Extraction to Bronze Tier from Source
def extract_category_to_bronze(table='category'):

    # Connect to AWS S3 and upload Extracted Dataframe as CSV file
    s3_conn = S3Buckets.credentials(config['AWS_ACCESS']['REGION'])
    s3_conn.upload_dataframe_to_s3(df=df,
                                   bucket_name=config['AWS_ACCESS']['PROJECT_BUCKET'],
                                   object_name=f'source/{table}.csv')
    print(f"The {table} table was uploaded")
    pass

def extract_date_to_bronze():
    pass

def extract_event_to_bronze():
    pass

def extract_listing_to_bronze():
    pass

def extract_sale_to_bronze():
    pass

def extract_user_to_bronze():
    pass

def extract_venue_to_bronze():
    pass




def transform_to_silver_tier():
    pass

def transform_cat_eve_ven():
    pass

def transform_date_list_sales():
    pass

def transform_date_list_users():
    pass