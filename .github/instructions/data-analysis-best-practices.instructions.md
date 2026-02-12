# Data Analysis Life Cycle Best Practices

## Purpose
This document provides **mandatory guidelines** for all data analysis work. When generating, reviewing, or modifying data analysis code, **ALWAYS follow these practices**.

## Rules

When assisting with data analysis tasks:

1. **NEVER modify files in `data/1_raw/`** - treat as read-only
2. **ALWAYS validate input data** before processing
3. **ALWAYS use type hints** in function definitions
4. **ALWAYS log using `logging` module**, never `print()` for production code
5. **ALWAYS save intermediate results** to `data/3_interim/` during processing
6. **ALWAYS save final results** to `data/4_processed/` with documentation
7. **ALWAYS use descriptive variable names** (`disease_burden_metrics` not `dbm`)
8. **ALWAYS handle exceptions** explicitly with informative error messages
9. **ALWAYS document data transformations** with clear comments
10. **ALWAYS generate data quality reports** after cleaning steps

## 🗂️ Required Folder Structure

```
data/
├── 1_raw/           # ❌ READ-ONLY: Original source data, never modify
├── 2_external/      # Third-party/reference data with documented sources  
├── 3_interim/       # ✅ WRITE: Intermediate processing checkpoints
├── 4_processed/     # ✅ WRITE: Final analysis-ready data with README
└── schemas/         # Data schemas and metadata definitions
```

## Overview

This document outlines best practices for the complete data analysis life cycle, from problem definition through deployment and monitoring. These practices ensure reproducibility, quality, and actionable insights from data analysis projects.

## Data Analysis Life Cycle Stages

```
1. Problem Definition & Planning
   ↓
2. Data Collection & Acquisition  
   ↓
3. Data Exploration & Understanding
   ↓
4. Data Preparation & Cleaning
   ↓
5. Feature Engineering & Transformation
   ↓
6. Analysis & Modeling
   ↓
7. Validation & Testing
   ↓
8. Interpretation & Visualization
   ↓
9. Documentation & Communication
   ↓
10. Deployment & Monitoring
```

---

## 1. Problem Definition & Planning

### Define Clear Objectives
- **Write specific, measurable questions** the analysis should answer
- Identify key stakeholders and their requirements
- Define success criteria and metrics upfront
- Document assumptions and constraints

### Create Problem Statement Document
```markdown
## Problem Statement
**Question**: What are the seasonal patterns in respiratory disease outbreaks?

**Stakeholders**: Public Health Epidemiologists, Healthcare Administrators

**Success Criteria**:
- Identify peak outbreak months with >80% accuracy
- Quantify disease burden by season
- Generate actionable early warning indicators

**Constraints**:
- Historical data available from 2015-2023
- Weekly aggregated case counts (no patient-level data)
- Analysis must complete within 2 weeks
```

### Plan Data Requirements
- List required data sources and availability
- Identify data quality concerns upfront
- Define minimum viable dataset criteria
- Plan data access and permissions

**Location**: Store in `docs/problem_statements/` or `docs/objectives/`

---

## 2. Data Collection & Acquisition

### Organize by Data Provenance
Use the standardized folder structure:

```
data/
├── 1_raw/           # Original, immutable source data
├── 2_external/      # Third-party or reference data
├── 3_interim/       # Intermediate processing steps
├── 4_processed/     # Final analysis-ready data
└── schemas/         # Data schemas and metadata
```

### Raw Data Management (`data/1_raw/`)
- **Never modify raw data files** - treat as read-only
- Preserve original file formats and structure
- Document data source, collection date, and methodology
- Include `.gitkeep` files to preserve directory structure
- Use descriptive filenames with dates: `disease_surveillance_2023-01-15.csv`

```python
# Good practice: Load raw data with metadata
from pathlib import Path
from datetime import datetime

RAW_DATA_PATH = Path('data/1_raw')

def load_raw_surveillance_data(filename: str) -> pd.DataFrame:
    """Load raw surveillance data with provenance tracking.
    
    Args:
        filename: Name of raw data file
        
    Returns:
        DataFrame with metadata attributes
    """
    filepath = RAW_DATA_PATH / filename
    
    if not filepath.exists():
        raise FileNotFoundError(f"Raw data not found: {filepath}")
    
    df = pd.read_csv(filepath)
    
    # Add metadata as attributes
    df.attrs['source_file'] = filename
    df.attrs['load_timestamp'] = datetime.now().isoformat()
    df.attrs['row_count_original'] = len(df)
    
    logger.info(f"Loaded {len(df):,} rows from {filename}")
    return df
```

