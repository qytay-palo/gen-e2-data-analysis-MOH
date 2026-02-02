# Prompt: Execute Programming Implementation Plan

## Role
You are a senior data analytics developer with expertise in writing production-grade, maintainable code. Your task is to execute a programming implementation plan by generating, organizing, and deploying code across the project structure.

---

## Input Requirements

Before starting, locate these files:
- **Implementation Plan**: `docs/methodology/implementation_plans/epic-{NUMBER}-*-implementation-plan.md`
- **Data Sources**: `docs/project_context/data_sources.md` - Database schemas, table structures, data characteristics, access methods. This document defines WHAT data to extract and WHERE it comes from. Read this FIRST before generating any extraction code.
- **Tech Stack**: `docs/project_context/tech_stack.md`
- **Epic Structure**: `epics/epic-{NUMBER}/README.md`

---

## Your Task

Systematically implement the plan by generating all required code, configurations, and documentation. Follow the implementation plan's structure and phases.

**CRITICAL FIRST STEP**: Before generating any data extraction code, thoroughly analyze `docs/project_context/data_sources.md` to understand:
- What data sources are available (databases, APIs, files, etc.)
- Table/collection structures and schemas
- Required fields and relationships
- Data volume and access patterns
- Any specific extraction requirements or constraints

Your extraction code MUST be tailored to the actual data sources specified in the project context.

---

## Phase 0: Data Source Analysis & Extraction Method Identification

**MANDATORY FIRST STEP**: Read `docs/project_context/data_sources.md` completely and identify:

### Step 0.1: Identify Data Source Type(s)

Analyze the data sources document to determine which extraction methods are needed:

