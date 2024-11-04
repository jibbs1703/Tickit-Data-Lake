# Tickit Data Lake : Building a Data Lake Using AWS Resources

Welcome to the Tickit Data Lake project! This repository demonstrates the creation of a robust, 3-tier data lake 
using AWS resources.

## Project Overview

The data pipeline collects, transforms, and stores raw data files into formats tailored for business unit needs. 
This pipeline can be modified to source data from various external inputs including API endpoints, flat files, 
application logs, databases, and mobile applications. 

In this project, raw, untransformed data resides in external databases and is initially extracted as .csv files 
into a source S3 bucket. The pipeline initiates upon ingestion of this raw data, processing it, and subsequently 
storing it in the appropriate data lake tier as determined by business requirements.

## Medallion Architecture

The data lake tiers are inspired by the medallion architecture concept from Databricks, this project features the 
three distinct data tiers:

- Bronze: Raw, unprocessed data

- Silver: Validated, cleaned data

- Gold: Enriched, business-ready data

Each tier houses its own schemas and tables, which differ based on data update frequencies and downstream use cases. 
This multi-layered approach ensures data integrity and optimizes its use for business needs.