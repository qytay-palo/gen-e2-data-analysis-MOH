# Data Table Quick Reference & Mapping Guide

**Purpose:** Quick lookup reference for data analysts to find and use specific tables  
**Version:** 1.0  
**Last Updated:** 30 January 2026

---

## Table Index by Category

### Healthcare Workforce (7 tables)

| # | Table File Name | Short Name | Years | Records | Key Dimensions |
|---|----------------|------------|-------|---------|----------------|
| 1 | `number-of-doctors.csv` | doctors | 2006-2019 | 78 | year, sector, specialist_status |
| 2 | `number-of-nurses-and-midwives.csv` | nurses | 2008-2019 | 126 | year, type, sector |
| 3 | `number-of-advanced-practice-nurses.csv` | apn | 2008-2019 | 36 | year, sector |
| 4 | `number-of-dentists.csv` | dentists | 2008-2019 | 72 | year, type, sector |
| 5 | `number-of-oral-health-therapists.csv` | oral_therapists | 2008-2019 | 36 | year, sector |
| 6 | `number-of-pharmacists.csv` | pharmacists | 2006-2019 | 42 | year, sector |
| 7 | `number-of-physiotherapists.csv` | physiotherapists | 2014-2019 | 18 | year, sector |

### Healthcare Facilities (4 tables)

| # | Table File Name | Short Name | Years | Records | Key Dimensions |
|---|----------------|------------|-------|---------|----------------|
| 8 | `health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private.csv` | facilities_detailed | 2009-2020 | 180 | year, institution_type, facility_type, ownership |
| 9 | `health-facilities-and-beds-in-inpatient-facilities.csv` | facilities_summary | 2009-2020 | 60 | year, institution_type, facility_type |
| 10 | `health-facilities-primary-care-dental-clinics-and-pharmacies.csv` | primary_care_facilities | 2009-2020 | 96 | year, institution_type, sector, facility_subtype |
| 11 | `health-facilities-dental-clinics-and-pharmacies.csv` | dental_pharmacy_facilities | 2009-2020 | 72 | year, institution_type, sector |

### Health Outcomes & Mortality (3 tables)

| # | Table File Name | Short Name | Years | Records | Metric |
|---|----------------|------------|-------|---------|--------|
| 12 | `age-standardised-mortality-rate-for-stroke.csv` | mortality_stroke | 1990-2019 | 30 | age_std_rate per 100k |
| 13 | `age-standardised-mortality-rate-for-ischaemic-heart-disease.csv` | mortality_ihd | 1990-2019 | 30 | age_std_rate per 100k |
| 14 | `age-standardised-mortality-rate-for-cancer.csv` | mortality_cancer | 1990-2019 | 30 | age_std_rate per 100k |

### Public Health & Prevention (6 tables)

| # | Table File Name | Short Name | Years | Records | Key Dimensions |
|---|----------------|------------|-------|---------|----------------|
| 15 | `common-health-problems-of-students-examined-defective-vision-annual.csv` | student_vision | 2009-2020 | 24 | year, gender |
| 16 | `common-health-problems-of-students-examined-obesity-annual.csv` | student_obesity | 2009-2020 | 48 | year, age_group, gender |
| 17 | `common-health-problems-of-students-examined-overweight-annual.csv` | student_overweight | 2009-2020 | 48 | year, age_group, gender |
| 18 | `dental-index-dental-health-status-of-the-school-children-at-12-and-15-years-old.csv` | dental_health_index | 2003-2020 | 36 | year, age |
| 19 | `vaccination-and-immunisation-of-students-annual.csv` | vaccinations | 2009-2019 | 33 | year, vaccination_type |

### Healthcare Utilization (3 tables)

| # | Table File Name | Short Name | Years | Records | Key Dimensions |
|---|----------------|------------|-------|---------|----------------|
| 20 | `hospital-admission-rate-by-sex.csv` | admissions_by_sex | 2009-2020 | 72 | year, facility_type, sex |
| 21 | `hospital-admission-rate-by-age-and-sex.csv` | admissions_detailed | 2009-2020 | 216 | year, facility_type, sex, age_group |
| 22 | `residential-long-term-care-admissions.csv` | ltc_admissions | 2007-2019 | 25 | year, type |
| 23 | `centre-based-care-services-attendances.csv` | day_care_attendances | 2006-2019 | 56 | year, type |

### Healthcare Expenditure (1 table)

| # | Table File Name | Short Name | Years | Records | Key Dimensions |
|---|----------------|------------|-------|---------|----------------|
| 24 | `government-health-expenditure.csv` | expenditure | 2006-2018 | 13 | financial_year |

### Nutrition (3 tables)

| # | Table File Name | Short Name | Years | Records | Key Dimensions |
|---|----------------|------------|-------|---------|----------------|
| 25 | `national-nutrition-survey-carbohydrate-intake-by-gender.csv` | nutrition_by_gender | 2004, 2010 | 6 | year, gender |
| 26 | `national-nutrition-survey-carbohydrate-intake-by-gender-and-race.csv` | nutrition_by_race | 2004, 2010 | 18 | year, gender, race |
| 27 | `national-nutrition-survey-carbohydrate-intake-by-gender-and-age-group.csv` | nutrition_by_age | 2004, 2010 | 30 | year, gender, age_group |

---

## Column Standardization Map

### Standard Column Names Across Tables

| Original Column | Standardized Name | Type | Description |
|----------------|-------------------|------|-------------|
| year | year | int64 | Calendar year |
| financial_year | financial_year | int64 | Fiscal year (starts April 1) |
| sector | sector | object | Public Sector, Private Sector, Not in Active Practice |
| public_private | ownership_type | object | Public, Not-for-Profit, Private |
| sex / gender | gender | object | Male, Female |
| age / age_group | age_group | object | Various age bands |
| race | race | object | Chinese, Malay, Indian |
| type | type | object | Context-dependent classification |
| count | count | int64 | Number of entities |
| no_of_facilities | facility_count | int64 | Number of facilities |
| no_beds | bed_count | int64 | Number of beds |
| rate | rate | float64 | Rate per 1,000 or 10,000 population |
| per_10000_examined | rate_per_10k | int64 | Rate per 10,000 examined |

---

## Common Analysis Queries

### Query 1: Healthcare Workforce Trends

**Tables:** doctors, nurses, pharmacists, dentists  
**Time Range:** 2008-2019 (common overlap)

```python
# Load workforce tables
doctors = pd.read_csv('number-of-doctors.csv')
nurses = pd.read_csv('number-of-nurses-and-midwives.csv')
pharmacists = pd.read_csv('number-of-pharmacists.csv')

# Filter to public sector and aggregate
workforce_trend = pd.concat([
    doctors[doctors['sector'] == 'Public'].groupby('year')['count'].sum().rename('doctors'),
    nurses[nurses['sector'] == 'Public Sector'].groupby('year')['count'].sum().rename('nurses'),
    pharmacists[pharmacists['sector'] == 'Public Sector'].groupby('year')['count'].sum().rename('pharmacists')
], axis=1)
```

### Query 2: Hospital Capacity Analysis

**Tables:** facilities_detailed  
**Metrics:** facility_count, bed_count by facility_type and ownership

```python
facilities = pd.read_csv('health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private.csv')

# Latest year capacity by ownership type
latest_year = facilities['year'].max()
capacity = facilities[facilities['year'] == latest_year].groupby(['facility_type_a', 'public_private']).agg({
    'no_of_facilities': 'sum',
    'no_beds': 'sum'
}).reset_index()
```

### Query 3: Disease Burden Trends

**Tables:** mortality_stroke, mortality_ihd, mortality_cancer  
**Time Range:** 1990-2019

```python
# Load mortality tables
stroke = pd.read_csv('age-standardised-mortality-rate-for-stroke.csv')
ihd = pd.read_csv('age-standardised-mortality-rate-for-ischaemic-heart-disease.csv')
cancer = pd.read_csv('age-standardised-mortality-rate-for-cancer.csv')

# Combine for comparison
mortality_trends = stroke.merge(ihd, on='year').merge(cancer, on='year')
mortality_trends.columns = ['year', 'stroke', 'ihd', 'cancer']
```

### Query 4: Healthcare Utilization by Demographics

**Table:** admissions_detailed  
**Dimensions:** facility_type, sex, age_group

```python
admissions = pd.read_csv('hospital-admission-rate-by-age-and-sex.csv')

# Acute hospital admissions by age group (latest year)
acute_admissions = admissions[
    (admissions['facility_type_a'] == 'Acute') &
    (admissions['year'] == admissions['year'].max())
].pivot_table(
    values='rate',
    index='age',
    columns='sex',
    aggfunc='mean'
)
```

### Query 5: Public Health Program Evaluation

**Tables:** student_obesity, student_overweight, student_vision  
**Focus:** Childhood health trends

```python
# Load student health tables
obesity = pd.read_csv('common-health-problems-of-students-examined-obesity-annual.csv')
overweight = pd.read_csv('common-health-problems-of-students-examined-overweight-annual.csv')
vision = pd.read_csv('common-health-problems-of-students-examined-defective-vision-annual.csv')

# Trend analysis for Primary 1 students
p1_obesity = obesity[obesity['age_group'].str.contains('Primary 1')].groupby('year')['per_10000_examined'].mean()
p1_vision = vision.groupby('year')['per_10000_examined'].mean()
```

### Query 6: Healthcare Spending vs. Outcomes

**Tables:** expenditure, mortality_cancer (or other outcomes)  
**Analysis:** Correlation between spending and health outcomes

```python
expenditure = pd.read_csv('government-health-expenditure.csv')
cancer = pd.read_csv('age-standardised-mortality-rate-for-cancer.csv')

# Align years and merge
# Note: expenditure uses financial_year, cancer uses year
spending_outcomes = expenditure.merge(
    cancer,
    left_on='financial_year',
    right_on='year',
    how='inner'
)
```

---

## Data Relationships & Joins

### Common Join Keys

```
Primary Keys:
  - year (for time-series analysis)
  - year + sector (for workforce tables)
  - year + facility_type (for utilization tables)
  - year + gender + age_group (for demographic tables)

Foreign Key Relationships:
  facilities_detailed.year → expenditure.financial_year
  doctors.year → admissions_detailed.year
  nurses.year → facilities_summary.year
```

### Example Multi-Table Join

```python
# Comprehensive healthcare system analysis
doctors_by_year = doctors.groupby('year')['count'].sum().rename('total_doctors')
beds_by_year = facilities_detailed.groupby('year')['no_beds'].sum().rename('total_beds')
admissions_by_year = admissions_detailed.groupby('year')['rate'].mean().rename('avg_admission_rate')

healthcare_system = pd.concat([
    doctors_by_year,
    beds_by_year,
    admissions_by_year
], axis=1).reset_index()
```

---

## Data Extraction Code Templates

### Template 1: Single Table Load

```python
import kagglehub
import pandas as pd

def load_table(filename: str, subdir: str = None) -> pd.DataFrame:
    """
    Load a single table from Kaggle dataset.
    
    Args:
        filename: CSV filename (e.g., 'number-of-doctors.csv')
        subdir: Subdirectory name (auto-detected if None)
    
    Returns:
        DataFrame with the table data
    """
    dataset_path = kagglehub.dataset_download(
        "subhamjain/health-dataset-complete-singapore"
    )
    
    # If subdir not provided, find it
    if subdir is None:
        import os
        for root, dirs, files in os.walk(dataset_path):
            if filename in files:
                file_path = os.path.join(root, filename)
                break
    else:
        file_path = f"{dataset_path}/{subdir}/{filename}"
    
    return pd.read_csv(file_path)

# Usage
doctors = load_table('number-of-doctors.csv')
```

### Template 2: Multi-Table Load by Category

```python
# Define table groups
WORKFORCE_TABLES = [
    'number-of-doctors.csv',
    'number-of-nurses-and-midwives.csv',
    'number-of-pharmacists.csv',
    'number-of-dentists.csv',
    'number-of-physiotherapists.csv'
]

FACILITY_TABLES = [
    'health-facilities-and-beds-in-inpatient-facilities.csv',
    'health-facilities-primary-care-dental-clinics-and-pharmacies.csv'
]

MORTALITY_TABLES = [
    'age-standardised-mortality-rate-for-stroke.csv',
    'age-standardised-mortality-rate-for-ischaemic-heart-disease.csv',
    'age-standardised-mortality-rate-for-cancer.csv'
]

def load_table_group(table_list: list) -> dict:
    """Load multiple tables and return as dictionary."""
    tables = {}
    for filename in table_list:
        table_name = filename.replace('.csv', '').replace('-', '_')
        tables[table_name] = load_table(filename)
        print(f"Loaded {table_name}: {len(tables[table_name])} records")
    return tables

# Usage
workforce_data = load_table_group(WORKFORCE_TABLES)
mortality_data = load_table_group(MORTALITY_TABLES)
```

### Template 3: Load with Data Quality Check

