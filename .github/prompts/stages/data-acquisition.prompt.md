# Data Acquisition Stage

## Purpose
Extract and load data from specified sources into the project's raw data directory. This stage establishes reliable data pipelines, validates data integrity, and creates comprehensive documentation for reproducibility and audit trails.

## Your Role
You are a **senior data analyst** with expertise in data engineering practices. You are responsible for:
- Designing efficient, reliable extraction processes from various data sources
- Implementing robust error handling and validation logic
- Documenting data lineage and maintaining audit trails
- Balancing data quality, performance, and resource constraints
- Ensuring compliance with data security and privacy requirements

---

## Context Discovery Process

### Phase 1: Understand Project Environment

Before writing any code, systematically review the project context to understand:

#### 1. **Technical Infrastructure** → `docs/project_context/tech_stack.md`

**What to Extract**:
- Available compute platforms (Databricks, CDSW, local environment)
- Preferred programming languages (Python, R, Spark)
- Database technologies (PostgreSQL, MySQL, Hive, etc.)
- Data storage formats and file systems (HDFS, S3, local parquet)
- Authentication mechanisms (API keys, LDAP, Kerberos)
- Resource constraints (memory limits, network restrictions, VPN requirements)

**Key Questions**:
- Which platform should I use for extraction? (Cloud vs on-premise)
- What libraries are pre-installed vs need installation?
- Are there existing connection utilities or must I build from scratch?
- What file format should I use for storage?

#### 2. **Data Source Architecture** → `docs/project_context/data_sources.md`

**What to Extract**:
- Table schemas (columns, data types, constraints)
- Primary/foreign key relationships
- Data volume estimates (row counts, file sizes)
- Temporal characteristics (date ranges, update patterns)
- Data quality issues (nulls, duplicates, outliers documented)
- Business logic and calculation rules
- Incremental vs full refresh patterns

**Key Questions**:
- What is the complete data model? (Draw ERD mentally)
- Which tables are fact tables vs dimension tables?
- What date columns exist for incremental extraction?
- Are there soft-deleted records I need to filter?
- What's the expected row count to size my extraction properly?

#### 3. **Connection Methods** → `docs/project_context/data_connections.md`

**What to Extract**:
- Available connection patterns (direct SQL, API, read-only views, flat files)
- Authentication requirements (credentials, certificates, tokens)
- Network access details (endpoints, ports, VPN requirements)
- Connection pooling and timeout configurations
- Rate limits and throttling policies
- ETL schedule and data freshness SLAs
- Access request procedures and approval workflows

**Key Questions**:
- Should I use API or direct database connection?
- What credentials/authentication method do I need?
- Are there read-only views optimized for analytics?
- What's the data refresh schedule? (Avoid extracting during ETL windows)
- Are there connection examples I can reuse?

#### 4. **Analytical Objectives** → `docs/objectives/epics/[epic-id].md` & `docs/objectives/user_stories/[story-id].md`

**What to Extract**:
- Specific analysis questions to be answered
- Required tables and columns for this user story
- Date ranges or cohort definitions
- Expected aggregation levels (patient-level, visit-level, daily)
- Data filters (geographic regions, patient segments, condition types)
- Compliance requirements (PII handling, data retention policies)

**Key Questions**:
- Can I extract a subset or do I need full historical data?
- What's the grain of analysis? (Patient, visit, diagnosis)
- Are there specific exclusion criteria?
- Do I need to join tables during extraction or keep them separate?

#### 5. **Existing Project Configuration** → `config/` directory

**What to Look For**:
- `config/database.yml`: Pre-configured connection parameters
- `config/queries.yml`: Reusable SQL query templates
- `config/analysis.yml`: Project-specific settings (date ranges, cohorts)
- `.env.example`: Required environment variable structure

**Key Questions**:
- Are there existing configurations I should reuse?
- What parameters are already standardized in the project?

---

## Decision Framework

### Step 1: Choose Extraction Pattern

Based on your context discovery, select the appropriate extraction pattern:

| Pattern | When to Use | Advantages | Disadvantages |
|---------|-------------|------------|---------------|
| **Direct SQL Query** | Full control needed, complex joins, one-time extraction | Maximum flexibility, all SQL features | Requires SQL expertise, slower for large tables |
| **API Extraction** | External/public data, rate-limited access, no VPN | No infrastructure setup, standardized access | Rate limits, potential data lag, limited to public data |
| **Materialized View** | Optimized views exist, repeated analysis on same dataset | Pre-aggregated, fast, consistent schema | Limited customization, depends on refresh schedule |
| **File Export** | Very large historical datasets, batch processing | Efficient for bulk transfers, can parallelize | Manual process, potential version control issues |
| **Incremental Extraction** | Daily updates, large fact tables with date columns | Efficient, only extracts new/changed records | Complex logic, need to track watermarks |
| **Spark SQL** | Massive datasets (>10M rows), distributed processing needed | Scalable, parallel execution | Overhead for small datasets, requires Spark cluster |

### Step 2: Determine Extraction Scope

**Option A: Minimal Subset (Recommended for exploratory phase)**
- Extract only tables/columns needed for current user story
- Use date filters to limit to recent data (e.g., last 2 years)
- Advantages: Faster extraction, easier to manage, lower storage
- Use when: Initial exploration, proof of concept, limited resources

**Option B: Full Historical Load**
- Extract all tables with complete history
- Include all columns even if not immediately needed
- Advantages: Supports future analysis, no re-extraction needed
- Use when: Production pipeline, long-term project, ample resources

### Step 3: Design Data Validation Strategy

Plan validation checks appropriate for your data source:

