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

    def list_clusters(self):
        """
        Lists redshift clusters in the user's AWS Glue account.

        :return: A list of clusters.
        """
        paginator = self.client.get_paginator("describe_clusters")
        clusters = []
        for page in paginator.paginate():
            clusters.extend(page["Clusters"])

        print(f"{len(clusters)} cluster(s) were found.")

        for cluster in clusters:
            print(f"  {cluster['ClusterIdentifier']}")

    def create_cluster(
        self,
        cluster_identifier,
        node_type,
        master_username,
        master_user_password,
        publicly_accessible,
        number_of_nodes,
    ):
        """
        Creates a cluster.

        :param cluster_identifier: The name of the cluster.
        :param node_type: The type of node in the cluster.
        :param master_username: The master username.
        :param master_user_password: The master user password.
        :param publicly_accessible: Whether the cluster is publicly accessible.
        :param number_of_nodes: The number of nodes in the cluster.
        :return: The cluster.
        """

        try:
            cluster = self.client.create_cluster(
                ClusterIdentifier=cluster_identifier,
                NodeType=node_type,
                MasterUsername=master_username,
                MasterUserPassword=master_user_password,
                PubliclyAccessible=publicly_accessible,
                NumberOfNodes=number_of_nodes,
            )
            return cluster
        except ClientError as err:
            logging.error(
                "Couldn't create a cluster. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def delete_cluster(self, cluster_identifier):
        """
        Deletes a cluster.

        :param cluster_identifier: The cluster identifier.
        """
        try:
            self.client.delete_cluster(
                ClusterIdentifier=cluster_identifier, SkipFinalClusterSnapshot=True
            )
        except ClientError as err:
            logging.error(
                "Couldn't delete a cluster. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def modify_cluster(self, cluster_identifier, preferred_maintenance_window):
        """
        Modifies a cluster.

        :param cluster_identifier: The cluster identifier.
        :param preferred_maintenance_window: The preferred maintenance window.
        """
        try:
            self.client.modify_cluster(
                ClusterIdentifier=cluster_identifier,
                PreferredMaintenanceWindow=preferred_maintenance_window,
            )
        except ClientError as err:
            logging.error(
                "Couldn't modify a cluster. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def describe_clusters(self, cluster_identifier):
        """
        Describes a cluster.

        :param cluster_identifier: The cluster identifier.
        :return: A list of clusters.
        """
        try:
            kwargs = {}
            if cluster_identifier:
                kwargs["ClusterIdentifier"] = cluster_identifier

            paginator = self.client.get_paginator("describe_clusters")
            clusters = []
            for page in paginator.paginate(**kwargs):
                clusters.extend(page["Clusters"])

            return clusters

        except ClientError as err:
            logging.error(
                "Couldn't describe a cluster. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise