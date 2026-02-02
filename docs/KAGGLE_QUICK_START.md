# Quick Start: Kaggle Data Source
# Singapore Health Dataset Integration

This guide helps you quickly set up and start using the Kaggle health dataset.

---

## 🚀 1-Minute Setup

```bash
# Step 1: Install dependencies
pip install kagglehub[pandas-datasets]

# Step 2: Configure Kaggle credentials
# Download from: https://www.kaggle.com/settings/account → "Create New API Token"
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Step 3: Test connection
python -c "from src.data_processing.kaggle_connector import KaggleDataConnector; KaggleDataConnector()"

# Step 4: Load data
python scripts/load_kaggle_data.py --validate --save-metadata
```

---

## 📊 Quick Usage Examples

### Example 1: Load and Explore
```python
from src.data_processing.kaggle_connector import KaggleDataConnector

# Initialize and load
connector = KaggleDataConnector()
df = connector.load_dataset()

# Quick exploration
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(df.head())
print(df.info())
```

### Example 2: Load with Validation
```python
# Load and validate quality
connector = KaggleDataConnector()
df = connector.load_dataset()
validation = connector.validate_dataset(df)

print(f"Quality: {validation['validation_status']}")
if validation['validation_status'] == 'PASSED':
    print("✓ Data ready for analysis!")
```

### Example 3: Get Metadata for LLM
```python
# Extract metadata for LLM interpretation
connector = KaggleDataConnector()
df = connector.load_dataset()
metadata = connector.get_metadata()

# Save for LLM agents
connector.save_metadata("data/metadata/kaggle/current.yml")

# Print summary
print(f"Rows: {metadata['shape']['rows']:,}")
print(f"Columns: {metadata['shape']['columns']}")
print(f"Quality: {100 - metadata['data_quality']['missing_percentage']:.1f}%")
```

### Example 4: Using the Command-Line Script
```bash
# Basic load
python scripts/load_kaggle_data.py

# Load with validation and metadata
python scripts/load_kaggle_data.py --validate --save-metadata

# Load sample for testing
python scripts/load_kaggle_data.py --sample 1000

# Custom output location
python scripts/load_kaggle_data.py --output data/processed/my_health_data.parquet

# Force fresh download (bypass cache)
python scripts/load_kaggle_data.py --force-download
```

---

## 🔍 What's Been Created

### New Files
1. **[kaggle_connector.py](../src/data_processing/kaggle_connector.py)**
   - Python module for loading Kaggle datasets
   - Automatic caching and validation
   - LLM-interpretable metadata extraction

2. **[load_kaggle_data.py](../scripts/load_kaggle_data.py)**
   - Command-line script for data loading
   - Supports validation, sampling, and metadata export

3. **[kaggle_data_source_analysis.md](../docs/data_dictionary/kaggle_data_source_analysis.md)**
   - Comprehensive documentation
   - LLM-interpretable format
   - Usage patterns and troubleshooting

### Updated Files
1. **[data_sources.md](../docs/project_context/data_sources.md)**
   - Added Kaggle as primary source
   - Connection details and authentication

2. **[database.yml](../config/database.yml)**
   - Kaggle connection configuration
   - Validation and caching settings

3. **[requirements.txt](../requirements.txt)**
   - Added `kagglehub[pandas-datasets]`

---

## 🗂️ Data Flow

```
Kaggle API
    ↓
kagglehub package
    ↓
KaggleDataConnector (src/data_processing/kaggle_connector.py)
    ↓
Local Cache (data/raw/kaggle/)
    ↓
Validation & Metadata Extraction
    ↓
Your Analysis (notebooks/ or scripts/)
```

---

## 📁 Directory Structure

