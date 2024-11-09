import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
logger = glueContext.get_logger()

job = Job(glueContext)
job.init(args['JOB_NAME'], args)


df = spark.read.option("header","true").csv("s3://tickit-project-bucket/bronze/category.csv")

# Writing output to target S3 bucket. Please update the Target S3 bucket name.
df.write.json("s3://tickit-project-bucket/silver/")

job.commit()