# System Architecture - MOH Data Extraction System

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     External Systems                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Polyclinic   │  │    NEHR      │  │  Data        │         │
│  │   Database   │  │   Database   │  │  Warehouse   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───────────┬──────────────┬────────────────┬───────────────────┘
            │              │                │
            └──────────────┴────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Connection Layer                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  DatabaseConnector                                          │ │
│  │  • Connection pooling                                       │ │
│  │  • Multi-DB support (PostgreSQL, MySQL, MSSQL, Oracle)     │ │
│  │  • Retry logic                                              │ │
│  │  • Timeout management                                       │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Extraction Layer                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  DataExtractor                                              │ │
│  │  • Query template management                                │ │
│  │  • Incremental extraction                                   │ │
│  │  • Batch processing                                         │ │
│  │  • Checkpoint management                                    │ │
│  │  • Retry on failure                                         │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Validation Layer                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  DataValidator                                              │ │
│  │  • Row count validation                                     │ │
│  │  • Null value checks                                        │ │
│  │  • Date range validation                                    │ │
│  │  • Duplicate detection                                      │ │
│  │  • Referential integrity                                    │ │
│  │  • Data type validation                                     │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Transformation Layer                           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  ETLPipeline (Transform Phase)                             │ │
│  │  • Deduplication                                            │ │
│  │  • Data type conversion                                     │ │
│  │  • Column standardization                                   │ │
│  │  • Metadata enrichment                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Storage Layer                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  File Output System                                         │ │
│  │  • Multiple formats (Parquet, CSV, Excel)                  │ │
│  │  • Compression (gzip)                                       │ │
│  │  • Partitioning by date                                     │ │
│  │  • Organized directory structure                            │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
            │                        │                    │
            ▼                        ▼                    ▼
    ┌──────────────┐       ┌──────────────┐    ┌──────────────┐
    │  data/raw/   │       │data/processed│    │data/interim/ │
    └──────────────┘       └──────────────┘    └──────────────┘

┌─────────────────────────────────────────────────────────────────┐
│             Cross-Cutting Concerns                               │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Logging    │  │  Monitoring  │  │   Alerting   │         │
│  │              │  │              │  │              │         │
│  │ • Extraction │  │ • Performance│  │ • Failures   │         │
│  │ • Errors     │  │ • Memory     │  │ • Quality    │         │
│  │ • Audit      │  │ • Duration   │  │ • Email/Slack│         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   Orchestration Layer                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Scheduler                                                  │ │
│  │  • Daily incremental jobs                                   │ │
│  │  • Weekly full extractions                                  │ │
│  │  • Monthly reference data refresh                           │ │
│  │  • Custom schedules                                         │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. DatabaseConnector
**Purpose**: Manage database connections across multiple database types

**Key Features**:
- Connection pooling for efficiency
- Environment-based credential management
- Retry logic for transient failures
- Query timeout handling
- Read-only mode for sensitive databases

**Supported Databases**:
- PostgreSQL
- MySQL
- MS SQL Server
- Oracle

### 2. DataExtractor
**Purpose**: Extract data from databases efficiently

**Key Features**:
- **Incremental Extraction**: Only extract new/updated records
- **Batch Processing**: Handle large datasets in manageable chunks
- **Checkpoint Management**: Resume from last successful point
- **Query Templates**: Parameterized SQL queries
- **Retry Logic**: Automatic retry on failures

**Extraction Modes**:
1. **Incremental**: Extract only changed data since last run
2. **Full**: Extract complete dataset
3. **Custom Date Range**: Extract specific time period

### 3. DataValidator
**Purpose**: Ensure data quality before processing

**Validation Checks**:
1. **Row Count**: Minimum threshold validation
2. **Null Values**: Check critical columns for nulls
3. **Date Ranges**: Validate dates within expected bounds
4. **Duplicates**: Detect duplicate records
5. **Referential Integrity**: Verify foreign key relationships
6. **Data Types**: Ensure correct data types
7. **Value Ranges**: Check numeric values are reasonable

**Output**: ValidationResult objects with pass/fail status and details

### 4. ETLPipeline
**Purpose**: Orchestrate complete data pipeline

**Phases**:
1. **Extract**: Pull data from source databases
2. **Validate**: Run quality checks
3. **Transform**: Clean and standardize data
4. **Load**: Save to output formats

**Features**:
- Phase-by-phase execution
- Execution logging and metrics
- Stop-on-failure configuration
- Summary generation

### 5. Scheduler
**Purpose**: Automate recurring extraction jobs

**Schedule Types**:
- **Daily** (e.g., 2:00 AM): Incremental extraction
- **Weekly** (e.g., Sunday midnight): Full extraction
- **Monthly** (e.g., 1st of month): Reference data refresh
- **Custom**: User-defined schedules

### 6. Logging & Monitoring
**Purpose**: Track operations and performance

**Components**:
- **Logging**: Multi-level logs (extraction, errors, audit)
- **Performance Monitor**: Track duration, memory, CPU
- **Alert Manager**: Notify on failures and issues

## Data Flow

### Incremental Extraction Flow

