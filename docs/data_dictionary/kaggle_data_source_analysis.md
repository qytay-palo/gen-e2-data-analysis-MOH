# Kaggle Data Source Analysis
# Singapore Health Dataset - Complete Analysis
# Dataset: subhamjain/health-dataset-complete-singapore
# Analysis Date: 2026-01-30

---

## Executive Summary

**Data Source**: Kaggle Public Dataset  
**Dataset ID**: `subhamjain/health-dataset-complete-singapore`  
**Access Method**: Kaggle Hub API (`kagglehub` Python package)  
**Purpose**: Comprehensive health data analysis for Singapore MOH polyclinic operations

### Quick Facts
- **Format**: CSV-based, loaded as Pandas DataFrame
- **Update Frequency**: Static snapshot (Kaggle-hosted)
- **Geography**: Singapore
- **Domain**: Healthcare - Complete patient records
- **Privacy**: De-identified/Anonymized
- **License**: Check Kaggle dataset page for specific license

---

## Data Connection Architecture

### Connection Flow (Data Flow Architecture)
```

1. Authentication Layer
   ├── ~/.kaggle/kaggle.json (API credentials)
   ├── Environment Variables (KAGGLE_USERNAME, KAGGLE_KEY)
   └── Auto-verification on connector initialization

2. Data Retrieval Layer
   ├── kagglehub.load_dataset()
   ├── Automatic caching in local directory
   └── Version management (latest by default)

3. Processing Layer
   ├── Pandas DataFrame conversion
   ├── Metadata extraction
   └── Data quality validation

4. Storage Layer
   ├── Raw data: data/raw/kaggle/
   ├── Metadata: data/metadata/kaggle/
   └── Processed: data/processed/
```

### Technical Stack
```yaml
Primary Components:
  - Python Package: kagglehub[pandas-datasets]
  - Data Format: CSV → Pandas DataFrame
  - Cache Strategy: Local filesystem cache
  - Authentication: Kaggle API credentials

Integration Points:
  - Connector Module: src/data_processing/kaggle_connector.py
  - Configuration: config/database.yml
  - ETL Pipeline: src/data_processing/etl_pipeline.py
```

---

## Data Structure & Schema (LLM-Interpretable)

### Expected Data Categories

Based on the dataset identifier "health-dataset-complete-singapore", the dataset likely contains:

#### 1. **Patient Demographics**
```yaml
Purpose: Individual patient characteristics
Typical Columns:
  - patient_id: Unique identifier (anonymized)
  - age / age_group: Patient age information
  - gender: M/F/Other
  - race: Chinese/Malay/Indian/Others (Singapore context)
  - nationality: Singaporean/PR/Foreigner
  - postal_code: Geographic location (truncated for privacy)
  - registration_date: First encounter date

LLM Analysis Prompts:
  - "What is the age distribution of patients?"
  - "Compare healthcare utilization by demographic groups"
  - "Identify geographic hotspots for specific conditions"
```

#### 2. **Clinical Encounters/Visits**
```yaml
Purpose: Records of patient visits to healthcare facilities
Typical Columns:
  - encounter_id / attendance_id: Unique visit identifier
  - patient_id: Links to patient demographics
  - encounter_date: When visit occurred
  - facility_type: Clinic/Hospital/Polyclinic
  - visit_type: Acute/Chronic/Preventive/Emergency
  - visit_status: Completed/Cancelled/No-show

LLM Analysis Prompts:
  - "What are peak utilization times?"
  - "Calculate average visits per patient"
  - "Identify no-show patterns and factors"
```

#### 3. **Diagnoses (ICD Codes)**
```yaml
Purpose: Medical conditions diagnosed during visits
Typical Columns:
  - diagnosis_id: Unique diagnosis record
  - encounter_id: Links to visit
  - patient_id: Links to patient
  - icd_code: International Classification of Diseases code
  - diagnosis_description: Human-readable condition name
  - diagnosis_type: Primary/Secondary
  - severity: Mild/Moderate/Severe (if available)

LLM Analysis Prompts:
  - "What are the most common diagnoses?"
  - "Track chronic disease prevalence trends"
  - "Identify comorbidity patterns"
  - "Analyze disease burden by age group"
```

#### 4. **Procedures/Treatments**
```yaml
Purpose: Medical procedures and interventions performed
Typical Columns:
  - procedure_id: Unique procedure record
  - encounter_id: Links to visit
  - procedure_code: Standardized procedure code
  - procedure_name: Description of procedure
  - procedure_date: When performed
  - outcome: Success/Complication/Other

LLM Analysis Prompts:
  - "What are the most common procedures?"
  - "Calculate procedure success rates"
  - "Analyze treatment patterns for specific conditions"
```

