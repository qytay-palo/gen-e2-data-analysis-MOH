# SQL Scripts and Queries

This directory contains SQL scripts for data extraction, views, and stored procedures.

## Directory Structure

### `/views/`
Reusable SQL views for common queries and analytics.

**Purpose**:
- Create abstraction layers for complex joins
- Standardize metrics calculations
- Simplify analyst queries

**Examples**:
- `patient_visit_summary.sql` - Aggregated patient visit metrics
- `chronic_disease_prevalence.sql` - Disease prevalence calculations
- `regional_capacity_metrics.sql` - Polyclinic capacity and utilization

### `/procedures/`
Stored procedures for data processing and transformations.

**Purpose**:
- Encapsulate complex ETL logic
- Reusable data quality checks
- Performance optimization

**Examples**:
- `sp_validate_attendance_data.sql` - Data validation procedures
- `sp_calculate_patient_metrics.sql` - Patient metric aggregations
- `sp_refresh_materialized_views.sql` - View refresh procedures

### `/extractions/`
Data extraction queries for initial data loads and incremental updates.

**Purpose**:
- Extract data from source systems
- Incremental extraction logic
- Full refresh queries

**Examples**:
- `extract_attendances_incremental.sql` - Daily attendance extractions
- `extract_diagnosis_full.sql` - Full diagnosis data load
- `extract_patient_demographics.sql` - Patient profile extraction

## Usage Guidelines

### Query Organization
- Name files descriptively: `{purpose}_{entity}_{type}.sql`
- Include header comments with purpose, author, date
- Document expected parameters and outputs

### Best Practices
1. **Parameterization**: Use parameter placeholders for dates, IDs
2. **Performance**: Include execution plans and optimization notes
3. **Testing**: Test on sample data before production
4. **Version Control**: Commit all SQL changes with descriptive messages

### Example Header Template
```sql
/*
 * File: extract_attendances_incremental.sql
 * Purpose: Extract polyclinic attendance records for specified date range
 * Author: Data Engineering Team
 * Created: 2026-01-30
 * Modified: 2026-01-30
 * 
 * Parameters:
 *   - {start_date}: Start date for extraction (YYYY-MM-DD)
 *   - {end_date}: End date for extraction (YYYY-MM-DD)
 *   - {batch_size}: Number of records per batch
 * 
 * Output: Attendance records with associated patient and facility info
 * 
 * Dependencies: POLYCLINIC_ATTENDANCES, PATIENT_DEMOGRAPHICS, POLYCLINIC_MASTER
 * 
 * Notes:
 *   - Run daily at 02:00 UTC+8
 *   - Incremental extraction based on attendance_date
 */
```

## Platform-Specific Notes

### For HEALIX (Databricks)
- Use **Databricks SQL** or **Spark SQL** syntax
- Leverage Delta Lake features (MERGE, time travel)
- Store views in Unity Catalog when available

### For MCDR (HUE/Hive)
- Use **HiveQL** syntax
- Consider partitioning for performance
- Store in HDFS with appropriate permissions

## Related Documentation
- [Query Templates](../../config/queries.yml) - Parameterized query templates
- [Data Sources](../../docs/project_context/data_sources.md) - Table schemas and relationships
- [ETL Pipeline](../../src/data_processing/etl_pipeline.py) - Python-based extraction logic
