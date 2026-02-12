# Domain Knowledge: Time Series Forecasting Best Practices for Infectious Diseases

## Overview
This document provides best practices, methodologies, and implementation guidance for forecasting infectious disease case counts. It is tailored to Singapore's MOH context with weekly surveillance data and supports evidence-based resource planning for healthcare facilities and policy makers.

## Related Problem Statements
- [Problem Statement PS-001 - Seasonal Outbreak Forecasting](../objectives/problem_statements/ps-001-seasonal-outbreak-forecasting.md)

## Related Stakeholders
- **MOH Policy Makers**: Use forecasts for strategic resource allocation and budget planning
- **Healthcare Facility Committees**: Apply forecasts for staffing and capacity decisions 2-3 months ahead
- **Public Health Surveillance Teams**: Interpret forecasts for outbreak preparedness
- **Epidemiologists**: Validate forecasting methodologies and model assumptions

## Key Concepts and Terminology

### Forecast Horizon
**Definition**: Time period into the future that predictions cover
**Relevance**: Longer horizons enable earlier planning but reduce accuracy
**Typical Ranges**: 
- Short-term: 1-4 weeks (high accuracy, operational planning)
- Medium-term: 8-12 weeks (moderate accuracy, strategic planning)
- Long-term: 6-12 months (lower accuracy, annual budgeting)
**Example**: 8-12 week forecast enables hiring temporary staff before predicted outbreak peak

### Point Forecast
**Definition**: Single predicted value for future time period
**Relevance**: Simple to communicate but doesn't capture uncertainty
**Interpretation**: Expected case count under most likely scenario
**Example**: "We forecast 850 dengue cases in Week 25"

### Prediction Interval
**Definition**: Range of values likely to contain the true future value with specified confidence
**Relevance**: Communicates forecast uncertainty; essential for risk management
**Typical Confidence Levels**: 80%, 90%, 95%
**Interpretation**: "95% confident dengue cases will be between 600-1,100 in Week 25"
**Example**: Wider intervals for diseases with high volatility (e.g., Zika outbreaks); narrower for stable endemic diseases

### Forecast Accuracy Metrics
**Definition**: Quantitative measures of how well forecasts match actual outcomes
**Key Metrics**:
- **MAE (Mean Absolute Error)**: Average absolute difference between forecast and actual
- **RMSE (Root Mean Square Error)**: Square root of average squared errors (penalizes large errors)
- **MAPE (Mean Absolute Percentage Error)**: MAE as percentage of actual values
- **Coverage**: Proportion of actual values falling within prediction intervals
**Use Case**: Compare models; track performance over time; set stakeholder expectations

### Baseline Model
**Definition**: Simple forecasting method used as performance benchmark
**Common Baselines**:
- **Naive**: Next value = current value
- **Seasonal Naive**: Next value = same period last year
- **Moving Average**: Next value = average of recent observations
**Relevance**: Complex models should outperform baselines to justify adoption
**Example**: If ARIMA forecast only 5% more accurate than seasonal naive, may not warrant complexity

### Stationarity
**Definition**: Time series properties (mean, variance) constant over time
**Relevance**: Many forecasting methods assume stationarity
**Non-Stationary Indicators**: Trends, changing seasonality, varying volatility
**Transformation**: Differencing, log transform, detrending to achieve stationarity
**Example**: Dengue cases with upward trend are non-stationary; first-difference series may be stationary

## Standard Metrics and KPIs

| Metric Name | Definition | Calculation Formula | Typical Range | Use Case | Data Requirements |
|-------------|-----------|---------------------|---------------|----------|-------------------|
| Mean Absolute Error (MAE) | Average absolute forecast error | Σ\|Actual - Forecast\| / n | 10-200 cases (disease-specific) | Model comparison, accuracy reporting | Forecasts, actuals |
| Root Mean Square Error (RMSE) | Root of average squared errors | √(Σ(Actual - Forecast)² / n) | 15-300 cases | Model selection (penalizes large misses) | Forecasts, actuals |
| Mean Absolute Percentage Error (MAPE) | MAE as % of actual | Σ(\|Actual - Forecast\| / Actual) / n × 100 | 15%-30% (good); 30%-50% (acceptable) | Relative accuracy, cross-disease comparison | Forecasts, actuals |
| Forecast Skill | Improvement over baseline | (MAE_baseline - MAE_model) / MAE_baseline × 100 | 10%-40% improvement | Justify model complexity | Forecasts, baseline, actuals |
| Prediction Interval Coverage | % actuals within interval | (Actuals within interval / Total forecasts) × 100 | Target: 80%, 90%, 95% (matches confidence level) | Validate uncertainty quantification | Forecasts with intervals, actuals |
| Bias | Average directional error | Σ(Forecast - Actual) / n | Near 0 (unbiased); positive = over-forecast | Detect systematic errors | Forecasts, actuals |

