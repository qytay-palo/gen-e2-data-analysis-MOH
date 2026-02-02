# Shared Components Across Data Flows

**Purpose**: Document reusable data processing, analysis, and visualization components used across multiple user stories and epics.

**Last Updated**: 2 February 2026

---

## Shared Data Extractions

### Component: `kaggle_base_extraction`

**Used By**: e01-s01, e02-s01, e03-s01, e04-s01, e05-s01, e06-s01

**Description**: Standard pattern for extracting data from Kaggle dataset using kagglehub API

**Implementation**:
```python
import kagglehub
import pandas as pd
from pathlib import Path

class KaggleExtractor:
    """Reusable Kaggle data extraction component"""
    
    def __init__(self, dataset_id="subhamjain/health-dataset-complete-singapore"):
        self.dataset_id = dataset_id
        self.dataset_path = None
    
    def download_dataset(self):
        """Download entire dataset (cached locally)"""
        self.dataset_path = kagglehub.dataset_download(self.dataset_id)
        return self.dataset_path
    
    def load_table(self, table_name):
        """Load specific table from dataset"""
        if not self.dataset_path:
            self.download_dataset()
        
        file_path = Path(self.dataset_path) / table_name / f"{table_name}.csv"
        return pd.read_csv(file_path)
    
    def load_multiple_tables(self, table_names):
        """Load multiple tables at once"""
        return {name: self.load_table(name) for name in table_names}
```

**Configuration**: `config/kaggle_connection.yml`

**Benefits**:
- Consistent authentication handling
- Local caching to avoid repeated API calls
- Error handling and logging
- Reusable across all epics

---

### Component: `facility_data_extraction`

**Used By**: e01-s01, e03-s01, e04-s01, e05-s01, e06-s01

**Description**: Extract facility-related data (hospitals, clinics, beds, capacity)

**Source Tables**:
- `admission-and-outpatient-attendances-by-restructured-hospitals`
- `number-of-hospital-beds`
- `facilities-in-the-registry-of-medical-clinics-and-dental-clinics`
- `health-facilities-and-beds-in-inpatient-facilities`

**Common Filters**:
```yaml
year_range: 2006-2020
required_fields:
  - year
  - facility_identifier
  - attendances_no OR beds_no
```

**Code Reference**: `src/data_processing/shared/extract_facility_data.py`

---

### Component: `disease_data_extraction`

**Used By**: e02-s01, e03-s02, e04-s03

**Description**: Extract disease surveillance and health outcomes data

**Source Tables**:
- `principal-causes-of-death`
- `communicable-diseases-quarterly-crude-rates`
- `reportable-infectious-diseases`

**Code Reference**: `src/data_processing/shared/extract_disease_data.py`

---

### Component: `workforce_data_extraction`

**Used By**: e03-s01, e04-s02, e06-s04

**Description**: Extract healthcare workforce data (doctors, nurses, allied health)

**Source Tables**:
- `number-of-doctors`
- `number-of-nurses-and-midwives`
- `number-of-pharmacists`
- `number-of-physiotherapists`
- `number-of-dentists`

**Code Reference**: `src/data_processing/shared/extract_workforce_data.py`

---

## Shared Data Transformations

### Component: `column_standardization`

**Used By**: All epics

**Description**: Standardize column names across all tables

**Logic**:
- Convert to lowercase
- Replace spaces with underscores
- Remove special characters
- Create consistent naming conventions

**Implementation**:
```python
def standardize_column_names(df):
    """Standardize DataFrame column names"""
    df.columns = (
        df.columns
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('-', '_')
        .str.replace('[^a-z0-9_]', '', regex=True)
    )
    return df
```

**Code Reference**: `src/data_processing/shared/standardization.py`

---

### Component: `temporal_feature_engineering`

**Used By**: All epics with time series data

**Description**: Create standard temporal features for time series analysis

**Features Created**:
- `year_month` (datetime): First day of year for annual data
- `quarter` (int): Quarter number (1-4)
- `year_quarter` (string): YYYY-QN format
- `days_since_epoch` (int): For regression models
- `is_recent` (boolean): Flag for recent years

**Implementation**:
```python
def create_temporal_features(df, date_col='year'):
    """Create standard temporal features"""
    df['year_month'] = pd.to_datetime(df[date_col].astype(str) + '-01-01')
    df['quarter'] = df['year_month'].dt.quarter
    df['year_quarter'] = df['year_month'].dt.to_period('Q').astype(str)
    df['days_since_epoch'] = (df['year_month'] - pd.Timestamp('2000-01-01')).dt.days
    df['is_recent'] = df[date_col] >= 2015
    return df
```

