# E01-S01: Extract and Profile Facility Utilization Data

**Story ID**: E01-S01  
**Epic**: EPIC-001 - Healthcare Facility Utilization & Bottleneck Analysis

## Parent Epic
Healthcare Facility Utilization & Bottleneck Analysis - Profile facility utilization patterns and identify operational bottlenecks across Singapore's healthcare network.

## Overview and Statement

Extract healthcare utilization and capacity data from the Kaggle MOH dataset and perform initial profiling to understand data structure, quality, and coverage.

**As a** data analyst  
**I want** to extract facility utilization data and perform comprehensive data profiling  
**So that** I understand data quality, coverage, and can establish baseline metrics for all healthcare facilities

### Acceptance Criteria
- [ ] Extract utilization tables from Kaggle dataset (admission-and-outpatient-attendances, hospital-beds, facilities registry)
- [ ] Load data into analysis environment (pandas/Spark DataFrames)
- [ ] Generate data quality report (completeness, missing values, outliers, date ranges)
- [ ] Calculate basic statistics (row counts, unique facilities, date coverage 2006-2020)
- [ ] Document data quality issues and assumptions
- [ ] Create facility inventory list with coverage status

### Technical Notes
- Use `kagglehub` to load dataset
- Primary tables: admission-and-outpatient-attendances, number-of-hospital-beds
- Expect annual aggregated data (2006-2020)
- Document any gaps in facility coverage or time periods

### Estimated Effort
2-3 days

### Priority
**HIGH** - Foundation for all subsequent analysis

## Dependencies
- Kaggle MOH dataset loaded and accessible
- Python environment with pandas, numpy configured