#### 5. **Medications/Prescriptions**
```yaml
Purpose: Medications prescribed to patients
Typical Columns:
  - prescription_id: Unique prescription record
  - encounter_id: Links to visit
  - patient_id: Links to patient
  - medication_name: Drug name
  - dosage: Amount prescribed
  - duration: Length of prescription
  - frequency: How often to take

LLM Analysis Prompts:
  - "What are the most prescribed medications?"
  - "Identify polypharmacy cases (multiple medications)"
  - "Analyze prescription patterns by condition"
```

#### 6. **Lab Results** (if available)
```yaml
Purpose: Laboratory test results
Typical Columns:
  - lab_id: Unique lab result identifier
  - patient_id: Links to patient
  - test_type: Type of lab test
  - test_value: Numeric or categorical result
  - reference_range: Normal range for test
  - abnormal_flag: Y/N indicator

LLM Analysis Prompts:
  - "Identify abnormal test result frequencies"
  - "Track biomarker trends over time"
  - "Correlate lab results with diagnoses"
```

---

## Data Quality & Validation Framework

### Automated Quality Checks

```yaml
Validation Rules (Implemented in kaggle_connector.py):
  
  1. Structural Validation:
     - Check for duplicate rows
     - Identify completely empty columns
     - Verify expected data types
     - Validate primary key uniqueness
  
  2. Completeness Checks:
     - Calculate missing value percentages per column
     - Flag columns with >50% missing data
     - Identify patterns in missingness
  
  3. Consistency Checks:
     - Verify foreign key relationships
     - Check date range validity
     - Validate categorical value domains
     - Ensure referential integrity
  
  4. Statistical Profiling:
     - Generate descriptive statistics
     - Identify outliers
     - Calculate data distribution metrics
     - Assess data skewness and balance

Quality Thresholds:
  - PASSED: <5% missing data, no empty columns
  - WARNING: 5-20% missing data, or duplicates present
  - FAILED: >20% missing data, empty columns, or integrity violations
```

### Metadata Extraction

The connector automatically extracts and stores:

```yaml
Metadata Components:
  - Dataset Dimensions: Row count, column count
  - Column Profiles:
      - Data type
      - Non-null count
      - Null percentage
      - Unique value count
      - Sample values (first 3)
  - Memory Usage: Total DataFrame memory consumption
  - Data Quality Metrics:
      - Total missing cells
      - Missing data percentage
      - Duplicate row count
  - Extraction Timestamp: When data was loaded
```

---

## Usage Patterns for LLM Agents

### Pattern 1: Initial Data Exploration

```python
"""
LLM Task: "Explore the health dataset and provide summary statistics"
"""
from src.data_processing.kaggle_connector import KaggleDataConnector

# Initialize and load
connector = KaggleDataConnector()
df = connector.load_dataset()

# Get LLM-interpretable metadata
metadata = connector.get_metadata()

# LLM can interpret:
print(f"Dataset contains {metadata['shape']['rows']:,} patient records")
print(f"Across {metadata['shape']['columns']} different fields")
print(f"Data quality score: {100 - metadata['data_quality']['missing_percentage']:.1f}%")

# Column analysis
for col, info in metadata['columns'].items():
    print(f"{col}: {info['dtype']}, {info['unique_values']} unique values")
```

### Pattern 2: Automated Data Validation

```python
"""
LLM Task: "Validate the dataset quality before analysis"
"""
# Load and validate
df = connector.load_dataset()
validation = connector.validate_dataset(df)

# LLM decision tree:
if validation['validation_status'] == 'PASSED':
    print("✓ Data quality check passed - proceed with analysis")
elif validation['validation_status'] == 'WARNING':
    print("⚠ Data quality warnings detected - review before analysis")
    print(f"Issues: {validation['checks']}")
else:
    print("✗ Data quality check failed - investigate before proceeding")
    print(f"Critical issues: {validation['checks']}")
```

### Pattern 3: Incremental Analysis Updates

```python
"""
LLM Task: "Check if new data is available and update analysis"
"""
# Check connection status
status = connector.get_connection_status()

if status['last_extraction'] == 'Never':
    print("First-time data load - full extraction needed")
    df = connector.load_dataset()
else:
    print(f"Last extraction: {status['last_extraction']}")
    # Kaggle datasets are static, but this pattern supports version checking
```

### Pattern 4: Cross-Source Data Integration

```python
"""
LLM Task: "Integrate Kaggle data with other sources"
"""
# Primary source: Kaggle
kaggle_connector = KaggleDataConnector()
df_primary = kaggle_connector.load_dataset()

# Secondary source: MOH API (if available)
# from src.data_processing.db_connector import DatabaseConnector
# db_connector = DatabaseConnector()
# df_secondary = db_connector.extract_table('attendances')

# LLM can orchestrate merge:
# df_integrated = pd.merge(df_primary, df_secondary, on='patient_id', how='outer')
```

