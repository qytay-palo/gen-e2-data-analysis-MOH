# Data Directory

This directory contains raw data, extracted datasets, and metadata generated from various data sources.

## Directory Structure

```
data/
├── dataset_exploration.json    # Generated metadata from Kaggle dataset
├── versions/                   # Versioned data snapshots (if using versioning)
├── raw/                        # Raw extracted data (gitignored)
├── processed/                  # Cleaned/transformed data (gitignored)
└── README.md                   # This file
```

## dataset_exploration.json

**Purpose:** Machine-readable metadata for all tables in the Kaggle Singapore Health Dataset

**Generated:** 30 January 2026  
**Source Script:** [`scripts/explore_kaggle_dataset.py`](../scripts/explore_kaggle_dataset.py)

### Contents

```json
{
  "dataset_name": "subhamjain/health-dataset-complete-singapore",
  "dataset_path": "/path/to/cached/dataset",
  "total_files": 70,
  "files": [
    {
      "filename": "table-name.csv",
      "relative_path": "subdirectory/table-name.csv",
      "size_mb": 0.05,
      "file_type": "CSV",
      "rows": 100,
      "columns": 5,
      "column_names": ["col1", "col2", ...],
      "column_details": [
        {
          "name": "col1",
          "dtype": "int64",
          "non_null_count": 100,
          "null_count": 0,
          "null_percentage": 0.0,
          "unique_count": 50,
          "sample_values": ["val1", "val2", ...],
          "value_distribution": {"val1": 20, "val2": 15, ...}
        }
      ],
      "data_quality": {
        "total_cells": 500,
        "null_cells": 0,
        "completeness_percentage": 100.0
      }
    }
  ]
}
```

### Usage

**Python:**
```python
import json
import pandas as pd

# Load metadata
with open('data/dataset_exploration.json', 'r') as f:
    metadata = json.load(f)

# List all available tables
csv_files = [f for f in metadata['files'] if f['file_type'] == 'CSV']
print(f"Found {len(csv_files)} CSV tables")

# Get schema for specific table
table_name = "number-of-doctors.csv"
table_meta = next(f for f in csv_files if f['filename'] == table_name)

print(f"\n{table_name}:")
print(f"  Rows: {table_meta['rows']}")
print(f"  Columns: {table_meta['columns']}")
print(f"  Column Names: {table_meta['column_names']}")
```

**JavaScript/Node.js:**
```javascript
const fs = require('fs');

// Load metadata
const metadata = JSON.parse(
  fs.readFileSync('data/dataset_exploration.json', 'utf8')
);

// Find tables with time series data (having 'year' column)
const timeSeriesTables = metadata.files.filter(file =>
  file.file_type === 'CSV' &&
  file.column_names && file.column_names.includes('year')
);

console.log(`Found ${timeSeriesTables.length} time-series tables`);
```

### Regenerating Metadata

To regenerate after dataset updates:

```bash
# Activate virtual environment
source venv/bin/activate

# Run exploration script
python scripts/explore_kaggle_dataset.py
```

This will:
1. Download latest dataset from Kaggle
2. Analyze all files
3. Generate updated `dataset_exploration.json`

## Data Versioning (Optional)

If using data versioning, snapshots are stored in `versions/`:

```
versions/
├── 20260130_120000/
│   ├── number-of-doctors.csv
│   ├── number-of-nurses-and-midwives.csv
│   ├── ...
│   └── metadata.json
└── 20260201_120000/
    └── ...
```

**Version Metadata Example:**
```json
{
  "version": "2026-01-30T12:00:00",
  "tables": ["number-of-doctors", "number-of-nurses", ...],
  "record_counts": {
    "number-of-doctors": 78,
    "number-of-nurses": 126
  }
}
```

## Data Security Notes

- **API Keys:** Never commit Kaggle credentials to this directory
- **.gitignore:** Raw/processed data directories are gitignored to save space
- **Sensitive Data:** If processing confidential data, ensure proper access controls

## Quick Reference

| File/Directory | Purpose | Tracked in Git |
|----------------|---------|----------------|
| `dataset_exploration.json` | Dataset metadata | ✓ Yes |
| `raw/` | Raw extracted CSVs | ✗ No (too large) |
| `processed/` | Cleaned data | ✗ No (reproducible) |
| `versions/` | Historical snapshots | ✗ No (optional) |

## Related Documentation

- **Data Catalog:** [`docs/data_dictionary/COMPREHENSIVE_DATA_CATALOG.md`](../docs/data_dictionary/COMPREHENSIVE_DATA_CATALOG.md)
- **Quick Reference:** [`docs/data_dictionary/TABLE_QUICK_REFERENCE.md`](../docs/data_dictionary/TABLE_QUICK_REFERENCE.md)
- **Data Sources:** [`docs/project_context/data_sources.md`](../docs/project_context/data_sources.md)

---

**Last Updated:** 30 January 2026