**Code Reference**: `src/data_processing/shared/temporal_features.py`

---

### Component: `facility_categorization`

**Used By**: e01-s01, e01-s02, e01-s03, e03-s01, e05-s01

**Description**: Categorize healthcare facilities into standard types

**Categories**:
- Hospital (acute care, specialty, psychiatric)
- Polyclinic (primary care)
- GP Clinic (general practice)
- Specialty Center (disease-specific)
- Long-term Care (nursing homes, community hospitals)
- Other

**Implementation**:
```python
def categorize_facility(facility_name, facility_type):
    """Categorize facility based on name and type"""
    facility_lower = facility_name.lower()
    type_lower = facility_type.lower() if facility_type else ''
    
    if 'hospital' in facility_lower or 'hospital' in type_lower:
        if 'community' in facility_lower:
            return 'Community Hospital'
        elif 'psychiatric' in facility_lower:
            return 'Psychiatric Hospital'
        else:
            return 'Acute Care Hospital'
    elif 'polyclinic' in facility_lower:
        return 'Polyclinic'
    elif 'clinic' in facility_lower and 'dental' not in facility_lower:
        return 'GP Clinic'
    elif 'nursing home' in facility_lower:
        return 'Nursing Home'
    else:
        return 'Other'
```

**Code Reference**: `src/data_processing/shared/facility_categorization.py`

---

### Component: `disease_name_standardization`

**Used By**: e02-s01, e02-s02, e02-s03, e03-s02

**Description**: Standardize disease names across different source tables

**Mapping File**: `config/disease_name_mappings.yml`

**Features**:
- Map variations to standard names (e.g., "TB" → "Tuberculosis")
- Assign ICD-10 codes where applicable
- Categorize by disease type (respiratory, vector-borne, chronic, etc.)

**Implementation**:
```python
import yaml

class DiseaseStandardizer:
    def __init__(self, mapping_file='config/disease_name_mappings.yml'):
        with open(mapping_file, 'r') as f:
            self.mappings = yaml.safe_load(f)
    
    def standardize(self, disease_name):
        """Return standardized disease name"""
        disease_lower = disease_name.lower().strip()
        if disease_lower in self.mappings:
            return self.mappings[disease_lower]['standard_name']
        return disease_name.title()  # Fallback
    
    def get_category(self, disease_name):
        """Get disease category"""
        disease_lower = disease_name.lower().strip()
        if disease_lower in self.mappings:
            return self.mappings[disease_lower].get('category', 'Other')
        return 'Other'
    
    def get_icd10(self, disease_name):
        """Get ICD-10 code if available"""
        disease_lower = disease_name.lower().strip()
        if disease_lower in self.mappings:
            return self.mappings[disease_lower].get('icd10', None)
        return None
```

**Code Reference**: `src/data_processing/shared/disease_standardization.py`

---

### Component: `data_quality_validation`

**Used By**: All epics

**Description**: Standard data quality checks applied after extraction and cleaning

**Checks Implemented**:
- Schema validation (required columns present)
- Data type validation
- Range validation (numeric fields within expected bounds)
- Null value checks
- Duplicate detection
- Outlier detection

**Implementation**:
```python
class DataQualityValidator:
    """Reusable data quality validation"""
    
    def validate_schema(self, df, required_columns):
        """Check all required columns are present"""
        missing = set(required_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        return True
    
    def validate_ranges(self, df, field, min_val, max_val):
        """Check numeric field is within expected range"""
        invalid = df[(df[field] < min_val) | (df[field] > max_val)]
        if len(invalid) > 0:
            print(f"Warning: {len(invalid)} records outside range [{min_val}, {max_val}]")
        return invalid
    
    def detect_outliers(self, df, field, method='iqr'):
        """Detect statistical outliers"""
        if method == 'iqr':
            Q1 = df[field].quantile(0.25)
            Q3 = df[field].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return df[(df[field] < lower_bound) | (df[field] > upper_bound)]
        elif method == 'zscore':
            from scipy.stats import zscore
            z_scores = zscore(df[field])
            return df[abs(z_scores) > 3]
    
    def generate_report(self, df, output_path):
        """Generate comprehensive data quality report"""
        report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'duplicates': df.duplicated().sum(),
            'completeness': {col: (1 - df[col].isnull().mean()) * 100 for col in df.columns}
        }
        
        # Save report
        import json
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
```