### External Reference Data (`data/2_external/`)
- Store third-party datasets (e.g., population data, disease taxonomies)
- Document source, version, and update frequency
- Include license information if applicable
- Create README.md listing all external sources

```markdown
# External Data Sources

## population_singapore_2023.csv
- **Source**: Singapore Department of Statistics
- **URL**: https://www.singstat.gov.sg/...
- **Date Retrieved**: 2024-01-15
- **Update Frequency**: Annual
- **License**: Public Domain

## who_disease_classification.json
- **Source**: WHO International Classification of Diseases (ICD-11)
- **Version**: 2023 Release
- **Date Retrieved**: 2024-01-10
```

### Data Acquisition Automation
```python
def download_external_data(
    url: str,
    destination: Path,
    force_update: bool = False
) -> Path:
    """Download external data with caching.
    
    Args:
        url: Source URL
        destination: Local file path in data/2_external/
        force_update: Re-download even if file exists
        
    Returns:
        Path to downloaded file
    """
    if destination.exists() and not force_update:
        logger.info(f"Using cached data: {destination}")
        return destination
    
    logger.info(f"Downloading from {url}")
    
    # Download logic here
    # ... 
    
    # Log metadata
    metadata = {
        'source_url': url,
        'download_date': datetime.now().isoformat(),
        'file_size_bytes': destination.stat().st_size
    }
    
    metadata_file = destination.with_suffix('.json')
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return destination
```

---

## 3. Data Exploration & Understanding

### Initial Data Profiling
Conduct systematic exploration before any transformations:

```python
def profile_dataset(df: pd.DataFrame, dataset_name: str) -> Dict:
    """Generate comprehensive data profile.
    
    Returns:
        Dictionary with profiling statistics
    """
    profile = {
        'dataset': dataset_name,
        'timestamp': datetime.now().isoformat(),
        'shape': {'rows': len(df), 'columns': len(df.columns)},
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'columns': {},
        'missing_data': df.isna().sum().to_dict(),
        'duplicate_rows': df.duplicated().sum(),
        'data_types': df.dtypes.astype(str).to_dict()
    }
    
    # Per-column statistics
    for col in df.columns:
        col_profile = {
            'dtype': str(df[col].dtype),
            'missing_count': df[col].isna().sum(),
            'missing_pct': (df[col].isna().sum() / len(df)) * 100,
            'unique_count': df[col].nunique()
        }
        
        if pd.api.types.is_numeric_dtype(df[col]):
            col_profile.update({
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'mean': float(df[col].mean()),
                'median': float(df[col].median()),
                'std': float(df[col].std())
            })
        
        profile['columns'][col] = col_profile
    
    return profile

# Usage in notebook or script
profile = profile_dataset(df_raw, 'disease_surveillance_raw')

# Save profile report
with open('data/3_interim/data_profile_report.json', 'w') as f:
    json.dump(profile, f, indent=2)
```

### Exploratory Data Analysis (EDA) Checklist
- [ ] Check data dimensions (rows, columns)
- [ ] Examine data types for each column
- [ ] Identify missing values and patterns
- [ ] Detect duplicates
- [ ] Analyze distributions (histograms, box plots)
- [ ] Check for outliers and anomalies
- [ ] Explore relationships between variables (correlation matrix)
- [ ] Identify temporal patterns if time-series data
- [ ] Document unexpected findings

### Use Notebooks for Exploration
- Keep exploratory notebooks in `notebooks/1_exploratory/`
- Name with sequence numbers: `01_initial_data_profiling.ipynb`
- Use markdown cells to document findings
- Clear outputs before committing to version control

```python
# Notebook cell 1: Setup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline
sns.set_style('whitegrid')

# Notebook cell 2: Document objective
"""
## Objective
Initial exploration of weekly disease surveillance data

## Data Source
data/1_raw/weekly_disease_bulletin_2020-2023.csv

## Key Questions
1. What is the completeness of the data?
2. Are there any temporal gaps?
3. What is the distribution of case counts?
"""
```

---

## 4. Data Preparation & Cleaning

### Store Interim Results (`data/3_interim/`)
- Save intermediate processing steps for debugging and auditing
- Use clear, descriptive filenames with processing step indicators
- Document what processing was applied

```python
def clean_disease_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize disease surveillance data.
    
    Cleaning steps:
    1. Remove duplicate records
    2. Standardize date formats
    3. Handle missing values
    4. Validate case counts (non-negative)
    5. Standardize disease names
    
    Args:
        df_raw: Raw disease surveillance data
        
    Returns:
        Cleaned DataFrame
    """
    logger.info(f"Starting data cleaning: {len(df_raw)} rows")
    
    df_clean = df_raw.copy()
    
    # Remove exact duplicates
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    duplicates_removed = initial_rows - len(df_clean)
    logger.info(f"Removed {duplicates_removed} duplicate rows")
    
    # Standardize dates
    df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
    invalid_dates = df_clean['date'].isna().sum()
    if invalid_dates > 0:
        logger.warning(f"Found {invalid_dates} invalid dates, removing rows")
        df_clean = df_clean.dropna(subset=['date'])
    
    # Handle missing case counts
    if 'case_count' in df_clean.columns:
        # Option 1: Drop rows with missing case counts
        df_clean = df_clean.dropna(subset=['case_count'])
        
        # Option 2: Alternative - fill with 0 if appropriate
        # df_clean['case_count'] = df_clean['case_count'].fillna(0)
    
    # Validate case counts are non-negative
    if 'case_count' in df_clean.columns:
        negative_counts = (df_clean['case_count'] < 0).sum()
        if negative_counts > 0:
            logger.error(f"Found {negative_counts} negative case counts")
            df_clean = df_clean[df_clean['case_count'] >= 0]
    
    # Standardize disease names (trim whitespace, title case)
    if 'disease' in df_clean.columns:
        df_clean['disease'] = df_clean['disease'].str.strip().str.title()
    
    # Save interim cleaned data
    interim_path = Path('data/3_interim/disease_data_cleaned.csv')
    df_clean.to_csv(interim_path, index=False)
    logger.info(f"Saved cleaned data: {interim_path}")
    
    logger.info(f"Cleaning complete: {len(df_clean)} rows retained")
    return df_clean
```

### Data Quality Report
Generate and save quality reports after cleaning:

```python
def generate_quality_report(
    df_raw: pd.DataFrame,
    df_cleaned: pd.DataFrame,
    output_path: str = 'results/tables/data_quality_report.json'
) -> Dict:
    """Generate data quality report comparing raw and cleaned data."""
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'raw_data': {
            'rows': len(df_raw),
            'columns': len(df_raw.columns),
            'missing_values': df_raw.isna().sum().sum(),
            'duplicates': df_raw.duplicated().sum()
        },
        'cleaned_data': {
            'rows': len(df_cleaned),
            'columns': len(df_cleaned.columns),
            'missing_values': df_cleaned.isna().sum().sum(),
            'duplicates': df_cleaned.duplicated().sum()
        },
        'changes': {
            'rows_removed': len(df_raw) - len(df_cleaned),
            'removal_rate': ((len(df_raw) - len(df_cleaned)) / len(df_raw)) * 100
        }
    }
    
    # Save report
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"Quality report saved: {output_path}")
    return report
```

---

## 5. Feature Engineering & Transformation

### Create Analysis-Ready Data (`data/4_processed/`)
- Final datasets ready for analysis/modeling
- Well-documented with data dictionaries
- Optimized data types for performance
- Include README.md explaining each file

