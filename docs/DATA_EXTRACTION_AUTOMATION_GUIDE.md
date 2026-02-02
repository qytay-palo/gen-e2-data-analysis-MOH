# Data Extraction Automation Guide
## Singapore Health Dataset - Kaggle

**Version:** 1.0  
**Last Updated:** 30 January 2026  
**Target Audience:** Data Analysts, Data Engineers, Automation Developers

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Dataset Structure](#dataset-structure)
4. [Extraction Patterns](#extraction-patterns)
5. [Automated ETL Pipeline](#automated-etl-pipeline)
6. [Data Validation](#data-validation)
7. [Error Handling](#error-handling)
8. [Scheduling](#scheduling)
9. [Best Practices](#best-practices)

---

## Overview

This guide provides comprehensive instructions for automating data extraction from the Singapore Health Dataset hosted on Kaggle.

### Dataset Information

- **Kaggle ID:** `subhamjain/health-dataset-complete-singapore`
- **Total Files:** 70 (35 data tables, 28 metadata files, 1 PDF report, 6 other)
- **Format:** Primarily CSV files
- **Size:** ~3.5 MB total
- **Update Frequency:** Annual (typically)

---

## Prerequisites

### 1. Software Requirements

```bash
# Required Python version
Python 3.7+

# Required packages
pip install kagglehub pandas openpyxl sqlalchemy psycopg2-binary pyyaml
```

### 2. Kaggle API Setup

**Option A: API Key File (Recommended)**

1. Login to Kaggle: https://www.kaggle.com
2. Go to Account Settings → API → Create New API Token
3. Download `kaggle.json`
4. Place in home directory:
   ```bash
   mkdir -p ~/.kaggle
   mv ~/Downloads/kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```

**Option B: Environment Variables**

```bash
export KAGGLE_USERNAME="your_username"
export KAGGLE_KEY="your_api_key"
```

### 3. Database Setup (Optional)

If loading data into a database:

```yaml
# config/database.yml
database:
  host: localhost
  port: 5432
  name: moh_health_data
  user: analyst
  password: ${DB_PASSWORD}
```

---

## Dataset Structure

### File Organization

```
dataset_root/
├── common-health-problems-in-students-defective-vision-annual/
│   └── common-health-problems-of-students-examined-defective-vision-annual.csv
├── common-health-problems-in-students-obesity-annual/
│   ├── common-health-problems-of-students-examined-obesity-annual.csv
│   └── metadata-common-health-problems-of-students-examined-obesity-annual.txt
├── number-of-doctors/
│   ├── number-of-doctors.csv
│   └── metadata-number-of-doctors.txt
├── [... 32 more table directories ...]
└── national-nutrition-survey-2010-report.pdf
```

### Table Categories

| Category | # Tables | Primary Use |
|----------|----------|-------------|
| Healthcare Workforce | 7 | Capacity planning, workforce analytics |
| Healthcare Facilities | 4 | Infrastructure planning, capacity analysis |
| Health Outcomes | 3 | Disease burden, mortality trends |
| Public Health | 6 | Prevention programs, school health |
| Healthcare Utilization | 3 | Demand forecasting, resource allocation |
| Expenditure | 1 | Budget planning, financial analysis |
| Nutrition | 3 | Population health, dietary patterns |

---

## Extraction Patterns

### Pattern 1: Single Table Extraction

```python
import kagglehub
import pandas as pd

def extract_single_table(table_subdir: str, filename: str) -> pd.DataFrame:
    """
    Extract a single table from the Kaggle dataset.
    
    Args:
        table_subdir: Subdirectory name (e.g., 'number-of-doctors')
        filename: CSV filename
    
    Returns:
        DataFrame with the table data
    """
    dataset_path = kagglehub.dataset_download(
        "subhamjain/health-dataset-complete-singapore"
    )
    
    file_path = f"{dataset_path}/{table_subdir}/{filename}"
    df = pd.read_csv(file_path)
    
    # Add metadata
    df['_source_file'] = filename
    df['_extraction_timestamp'] = pd.Timestamp.now()
    
    return df

# Example usage
doctors_df = extract_single_table('number-of-doctors', 'number-of-doctors.csv')
print(f"Extracted {len(doctors_df)} records")
```

### Pattern 2: Bulk Extraction with Metadata

```python
import os
from pathlib import Path
from typing import Dict

def extract_all_tables() -> Dict[str, pd.DataFrame]:
    """
    Extract all CSV tables from the dataset.
    
    Returns:
        Dictionary mapping table names to DataFrames
    """
    dataset_path = kagglehub.dataset_download(
        "subhamjain/health-dataset-complete-singapore"
    )
    
    tables = {}
    extraction_log = []
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                table_name = file.replace('.csv', '')
                
                try:
                    df = pd.read_csv(file_path)
                    
                    # Add metadata columns
                    df['_source_file'] = file
                    df['_source_directory'] = os.path.basename(root)
                    df['_extraction_timestamp'] = pd.Timestamp.now()
                    df['_record_count'] = len(df)
                    
                    tables[table_name] = df
                    
                    extraction_log.append({
                        'table_name': table_name,
                        'file_path': file_path,
                        'records': len(df),
                        'columns': df.shape[1],
                        'status': 'success'
                    })
                    
                    print(f"✓ Loaded {table_name}: {len(df)} rows × {df.shape[1]} cols")
                    
                except Exception as e:
                    extraction_log.append({
                        'table_name': table_name,
                        'file_path': file_path,
                        'status': 'error',
                        'error': str(e)
                    })
                    print(f"✗ Failed to load {table_name}: {e}")
    
    # Save extraction log
    log_df = pd.DataFrame(extraction_log)
    log_df.to_csv('logs/etl/extraction_log.csv', index=False)
    
    return tables

# Usage
all_tables = extract_all_tables()
print(f"\nTotal tables extracted: {len(all_tables)}")
```

### Pattern 3: Incremental Extraction with Change Detection

```python
import hashlib
import json
from datetime import datetime

class IncrementalExtractor:
    """Handle incremental data extraction with change detection."""
    
    def __init__(self, state_file: str = 'data/.extraction_state.json'):
        self.state_file = state_file
        self.state = self._load_state()
    
    def _load_state(self) -> dict:
        """Load previous extraction state."""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_state(self):
        """Save current extraction state."""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def _calculate_hash(self, file_path: str) -> str:
        """Calculate file hash for change detection."""
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    
    def extract_if_changed(self, table_subdir: str, filename: str) -> tuple:
        """
        Extract table only if it has changed since last extraction.
        
        Returns:
            (DataFrame or None, bool indicating if changed)
        """
        dataset_path = kagglehub.dataset_download(
            "subhamjain/health-dataset-complete-singapore"
        )
        file_path = f"{dataset_path}/{table_subdir}/{filename}"
        
        current_hash = self._calculate_hash(file_path)
        table_key = f"{table_subdir}/{filename}"
        
        # Check if file has changed
        if table_key in self.state:
            if self.state[table_key]['hash'] == current_hash:
                print(f"⊘ Skipped {filename} (no changes)")
                return None, False
        
        # File is new or changed, extract it
        df = pd.read_csv(file_path)
        
        # Update state
        self.state[table_key] = {
            'hash': current_hash,
            'last_extracted': datetime.now().isoformat(),
            'records': len(df)
        }
        self._save_state()
        
        print(f"↻ Extracted {filename} ({len(df)} records)")
        return df, True
    
    def extract_all_changed(self) -> Dict[str, pd.DataFrame]:
        """Extract all tables that have changed."""
        dataset_path = kagglehub.dataset_download(
            "subhamjain/health-dataset-complete-singapore"
        )
        
        changed_tables = {}
        
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith('.csv'):
                    subdir = os.path.basename(root)
                    df, changed = self.extract_if_changed(subdir, file)
                    
                    if changed:
                        table_name = file.replace('.csv', '')
                        changed_tables[table_name] = df
        
        return changed_tables

# Usage
extractor = IncrementalExtractor()
changed_tables = extractor.extract_all_changed()
print(f"\n{len(changed_tables)} tables have changed since last extraction")
```

---

## Automated ETL Pipeline

### Complete ETL Pipeline Example

```python
# scripts/kaggle_etl_pipeline.py

import kagglehub
import pandas as pd
import sqlalchemy
from typing import Dict, List
import yaml
import logging
from datetime import datetime

class KaggleHealthDataETL:
    """Complete ETL pipeline for Singapore Health Dataset."""
    
    def __init__(self, config_path: str = 'config/database.yml'):
        self.config = self._load_config(config_path)
        self.setup_logging()
        self.dataset_name = "subhamjain/health-dataset-complete-singapore"
    
    def _load_config(self, config_path: str) -> dict:
        """Load database configuration."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def setup_logging(self):
        """Configure logging."""
        logging.basicConfig(
            filename=f'logs/etl/kaggle_etl_{datetime.now():%Y%m%d}.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def extract(self) -> Dict[str, pd.DataFrame]:
        """
        EXTRACT: Download and read all CSV files from Kaggle.
        """
        self.logger.info("Starting extraction phase")
        
        dataset_path = kagglehub.dataset_download(self.dataset_name)
        self.logger.info(f"Dataset downloaded to: {dataset_path}")
        
        tables = {}
        
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith('.csv'):
                    try:
                        file_path = os.path.join(root, file)
                        df = pd.read_csv(file_path)
                        table_name = file.replace('.csv', '').replace('-', '_')
                        tables[table_name] = df
                        
                        self.logger.info(
                            f"Extracted {table_name}: {len(df)} rows"
                        )
                    except Exception as e:
                        self.logger.error(
                            f"Failed to extract {file}: {str(e)}"
                        )
        
        self.logger.info(f"Extraction complete: {len(tables)} tables")
        return tables
    
    def transform(self, tables: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """
        TRANSFORM: Clean and standardize data.
        """
        self.logger.info("Starting transformation phase")
        
        transformed = {}
        
        for table_name, df in tables.items():
            try:
                df_clean = df.copy()
                
                # Standardize column names
                df_clean.columns = [
                    col.lower().replace(' ', '_').replace('-', '_')
                    for col in df_clean.columns
                ]
                
                # Convert year columns to int (if present)
                for col in df_clean.columns:
                    if 'year' in col and df_clean[col].dtype == 'object':
                        df_clean[col] = pd.to_numeric(
                            df_clean[col], errors='coerce'
                        )
                
                # Add audit columns
                df_clean['_etl_timestamp'] = datetime.now()
                df_clean['_source_table'] = table_name
                df_clean['_source_dataset'] = self.dataset_name
                
                transformed[table_name] = df_clean
                
                self.logger.info(f"Transformed {table_name}")
                
            except Exception as e:
                self.logger.error(
                    f"Failed to transform {table_name}: {str(e)}"
                )
        
        self.logger.info(f"Transformation complete: {len(transformed)} tables")
        return transformed
    
    def load(self, tables: Dict[str, pd.DataFrame], schema: str = 'kaggle'):
        """
        LOAD: Write data to database.
        """
        self.logger.info("Starting load phase")
        
        # Create database connection
        db_config = self.config['database']
        engine = sqlalchemy.create_engine(
            f"postgresql://{db_config['user']}:{db_config['password']}"
            f"@{db_config['host']}:{db_config['port']}/{db_config['name']}"
        )
        
        # Create schema if not exists
        with engine.connect() as conn:
            conn.execute(sqlalchemy.text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
            conn.commit()
        
        # Load each table
        for table_name, df in tables.items():
            try:
                df.to_sql(
                    name=table_name,
                    con=engine,
                    schema=schema,
                    if_exists='replace',
                    index=False,
                    method='multi',
                    chunksize=1000
                )
                
                self.logger.info(
                    f"Loaded {table_name} to {schema}.{table_name}: "
                    f"{len(df)} rows"
                )
                
            except Exception as e:
                self.logger.error(
                    f"Failed to load {table_name}: {str(e)}"
                )
        
        self.logger.info("Load phase complete")
    
    def run(self):
        """Execute complete ETL pipeline."""
        self.logger.info("=" * 80)
        self.logger.info("Starting Kaggle Health Data ETL Pipeline")
        self.logger.info("=" * 80)
        
        try:
            # Extract
            tables = self.extract()
            
            # Transform
            tables = self.transform(tables)
            
            # Load
            self.load(tables)
            
            self.logger.info("ETL Pipeline completed successfully")
            
        except Exception as e:
            self.logger.error(f"ETL Pipeline failed: {str(e)}")
            raise

# Usage
if __name__ == "__main__":
    etl = KaggleHealthDataETL()
    etl.run()
```

---

## Data Validation

### Validation Rules

```python
class DataValidator:
    """Validate extracted data quality."""
    
    def __init__(self):
        self.validation_rules = self._load_rules()
    
    def _load_rules(self) -> dict:
        """Load validation rules from config."""
        return {
            'number_of_doctors': {
                'required_columns': ['year', 'sector', 'count'],
                'min_year': 2006,
                'max_year': 2025,
                'sectors': ['Public', 'Private', 'Not In Active Practice'],
                'count_min': 0,
                'count_max': 50000
            },
            'government_health_expenditure': {
                'required_columns': ['financial_year', 'government_health_expenditure'],
                'min_year': 2000,
                'expenditure_min': 0,
                'expenditure_max': 50000  # millions SGD
            },
            # Add rules for other tables...
        }
    
    def validate_table(self, table_name: str, df: pd.DataFrame) -> dict:
        """
        Validate a single table.
        
        Returns:
            Dictionary with validation results
        """
        results = {
            'table_name': table_name,
            'passed': True,
            'issues': []
        }
        
        if table_name not in self.validation_rules:
            results['issues'].append("No validation rules defined")
            return results
        
        rules = self.validation_rules[table_name]
        
        # Check required columns
        if 'required_columns' in rules:
            missing = set(rules['required_columns']) - set(df.columns)
            if missing:
                results['passed'] = False
                results['issues'].append(f"Missing columns: {missing}")
        
        # Check year range
        if 'min_year' in rules and 'year' in df.columns:
            invalid_years = df[
                (df['year'] < rules['min_year']) | 
                (df['year'] > rules.get('max_year', 2100))
            ]
            if len(invalid_years) > 0:
                results['passed'] = False
                results['issues'].append(
                    f"Invalid years: {invalid_years['year'].tolist()}"
                )
        
        # Check value ranges
        for col, min_val in [(k, v) for k, v in rules.items() if k.endswith('_min')]:
            col_name = col.replace('_min', '')
            if col_name in df.columns:
                invalid = df[df[col_name] < min_val]
                if len(invalid) > 0:
                    results['passed'] = False
                    results['issues'].append(
                        f"{col_name} has values < {min_val}"
                    )
        
        # Check for nulls in critical columns
        for col in rules.get('required_columns', []):
            if col in df.columns:
                null_count = df[col].isna().sum()
                if null_count > 0:
                    results['passed'] = False
                    results['issues'].append(
                        f"{col} has {null_count} null values"
                    )
        
        return results
    
    def validate_all(self, tables: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Validate all tables and return summary."""
        validation_results = []
        
        for table_name, df in tables.items():
            result = self.validate_table(table_name, df)
            validation_results.append(result)
        
        return pd.DataFrame(validation_results)

# Usage
validator = DataValidator()
validation_summary = validator.validate_all(all_tables)
print(validation_summary)

# Save validation report
validation_summary.to_csv('reports/data_validation_report.csv', index=False)
```

---

## Error Handling

### Robust Error Handling Patterns

```python
import traceback
from typing import Optional

def safe_extract(table_subdir: str, filename: str) -> Optional[pd.DataFrame]:
    """Extract with comprehensive error handling."""
    try:
        dataset_path = kagglehub.dataset_download(
            "subhamjain/health-dataset-complete-singapore"
        )
        file_path = f"{dataset_path}/{table_subdir}/{filename}"
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        df = pd.read_csv(file_path)
        
        if df.empty:
            raise ValueError(f"File is empty: {filename}")
        
        return df
        
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return None
    
    except pd.errors.EmptyDataError:
        logging.error(f"Empty CSV file: {filename}")
        return None
    
    except pd.errors.ParserError as e:
        logging.error(f"CSV parsing error in {filename}: {e}")
        return None
    
    except Exception as e:
        logging.error(f"Unexpected error extracting {filename}: {e}")
        logging.error(traceback.format_exc())
        return None

# Retry logic
from functools import wraps
import time

def retry(max_attempts=3, delay=5):
    """Decorator for retrying failed operations."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logging.warning(
                        f"Attempt {attempt + 1} failed: {e}. "
                        f"Retrying in {delay}s..."
                    )
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=10)
def extract_with_retry(table_subdir: str, filename: str) -> pd.DataFrame:
    """Extract data with automatic retry on failure."""
    return safe_extract(table_subdir, filename)
```

---

## Scheduling

### Option 1: Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Run ETL daily at 2 AM
0 2 * * * cd /path/to/project && source venv/bin/activate && python scripts/kaggle_etl_pipeline.py >> logs/etl/cron.log 2>&1

# Run ETL weekly on Sunday at 3 AM
0 3 * * 0 cd /path/to/project && source venv/bin/activate && python scripts/kaggle_etl_pipeline.py
```

### Option 2: Python Schedule Library

```python
# scripts/run_scheduler.py

import schedule
import time
from kaggle_etl_pipeline import KaggleHealthDataETL

def run_etl():
    """Execute ETL pipeline."""
    print(f"Starting ETL at {datetime.now()}")
    try:
        etl = KaggleHealthDataETL()
        etl.run()
        print("ETL completed successfully")
    except Exception as e:
        print(f"ETL failed: {e}")

# Schedule ETL
schedule.every().day.at("02:00").do(run_etl)  # Daily at 2 AM
# schedule.every().sunday.at("03:00").do(run_etl)  # Weekly on Sunday

print("Scheduler started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

### Option 3: Airflow DAG

```python
# dags/kaggle_health_etl_dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'kaggle_health_data_etl',
    default_args=default_args,
    description='Extract Singapore Health Data from Kaggle',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False,
)

def extract_task():
    from kaggle_etl_pipeline import KaggleHealthDataETL
    etl = KaggleHealthDataETL()
    return etl.extract()

def transform_task(**context):
    from kaggle_etl_pipeline import KaggleHealthDataETL
    etl = KaggleHealthDataETL()
    tables = context['task_instance'].xcom_pull(task_ids='extract')
    return etl.transform(tables)

def load_task(**context):
    from kaggle_etl_pipeline import KaggleHealthDataETL
    etl = KaggleHealthDataETL()
    tables = context['task_instance'].xcom_pull(task_ids='transform')
    etl.load(tables)

t1 = PythonOperator(
    task_id='extract',
    python_callable=extract_task,
    dag=dag,
)

t2 = PythonOperator(
    task_id='transform',
    python_callable=transform_task,
    provide_context=True,
    dag=dag,
)

t3 = PythonOperator(
    task_id='load',
    python_callable=load_task,
    provide_context=True,
    dag=dag,
)

t1 >> t2 >> t3
```

---

## Best Practices

### 1. Configuration Management

```yaml
# config/extraction.yml
kaggle:
  dataset: "subhamjain/health-dataset-complete-singapore"
  cache_dir: "~/.kaggle_cache"
  
extraction:
  batch_size: 10
  retry_attempts: 3
  retry_delay: 5
  
tables:
  priority_tables:
    - number-of-doctors
    - government-health-expenditure
    - hospital-admission-rate-by-age-and-sex
  
  exclude_tables:
    - metadata-*.txt
    - "*.pdf"
```

### 2. Monitoring and Alerts

```python
class ETLMonitor:
    """Monitor ETL execution and send alerts."""
    
    def __init__(self):
        self.metrics = {
            'start_time': None,
            'end_time': None,
            'tables_extracted': 0,
            'tables_failed': 0,
            'total_records': 0,
            'errors': []
        }
    
    def send_alert(self, subject: str, message: str):
        """Send email alert (implement based on your email system)."""
        # Implementation here
        pass
    
    def generate_report(self) -> str:
        """Generate ETL execution report."""
        duration = (self.metrics['end_time'] - self.metrics['start_time']).total_seconds()
        
        report = f"""
        ETL Execution Report
        ====================
        Start Time: {self.metrics['start_time']}
        End Time: {self.metrics['end_time']}
        Duration: {duration:.2f} seconds
        
        Tables Extracted: {self.metrics['tables_extracted']}
        Tables Failed: {self.metrics['tables_failed']}
        Total Records: {self.metrics['total_records']:,}
        
        Errors: {len(self.metrics['errors'])}
        """
        
        if self.metrics['errors']:
            report += "\n\nError Details:\n"
            for error in self.metrics['errors']:
                report += f"  - {error}\n"
        
        return report
```

### 3. Data Versioning

```python
import shutil
from datetime import datetime

class DataVersionManager:
    """Manage data versions for reproducibility."""
    
    def __init__(self, base_dir: str = 'data/versions'):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
    
    def save_version(self, tables: Dict[str, pd.DataFrame]):
        """Save current version of all tables."""
        version_dir = f"{self.base_dir}/{datetime.now():%Y%m%d_%H%M%S}"
        os.makedirs(version_dir, exist_ok=True)
        
        for table_name, df in tables.items():
            df.to_csv(f"{version_dir}/{table_name}.csv", index=False)
        
        # Save metadata
        metadata = {
            'version': datetime.now().isoformat(),
            'tables': list(tables.keys()),
            'record_counts': {k: len(v) for k, v in tables.items()}
        }
        
        with open(f"{version_dir}/metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Version saved to: {version_dir}")
```

### 4. Performance Optimization

```python
# Use multiprocessing for parallel extraction
from multiprocessing import Pool
from functools import partial

def parallel_extract(tables_list: List[tuple], num_workers: int = 4):
    """Extract multiple tables in parallel."""
    with Pool(num_workers) as pool:
        results = pool.starmap(extract_single_table, tables_list)
    return dict(zip([t[1] for t in tables_list], results))

# Use chunking for large datasets
def load_large_table(df: pd.DataFrame, table_name: str, engine, chunk_size=10000):
    """Load large table in chunks to avoid memory issues."""
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        chunk.to_sql(
            name=table_name,
            con=engine,
            if_exists='append' if i > 0 else 'replace',
            index=False
        )
        print(f"Loaded chunk {i//chunk_size + 1}: {len(chunk)} records")
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Missing/invalid Kaggle credentials | Check `~/.kaggle/kaggle.json` |
| `FileNotFoundError` | Dataset structure changed | Re-run exploration script |
| `MemoryError` | Large dataset | Use chunking, increase memory |
| `ConnectionError` | Network issues | Implement retry logic |
| `SQLAlchemyError` | Database connection | Check database config |

---

## Additional Resources

- **Kaggle Hub Documentation:** https://github.com/Kaggle/kagglehub
- **Project Data Catalog:** [COMPREHENSIVE_DATA_CATALOG.md](./data_dictionary/COMPREHENSIVE_DATA_CATALOG.md)
- **ETL Pipeline Script:** [scripts/kaggle_etl_pipeline.py](../scripts/kaggle_etl_pipeline.py)

---

**Document Version:** 1.0  
**Last Updated:** 30 January 2026  
**Maintainer:** Data Analytics Team
