# Comprehensive Data Catalog: Singapore Health Dataset

**Generated:** 30 January 2026  
**Dataset Source:** Kaggle - `subhamjain/health-dataset-complete-singapore`  
**Total Tables:** 35 CSV files  
**Total Files:** 70 (including metadata and reports)

---

## Executive Summary

This dataset contains comprehensive health data for Singapore covering various domains:
- **Healthcare Workforce**: Doctors, nurses, dentists, pharmacists, physiotherapists
- **Healthcare Facilities**: Hospitals, clinics, dental facilities, long-term care
- **Health Outcomes**: Mortality rates, disease indicators
- **Public Health**: Student health, vaccinations, nutrition surveys
- **Healthcare Spending**: Government expenditures
- **Healthcare Utilization**: Hospital admissions, care attendances

**Data Quality:** 100% completeness across all tables (no missing values)  
**Time Coverage:** Primarily 2003-2020  
**Format:** CSV files with standardized structures

---

## Table of Contents

1. [Healthcare Workforce Data](#healthcare-workforce-data)
2. [Healthcare Facilities Data](#healthcare-facilities-data)
3. [Health Outcomes & Mortality](#health-outcomes--mortality)
4. [Public Health & Prevention](#public-health--prevention)
5. [Healthcare Expenditure](#healthcare-expenditure)
6. [Healthcare Utilization](#healthcare-utilization)
7. [Nutrition Surveys](#nutrition-surveys)
8. [Quick Reference Tables](#quick-reference-tables)

---

## Healthcare Workforce Data

### 1. Doctors (number-of-doctors.csv)

**Purpose:** Track the number and distribution of doctors across sectors and specializations

**Dimensions:**
- **Time Range:** 2006-2019 (14 years)
- **Total Records:** 78
- **Granularity:** Year × Sector × Specialization

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 14 | 0% |
| sector | object | Employment sector | 3 (Public, Private, Not In Active Practice) | 0% |
| specialist_non-specialist | object | Specialization status | 3 (na, Specialist, Non-Specialist) | 0% |
| count | int64 | Number of doctors | 76 | 0% |

**Sample Data:**
```
year=2006, sector=Public, specialist_non-specialist=na, count=3505
year=2006, sector=Private, specialist_non-specialist=na, count=2966
year=2006, sector=Not In Active Practice, specialist_non-specialist=na, count=460
```

**Use Cases:**
- Healthcare workforce planning
- Public vs. private sector analysis
- Specialist capacity assessment
- Time-series trend analysis

---

### 2. Nurses & Midwives (number-of-nurses-and-midwives.csv)

**Purpose:** Monitor nursing workforce across sectors and roles

**Dimensions:**
- **Time Range:** 2008-2019 (12 years)
- **Total Records:** 126
- **Granularity:** Year × Type × Sector

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 12 | 0% |
| type | object | Healthcare role | 4 (Enrolled Nurses, etc.) | 0% |
| sector | object | Employment sector | 3 | 0% |
| count | int64 | Number of personnel | 119 | 0% |

**Unique Types:**
- Enrolled Nurses
- Staff Nurses
- Registered Midwives
- Midwives

**Use Cases:**
- Nursing workforce capacity planning
- Skill mix analysis
- Sector distribution analysis

---

### 3. Advanced Practice Nurses (number-of-advanced-practice-nurses.csv)

**Purpose:** Track specialized nursing workforce

**Dimensions:**
- **Time Range:** 2008-2019 (12 years)
- **Total Records:** 36
- **Granularity:** Year × Sector

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 12 | 0% |
| sector | object | Employment sector | 3 | 0% |
| count | int64 | Number of APNs | 22 | 0% |

**Sample Values:** 15, 2, 0 (shows concentration in public sector)

---

### 4. Dentists (number-of-dentists.csv)

**Purpose:** Monitor dental workforce by specialization and sector

**Dimensions:**
- **Time Range:** 2008-2019 (12 years)
- **Total Records:** 72
- **Granularity:** Year × Type × Sector

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 12 | 0% |
| type | object | Specialization | 2 (Dental Specialists, General) | 0% |
| sector | object | Employment sector | 3 | 0% |
| count | int64 | Number of dentists | 66 | 0% |

---

### 5. Oral Health Therapists (number-of-oral-health-therapists.csv)

**Purpose:** Track oral health support workforce

**Dimensions:**
- **Time Range:** 2008-2019 (12 years)
- **Total Records:** 36
- **Granularity:** Year × Sector

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 12 | 0% |
| sector | object | Employment sector | 3 | 0% |
| count | int64 | Number of therapists | 31 | 0% |

**Sample Data:** Public Sector=205, Private Sector=29, Not in Practice=9

---

### 6. Pharmacists (number-of-pharmacists.csv)

**Purpose:** Monitor pharmaceutical workforce distribution

**Dimensions:**
- **Time Range:** 2006-2019 (14 years)
- **Total Records:** 42
- **Granularity:** Year × Sector

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 14 | 0% |
| sector | object | Employment sector | 3 | 0% |
| count | int64 | Number of pharmacists | 40 | 0% |

**Sample Data:** Public=449, Private=832, Not Active=140 (2006)

---

### 7. Physiotherapists (number-of-physiotherapists.csv)

**Purpose:** Track physiotherapy workforce

**Dimensions:**
- **Time Range:** 2014-2019 (6 years)
- **Total Records:** 18
- **Granularity:** Year × Sector

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 6 | 0% |
| sector | object | Employment sector | 3 | 0% |
| count | int64 | Number of physiotherapists | 18 | 0% |

**Sample Data:** Public=861, Private=531, Not Active=2 (2014)

---

## Healthcare Facilities Data

### 8. Inpatient Facilities - Detailed (health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private.csv)

**Purpose:** Comprehensive tracking of hospital facilities and bed capacity by ownership type

**Dimensions:**
- **Time Range:** 2009-2020 (12 years)
- **Total Records:** 180
- **Granularity:** Year × Institution Type × Facility Type × Ownership

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 12 | 0% |
| institution_type | object | Type of institution | 2 (Hospital, Other) | 0% |
| facility_type_a | object | Facility classification | 5 (Acute, Psychiatric, etc.) | 0% |
| public_private | object | Ownership type | 3 (Public, Not-for-Profit, Private) | 0% |
| no_of_facilities | int64 | Number of facilities | 26 | 0% |
| no_beds | int64 | Total bed capacity | 102 | 0% |

**Facility Types:**
- Acute
- Psychiatric Hospitals
- Community Hospitals
- Specialty
- Nursing Homes

**Sample Data:**
```
2009: Public Acute=7 facilities, 6416 beds
2009: Not-for-Profit Acute=1 facility, 303 beds
2009: Private Acute=6 facilities, 1570 beds
```

---

### 9. Inpatient Facilities - Summary (health-facilities-and-beds-in-inpatient-facilities.csv)

**Purpose:** Simplified view of hospital facilities and beds

**Dimensions:**
- **Time Range:** 2009-2020 (12 years)
- **Total Records:** 60
- **Granularity:** Year × Institution Type × Facility Type

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 12 | 0% |
| institution_type | object | Type of institution | 2 | 0% |
| facility_type_a | object | Facility classification | 6 | 0% |
| no_of_facilities | int64 | Number of facilities | 22 | 0% |
| no_beds | int64 | Total bed capacity | 45 | 0% |

---

### 10. Primary Care, Dental & Pharmacy Facilities (health-facilities-primary-care-dental-clinics-and-pharmacies.csv)

**Purpose:** Track outpatient care facilities across public and private sectors

**Dimensions:**
- **Time Range:** 2009-2020 (12 years)
- **Total Records:** 96
- **Granularity:** Year × Institution Type × Sector × Facility Sub-Type

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 12 | 0% |
| institution_type | object | Type of institution | 3 | 0% |
| sector | object | Public or Private | 2 | 0% |
| facility_type_b | object | Specific facility type | 8 | 0% |
| no_of_facilities | int64 | Number of facilities | 59 | 0% |

**Institution Types:**
- Primary Care Facilities
- Dental Clinics
- Pharmacies

**Facility Sub-Types:**
- Polyclinics
- General Practitioner Clinics
- Polyclinic Dental Clinics
- Private Sector Dental Clinics
- Community Pharmacies
- Hospital Pharmacies
- And more...

**Sample Data:**
```
2009: Public Polyclinics=18
2009: Private GP Clinics=1628
2009: Public Polyclinic Dental Clinics=9
```

---

### 11. Dental Clinics & Pharmacies (health-facilities-dental-clinics-and-pharmacies.csv)

**Purpose:** Focused view of dental and pharmacy facilities

**Dimensions:**
- **Time Range:** 2009-2020 (12 years)
- **Total Records:** 72
- **Granularity:** Year × Institution Type × Sector

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 12 | 0% |
| institution_type | object | Type of institution | 2 (Dental Clinics, Pharmacies) | 0% |
| sector | object | Aggregation level | 3 (Total, Public, Private) | 0% |
| no_of_facilities | int64 | Number of facilities | 61 | 0% |

---

## Health Outcomes & Mortality

### 12-14. Age-Standardized Mortality Rates

**Three related tables:**
1. **age-standardised-mortality-rate-for-stroke.csv**
2. **age-standardised-mortality-rate-for-ischaemic-heart-disease.csv**
3. **age-standardised-mortality-rate-for-cancer.csv**

**Purpose:** Track mortality trends for major causes of death

**Common Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 30 | 0% |
| [disease] | float64 | Age-standardized rate per 100,000 | 29-30 | 0% |

**Dimensions:**
- **Time Range:** 1990-2019 (30 years)
- **Total Records:** 30 per table
- **Granularity:** Annual

**Sample Values (1990-1992):**
- **Stroke:** 95.8 → 95.5 → 83.7 (declining trend)
- **IHD:** 178.9 → 165.5 → 165.8
- **Cancer:** 244.5 → 241.0 → 240.8

**Use Cases:**
- Long-term mortality trend analysis
- Disease burden assessment
- Public health intervention evaluation
- International comparisons (age-standardized)

---

## Public Health & Prevention

### 15. Student Health - Defective Vision (common-health-problems-of-students-examined-defective-vision-annual.csv)

**Purpose:** Monitor vision problems in school-age children

**Dimensions:**
- **Time Range:** 2009-2020 (12 years)
- **Total Records:** 24
- **Granularity:** Year × Gender

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 12 | 0% |
| gender | object | Student gender | 2 (Male, Female) | 0% |
| per_10000_examined | int64 | Rate per 10,000 students examined | 24 | 0% |

**Use Cases:**
- Pediatric vision health trends
- Gender-based analysis
- School health program evaluation

---

### 16. Student Health - Obesity (common-health-problems-of-students-examined-obesity-annual.csv)

**Purpose:** Track childhood obesity rates

**Dimensions:**
- **Time Range:** 2009-2020 (12 years)
- **Total Records:** 48
- **Granularity:** Year × Age Group × Gender

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 12 | 0% |
| age_group | object | Student age group | 2 (Primary 1, Primary 5 equivalents) | 0% |
| gender | object | Student gender | 2 | 0% |
| per_10000_examined | int64 | Rate per 10,000 students | 48 | 0% |

**Age Groups:**
- Primary 1 and equivalent age groups
- Primary 5 and equivalent age groups

**Use Cases:**
- Childhood obesity surveillance
- Age-specific trend analysis
- Gender differences in obesity rates
- Public health intervention targeting

---

### 17. Student Health - Overweight (common-health-problems-of-students-examined-overweight-annual.csv)

**Purpose:** Monitor overweight prevalence in students

**Dimensions:**
- **Time Range:** 2009-2020 (12 years)
- **Total Records:** 48
- **Granularity:** Year × Age Group × Gender

**Schema:** (Same as obesity table)

**Sample Data (2009):**
```
Primary 1, Male: 1212 per 10,000
Primary 1, Female: 1080 per 10,000
Primary 5, Male: 1787 per 10,000
```

---

### 18. Dental Health Index (dental-index-dental-health-status-of-the-school-children-at-12-and-15-years-old.csv)

**Purpose:** Track dental health status of adolescents using DMFT index

**Dimensions:**
- **Time Range:** 2003-2020 (18 years)
- **Total Records:** 36
- **Granularity:** Year × Age Group

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 18 | 0% |
| age | object | Age group | 2 (12 YEARS OLD, 15 YEARS OLD) | 0% |
| dental_index | float64 | DMFT index score | 28 | 0% |

**About DMFT Index:**
- DMFT = Decayed, Missing, Filled Teeth
- Lower values indicate better dental health
- International standard for dental health measurement

**Sample Values:**
```
2003: 12 years old=0.74, 15 years old=1.14
2004: 12 years old=0.73
```

**Use Cases:**
- Dental health trend monitoring
- Evaluation of school dental programs
- Age-specific dental care needs assessment

---

### 19. Vaccinations - Students Annual (vaccination-and-immunisation-of-students-annual.csv)

**Purpose:** Track student vaccination coverage

**Dimensions:**
- **Time Range:** 2009-2019 (11 years)
- **Total Records:** 33
- **Granularity:** Year × Vaccination Type

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 11 | 0% |
| vaccination_type | object | Type of vaccine | 3 | 0% |
| no_of_doses_in_thousands | float64 | Number of doses (thousands) | 29 | 0% |

**Vaccination Types:**
1. Diphtheria tetanus
2. Poliomyelitis
3. Measles mumps rubella

**Sample Data (2009):**
```
Diphtheria tetanus: 48.7k doses
Poliomyelitis: 92.1k doses
Measles mumps rubella: 89.9k doses
```

**Use Cases:**
- Vaccination coverage monitoring
- Immunization program evaluation
- Compliance tracking

---

## Healthcare Expenditure

### 20. Government Health Expenditure (government-health-expenditure.csv)

**Purpose:** Track government spending on healthcare

**Dimensions:**
- **Time Range:** 2006-2018 (13 years, Financial Years)
- **Total Records:** 13
- **Granularity:** Annual (Financial Year)

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| financial_year | int64 | Financial year | 13 | 0% |
| operating_expenditure | int64 | Operating costs (million SGD) | 13 | 0% |
| development_expenditure | int64 | Capital/development costs (million SGD) | 13 | 0% |
| government_health_expenditure | float64 | Total expenditure (million SGD) | 13 | 0% |
| percentage_gdp | float64 | Percentage of GDP | 8 | 0% |

**Sample Data:**
```
FY2006: Operating=1840M, Development=96M, Total=2009.7M, GDP%=0.9%
FY2007: Operating=2019M, Development=185M, Total=2283.2M, GDP%=0.8%
FY2008: Operating=2379M, Development=336M, Total=2814.1M, GDP%=1.0%
```

**Expenditure Components:**
- **Operating:** Day-to-day healthcare operations
- **Development:** Infrastructure, equipment, new programs

**Use Cases:**
- Healthcare budget planning
- GDP allocation analysis
- Operating vs. capital expenditure trends
- Long-term spending pattern analysis

---

## Healthcare Utilization

### 21. Hospital Admission Rate by Sex (hospital-admission-rate-by-sex.csv)

**Purpose:** Monitor hospital utilization by gender

**Dimensions:**
- **Time Range:** 2009-2020 (12 years)
- **Total Records:** 72
- **Granularity:** Year × Facility Type × Sex

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 12 | 0% |
| facility_type_a | object | Type of hospital | 3 | 0% |
| sex | object | Gender | 2 (Male, Female) | 0% |
| rate | float64 | Admission rate per 1,000 population | 44 | 0% |

**Facility Types:**
1. Acute hospitals
2. Psychiatric Hospitals
3. Community Hospitals

**Sample Data (2009):**
```
Acute, Male: 90.2 per 1,000
Acute, Female: 96.4 per 1,000
Psychiatric, Male: 2.7 per 1,000
```

---

### 22. Hospital Admission Rate by Age and Sex (hospital-admission-rate-by-age-and-sex.csv)

**Purpose:** Detailed hospital utilization analysis by demographics

**Dimensions:**
- **Time Range:** 2009-2020 (12 years)
- **Total Records:** 216
- **Granularity:** Year × Facility Type × Sex × Age Group

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 12 | 0% |
| facility_type_a | object | Type of hospital | 3 | 0% |
| sex | object | Gender | 2 | 0% |
| age | object | Age group | 3 | 0% |
| rate | float64 | Admission rate per 1,000 | 125 | 0% |

**Age Groups:**
1. 0-14 Years
2. 15-64 years
3. 65 years & over

**Sample Data (2009, Acute, Male):**
```
0-14 Years: 100.1 per 1,000
15-64 years: 62.7 per 1,000
65 years & over: 323.0 per 1,000
```

**Key Insights:**
- Elderly (65+) have 3-5x higher admission rates
- Enables targeted capacity planning

---

### 23. Residential Long-Term Care Admissions (residential-long-term-care-admissions.csv)

**Purpose:** Track admissions to long-term residential care facilities

**Dimensions:**
- **Time Range:** 2007-2019 (13 years)
- **Total Records:** 25
- **Granularity:** Year × Type

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 13 | 0% |
| type | object | Facility type | 2 | 0% |
| count | int64 | Number of admissions | 25 | 0% |

**Facility Types:**
1. Inpatient Hospices
2. Nursing Homes

**Sample Data:**
```
2007: Inpatient Hospices=1168, Nursing Homes=3941
2008: Inpatient Hospices=1102
```

---

### 24. Centre-Based Care Services Attendances (centre-based-care-services-attendances.csv)

**Purpose:** Monitor day care and community rehabilitation service usage

**Dimensions:**
- **Time Range:** 2006-2019 (14 years)
- **Total Records:** 56
- **Granularity:** Year × Type

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Year of record | 14 | 0% |
| type | object | Service type | 4 | 0% |
| count | int64 | Number of attendances | 39 | 0% |

**Service Types:**
1. Dementia Day Care
2. Day Care/Community Rehabilitation
3. Day Care
4. (Others)

**Sample Data (2006):**
```
Dementia Day Care: 35,276 attendances
Day Care/Community Rehabilitation: 208,255 attendances
```

---

## Nutrition Surveys

### 25. Carbohydrate Intake by Gender (national-nutrition-survey-carbohydrate-intake-by-gender.csv)

**Purpose:** National nutrition baseline data by gender

**Dimensions:**
- **Survey Years:** 2004, 2010
- **Total Records:** 6
- **Granularity:** Year × Gender

**Schema:**
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| year | int64 | Survey year | 2 | 0% |
| gender | object | Gender category | 3 (Overall, Male, Female) | 0% |
| mean | float64 | Mean intake (grams/day) | 6 | 0% |
| standard_error_of_mean | float64 | SEM | 5 | 0% |
| 5th_percentile | float64 | 5th percentile value | 6 | 0% |
| 10th_percentile | float64 | 10th percentile value | 6 | 0% |
| 25th_percentile | float64 | 25th percentile value | 6 | 0% |
| 50th_percentile | float64 | Median | 6 | 0% |
| 75th_percentile | float64 | 75th percentile value | 6 | 0% |
| 90th_percentile | float64 | 90th percentile value | 6 | 0% |
| 95th_percentile | float64 | 95th percentile value | 6 | 0% |

**Sample Data (2004):**
```
Overall: Mean=336.7g, Median=318.6g
Male: Mean=378.5g, Median=351.8g
Female: Mean=295.6g, Median=283.3g
```

---

### 26. Carbohydrate Intake by Gender and Race (national-nutrition-survey-carbohydrate-intake-by-gender-and-race.csv)

**Purpose:** Nutrition data segmented by gender and ethnicity

**Dimensions:**
- **Survey Years:** 2004, 2010
- **Total Records:** 18
- **Granularity:** Year × Gender × Race

**Schema:** Same as above plus:
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| race | object | Ethnic group | 3 (Chinese, Malay, Indian) | 0% |

**Sample Data (2004, Overall):**
```
Chinese: Mean=331.9g
Malay: Mean=356.4g
Indian: Mean=352.9g
```

---

### 27. Carbohydrate Intake by Gender and Age Group (national-nutrition-survey-carbohydrate-intake-by-gender-and-age-group.csv)

**Purpose:** Nutrition data across age demographics

**Dimensions:**
- **Survey Years:** 2004, 2010
- **Total Records:** 30
- **Granularity:** Year × Gender × Age Group

**Schema:** Same as gender table plus:
| Column | Type | Description | Unique Values | Nulls |
|--------|------|-------------|---------------|-------|
| age_group | object | Age category | 5 | 0% |

**Age Groups:**
1. 18 to 29 Years Old
2. 30 to 39 Years Old
3. 40 to 49 Years Old
4. 50 to 59 Years Old
5. 60 to 69 Years Old

**Sample Data (2004, Overall):**
```
18-29: Mean=369.9g
30-39: Mean=346.3g
40-49: Mean=329.7g
```

**Key Features:**
- Full distribution statistics (percentiles)
- Standard errors for statistical testing
- Adult population focus (18-69 years)

---

## Quick Reference Tables

### Table Size Summary

| Table Name | Records | Columns | Time Span | Update Frequency |
|------------|---------|---------|-----------|------------------|
| Doctors | 78 | 4 | 2006-2019 | Annual |
| Nurses & Midwives | 126 | 4 | 2008-2019 | Annual |
| Hospital Admissions (detailed) | 216 | 5 | 2009-2020 | Annual |
| Inpatient Facilities (detailed) | 180 | 6 | 2009-2020 | Annual |
| Primary Care Facilities | 96 | 5 | 2009-2020 | Annual |
| Mortality Rates (each) | 30 | 2 | 1990-2019 | Annual |
| Government Expenditure | 13 | 5 | 2006-2018 | Annual |
| Nutrition Survey (by age/gender) | 30 | 12 | 2004, 2010 | Survey-based |
| Student Health (each) | 24-48 | 3-4 | 2009-2020 | Annual |

### Common Dimensions Across Tables

**Time Dimensions:**
- `year` (int64) - Most common, annual granularity
- `financial_year` (int64) - For expenditure data

**Geographic/Sectoral:**
- `sector` (object) - Public Sector, Private Sector, Not in Active Practice
- `public_private` (object) - Public, Not-for-Profit, Private

**Demographic:**
- `gender` / `sex` (object) - Male, Female
- `age` / `age_group` (object) - Various age bands
- `race` (object) - Chinese, Malay, Indian

**Healthcare-Specific:**
- `institution_type` (object) - Hospital, Primary Care, etc.
- `facility_type_a` (object) - Acute, Psychiatric, Community
- `type` - Various classifications

### Data Quality Indicators

**Completeness:** 100% across all tables  
**Consistency:** Standardized column naming conventions  
**Timeliness:** Most recent data from 2019-2020  
**Granularity:** Primarily annual, with demographic breakdowns

---

## Metadata Files

The dataset includes `.txt` metadata files for most tables:
- Data definitions
- Data collection methodology
- Data quality notes
- Update schedules
- Contact information

**Location:** Same directory as corresponding CSV files  
**Naming:** `metadata-[table-name].txt`

---

## Additional Resources

**PDF Report:**
- `national-nutrition-survey-2010-report.pdf` - Comprehensive nutrition survey documentation

---

## Data Access Patterns for Automation

### Loading Individual Tables

```python
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Download full dataset
dataset_path = kagglehub.dataset_download("subhamjain/health-dataset-complete-singapore")

# Load specific CSV
import pandas as pd
df = pd.read_csv(f"{dataset_path}/[subfolder]/[filename].csv")
```

### Batch Loading All Tables

```python
import os
import pandas as pd

dataset_path = kagglehub.dataset_download("subhamjain/health-dataset-complete-singapore")

# Get all CSV files
csv_files = []
for root, dirs, files in os.walk(dataset_path):
    for file in files:
        if file.endswith('.csv'):
            csv_files.append(os.path.join(root, file))

# Load all into dictionary
data_tables = {}
for csv_file in csv_files:
    table_name = os.path.basename(csv_file).replace('.csv', '')
    data_tables[table_name] = pd.read_csv(csv_file)
```

---

## Contact & Support

**Dataset Owner:** subhamjain (Kaggle)  
**Source:** Ministry of Health, Singapore (via data.gov.sg)  
**License:** Check Kaggle dataset page for current license  
**Documentation Generated:** 30 January 2026

---

**Document Version:** 1.0  
**Last Updated:** 30 January 2026
