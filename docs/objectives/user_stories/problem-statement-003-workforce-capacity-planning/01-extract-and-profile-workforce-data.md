# User Story: 1 - Extract and Profile Healthcare Workforce Data

**As a** workforce planning analyst,
**I want** to extract and comprehensively profile healthcare workforce data for doctors, nurses/midwives, and pharmacists across public and private sectors (2006-2019),
**so that** I can establish a complete inventory of workforce trends and assess data quality before capacity analysis.

## 1. 🎯 Acceptance Criteria

1. **Complete Workforce Data Extraction**
   - Doctors dataset: 78 records (2006-2019, by sector)
   - Nurses & Midwives dataset: 126 records (2008-2019, by sector)
   - Pharmacists dataset: 42 records (2006-2019, by sector)
   - All datasets loaded successfully from Kaggle

2. **Data Profiling Completed**
   - Summary statistics for each profession (total workforce, growth rates)
   - Sector distribution analyzed (public, private, not-for-profit)
   - Temporal coverage validated (annual data, no missing years)
   - Data quality verified (100% completeness expected)

3. **Workforce Trends Visualized**
   - Time series plots showing workforce growth (2006-2019)
   - Sector breakdowns (public vs. private) over time
   - Growth rate calculations and visualizations
   - Cross-profession comparisons

4. **Data Quality Assessment**
   - Missing values checked (expect 0%)
   - Temporal consistency verified (consecutive years)
   - Outliers identified and validated
   - Any data quality issues documented

## 2. 🔒 Technical Constraints

- **Data Processing**: Polars for efficient data manipulation
- **Platform**: Databricks (HEALIX) for collaborative analysis
- **Output**: Workforce profiling report as Databricks notebook
- **Data Sources**: Three separate CSV files from Kaggle dataset

## 3. 📚 Domain Knowledge References

- [Healthcare Workforce Metrics and KPIs](../../../domain_knowledge/healthcare-workforce-metrics-kpis.md) - Workforce density, growth rates, sector distribution
- [Data Sources](../../../project_context/data-sources.md) - Kaggle dataset details and access methods

**Key Workforce Concepts**:
- **Workforce Density**: Healthcare workers per 1,000 population (WHO benchmark)
- **Sector Distribution**: Public vs. private employment patterns
- **Growth Rate**: Year-over-year percentage change in workforce
- **Public-to-Private Ratio**: Balance of workforce across sectors

## 4. 📦 Dependencies

**External Packages**:
- `polars` - Fast DataFrame operations
- `kagglehub` - Dataset download
- `matplotlib` / `seaborn` - Visualization
- `numpy` - Statistical calculations

**Internal Dependencies**:
- Kaggle API configured
- Databricks environment set up

## 5. ✅ Implementation Tasks

### Data Extraction
- ⬜ Download `number-of-doctors.csv` via kagglehub
- ⬜ Download `number-of-nurses-and-midwives.csv`
- ⬜ Download `number-of-pharmacists.csv`
- ⬜ Load all three datasets into Polars DataFrames
- ⬜ Verify record counts and schemas

### Data Profiling
- ⬜ Calculate total workforce by profession and year
- ⬜ Calculate sector breakdowns (public, private, not-for-profit)
- ⬜ Identify temporal coverage (years available per profession)
- ⬜ Calculate summary statistics (mean, median, range, growth rates)

### Data Quality Validation
- ⬜ Check for missing values (expect 0%)
- ⬜ Verify temporal continuity (no missing years)
- ⬜ Identify outliers using statistical methods
- ⬜ Validate sector totals (sum of sectors = total workforce)

### Workforce Trend Analysis
- ⬜ Calculate year-over-year growth rates for each profession
- ⬜ Calculate Compound Annual Growth Rate (CAGR) 2006-2019
- ⬜ Analyze sector shift trends (public to private migration)
- ⬜ Compare growth rates across professions

### Visualization
- ⬜ Create time series plots for total workforce (all three professions)
- ⬜ Create stacked area charts showing sector distribution over time
- ⬜ Generate growth rate comparison charts
- ⬜ Create sector migration visualizations (public-to-private ratio trends)

### Documentation
- ⬜ Write workforce profiling report with key findings
- ⬜ Document data quality assessment results
- ⬜ Highlight key trends observed (e.g., private sector growth)
- ⬜ Save clean datasets for subsequent analysis

## 6. Notes

**Expected Workforce Levels** (approximate from problem statement):
- **Doctors**: 78 records over 14 years (2006-2019)
- **Nurses & Midwives**: 126 records over 12 years (2008-2019) - started later
- **Pharmacists**: 42 records over 14 years (2006-2019)

**Data Structure**: Annual snapshots by sector (public, private, not-for-profit). Each row represents workforce count for a specific profession, year, and sector.

**Sector Trends**: Problem statement mentions migration from public to private sector over time. This should be visible in sector distribution trends.

**Data Quality**: MOH official workforce registry data expected to be high quality with 100% completeness.

**COVID-19 Note**: Data ends in 2019, so COVID-19 workforce impacts (2020+) not captured. This is a known limitation.

**Profession Coverage**: Limited to three professions (doctors, nurses, pharmacists). Allied health professionals, technicians, and support staff not included in this dataset.
