import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError


class Glue:
    @classmethod
    def credentials(cls, region=None):
        """
        Retrieves the user's AWS credentials from a hidden environment file.

        This class method accesses the user's AWS secret and access keys stored in an environment file. 
        If a region is specified, the AWS Glue methods are executed within that region. If no region is 
        specified, AWS will default to an available region for service execution.

        :param region: AWS region specified by the user (default is None)
        :return: An instance of the Glue class initialized with the user's credentials and specified region
        """
        load_dotenv()
        secret = os.getenv("ACCESS_SECRET")
        access = os.getenv("ACCESS_KEY")
        return cls(secret, access, region)
    
    def __init__(self, secret, access, region):
        """
        Initializes the Glue class with user credentials and creates the AWS Glue client.

        This constructor method initializes the Glue class using the provided secret and access keys. 
        It creates an AWS Glue client using the boto3 library. If no region is specified, AWS assigns 
        a region. The created client is available for subsequent methods within the class.

        :param secret: User's AWS secret key loaded from the environment file
        :param access: User's AWS access key loaded from the environment file
        :param region: Specified AWS region during instantiation (default is None)
        """
        if region is None:
            self.client = boto3.client('glue', aws_access_key_id=access, aws_secret_access_key=secret)
            print(secret, access, region)
        else:
            self.location = {'LocationConstraint': region}
            self.client = boto3.client('glue', aws_access_key_id=access, aws_secret_access_key=secret, region_name=region)

    def list_jobs(self):
        """
        Lists job definitions in the user's AWS Glue account.

        This method retrieves and prints the job definitions from the user's AWS Glue account using 
        the AWS SDK for Python (Boto3). The jobs are listed with a pagination limit of 10 jobs per page.

        :return: None
        """
        try:
            paginator = self.client.get_paginator("get_jobs")
            response_iterator = paginator.paginate(
                PaginationConfig={"MaxItems": 10, "PageSize": 10}
            )

            print("Here are the jobs in your account:")
            for page in response_iterator:
                for job in page["Jobs"]:
                    print(f"\t{job['Name']}")
        except ClientError as e:
            print(f"Error: {e}")