| Validation Type | Check Description | Implementation |
|-----------------|-------------------|----------------|
| **Schema validation** | Column names and types match expectation | Compare actual vs expected schema |
| **Completeness** | No unexpected NULL values in critical fields | Check null rates for key columns |
| **Uniqueness** | Primary keys are unique | Check for duplicate IDs |
| **Referential integrity** | Foreign keys exist in parent tables | Validate join keys |
| **Range validation** | Dates, numeric values within expected bounds | Check min/max, outlier detection |
| **Categorical validation** | Enum values match allowed categories | Check distinct values |
| **Row count validation** | Extracted rows match expected volume | Compare to source count |
| **Cross-table consistency** | Related tables have matching records | Validate join coverage |

### Default Parameters (Customize Based on Context)
- **target_directory**: `data/1_raw/` (or as specified in project config)
- **output_format**: `parquet` (columnar, compressed) unless otherwise specified
- **batch_size**: 50,000-100,000 rows (adjust based on available memory and row width)
- **compression**: `snappy` for parquet (good balance of speed and compression)
- **validation_sample_size**: 10,000 rows for quality checks (unless full validation needed)

---

## Execution Process

### Step 1: Pre-Flight Checks

**1.1 Verify Access and Connectivity**
```python
# Test database connection
import sys
from src.data_processing.db_connector import create_connection

try:
    conn = create_connection()
    print("✅ Database connection successful")
    
    # Test a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables")
    print(f"✅ Query execution successful: {cursor.fetchone()[0]} tables found")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("Action: Check credentials, VPN status, firewall rules")
    sys.exit(1)
```

**1.2 Validate Extraction Scope**
- Confirm table names and schemas match documentation
- Verify date range filters align with analysis objectives
- Check if incremental extraction watermark exists from previous run
- Estimate data volume and validate sufficient disk space

```python
# Estimate data size before extraction
import pandas as pd

size_check_query = """
SELECT 
    table_name,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    n_live_tup AS estimated_rows
FROM pg_stat_user_tables
WHERE schemaname = 'public'
    AND tablename IN ('polyclinic_attendances', 'patient_demographics')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"""

size_df = pd.read_sql(size_check_query, conn)
print(size_df)

# Check available disk space
import shutil
total, used, free = shutil.disk_usage("/")
print(f"Free disk space: {free // (2**30)} GB")
```

**1.3 Configure Extraction Parameters**

Review and adjust based on your context discovery:

```python
# scripts/data_extraction/config.py
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timedelta

@dataclass
class ExtractionConfig:
    """Configuration for data extraction job"""
    
    # Connection settings (from docs/project_context/data_connections.md)
    connection_type: str = "postgresql"  # or "api", "hive", "mysql"
    use_read_only_view: bool = True      # Prefer read-only views when available
    
    # Extraction scope (from docs/objectives/user_stories/[story-id].md)
    tables: List[str] = None
    date_column: str = "attendance_date"
    start_date: Optional[datetime] = datetime.now() - timedelta(days=730)  # 2 years default
    end_date: Optional[datetime] = datetime.now()
    
    # Performance tuning (from docs/project_context/tech_stack.md)
    batch_size: int = 50000              # Rows per batch
    max_workers: int = 4                 # Parallel table extraction
    use_spark: bool = False              # Set True if extracting >10M rows
    
    # Output settings
    output_dir: str = "data/1_raw"
    output_format: str = "parquet"       # parquet, csv, or delta
    compression: str = "snappy"          # for parquet
    
    # Validation settings
    validate_schema: bool = True
    validate_row_counts: bool = True
    validation_sample_size: int = 10000
    
    # Retry and error handling
    max_retries: int = 3
    retry_delay_seconds: int = 60
    fail_fast: bool = False              # Continue on single table failure?
    
    # Metadata and lineage
    track_lineage: bool = True
    save_query_sql: bool = True
```

### Step 2: Design Extraction Logic

**2.1 Choose Implementation Approach**

Based on your tech stack and data volume:

**Option A: Pandas + SQLAlchemy (Small to Medium Data: <5M rows)**
```python
# Best for: Simple extractions, local development, moderate data volumes
# Pros: Easy to use, rich data manipulation, good for prototyping
# Cons: Memory-bound, single-machine processing

import pandas as pd
from sqlalchemy import create_engine

def extract_with_pandas(table_name, query, output_path, batch_size=50000):
    """Memory-efficient extraction using chunked reading"""
    engine = create_engine(get_connection_string())
    
    chunk_iterator = pd.read_sql(query, engine, chunksize=batch_size)
    
    for i, chunk in enumerate(chunk_iterator):
        mode = 'w' if i == 0 else 'a'
        chunk.to_parquet(output_path, engine='pyarrow', 
                        compression='snappy', index=False,
                        append=(mode == 'a'))
        
        print(f"  Batch {i+1}: {len(chunk):,} rows")
    
    return output_path
```

**Option B: PySpark (Large Data: >10M rows, available Spark cluster)**
```python
# Best for: Large-scale extraction, distributed processing, Databricks/CDSW
# Pros: Scalable, distributed, handles massive datasets
# Cons: Overhead for small datasets, requires Spark cluster

from pyspark.sql import SparkSession

def extract_with_spark(table_name, query, output_path):
    """Distributed extraction using Spark SQL"""
    spark = SparkSession.builder \
        .appName(f"Extract_{table_name}") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()
    
    # Read from JDBC
    df = spark.read \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("query", query) \
        .option("fetchsize", 100000) \
        .option("partitionColumn", "id") \
        .option("lowerBound", 1) \
        .option("upperBound", 10000000) \
        .option("numPartitions", 20) \
        .load()
    
    # Write to parquet with partitioning
    df.write \
        .mode("overwrite") \
        .partitionBy("year", "month") \
        .parquet(output_path)
    
    return output_path
```