```python
def engineer_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add time-based features for temporal analysis.
    
    Features added:
    - year, month, week, quarter
    - day_of_week, is_weekend
    - season (meteorological)
    """
    df_featured = df.copy()
    
    # Ensure date column is datetime
    df_featured['date'] = pd.to_datetime(df_featured['date'])
    
    # Extract temporal components
    df_featured['year'] = df_featured['date'].dt.year.astype('int16')
    df_featured['month'] = df_featured['date'].dt.month.astype('int8')
    df_featured['week'] = df_featured['date'].dt.isocalendar().week.astype('int8')
    df_featured['quarter'] = df_featured['date'].dt.quarter.astype('int8')
    df_featured['day_of_week'] = df_featured['date'].dt.dayofweek.astype('int8')
    df_featured['is_weekend'] = (df_featured['day_of_week'] >= 5).astype('int8')
    
    # Add season (Singapore context - monsoon seasons)
    def get_season(month):
        """Singapore monsoon seasons."""
        if month in [12, 1, 2]:
            return 'Northeast Monsoon'
        elif month in [3, 4, 5]:
            return 'Inter-monsoon'
        elif month in [6, 7, 8, 9]:
            return 'Southwest Monsoon'
        else:
            return 'Inter-monsoon'
    
    df_featured['season'] = df_featured['month'].apply(get_season)
    df_featured['season'] = df_featured['season'].astype('category')
    
    return df_featured

def create_processed_dataset(df: pd.DataFrame, output_name: str) -> Path:
    """Create final processed dataset with optimizations.
    
    Args:
        df: Cleaned and featured DataFrame
        output_name: Name for processed file
        
    Returns:
        Path to saved file
    """
    # Optimize data types
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() < 50:  # Low cardinality
            df[col] = df[col].astype('category')
    
    # Save to processed folder
    output_path = Path('data/4_processed') / output_name
    df.to_csv(output_path, index=False)
    
    logger.info(f"Processed data saved: {output_path}")
    logger.info(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    return output_path
```

### Document Processed Datasets
Create `data/4_processed/README.md`:

```markdown
# Processed Datasets

## disease_burden_metrics.csv
**Description**: Disease burden metrics calculated from weekly surveillance data

**Source**: Derived from data/1_raw/weekly_disease_bulletin_2020-2023.csv

**Processing Steps**:
1. Data cleaning and validation (scripts/clean_data.py)
2. Temporal feature engineering
3. Burden metric calculations (incidence rate, YLL, etc.)

**Columns**:
- `disease` (str): Standardized disease name
- `year` (int): Year of observation
- `week` (int): ISO week number
- `case_count` (int): Number of reported cases
- `incidence_rate` (float): Cases per 100,000 population
- `burden_score` (float): Composite burden metric (0-100)

**Rows**: 12,458
**Date Range**: 2020-W01 to 2023-W52
**Last Updated**: 2024-02-11
```

---

## 6. Analysis & Modeling

### Separate Analysis Notebooks
Keep analysis notebooks in `notebooks/2_analysis/`:

```
notebooks/
├── 1_exploratory/
│   ├── 01_disease_data_profiling.ipynb
│   └── 02_temporal_patterns_exploration.ipynb
└── 2_analysis/
    ├── 01_burden_metrics_calculation.ipynb
    ├── 02_seasonal_trend_analysis.ipynb
    └── 03_outbreak_detection_model.ipynb
```

### Modular Analysis Functions
Extract reusable analysis code to `src/analysis/`:

```python
# src/analysis/burden_metrics.py

def calculate_incidence_rate(
    cases: pd.Series,
    population: int,
    per_population: int = 100_000
) -> pd.Series:
    """Calculate incidence rate per specified population.
    
    Args:
        cases: Series of case counts
        population: Total population at risk
        per_population: Rate per this many people (default: 100,000)
        
    Returns:
        Series of incidence rates
    """
    return (cases / population) * per_population

def calculate_disease_burden_score(
    incidence_rate: float,
    severity_weight: float,
    hospitalization_rate: float
) -> float:
    """Calculate composite disease burden score.
    
    Score combines incidence, severity, and healthcare utilization.
    
    Args:
        incidence_rate: Cases per 100k population
        severity_weight: Disease severity factor (0-1)
        hospitalization_rate: Proportion requiring hospitalization
        
    Returns:
        Burden score (0-100 scale)
    """
    raw_score = incidence_rate * severity_weight * (1 + hospitalization_rate)
    # Normalize to 0-100 scale
    normalized_score = min(100, raw_score / 10)
    return normalized_score
```

### Analysis Workflow Pattern

