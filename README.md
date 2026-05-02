# Vehicle Engine Data Pipeline — AWS Data Engineering Project

## Project Overview
An end-to-end data pipeline that ingests raw vehicle engine data, cleans and transforms it using AWS Glue and PySpark, stores it as Parquet in S3, and serves analytics queries via Amazon Athena.

**Dataset:** 1,737 vehicle engine records across 15+ manufacturers  
**Built by:** Aditya Rawat | [LinkedIn](https://linkedin.com/in/aditya-rawat-b6635521a) | [GitHub](https://github.com/AdityaUK01)

---

## Architecture
Excel File (local)
↓
generate_bronze.py (Python)
↓
S3 bronze/ (raw CSV)
↓
AWS Glue ETL Job (PySpark)
↓
S3 silver/ (clean Parquet)
↓
Amazon Athena (SQL analytics)

---

## Tech Stack
- Python 3, Pandas
- AWS S3, AWS Glue 5.1 (PySpark), Amazon Athena, IAM

---

## Key Results

| Manufacturer | Engine Models |
|---|---|
| Toyota | 157 |
| Ford | 102 |
| Nissan | 98 |

| Fuel Type | Avg Power (hp) |
|---|---|
| 98-octane petrol | 252 |
| Petrol | 184 |
| Diesel | 140 |

---

## How to Run
1. `pip install pandas openpyxl`
2. `python generate_bronze.py`
3. Upload CSV to S3 bronze/
4. Run Glue job with glue_etl.py
5. Query in Athena

## Status
- [x] S3 bronze/silver/gold layers
- [x] Glue ETL job
- [x] Athena analytics
- [ ] Lambda trigger
- [ ] CloudWatch monitoring