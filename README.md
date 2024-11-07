# Tickit Data Lake : Building a Data Lake Using AWS Resources

Welcome to the Tickit Data Lake project! This repository demonstrates the creation of a robust, 3-tier data lake 
using AWS resources. This pipeline is designed to handle the extraction, loading, and transformation of batch data. 

## Project Overview

The data pipeline collects, transforms, and stores raw data files into formats tailored for business unit needs. 
This pipeline can be modified to source data from various external inputs including API endpoints, flat files, 
application logs, databases, and mobile applications. 

In this project, raw, untransformed data resides in external databases and is initially extracted as .csv files 
into a bronze tier S3 bucket. The pipeline works on the raw data, processing it, and subsequently storing it in
 the appropriate data lake tier as determined by business requirements.

An orchestrator triggers the extraction of the raw and untransformed data into the bronze tier S3 where it is 
then moved on to the other tiers, getting enriched as it gets refined up the data lake tiers.

An understanding of creating and assigning IAM roles is required as the AWS resources used are configured in such
a way to interact with one another, i.e., a role that grants permission to let AWS Glue access the resources it needs.
The degree of restrictions can be narrowed down based on the level of securityneeded. For this pipeline, I assigned 
an IAM role to access AWS Glue resources and read/write to a specified S3 bucket. 

## Medallion Architecture

The data lake tiers are inspired by the medallion architecture concept from Databricks, this project features the 
three distinct data tiers:

- Bronze: Raw, unprocessed data

- Silver: Validated, cleaned data

- Gold: Enriched, business-ready data

Each tier houses its own schemas and tables, which differ based on data update frequencies and downstream use cases. 
This multi-layered approach ensures data integrity and optimizes its use for business needs.