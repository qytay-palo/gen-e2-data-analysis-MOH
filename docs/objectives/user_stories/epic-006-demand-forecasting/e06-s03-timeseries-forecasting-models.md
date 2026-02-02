# E06-S03: Develop Time-Series Forecasting Models

**Story ID**: E06-S03  
**Epic**: EPIC-006 - Predictive Demand Forecasting for Capacity Planning

## Parent Epic
Predictive Demand Forecasting for Capacity Planning - Building validated demand forecasting models to predict patient visits and provide evidence-based capacity recommendations for strategic planning.

## Overview and Statement

Build and validate time-series forecasting models (ARIMA, SARIMA, Prophet) to predict healthcare demand 1-year and 5-years ahead with accuracy ≤15% MAPE.

**As a** predictive analytics specialist  
**I want to** develop accurate time-series models forecasting future healthcare demand  
**So that** planners can anticipate future capacity needs

### Acceptance Criteria
- [ ] Develop multiple forecasting models: ARIMA, SARIMA, Facebook Prophet
- [ ] Generate 1-year and 5-year ahead forecasts by facility and service type
- [ ] Achieve ≤15% mean absolute percentage error (MAPE) on validation data
- [ ] Provide forecast confidence intervals (80%, 95%)
- [ ] Use walk-forward validation for model testing
- [ ] Compare model performance and select best approach by use case
- [ ] Document model specifications and parameters
- [ ] Create forecast visualizations with uncertainty bands

### Technical Notes
- Use statsmodels for ARIMA/SARIMA implementation
- Apply Facebook Prophet for automatic seasonality handling
- Split data: train on 2006-2017, validate on 2018-2020
- Test stationarity (ADF test) and difference if needed
- Grid search for optimal ARIMA parameters
- Evaluate multiple accuracy metrics (MAPE, RMSE, MAE)
- Consider ensemble approaches combining multiple models

### Estimated Effort
8 days

### Priority
Critical

## Dependencies
- E06-S01: Requires prepared demand data
- E06-S02: Requires understanding of demand patterns
