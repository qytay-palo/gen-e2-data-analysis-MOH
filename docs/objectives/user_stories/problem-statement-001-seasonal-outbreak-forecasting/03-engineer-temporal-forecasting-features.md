# User Story: 3 - Engineer Temporal Forecasting Features

**As a** data scientist,
**I want** to create temporal features including lag variables, rolling statistics, and seasonal indicators for Dengue and HFMD,
**so that** I can build robust forecasting models that capture disease transmission dynamics and seasonal patterns.

## 1. 🎯 Acceptance Criteria

1. **Lag Features Created**
   - Previous week case counts (lag-1, lag-2, lag-4, lag-8, lag-12)
   - Previous year same week (lag-52) for year-over-year comparison
   - Lag features validated for data leakage (no future information)

2. **Rolling Window Features**
   - 2-week, 4-week, 8-week rolling averages (moving average smoothing)
   - 4-week rolling standard deviation (volatility measure)
   - Rolling minimum and maximum over 8-week window

3. **Seasonal Indicator Features**
   - Week of year (1-53) as cyclical feature
   - Month (1-12) as categorical and cyclical
   - Quarter (Q1-Q4) for broader seasonal grouping
   - Sine and cosine transforms for week of year (captures cyclical nature)

4. **Calendar Features**
   - Public holiday indicators (Singapore holidays)
   - School holiday indicators (MOE school term calendar)
   - Year indicator for capturing long-term trends

5. **Feature Engineering Documentation**
   - All features documented with rationale and calculation method
   - Feature correlation analysis performed
   - Feature importance validated against domain knowledge
   - Dataset ready for model training with engineered features

## 2. 🔒 Technical Constraints

- **Data Processing**: Polars for efficient feature engineering
- **Feature Store**: Save engineered features as separate dataset for reuse
- **Validation**: Ensure no data leakage (future information in features)
- **Scalability**: Feature engineering pipeline should work for all 45 diseases
- **Documentation**: Clear naming conventions for features (e.g., `cases_lag_1`, `cases_rolling_avg_4w`)

## 3. 📚 Domain Knowledge References

- [Time Series Forecasting Best Practices](../../../domain_knowledge/time-series-forecasting-best-practices.md) - Lag features, rolling statistics, seasonal features, Fourier transforms
- [Infectious Disease Epidemiology Terminology](../../../domain_knowledge/infectious-disease-epidemiology-terminology-glossary.md) - Disease transmission dynamics, seasonality concepts

**Feature Engineering Rationale**:
- **Lag-1**: Captures disease persistence (this week's cases depend on last week)
- **Lag-52**: Year-over-year comparison (same seasonal period last year)
- **Rolling averages**: Smooth out noise, reveal underlying trends
- **Week of year**: Captures within-year seasonality (Dengue peaks week 20-35)
- **Sine/cosine transforms**: Preserves cyclical continuity (week 52 → week 1)

## 4. 📦 Dependencies

**External Packages**:
- `polars` - Feature engineering and data manipulation
- `numpy` - Trigonometric functions for cyclical encoding
- `scikit-learn` - Feature scaling if needed
- `pandas` - Secondary support for date handling

**Internal Dependencies**:
- Clean disease surveillance dataset from User Story 1
- Exploratory analysis findings from User Story 2 (inform feature selection)
- Singapore public holiday calendar (if available) or workaround calendar

## 5. ✅ Implementation Tasks

### Lag Feature Engineering
- ⬜ Create lag-1 (previous week) cases for Dengue and HFMD
- ⬜ Create lag-2, lag-4, lag-8, lag-12 (recent history features)
- ⬜ Create lag-52 (same week last year for seasonality)
- ⬜ Handle missing values at beginning of series (first 52 weeks have no lag-52)

### Rolling Window Features
- ⬜ Calculate 2-week rolling average (short-term smoothing)
- ⬜ Calculate 4-week rolling average (monthly smoothing)
- ⬜ Calculate 8-week rolling average (longer-term trend)
- ⬜ Calculate 4-week rolling standard deviation (volatility measure)
- ⬜ Calculate 8-week rolling min and max (range indicators)

### Seasonal and Calendar Features
- ⬜ Extract week of year (1-53) from epi_week
- ⬜ Create sine transform: sin(2π × week / 52)
- ⬜ Create cosine transform: cos(2π × week / 52)
- ⬜ Extract month (1-12) from epi_week
- ⬜ Create quarter feature (Q1-Q4)
- ⬜ Create year feature (2012-2020)

### Calendar Event Features
- ⬜ Create public holiday indicator (1 if week includes Singapore public holiday)
- ⬜ Create school holiday indicator (1 during MOE school vacation periods)
- ⬜ Document holiday dates and mapping logic

### Feature Validation and Analysis
- ⬜ Check for data leakage (no future information in features)
- ⬜ Calculate correlation matrix for all features
- ⬜ Identify highly correlated features (potential multicollinearity)
- ⬜ Validate features against domain knowledge expectations

### Feature Dataset Creation
- ⬜ Combine all engineered features into comprehensive dataset
- ⬜ Handle missing values (first 52 weeks lack lag-52)
- ⬜ Split data: training (2012-2018), validation (2019), test (2020)
- ⬜ Save feature-engineered dataset for model training

### Documentation
- ⬜ Document all features with name, calculation, rationale
- ⬜ Create feature engineering pipeline notebook
- ⬜ Generate feature summary statistics
- ⬜ Write feature engineering report with recommendations

## 6. Notes

**Feature Engineering Best Practices**:
- **Avoid data leakage**: Features must only use information available at prediction time. Lag features ensure this.
- **Handle missing values**: First 52 weeks have no lag-52 values. Options: drop rows, forward fill, or use shorter lags.
- **Cyclical encoding**: Week 52 is close to week 1 (cyclically). Sine/cosine encoding preserves this relationship.
- **Feature selection**: Not all features may improve model. Use correlation analysis and domain knowledge to select relevant features.

**Expected Feature Importance**:
- **High importance**: lag-1, lag-52, week of year (strong autocorrelation and seasonality)
- **Medium importance**: rolling averages, month
- **Lower importance**: year (long-term trend less relevant for 8-12 week forecasts)

**Calendar Features**: Singapore public holidays and school holidays may affect case reporting and disease transmission (e.g., HFMD lower during school holidays). If holiday calendar unavailable, this is optional.

**Scalability**: Feature engineering pipeline should be parameterized to work for all 45 diseases, not just Dengue and HFMD. This enables future expansion.
