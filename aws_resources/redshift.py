import os
from dotenv import load_dotenv
import boto3
import logging
from botocore.exceptions import ClientError


# Create Logger
logger = logging.getLogger(__name__)


class Redshift:
    @classmethod
    def credentials(cls, region=None):
        """
        Retrieves the user's AWS credentials from a hidden environment file.

        This class method accesses the user's AWS secret and access keys stored in an environment file. 
        If a region is specified, the AWS Redshift methods are executed within that region. If no region is 
        specified, AWS will default to an available region for service execution.

        :param region: AWS region specified by the user (default is None)
        :return: An instance of the Redshift class initialized with the user's credentials and specified region
        """
        load_dotenv()
        secret = os.getenv("ACCESS_SECRET")
        access = os.getenv("ACCESS_KEY")
        return cls(secret, access, region)

    def __init__(self, secret, access, region):
        """
        Initializes the Redshift class with user credentials and creates the AWS Redshift client.

        This constructor method initializes the Redshift class using the provided secret and access keys.
        It creates an AWS Redshift client using the boto3 library. If no region is specified, AWS assigns
        a region. The created client is available for subsequent methods within the class.

        :param secret: User's AWS secret key loaded from the environment file
        :param access: User's AWS access key loaded from the environment file
        :param region: Specified AWS region during instantiation (default is None)
        """
        if region is None:
            self.client = boto3.client('redshift', aws_access_key_id=access, aws_secret_access_key=secret)
            print(secret, access, region)
        else:
            self.location = {'LocationConstraint': region}
            self.client = boto3.client('redshift', aws_access_key_id=access, aws_secret_access_key=secret,
                                       region_name=region)