## Feature Engineering Guidance

### Common Features for Infectious Disease Forecasting

#### Temporal Features (Essential)
- **Lag Features**: Previous case counts (lag-1, lag-2, ..., lag-12 weeks)
  - **Description**: Historical case counts from prior weeks
  - **Calculation**: Shift time series by n periods
  - **Interpretation**: Captures autocorrelation; last week's cases inform this week's forecast
  - **Use Cases**: ARIMA, regression models, machine learning
  - **Example**: HFMD forecast uses lag-1 (last week) and lag-52 (same week last year)

- **Rolling Statistics**: Moving averages, standard deviations
  - **Description**: Aggregated metrics over rolling windows (4-week, 8-week, 12-week)
  - **Calculation**: Mean, SD, min, max over rolling window
  - **Interpretation**: Smoothed trends capture underlying patterns
  - **Use Cases**: Trend-based models, outbreak detection thresholds
  - **Example**: 4-week moving average as baseline for anomaly detection

- **Seasonal Indicators**: Week of year, month, quarter
  - **Description**: Cyclical patterns within year
  - **Calculation**: Extract week number (1-53), month (1-12), quarter (Q1-Q4)
  - **Interpretation**: Diseases peak predictably each year
  - **Use Cases**: Seasonal decomposition, Prophet, regression
  - **Example**: Dengue peaks weeks 20-35; include week-of-year as feature

#### Calendar Features
- **Public Holidays**: Binary indicators for holiday weeks
  - **Description**: 1 if week includes public holiday, 0 otherwise
  - **Calculation**: Merge with Singapore public holiday calendar
  - **Interpretation**: Holidays affect healthcare-seeking behavior, reporting delays
  - **Use Cases**: Adjust forecasts for holiday weeks
  - **Example**: Chinese New Year week may show reduced clinic visits (delayed diagnosis)

- **School Holidays**: Binary indicators for school vacation periods
  - **Description**: 1 during school holidays, 0 otherwise
  - **Calculation**: Map weeks to MOE school term calendar
  - **Interpretation**: HFMD transmission lower when schools closed
  - **Use Cases**: Forecast HFMD, influenza-like illnesses
  - **Example**: June-July school holiday correlates with HFMD decrease

#### Statistical Transformations
- **Log Transform**: Log(cases + 1) to stabilize variance
  - **Description**: Natural logarithm of case counts
  - **Calculation**: ln(cases + 1) to handle zeros
  - **Interpretation**: Reduces impact of extreme values, stabilizes variance
  - **Use Cases**: When variance increases with case counts
  - **Example**: Dengue outbreak peaks distort scale; log transform normalizes

- **Differencing**: First-order differences to remove trends
  - **Description**: Current value minus previous value
  - **Calculation**: cases_t - cases_(t-1)
  - **Interpretation**: Converts non-stationary to stationary series
  - **Use Cases**: ARIMA models require stationarity
  - **Example**: Dengue cases trending up; differencing removes trend

### Domain-Specific Patterns

#### Seasonal Decomposition (STL)
**Description**: Separate time series into trend, seasonal, and residual components
**When to Apply**: Understanding drivers of case fluctuations; isolating seasonal patterns
**Implementation**: Use `statsmodels.tsa.seasonal.seasonal_decompose` or `stl` in R
**Example**: Dengue = upward trend (population growth, urbanization) + seasonal (weather) + residual (random fluctuations)

#### Fourier Terms for Seasonality
**Description**: Sine and cosine functions to model cyclical patterns
**When to Apply**: Flexible seasonal modeling; multiple seasonal periods
**Implementation**: `FourierFeaturizer` in Prophet; manual construction for regression
**Example**: Annual cycle: sin(2π × week/52), cos(2π × week/52)

