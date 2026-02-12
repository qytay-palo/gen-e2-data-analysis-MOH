# User Story: 2 - Exploratory Seasonal Pattern Analysis

**As a** public health surveillance analyst,
**I want** to explore and visualize seasonal patterns, trends, and cyclical behavior for Dengue Fever and HFMD over 9 years,
**so that** I can understand disease dynamics, identify predictable patterns, and formulate hypotheses for forecasting models.

## 1. 🎯 Acceptance Criteria

1. **Temporal Trend Analysis**
   - Overall trends visualized for Dengue and HFMD (2012-2020)
   - Long-term growth/decline patterns identified
   - Year-over-year comparisons conducted
   - COVID-19 impact in 2020 documented

2. **Seasonal Pattern Identification**
   - Seasonal decomposition performed (trend, seasonal, residual components)
   - Peak and trough periods identified by calendar month/week
   - Seasonality strength quantified
   - Consistent seasonal patterns validated across years

3. **Outbreak Episode Detection**
   - Outbreak threshold defined (e.g., mean + 2 standard deviations)
   - Outbreak episodes identified and cataloged (dates, duration, magnitude)
   - Outbreak frequency calculated (outbreaks per year)
   - Outbreak intensity measured (peak-to-baseline ratio)

4. **Exploratory Data Analysis Report**
   - Summary of key findings and patterns
   - Hypotheses for forecasting formulated
   - Visualizations: time series plots, seasonal subseries plots, autocorrelation plots
   - Recommendations for model development

## 2. 🔒 Technical Constraints

- **Data Processing**: Polars for data manipulation; Pandas for time series decomposition if needed
- **Visualization**: Matplotlib, Seaborn for static plots; Plotly for interactive exploration
- **Statistical Analysis**: Statsmodels for seasonal decomposition, ACF/PACF
- **Platform**: Databricks notebook with version control
- **Output**: Interactive EDA report with embedded visualizations

## 3. 📚 Domain Knowledge References

- [Infectious Disease Epidemiology Terminology](../../../domain_knowledge/infectious-disease-epidemiology-terminology-glossary.md) - Seasonality, outbreak definitions, endemic patterns
- [Time Series Forecasting Best Practices](../../../domain_knowledge/time-series-forecasting-best-practices.md) - Seasonal decomposition, stationarity, autocorrelation
- [Infectious Disease Bulletin Data Dictionary](../../../data_dictionary/infectious_disease_bulletin.md) - Case count interpretation

**Key Concepts**:
- **Seasonality**: Dengue typically peaks May-October (warmer, wetter months)
- **Outbreak**: Cases exceeding mean + 2 SD baseline
- **Endemic baseline**: Typical case count range during non-outbreak periods
- **Autocorrelation**: Cases correlated with previous weeks (disease persistence)

## 4. 📦 Dependencies

**External Packages**:
- `statsmodels` - Seasonal decomposition (STL), ACF/PACF analysis
- `scipy` - Statistical tests (Mann-Kendall trend test)
- `plotly` - Interactive visualizations
- `polars` / `pandas` - Data manipulation

**Internal Dependencies**:
- Clean disease surveillance dataset from User Story 1
- Harmonized HFMD data (combined naming variants)

## 5. ✅ Implementation Tasks

### Temporal Trend Analysis
- ⬜ Create weekly time series plots for Dengue and HFMD (2012-2020)
- ⬜ Calculate and visualize 4-week and 12-week moving averages
- ⬜ Perform Mann-Kendall trend test to assess significance
- ⬜ Compare 2020 patterns to 2012-2019 (COVID-19 impact check)

### Seasonal Pattern Analysis
- ⬜ Perform STL decomposition (Seasonal-Trend-Loess) for both diseases
- ⬜ Extract seasonal component and calculate seasonal indices by week/month
- ⬜ Create seasonal subseries plots (compare same week/month across years)
- ⬜ Quantify seasonality strength (seasonal range / mean)

### Cyclical Behavior Analysis
- ⬜ Calculate autocorrelation function (ACF) for lag 1-52 weeks
- ⬜ Calculate partial autocorrelation function (PACF)
- ⬜ Identify significant lag correlations for forecasting
- ⬜ Check for biennial or multi-year cycles

### Outbreak Detection and Characterization
- ⬜ Define outbreak threshold: mean + 2 SD (separately for each disease)
- ⬜ Identify all outbreak episodes (consecutive weeks above threshold)
- ⬜ Calculate outbreak metrics: frequency, duration, peak magnitude
- ⬜ Visualize outbreak timeline with annotated episodes

### Statistical Testing
- ⬜ Test for stationarity using Augmented Dickey-Fuller (ADF) test
- ⬜ Assess need for differencing or detrending
- ⬜ Test seasonal pattern significance
- ⬜ Perform hypothesis tests comparing outbreak vs. non-outbreak periods

### Visualization and Reporting
- ⬜ Create comprehensive EDA dashboard with key visualizations
- ⬜ Document seasonal patterns with calendar heatmaps
- ⬜ Generate summary statistics table (by year, by season)
- ⬜ Write findings report with forecasting recommendations

## 6. Notes

**Expected Seasonal Patterns**:
- **Dengue**: Strong seasonality with peaks during Jun-Oct (warmer, wetter monsoon season); troughs Dec-Mar
- **HFMD**: Biennial pattern observed in some years; school-related transmission (lower during school holidays)

**Outbreak Definition**: Threshold-based approach (mean + 2 SD) is standard for surveillance. May need disease-specific adjustments based on distribution characteristics.

**Stationarity**: Time series forecasting models (ARIMA) require stationary data. Non-stationary trends may require differencing or transformation.

**COVID-19 Impact**: 2020 data may show disrupted patterns due to circuit breaker measures, social distancing, and reduced healthcare-seeking behavior. Consider analyzing 2012-2019 separately if 2020 is anomalous.

**Hypothesis Formulation**: EDA findings should directly inform model selection (e.g., strong seasonality → use seasonal ARIMA or Prophet; high autocorrelation → include lag features).
