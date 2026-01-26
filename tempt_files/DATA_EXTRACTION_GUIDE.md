# Automated Data Extraction System - MOH Polyclinic Data

## Overview

This automated data extraction system is designed to efficiently extract, validate, transform, and load polyclinic data from MOH databases. The system supports incremental extraction, data quality validation, automated scheduling, and comprehensive monitoring.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Configuration Layer                      │
│  - database.yml: DB connections & extraction settings        │
│  - queries.yml: SQL query templates                          │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────┴───────────────────────────────┐
│                                                               │
▼                              ▼                               ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Extract    │───▶│    Validate      │───▶│   Transform      │
│              │    │                  │    │                  │
│ • Batch      │    │ • Row count      │    │ • Deduplicate    │
│ • Increment  │    │ • Null checks    │    │ • Type convert   │
│ • Retry      │    │ • Date ranges    │    │ • Standardize    │
│              │    │ • Duplicates     │    │                  │
└──────────────┘    └──────────────────┘    └──────────────────┘
                                                       │
                                                       ▼
                                            ┌──────────────────┐
                                            │      Load        │
                                            │                  │
                                            │ • Parquet        │
                                            │ • CSV            │
                                            │ • Partitioning   │
                                            └──────────────────┘
                                                       │
┌─────────────────────────────────────────────────────┴───────┐
│                                                               │
▼                              ▼                               ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Logging    │    │   Monitoring     │    │   Alerting       │
│              │    │                  │    │                  │
│ • Extraction │    │ • Performance    │    │ • Failures       │
│ • Errors     │    │ • Memory         │    │ • Quality issues │
│ • Audit      │    │ • Duration       │    │ • Email/Slack    │
└──────────────┘    └──────────────────┘    └──────────────────┘
```

## Features

### 1. **Multi-Database Support**
- PostgreSQL, MySQL, MS SQL Server, Oracle
- Connection pooling for efficiency
- Secure credential management via environment variables
- Read-only mode for sensitive databases (e.g., NEHR)

### 2. **Intelligent Data Extraction**
- **Incremental Extraction**: Extract only new/updated records
- **Batch Processing**: Handle large datasets efficiently
- **Checkpoint Management**: Resume from last successful extraction
- **Retry Logic**: Automatic retry on transient failures
- **Query Templates**: Reusable, parameterized SQL queries

### 3. **Comprehensive Data Validation**
- Row count validation
- Null value detection in critical columns
- Date range validation
- Duplicate detection
- Referential integrity checks
- Data type validation
- Value range validation

### 4. **Automated Pipeline Orchestration**
- Complete ETL workflow automation
- Phase-by-phase execution with logging
- Configurable stop-on-failure behavior
- Execution summaries with metrics

### 5. **Scheduling & Automation**
- **Daily**: Incremental extraction of transactional data
- **Weekly**: Full extraction for comprehensive refresh
- **Monthly**: Reference data updates
- **Custom**: Define your own schedules
- Background execution with process monitoring

### 6. **Logging & Monitoring**
- Multi-level logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Separate log files for extraction, errors, and audit
- Log rotation with configurable size limits
- Structured JSON logging for audit trail
- Performance metrics tracking (duration, memory, CPU)
- Alert system for failures and quality issues

## Installation

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Required system packages (Ubuntu/Debian)
sudo apt-get install python3-dev libpq-dev

# Required system packages (macOS)
brew install postgresql
```

### Python Dependencies

```bash
# Install required packages
pip install pandas pyarrow pyyaml psycopg2-binary pymysql pyodbc cx_Oracle schedule psutil

# Or use requirements file
pip install -r requirements.txt
```

### Configuration Setup

1. **Copy environment template**:
```bash
cp .env.example .env
```

2. **Configure database credentials** in `.env`:
```bash
# Primary database
DB_HOST=your-db-host
DB_PORT=5432
DB_NAME=polyclinic_db
DB_SCHEMA=public
DB_USER=your-username
DB_PASSWORD=your-password

# NEHR database
NEHR_HOST=nehr-host
NEHR_PORT=5432
NEHR_DB=nehr_db
NEHR_USER=nehr-user
NEHR_PASSWORD=nehr-password
```

