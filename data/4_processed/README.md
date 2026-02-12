# Processed Infectious Disease Data

**Generated**: 2026-02-11 13:54:06
**Source**: Kaggle - Weekly Infectious Disease Bulletin Cases (2012-2020)

## Files

### Cleaned Data
- `cleaned_disease_data.parquet` - Cleaned time series data
  - Records: 16,066
  - Diseases: 44
  - Time period: 2012-2020

### Disease Statistics
- `disease_summary_statistics.csv` - Comprehensive disease metrics
  - Total cases, rankings, burden tiers
  - Summary statistics (mean, median, SD, CV)

### Category Mappings
- `disease_categories.json` - Disease taxonomy
  - Transmission categories: Vector-borne, Foodborne, Vaccine-preventable, Respiratory, Other
  - Burden tiers: High, Medium, Low

### Results
- `../tables/disease_summary_statistics.csv` - Statistical summary
- `../tables/final_quality_report.json` - Data quality metrics
- `../figures/` - Visualizations (PNG format)

## Data Quality

- Completeness: 100% (no missing values)
- Temporal coverage: 470 weeks across 9 years
- Standardization: 1 disease variants merged
- Outliers flagged: 3.0% of weeks (outbreak periods)

## Usage

```python
import polars as pl

# Load cleaned data
df = pl.read_parquet('data/3_interim/cleaned_disease_data.parquet')

# Load disease statistics
stats = pl.read_csv('data/4_processed/disease_summary_statistics.csv')
```

## Next Steps

1. **Problem Statement 002**: Disease Burden Prioritization
2. **Problem Statement 001**: Seasonal Outbreak Forecasting
3. **Problem Statement 003**: Workforce Capacity Planning