**Code Reference**: `src/data_processing/shared/data_quality.py`

---

## Shared Analysis Methods

### Component: `utilization_rate_calculation`

**Used By**: e01-s02, e06-s02

**Description**: Calculate facility utilization rates

**Formula**: `utilization_rate = (actual_visits / capacity) × 100`

**Variations**:
- Daily utilization: `actual_visits / (beds × 365)`
- Bed occupancy rate: `occupied_bed_days / (available_beds × days)`

**Code Reference**: `src/analysis/shared/utilization_metrics.py`

---

### Component: `percentile_ranking`

**Used By**: e01-s03, e03-s06, e04-s05

**Description**: Calculate percentile rankings and performance tiers

**Implementation**:
```python
def calculate_percentile_rankings(df, metric_col, entity_col):
    """Calculate percentile rankings for entities"""
    df[f'{metric_col}_percentile'] = df[metric_col].rank(pct=True) * 100
    return df

def assign_performance_tier(percentile):
    """Assign performance tier based on percentile"""
    if percentile >= 90:
        return 'Top Performer'
    elif percentile >= 75:
        return 'High Performer'
    elif percentile >= 25:
        return 'Average Performer'
    elif percentile >= 10:
        return 'Below Average'
    else:
        return 'Low Performer'
```

**Code Reference**: `src/analysis/shared/ranking.py`

---

### Component: `time_series_baseline`

**Used By**: e02-s02, e04-s03, e06-s05

**Description**: Establish statistical baselines for time series data

**Methods**:
- Mean and standard deviation
- Seasonal decomposition
- Confidence intervals (95%, 99%)
- Alert thresholds

**Code Reference**: `src/analysis/shared/baseline_calculation.py`

---

### Component: `anomaly_detection`

**Used By**: e02-s03, e04-s03, e06-s05

**Description**: Statistical anomaly detection algorithms

**Algorithms**:
- Z-score method
- CUSUM (Cumulative Sum)
- EWMA (Exponentially Weighted Moving Average)
- Isolation Forest (ML-based)

**Code Reference**: `src/analysis/shared/anomaly_detection.py`

---

### Component: `forecasting_pipeline`

**Used By**: e02-s05, e06-s05

**Description**: Time series forecasting models