---

## Authentication Setup Guide

### Method 1: Kaggle JSON Configuration (Recommended)

```bash
# Step 1: Get API credentials from Kaggle
# Visit: https://www.kaggle.com/settings/account
# Scroll to "API" section → Click "Create New API Token"
# Downloads kaggle.json file

# Step 2: Move to correct location
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Step 3: Verify (file should contain username and key)
cat ~/.kaggle/kaggle.json
# {"username":"your_username","key":"your_api_key"}
```

### Method 2: Environment Variables

```bash
# Add to ~/.zshrc or ~/.bashrc
export KAGGLE_USERNAME="your_username"
export KAGGLE_KEY="your_api_key"

# Reload shell configuration
source ~/.zshrc

# Verify
echo $KAGGLE_USERNAME
```

### Verification

```python
# Test connection
from src.data_processing.kaggle_connector import KaggleDataConnector

try:
    connector = KaggleDataConnector()
    print("✓ Authentication successful!")
except EnvironmentError as e:
    print(f"✗ Authentication failed: {e}")
```

---

## Integration with Existing Project Structure

### Updated Directory Structure

```
gen-e2-data-analysis-MOH/
├── data/
│   ├── raw/
│   │   ├── kaggle/          # ← NEW: Kaggle data cache
│   │   └── moh_api/         # Legacy API data
│   ├── metadata/
│   │   ├── kaggle/          # ← NEW: Kaggle metadata
│   │   └── extraction_logs.json
│   ├── processed/
│   └── interim/
├── src/
│   ├── data_processing/
│   │   ├── kaggle_connector.py    # ← NEW: Kaggle connector
│   │   ├── db_connector.py        # Existing DB connector
│   │   ├── etl_pipeline.py        # Update to use Kaggle
│   │   └── data_validator.py
├── config/
│   └── database.yml         # ← UPDATED: Added Kaggle config
└── scripts/
    ├── run_extraction.py    # ← UPDATE: Support Kaggle source
    └── load_kaggle_data.py  # ← NEW: Dedicated Kaggle loader
```

### Configuration Hierarchy

```yaml
Priority Order:
  1. Kaggle (Primary Source)
     - Fast access
     - No authentication hassles
     - Complete dataset
  
  2. MOH API (Secondary/Validation)
     - Real-time updates
     - Official source
     - Requires API key
  
  3. Direct Database (Backup)
     - Historical data
     - Custom queries
     - Requires VPN/credentials
```

---

## Performance Considerations

### Caching Strategy

```yaml
Cache Behavior:
  - First Load: Downloads from Kaggle → Saves to data/raw/kaggle/
  - Subsequent Loads: Reads from local cache (instant)
  - Force Refresh: Set force_download=True to bypass cache
  
Memory Management:
  - Large datasets: Consider chunked reading
  - RAM Requirements: Monitor metadata['memory_usage_mb']
  - Optimization: Use data types optimization (category, int8, etc.)
```

### Optimization Tips for LLM Agents

```python
# Tip 1: Load specific columns only (if supported)
df = connector.load_dataset(pandas_kwargs={'usecols': ['patient_id', 'diagnosis']})

# Tip 2: Sample for exploration
df_sample = df.sample(n=10000, random_state=42)

# Tip 3: Optimize data types
df['category_col'] = df['category_col'].astype('category')
df['int_col'] = pd.to_numeric(df['int_col'], downcast='integer')
```

---

## Monitoring & Logging

### LLM-Interpretable Logs

The connector generates structured logs in this format:

```
2026-01-30 10:30:15 | INFO | Loading dataset: subhamjain/health-dataset-complete-singapore
2026-01-30 10:30:20 | INFO | Successfully loaded dataset with shape: (150000, 45)
2026-01-30 10:30:21 | INFO | Dataset dimensions: 150,000 rows × 45 columns
2026-01-30 10:30:21 | INFO | Memory usage: 52.3 MB
2026-01-30 10:30:21 | INFO | Missing data: 2.4%
2026-01-30 10:30:22 | INFO | Validation completed: PASSED
```

### Metadata Output Example