#### Change Point Detection
**Description**: Identify time points where statistical properties abruptly change
**When to Apply**: Structural breaks (e.g., intervention effects, surveillance changes)
**Implementation**: PELT algorithm, Bayesian change point detection
**Example**: 2016 Zika outbreak introduced new transmission pattern; model before/after separately

### Temporal Features
- **Lag Features**: Previous weeks' case counts (lag-1 through lag-12)
- **Rolling Windows**: 2-week, 4-week, 8-week moving averages and standard deviations
- **Seasonal Indicators**: Week of year (1-53), month (1-12), quarter (Q1-Q4)
- **Year-over-Year**: Same week in previous year for seasonal comparison
- **Holiday Indicators**: Public holidays, school holidays (affect transmission and reporting)

### Aggregation Strategies
- **Multi-Disease Aggregates**: Total cases across related diseases (e.g., all foodborne)
- **Geographic Aggregates**: If regional data available; national-level limits spatial features
- **Demographic Aggregates**: Age-stratified forecasts if data available (not in current dataset)

## Data Quality Considerations

### Reporting Delays
- **Description**: Lag between case occurrence and data availability (typically 1-2 weeks for weekly bulletin)
- **Impact**: Real-time forecasts use incomplete recent data; underestimate current week
- **Detection**: Compare provisional vs. final case counts from bulletins
- **Mitigation**: Nowcasting methods to adjust for reporting lags; clearly state forecast date vs. data date

### Outliers and Anomalies
- **Description**: Unusually high/low case counts due to outbreaks, data errors, or reporting artifacts
- **Impact**: Distort model fitting; reduce forecast accuracy
- **Detection**: Statistical outlier detection (z-score > 3, IQR method); domain expert review
- **Mitigation**: Winsorize extreme values; robust forecasting methods (e.g., median-based); model outbreaks separately

### Data Revisions
- **Description**: Case counts updated retroactively as additional reports received
- **Impact**: Historical data changes; models trained on provisional data may differ from final
- **Detection**: Compare multiple downloads of same historical data
- **Mitigation**: Use most recent data version; retrain models periodically; document data vintage

### Missing Data
- **Description**: Weeks with no reported data (e.g., system downtime, public health emergencies)
- **Impact**: Breaks time series continuity; models assume regular intervals
- **Detection**: Check for gaps in epi-week sequence
- **Mitigation**: Interpolate missing values; exclude affected period; note data quality issues

### Non-Stationarity
- **Description**: Mean, variance, or seasonality changing over time (e.g., increasing dengue trend)
- **Impact**: Violates assumptions of many forecasting methods
- **Detection**: Augmented Dickey-Fuller test, visual inspection of time series plot
- **Mitigation**: Differencing, detrending, log transform; use methods robust to non-stationarity (e.g., Prophet)

## Analytical Methodologies

### ARIMA (AutoRegressive Integrated Moving Average)
- **Application**: Univariate time series forecasting for diseases with stable patterns
- **Assumptions**: Stationarity (after differencing); linear relationships; Gaussian errors
- **Implementation Notes**: 
  - Select order (p, d, q) using ACF/PACF plots, AIC/BIC criteria, or auto.arima
  - p = autoregressive lags; d = differencing order; q = moving average lags
  - SARIMA extends to seasonal patterns (P, D, Q, s) where s = seasonal period (52 weeks)
- **Interpretation**: Forecast = weighted sum of past values and errors; confidence intervals widen with horizon
- **Strengths**: Statistically rigorous; well-understood; fast computation
- **Limitations**: Requires stationarity; assumes linear relationships; struggles with regime changes

### Prophet (Facebook)
- **Application**: Automated forecasting with strong seasonality and holidays
- **Assumptions**: Piecewise linear/logistic trend; additive/multiplicative seasonality; holiday effects
- **Implementation Notes**:
  - Specify daily seasonality (False for weekly data), weekly seasonality (False), yearly seasonality (True)
  - Add custom holidays/school vacation periods
  - Tune changepoint prior scale (flexibility) and seasonality prior scale (strength)
- **Interpretation**: Forecast = trend + seasonality + holidays + error; decomposition aids interpretation
- **Strengths**: Handles missing data, outliers; easy to add domain knowledge; intuitive for non-experts
- **Limitations**: Less flexible than machine learning; may overfit with short time series