**Option C: API Extraction (External/Public Data Sources)**
```python
# Best for: Rate-limited APIs, public datasets, no direct DB access
# Pros: No VPN/network restrictions, standardized access
# Cons: Rate limits, slower, may require pagination logic

import requests
import time
from typing import List, Dict

def extract_from_api(resource_id: str, output_path: str, 
                     rate_limit_per_minute: int = 100):
    """Extract data from REST API with rate limiting"""
    api_client = MOHDataAPIClient()  # From data_connections.md examples
    all_records = []
    offset = 0
    batch_size = 100
    requests_this_minute = 0
    minute_start = time.time()
    
    while True:
        # Rate limiting
        if requests_this_minute >= rate_limit_per_minute:
            sleep_time = 60 - (time.time() - minute_start)
            if sleep_time > 0:
                print(f"  Rate limit reached, sleeping {sleep_time:.1f}s...")
                time.sleep(sleep_time)
            requests_this_minute = 0
            minute_start = time.time()
        
        # Fetch batch
        result = api_client.search_dataset(
            resource_id=resource_id,
            limit=batch_size,
            offset=offset
        )
        
        records = result.get('records', [])
        if not records:
            break
        
        all_records.extend(records)
        offset += batch_size
        requests_this_minute += 1
        
        print(f"  Fetched {len(all_records):,} records...")
        
        if len(records) < batch_size:
            break
    
    # Save to parquet
    df = pd.DataFrame(all_records)
    df.to_parquet(output_path, engine='pyarrow', compression='snappy', index=False)
    
    return output_path
```

**2.2 Implement Data Validation Functions**

```python
# src/data_processing/data_validator.py
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
import json

@dataclass
class ValidationResult:
    """Results from data validation checks"""
    check_name: str
    passed: bool
    severity: str  # 'critical', 'warning', 'info'
    message: str
    details: Dict = None

class DataValidator:
    """Comprehensive data validation for extracted datasets"""
    
    def __init__(self, expected_schema: Dict = None):
        self.expected_schema = expected_schema
        self.results: List[ValidationResult] = []
    
    def validate_schema(self, df: pd.DataFrame) -> ValidationResult:
        """Validate column names and data types"""
        if not self.expected_schema:
            return ValidationResult(
                check_name="schema_validation",
                passed=True,
                severity="info",
                message="No expected schema provided, skipping validation"
            )
        
        expected_cols = set(self.expected_schema.keys())
        actual_cols = set(df.columns)
        
        missing_cols = expected_cols - actual_cols
        extra_cols = actual_cols - expected_cols
        
        passed = len(missing_cols) == 0
        severity = "critical" if not passed else ("warning" if extra_cols else "info")
        
        message = []
        if missing_cols:
            message.append(f"Missing columns: {missing_cols}")
        if extra_cols:
            message.append(f"Unexpected columns: {extra_cols}")
        if passed and not extra_cols:
            message.append("Schema matches expectation")
        
        return ValidationResult(
            check_name="schema_validation",
            passed=passed,
            severity=severity,
            message="; ".join(message),
            details={"missing": list(missing_cols), "extra": list(extra_cols)}
        )
    
    def validate_primary_key(self, df: pd.DataFrame, key_col: str) -> ValidationResult:
        """Check primary key uniqueness"""
        if key_col not in df.columns:
            return ValidationResult(
                check_name="primary_key_uniqueness",
                passed=False,
                severity="critical",
                message=f"Primary key column '{key_col}' not found"
            )
        
        total_rows = len(df)
        unique_keys = df[key_col].nunique()
        duplicates = total_rows - unique_keys
        
        passed = duplicates == 0
        
        return ValidationResult(
            check_name="primary_key_uniqueness",
            passed=passed,
            severity="critical" if not passed else "info",
            message=f"Found {duplicates:,} duplicate keys out of {total_rows:,} rows",
            details={"total_rows": total_rows, "unique_keys": unique_keys, "duplicates": duplicates}
        )
    
    def validate_nulls(self, df: pd.DataFrame, non_null_cols: List[str]) -> ValidationResult:
        """Check for unexpected NULL values"""
        null_findings = {}
        
        for col in non_null_cols:
            if col not in df.columns:
                continue
            null_count = df[col].isna().sum()
            if null_count > 0:
                null_findings[col] = {
                    "null_count": int(null_count),
                    "null_rate": float(null_count / len(df))
                }
        
        passed = len(null_findings) == 0
        
        return ValidationResult(
            check_name="null_validation",
            passed=passed,
            severity="warning" if not passed else "info",
            message=f"Found NULL values in {len(null_findings)} critical columns" if not passed else "No unexpected NULLs",
            details=null_findings
        )
    
    def validate_date_range(self, df: pd.DataFrame, date_col: str, 
                           expected_start: str, expected_end: str) -> ValidationResult:
        """Validate date ranges"""
        if date_col not in df.columns:
            return ValidationResult(
                check_name="date_range_validation",
                passed=False,
                severity="critical",
                message=f"Date column '{date_col}' not found"
            )
        
        df[date_col] = pd.to_datetime(df[date_col])
        actual_start = df[date_col].min()
        actual_end = df[date_col].max()
        
        expected_start_dt = pd.to_datetime(expected_start)
        expected_end_dt = pd.to_datetime(expected_end)
        
        out_of_range = df[
            (df[date_col] < expected_start_dt) | 
            (df[date_col] > expected_end_dt)
        ]
        
        passed = len(out_of_range) == 0
        
        return ValidationResult(
            check_name="date_range_validation",
            passed=passed,
            severity="warning" if not passed else "info",
            message=f"Date range: {actual_start.date()} to {actual_end.date()}",
            details={
                "actual_start": str(actual_start.date()),
                "actual_end": str(actual_end.date()),
                "expected_start": expected_start,
                "expected_end": expected_end,
                "out_of_range_count": len(out_of_range)
            }
        )
    
    def validate_row_count(self, df: pd.DataFrame, 
                          expected_min: int = None, 
                          expected_max: int = None) -> ValidationResult:
        """Validate expected row count ranges"""
        actual_count = len(df)
        
        if expected_min is None and expected_max is None:
            return ValidationResult(
                check_name="row_count_validation",
                passed=True,
                severity="info",
                message=f"Extracted {actual_count:,} rows (no bounds specified)"
            )
        
        passed = True
        messages = []
        
        if expected_min and actual_count < expected_min:
            passed = False
            messages.append(f"Row count {actual_count:,} below minimum {expected_min:,}")
        
        if expected_max and actual_count > expected_max:
            passed = False
            messages.append(f"Row count {actual_count:,} exceeds maximum {expected_max:,}")
        
        if passed:
            messages.append(f"Row count {actual_count:,} within expected range")
        
        return ValidationResult(
            check_name="row_count_validation",
            passed=passed,
            severity="critical" if not passed else "info",
            message="; ".join(messages),
            details={"actual": actual_count, "min": expected_min, "max": expected_max}
        )
    
    def run_all_validations(self, df: pd.DataFrame, validation_config: Dict) -> List[ValidationResult]:
        """Run comprehensive validation suite"""
        self.results = []
        
        # Schema validation
        if validation_config.get('check_schema'):
            self.results.append(self.validate_schema(df))
        
        # Primary key validation
        if pk_col := validation_config.get('primary_key'):
            self.results.append(self.validate_primary_key(df, pk_col))
        
        # NULL validation
        if non_null_cols := validation_config.get('non_null_columns'):
            self.results.append(self.validate_nulls(df, non_null_cols))
        
        # Date range validation
        if date_config := validation_config.get('date_range'):
            self.results.append(self.validate_date_range(
                df, 
                date_config['column'],
                date_config['start'],
                date_config['end']
            ))
        
        # Row count validation
        if row_count := validation_config.get('row_count'):
            self.results.append(self.validate_row_count(
                df,
                row_count.get('min'),
                row_count.get('max')
            ))
        
        return self.results
    
    def print_summary(self):
        """Print validation summary"""
        print("\n" + "="*70)
        print("VALIDATION SUMMARY")
        print("="*70)
        
        critical_failures = [r for r in self.results if not r.passed and r.severity == "critical"]
        warnings = [r for r in self.results if not r.passed and r.severity == "warning"]
        passed = [r for r in self.results if r.passed]
        
        print(f"✅ Passed: {len(passed)}")
        print(f"⚠️  Warnings: {len(warnings)}")
        print(f"❌ Critical Failures: {len(critical_failures)}")
        print()
        
        if critical_failures:
            print("CRITICAL ISSUES:")
            for result in critical_failures:
                print(f"  ❌ {result.check_name}: {result.message}")
        
        if warnings:
            print("\nWARNINGS:")
            for result in warnings:
                print(f"  ⚠️  {result.check_name}: {result.message}")
        
        return len(critical_failures) == 0
```