```yaml
extraction_timestamp: '2026-01-30T10:30:15'
dataset_id: subhamjain/health-dataset-complete-singapore
shape:
  rows: 150000
  columns: 45
columns:
  patient_id:
    dtype: int64
    non_null_count: 150000
    null_count: 0
    null_percentage: 0.0
    unique_values: 50000
    sample_values: [1001, 1002, 1003]
  diagnosis_code:
    dtype: object
    non_null_count: 147500
    null_count: 2500
    null_percentage: 1.67
    unique_values: 1250
    sample_values: ['J06.9', 'E11.9', 'I10']
memory_usage_mb: 52.3
data_quality:
  total_cells: 6750000
  missing_cells: 162000
  missing_percentage: 2.4
```

---

## LLM Agent Instructions

### When to Use This Connector

```
Use kaggle_connector.py when:
✓ Initial data exploration needed
✓ User requests "load health dataset"
✓ Baseline analysis required
✓ Fresh data pull requested
✓ Data validation needed before analysis

Do NOT use when:
✗ Data already loaded in memory
✗ User wants specific SQL query on database
✗ Real-time/streaming data required
✗ Custom API integration needed
```

### Typical LLM Workflow

```
1. Load Data
   → connector = KaggleDataConnector()
   → df = connector.load_dataset()

2. Inspect Metadata
   → metadata = connector.get_metadata()
   → Interpret structure and quality

3. Validate Quality
   → validation = connector.validate_dataset(df)
   → Make go/no-go decision

4. Proceed with Analysis
   → Based on validation status
   → Use df for downstream tasks

5. Document Findings
   → Save metadata for reproducibility
   → connector.save_metadata()
```

---

## Troubleshooting Guide

### Common Issues & Solutions

```yaml
Issue 1: "Kaggle credentials not found"
Solution:
  - Check ~/.kaggle/kaggle.json exists
  - Verify file permissions (chmod 600)
  - Or set KAGGLE_USERNAME and KAGGLE_KEY env vars
Command: ls -la ~/.kaggle/

Issue 2: "Dataset not found" / 404 Error
Solution:
  - Verify dataset ID is correct
  - Check dataset is public (not private)
  - Visit dataset URL on Kaggle to confirm
URL: https://www.kaggle.com/datasets/subhamjain/health-dataset-complete-singapore

Issue 3: "Memory error during load"
Solution:
  - Check available RAM
  - Load in chunks
  - Use data type optimization
  - Sample the data first

Issue 4: "Slow download speed"
Solution:
  - Downloads are cached after first load
  - Check internet connection
  - Kaggle may have server-side limits
  - Cache persists across sessions

Issue 5: "Import error: No module kagglehub"
Solution:
  - Install package: pip install kagglehub[pandas-datasets]
  - Verify installation: pip show kagglehub
  - Check Python environment is activated
```

---

## Next Steps & Recommendations

### For LLM Agents

1. **First Time Setup**
   ```bash
   # Install dependencies
   pip install kagglehub[pandas-datasets]
   
   # Setup credentials (if not done)
   # Follow Authentication Setup Guide above
   
   # Test connection
   python -c "from src.data_processing.kaggle_connector import KaggleDataConnector; KaggleDataConnector()"
   ```

2. **Initial Data Load**
   ```python
   # Load and inspect
   from src.data_processing.kaggle_connector import KaggleDataConnector
   
   connector = KaggleDataConnector()
   df = connector.load_dataset()
   
   # Save metadata for future reference
   connector.save_metadata("data/metadata/kaggle/initial_load.yml")
   
   # Print summary
   print(df.info())
   print(df.describe())
   print(df.head())
   ```

3. **Integrate with Existing Pipeline**
   - Update [etl_pipeline.py](../src/data_processing/etl_pipeline.py) to use Kaggle connector
   - Modify [run_extraction.py](../scripts/run_extraction.py) to support Kaggle source
   - Create scheduled jobs for periodic refresh

4. **Create Analysis Notebooks**
   - Exploratory analysis: notebooks/1_exploratory/kaggle_data_exploration.ipynb
   - Feature engineering: notebooks/3_feature_engineering/kaggle_features.ipynb

---

## References & Documentation

### Internal Documentation
- [Data Sources Overview](./data_sources.md)
- [Connector Module](../src/data_processing/kaggle_connector.py)
- [Database Configuration](../config/database.yml)
- [ETL Pipeline](../src/data_processing/etl_pipeline.py)

### External Resources
- Kaggle Dataset: https://www.kaggle.com/datasets/subhamjain/health-dataset-complete-singapore
- Kaggle Hub Documentation: https://github.com/Kaggle/kagglehub
- Kaggle API Setup: https://www.kaggle.com/docs/api

### Support
- Technical Issues: Check logs in `logs/etl/`
- Authentication Help: See Authentication Setup Guide above
- Data Quality Concerns: Review validation reports in `data/metadata/`

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-30  
**Maintained By**: Data Engineering Team  
**LLM-Optimized**: Yes ✓
