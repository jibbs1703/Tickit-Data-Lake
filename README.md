# Tickit Data Lake : Building a Data Lake Using AWS Resources

Welcome to the Tickit Data Lake project! This repository demonstrates the creation of a robust, 3-tier data lake 
using AWS resources. This pipeline is designed to handle the extraction, loading, and transformation of batch data.
This pipeline automates the steps of gathering the data, extracting it, processing it, enriching it, and formatting 
it in a way that can be used by the business in downstream tasks and applications.

## Project Overview

The data pipeline collects, transforms, and stores raw data files into formats tailored for business unit needs. 
This pipeline can be modified to source data from various external inputs including API endpoints, flat files, 
application logs, databases, and mobile applications. The steps in the pipeline can be performed using either 
the Python shell or Pyspark jobs. 

In this project, raw, untransformed data resides in external databases and is initially extracted as .csv files 
into a bronze tier S3 bucket. The pipeline works on the raw data, processing it, and subsequently storing it in
the appropriate data lake tier as determined by business requirements. The tiers are represented as folders within
a single S3 bucket for this project. However, each tier should be given a dedicated bucket (as it is in production
environments).

An orchestrator triggers the extraction of the ingested raw and untransformed data into the bronze tier S3 where 
it is then moved on to the other tiers, getting enriched as it gets refined up the data lake tiers.

An understanding of creating and assigning IAM roles is required as the AWS resources used are configured in such
a way to interact with one another, i.e., a role that grants permission to let AWS Glue access the resources it needs.
The degree of restrictions can be narrowed down based on the level of security needed. For this pipeline, I assigned 
an IAM role to access AWS Glue resources and read/write to AWS S3 and Redshift.

## Medallion Architecture

The data lake tiers are inspired by the medallion architecture concept from Databricks, this project features the 
three distinct data tiers:

- Bronze: Raw, unprocessed data

- Silver: Validated, cleaned data

- Gold: Enriched, business-ready data

Each tier houses its own schemas and tables, which differ based on data update frequencies and downstream use cases. 
This multi-layered approach ensures data integrity and optimizes its use for business needs.


## Pipeline Steps

### Ingesting the Data From Source

The first step in establishing the three distinct data tiers is to have a data source. In production, the raw data is 
usually stored across several sources and pulled into a landing area where the data pipeline kicks off. For example,
the raw data could be stored in a postgresql database, mysql database, mssql database and a NoSQL database 
like mongodb. In this case, four separate glue crawlers would be needed to catalog each data source. 

For this project, all source tables are housed in the same database and are extracted into a source S3 bucket. This 
implies that just one glue crawler is needed to catalog all tables from the data source. The source S3 bucket serves
as the starting point of the pipeline. The seven tables are crawled and their metadata is saved in the glue data 
catalog. 


### Creating the Bronze Data Tier

The bronze data tier is simply the raw data ingestion layer of the medallion architecture. There is no data cleanup 
or validation performed in this layer. The process here is simply an Extraction-Load process with no transformation 
performed. For this project, all seven tables are simply moved from the data landing bucket that houses all source 
data, into the bronze layer, in a separate bucket (usually more secure with more access restrictions compared to the 
source bucket).


### Creating the Silver Data Tier

The silver data tier takes the data a step further in its refinement as the data passes through extensive cleanup and
validation. The silver tier sees the datatype standardization, filling and/or removal of null values, creation of 
desirable datatypes, detection and removal of duplicates, and to a certain degree, some data aggregation as some facts
and dimension tables could be merged in the silver tier to allow downstream users utilize the data. 


