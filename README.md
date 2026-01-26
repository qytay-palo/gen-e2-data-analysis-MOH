# MOH Polyclinic Data Analysis - Automated Extraction System

Automated data extraction, validation, and ETL pipeline for MOH polyclinic data analysis.

## Overview

This project provides a comprehensive automated system for extracting and processing polyclinic data from MOH databases. Built to support strategic policy planning, resource allocation, population health initiatives, and healthcare quality improvements.

### Key Features

- ✅ **Automated Data Extraction** - Incremental and full extraction modes with checkpoint management
- ✅ **Multi-Database Support** - PostgreSQL, MySQL, MS SQL Server, Oracle
- ✅ **Data Quality Validation** - Comprehensive validation checks for data integrity
- ✅ **ETL Pipeline** - Complete Extract-Transform-Load workflow orchestration
- ✅ **Scheduled Automation** - Daily, weekly, and monthly automated runs
- ✅ **Monitoring & Alerts** - Performance tracking and failure notifications
- ✅ **Logging & Audit** - Comprehensive logging for compliance and troubleshooting

## Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Database
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### Run First Extraction
```bash
# Extract patient data from last 7 days
python scripts/run_extraction.py --sources patients --last-n-days 7
```

📖 **[Full Quick Start Guide](docs/QUICK_START.md)** | 📚 **[Complete Documentation](docs/DATA_EXTRACTION_GUIDE.md)**

## System Components

### 1. Configuration (`config/`)
- **database.yml** - Database connections, extraction settings, validation rules
- **queries.yml** - SQL query templates for data extraction

### 2. Data Processing (`src/data_processing/`)
- **db_connector.py** - Database connection management
- **data_extractor.py** - Data extraction with batching and retry logic
- **data_validator.py** - Data quality validation checks
- **etl_pipeline.py** - Complete ETL workflow orchestration

### 3. Utilities (`src/utils/`)
- **logging_config.py** - Logging configuration and structured logging
- **monitoring.py** - Performance monitoring and alerting

### 4. Scripts (`scripts/`)
- **run_extraction.py** - Manual data extraction with CLI options
- **run_scheduler.py** - Automated scheduler for recurring jobs

## Usage Examples

### Manual Extraction

```bash
# Extract specific sources
python scripts/run_extraction.py --sources attendances diagnoses

# Extract date range
python scripts/run_extraction.py \
  --sources all \
  --start-date 2025-01-01 \
  --end-date 2025-01-31

# Full extraction (not incremental)
python scripts/run_extraction.py --sources all --full
```

### Python API

```python
from src.data_processing.etl_pipeline import ETLPipeline

pipeline = ETLPipeline()
result = pipeline.run_full_pipeline(
    sources=['attendances', 'diagnoses'],
    start_date='2025-01-01',
    incremental=True
)
```

### Automated Scheduling

```bash
# Start scheduler for automated runs
python scripts/run_scheduler.py
```

## Project Structure

```
├── config/                 # Configuration files
│   ├── database.yml       # Database and extraction config
│   └── queries.yml        # SQL query templates
├── src/                   # Source code
│   ├── data_processing/   # ETL components
│   ├── utils/            # Logging, monitoring
│   ├── analysis/         # Analysis modules (future)
│   └── visualization/    # Visualization tools (future)
├── scripts/              # Executable scripts
│   ├── run_extraction.py
│   └── run_scheduler.py
├── data/                 # Data storage
│   ├── raw/             # Raw extracted data
│   ├── processed/       # Cleaned data
│   └── interim/         # Intermediate files
├── logs/                # Log files
├── results/             # Analysis outputs
│   └── metrics/         # Execution metrics
└── docs/                # Documentation
    ├── QUICK_START.md
    ├── DATA_EXTRACTION_GUIDE.md
    ├── objectives/      # Project objectives
    └── data_dictionary/ # Data schemas
```

## Data Sources

The system supports extraction from:
- **Attendances** - Patient visits and appointments
- **Patients** - Demographics and registration data
- **Diagnoses** - Diagnosis records with ICD codes
- **Procedures** - Medical procedures and treatments
- **Medications** - Prescription records
- **Lab Results** - Laboratory test results
- **Reference Data** - Polyclinics, conditions, and master data

## Monitoring & Outputs

### Log Files
- `logs/extraction.log` - Main extraction activities
- `logs/errors.log` - Error tracking
- `logs/audit.log` - Structured audit trail

### Outputs
- `data/raw/` - Raw extracted data (Parquet/CSV)
- `data/processed/` - Cleaned, analysis-ready data
- `results/metrics/` - Execution summaries and performance metrics

## Project Objectives

This system supports MOH's strategic objectives:
- 📊 **Strategic Planning** - Long-term healthcare capacity and funding
- 🏥 **Resource Allocation** - Equitable distribution across polyclinics
- 👥 **Population Health** - Demographic analysis and health equity
- 📈 **Quality of Care** - Clinical outcomes and best practices
- 🔄 **System Integration** - Data sharing with NEHR and hospitals

See [User Stories](docs/objectives/01-user-stores.md) and [Agile Stories](docs/objectives/02-agile-user-stories.md) for detailed requirements.

## Requirements

- Python 3.8+
- PostgreSQL/MySQL/MS SQL Server/Oracle
- 2GB+ RAM (for large extractions)
- Required packages: pandas, pyarrow, pyyaml, psycopg2, schedule, psutil

## Documentation

- 📖 [Quick Start Guide](docs/QUICK_START.md) - Get started in 5 minutes
- 📚 [Complete Documentation](docs/DATA_EXTRACTION_GUIDE.md) - Full system guide
- 🎯 [Project Objectives](docs/objectives/) - User stories and requirements
- 📋 [Data Dictionary](docs/data_dictionary/) - Data schemas and definitions

## License

Internal MOH use only. Confidential and proprietary.

---

**Version**: 1.0  
**Last Updated**: 2026-01-26  
**Maintained By**: MOH Data Analytics Team