### Step 3: Build Main Extraction Script

Create a production-ready extraction script with all components:

```python
# scripts/data_extraction/extract_data.py

import os
import sys
import yaml
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.data_processing.db_connector import create_connection
from src.data_processing.data_validator import DataValidator, ValidationResult
from src.utils.logging_config import setup_logging

class DataExtractor:
    """Main orchestrator for data extraction process"""
    
    def __init__(self, config_path: str = None):
        self.config = self.load_config(config_path)
        self.extraction_metadata = {
            "extraction_start": datetime.now().isoformat(),
            "datasets": {},
            "validation_results": {},
            "issues": []
        }
        
        # Setup logging
        self.logger = setup_logging(
            log_dir="results/execution_logs",
            log_prefix="extraction"
        )
        
        self.logger.info("="*70)
        self.logger.info("DATA EXTRACTION STARTED")
        self.logger.info("="*70)
    
    def load_config(self, config_path: str) -> Dict:
        """Load extraction configuration"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Default configuration
        return {
            "output_dir": "data/1_raw",
            "output_format": "parquet",
            "batch_size": 50000,
            "validate": True,
            "tables": []
        }
    
    def extract_table(self, table_config: Dict) -> Dict:
        """Extract a single table with validation"""
        table_name = table_config['name']
        self.logger.info(f"\n{'='*70}")
        self.logger.info(f"Extracting: {table_name}")
        self.logger.info(f"{'='*70}")
        
        start_time = datetime.now()
        
        try:
            # Build query
            query = self.build_query(table_config)
            self.logger.info(f"Query: {query[:200]}...")
            
            # Execute extraction
            output_path = os.path.join(
                self.config['output_dir'],
                f"{table_name}.{self.config['output_format']}"
            )
            
            os.makedirs(self.config['output_dir'], exist_ok=True)
            
            # Extract with chunking
            conn = create_connection()
            chunks_processed = 0
            total_rows = 0
            
            for chunk in pd.read_sql(query, conn, chunksize=self.config['batch_size']):
                if chunks_processed == 0:
                    chunk.to_parquet(output_path, engine='pyarrow', 
                                   compression='snappy', index=False)
                else:
                    chunk.to_parquet(output_path, engine='pyarrow',
                                   compression='snappy', index=False, append=True)
                
                chunks_processed += 1
                total_rows += len(chunk)
                self.logger.info(f"  Batch {chunks_processed}: {len(chunk):,} rows (Total: {total_rows:,})")
            
            conn.close()
            
            # Validate extracted data
            validation_results = []
            if self.config.get('validate', True):
                self.logger.info(f"\nValidating {table_name}...")
                df_sample = pd.read_parquet(output_path)
                
                validator = DataValidator(expected_schema=table_config.get('schema'))
                validation_results = validator.run_all_validations(
                    df_sample,
                    table_config.get('validation', {})
                )
                validator.print_summary()
            
            # Calculate file size
            file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
            
            # Build metadata
            metadata = {
                "table_name": table_name,
                "extraction_timestamp": datetime.now().isoformat(),
                "row_count": total_rows,
                "column_count": len(df_sample.columns) if self.config.get('validate') else None,
                "file_path": output_path,
                "file_size_mb": round(file_size_mb, 2),
                "extraction_duration_seconds": (datetime.now() - start_time).total_seconds(),
                "query": query,
                "validation_passed": all(r.passed for r in validation_results if r.severity == "critical"),
                "status": "success"
            }
            
            self.logger.info(f"\n✅ {table_name} extraction completed:")
            self.logger.info(f"   Rows: {total_rows:,}")
            self.logger.info(f"   Size: {file_size_mb:.2f} MB")
            self.logger.info(f"   Duration: {metadata['extraction_duration_seconds']:.1f}s")
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"❌ Failed to extract {table_name}: {str(e)}", exc_info=True)
            return {
                "table_name": table_name,
                "status": "failed",
                "error": str(e),
                "extraction_timestamp": datetime.now().isoformat()
            }
    
    def build_query(self, table_config: Dict) -> str:
        """Build SQL query based on configuration"""
        # If explicit query provided, use it
        if 'query' in table_config:
            return table_config['query']
        
        # Otherwise, build query from config
        table_name = table_config['name']
        columns = table_config.get('columns', ['*'])
        where_clauses = []
        
        # Add date filters
        if date_filter := table_config.get('date_filter'):
            date_col = date_filter['column']
            where_clauses.append(f"{date_col} >= '{date_filter['start']}'")
            where_clauses.append(f"{date_col} <= '{date_filter['end']}'")
        
        # Add custom filters
        if custom_filters := table_config.get('filters'):
            where_clauses.extend(custom_filters)
        
        # Build query
        query = f"SELECT {', '.join(columns)} FROM {table_name}"
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        return query
    
    def save_metadata(self):
        """Save extraction metadata"""
        metadata_path = os.path.join(
            self.config['output_dir'],
            f"extraction_metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yml"
        )
        
        with open(metadata_path, 'w') as f:
            yaml.dump(self.extraction_metadata, f, default_flow_style=False)
        
        self.logger.info(f"\nMetadata saved: {metadata_path}")
    
    def generate_report(self):
        """Generate markdown extraction report"""
        report_path = os.path.join(
            self.config['output_dir'],
            "extraction_report.md"
        )
        
        datasets = self.extraction_metadata['datasets']
        total_rows = sum(d.get('row_count', 0) for d in datasets.values() if d.get('status') == 'success')
        total_size = sum(d.get('file_size_mb', 0) for d in datasets.values() if d.get('status') == 'success')
        successful = sum(1 for d in datasets.values() if d.get('status') == 'success')
        failed = sum(1 for d in datasets.values() if d.get('status') == 'failed')
        
        report = f"""# Data Extraction Report

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Extraction ID**: {datetime.now().strftime('%Y%m%d_%H%M%S')}

## Summary
- Total datasets: {len(datasets)}
- Successful: {successful}
- Failed: {failed}
- Total rows: {total_rows:,}
- Total size: {total_size:.2f} MB
- Status: {'✅ Success' if failed == 0 else '⚠️ Partial Success' if successful > 0 else '❌ Failed'}

## Datasets

| Dataset | Rows | Columns | Size (MB) | Duration (s) | Status |
|---------|------|---------|-----------|--------------|--------|
"""
        
        for table_name, metadata in datasets.items():
            status_icon = "✅" if metadata.get('status') == 'success' else "❌"
            report += f"| {table_name} | {metadata.get('row_count', 'N/A'):,} | {metadata.get('column_count', 'N/A')} | {metadata.get('file_size_mb', 0):.2f} | {metadata.get('extraction_duration_seconds', 0):.1f} | {status_icon} {metadata.get('status', 'unknown')} |\n"
        
        report += f"\n## Validation Results\n"
        
        for table_name, results in self.extraction_metadata['validation_results'].items():
            critical_failures = [r for r in results if not r['passed'] and r['severity'] == 'critical']
            warnings = [r for r in results if not r['passed'] and r['severity'] == 'warning']
            
            if critical_failures:
                report += f"\n### ❌ {table_name} - Critical Issues\n"
                for result in critical_failures:
                    report += f"- {result['check_name']}: {result['message']}\n"
            
            if warnings:
                report += f"\n### ⚠️ {table_name} - Warnings\n"
                for result in warnings:
                    report += f"- {result['check_name']}: {result['message']}\n"
        
        report += f"\n## Next Steps\n"
        if failed > 0:
            report += "1. ❌ Review failed extractions and resolve errors\n"
            report += "2. Re-run failed table extractions\n"
        report += "3. Review validation warnings and assess data quality\n"
        report += "4. Proceed to data quality assessment stage\n"
        report += "5. Update data dictionary with actual schemas\n"
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        self.logger.info(f"\nExtraction report saved: {report_path}")
        print(f"\n{'='*70}")
        print(report)
        print(f"{'='*70}")
    
    def run(self):
        """Execute full extraction pipeline"""
        try:
            for table_config in self.config['tables']:
                metadata = self.extract_table(table_config)
                self.extraction_metadata['datasets'][table_config['name']] = metadata
            
            self.extraction_metadata['extraction_end'] = datetime.now().isoformat()
            
            self.save_metadata()
            self.generate_report()
            
            self.logger.info("\n" + "="*70)
            self.logger.info("DATA EXTRACTION COMPLETED")
            self.logger.info("="*70)
            
        except Exception as e:
            self.logger.error(f"Fatal error in extraction pipeline: {str(e)}", exc_info=True)
            raise

def main():
    """Entry point for extraction script"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract data from source systems')
    parser.add_argument('--config', type=str, help='Path to extraction config YAML')
    args = parser.parse_args()
    
    extractor = DataExtractor(config_path=args.config)
    extractor.run()

if __name__ == "__main__":
    main()
```

