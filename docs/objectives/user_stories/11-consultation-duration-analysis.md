# Story 11: Consultation Duration Analysis and Prediction

## Overview and Statement

Consultation duration variability impacts appointment scheduling accuracy and waiting times. This story analyzes factors influencing consultation length and builds a predictive model to estimate expected duration for each visit type.

**As a** Clinical Operations Manager  
**I want** to understand what factors drive longer consultation times  
**So that** I can allocate appropriate time slots for different visit types and patient profiles

### Acceptance Criteria
- [ ] Descriptive analysis of consultation_duration_minutes by:
  - Visit type (acute, chronic, preventive)
  - Patient age group and chronic condition count
  - Diagnosis complexity (number of diagnoses)
  - Procedures performed during visit
- [ ] Build regression model predicting consultation duration
- [ ] Features include:
  - visit_type, appointment_type
  - Patient demographics (age_group, chronic_conditions_count)
  - Historical average consultation time for patient
  - Number of diagnoses/procedures expected
- [ ] Model performance: MAE < 5 minutes, RMSE < 8 minutes
- [ ] Generate recommended consultation time allocations by visit type
- [ ] Identify outlier cases (unusually long consultations) for quality review

### Technical Notes
- Use XGBoost Regressor or Random Forest Regressor
- Handle right-skewed distribution of consultation times (log transformation or quantile regression)
- Join POLYCLINIC_ATTENDANCES with DIAGNOSIS_RECORDS and PROCEDURE_RECORDS
- Platform: Databricks with Python (scikit-learn, xgboost)
- Save model to `models/consultation_duration_predictor_v1.pkl`

### Estimated Effort
13-16 days

### Priority
Medium

## Dependencies
- POLYCLINIC_ATTENDANCES with consultation_duration_minutes
- DIAGNOSIS_RECORDS and PROCEDURE_RECORDS for complexity features
- PATIENT_DEMOGRAPHICS for patient characteristics
