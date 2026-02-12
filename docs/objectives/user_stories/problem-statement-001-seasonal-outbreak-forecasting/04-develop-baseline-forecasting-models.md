# User Story: 4 - Develop Baseline Forecasting Models

**As a** data scientist,
**I want** to develop and compare multiple baseline forecasting models for Dengue Fever and HFMD with 8-12 week forecast horizons,
**so that** I can establish benchmark performance and identify the most promising modeling approaches for operational deployment.

## 1. 🎯 Acceptance Criteria

1. **Multiple Models Implemented**
   - Naive baseline (next week = current week)
   - Seasonal naive (next week = same week last year)
   - Moving average (4-week, 8-week)
   - ARIMA/SARIMA (auto-tuned parameters)
   - Prophet (Facebook's forecasting tool)
   - Ensemble approach combining models

2. **Forecast Horizons Tested**
   - 4-week ahead forecasts
   - 8-week ahead forecasts
   - 12-week ahead forecasts
   - Rolling forecast validation (walk-forward)

3. **Model Performance Evaluated**
   - MAE (Mean Absolute Error) calculated for each model and horizon
   - RMSE (Root Mean Square Error) calculated
   - MAPE (Mean Absolute Percentage Error) calculated
   - Forecast skill vs. baseline quantified
   - Performance compared across forecast horizons

4. **Best Model Identified**
   - Model rankings by accuracy metrics
   - Trade-offs documented (accuracy vs. complexity vs. interpretability)
   - Recommendation for production model
   - Confidence intervals/prediction intervals generated

## 2. 🔒 Technical Constraints

- **Training Data**: 2012-2018 (7 years)
- **Validation Data**: 2019 (1 year)
- **Test Data**: 2020 (held out for final evaluation)
- **Platform**: Databricks with Python
- **Libraries**: Statsmodels (ARIMA), Prophet, scikit-learn
- **Computational Budget**: Models should train in reasonable time (<1 hour per disease)

## 3. 📚 Domain Knowledge References

- [Time Series Forecasting Best Practices](../../../domain_knowledge/time-series-forecasting-best-practices.md) - Forecast horizons, accuracy metrics, baseline models, ARIMA, Prophet
- [Infectious Disease Epidemiology Terminology](../../../domain_knowledge/infectious-disease-epidemiology-terminology-glossary.md) - Outbreak forecasting context

**Model Selection Rationale**:
- **Naive/Seasonal Naive**: Simple benchmarks every model must beat
- **ARIMA/SARIMA**: Standard time series forecasting; captures autocorrelation and seasonality
- **Prophet**: Handles seasonality, holidays, missing data; designed for business forecasting
- **Ensemble**: Combine strengths of multiple models; often improves accuracy

**Target Accuracy**: 70%+ accuracy for 8-12 week forecasts (per problem statement acceptance criteria)

## 4. 📦 Dependencies

**External Packages**:
- `statsmodels` - ARIMA, SARIMA, auto_arima
- `prophet` (fbprophet) - Facebook Prophet forecasting
- `scikit-learn` - Model evaluation, cross-validation
- `polars` / `pandas` - Data manipulation
- `numpy` - Numerical operations

**Internal Dependencies**:
- Feature-engineered dataset from User Story 3
- Seasonal pattern analysis from User Story 2 (informs model configuration)

## 5. ✅ Implementation Tasks

### Baseline Models
- ⬜ Implement naive forecast (next value = current value)
- ⬜ Implement seasonal naive (next value = same period last year)
- ⬜ Implement moving average (4-week, 8-week windows)
- ⬜ Evaluate baseline models on validation set

### ARIMA/SARIMA Models
- ⬜ Test for stationarity (ADF test); apply differencing if needed
- ⬜ Use auto_arima to identify optimal ARIMA parameters (p, d, q)
- ⬜ Fit SARIMA models with seasonal parameters (P, D, Q, s=52 for weekly seasonality)
- ⬜ Generate forecasts for 4-week, 8-week, 12-week horizons
- ⬜ Calculate prediction intervals (80%, 95% confidence)

### Prophet Models
- ⬜ Prepare data in Prophet format (ds, y columns)
- ⬜ Configure seasonality: yearly (period=52 weeks)
- ⬜ Add Singapore public holiday calendar if available
- ⬜ Tune hyperparameters: changepoint_prior_scale, seasonality_prior_scale
- ⬜ Generate forecasts with uncertainty intervals

### Ensemble Model
- ⬜ Implement simple ensemble (average of ARIMA, Prophet, seasonal naive)
- ⬜ Implement weighted ensemble (weights based on validation performance)
- ⬜ Test ensemble on validation set

### Model Evaluation
- ⬜ Implement walk-forward validation (rolling forecast origin)
- ⬜ Calculate MAE, RMSE, MAPE for each model and horizon
- ⬜ Calculate forecast skill: (MAE_baseline - MAE_model) / MAE_baseline
- ⬜ Compare model performance across 4-week, 8-week, 12-week horizons
- ⬜ Generate model comparison table and visualizations

### Model Selection
- ⬜ Rank models by accuracy metrics
- ⬜ Assess model complexity vs. performance trade-offs
- ⬜ Validate interpretability for stakeholders
- ⬜ Select recommended model for each disease and horizon
- ⬜ Document model selection rationale

### Forecast Visualization
- ⬜ Plot actual vs. forecast for each model
- ⬜ Include prediction intervals in plots
- ⬜ Create forecast comparison dashboard
- ⬜ Generate model performance summary report

## 6. Notes

**Model Training Strategy**: Use walk-forward validation to mimic operational forecasting. Train model on data up to time t, forecast t+h, then move forward one week and repeat.

**Forecast Accuracy Targets** (from PS-001):
- **Target**: 70%+ accuracy for 8-12 week ahead forecasts
- **Interpretation**: MAPE < 30% or forecast skill > 30% vs. seasonal naive baseline

**Model Selection Criteria**:
1. **Accuracy**: Primary criterion (MAE, RMSE, MAPE)
2. **Robustness**: Performance across different time periods and outbreak scenarios
3. **Interpretability**: Stakeholders must understand and trust model
4. **Computational cost**: Retraining time should be reasonable for weekly updates
5. **Uncertainty quantification**: Confidence intervals essential for decision-making

**Expected Results**:
- **Baseline models**: Likely MAPE 40-60% for 8-12 week forecasts
- **ARIMA/SARIMA**: Should achieve 25-35% MAPE if seasonality captured well
- **Prophet**: Similar to ARIMA; may handle holidays and trend changes better
- **Ensemble**: Potential 5-10% improvement over single best model

**COVID-19 Consideration**: 2020 test data may show degraded accuracy due to COVID-19 public health measures disrupting disease transmission patterns. Document this limitation.

**Model Maintenance**: Selected models will need periodic retraining as new data becomes available. Document retraining frequency recommendation (e.g., quarterly).