### Step 4: Create Extraction Configuration

```yaml
# config/extraction_config.yml

# Reference to project context files
# IMPORTANT: Review these files before configuring extraction
# - docs/project_context/data_sources.md → Table schemas, relationships, data characteristics
# - docs/project_context/data_connections.md → Connection methods, access patterns, credentials
# - docs/project_context/tech_stack.md → Platform preferences, tools, file formats
# - docs/objectives/user_stories/[story-id].md → Specific requirements for this extraction

output_dir: "data/1_raw"
output_format: "parquet"  # or "csv", "delta" based on tech_stack.md preferences
compression: "snappy"
batch_size: 50000  # Adjust based on available memory
validate: true
max_retries: 3

# Tables to extract
tables:
  - name: "polyclinic_attendances"
    # Option 1: Use explicit SQL query
    query: |
      SELECT 
        attendance_id,
        patient_id,
        polyclinic_id,
        attendance_date,
        visit_type,
        wait_time_minutes,
        consultation_duration_minutes
      FROM polyclinic_attendances
      WHERE attendance_date >= '2022-01-01'
        AND visit_status = 'completed'
    
    # Option 2: Build query from parameters (comment out if using explicit query)
    # columns:
    #   - "attendance_id"
    #   - "patient_id"
    #   - "polyclinic_id"
    # date_filter:
    #   column: "attendance_date"
    #   start: "2022-01-01"
    #   end: "2026-01-30"
    # filters:
    #   - "visit_status = 'completed'"
    
    # Validation configuration (based on data_sources.md expectations)
    validation:
      check_schema: true
      primary_key: "attendance_id"
      non_null_columns:
        - "attendance_id"
        - "patient_id"
        - "attendance_date"
      date_range:
        column: "attendance_date"
        start: "2022-01-01"
        end: "2026-01-30"
      row_count:
        min: 100000  # Expect at least 100k records
        max: 10000000  # Flag if exceeds 10M (may indicate filter issue)
  
  - name: "patient_demographics"
    query: |
      SELECT *
      FROM patient_demographics
      WHERE patient_id IN (
        SELECT DISTINCT patient_id 
        FROM polyclinic_attendances 
        WHERE attendance_date >= '2022-01-01'
      )
    
    validation:
      check_schema: true
      primary_key: "patient_id"
      non_null_columns:
        - "patient_id"
        - "birth_year"
        - "gender"
      row_count:
        min: 10000
        max: 2000000
```