### Exponential Smoothing (ETS)
- **Application**: Trend and seasonal patterns with automatic weighting of recent data
- **Assumptions**: Errors additive or multiplicative; trend and seasonality evolve smoothly
- **Implementation Notes**:
  - Select model (ETS(A,A,A) = additive errors, trend, seasonality)
  - Holt-Winters method for seasonal data
- **Interpretation**: Forecast weights recent observations more heavily; smoothing parameters control responsiveness
- **Strengths**: Simple, fast; handles trend and seasonality; robust to outliers
- **Limitations**: Limited flexibility; assumes smooth evolution of patterns

### Machine Learning (Random Forest, XGBoost, LSTM)
- **Application**: Complex, non-linear patterns; multiple predictors (multivariate forecasting)
- **Assumptions**: Sufficient training data; features capture relevant patterns; overfitting controlled
- **Implementation Notes**:
  - Engineer lag features, rolling statistics, seasonal indicators
  - Time series cross-validation (rolling origin, expanding window)
  - Hyperparameter tuning (grid search, Bayesian optimization)
- **Interpretation**: Black-box models; use SHAP values for feature importance
- **Strengths**: Handles non-linearity, interactions; flexible feature engineering
- **Limitations**: Requires more data; risk of overfitting; less interpretable; computationally intensive

### Ensemble Methods
- **Application**: Combine multiple models to improve robustness and accuracy
- **Assumptions**: Individual models capture different patterns; errors are uncorrelated
- **Implementation Notes**:
  - Simple average, weighted average (inverse MAE), or stacking
  - Combine statistical (ARIMA) + machine learning (XGBoost) + domain (seasonal naive)
- **Interpretation**: Forecast = consensus of multiple perspectives; reduces model-specific risk
- **Strengths**: Often outperforms single models; robust to model misspecification
- **Limitations**: More complex; requires maintaining multiple models

## Common Pitfalls and Best Practices

### Pitfalls to Avoid
- **Overfitting**: Model captures noise, not signal; performs well on training data, poorly on new data
  - *Prevention*: Use time series cross-validation; penalize complexity (AIC, BIC); limit hyperparameter tuning
- **Ignoring Seasonality**: Seasonal patterns dominate infectious disease dynamics
  - *Prevention*: Visual inspection of time series; seasonal decomposition; include seasonal features
- **Extrapolating Trends**: Linear trends don't continue indefinitely (e.g., saturation effects, interventions)
  - *Prevention*: Use logistic trend (Prophet); cap forecasts at plausible maximum; scenario planning
- **Training on Full Data**: Evaluating on same data used for training inflates accuracy estimates
  - *Prevention*: Holdout recent data for testing; time series cross-validation
- **Forecasting Outbreaks**: Extreme events are inherently unpredictable; models trained on endemic periods miss outbreaks
  - *Prevention*: Probabilistic forecasts with wide intervals; separate outbreak detection system; scenario-based planning

### Best Practices
- **Start Simple**: Baseline models (seasonal naive) establish minimum performance; add complexity incrementally
- **Visualize Data and Forecasts**: Plots reveal patterns, anomalies, and forecast plausibility better than metrics alone
- **Use Multiple Metrics**: MAE, RMSE, MAPE capture different aspects of accuracy; coverage validates uncertainty
- **Cross-Validate Properly**: Time series CV (rolling origin, expanding window) respects temporal order; no data leakage
- **Document Assumptions**: State data limitations, model choices, and forecast caveats clearly for stakeholders
- **Update Models Regularly**: Retrain with new data quarterly or annually; monitor performance degradation
- **Communicate Uncertainty**: Always report prediction intervals; educate stakeholders on probabilistic interpretation
- **Validate with Domain Experts**: Epidemiologists assess forecast plausibility; identify data quality issues
- **Scenario Planning**: Supplement point forecasts with best/worst case scenarios for risk management

## Forecasting Workflow

### 1. Data Preparation (Week 1)
- Load historical weekly case data
- Check completeness, outliers, data quality
- Visualize time series for all diseases
- Select priority diseases (high burden, strong seasonality)

