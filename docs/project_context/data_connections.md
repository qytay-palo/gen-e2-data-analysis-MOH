# API Data Connection Guide
## MOH Polyclinic Data Analysis Project

**Document Version**: 1.0  
**Last Updated**: 2026-01-28  
**Author**: Senior Context Engineering Team  
**Platforms**: HEALIX (Databricks) & MCDR (CDSW)

---

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Connection Methods](#connection-methods)
4. [API Authentication](#api-authentication)
5. [Database Connection Setup](#database-connection-setup)
6. [Platform-Specific Instructions](#platform-specific-instructions)
7. [Code Examples](#code-examples)
8. [Troubleshooting](#troubleshooting)
9. [Security Best Practices](#security-best-practices)

---

## Overview

This guide provides step-by-step instructions for connecting to MOH polyclinic data sources through APIs and database connections. The project supports two primary data access methods:

1. **MOH Singapore Open Data API** - Public REST API for healthcare data
2. **Direct Database Connection** - PostgreSQL/MySQL/MSSQL/Oracle database access

### Supported Platforms
- **HEALIX (GCC Cloud)**: Databricks environment with Python/R/STATA
- **MCDR (On-Premise)**: Cloudera CDSW with Spark, Python/R, HUE SQL interface

---

## Prerequisites

### Required Tools & Libraries

#### For Python (HEALIX Databricks / MCDR CDSW)
```bash
# Install required packages
pip install psycopg2-binary pymysql pyodbc cx-Oracle requests pyyaml pandas
```

#### For R (HEALIX Databricks / MCDR CDSW)
```r
# Install required packages
install.packages(c("DBI", "RPostgreSQL", "RMySQL", "odbc", "httr", "jsonlite", "yaml", "dplyr"))
```

#### For Spark (MCDR CDSW)
```bash
# JDBC drivers should be pre-configured in CDSW
# Verify with: spark.conf.get("spark.jars")
```

### Environment Variables Setup

Create a `.env` file in your project root (never commit to git):

```bash
# MOH Open Data API
MOH_API_KEY=your_api_key_here

# Database Credentials
DB_HOST=your_database_host
DB_PORT=5432
DB_NAME=moh_polyclinic_data
DB_SCHEMA=public
DB_USER=your_username
DB_PASSWORD=your_password
```

**Security Note**: Add `.env` to `.gitignore` immediately.

---

## Data Access & Constraints

### Database Access Patterns

The MOH polyclinic data can be accessed through multiple patterns depending on your use case:

#### 1. **Read-Only Views** (Recommended for Analytics)
- **Use Case**: Data analysis, reporting, dashboards without risk of modifying source data
- **Access Method**: Materialized views or database views with SELECT-only permissions
- **Advantages**: 
  - Prevents accidental data modifications
  - Optimized query performance through pre-aggregated views
  - Simplified schema (business-friendly column names)
- **Limitations**: 
  - Cannot perform INSERT/UPDATE/DELETE operations
  - View refresh schedule determines data freshness
- **Example Views**:
  - `vw_daily_attendance_summary`
  - `vw_patient_chronic_conditions`
  - `vw_waiting_time_metrics`

#### 2. **Direct Database Queries** (Advanced Users)
- **Use Case**: Custom analysis requiring complex joins, ad-hoc exploration
- **Access Method**: Direct SQL queries to source tables via JDBC/ODBC
- **Advantages**:
  - Full flexibility for complex queries
  - Access to raw, unfiltered data
  - Real-time data (subject to replication lag)
- **Limitations**:
  - Requires strong SQL knowledge
  - Performance depends on query optimization
  - Must handle data quality issues
- **Required Permissions**: `SELECT` on schema `public` or `moh_polyclinic`

#### 3. **API Access** (External/Public Users)
- **Use Case**: Integration with external systems, rate-limited public access
- **Access Method**: RESTful API endpoints
- **Advantages**:
  - No VPN/network restrictions
  - Standardized JSON responses
  - Built-in rate limiting and caching
- **Limitations**:
  - Rate limits (100 requests/minute for public API)
  - Limited to public datasets only
  - May not include recent data (24-48hr lag)

### Data Refresh Frequency

| Table/Dataset | Refresh Frequency | Refresh Time (SGT) | Incremental/Full | Latency |
|---------------|-------------------|-------------------|------------------|----------|
| **POLYCLINIC_ATTENDANCES** | Daily | 02:00 AM | Incremental (last 3 days) | ~6 hours |
| **PATIENT_DEMOGRAPHICS** | Daily | 03:00 AM | Incremental (updated records) | ~6 hours |
| **DIAGNOSIS_RECORDS** | Daily | 02:30 AM | Incremental (last 3 days) | ~6 hours |
| **PROCEDURE_RECORDS** | Daily | 02:45 AM | Incremental (last 3 days) | ~6 hours |
| **MEDICATION_PRESCRIPTIONS** | Daily | 03:15 AM | Incremental (last 3 days) | ~6 hours |
| **LABORATORY_RESULTS** | Daily | 04:00 AM | Incremental (last 7 days) | ~24-48 hours |
| **POLYCLINIC_MASTER** (Reference) | Monthly | 1st day, 05:00 AM | Full refresh | N/A |
| **CONDITION_MASTER** (Reference) | Quarterly | 1st day, 05:30 AM | Full refresh | N/A |

**ETL Pipeline Details**:
- **Source System**: MOH CDMS (Clinical Data Management System)
- **ETL Tool**: Apache Airflow (MCDR) / Databricks Jobs (HEALIX)
- **Data Validation**: Automated data quality checks run post-extraction
- **Failure Handling**: Email alerts to data engineering team; automatic retry 3x
- **Historical Backfill**: Available on request for analysis requiring >90 days lookback

**Real-Time Data Considerations**:
- Current ETL provides **near-daily** refresh (D-1 data available by 6 AM)
- For real-time needs (<1 hour latency), contact data engineering team for streaming setup
- Intraday updates not available in current architecture

### Access Request Process

1. **Submit Data Access Request**: Email data.governance@moh.gov.sg with:
   - Project title and objectives
   - Required tables/datasets
   - Access pattern (read-only view vs direct query vs API)
   - Expected query frequency and data volume

2. **Approval Timeline**: 5-10 business days

3. **Credentials Provisioning**: Receive credentials via secure channel

4. **Onboarding Session**: Mandatory 1-hour training on data security and usage policies

---

## Connection Methods

### Method 1: MOH Singapore Open Data API

**Use Case**: Public datasets, rate-limited access, no VPN required

**Endpoint**: `https://data.gov.sg/api/action/datastore_search`

**Rate Limits**: 100 requests/minute

**Authentication**: API Key (obtain from data.gov.sg)

#### Python Implementation

```python
import requests
import os
from typing import Dict, List, Any

class MOHDataAPIClient:
    """Client for MOH Singapore Open Data API"""
    
    def __init__(self, api_key: str = None):
        self.base_url = "https://data.gov.sg/api/action"
        self.api_key = api_key or os.getenv('MOH_API_KEY')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })
    
    def search_dataset(self, resource_id: str, limit: int = 100, 
                      offset: int = 0, filters: Dict = None) -> Dict:
        """
        Search dataset by resource ID
        
        Args:
            resource_id: Dataset resource identifier
            limit: Number of records per request (max 100)
            offset: Starting record number
            filters: Query filters as dictionary
            
        Returns:
            Dictionary with 'records' and 'total' count
        """
        endpoint = f"{self.base_url}/datastore_search"
        
        params = {
            'resource_id': resource_id,
            'limit': limit,
            'offset': offset
        }
        
        if filters:
            params['filters'] = filters
        
        try:
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            return response.json()['result']
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            raise
    
    def fetch_all_records(self, resource_id: str, 
                         batch_size: int = 100) -> List[Dict]:
        """
        Fetch all records from dataset with pagination
        
        Args:
            resource_id: Dataset resource identifier
            batch_size: Records per request
            
        Returns:
            List of all records
        """
        all_records = []
        offset = 0
        
        while True:
            result = self.search_dataset(
                resource_id=resource_id,
                limit=batch_size,
                offset=offset
            )
            
            records = result.get('records', [])
            if not records:
                break
                
            all_records.extend(records)
            offset += batch_size
            
            # Check if we've reached the end
            if len(records) < batch_size:
                break
        
        return all_records

# Usage Example
api_client = MOHDataAPIClient()
attendances = api_client.fetch_all_records(
    resource_id='polyclinic-attendances-522',
    batch_size=100
)
```

#### R Implementation

```r
library(httr)
library(jsonlite)

MOHDataAPIClient <- R6::R6Class(
  "MOHDataAPIClient",
  
  public = list(
    base_url = "https://data.gov.sg/api/action",
    api_key = NULL,
    
    initialize = function(api_key = NULL) {
      self$api_key <- api_key %||% Sys.getenv("MOH_API_KEY")
    },
    
    search_dataset = function(resource_id, limit = 100, 
                            offset = 0, filters = NULL) {
      endpoint <- paste0(self$base_url, "/datastore_search")
      
      query_params <- list(
        resource_id = resource_id,
        limit = limit,
        offset = offset
      )
      
      if (!is.null(filters)) {
        query_params$filters <- toJSON(filters, auto_unbox = TRUE)
      }
      
      response <- GET(
        url = endpoint,
        query = query_params,
        add_headers(
          Authorization = paste("Bearer", self$api_key),
          `Content-Type` = "application/json"
        ),
        timeout(30)
      )
      
      stop_for_status(response)
      content(response, as = "parsed")$result
    },
    
    fetch_all_records = function(resource_id, batch_size = 100) {
      all_records <- list()
      offset <- 0
      
      repeat {
        result <- self$search_dataset(resource_id, batch_size, offset)
        records <- result$records
        
        if (length(records) == 0) break
        
        all_records <- c(all_records, records)
        offset <- offset + batch_size
        
        if (length(records) < batch_size) break
      }
      
      as.data.frame(do.call(rbind, all_records))
    }
  )
)

# Usage
api_client <- MOHDataAPIClient$new()
attendances <- api_client$fetch_all_records("polyclinic-attendances-522")
```

---

### Method 2: Direct Database Connection

**Use Case**: Internal database access, higher throughput, requires VPN/network access

**Supported Databases**: PostgreSQL, MySQL, MS SQL Server, Oracle

#### Python - PostgreSQL Connection

```python
import psycopg2
from psycopg2 import pool
import os
from contextlib import contextmanager

class PostgreSQLConnector:
    """PostgreSQL database connector with connection pooling"""
    
    def __init__(self, host: str = None, port: int = None, 
                 database: str = None, user: str = None, 
                 password: str = None, pool_size: int = 5):
        
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=pool_size,
            host=host or os.getenv('DB_HOST'),
            port=port or os.getenv('DB_PORT', 5432),
            database=database or os.getenv('DB_NAME'),
            user=user or os.getenv('DB_USER'),
            password=password or os.getenv('DB_PASSWORD'),
            sslmode='require',
            connect_timeout=30
        )
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = self.connection_pool.getconn()
        try:
            yield conn
        finally:
            self.connection_pool.putconn(conn)
    
    def execute_query(self, query: str, params: tuple = None):
        """Execute query and return results as list of dictionaries"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
                
                conn.commit()
                return None
    
    def close_pool(self):
        """Close all connections in pool"""
        if self.connection_pool:
            self.connection_pool.closeall()

# Usage Example
db = PostgreSQLConnector()

# Fetch polyclinic attendances for date range
query = """
SELECT 
    attendance_id, 
    patient_id, 
    polyclinic_id,
    attendance_date,
    waiting_time_minutes,
    visit_type
FROM polyclinic_attendances
WHERE attendance_date >= %s 
  AND attendance_date <= %s
ORDER BY attendance_date DESC
"""

results = db.execute_query(query, ('2026-01-01', '2026-01-28'))
print(f"Fetched {len(results)} attendance records")
```

#### R - PostgreSQL Connection

```r
library(DBI)
library(RPostgreSQL)

# Create database connection
create_postgres_connection <- function() {
  con <- dbConnect(
    PostgreSQL(),
    host = Sys.getenv("DB_HOST"),
    port = as.integer(Sys.getenv("DB_PORT", "5432")),
    dbname = Sys.getenv("DB_NAME"),
    user = Sys.getenv("DB_USER"),
    password = Sys.getenv("DB_PASSWORD"),
    sslmode = "require"
  )
  return(con)
}

# Execute query with parameters
execute_query <- function(con, query, params = NULL) {
  if (!is.null(params)) {
    result <- dbGetQuery(con, query, params = params)
  } else {
    result <- dbGetQuery(con, query)
  }
  return(result)
}

# Usage Example
con <- create_postgres_connection()

attendances <- execute_query(
  con,
  "SELECT * FROM polyclinic_attendances 
   WHERE attendance_date >= $1 AND attendance_date <= $2",
  params = list("2026-01-01", "2026-01-28")
)

dbDisconnect(con)
```

---

## Platform-Specific Instructions

### HEALIX (Databricks) Setup

#### Step 1: Create Databricks Secrets

```python
# In Databricks notebook
dbutils.secrets.createScope(scope="moh-polyclinic")

# Add secrets
dbutils.secrets.put(
    scope="moh-polyclinic",
    key="api-key",
    string_value="your_api_key_here"
)

dbutils.secrets.put(
    scope="moh-polyclinic",
    key="db-password",
    string_value="your_db_password"
)
```

#### Step 2: Connect in Databricks Notebook

```python
# Retrieve secrets
api_key = dbutils.secrets.get(scope="moh-polyclinic", key="api-key")
db_password = dbutils.secrets.get(scope="moh-polyclinic", key="db-password")

# Option 1: Use API
from notebooks.utils.api_client import MOHDataAPIClient
client = MOHDataAPIClient(api_key=api_key)
df = spark.createDataFrame(client.fetch_all_records("resource-id"))

# Option 2: Use JDBC connection
jdbc_url = f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"
connection_properties = {
    "user": db_user,
    "password": db_password,
    "driver": "org.postgresql.Driver",
    "ssl": "true"
}

df = spark.read.jdbc(
    url=jdbc_url,
    table="polyclinic_attendances",
    properties=connection_properties
)
```

#### Step 3: Query with Spark SQL

```python
# Register as temp view
df.createOrReplaceTempView("attendances")

# Query with Spark SQL
result = spark.sql("""
    SELECT 
        polyclinic_id,
        DATE(attendance_date) as visit_date,
        COUNT(*) as daily_visits,
        AVG(waiting_time_minutes) as avg_wait_time
    FROM attendances
    WHERE attendance_date >= '2026-01-01'
    GROUP BY polyclinic_id, DATE(attendance_date)
    ORDER BY visit_date DESC
""")

display(result)
```

---

### MCDR (CDSW) Setup

#### Step 1: Store Credentials in CDSW Environment Variables

1. Go to CDSW Project Settings → Environment Variables
2. Add variables:
   - `DB_HOST`
   - `DB_PORT`
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`
   - `MOH_API_KEY`

#### Step 2: Connect Using PySpark

```python
from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder \
    .appName("MOH Polyclinic Analysis") \
    .config("spark.jars", "/path/to/postgresql-jdbc.jar") \
    .getOrCreate()

# Database connection properties
jdbc_url = f"jdbc:postgresql://{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
connection_properties = {
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "driver": "org.postgresql.Driver"
}

# Read data with predicate pushdown
df = spark.read.jdbc(
    url=jdbc_url,
    table="polyclinic_attendances",
    column="attendance_date",
    lowerBound="2026-01-01",
    upperBound="2026-01-31",
    numPartitions=4,
    properties=connection_properties
)

# Write to HDFS
df.write.mode("overwrite").parquet("/user/data/polyclinic/attendances")
```

#### Step 3: Use HUE for SQL Queries

1. Open HUE interface
2. Select PostgreSQL/Impala connection
3. Execute SQL:

```sql
-- Example: Daily attendance statistics
SELECT 
    polyclinic_id,
    attendance_date,
    COUNT(*) as total_visits,
    AVG(waiting_time_minutes) as avg_waiting_time,
    SUM(CASE WHEN visit_status = 'no-show' THEN 1 ELSE 0 END) as no_shows
FROM polyclinic_attendances
WHERE attendance_date >= '2026-01-01'
GROUP BY polyclinic_id, attendance_date
ORDER BY attendance_date DESC;
```

4. Export results or save as HDFS table

---

## Code Examples

### Full ETL Pipeline Example (Python)

```python
"""
Complete ETL pipeline for MOH polyclinic data extraction
Supports both API and database sources
"""

import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# Import project modules
from src.data_processing.db_connector import DatabaseConnector
from src.data_processing.data_extractor import DataExtractor
from src.data_processing.data_validator import DataValidator

def run_extraction_pipeline(
    source_type='database',
    start_date=None,
    end_date=None,
    output_dir='data/1_raw'
):
    """
    Run complete data extraction pipeline
    
    Args:
        source_type: 'api' or 'database'
        start_date: Start date for extraction (YYYY-MM-DD)
        end_date: End date for extraction (YYYY-MM-DD)
        output_dir: Output directory for raw data
    """
    # Set default dates if not provided
    if not end_date:
        end_date = datetime.now().date()
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    print(f"Starting extraction from {start_date} to {end_date}")
    
    # Initialize components
    if source_type == 'database':
        connector = DatabaseConnector('config/database.yml')
    else:
        connector = MOHDataAPIClient()
    
    extractor = DataExtractor(connector)
    validator = DataValidator('config/validation_rules.yml')
    
    # Extract data for each table
    tables = [
        'polyclinic_attendances',
        'patient_demographics',
        'diagnosis_records',
        'medication_records'
    ]
    
    results = {}
    for table in tables:
        print(f"Extracting {table}...")
        
        # Extract data
        df = extractor.extract_table(
            table_name=table,
            start_date=start_date,
            end_date=end_date
        )
        
        # Validate data
        validation_report = validator.validate(df, table)
        
        if validation_report['passed']:
            # Save to parquet
            output_path = Path(output_dir) / f"{table}_{end_date}.parquet"
            df.to_parquet(output_path, index=False, compression='snappy')
            
            results[table] = {
                'status': 'success',
                'records': len(df),
                'path': str(output_path)
            }
            print(f"✓ {table}: {len(df)} records saved")
        else:
            results[table] = {
                'status': 'failed',
                'errors': validation_report['errors']
            }
            print(f"✗ {table}: Validation failed")
    
    return results

# Run pipeline
if __name__ == "__main__":
    results = run_extraction_pipeline(
        source_type='database',
        start_date='2026-01-01',
        end_date='2026-01-28'
    )
    
    print("\nExtraction Summary:")
    for table, result in results.items():
        print(f"  {table}: {result['status']} - {result.get('records', 0)} records")
```

### Incremental Load Example (R)

```r
# Incremental data extraction with state management
library(DBI)
library(dplyr)
library(readr)
library(lubridate)

# Track last extraction timestamp
get_last_extraction_date <- function(table_name, state_file = "data/extraction_state.csv") {
  if (file.exists(state_file)) {
    state <- read_csv(state_file, show_col_types = FALSE)
    last_date <- state %>% 
      filter(table == table_name) %>% 
      pull(last_extraction_date)
    
    if (length(last_date) > 0) {
      return(as.Date(last_date))
    }
  }
  # Default to 30 days ago
  return(Sys.Date() - 30)
}

# Update extraction state
update_extraction_state <- function(table_name, extraction_date, 
                                   state_file = "data/extraction_state.csv") {
  new_state <- tibble(
    table = table_name,
    last_extraction_date = extraction_date,
    last_run_timestamp = Sys.time()
  )
  
  if (file.exists(state_file)) {
    existing_state <- read_csv(state_file, show_col_types = FALSE)
    updated_state <- existing_state %>%
      filter(table != table_name) %>%
      bind_rows(new_state)
  } else {
    updated_state <- new_state
  }
  
  write_csv(updated_state, state_file)
}

# Incremental extraction
extract_incremental <- function(con, table_name, date_column = "attendance_date") {
  last_date <- get_last_extraction_date(table_name)
  current_date <- Sys.Date()
  
  query <- glue::glue(
    "SELECT * FROM {table_name} 
     WHERE {date_column} > '{last_date}' 
       AND {date_column} <= '{current_date}'
     ORDER BY {date_column}"
  )
  
  data <- dbGetQuery(con, query)
  
  if (nrow(data) > 0) {
    # Save to parquet
    output_file <- glue::glue("data/1_raw/{table_name}_{current_date}.parquet")
    arrow::write_parquet(data, output_file)
    
    # Update state
    update_extraction_state(table_name, current_date)
    
    message(glue::glue("✓ Extracted {nrow(data)} new records from {table_name}"))
  } else {
    message(glue::glue("No new records for {table_name} since {last_date}"))
  }
  
  return(data)
}

# Usage
con <- create_postgres_connection()
attendances <- extract_incremental(con, "polyclinic_attendances")
dbDisconnect(con)
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Connection Timeout

**Error**: `psycopg2.OperationalError: timeout expired`

**Solution**:
```python
# Increase timeout in connection string
connection_properties = {
    'connect_timeout': 60,  # Increase from default 30
    'options': '-c statement_timeout=300000'  # 5 minutes
}
```

#### 2. SSL Certificate Errors

**Error**: `SSL connection error: certificate verify failed`

**Solution**:
```python
# Option 1: Require SSL but trust server certificate
sslmode='require'

# Option 2: Verify with custom CA bundle
import ssl
ssl_context = ssl.create_default_context(cafile='/path/to/ca-bundle.crt')
```

#### 3. API Rate Limiting

**Error**: `429 Too Many Requests`

**Solution**:
```python
import time
from functools import wraps

def rate_limited(max_per_minute):
    min_interval = 60.0 / max_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_time = min_interval - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limited(100)  # 100 requests per minute
def api_call():
    # Your API call here
    pass
```

#### 4. Memory Issues with Large Datasets

**Solution - Use Chunked Reading**:
```python
# For PostgreSQL
chunk_size = 10000
for chunk in pd.read_sql(query, con, chunksize=chunk_size):
    process_chunk(chunk)

# For Spark
df = spark.read.jdbc(...).repartition(20)
```

#### 5. Network/VPN Connectivity

**Check Connection**:
```bash
# Test database connectivity
nc -zv your_db_host 5432

# Test API connectivity
curl -I https://data.gov.sg/api/action/datastore_search
```

---

## Security Best Practices

### 1. Credential Management

✅ **DO**:
- Use environment variables for sensitive data
- Store secrets in platform-native secret managers (Databricks Secrets, AWS Secrets Manager)
- Rotate credentials regularly
- Use read-only database accounts when possible

❌ **DON'T**:
- Hard-code credentials in scripts
- Commit `.env` files to version control
- Share credentials via email or chat
- Use production credentials in development

### 2. Network Security

```python
# Always use SSL/TLS for database connections
connection_config = {
    'sslmode': 'require',
    'sslcert': '/path/to/client-cert.pem',
    'sslkey': '/path/to/client-key.pem',
    'sslrootcert': '/path/to/ca-cert.pem'
}
```

### 3. Query Security

```python
# Use parameterized queries to prevent SQL injection
# ✅ SAFE
cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))

# ❌ UNSAFE
cursor.execute(f"SELECT * FROM patients WHERE patient_id = {patient_id}")
```

### 4. Data Access Logging

```python
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def log_data_access(user, table, query, record_count):
    """Log all data access for audit trail"""
    logger.info(
        f"DATA_ACCESS | User: {user} | Table: {table} | "
        f"Records: {record_count} | Timestamp: {datetime.now()}"
    )
```

### 5. Data Minimization

```python
# Only extract necessary columns
query = """
SELECT 
    patient_id,  -- Keep anonymized ID
    age_group,   -- Use binned ages, not exact DOB
    postal_code_district  -- First 2 digits only
FROM patient_demographics
"""
# Don't extract: full names, full DOB, exact addresses
```

---

## Quick Reference

### Environment Setup Checklist

- [ ] Install required Python/R packages
- [ ] Configure environment variables (`.env` file)
- [ ] Obtain API key from data.gov.sg
- [ ] Configure database credentials
- [ ] Test network connectivity (VPN if required)
- [ ] Set up platform-specific secrets (Databricks/CDSW)
- [ ] Verify JDBC drivers (for Spark connections)
- [ ] Create output directories (`data/1_raw`, `data/3_interim`)

### Key Configuration Files

| File | Purpose |
|------|---------|
| `config/database.yml` | Database connection settings |
| `config/queries.yml` | Predefined SQL queries |
| `.env` | Environment variables (do not commit) |
| `src/data_processing/db_connector.py` | Database connection class |
| `scripts/run_extraction.py` | CLI tool for data extraction |

### Useful Commands

```bash
# Run extraction with default settings
python scripts/run_extraction.py --sources all

# Extract specific date range
python scripts/run_extraction.py \
    --start-date 2026-01-01 \
    --end-date 2026-01-28 \
    --incremental

# Extract last N days
python scripts/run_extraction.py --last-n-days 7

# Full extraction with specific sources
python scripts/run_extraction.py \
    --sources polyclinic_attendances patient_demographics \
    --full
```

---

## Support & Resources

**Project Documentation**: `/docs/project_context/`  
**Data Dictionary**: `/docs/data_dictionary/`  
**Configuration**: `/config/`  
**Source Code**: `/src/data_processing/`

For technical support, consult:
1. [MOH Data Portal Documentation](https://data.gov.sg)
2. Platform-specific guides (Databricks, CDSW)
3. Project team leads

---