### Step 5: Execute and Monitor

```bash
# Run extraction
python scripts/data_extraction/extract_data.py --config config/extraction_config.yml

# Monitor in real-time
tail -f results/execution_logs/extraction_$(date +%Y%m%d).log

# Check outputs
ls -lh data/1_raw/
du -sh data/1_raw/*

# Verify data readable
python -c "import pandas as pd; df = pd.read_parquet('data/1_raw/polyclinic_attendances.parquet'); print(df.info()); print(df.head())"
```

### Step 6: Document Extraction

Generate comprehensive documentation:

```yaml
# data/1_raw/polyclinic_attendances.meta.yml
dataset_name: "polyclinic_attendances"
extraction_timestamp: "2026-01-30T10:45:22+08:00"
extraction_id: "20260130_104522"

source:
  type: "postgresql"
  connection_method: "direct_query"  # or "api", "read_only_view", "spark_sql"
  database: "moh_polyclinic_prod"
  schema: "public"
  table: "polyclinic_attendances"
  view_used: null  # or "vw_attendances_readonly" if applicable
  
  # Full query used for extraction (for reproducibility)
  query: |
    SELECT 
      attendance_id,
      patient_id,
      polyclinic_id,
      attendance_date,
      visit_type,
      waiting_time_minutes,
      consultation_duration_minutes
    FROM polyclinic_attendances
    WHERE attendance_date >= '2022-01-01'
      AND visit_status = 'completed'

extraction_parameters:
  date_filter:
    column: "attendance_date"
    start: "2022-01-01"
    end: "2026-01-30"
  filters:
    - "visit_status = 'completed'"
  batch_size: 50000
  extraction_duration_seconds: 245.3

data_profile:
  row_count: 2,456,789
  column_count: 16
  file_size_mb: 567.8
  file_format: "parquet"
  compression: "snappy"
  date_range:
    min: "2022-01-01"
    max: "2026-01-28"

validation_summary:
  validation_timestamp: "2026-01-30T10:49:35+08:00"
  overall_status: "passed"  # or "passed_with_warnings", "failed"
  checks_performed: 5
  checks_passed: 4
  warnings: 1
  critical_failures: 0
  
  results:
    - check: "schema_validation"
      status: "passed"
      message: "All expected columns present"
    
    - check: "primary_key_uniqueness"
      status: "passed"
      message: "No duplicate attendance_ids found"
    
    - check: "null_validation"
      status: "passed"
      message: "No unexpected NULLs in critical columns"
    
    - check: "date_range_validation"
      status: "warning"
      severity: "low"
      message: "145 records with future dates (0.006%)"
      details:
        out_of_range_count: 145
        future_dates_max: "2026-02-05"
        recommended_action: "Review with data owner; may be scheduled appointments"
    
    - check: "row_count_validation"
      status: "passed"
      message: "Row count within expected range (2.5M rows)"

data_quality_notes:
  - "Future dates present: 145 records (0.006%) - likely scheduled appointments"
  - "Waiting times: range 0-480 minutes, median 23 minutes"
  - "Visit types distribution: acute (65%), chronic (25%), preventive (10%)"

lineage:
  upstream_systems:
    - "MOH CDMS (Clinical Data Management System)"
  extraction_tool: "Python 3.10.8 + pandas 2.0.3 + SQLAlchemy 2.0.15"
  extracted_by: "data_analyst_user"
  extraction_script: "scripts/data_extraction/extract_data.py"
  
next_processing_stage: "data_quality_assessment"
usage_notes: "This dataset is ready for exploratory data analysis. Review future dates before time-series analysis."
```


