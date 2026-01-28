# Story 19: Data Pipeline Infrastructure Setup

## Overview and Statement

Reliable analytics requires robust data infrastructure. This story establishes the foundational data pipeline for incremental extraction, transformation, and loading of polyclinic data from source systems to the analytics platform.

**As a** Data Engineer  
**I want** to build an automated ETL pipeline that incrementally extracts polyclinic data daily  
**So that** analysts have access to fresh, clean data for ongoing analysis

### Acceptance Criteria
- [ ] ETL pipeline extracts data from source tables daily:
  - POLYCLINIC_ATTENDANCES (incremental by attendance_date)
  - PATIENT_DEMOGRAPHICS (incremental by updated_at)
  - DIAGNOSIS_RECORDS, PROCEDURE_RECORDS, MEDICATION_PRESCRIPTIONS
- [ ] Data transformations applied:
  - Data type conversions and formatting
  - Derived features (age from birth_year, day_of_week from attendance_date)
  - Data quality validation checks (Story 01 validations)
- [ ] Processed data stored in structured format (Parquet or Delta Lake)
- [ ] Pipeline orchestration with error handling and retry logic
- [ ] Logging and monitoring of pipeline execution (success/failure, row counts)
- [ ] Documentation of pipeline architecture and data lineage

### Technical Notes
- Use Apache Spark for distributed data processing
- Extract data via HUE/SQL from source database
- Store processed data in HDFS or Databricks Delta Lake
- Orchestrate with Airflow, Databricks Workflows, or cron
- Incremental loading strategy: track last processed date per table
- Platform: Databricks or CDSW with Spark

### Estimated Effort
15-20 days

### Priority
High

## Dependencies
- Access credentials to source database (HUE)
- Target storage location (HDFS or cloud storage)
- Workflow orchestration platform configuration
