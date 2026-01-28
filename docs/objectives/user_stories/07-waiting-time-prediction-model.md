# Story 07: Real-Time Waiting Time Prediction Model

## Overview and Statement

Providing accurate waiting time estimates improves patient experience and sets realistic expectations. This story builds a regression model to predict expected waiting times based on current queue state and patient characteristics.

**As a** Patient  
**I want** to see an estimated waiting time when I arrive at the polyclinic  
**So that** I can plan my day accordingly and have realistic expectations

### Acceptance Criteria
- [ ] Build regression model predicting waiting_time_minutes
- [ ] Features include:
  - Current queue length (number of patients waiting)
  - Time of day, day of week
  - Patient visit_type (acute vs chronic)
  - Historical average waiting time for polyclinic
  - Current staff availability (if data available)
- [ ] Train multiple regression algorithms (Linear Regression, XGBoost Regression, Neural Network)
- [ ] Model performance:
  - MAE (Mean Absolute Error) < 10 minutes
  - RMSE < 15 minutes
  - R² > 0.60
- [ ] Generate prediction intervals (e.g., "15-25 minutes" with 90% confidence)
- [ ] Real-time inference capability (predict waiting time in <1 second)
- [ ] Integration design with queue monitoring system

### Technical Notes
- XGBoost Regressor recommended for non-linear patterns
- Train on last 12 months of data with complete timestamps
- Feature engineering: derive "queue congestion index" (current queue / typical queue)
- Handle outliers in waiting_time_minutes (cap at 99th percentile during training)
- Save model to `models/waiting_time_predictor_v1.pkl`
- Platform: Databricks with Python (scikit-learn, xgboost)

### Estimated Effort
18-22 days

### Priority
High

## Dependencies
- [Story 03: Temporal Visitation EDA](#03-temporal-visitation-eda.md) - Understand typical waiting time patterns
- POLYCLINIC_ATTENDANCES with complete timestamp fields
- Real-time queue length data (may require integration with appointment system)
