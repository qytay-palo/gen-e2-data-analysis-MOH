# Story 05: Daily Occupancy Forecasting Model

## Overview and Statement

Predicting future polyclinic attendance volumes enables proactive resource planning and prevents overcrowding. This story builds time-series forecasting models to predict daily attendance by polyclinic, accounting for trends, seasonality, and external factors.

**As a** Polyclinic Operations Manager  
**I want** to forecast expected daily attendance volumes for my polyclinic over the next 4 weeks  
**So that** I can adjust staffing levels and appointment slot availability in advance

### Acceptance Criteria
- [ ] Train time-series forecasting models (Prophet, ARIMA/SARIMA) on historical attendance data
- [ ] Generate 4-week ahead forecasts for each polyclinic
- [ ] Incorporate external regressors (public holidays, day of week)
- [ ] Model evaluation metrics:
  - MAPE (Mean Absolute Percentage Error) < 15%
  - RMSE reported for each polyclinic
- [ ] Generate forecast confidence intervals (80%, 95%)
- [ ] Create forecast visualization dashboard showing actual vs predicted volumes
- [ ] Document model assumptions, limitations, and retraining frequency

### Technical Notes
- Use Prophet (Facebook) for trend/seasonality decomposition (Python)
- Consider SARIMA for polyclinics with strong seasonal patterns
- Train/test split: Train on first 18 months, test on last 6 months
- Save trained models to `models/` directory with versioning
- Automate weekly re-forecasting pipeline
- Platform: Databricks with Python (fbprophet, statsmodels)

### Estimated Effort
15-20 days

### Priority
High

## Dependencies
- [Story 03: Temporal Visitation EDA](#03-temporal-visitation-eda.md) - Understanding seasonality patterns
- Minimum 24 months of attendance data for robust seasonality detection