3. **Review and customize** `config/database.yml` and `config/queries.yml`

## Usage

### Method 1: Manual Extraction (Command Line)

Run immediate extraction with command-line options:

```bash
# Extract all sources (incremental mode)
python scripts/run_extraction.py --sources all --incremental

# Extract specific sources
python scripts/run_extraction.py --sources attendances diagnoses patients

# Extract last 7 days of data
python scripts/run_extraction.py --sources all --last-n-days 7

# Extract with custom date range
python scripts/run_extraction.py \
  --sources attendances \
  --start-date 2025-01-01 \
  --end-date 2025-01-31

# Full extraction (not incremental)
python scripts/run_extraction.py --sources all --full

# Stop on validation failure
python scripts/run_extraction.py --sources all --stop-on-validation-failure

# Debug mode
python scripts/run_extraction.py --sources patients --log-level DEBUG
```

### Method 2: Automated Scheduling

Start the scheduler for automated runs:

```bash
# Start scheduler (runs in foreground)
python scripts/run_scheduler.py

# Run in background (Linux/macOS)
nohup python scripts/run_scheduler.py &

# As a systemd service (recommended for production)
sudo systemctl start moh-extraction-scheduler
```

### Method 3: Python API

Use the Python API in your own scripts:

```python
from src.data_processing.etl_pipeline import ETLPipeline
from src.utils.logging_config import setup_logging

# Setup logging
setup_logging(log_level='INFO')

# Initialize pipeline
pipeline = ETLPipeline()

# Run full pipeline
result = pipeline.run_full_pipeline(
    sources=['attendances', 'diagnoses'],
    start_date='2025-01-01',
    end_date='2025-01-31',
    incremental=True
)

print(f"Status: {result['status']}")
print(f"Rows extracted: {result['total_rows_extracted']}")
```

## Configuration Reference

### Database Configuration (`config/database.yml`)

Key sections:
- **databases**: Define database connections
- **extraction**: Batch sizes, retry logic, timeouts
- **data_sources**: Table mappings and extraction modes
- **output**: File formats, paths, naming conventions
- **quality_checks**: Validation rules and thresholds
- **schedule**: Automated job schedules
- **logging**: Log levels and file locations
- **monitoring**: Alert conditions and notifications

### Query Templates (`config/queries.yml`)

Structure:
- **queries**: SQL templates for data extraction
  - `incremental_query`: For incremental extraction
  - `full_query`: For full extraction
  - `query`: For reference data
- **validation**: Data quality validation queries

### Customization

#### Add New Data Source

1. Add to `config/database.yml`:
```yaml
data_sources:
  my_new_source:
    table: my_table
    primary_key: id
    date_column: created_at
    incremental: true
```

2. Add query to `config/queries.yml`:
```yaml
queries:
  my_new_source:
    description: "Extract my new data"
    incremental_query: |
      SELECT * FROM my_table
      WHERE created_at >= '{start_date}'
        AND created_at < '{end_date}'
      LIMIT {batch_size} OFFSET {batch_offset}
```

#### Customize Schedule

Modify `config/database.yml`:
```yaml
schedule:
  daily:
    enabled: true
    time: "03:00"  # Run at 3 AM
    extractions:
      - attendances
      - diagnoses
```

## Output Structure

Extracted data is saved with the following structure:

```
data/
├── raw/                    # Raw extracted data
│   ├── attendances_20260126_143052.parquet
│   ├── diagnoses_20260126_143102.parquet
│   └── ...
├── processed/             # Cleaned and transformed data
│   ├── attendances_20260126_143105.parquet
│   └── ...
└── interim/               # Intermediate processing outputs
    └── extraction_checkpoint.json

results/
├── metrics/               # Performance and execution metrics
│   ├── etl_summary_20260126_143052.json
│   └── performance_20260126_143052.json
└── exports/              # Analysis-ready exports

logs/
├── extraction.log        # Main extraction log
├── errors.log           # Error log
└── audit.log            # Structured audit trail
```