| Source Type | Indicators in data_sources.md | Required Libraries | Skip SQL Phase? |
|-------------|-------------------------------|-------------------|------------------|
| **Kaggle Dataset** | - Mentions "kagglehub" API<br>- References Kaggle URLs<br>- Shows `.dataset_download()` examples<br>- CSV files from Kaggle | `kagglehub`, `pandas` | ✅ YES - Skip Phase 4 |
| **SQL Database** | - Connection strings (PostgreSQL, MySQL, SQL Server)<br>- Shows database credentials<br>- SQL query examples<br>- Table schemas with PRIMARY KEY/FOREIGN KEY | `psycopg2`, `sqlalchemy`, `pyodbc` | ❌ NO - Use Phase 4 |
| **NoSQL Database** | - MongoDB connection strings<br>- Collection names (not tables)<br>- Document structure examples<br>- Shows `pymongo` usage | `pymongo`, `motor` | ✅ YES - Skip Phase 4 |
| **REST APIs** | - API endpoints (https://api...)<br>- Authentication tokens/keys<br>- Rate limits mentioned<br>- JSON response examples | `requests`, `aiohttp` | ✅ YES - Skip Phase 4 |
| **Cloud Storage** | - S3 buckets, Azure Blob, GCS paths<br>- Shows `boto3` or cloud SDK usage<br>- Parquet/CSV in cloud storage | `boto3`, `azure-storage-blob`, `gcsfs` | ✅ YES - Skip Phase 4 |
| **Local Files** | - File paths like `data/raw/*.csv`<br>- Excel, JSON, Parquet files<br>- No remote connections | `pandas`, `openpyxl`, `pyarrow` | ✅ YES - Skip Phase 4 |
| **Data Warehouse** | - Snowflake, BigQuery, Redshift<br>- Warehouse-specific connectors<br>- SQL-like but cloud-native | Warehouse-specific SDKs | ⚠️ PARTIAL - Use warehouse SDK, not raw SQL |

### Step 0.2: Document Your Findings

Before generating ANY code, create a summary:

```
DATA SOURCE ANALYSIS SUMMARY:
============================
Primary Source Type: [e.g., Kaggle Dataset]
Secondary Sources: [e.g., None]
Extraction Method: [e.g., kagglehub API with CSV loading]
SQL Phase Applicable: [YES/NO]
Required Libraries: [e.g., kagglehub, pandas, pathlib]
Connection Pattern: [e.g., Download cached dataset, load CSVs by path]
File Format: [e.g., CSV files]
Total Tables/Files: [e.g., 35 CSV files]
Schema Source: [e.g., Documented in data_sources.md with sample records]
```

### Step 0.3: Adjust Implementation Phases

Based on your analysis:

- **If Kaggle/Files/APIs detected**: 
  - ✅ Implement Phase 2.1 with appropriate API/file loading code
  - ❌ SKIP Phase 4 (SQL Queries) entirely
  - ✅ Use pandas for data manipulation
  
- **If SQL Database detected**:
  - ✅ Implement Phase 2.1 with database connectors
  - ✅ KEEP Phase 4 (SQL Queries)
  - ✅ Use SQLAlchemy or similar ORMs

- **If Mixed Sources**:
  - ✅ Implement multiple extraction modules (one per source type)
  - ⚠️ Implement Phase 4 only for SQL sources
  - ✅ Create unified data loading interface

---

## Implementation Approach

### Phase 1: Setup & Structure

#### 1.1 Create/Verify Directory Structure
- Create all directories specified in the implementation plan
- Ensure proper separation of concerns (src, tests, config, scripts, notebooks)
- Create `__init__.py` files for Python packages
- Set up logging directories if specified

#### 1.2 Generate Configuration Files
Based on `config/` specifications in the plan, create:
- `config/database.yml` or `.yaml`: Database connections, credentials placeholders
- `config/analysis.yml`: Model parameters, feature lists, thresholds
- `config/platform.yml`: Computing environment settings
- `config/queries.yml`: Parameterized SQL query templates (or create `sql/` folder)
- `config/.env.template`: Environment variable template

**Requirements:**
- Use secure credential management (environment variables, never hardcode)
- Include clear comments explaining each configuration parameter
- Provide example values where helpful
- Support multiple environments (dev, staging, prod) if specified

#### 1.3 Create Requirements/Environment Files
- Generate `requirements.txt` with all dependencies and versions
- OR `environment.yml` for conda environments
- Include development dependencies separately if needed
- Pin versions for reproducibility

---

### Phase 2: Core Module Implementation

For each module specified in the implementation plan:

#### 2.1 Data Processing Module (`src/data_processing/`)

**Files to Create:**
- `__init__.py`: Package initialization, export public APIs
- `db_connector.py`: Database connection management
- `data_extractor.py`: Data extraction functions
- `data_validator.py`: Data quality validation
- `etl_pipeline.py`: End-to-end ETL orchestration

**Implementation Requirements:**

**`db_connector.py`:**
```python
# Should include:
# - Connection pooling
# - Context managers for safe connection handling
# - Retry logic with exponential backoff
# - Support for multiple database types (based on tech_stack.md)
# - Logging of connection events
# - Error handling with specific exceptions
```

**`data_extractor.py`:**

**BEFORE WRITING CODE**: Read `project_context/data_sources.md` to identify:
- All data sources (PostgreSQL, MySQL, MongoDB, CSV files, APIs, Kaggle, etc.)
- Table/collection names and their schemas
- Required columns/fields for extraction
- Join requirements between tables
- Date ranges and filtering criteria

**Generate extraction functions based on identified data sources:**

```python
# Should include:
# - One extraction function per data source/table identified in data_sources.md
# - Source-specific connection handling (SQL databases, NoSQL, APIs, files)
# - Schema-aware queries that match the table structures in data_sources.md
# - Incremental extraction with checkpoint management
# - Query parameterization from config files
# - Data type enforcement matching source schemas
# - Progress tracking for large extractions
# - Export to specified file formats (CSV, Parquet, etc.)
# - Error handling for missing tables or fields
#
# Example structure:
# def extract_patient_data(conn, start_date, end_date, output_path):
#     """Extract patient data from patients table."""
#     query = """
#         SELECT patient_id, admission_date, diagnosis_code, facility_id
#         FROM patients
#         WHERE admission_date BETWEEN %s AND %s
#     """
#     # Implementation...
#
# def extract_facility_data(conn, output_path):
#     """Extract facility data from facilities table."""
#     # Implementation...
```

**Code Generation Rules (AFTER completing Phase 0 analysis):**

1. **Match the extraction pattern to the identified source type:**
   
   **For Kaggle Datasets:**
   ```python
   import kagglehub
   from pathlib import Path
   import pandas as pd
   
   def extract_{table_name}(dataset_id: str, output_path: Path) -> pd.DataFrame:
       """Extract {table_name} from Kaggle dataset."""
       # Download dataset (cached)
       dataset_path = Path(kagglehub.dataset_download(dataset_id))
       
       # Load specific CSV file
       file_path = dataset_path / "{folder_name}" / "{file_name}.csv"
       df = pd.read_csv(file_path)
       
       # Validation and return
       logger.info(f"Extracted {len(df)} records from {table_name}")
       return df
   ```

   **For SQL Databases:**
   ```python
   import pandas as pd
   from sqlalchemy import create_engine
   
   def extract_{table_name}(conn, start_date, end_date) -> pd.DataFrame:
       """Extract {table_name} from database."""
       query = """
           SELECT column1, column2, column3
           FROM {table_name}
           WHERE date_column BETWEEN %s AND %s
       """
       df = pd.read_sql(query, conn, params=(start_date, end_date))
       logger.info(f"Extracted {len(df)} records from {table_name}")
       return df
   ```

   **For REST APIs:**
   ```python
   import requests
   import pandas as pd
   
   def extract_{endpoint_name}(api_url: str, api_key: str) -> pd.DataFrame:
       """Extract data from API endpoint."""
       headers = {"Authorization": f"Bearer {api_key}"}
       response = requests.get(api_url, headers=headers)
       response.raise_for_status()
       
       data = response.json()
       df = pd.DataFrame(data['results'])
       logger.info(f"Extracted {len(df)} records from API")
       return df
   ```

   **For Local Files:**
   ```python
   import pandas as pd
   from pathlib import Path
   
   def extract_{file_name}(file_path: Path) -> pd.DataFrame:
       """Extract data from local file."""
       if file_path.suffix == '.csv':
           df = pd.read_csv(file_path)
       elif file_path.suffix in ['.xlsx', '.xls']:
           df = pd.read_excel(file_path)
       elif file_path.suffix == '.parquet':
           df = pd.read_parquet(file_path)
       elif file_path.suffix == '.json':
           df = pd.read_json(file_path)
       else:
           raise ValueError(f"Unsupported file format: {file_path.suffix}")
       
       logger.info(f"Extracted {len(df)} records from {file_path.name}")
       return df
   ```

2. Use EXACT table/file names from `data_sources.md`
3. Match data types to schemas provided
4. Include all fields required for analysis (check implementation plan)
5. Add comprehensive logging for each extraction step
6. Include data validation checks post-extraction
7. Handle errors specific to the source type:
   - Network errors for APIs
   - File not found for local files
   - Connection timeouts for databases
   - Authentication failures
8. Create ONE function per data source/table mentioned in `data_sources.md`

**`data_validator.py`:**
```python
# Should include:
# - Schema validation (column names, types)
# - Data quality checks (null counts, duplicates, outliers)
# - Business rule validation
# - Quality report generation
# - Automated alerts for quality issues
# - Integration with data quality frameworks (Great Expectations, if specified)
```

**`etl_pipeline.py`:**
```python
# Should include:
# - Pipeline orchestration class/functions
# - Dependency management between steps
# - Checkpoint/restart capability
# - Progress logging
# - Performance metrics collection
# - Error recovery mechanisms
```

#### 2.2 Feature Engineering Module (`src/features/`)

**Files to Create:**
- `__init__.py`
- `feature_calculator.py`: Feature computation functions
- `transformers.py`: Data transformation classes
- `feature_store.py`: Feature caching and versioning

**Implementation Requirements:**
- Vectorized operations for performance (NumPy/Pandas/Spark)
- Feature documentation as docstrings
- Unit tests for each feature function
- Feature versioning metadata
- Configurable parameters from `config/analysis.yml`

#### 2.3 Analysis Module (`src/analysis/`)

**Files to Create:**
- `__init__.py`
- `statistical_tests.py`: Hypothesis testing, statistical analysis
- `descriptive_stats.py`: Summary statistics, distributions
- `comparative_analysis.py`: Group comparisons, trend analysis

**Implementation Requirements:**
- Use appropriate statistical libraries (scipy, statsmodels, etc.)
- Return structured results (dictionaries, dataclasses)
- Include confidence intervals and p-values
- Comprehensive docstrings with method references
- Visualization integration

#### 2.4 Model Module (`src/models/`)

**Files to Create:**
- `__init__.py`
- `model_trainer.py`: Model training pipeline
- `model_evaluator.py`: Model evaluation and metrics
- `model_registry.py`: Model versioning and persistence

**Implementation Requirements:**
- Support for multiple model types (based on plan)
- Hyperparameter tuning with cross-validation
- Model serialization (pickle, joblib, MLflow)
- Performance metrics calculation
- Model reproducibility (random seeds, version tracking)

#### 2.5 Visualization Module (`src/visualization/`)

**Files to Create:**
- `__init__.py`
- `plot_utils.py`: Reusable plotting functions
- `dashboard_components.py`: Dashboard elements (if applicable)
- `report_generator.py`: Automated report creation

**Implementation Requirements:**
- Consistent styling across visualizations
- Publication-ready plots (high DPI, proper labels)
- Interactive plots (Plotly, if specified)
- Export to multiple formats (PNG, SVG, PDF)
- Accessibility considerations (colorblind-friendly palettes)

#### 2.6 Utility Module (`src/utils/`)

**Files to Create:**
- `__init__.py`
- `logging_config.py`: Centralized logging setup
- `file_manager.py`: File I/O utilities
- `monitoring.py`: Performance monitoring
- `helpers.py`: Common utility functions

**Implementation Requirements:**
- Structured logging with appropriate levels
- Thread-safe logging
- Performance decorators
- File path management utilities
- Memory and execution time monitoring

---

### Phase 3: Script Generation (`scripts/`)

Create executable scripts for each phase in the execution plan:

**Template Structure:**
```python
#!/usr/bin/env python3
"""
Script: run_phase_{N}_{description}.py
Description: {Brief description of what this phase accomplishes}
Inputs: {List input files/databases}
Outputs: {List output files/artifacts}
Dependencies: {Previous phases or external requirements}
"""

import argparse
import logging
from pathlib import Path
from src.utils.logging_config import setup_logging
from src.data_processing import ...

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="...")
    parser.add_argument('--config', type=str, required=True)
    parser.add_argument('--output-dir', type=str, required=True)
    # ... more arguments
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(log_level=args.log_level)
    logger = logging.getLogger(__name__)
    
    # Load configuration
    # Execute phase logic
    # Validate outputs
    # Log completion

if __name__ == "__main__":
    main()
```

**Scripts to Create:**
- `run_extraction.py`: Data extraction orchestration
- `run_validation.py`: Data quality checks
- `run_feature_engineering.py`: Feature generation
- `run_analysis.py`: Statistical analysis execution
- `run_modeling.py`: Model training and evaluation
- `run_reporting.py`: Report and visualization generation
- `run_full_pipeline.py`: Complete end-to-end execution
- `run_scheduler.py`: Scheduled job execution (if applicable)

---

### Phase 4: SQL Queries (`sql/`)

**⚠️ CONDITIONAL PHASE**: Only implement this phase if Phase 0 analysis identified SQL databases as a data source.

**SKIP THIS PHASE IF:**
- Data source is Kaggle datasets (use kagglehub API instead)
- Data source is REST APIs (use requests/http clients)
- Data source is local files (use pandas.read_csv/read_excel/read_parquet)
- Data source is cloud storage (use cloud SDKs)
- Data source is NoSQL databases (use database-specific clients)

**IMPLEMENT THIS PHASE IF:**
- Data sources document shows SQL database connection strings
- PostgreSQL, MySQL, SQL Server, Oracle databases are mentioned
- Implementation plan explicitly requires SQL query files
- Traditional relational database is the primary data source

---

If implementing this phase (SQL sources confirmed):

**CRITICAL**: Generate SQL queries based on actual tables and schemas in `project_context/data_sources.md`

**Folder Structure:**
```
sql/
├── extractions/
│   ├── 01_patient_data.sql
│   ├── 02_facility_data.sql
│   └── ...
├── views/
│   └── vw_analysis_mart.sql
├── procedures/
│   └── sp_update_features.sql
└── README.md
```

**Query Generation Requirements:**
1. **Match Schema**: Use EXACT table names, column names, and data types from `data_sources.md`
2. **Select Required Fields**: Include all columns needed for analysis (check implementation plan)
3. **Apply Filters**: Add WHERE clauses for date ranges, status flags, etc. as specified
4. **Join Tables**: Create joins between related tables as defined in data sources
5. **Optimize Performance**: Add indexes, limit results, partition by date ranges
6. **Parameterize**: Use placeholders for dynamic values: `{start_date}`, `{end_date}`, `{facility_id}`
7. **Document**: Add comments explaining business logic and expected outputs

**Example Query Structure:**
```sql
-- Extraction: Patient Admissions Data
-- Source Tables: patients, admissions, facilities (from data_sources.md)
-- Expected Rows: ~10,000 per month
-- Runtime: ~30 seconds

SELECT 
    p.patient_id,
    p.age,
    p.gender,
    a.admission_date,
    a.discharge_date,
    a.diagnosis_code,
    f.facility_name,
    f.facility_type
FROM patients p
INNER JOIN admissions a ON p.patient_id = a.patient_id
INNER JOIN facilities f ON a.facility_id = f.facility_id
WHERE a.admission_date BETWEEN '{start_date}' AND '{end_date}'
    AND a.status = 'completed'
ORDER BY a.admission_date;
```

**Additional Requirements:**
- Clear comments explaining logic
- Consistent naming conventions (lowercase with underscores)
- Include expected row counts or runtime estimates in comments
- Test queries with LIMIT clause first

---

### Phase 5: Testing Suite (`tests/`)

Create comprehensive tests:

#### 5.1 Unit Tests (`tests/unit/`)
- Test each function in isolation
- Mock external dependencies (databases, APIs)
- Aim for >80% code coverage
- Use pytest fixtures for setup/teardown

```python
# Example: tests/unit/test_data_validator.py
import pytest
from src.data_processing.data_validator import validate_schema

def test_validate_schema_valid():
    # Test with valid data
    assert validate_schema(valid_df, expected_schema) == True

def test_validate_schema_missing_column():
    # Test error handling
    with pytest.raises(ValidationError):
        validate_schema(invalid_df, expected_schema)
```

#### 5.2 Integration Tests (`tests/integration/`)
- Test module interactions
- Use test databases or fixtures
- Validate end-to-end flows

#### 5.3 Data Quality Tests (`tests/data_quality/`)
- Create Great Expectations suites (if using)
- Validate data assumptions
- Automated quality checks

#### 5.4 Test Configuration
- `tests/conftest.py`: Shared pytest fixtures
- `pytest.ini`: Pytest configuration
- `.coveragerc`: Coverage configuration

---

### Phase 6: Notebooks (`notebooks/`)

Create Jupyter/R notebooks for exploration and reporting:

**Structure:**
```
notebooks/
├── 1_exploratory/
│   ├── 01_initial_data_exploration.ipynb
│   └── 02_feature_distributions.ipynb
├── 2_analysis/
│   ├── 01_hypothesis_testing.ipynb
│   └── 02_model_experiments.ipynb
├── 3_reporting/
│   └── 01_executive_summary.ipynb
└── README.md
```

**Requirements:**
- Clear markdown cells explaining each step
- Reproducible (load from configs, use fixed seeds)
- Output visualizations inline
- Export key results to files
- Keep notebooks focused (< 100 cells)

---

### Phase 7: Documentation

Create comprehensive documentation:

#### 7.1 Main Project README
**CRITICAL**: Create a comprehensive `README.md` (root) that serves as the primary entry point for users to understand and run the entire system.

**Required Sections:**
```markdown
# {Project Name}

## Overview
Brief description of what the system does and its purpose.

## Prerequisites
- Python version (e.g., Python 3.8+)
- Required software (PostgreSQL, Spark, etc.)
- Access credentials needed
- System requirements (memory, storage)

## Installation

### 1. Clone Repository
```bash
git clone {repository_url}
cd {project_directory}
```

### 2. Set Up Environment
```bash
# Using pip
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# OR using conda
conda env create -f environment.yml
conda activate {env_name}
```

### 3. Configure Environment
```bash
cp config/.env.template .env
# Edit .env with your credentials
```

## Configuration
- Explain each configuration file in `config/`
- Provide examples of key settings
- Link to `config/README.md` for details

## Running the System

### Quick Start (Full Pipeline)
```bash
python scripts/run_full_pipeline.py --config config/analysis.yml
```

### Step-by-Step Execution

#### Phase 1: Data Extraction
```bash
python scripts/run_extraction.py \
  --config config/database.yml \
  --output-dir data/raw/ \
  --start-date 2024-01-01 \
  --end-date 2024-12-31
```

#### Phase 2: Data Validation
```bash
python scripts/run_validation.py \
  --input-dir data/raw/ \
  --output-dir data/validated/
```

#### Phase 3: Feature Engineering
```bash
python scripts/run_feature_engineering.py \
  --input-dir data/validated/ \
  --output-dir data/features/ \
  --config config/analysis.yml
```

#### Phase 4: Analysis
```bash
python scripts/run_analysis.py \
  --input-dir data/features/ \
  --output-dir results/
```

#### Phase 5: Generate Reports
```bash
python scripts/run_reporting.py \
  --results-dir results/ \
  --output-dir reports/
```

### Running Notebooks
```bash
jupyter notebook notebooks/
# Navigate to desired notebook
```

### Scheduled Execution
```bash
# Set up daily automated runs
python scripts/run_scheduler.py --schedule daily --time 02:00
```

## Output Locations
- Raw data: `data/raw/`
- Processed data: `data/processed/`
- Features: `data/features/`
- Results: `results/`
- Reports: `reports/`
- Logs: `logs/`

## Testing
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test suite
pytest tests/unit/test_data_validator.py
```

## Troubleshooting
Link to common issues and solutions (see `docs/TROUBLESHOOTING.md`)

## Project Structure
Brief overview of key directories and their purpose

## Documentation
- [Architecture Guide](docs/ARCHITECTURE.md)
- [API Reference](docs/API_REFERENCE.md)
- [User Guide](docs/USER_GUIDE.md)
- [Development Guide](docs/DEVELOPMENT.md)

## Support
Contact information or issue reporting instructions

## License
License information
```

#### 7.2 Additional README Files
- `src/README.md`: Architecture overview
- `tests/README.md`: Testing guide
- `config/README.md`: Configuration guide
- `data/README.md`: Data directory structure and descriptions

#### 7.3 Technical Documentation
- `docs/ARCHITECTURE.md`: System design, data flows
- `docs/API_REFERENCE.md`: Function/class documentation
- `docs/DEVELOPMENT.md`: Development setup, contribution guide
- `docs/DEPLOYMENT.md`: Deployment procedures

#### 7.4 User Guides
- `docs/USER_GUIDE.md`: End-user instructions
- `docs/DATA_DICTIONARY.md`: Data field definitions
- `docs/TROUBLESHOOTING.md`: Common issues and solutions

#### 7.5 Inline Documentation
- Docstrings for all functions/classes (Google or NumPy style)
- Type hints for Python 3.6+
- Inline comments for complex logic

---

### Phase 8: DevOps & Automation

If specified in the plan:

#### 8.1 Version Control
- `.gitignore`: Exclude data, credentials, cache files
- `.gitattributes`: Handle line endings, LFS for large files

#### 8.2 CI/CD (if applicable)
- `.github/workflows/test.yml`: Automated testing
- `.github/workflows/lint.yml`: Code quality checks

#### 8.3 Containerization (if applicable)
- `Dockerfile`: Container image definition
- `docker-compose.yml`: Multi-container orchestration
- `.dockerignore`: Exclude unnecessary files

#### 8.4 Orchestration (if applicable)
- Airflow DAGs (`dags/`)
- Prefect flows
- Cron job scripts

---

## Code Quality Standards

Ensure all generated code follows these standards:

### 1. Style & Formatting
- **Python**: PEP 8 compliance (use black, flake8)
- **R**: tidyverse style guide
- **SQL**: Consistent capitalization, indentation
- Maximum line length: 100 characters
- Consistent naming: `snake_case` for Python, `camelCase` for R (if preferred)

### 2. Error Handling
- Try-except blocks for external operations
- Specific exception types
- Informative error messages
- Logging of errors with context
- Graceful degradation where possible

### 3. Logging
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Structured logging with context
- No sensitive data in logs
- Consistent log format

### 4. Performance
- Vectorized operations over loops
- Efficient data structures
- Memory profiling for large datasets
- Caching of expensive computations
- Parallel processing where beneficial

### 5. Security
- No hardcoded credentials
- Input validation and sanitization
- SQL injection prevention (parameterized queries)
- Secure file permissions
- Secrets management (environment variables, vaults)

### 6. Maintainability
- DRY principle (Don't Repeat Yourself)
- Single Responsibility Principle
- Clear function/class names
- Comprehensive docstrings
- Type hints for better IDE support

---

## Platform-Specific Considerations

Adapt code based on `tech_stack.md`:

### Databricks Environment
- Use Databricks utilities: `dbutils.fs`, `dbutils.secrets`
- Spark DataFrame operations for large data
- Notebook widgets for parameterization
- Delta Lake for data storage

### CDSW/Cloudera Environment
- Spark for distributed computing
- HDFS for data storage
- Resource management (executor memory, cores)
- Kerberos authentication

### Local Development
- Virtual environment setup
- Local database (SQLite for testing)
- Docker for dependencies
- Lighter weight libraries

---

## Execution Checklist

After implementation, verify:

- [ ] **PHASE 0 COMPLETED**: Data sources analyzed and extraction method identified
- [ ] **PHASE 0 COMPLETED**: Source type documented (Kaggle/SQL/API/Files/etc.)
- [ ] **PHASE 0 COMPLETED**: Data Source Analysis Summary created
- [ ] **PHASE 0 COMPLETED**: Decision made on SQL phase (skip or implement)
- [ ] **PHASE 0 COMPLETED**: Required libraries list created based on source type
- [ ] Data sources analyzed from `project_context/data_sources.md`
- [ ] Extraction code generated for ALL data sources identified
- [ ] Extraction code pattern matches identified source type (e.g., kagglehub for Kaggle)
- [ ] SQL queries match actual table/column names from data sources (if SQL phase implemented)
- [ ] All directories created as specified
- [ ] Configuration files with placeholders created
- [ ] All modules implemented with proper structure
- [ ] Scripts executable with proper permissions
- [ ] SQL queries formatted and parameterized
- [ ] Tests written and passing (run `pytest`)
- [ ] Documentation complete and accurate
- [ ] Requirements file with all dependencies
- [ ] `.gitignore` properly configured
- [ ] Code follows style guidelines (run linter)
- [ ] Logging configured and tested
- [ ] Error handling in all external operations
- [ ] Type hints added (Python 3.6+)
- [ ] No hardcoded credentials or paths
- [ ] Example usage provided in README
- [ ] Integration with existing codebase verified

---

## Deliverables

Provide:

1. **Complete Codebase**: All modules, scripts, configurations
2. **Comprehensive README.md**: Primary user guide showing:
   - How to install and set up the system
   - How to run the complete pipeline
   - How to run individual phases
   - Where to find outputs
   - Quick start guide for new users
3. **Installation Instructions**: Step-by-step setup guide (in README)
4. **Usage Examples**: How to run each script/pipeline (in README)
5. **Testing Results**: Test coverage report, passed tests
6. **Documentation**: Technical and user documentation
7. **Deployment Guide**: How to deploy to target environment
8. **Troubleshooting Guide**: Common issues and resolutions

---

## Output Format

Organize generated code by:

1. **File-by-file generation**: Create each file with full content
2. **Logical grouping**: Group related files together
3. **Clear separation**: Mark each file clearly with path and description
4. **Execution order**: Present files in implementation order

For each file:
```
## File: {relative/path/to/file.py}
**Purpose**: {Brief description}
**Dependencies**: {Required modules/files}

```python
# Full file content here
```
```

---

## Success Criteria

The implementation is complete when:

1. ✓ All code can be executed without errors
2. ✓ All tests pass successfully
3. ✓ Configuration is externalized and documented
4. ✓ Code follows style and quality standards
5. ✓ **A comprehensive README.md exists that enables any user to run the entire system from scratch**
6. ✓ Documentation enables new users to understand and run the project
7. ✓ The implementation matches the original plan specifications
8. ✓ Error handling and logging are comprehensive
9. ✓ The code is maintainable and extensible

---

## Notes

- **Prioritize correctness over speed**: Ensure code works before optimizing
- **Reference tech_stack.md**: Use specified technologies and patterns
- **Maintain consistency**: Follow established patterns throughout
- **Think production-ready**: Code should be deployable, not just functional
- **Document assumptions**: Note any decisions made due to ambiguity
- **Provide alternatives**: Suggest improvements or alternative approaches
- **Consider scalability**: Design for growth in data volume and complexity

---

## Begin Implementation

Read the implementation plan and project context carefully, then systematically create all specified files, following the structure and requirements outlined above. Work through each phase sequentially, ensuring completeness before moving to the next phase.