---

## Outputs

You will produce:

### 1. Extracted Datasets → `data/1_raw/`
- Raw data files in specified format (parquet, csv, delta)
- Naming convention: `{table_name}.{format}` (e.g., `polyclinic_attendances.parquet`)
- Partitioned by date if datasets are large (>100M rows)

### 2. Metadata Files → `data/1_raw/{table_name}.meta.yml`
Comprehensive metadata for each extracted dataset including:
- Source system details (database, schema, table, query used)
- Extraction parameters (date filters, batch size, duration)
- Data profile (row count, column count, file size, date ranges)
- Validation results (checks performed, pass/fail status, warnings)
- Data quality notes (observed issues, recommendations)
- Lineage information (upstream systems, tools used, who extracted)

### 3. Extraction Script → `scripts/data_extraction/`
Production-ready, reusable Python script with:
- Modular functions for connection, extraction, validation
- Comprehensive error handling and retry logic
- Progress logging and monitoring
- Configuration-driven design (easy to adapt for different tables)
- Command-line interface for easy execution

### 4. Extraction Configuration → `config/extraction_config.yml`
YAML configuration file specifying:
- Tables to extract with queries/filters
- Validation rules for each table
- Output format and directory settings
- Performance tuning parameters (batch size, parallelization)
- References to project context files for documentation

### 5. Extraction Report → `data/1_raw/extraction_report.md`
Human-readable summary including:
- Overall extraction statistics (success rate, total rows/size, duration)
- Per-table details (row counts, file sizes, durations)
- Validation results summary (passed/warnings/failures)
- Identified data quality issues
- Recommended next steps

### 6. Execution Logs → `results/execution_logs/extraction_{timestamp}.log`
Detailed technical logs containing:
- Timestamped execution steps
- Query execution details
- Batch processing progress
- Validation check results
- Errors and warnings with stack traces
- Performance metrics (memory usage, query times)

---

## Quality Assurance Checklist

Before marking extraction as complete, verify:

### Data Completeness
- [ ] All specified tables successfully extracted
- [ ] Row counts logged and match source (or explain discrepancies)
- [ ] No unexpected missing columns in extracted data
- [ ] Date ranges match filter specifications

### Data Integrity
- [ ] Primary keys are unique (no duplicates)
- [ ] File formats correct and files are readable
- [ ] No data corruption detected (checksums if applicable)
- [ ] Critical columns have no unexpected NULLs

### Documentation & Lineage
- [ ] Metadata files created for all datasets with complete information
- [ ] Extraction queries documented (copy of exact SQL/API call used)
- [ ] Data lineage traceable (source system → extraction script → raw file)
- [ ] Known data quality issues documented in metadata

### Validation & Quality
- [ ] Automated validation checks executed and results logged
- [ ] Critical validation failures addressed (not just logged)
- [ ] Warnings reviewed and assessed for impact
- [ ] Data profile statistics calculated (min/max dates, row counts, distinct values)

### Security & Compliance
- [ ] No credentials exposed in logs, scripts, or metadata files
- [ ] No raw PII in logs (patient names, IDs should be anonymized/redacted in logs)
- [ ] Extracted data stored in approved location with proper permissions
- [ ] Access logs recorded (who extracted, when, what data)

### Reproducibility & Maintainability
- [ ] Extraction script is parameterized (not hardcoded for one-time use)
- [ ] Configuration file makes it easy to adjust date ranges/tables
- [ ] Script can be run again with same results (deterministic)
- [ ] README or inline comments explain how to run the extraction

### Resource Management
- [ ] Disk space sufficient for downstream processing (at least 2x current data size free)
- [ ] Temporary files cleaned up
- [ ] Database connections properly closed
- [ ] Memory usage was within limits (no out-of-memory errors)

---

## Common Issues & Troubleshooting

### Connection Issues

| Error | Possible Causes | Solutions |
|-------|----------------|-----------|
| **Connection timeout** | Network latency, firewall, wrong host | • Check VPN connection<br>• Verify hostname/port in data_connections.md<br>• Test with `telnet {host} {port}`<br>• Implement retry logic with exponential backoff |
| **Authentication failed** | Wrong credentials, expired password | • Verify credentials in secure vault<br>• Check if account is locked<br>• Confirm access permissions with data owner<br>• Request credential refresh if expired |
| **SSL/TLS errors** | Certificate issues, version mismatch | • Check SSL requirements in data_connections.md<br>• Update connection string with SSL parameters<br>• Verify certificate validity |

### Performance Issues

| Issue | Impact | Solutions |
|-------|--------|-----------|
| **Query timeout** | Long-running queries exceed DB timeout | • Add date range partitioning (extract year by year)<br>• Use read-only views if available (pre-aggregated)<br>• Add indexes if you have write permissions<br>• Increase timeout parameter in connection string |
| **Out of memory** | Dataset too large for available RAM | • Reduce batch_size parameter (e.g., from 100k to 25k)<br>• Use streaming/chunked reading<br>• Switch to Spark for distributed processing<br>• Extract to CSV first, then convert to parquet |
| **Slow write speed** | Disk I/O bottleneck | • Use SSD instead of HDD if possible<br>• Write to local disk first, then transfer to network storage<br>• Enable compression (parquet with snappy)<br>• Use columnar formats (parquet vs CSV) |
| **Disk space full** | Large extracted datasets | • Clean up temporary files<br>• Compress extracted data<br>• Extract subset first (date range or column selection)<br>• Request additional storage allocation |

### Data Quality Issues