## Monitoring & Alerts

### Log Files

- **extraction.log**: All extraction activities (INFO and above)
- **errors.log**: Errors and critical issues only
- **audit.log**: Structured JSON logs for compliance and auditing

### Metrics

Each pipeline run generates:
- Execution summary (JSON)
- Performance metrics (duration, memory, CPU)
- Validation results per source
- Row counts and data quality indicators

### Alerts

Configured alerts trigger on:
- Extraction failures
- Data quality check failures
- Row count deviations from historical averages
- Critical validation failures

Notification channels (configure in `config/database.yml`):
- Email
- Slack
- Microsoft Teams

## Troubleshooting

### Common Issues

**1. Connection Errors**
```bash
# Test database connection
python -c "from src.data_processing.db_connector import DatabaseConnector; \
  dc = DatabaseConnector(); print(dc.test_connection())"
```

**2. Memory Issues**
- Reduce `batch_size` in `config/database.yml`
- Increase `max_memory_mb` limit
- Process fewer sources concurrently

**3. Slow Extraction**
- Check database query performance
- Increase `batch_size` for better throughput
- Add database indexes on date columns
- Use `max_workers` for parallel processing

**4. Validation Failures**
- Review validation results in logs
- Adjust thresholds in `quality_checks` section
- Use `--stop-on-validation-failure=false` to continue

### Debug Mode

Run with verbose logging:
```bash
python scripts/run_extraction.py --sources all --log-level DEBUG
```

### Check Extraction Status

```python
from src.data_processing.data_extractor import DataExtractor

extractor = DataExtractor()
stats = extractor.get_extraction_stats('attendances')
print(f"Last extraction: {stats['last_extraction_date']}")
```

## Best Practices

1. **Start Small**: Test with one source before running full extraction
2. **Monitor First Runs**: Watch logs during initial executions
3. **Validate Data**: Always review validation results
4. **Incremental Mode**: Use incremental extraction for daily updates
5. **Schedule Off-Peak**: Run large extractions during low-usage periods
6. **Backup Configuration**: Keep versioned copies of config files
7. **Review Logs**: Regularly check error and audit logs
8. **Performance Tuning**: Adjust batch sizes based on data volume
9. **Test Queries**: Validate SQL queries on sample data first
10. **Security**: Never commit `.env` file with credentials

## Performance Optimization

### Database Side
- Add indexes on date columns used for incremental extraction
- Optimize queries for specific date ranges
- Use materialized views for complex aggregations
- Partition large tables by date

### Application Side
- Increase batch size for faster extraction (watch memory)
- Use connection pooling (already configured)
- Enable parallel extraction for independent sources
- Compress output files (already configured)

### System Side
- Allocate sufficient memory (2GB+ recommended)
- Use SSD storage for interim files
- Schedule large jobs during off-peak hours
- Monitor system resources during execution

## Maintenance

### Regular Tasks

**Daily**:
- Check extraction logs for errors
- Review validation failure alerts
- Monitor disk space usage

**Weekly**:
- Review performance metrics
- Analyze data quality trends
- Clean up old log files

**Monthly**:
- Update query templates if schema changes
- Review and adjust validation thresholds
- Archive old extraction files
- Update dependencies

### Backup & Recovery

**Backup**:
```bash
# Backup configuration
tar -czf backup_$(date +%Y%m%d).tar.gz config/ .env

# Backup checkpoint file
cp data/interim/extraction_checkpoint.json backups/
```

**Recovery**:
- Restore configuration files
- Restore checkpoint file to resume from last point
- Re-run failed extractions with date range

## Support & Contact

For issues, questions, or contributions:
- Review logs in `logs/` directory
- Check execution summaries in `results/metrics/`
- Consult project objectives in `docs/objectives/`

## License

Internal MOH use only. Confidential and proprietary.

---

**Version**: 1.0  
**Last Updated**: 2026-01-26  
**Maintained By**: MOH Data Analytics Team
