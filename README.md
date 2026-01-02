# XKCD Data Pipeline  
### Data Engineering Case Study

---

## 📌 Project Overview

This project implements an **end-to-end data pipeline** for ingesting, transforming, and modeling **XKCD comics data**.

### The pipeline:
- Fetches comics from the XKCD public API  
- Loads data into a PostgreSQL database (Neon)  
- Transforms raw data into analytics-ready dimensional models  
- Supports automation using **Airflow** and **dbt**

The solution is intentionally designed to be **clear, reliable, and interview-friendly**, rather than production-grade complex.

---

##  Architecture Overview

**High-level data flow:**

XKCD API
↓
Python Ingestion Script
↓
PostgreSQL (Neon)
↓
dbt Transformations
↓
Dim / Fact Tables (Analytics Ready)


### Automation tools used:
- **Airflow** → orchestration & scheduling  
- **dbt** → transformations & data quality checks  

---

##  Part 1: Extract & Load

### What Was Built

A Python ingestion script that:
- Fetches comics using the official XKCD API  
- Implements polling logic to detect newly published comics  
- Inserts data into PostgreSQL  
- Prevents duplicate inserts using `ON CONFLICT DO NOTHING`  
- Automatically resumes from the last successfully ingested comic  

---

### Key Files

ingestion/
└── fetch_xkcd.py


---

### Tables Created

- **xkcd_raw** – stores raw comic data  
- **ingestion_state** – tracks the last successfully ingested comic ID  

---

### Scheduling Logic

- XKCD publishes comics on **Mondays, Wednesdays, and Fridays**
- Polling logic ensures comics are ingested **as soon as they become available**

---

##  Part 2: Transform

### Business Requirements Implemented

| Metric | Logic |
|------|------|
| Cost | Number of letters in title × 5 EUR |
| Views | Random number between 0 and 1 × 10,000 |
| Reviews | Random score between 1.0 and 10.0 |

---

##  Data Warehouse Model (Kimball Style)

### Dimension Table: `dim_comic`

- `comic_id` (Primary Key)  
- `title`  
- `publish_date`  
- `img_url`  
- `alt_text`  

---

### Fact Table: `fact_comic_metrics`

- `comic_id` (Foreign Key)  
- `views`  
- `cost_eur`  
- `review_score`  
- `snapshot_date`  

This model supports efficient aggregation and BI-friendly analysis.

---

##  Data Quality Checks

Implemented using **dbt tests**:
- Primary key uniqueness  
- Non-null constraints  
- Referential integrity between fact and dimension tables  
- Valid numeric ranges for:
  - `views`
  - `review_score`

---

## ⚙️ Automation

### Airflow

- DAG scheduled for **Monday / Wednesday / Friday**
- Tasks:
  - Poll XKCD API
  - Execute ingestion script (`fetch_xkcd.py`)
- DAG provided as production-ready code (not executed locally)

airflow/dags/xkcd_ingestion_dag.py

---

### dbt

- Used as the transformation layer
- Generates:
  - `dim_comic`
  - `fact_comic_metrics`
- Includes automated data quality tests

dbt/
├── models/
├── tests/
└── dbt_project.yml


---

##  How to Run Locally

### 1. Run ingestion manually
```bash
python ingestion/fetch_xkcd.py

2. Run transformations and tests
dbt run
dbt test

---
| Requirement                    | Status     |
| ------------------------------ | ---------- |
| Fetch XKCD data                | ✓          |
| Insert into database           | ✓          |
| Polling logic                  | ✓          |
| Dimensional model              | ✓          |
| Views / Cost / Reviews metrics | ✓          |
| Data quality checks            | ✓          |
| dbt transformations            | ✓          |
| Airflow DAG                    | ✓ (bonus)  |
| Automated scheduling           | ✓ (design) |
