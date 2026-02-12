# User Story: 5 - Evaluate Forecast Model Performance and Reliability

**As a** healthcare data analyst,
**I want** to rigorously evaluate forecast model performance across different scenarios, diseases, and time periods,
**so that** I can communicate prediction reliability, model limitations, and deployment recommendations to MOH stakeholders with confidence.

## 1. 🎯 Acceptance Criteria

1. **Comprehensive Performance Assessment**
   - Accuracy metrics (MAE, RMSE, MAPE) calculated for each model, disease, and forecast horizon
   - Performance compared against naive and seasonal naive baselines
   - Forecast skill scores quantified (improvement over baseline)
   - Best-performing models identified for each disease and horizon

2. **Robustness Testing**
   - Model performance evaluated across different seasons (peak vs. trough)
   - Outbreak period forecasting accuracy assessed separately
   - 2020 COVID-19 impact on forecast accuracy quantified
   - Performance variability analyzed (consistency across time periods)

3. **Uncertainty Quantification**
   - Prediction interval coverage validated (actual vs. target: 80%, 95%)
   - Forecast bias assessed (systematic over/under-prediction)
   - Uncertainty increases with forecast horizon documented
   - Confidence intervals calibrated if needed

4. **Validation Report Delivered**
   - Model evaluation report with performance summary tables
   - Visualization of actual vs. forecast with error bands
   - Deployment recommendations with limitations clearly stated
   - Stakeholder-friendly executive summary

## 2. 🔒 Technical Constraints

- **Evaluation Data**: Validation set (2019) and test set (2020)
- **Metrics**: Standardized across all models for fair comparison
- **Scenarios**: Peak season, trough season, outbreak periods, stable periods
- **Output Format**: Report as Databricks notebook + PDF export for stakeholders
- **Reproducibility**: Evaluation code versioned and documented

## 3. 📚 Domain Knowledge References

- [Time Series Forecasting Best Practices](../../../domain_knowledge/time-series-forecasting-best-practices.md) - Forecast accuracy metrics, prediction intervals, model validation
- [Infectious Disease Epidemiology Terminology](../../../domain_knowledge/infectious-disease-epidemiology-terminology-glossary.md) - Outbreak definitions, seasonal patterns

**Evaluation Criteria from Domain Knowledge**:
- **MAE**: Average absolute error in case counts
- **MAPE**: 15-30% = good; 30-50% = acceptable for infectious disease forecasting
- **Coverage**: 80%/95% of actuals should fall within 80%/95% prediction intervals
- **Forecast skill**: 20-40% improvement over seasonal naive baseline is strong performance

## 4. 📦 Dependencies

**External Packages**:
- `scikit-learn` - Evaluation metrics (MAE, RMSE, MAPE)
- `numpy` / `scipy` - Statistical tests, confidence interval calculations
- `matplotlib` / `seaborn` / `plotly` - Visualization
- `polars` / `pandas` - Data manipulation

**Internal Dependencies**:
- Trained forecasting models from User Story 4
- Validation and test datasets
- Seasonal pattern analysis from User Story 2 (for scenario segmentation)

## 5. ✅ Implementation Tasks

### Accuracy Metric Calculation
- ⬜ Calculate MAE (Mean Absolute Error) for each model and horizon
- ⬜ Calculate RMSE (Root Mean Square Error)
- ⬜ Calculate MAPE (Mean Absolute Percentage Error)
- ⬜ Calculate forecast skill vs. seasonal naive baseline
- ⬜ Generate accuracy metric comparison table

### Scenario-Based Evaluation
- ⬜ Segment validation data by season (peak months vs. trough months)
- ⬜ Identify outbreak periods in validation set
- ⬜ Calculate accuracy metrics separately for peak, trough, and outbreak scenarios
- ⬜ Compare model performance across scenarios

### Robustness Testing
- ⬜ Evaluate forecast accuracy by forecast horizon (4-week, 8-week, 12-week)
- ⬜ Assess performance degradation with longer horizons
- ⬜ Test model stability across different starting points (rolling validation)
- ⬜ Compare 2019 (normal year) vs. 2020 (COVID-19) performance

### Uncertainty Quantification
- ⬜ Calculate prediction interval coverage (% of actuals within 80% PI, 95% PI)
- ⬜ Assess forecast bias: mean(forecast - actual)
- ⬜ Analyze error distribution (symmetric vs. skewed)
- ⬜ Calibrate prediction intervals if coverage is off-target
- ⬜ Document uncertainty increase with forecast horizon

### Statistical Significance Testing
- ⬜ Perform Diebold-Mariano test to compare model forecasts
- ⬜ Test if performance differences are statistically significant
- ⬜ Assess consistency of results across cross-validation folds

### Visualization and Communication
- ⬜ Create forecast vs. actual plots with prediction intervals
- ⬜ Generate model performance comparison charts (bar charts, heatmaps)
- ⬜ Visualize error distribution and bias
- ⬜ Create scenario-specific performance dashboards

### Validation Report Creation
- ⬜ Write executive summary (1-2 pages) for non-technical stakeholders
- ⬜ Document model performance with accuracy metrics and interpretations
- ⬜ Clearly state model limitations and assumptions
- ⬜ Provide deployment recommendations with confidence levels
- ⬜ Include risk mitigation strategies for forecast errors

## 6. Notes

**Success Criteria from PS-001**:
- **Target**: 70%+ accuracy for 8-12 week forecasts
- **Interpretation**: MAPE ≤ 30% or MAE significantly better than seasonal naive baseline
- **Stakeholder Use**: Healthcare facility committees can confidently use forecasts for staffing decisions 2-3 months ahead

**Expected Performance**:
- **4-week horizon**: High accuracy (MAPE 15-25%), narrow prediction intervals
- **8-week horizon**: Moderate accuracy (MAPE 25-35%), wider intervals
- **12-week horizon**: Lower accuracy (MAPE 35-50%), substantial uncertainty

**Scenario Performance Insights**:
- **Peak season**: Higher absolute errors but similar MAPE (% error)
- **Outbreak periods**: Harder to forecast; may have higher MAPE
- **Stable periods**: More predictable; lower error rates

**COVID-19 Impact (2020)**:
- Public health measures (circuit breaker, distancing) disrupted transmission
- Forecast accuracy likely degraded in 2020 vs. 2019
- Document as external validity limitation
- Recommend excluding 2020 from normal accuracy benchmarks

**Model Deployment Decision**:
- If MAPE > 30% for all models at 8-12 weeks: Recommend shorter horizon or hybrid approach
- If one model clearly outperforms: Deploy as primary model
- If models perform similarly: Use ensemble or simplest model for maintainability

**Stakeholder Communication**:
- Avoid technical jargon; focus on "forecast accuracy," "confidence levels," "reliability"
- Use visual examples: "80% confident cases will be between 600-900"
- Emphasize practical implications: "Forecasts enable 8-week staffing planning with X% reliability"
