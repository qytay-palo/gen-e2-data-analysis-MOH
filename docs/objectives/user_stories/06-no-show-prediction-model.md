# Story 06: Patient No-Show Prediction Model

## Overview and Statement

Patient no-shows reduce clinic utilization and waste resources. This story builds a machine learning classifier to predict which appointments are at high risk of no-shows, enabling proactive interventions or overbooking strategies.

**As a** Appointment Scheduler  
**I want** to identify patients at high risk of not showing up for their appointment  
**So that** I can send targeted reminders or optimize overbooking to maintain clinic utilization

### Acceptance Criteria
- [ ] Build binary classification model (show=0, no-show=1) using historical appointment data
- [ ] Features include:
  - Patient characteristics (age_group, chronic_conditions_count)
  - Appointment characteristics (appointment_type, day_of_week, lead time)
  - Historical no-show rate for the patient
  - Weather conditions (optional, if available)
- [ ] Train multiple algorithms (Logistic Regression, XGBoost, Random Forest)
- [ ] Model performance:
  - AUC-ROC > 0.75
  - F1-score > 0.70
  - Precision-Recall curve analysis
- [ ] Generate risk scores (0-1 probability) for each scheduled appointment
- [ ] Feature importance analysis to understand no-show drivers
- [ ] Production-ready prediction pipeline for daily scoring

### Technical Notes
- Use XGBoost or LightGBM for best performance on tabular data
- Handle class imbalance (no-shows typically 10-20%) using SMOTE or class weights
- Cross-validation: 5-fold stratified CV
- Save model to `models/no_show_classifier_v1.pkl`
- Platform: Databricks with Python (scikit-learn, xgboost)
- Retrain monthly to capture evolving patterns

### Estimated Effort
18-22 days

### Priority
High

## Dependencies
- [Story 02: Baseline Metrics Calculation](#02-baseline-metrics-calculation.md) - Understand current no-show rates
- POLYCLINIC_ATTENDANCES table with visit_status='no-show' labels
- PATIENT_DEMOGRAPHICS for patient features
