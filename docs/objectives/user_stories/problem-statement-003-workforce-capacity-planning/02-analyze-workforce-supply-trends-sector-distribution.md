# User Story: 2 - Analyze Workforce Supply Trends and Sector Distribution

**As a** workforce planning team member,
**I want** to analyze multi-year workforce trends, growth patterns, and public-private sector shifts for doctors, nurses, and pharmacists,
**so that** I can identify workforce supply dynamics, sector imbalances, and project future supply trajectories.

## 1. 🎯 Acceptance Criteria

1. **Workforce Growth Trends Analyzed**
   - Historical growth rates calculated for each profession (2006-2019)
   - CAGR (Compound Annual Growth Rate) calculated
   - Growth acceleration/deceleration identified
   - Cross-profession growth comparisons conducted

2. **Sector Distribution Patterns Identified**
   - Public, private, not-for-profit workforce proportions analyzed over time
   - Public-to-private migration trends quantified
   - Sector shift rates calculated (% workforce moving between sectors)
   - Sector competitiveness assessed

3. **Workforce Supply Projections Developed**
   - 3-5 year workforce projections using trend extrapolation
   - Multiple scenarios modeled (base case, optimistic, pessimistic)
   - Projection confidence intervals calculated
   - Assumptions documented

4. **Trend Analysis Report Delivered**
   - Comprehensive trend analysis with visualizations
   - Key findings highlighted (growth patterns, sector shifts)
   - Implications for workforce planning documented
   - Recommendations for supply-side interventions

## 2. 🔒 Technical Constraints

- **Data Processing**: Polars for trend calculations
- **Statistical Methods**: Linear regression, CAGR, moving averages
- **Projections**: Simple extrapolation; avoid complex forecasting (annual data limits sophistication)
- **Output**: Trend analysis report as Databricks notebook

## 3. 📚 Domain Knowledge References

- [Healthcare Workforce Metrics and KPIs](../../../domain_knowledge/healthcare-workforce-metrics-kpis.md) - Growth rates, workforce density, sector distribution metrics
- [Time Series Forecasting Best Practices](../../../domain_knowledge/time-series-forecasting-best-practices.md) - Trend analysis methods (applicable to annual data)

**Key Metrics**:
- **CAGR**: Typical 2-5% annual growth for healthcare workforce in developed countries
- **Public-to-Private Ratio**: <1 indicates private-heavy; trend shows sector preferences
- **Growth Rate Benchmarks**: Compare to population growth, healthcare demand growth

## 4. 📦 Dependencies

**External Packages**:
- `polars` - Data manipulation and trend calculations
- `statsmodels` - Linear regression, trend decomposition
- `numpy` - Mathematical operations
- `matplotlib` / `seaborn` - Visualization

**Internal Dependencies**:
- Clean workforce datasets from User Story 1
- Historical population data (Singapore ~5.7M) for workforce density calculations

## 5. ✅ Implementation Tasks

### Growth Trend Analysis
- ⬜ Calculate year-over-year growth rates for each profession and sector
- ⬜ Calculate overall CAGR (2006-2019 for doctors/pharmacists, 2008-2019 for nurses)
- ⬜ Identify growth inflection points (acceleration/deceleration)
- ⬜ Compare growth rates across professions (doctors vs. nurses vs. pharmacists)

### Sector Distribution Analysis
- ⬜ Calculate sector proportions (% public, private, not-for-profit) by year
- ⬜ Calculate public-to-private ratio trends over time
- ⬜ Identify sector shift patterns (e.g., declining public share)
- ⬜ Quantify net workforce migration between sectors

### Statistical Trend Modeling
- ⬜ Fit linear regression models (workforce ~ year) for each profession
- ⬜ Test trend significance (p-values, R-squared)
- ⬜ Calculate trend coefficients (workforce added per year)
- ⬜ Assess linearity (residual plots, diagnostic checks)

### Workforce Density Analysis
- ⬜ Calculate workforce-to-population ratios (per 1,000 or 10,000 population)
- ⬜ Compare to WHO standards (doctors: >2.3 per 1,000)
- ⬜ Benchmark against OECD countries
- ⬜ Assess adequacy of current workforce levels

### Supply Projections
- ⬜ Develop 3-year and 5-year projections using historical trend extrapolation
- ⬜ Create base case scenario (trend continues)
- ⬜ Create optimistic scenario (higher growth)
- ⬜ Create pessimistic scenario (lower growth)
- ⬜ Calculate projection confidence intervals (±10%, ±20%)
- ⬜ Document assumptions for each scenario

### Cross-Profession Comparisons
- ⬜ Compare growth rates across doctors, nurses, pharmacists
- ⬜ Analyze sector distribution differences (e.g., nurses more public-heavy)
- ⬜ Identify professions with supply concerns (low growth, high sector imbalance)

### Visualization
- ⬜ Create time series plots with trend lines (historical + projections)
- ⬜ Generate sector distribution stacked area charts
- ⬜ Create public-to-private ratio line plots
- ⬜ Build scenario comparison charts (3-year, 5-year projections)

### Report Generation
- ⬜ Write trend analysis report with key findings
- ⬜ Document growth patterns and sector shifts
- ⬜ Highlight supply concerns and imbalances
- ⬜ Provide recommendations for workforce development strategies

## 6. Notes

**Expected Trends** (from problem statement context):
- **Public to Private Migration**: Workforce shifting from public to private sector over time (higher pay, better work-life balance in private)
- **Overall Growth**: Positive growth expected across all professions but rates may vary
- **Nurses**: Potentially higher growth due to expansion of healthcare services
- **Sector Imbalances**: Public healthcare may face recruitment challenges if private sector dominance increases

**Projection Limitations**:
- Annual data only (14 years for doctors/pharmacists, 12 years for nurses) limits sophistication
- Linear trend extrapolation assumes continuation of historical patterns
- External shocks (policy changes, immigration restrictions, pandemics) not accounted for
- Projections are indicative only; sensitivity analysis essential

**Supply-Side Interventions**:
- **Recruitment**: Increase domestic training capacity (medical/nursing schools)
- **Immigration**: Attract foreign healthcare professionals
- **Retention**: Improve public sector compensation and working conditions to reduce migration to private
- **Re-entry**: Encourage inactive workforce to return to practice

**International Benchmarks**:
- **WHO Standard**: 2.3 doctors per 1,000 population (Singapore likely exceeds)
- **OECD Average**: ~3.5 doctors per 1,000; ~8-10 nurses per 1,000
- Singapore context: High-income country with strong healthcare system; workforce density should be compared to peer countries (not global average)

**Sector Shift Implications**:
- Public sector shortages affect access to subsidized care
- Private sector growth supports medical tourism, higher-end services
- Imbalance may require policy intervention (salary adjustments, retention bonuses)