```
data/
├── raw/kaggle/              # Cached Kaggle datasets
├── metadata/kaggle/         # Dataset metadata (YAML)
├── processed/               # Processed datasets
└── interim/                 # Temporary files

src/data_processing/
├── kaggle_connector.py      # Kaggle connector (NEW)
├── db_connector.py          # Database connector (existing)
└── etl_pipeline.py          # ETL pipeline (update to use Kaggle)

scripts/
├── load_kaggle_data.py      # Kaggle loader script (NEW)
├── run_extraction.py        # Main extraction script (existing)
└── run_scheduler.py         # Scheduler (existing)

config/
└── database.yml             # Updated with Kaggle config

docs/
├── project_context/
│   └── data_sources.md      # Updated with Kaggle info
└── data_dictionary/
    └── kaggle_data_source_analysis.md  # Comprehensive guide (NEW)
```

---

## ⚙️ Configuration Reference

From [database.yml](../config/database.yml):

```yaml
kaggle_connection:
  dataset_id: "subhamjain/health-dataset-complete-singapore"
  source_type: "kaggle"
  adapter: "pandas"
  cache_enabled: true
  cache_directory: "data/raw/kaggle"
  
  validation:
    enabled: true
    check_duplicates: true
    check_missing_threshold: 0.5
    check_empty_columns: true
  
  metadata:
    auto_extract: true
    save_path: "data/metadata/kaggle"
    format: "yaml"
```

---

## 🤖 For LLM Agents

### When analyzing this project, you can:

1. **Load the dataset:**
   ```python
   from src.data_processing.kaggle_connector import KaggleDataConnector
   connector = KaggleDataConnector()
   df = connector.load_dataset()
   ```

2. **Get metadata for interpretation:**
   ```python
   metadata = connector.get_metadata()
   # Returns LLM-friendly dictionary with column info, stats, quality metrics
   ```

3. **Validate before analysis:**
   ```python
   validation = connector.validate_dataset(df)
   # Returns validation status: PASSED/WARNING/FAILED
   ```

4. **Check connection status:**
   ```python
   status = connector.get_connection_status()
   # Returns authentication, cache info, last extraction time
   ```

### Key metadata fields for LLM:
- `metadata['shape']` - Dimensions
- `metadata['columns'][col_name]` - Column details
- `metadata['data_quality']` - Missing data stats
- `metadata['memory_usage_mb']` - Memory consumption

---

## ❓ Troubleshooting

### "Kaggle credentials not found"
```bash
# Check if kaggle.json exists
ls -la ~/.kaggle/

# If missing, download from Kaggle settings
# https://www.kaggle.com/settings/account → "Create New API Token"
```

### "Module kagglehub not found"
```bash
pip install kagglehub[pandas-datasets]
# or
pip install -r requirements.txt
```

### "Dataset not found"
- Verify dataset ID: `subhamjain/health-dataset-complete-singapore`
- Check if dataset is public on Kaggle
- Visit: https://www.kaggle.com/datasets/subhamjain/health-dataset-complete-singapore

### Data loads slowly
- First load downloads from Kaggle (may take time)
- Subsequent loads use local cache (instant)
- Cache location: `data/raw/kaggle/`

---

## 📚 Next Steps

1. **Load the data:**
   ```bash
   python scripts/load_kaggle_data.py --validate --save-metadata
   ```

2. **Explore in notebook:**
   - Create `notebooks/1_exploratory/kaggle_exploration.ipynb`
   - Load with connector
   - Inspect columns and data types
   - Generate basic statistics

3. **Update ETL pipeline:**
   - Modify `src/data_processing/etl_pipeline.py`
   - Add Kaggle source as primary
   - Implement data transformations

4. **Run analysis:**
   - Use processed data for your research questions
   - Refer to [kaggle_data_source_analysis.md](../docs/data_dictionary/kaggle_data_source_analysis.md) for detailed guidance

---

## 📖 Documentation

- **Full Guide:** [docs/data_dictionary/kaggle_data_source_analysis.md](../docs/data_dictionary/kaggle_data_source_analysis.md)
- **Data Sources:** [docs/project_context/data_sources.md](../docs/project_context/data_sources.md)
- **Connector Module:** [src/data_processing/kaggle_connector.py](../src/data_processing/kaggle_connector.py)
- **Config:** [config/database.yml](../config/database.yml)

---

**Status**: ✅ Ready to use  
**Last Updated**: 2026-01-30  
**LLM-Friendly**: Yes