### 2. Exploratory Analysis (Week 1-2)
- Identify seasonal patterns (STL decomposition, seasonal plots)
- Test stationarity (ADF test)
- Examine autocorrelation (ACF/PACF plots)
- Detect outliers and structural breaks

### 3. Feature Engineering (Week 2)
- Create lag features, rolling statistics
- Add seasonal indicators, holiday flags
- Apply transformations (log, differencing) if needed
- Split data: training (2012-2018), validation (2019), test (2020)

### 4. Baseline Models (Week 2)
- Implement seasonal naive, moving average
- Calculate MAE, RMSE, MAPE on validation set
- Establish performance benchmarks

### 5. Model Development (Week 3-4)
- Fit ARIMA, Prophet, exponential smoothing
- Tune hyperparameters using validation set
- Optionally: machine learning models if baseline insufficient
- Compare models on validation set

### 6. Model Selection (Week 4)
- Choose best-performing model(s) for each disease
- Consider accuracy, simplicity, interpretability trade-offs
- Ensemble top models if improvement significant

### 7. Final Evaluation (Week 5)
- Evaluate selected model(s) on test set (2020 data)
- Calculate final accuracy metrics
- Validate prediction interval coverage
- Generate diagnostic plots (residuals, forecast vs. actual)

### 8. Deployment (Week 5-6)
- Retrain on full data (2012-2020)
- Generate 8-12 week forecasts
- Document methodology, assumptions, limitations
- Create stakeholder-facing dashboard/report

### 9. Monitoring (Ongoing)
- Track forecast accuracy as new data arrives
- Retrain models quarterly or when performance degrades
- Update forecasts weekly (or as new data published)

## Model Selection Criteria

| Criterion | Consideration | Decision Rule |
|-----------|--------------|---------------|
| **Accuracy** | MAE, RMSE, MAPE on validation set | Favor model with lowest error; >10% improvement justifies complexity |
| **Simplicity** | Model complexity, interpretability | Prefer simpler models if accuracy difference <5%; easier maintenance |
| **Robustness** | Performance across diseases, time periods | Consistent performance across diseases favored over disease-specific tuning |
| **Uncertainty Quantification** | Prediction interval coverage | Must achieve target coverage (e.g., 80%, 90%); miscalibrated intervals unacceptable |
| **Computational Cost** | Training time, forecasting time | Must retrain within reasonable time (< 1 hour); real-time forecasting if needed |
| **Stakeholder Trust** | Interpretability, transparency | Epidemiologists must understand methodology; black-box models require justification |

## References and Sources

### Authoritative Sources
- **CDC Forecasting Guidelines**: https://www.cdc.gov/flu/weekly/overview.htm - Influenza forecasting best practices applicable to other diseases
- **WHO Epidemic Intelligence**: https://www.who.int/teams/epidemic-and-pandemic-prevention-and-preparedness - Global standards for disease forecasting

### Academic References
- Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice* (3rd ed.). OTexts. https://otexts.com/fpp3/
- Taylor, S. J., & Letham, B. (2018). "Forecasting at scale." *The American Statistician*, 72(1), 37-45.
- Box, G. E. P., Jenkins, G. M., Reinsel, G. C., & Ljung, G. M. (2015). *Time Series Analysis: Forecasting and Control* (5th ed.). Wiley.

### Industry Standards
- **ISO 8601 Week Dates**: Standard for epidemiological week numbering
- **WMO Statistical Forecasting Guidelines**: World Meteorological Organization standards applicable to time series

## Cross-References

### Related Domain Knowledge Files
- [Infectious Disease Epidemiology Terminology](infectious-disease-epidemiology-terminology-glossary.md) - Core concepts and definitions
- [Stakeholder: Public Health Surveillance Team Expertise](stakeholder-public-health-surveillance-team-expertise.md) - Forecast user perspective

### Related Data Dictionary Entries
- [Weekly Infectious Disease Bulletin](../data_dictionary/infectious_disease_bulletin.md) - Data source for forecasting

## Metadata

**Created**: 9 February 2026
**Last Updated**: 9 February 2026
**Updated By**: GitHub Copilot
**Update Reason**: Initial creation for PS-001 user story generation
**Version**: 1.0

## Notes

This document focuses on methods applicable to weekly, national-level infectious disease data. For facility-level or daily forecasting, additional considerations apply. Consult epidemiologists before deploying forecasts for operational decision-making.