**Models Supported**:
- ARIMA (statistical)
- Prophet (Facebook's forecasting library)
- LSTM (deep learning, if applicable)

**Code Reference**: `src/models/shared/forecasting.py`

---

## Shared Visualizations

### Component: `plotly_templates`

**Used By**: All epics

**Description**: Standard Plotly visualization templates with consistent styling

**Templates**:
- Line charts (time series trends)
- Bar charts (comparisons)
- Scatter plots (correlations)
- Heatmaps (matrices)
- Choropleth maps (geographic)
- Box plots (distributions)
- Histogram (frequencies)

**Styling**:
```python
import plotly.graph_objects as go
import plotly.express as px

# Standard color palette
MOH_COLORS = {
    'primary': '#003366',  # Dark blue
    'secondary': '#0066CC',  # Blue
    'accent': '#FF6600',  # Orange
    'success': '#00CC66',  # Green
    'warning': '#FFCC00',  # Yellow
    'danger': '#CC0000',  # Red
    'neutral': '#666666'  # Gray
}

# Standard template
MOH_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        font={'family': 'Arial, sans-serif', 'size': 12},
        title={'font': {'size': 18, 'color': MOH_COLORS['primary']}},
        paper_bgcolor='white',
        plot_bgcolor='#F5F5F5'
    )
)

def create_line_chart(df, x, y, color=None, title=''):
    """Create standard line chart"""
    fig = px.line(df, x=x, y=y, color=color, title=title, template=MOH_TEMPLATE)
    return fig
```

**Code Reference**: `src/visualization/shared/plotly_templates.py`

---

### Component: `dashboard_components`

**Used By**: e01-s08, e02-s07, e03-s09

**Description**: Reusable Plotly Dash dashboard components

**Components**:
- KPI cards
- Filter dropdowns
- Date range pickers
- Data tables with sorting/filtering
- Download buttons

**Code Reference**: `src/visualization/shared/dashboard_components.py`

---

### Component: `report_generator`

**Used By**: e01-s07, e03-s08, e04-s07

**Description**: Generate PDF reports with standard formatting

**Features**:
- Standard report template (header, footer, sections)
- Table formatting
- Chart embedding
- Table of contents

**Library**: ReportLab or WeasyPrint

**Code Reference**: `src/visualization/shared/report_generator.py`

---

## Shared Utilities

### Component: `logging_config`

**Used By**: All epics

**Description**: Centralized logging configuration

**Features**:
- Console and file logging
- Different log levels (DEBUG, INFO, WARNING, ERROR)
- Timestamped log files
- Structured logging (JSON format)

**Code Reference**: `src/utils/logging_config.py`

---

### Component: `config_loader`

**Used By**: All epics

**Description**: Load configuration from YAML files

**Implementation**:
```python
import yaml
from pathlib import Path

class ConfigLoader:
    """Load configuration files"""
    
    def __init__(self, config_dir='config'):
        self.config_dir = Path(config_dir)
    
    def load(self, config_name):
        """Load specific config file"""
        config_path = self.config_dir / f'{config_name}.yml'
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
```

**Code Reference**: `src/utils/config_loader.py`

---

### Component: `file_path_manager`

**Used By**: All epics

**Description**: Manage file paths and directory structure

**Implementation**:
```python
from pathlib import Path

class FilePathManager:
    """Manage project file paths"""
    
    def __init__(self, project_root):
        self.root = Path(project_root)
        self.data = self.root / 'data'
        self.processed = self.data / 'processed'
        self.raw = self.data / 'raw'
        self.results = self.root / 'results'
        self.exports = self.results / 'exports'
        self.figures = self.root / 'reports' / 'figures'
    
    def ensure_dirs(self):
        """Create directories if they don't exist"""
        for path in [self.processed, self.raw, self.exports, self.figures]:
            path.mkdir(parents=True, exist_ok=True)
    
    def get_processed_path(self, filename):
        """Get path for processed data file"""
        return self.processed / filename
```

**Code Reference**: `src/utils/file_paths.py`

---

## Configuration Files

### `config/kaggle_connection.yml`

```yaml
dataset_id: "subhamjain/health-dataset-complete-singapore"
cache_dir: "~/.kaggle/cache"
timeout_seconds: 300
```

### `config/disease_name_mappings.yml`

```yaml
tuberculosis:
  standard_name: "Tuberculosis"
  icd10: "A15-A19"
  category: "Respiratory"

dengue:
  standard_name: "Dengue Fever"
  icd10: "A90"
  category: "Vector-Borne"

# ... more mappings
```

### `config/facility_categories.yml`

```yaml
acute_care_hospitals:
  - "Singapore General Hospital"
  - "National University Hospital"
  # ... more hospitals

polyclinics:
  - "Ang Mo Kio Polyclinic"
  - "Bedok Polyclinic"
  # ... more polyclinics
```

---

## Testing Strategy

### Component: `shared_test_fixtures`

**Description**: Reusable test data and fixtures for unit tests

**Fixtures**:
- Sample facility data (5-10 rows)
- Sample disease data (20-30 rows)
- Mock API responses
- Expected output schemas

**Code Reference**: `tests/fixtures/shared_fixtures.py`

---

## Dependency Management

### Shared Python Dependencies

```txt
# Data processing
pandas>=2.0.0
numpy>=1.24.0

# Kaggle API
kagglehub>=0.2.0

# Visualization
plotly>=5.14.0
seaborn>=0.12.0
matplotlib>=3.7.0

# Statistical analysis
scipy>=1.10.0
statsmodels>=0.14.0

# Machine learning (if needed)
scikit-learn>=1.2.0

# Time series forecasting
prophet>=1.1.0

# Dashboard
dash>=2.9.0
dash-bootstrap-components>=1.4.0

# Utilities
pyyaml>=6.0
python-dateutil>=2.8.0

# Testing
pytest>=7.3.0
pytest-cov>=4.0.0
```

**File**: `requirements.txt` (root level)

---

## Summary of Reusability

| Component | Epics Using | Lines Saved | Maintenance Effort |
|-----------|-------------|-------------|-------------------|
| kaggle_base_extraction | All 6 epics | ~600 lines | Low |
| column_standardization | All 6 epics | ~300 lines | Low |
| temporal_features | 5 epics | ~400 lines | Low |
| disease_standardization | 3 epics | ~500 lines | Medium |
| data_quality_validation | All 6 epics | ~800 lines | Low |
| plotly_templates | All 6 epics | ~1000 lines | Low |
| dashboard_components | 3 epics | ~1200 lines | Medium |

**Total Estimated Lines Saved**: ~4,800 lines of code

---

**Maintenance Note**: All shared components should have:
- Comprehensive docstrings
- Unit tests with >80% coverage
- Version control
- Change log
- Examples in documentation