```python
def load_with_validation(filename: str) -> pd.DataFrame:
    """Load table and perform basic validation."""
    df = load_table(filename)
    
    # Check for empty dataframe
    assert not df.empty, f"{filename} is empty"
    
    # Check for null values
    null_cols = df.columns[df.isnull().any()].tolist()
    if null_cols:
        print(f"Warning: {filename} has nulls in: {null_cols}")
    
    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"Warning: {filename} has {duplicates} duplicate rows")
    
    # Add audit columns
    df['_loaded_at'] = pd.Timestamp.now()
    df['_source_file'] = filename
    
    return df
```

---

## Dimension Value Reference

### Sectors
```
Public / Public Sector
Private / Private Sector
Not in Active Practice / Not In Active Practice
```

### Facility Types
```
Acute (hospitals)
Psychiatric Hospitals
Community Hospitals
Specialty
Inpatient Hospices
Nursing Homes
Primary Care Facilities
Dental Clinics
Pharmacies
```

### Age Groups (varies by table)
```
Student Health:
  - Primary 1 and equivalent age groups
  - Primary 5 and equivalent age groups
  - 12 YEARS OLD
  - 15 YEARS OLD

Hospital Admissions:
  - 0-14 Years
  - 15-64 years
  - 65 years & over

Nutrition Survey:
  - 18 to 29 Years Old
  - 30 to 39 Years Old
  - 40 to 49 Years Old
  - 50 to 59 Years Old
  - 60 to 69 Years Old
```

### Races
```
Chinese
Malay
Indian
```

### Vaccination Types
```
Diphtheria tetanus
Poliomyelitis
Measles mumps rubella
```

---

## File Size & Performance Notes

### Small Tables (< 1KB, instant load)
- mortality tables (30 records each)
- expenditure (13 records)
- nutrition surveys (6-30 records)

### Medium Tables (1-50KB, < 1 second)
- Most workforce tables (18-126 records)
- Student health tables (24-48 records)
- Facility tables (60-96 records)

### Large Tables (> 50KB, < 2 seconds)
- admissions_detailed (216 records)
- facilities_detailed (180 records)

**Note:** All tables load very quickly. No special optimization needed.

---

## Tips for Data Analysts

### 1. Start with These Core Tables
- `number-of-doctors.csv` - Healthcare workforce baseline
- `government-health-expenditure.csv` - Financial context
- `hospital-admission-rate-by-age-and-sex.csv` - Utilization patterns
- `age-standardised-mortality-rate-for-*.csv` - Health outcomes

### 2. Common Pitfalls
- **Year alignment:** Expenditure uses `financial_year`, others use `year`
- **Sector naming:** Inconsistent capitalization/spacing across tables
- **Missing years:** Not all tables cover same time periods
- **Different rates:** Some per 1,000, others per 10,000

### 3. Data Enrichment Opportunities
- Add population data for per-capita calculations
- Add GDP data for healthcare spending ratios
- Add international benchmarks for comparisons

### 4. Recommended Visualizations
- Time series: Line charts for trends
- Comparisons: Grouped bar charts for sector/facility comparisons
- Demographics: Heatmaps for age/gender patterns
- Correlations: Scatter plots for spending vs outcomes

---

## Quick Load Script

Save as `quick_load.py` for rapid analysis:

```python
import kagglehub
import pandas as pd
from pathlib import Path

# Download dataset once
DATASET_PATH = kagglehub.dataset_download(
    "subhamjain/health-dataset-complete-singapore"
)

# Quick load functions
def load_doctors(): return pd.read_csv(Path(DATASET_PATH) / 'number-of-doctors/number-of-doctors.csv')
def load_nurses(): return pd.read_csv(Path(DATASET_PATH) / 'number-of-nurses-and-midwives/number-of-nurses-and-midwives.csv')
def load_expenditure(): return pd.read_csv(Path(DATASET_PATH) / 'government-health-expenditure/government-health-expenditure.csv')
def load_admissions(): return pd.read_csv(Path(DATASET_PATH) / 'hospital-admission-rate-by-age-and-sex/hospital-admission-rate-by-age-and-sex.csv')
def load_mortality_cancer(): return pd.read_csv(Path(DATASET_PATH) / 'age-standardised-mortality-rate-for-cancer/age-standardised-mortality-rate-for-cancer.csv')

# Usage
if __name__ == "__main__":
    doctors = load_doctors()
    print(f"Doctors data: {len(doctors)} records, {doctors['year'].min()}-{doctors['year'].max()}")
```

---

**Document Version:** 1.0  
**Last Updated:** 30 January 2026  
**For questions:** Contact Data Analytics Team