```python
# notebooks/2_analysis/01_burden_metrics_calculation.ipynb

# Cell 1: Imports
from pathlib import Path
import pandas as pd
from src.analysis.burden_metrics import (
    calculate_incidence_rate,
    calculate_disease_burden_score
)
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Cell 2: Load processed data
PROCESSED_DATA = Path('data/4_processed')
df = pd.read_csv(PROCESSED_DATA / 'disease_data_featured.csv')
logger.info(f"Loaded {len(df):,} records")

# Cell 3: Load parameters
with open(Path('data/parameters/disease_parameters.json'), 'r') as f:
    disease_params = json.load(f)

# Cell 4: Calculate metrics
SINGAPORE_POPULATION = 5_686_000  # 2023 estimate

df['incidence_rate'] = calculate_incidence_rate(
    df['case_count'],
    SINGAPORE_POPULATION
)

# Cell 5: Save results
results_path = Path('data/4_processed/disease_burden_metrics.csv')
df.to_csv(results_path, index=False)
logger.info(f"Results saved: {results_path}")
```

---

## 7. Validation & Testing

### Statistical Validation
```python
def validate_analysis_results(
    results: pd.DataFrame,
    expected_columns: List[str],
    value_ranges: Dict[str, Tuple[float, float]]
) -> bool:
    """Validate analysis results meet expectations.
    
    Args:
        results: DataFrame with analysis results
        expected_columns: Required column names
        value_ranges: Dict of {column: (min, max)} acceptable ranges
        
    Returns:
        True if all validations pass
        
    Raises:
        ValueError: If validation fails
    """
    # Check required columns
    missing_cols = set(expected_columns) - set(results.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Check value ranges
    for col, (min_val, max_val) in value_ranges.items():
        if col not in results.columns:
            continue
        
        out_of_range = (
            (results[col] < min_val) | (results[col] > max_val)
        ).sum()
        
        if out_of_range > 0:
            logger.warning(
                f"{out_of_range} values in {col} outside range "
                f"[{min_val}, {max_val}]"
            )
    
    # Check for unexpected nulls
    null_counts = results.isna().sum()
    if null_counts.any():
        logger.warning(f"Null values found:\n{null_counts[null_counts > 0]}")
    
    return True

# Usage
validate_analysis_results(
    df_metrics,
    expected_columns=['disease', 'incidence_rate', 'burden_score'],
    value_ranges={
        'incidence_rate': (0, 10000),
        'burden_score': (0, 100)
    }
)
```

### Sensitivity Analysis
Test robustness of results to parameter changes:

```python
def run_sensitivity_analysis(
    data: pd.DataFrame,
    analysis_func: callable,
    param_name: str,
    param_values: List[float]
) -> pd.DataFrame:
    """Run sensitivity analysis on analysis function.
    
    Args:
        data: Input data
        analysis_func: Function to test
        param_name: Name of parameter to vary
        param_values: List of parameter values to test
        
    Returns:
        DataFrame with results for each parameter value
    """
    results = []
    
    for value in param_values:
        logger.info(f"Testing {param_name}={value}")
        
        result = analysis_func(data, **{param_name: value})
        result['sensitivity_param'] = param_name
        result['sensitivity_value'] = value
        
        results.append(result)
    
    return pd.concat(results, ignore_index=True)
```

---

## 8. Interpretation & Visualization

### Create Publication-Quality Figures
Save all figures to `results/figures/`:

```python
def create_disease_burden_heatmap(
    df: pd.DataFrame,
    save_path: str = 'results/figures/disease_burden_heatmap.png'
) -> None:
    """Create heatmap of disease burden over time.
    
    Args:
        df: DataFrame with disease, time period, and burden metrics
        save_path: Where to save figure
    """
    # Pivot data for heatmap
    pivot = df.pivot_table(
        index='disease',
        columns='year',
        values='burden_score',
        aggfunc='mean'
    )
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    sns.heatmap(
        pivot,
        annot=True,
        fmt='.1f',
        cmap='YlOrRd',
        cbar_kws={'label': 'Burden Score'},
        ax=ax
    )
    
    ax.set_title(
        'Disease Burden Score by Year',
        fontsize=16,
        fontweight='bold',
        pad=20
    )
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Disease', fontsize=12)
    
    plt.tight_layout()
    
    # Save with high DPI
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    logger.info(f"Figure saved: {save_path}")
    
    plt.show()
```

### Save Summary Tables
Store summary tables in `results/tables/`:

```python
def create_summary_table(
    df: pd.DataFrame,
    save_path: str = 'results/tables/burden_metrics_summary.csv'
) -> pd.DataFrame:
    """Create summary statistics table.
    
    Args:
        df: DataFrame with metrics
        save_path: Where to save table
        
    Returns:
        Summary DataFrame
    """
    summary = df.groupby('disease').agg({
        'case_count': ['sum', 'mean', 'std'],
        'incidence_rate': ['mean', 'max'],
        'burden_score': ['mean', 'max']
    }).round(2)
    
    # Flatten column names
    summary.columns = ['_'.join(col).strip() for col in summary.columns]
    summary = summary.reset_index()
    
    # Sort by total cases
    summary = summary.sort_values('case_count_sum', ascending=False)
    
    # Save
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(save_path, index=False)
    logger.info(f"Summary table saved: {save_path}")
    
    return summary
```

---

## 9. Documentation & Communication

### Analysis Documentation Structure
```
docs/
├── objectives/              # Problem statements and goals
├── methodology/            # Analysis methods and approaches
├── data_dictionary/        # Data field definitions
├── domain_knowledge/       # Subject matter context
└── results/                # Analysis findings and reports
```

### Document Key Decisions
Create decision log for important analytical choices:

```markdown
# Analysis Decision Log

## Decision 001: Missing Value Handling
**Date**: 2024-02-10
**Context**: 3.2% of case_count values are missing in raw data
**Decision**: Drop rows with missing case_counts
**Rationale**: 
- Missing values are random (MCAR confirmed by Little's test)
- Small percentage won't bias results
- Imputation would introduce uncertainty in public health metrics
**Alternatives Considered**:
- Mean imputation: Rejected - artificial inflation of case counts
- Zero-fill: Rejected - misrepresents actual missing data
**Impact**: Dataset reduced from 12,845 to 12,433 rows

## Decision 002: Outbreak Threshold Selection
**Date**: 2024-02-11
**Context**: Need to define outbreak alert threshold
**Decision**: Use 2 standard deviations above 4-week rolling mean
**Rationale**:
- Balances sensitivity (95% confidence) with specificity
- 4-week window smooths weekly reporting variations
- Aligns with WHO outbreak detection guidelines
**Parameters**: threshold_std=2.0, window=4 weeks
```

### Create Analysis Reports
```python
def generate_analysis_report(
    summary_stats: Dict,
    figures: List[str],
    output_path: str = 'docs/results/analysis_report.md'
) -> None:
    """Generate markdown analysis report.
    
    Args:
        summary_stats: Dictionary of key statistics
        figures: List of figure paths to include
        output_path: Where to save report
    """
    report = f"""# Disease Burden Analysis Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Analysis Period**: {summary_stats['date_range']['start']} to {summary_stats['date_range']['end']}

## Executive Summary

This analysis examined disease burden patterns across {summary_stats['n_diseases']} 
infectious diseases over {summary_stats['n_years']} years.

### Key Findings

1. **Highest Burden Disease**: {summary_stats['top_disease']} 
   - Total cases: {summary_stats['top_disease_cases']:,}
   - Peak incidence: {summary_stats['peak_incidence']:.1f} per 100k

2. **Seasonal Patterns**: Clear seasonality detected in {summary_stats['n_seasonal']} diseases

3. **Trend Analysis**: {summary_stats['increasing_diseases']} diseases show 
   increasing trends over study period

## Visualizations

"""
    
    for fig_path in figures:
        report += f"![{Path(fig_path).stem}]({fig_path})\n\n"
    
    report += f"""
## Methodology

- **Data Source**: Weekly disease surveillance bulletins
- **Analysis Period**: {summary_stats['date_range']['start']} to {summary_stats['date_range']['end']}
- **Metrics Calculated**: Incidence rate, disease burden score
- **Statistical Methods**: Time series decomposition, trend analysis

## Data Quality

- **Completeness**: {summary_stats['completeness']:.1f}%
- **Records Analyzed**: {summary_stats['n_records']:,}
- **Data Quality Score**: {summary_stats['quality_score']:.1f}/100

## Recommendations

Based on this analysis, we recommend:

1. Enhanced surveillance for high-burden diseases
2. Seasonal preparedness planning for diseases with clear seasonal patterns
3. Further investigation into increasing disease trends

---
*Full analysis code available in notebooks/2_analysis/*
"""
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(report)
    
    logger.info(f"Analysis report saved: {output_path}")
```

---

## 10. Deployment & Monitoring

### Automate Reproducible Workflows
Create scripts in `scripts/` for end-to-end pipeline:

```python
# scripts/run_full_analysis_pipeline.py

"""
Complete analysis pipeline automation.
Run: python scripts/run_full_analysis_pipeline.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_processing.validation import load_disease_data
from src.data_processing.profiling import profile_dataset
from src.analysis.burden_metrics import calculate_all_metrics
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    """Run complete analysis pipeline."""
    
    logger.info("="*60)
    logger.info("Starting Disease Burden Analysis Pipeline")
    logger.info(f"Timestamp: {datetime.now()}")
    logger.info("="*60)
    
    try:
        # Stage 1: Load raw data
        logger.info("\n[1/5] Loading raw data...")
        df_raw = load_disease_data('data/1_raw/disease_surveillance.csv')
        
        # Stage 2: Data profiling
        logger.info("\n[2/5] Profiling data...")
        profile = profile_dataset(df_raw, 'disease_surveillance')
        
        # Stage 3: Data cleaning
        logger.info("\n[3/5] Cleaning data...")
        from src.data_processing.cleaning import clean_disease_data
        df_clean = clean_disease_data(df_raw)
        
        # Save interim
        df_clean.to_csv('data/3_interim/disease_data_cleaned.csv', index=False)
        
        # Stage 4: Calculate metrics
        logger.info("\n[4/5] Calculating burden metrics...")
        df_metrics = calculate_all_metrics(df_clean)
        
        # Save processed
        df_metrics.to_csv('data/4_processed/disease_burden_metrics.csv', index=False)
        
        # Stage 5: Generate outputs
        logger.info("\n[5/5] Generating visualizations and reports...")
        from src.visualization.plots import create_all_figures
        from src.reporting.summary import generate_analysis_report
        
        create_all_figures(df_metrics)
        generate_analysis_report(df_metrics)
        
        logger.info("\n" + "="*60)
        logger.info("Pipeline completed successfully!")
        logger.info("="*60)
        
        return 0
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

### Version Control for Analysis
Tag analysis versions in git:

```bash
# After completing major analysis milestone
git tag -a v1.0-burden-analysis -m "Initial disease burden analysis complete"
git push origin v1.0-burden-analysis
```

### Create Analysis Manifest
Document exact environment and data versions:

```json
{
  "analysis_id": "burden-analysis-v1.0",
  "timestamp": "2024-02-11T14:30:00Z",
  "analyst": "Public Health Team",
  "data_sources": [
    {
      "file": "data/1_raw/disease_surveillance_2020-2023.csv",
      "md5_hash": "a3f5e1b2c4d5e6f7a8b9c0d1e2f3a4b5",
      "row_count": 12845
    }
  ],
  "environment": {
    "python_version": "3.10.12",
    "key_packages": {
      "pandas": "2.0.3",
      "numpy": "1.24.3",
      "scikit-learn": "1.3.0"
    }
  },
  "parameters": {
    "outbreak_threshold_std": 2.0,
    "rolling_window_weeks": 4,
    "singapore_population": 5686000
  },
  "outputs": [
    "data/4_processed/disease_burden_metrics.csv",
    "results/figures/disease_burden_heatmap.png",
    "results/tables/burden_metrics_summary.csv"
  ]
}
```

---

## Summary Checklist

### ✅ For Each Analysis Project

**Planning Phase**
- [ ] Problem statement documented
- [ ] Success criteria defined
- [ ] Data requirements identified
- [ ] Stakeholders consulted

**Data Collection**
- [ ] Raw data stored in `data/1_raw/` (read-only)
- [ ] External data documented in `data/2_external/`
- [ ] Data provenance tracked
- [ ] .gitignore configured

**Exploration**
- [ ] Data profiling report generated
- [ ] EDA notebook created
- [ ] Data quality issues documented
- [ ] Unexpected findings noted

**Preparation**
- [ ] Cleaning steps documented
- [ ] Interim data saved to `data/3_interim/`
- [ ] Data quality report generated
- [ ] Missing value strategy documented

**Feature Engineering**
- [ ] Features engineered and documented
- [ ] Final dataset saved to `data/4_processed/`
- [ ] README.md created for processed data
- [ ] Data types optimized

**Analysis**
- [ ] Analysis notebooks organized in `notebooks/2_analysis/`
- [ ] Reusable functions extracted to `src/`
- [ ] Results validated
- [ ] Sensitivity analysis conducted

**Visualization & Communication**
- [ ] Publication-quality figures created
- [ ] Summary tables generated
- [ ] Analysis report written
- [ ] Key decisions documented

**Deployment**
- [ ] Pipeline script created
- [ ] Analysis reproducible
- [ ] Environment documented
- [ ] Version tagged in git

---

## Anti-Patterns to Avoid

### ❌ Don't Do This

1. **Modifying raw data in place**
   ```python
   # BAD - Never do this!
   df_raw = pd.read_csv('data/1_raw/original.csv')
   df_raw['new_column'] = calculation()
   df_raw.to_csv('data/1_raw/original.csv', index=False)  # Overwrites original!
   ```

2. **Analysis without exploration**
   - Jumping straight to modeling without understanding your data
   - Not checking distributions, missing values, or outliers first

3. **Undocumented transformations**
   ```python
   # BAD - What did this do?
   df2 = df1.copy()
   df2['x'] = df2['x'] * 2.5
   df2 = df2[df2['y'] > threshold]
   ```

4. **Hard-to-reproduce analysis**
   - Manual Excel manipulations not scripted
   - Point-and-click tools without audit trail
   - "Final_FINAL_v3" file naming

5. **Results without validation**
   - Not checking if results make domain sense
   - No sensitivity analysis
   - Ignoring data quality issues

6. **Missing documentation**
   - No README explaining what files are
   - No data dictionary
   - No methodology notes

---

## Tools and Libraries

### Recommended Python Stack
```python
# Data manipulation
pandas>=2.0.0
numpy>=1.24.0