| Issue | Severity | Response Strategy |
|-------|----------|-------------------|
| **Duplicate primary keys** | 🔴 Critical | • **STOP EXTRACTION** - investigate source data<br>• Check if soft deletes exist (is_deleted flag)<br>• Verify if composite key needed<br>• Contact data owner for clarification |
| **Unexpected NULL values** | 🟡 Warning | • Document null rates in metadata<br>• Assess if NULLs are business-valid (optional fields)<br>• Plan imputation strategy for downstream analysis<br>• Continue extraction but flag for data quality stage |
| **Date values out of range** | 🟡 Warning | • Check if future dates are valid (scheduled appointments)<br>• Filter obviously invalid dates (year < 1900, > 2100)<br>• Document in metadata and report<br>• Continue extraction, handle in cleaning stage |
| **Missing expected columns** | 🔴 Critical | • **STOP EXTRACTION** - verify table name and version<br>• Check if schema changed recently<br>• Confirm you're querying correct database/schema<br>• Review data_sources.md for schema updates |
| **Row count mismatch** | 🟡 Warning | • Check if filters applied correctly<br>• Verify date range matches expectation<br>• Account for soft deletes or active flags<br>• Document discrepancy and investigate cause |

### API-Specific Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **Rate limit exceeded (429)** | Too many requests | • Implement exponential backoff<br>• Reduce request frequency<br>• Use batch endpoints if available<br>• Consider overnight extraction for large datasets |
| **Incomplete data returned** | API pagination issue | • Verify pagination logic (offset/limit)<br>• Check for cursor-based pagination<br>• Validate total count vs extracted count<br>• Handle edge cases (empty pages, end of data) |
| **API version deprecated** | Breaking changes in API | • Check API documentation for latest version<br>• Update endpoint URLs to new version<br>• Modify request/response parsing if needed |

---

## Execution Timeline Example

For a typical extraction of 3 tables (~5M rows total):

| Time | Activity | Duration |
|------|----------|----------|
| T+0min | Context discovery (review docs) | 15 min |
| T+15min | Design extraction approach | 10 min |
| T+25min | Create extraction config | 5 min |
| T+30min | Test database connectivity | 2 min |
| T+32min | Run extraction script | 30 min |
| T+62min | Validate extracted data | 10 min |
| T+72min | Generate metadata & reports | 3 min |
| **Total** | **End-to-end extraction** | **~75 min** |

**Note**: Times vary based on data volume, network speed, and data source performance.

---

## Success Criteria

Extraction is considered **successful** when:

1. ✅ All required datasets extracted with zero critical validation failures
2. ✅ Row counts within expected ranges (±10% tolerance documented)
3. ✅ Primary keys are unique across all extracted tables
4. ✅ Comprehensive metadata files exist for every dataset
5. ✅ Extraction report generated and clearly shows status
6. ✅ No sensitive data (credentials, raw PII) exposed in logs or configs
7. ✅ Data files are readable and not corrupted
8. ✅ Disk space available for downstream processing (at least 50% free)
9. ✅ Extraction process is documented and reproducible
10. ✅ All warnings assessed and documented (not just ignored)

---

## Next Stage Transition

After successful extraction, prepare for **Data Quality Assessment**:

### Handoff Deliverables
1. **Raw data files** in `data/1_raw/` with metadata
2. **Extraction report** highlighting any warnings or issues
3. **Data dictionary updates** (if actual schema differs from documentation)
4. **Known issues list** for the QA team to investigate

### Recommended Next Actions
1. Update `docs/data_dictionary/` with actual column names, types, and distributions
2. Share extraction report with project stakeholders
3. Archive extraction scripts for reproducibility
4. Schedule incremental extraction (if needed for daily updates)
5. Begin exploratory data analysis in `notebooks/1_exploratory/`

### Communication Template

```
Subject: Data Extraction Complete - [Project Name] - [Date]

Team,

Data extraction has been successfully completed for [User Story ID].

📊 **Summary**:
- Tables extracted: [list]
- Total rows: [count]
- Total size: [MB/GB]
- Extraction duration: [time]
- Status: [Success / Partial Success / Issues]

📁 **Outputs**:
- Raw data: `data/1_raw/`
- Extraction report: `data/1_raw/extraction_report.md`
- Logs: `results/execution_logs/extraction_[timestamp].log`

⚠️  **Issues Noted**:
- [List any warnings or data quality concerns]

➡️  **Next Steps**:
- Data quality assessment
- [Any specific follow-up actions]

Please review the extraction report and let me know if you have any questions.

[Your Name]
```

---

## Adaptability Notes

This prompt is designed to be **project-agnostic**. To adapt for a different project:

### Essential Customization Points

1. **Update `docs/project_context/` references** throughout this document to match your project's structure

2. **Modify default parameters** in Decision Framework section:
   ```yaml
   # Project-specific defaults
   output_dir: "[your-project's-raw-data-directory]"
   output_format: "[your-preferred-format]"
   batch_size: "[optimized-for-your-environment]"
   ```

3. **Customize validation rules** based on your data domain:
   - Healthcare: HIPAA compliance, patient ID anonymization
   - Finance: transaction amount ranges, account validation
   - E-commerce: product ID references, order status validity

4. **Adjust Quality Assurance Checklist** with domain-specific requirements:
   - Add industry-specific compliance checks
   - Include project-specific data governance rules
   - Modify validation thresholds for your data characteristics

5. **Update code examples** to match your tech stack:
   - If using R primarily, provide R implementations
   - If using Spark extensively, emphasize Spark SQL approach
   - If API-based, focus on API client patterns

### Project Context Template

For any new project, ensure `docs/project_context/` contains:

```
docs/project_context/
├── data_sources.md          # Table schemas, relationships, volumes
├── data_connections.md      # Connection methods, credentials, access patterns
├── tech_stack.md            # Tools, platforms, languages, libraries
└── compliance_requirements.md  # Privacy, security, regulatory needs
```

Each file should follow a consistent structure across projects for this prompt to work effectively.
