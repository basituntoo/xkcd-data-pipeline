# xkcd-data-pipeline
#XKCD Data Pipeline – Data Engineering Case Study
##📌 Project Overview

This project implements an end-to-end data pipeline for ingesting, transforming, and modeling XKCD comics data.

###The pipeline:

Fetches comics from the XKCD public API

Loads them into a PostgreSQL database (Neon)

Transforms raw data into analytics-ready dimensional models

Supports automation via Airflow and dbt

The solution is designed with simplicity, reliability, and interview clarity in mind rather than production-grade complexity.

🏗 ###Architecture Overview

High-level flow:
XKCD API
   ↓
Python Ingestion Script
   ↓
PostgreSQL (Neon)
   ↓
dbt Transformations
   ↓
Dim / Fact Tables (Analytics Ready)


Automation is handled using:

Airflow → orchestration & scheduling

dbt → transformations & data quality checks

##Part 1: Extract & Load
What was built

A Python ingestion script that:

Fetches XKCD comics using the official API

Implements polling logic to detect new comics

Inserts data into PostgreSQL

Avoids duplicate inserts using ON CONFLICT DO NOTHING

Resumes automatically if interrupted

###Key files
ingestion/
└── fetch_xkcd.py

###Tables created

xkcd_raw – raw comic data

ingestion_state – tracks last successfully ingested comic ID

###Scheduling

Comics are published Mondays, Wednesdays, Fridays

Polling logic ensures comics are ingested as soon as available

🔄## Part 2: Transform
###Business requirements implemented
Metric	Logic
Cost	number_of_letters_in_title × 5 EUR
Views	random number between 0 and 1 × 10,000
Reviews	random score between 1.0 and 10.0

###Data Warehouse Model (Kimball Style)
####Dimension table

dim_comic

comic_id (PK)

title

publish_date

img_url

alt_text

####Fact table

fact_comic_metrics

comic_id (FK)

views

cost_eur

review_score

snapshot_date

This model supports easy aggregation and BI analysis.

###✅ Data Quality Checks

Implemented via dbt tests:

Primary key uniqueness

Non-null constraints

Referential integrity between fact and dimension tables

Valid numeric ranges for:

views

review_score

##⚙️ Automation
###Airflow

DAG scheduled for Mon/Wed/Fri

Tasks:

Poll XKCD API

Run ingestion script (fetch_xkcd.py)

DAG provided as production-ready code (not executed locally)
airflow/dags/xkcd_ingestion_dag.py

###dbt

Used for transformation layer

Generates:

dim_comic

fact_comic_metrics

Includes automated tests
dbt/
├── models/
├── tests/
└── dbt_project.yml

##How to Run Locally
###1. Run ingestion manually
dbt run
dbt test

##Requirements Coverage
Requirement	Status
Fetch XKCD data	✅
Insert into DB	✅
Polling logic	✅
Dimensional model	✅
Views / Cost / Reviews	✅
Data quality checks	✅
dbt transformations	✅
Airflow DAG	✅ (bonus)
Automated scheduling	✅ (design)