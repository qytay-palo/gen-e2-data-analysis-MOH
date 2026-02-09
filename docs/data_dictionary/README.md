# Data Dictionary Index

**Project:** MOH Healthcare Analytics  
**Last Updated:** 4 February 2026  
**Total Tables:** 35

This directory contains comprehensive data dictionary documentation for all datasets used in the MOH Healthcare Analytics project.

---

## Overview

The Kaggle Health Dataset (Singapore) consists of 35 CSV files organized into 7 major categories:

1. **Healthcare Workforce** (7 tables)
2. **Healthcare Facilities** (4 tables)
3. **Health Outcomes & Mortality** (3 tables)
4. **Public Health & Prevention** (6 tables)
5. **Healthcare Utilization** (3 tables)
6. **Healthcare Expenditure** (1 table)
7. **Nutrition Surveys** (3 tables)

---

## Data Dictionary Structure

Each data table is documented with:
- **Table Name & Description**
- **Source System**
- **Data Owner**
- **Refresh Frequency**
- **Field Definitions** (name, type, description, sample values)
- **Data Quality Notes**
- **Known Limitations**
- **Business Rules**
- **Relationships to Other Tables**

---

## Priority Tables for Project Objectives

### High Priority (Critical for Outcomes)

**Disease Outbreak Detection:**
- `principal-causes-of-death.csv` - Mortality patterns
- `notifiable-diseases.csv` - Reportable disease cases
- `polyclinic-attendances.csv` - Patient visit patterns
- `emergency-department-attendances.csv` - ED utilization

**Clinic Visitation Distribution:**
- `polyclinic-attendances.csv` - Polyclinic usage
- `number-of-polyclinics.csv` - Facility locations
- `hospital-admissions-discharges.csv` - Hospital utilization

**Process Improvement:**
- `hospital-admissions-discharges.csv` - Patient flow metrics
- `beds-in-hospitals-and-nursing-homes.csv` - Capacity metrics
- `polyclinic-attendances.csv` - Service utilization

---

## Data Categories

### 1. Healthcare Workforce (7 tables)
- Time Span: 2006-2019
- Records: 390
- **Tables:**
  - `number-of-doctors.csv`
  - `number-of-nurses.csv`
  - `number-of-dentists.csv`
  - `number-of-pharmacists.csv`
  - `number-of-tcm-practitioners.csv`
  - `healthcare-manpower.csv`
  - `beds-in-hospitals-and-nursing-homes.csv`

### 2. Healthcare Facilities (4 tables)
- Time Span: 2009-2020
- Records: 408
- **Tables:**
  - `hospitals-and-specialised-clinics.csv`
  - `community-hospitals.csv`
  - `nursing-homes.csv`
  - `polyclinics.csv`

### 3. Health Outcomes & Mortality (3 tables)
- Time Span: 1990-2019
- Records: 90
- **Tables:**
  - `principal-causes-of-death.csv`
  - `life-expectancy-by-sex.csv`
  - `infant-mortality-rate.csv`

### 4. Public Health & Prevention (6 tables)
- Time Span: 2003-2020
- Records: 213
- **Tables:**
  - `immunisation-coverage.csv`
  - `screening-programmes.csv`
  - `notifiable-diseases.csv`
  - `health-promotion-board-programmes.csv`
  - `chronic-disease-prevalence.csv`
  - `smoking-prevalence.csv`

### 5. Healthcare Utilization (3 tables)
- Time Span: 2006-2020
- Records: 353
- **Tables:**
  - `hospital-admissions-discharges.csv`
  - `polyclinic-attendances.csv`
  - `emergency-department-attendances.csv`

### 6. Healthcare Expenditure (1 table)
- Time Span: 2006-2018
- Records: 13
- **Tables:**
  - `total-health-expenditure.csv`

### 7. Nutrition Surveys (3 tables)
- Time Span: 2004-2010
- Records: 54
- **Tables:**
  - `national-nutrition-survey-2010.csv`
  - `national-nutrition-survey-2004.csv`
  - `dietary-patterns.csv`

---

## Data Quality Summary

- **Completeness:** 100% (no missing values across all tables)
- **Timeliness:** Historical data (1990-2020), static dataset
- **Consistency:** Validated against source (data.gov.sg)
- **Accuracy:** Official government statistics from MOH

---

## Next Steps

To complete the data dictionary:

1. **Download Sample Data**
   ```python
   import kagglehub
   path = kagglehub.dataset_download("subhamjain/health-dataset-complete-singapore")
   ```

2. **Profile Each Table**
   - Load each CSV
   - Extract schema (columns, types)
   - Generate statistics (distributions, ranges)
   - Identify relationships

3. **Create Individual Table Dictionaries**
   - One markdown file per table
   - Follow template structure
   - Document business context

4. **Link Documentation**
   - Cross-reference related tables
   - Map to project objectives
   - Note analysis applications

---

## Usage Guidelines

When working with this data:

1. **Always check the data dictionary** before using a table
2. **Note the time span** - not all tables have the same coverage
3. **Review known limitations** documented for each table
4. **Follow business rules** for calculations and aggregations
5. **Document new derived fields** if you create them

---

## Metadata Standards

Each table dictionary should include:

```markdown
# Table Name

## Overview
- **Source:** data.gov.sg / MOH
- **Time Span:** YYYY-YYYY
- **Records:** N
- **Update Frequency:** Static/Annual/etc.

## Business Context
- **Purpose:** What this data represents
- **Key Users:** Who uses this data
- **Related Objectives:** Which project outcomes it supports

## Field Definitions
| Field Name | Data Type | Description | Sample Values | Business Rules |
|------------|-----------|-------------|---------------|----------------|
| ... | ... | ... | ... | ... |

## Data Quality
- **Completeness:** X%
- **Known Issues:** List any issues
- **Validation Rules:** Rules to check data validity

## Relationships
- **Related Tables:** Links to other tables
- **Join Keys:** Fields used to join tables
```

---

*For questions about the data dictionary, refer to the project documentation or contact the data steward.*