```
1. Read checkpoint file
   └─> Get last extraction date for source
   
2. Calculate date range
   └─> From last extraction to today
   
3. Build SQL query
   └─> Apply date filters
   └─> Add batch parameters
   
4. Execute extraction
   └─> Fetch in batches (10,000 rows)
   └─> Process each batch
   └─> Combine results
   
5. Validate data
   └─> Run all validation checks
   └─> Generate validation report
   
6. Transform data
   └─> Remove duplicates
   └─> Standardize formats
   └─> Add metadata
   
7. Save output
   └─> Write to Parquet/CSV
   └─> Apply compression
   └─> Update checkpoint
   
8. Generate summary
   └─> Log metrics
   └─> Create summary report
```

### Full Extraction Flow

```
1. Identify source
   └─> Get table configuration
   
2. Build SQL query
   └─> No date filters
   └─> Batch parameters only
   
3. Execute extraction
   └─> [Same as incremental, steps 4-8]
```

## Configuration Management

### Configuration Files

```
config/
├── database.yml          # Main configuration
│   ├── databases        # DB connections
│   ├── extraction       # Extraction settings
│   ├── data_sources     # Table mappings
│   ├── output           # Output settings
│   ├── quality_checks   # Validation rules
│   ├── schedule         # Job schedules
│   └── logging          # Log configuration
│
└── queries.yml          # SQL templates
    ├── queries          # Data extraction queries
    └── validation       # Validation queries
```

### Environment Variables

```
.env                     # Credentials (not in git)
├── DB_HOST             # Database host
├── DB_PORT             # Database port
├── DB_NAME             # Database name
├── DB_USER             # Username
├── DB_PASSWORD         # Password
└── ...                 # Other DB configs
```

## Execution Modes

### Mode 1: Manual Execution
```bash
python scripts/run_extraction.py --sources <source> --last-n-days 7
```

**Use Cases**:
- Ad-hoc extraction
- Testing
- Historical data backfill
- Development

### Mode 2: Scheduled Execution
```bash
python scripts/run_scheduler.py
```

**Use Cases**:
- Production operations
- Daily incremental updates
- Weekly full refreshes
- Automated monitoring

### Mode 3: Python API
```python
pipeline = ETLPipeline()
result = pipeline.run_full_pipeline(...)
```

**Use Cases**:
- Integration with other systems
- Custom workflows
- Jupyter notebooks
- Analysis scripts

## Security Features

1. **Credential Management**
   - Environment variables (not hardcoded)
   - .env file (excluded from git)
   - No credentials in logs

2. **Database Access**
   - Read-only mode for sensitive DBs
   - Connection timeout limits
   - SSL/TLS support

3. **Audit Trail**
   - Structured audit logging
   - Extraction timestamps
   - User/system identification

4. **Data Protection**
   - Secure file permissions
   - Encrypted connections
   - Access logging

## Performance Optimization

### Database Level
- Connection pooling (5 connections default)
- Batch size: 10,000 rows
- Query timeout: 300 seconds
- Indexed date columns

### Application Level
- Memory limit: 2048 MB
- Parallel processing: 4 workers
- Retry logic: 3 attempts, 5s delay
- Incremental extraction

### Storage Level
- Parquet format (columnar, efficient)
- Gzip compression
- Partitioning by date
- Clean old files

## Monitoring & Alerting

### Metrics Tracked
- Extraction duration
- Row counts
- Memory usage
- CPU utilization
- Success/failure rates
- Validation results

### Alert Conditions
- Extraction failure
- Quality check failure
- Row count deviation (>20%)
- Critical validation failures

### Notification Channels
- Email
- Slack
- Microsoft Teams
- Log files

## Disaster Recovery

### Checkpoint System
- Saves last successful extraction date
- Enables resume from failure point
- JSON format for easy inspection

### Backup Strategy
1. Configuration files (daily)
2. Checkpoint files (after each run)
3. Extracted data (retention policy)
4. Log files (rotation with backups)

### Recovery Procedure
1. Restore configuration
2. Restore checkpoint file
3. Re-run extraction with date range
4. Validate recovered data

## Extension Points

### Adding New Data Sources
1. Add to `config/database.yml` → `data_sources`
2. Add query to `config/queries.yml`
3. Run extraction

### Custom Transformations
1. Extend `ETLPipeline.run_transformation()`
2. Add source-specific logic
3. Test with sample data

### Custom Validations
1. Extend `DataValidator` class
2. Add validation method
3. Register in validation flow

### Custom Schedules
1. Use `scheduler.run_custom_job()`
2. Define job function
3. Set schedule time

## Technology Stack

- **Language**: Python 3.8+
- **Database Drivers**: psycopg2, pymysql, pyodbc, cx_Oracle
- **Data Processing**: pandas, pyarrow
- **Configuration**: PyYAML, python-dotenv
- **Scheduling**: schedule
- **Monitoring**: psutil
- **Storage**: Parquet, CSV, Excel

## Deployment Options

### Option 1: Standalone Server
- Single dedicated server
- Cron/systemd for scheduling
- Local file storage

### Option 2: Container (Docker)
- Dockerized application
- Kubernetes orchestration
- Persistent volumes

### Option 3: Cloud (AWS/Azure/GCP)
- Lambda/Functions for execution
- S3/Blob/GCS for storage
- CloudWatch/Monitor for logging

---

**Version**: 1.0  
**Last Updated**: 2026-01-26