# Visualization
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0  # For interactive plots

# Statistical analysis
scipy>=1.10.0
statsmodels>=0.14.0
scikit-learn>=1.3.0

# Data profiling
pandas-profiling>=3.6.0  # Automated EDA reports

# Data validation
great-expectations>=0.17.0  # Data quality framework

# Utilities
pyyaml>=6.0
python-dotenv>=1.0.0  # Environment variables
```

### Useful Commands

```bash
# Generate automated data profile
pandas_profiling data/1_raw/disease_data.csv --output results/data_profile.html

# Run full pipeline
python scripts/run_full_analysis_pipeline.py

# Run specific analysis notebook
jupyter nbconvert --to notebook --execute notebooks/2_analysis/01_burden_metrics.ipynb

# Check data file hash for versioning
md5 data/1_raw/disease_surveillance.csv
```

---

## 🤖 LLM Instruction Summary

When writing or reviewing data analysis code:

### ✅ ALWAYS Do:
- Load raw data from `data/1_raw/` (read-only)
- Validate data immediately after loading
- Use type hints: `def func(df: pd.DataFrame, col: str) -> pd.Series:`
- Log with `logger.info()`, `logger.warning()`, `logger.error()`
- Save checkpoints to `data/3_interim/` with descriptive names
- Save final outputs to `data/4_processed/` with README.md
- Use constants: `SINGAPORE_POPULATION = 5_686_000`
- Handle exceptions: `try/except` with specific exception types
- Document transformations in docstrings
- Generate quality reports after cleaning
- Create visualizations in `results/figures/`
- Create summary tables in `results/tables/`

### ❌ NEVER Do:
- Modify files in `data/1_raw/`
- Use `print()` for logging in production code
- Use hardcoded paths: `/Users/john/Desktop/data.csv`
- Use magic numbers without explanation
- Silence exceptions with bare `except: pass`
- Leave undocumented transformations
- Create "final_v2_FINAL.py" files
- Skip data validation steps
- Ignore missing values without strategy
- Overwrite processed data without versioning

### 📊 Standard Analysis Pattern:
```python
# 1. Load and validate
df_raw = load_disease_data('data/1_raw/surveillance.csv')

# 2. Clean and save interim
df_clean = clean_disease_data(df_raw)
df_clean.to_csv('data/3_interim/surveillance_cleaned.csv', index=False)

# 3. Feature engineering
df_featured = engineer_features(df_clean)

# 4. Calculate metrics
df_metrics = calculate_burden_metrics(df_featured)

# 5. Save final with documentation
df_metrics.to_csv('data/4_processed/disease_burden_metrics.csv', index=False)

# 6. Generate outputs
create_visualizations(df_metrics, save_path='results/figures/')
create_summary_table(df_metrics, save_path='results/tables/')
```

---

**Remember**: Good data analysis is reproducible, well-documented, and tells a clear story from data to insights.