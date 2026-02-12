# User Story: 1 - Extract and Profile Disease Surveillance Data

**As a** healthcare data analyst,
**I want** to extract and profile 9 years of weekly infectious disease surveillance data for Dengue Fever and HFMD,
**so that** I can assess data completeness, quality, and establish a reliable foundation for forecasting analysis.

## 1. 🎯 Acceptance Criteria

1. **Data Extraction**
   - Weekly case counts extracted for all 45 diseases from `weekly-infectious-disease-bulletin-cases.csv`
   - Data covers full period: 2012-W01 to 2020-W53 (470 weeks)
   - Dengue Fever and HFMD identified as primary focus diseases
   - Data loaded into Databricks environment for analysis

2. **Data Quality Assessment**
   - 100% completeness verified (no missing values)
   - Temporal consistency confirmed (all weeks present, no gaps)
   - Data types validated (epi_week format, integer case counts)
   - Outliers and anomalies documented

3. **Data Profiling Report**
   - Summary statistics for Dengue and HFMD (mean, median, std dev, min, max)
   - Case count distributions visualized
   - Temporal coverage confirmed (2012-2020)
   - Data quality metrics documented (completeness, consistency)

4. **Disease Classification Harmonization**
   - "Hand, Foot Mouth Disease" and "HFMD" merged as single disease
   - Naming inconsistencies resolved across time periods
   - Disease totals recalculated after harmonization

## 2. 🔒 Technical Constraints

- **Data Processing Library**: Use Polars for efficient data manipulation (preferred over Pandas)
- **Platform**: Databricks (HEALIX) for collaborative notebook development
- **Language**: Python 3.7+
- **Data Source**: Kaggle dataset `subhamjain/health-dataset-complete-singapore`
- **Output Format**: Profiling report as Databricks notebook with visualizations

## 3. 📚 Domain Knowledge References

- [Infectious Disease Bulletin Data Dictionary](../../../data_dictionary/infectious_disease_bulletin.md) - Data structure and field definitions
- [Infectious Disease Epidemiology Terminology](../../../domain_knowledge/infectious-disease-epidemiology-terminology-glossary.md) - Epidemiological week system, case definitions
- [Data Sources](../../../project_context/data-sources.md) - Dataset access methods

**Key Considerations**:
- Epidemiological week format: `YYYY-Wxx` (ISO 8601 standard)
- Disease naming changes over time require harmonization
- Data quality is high (100% complete) per MOH standards

## 4. 📦 Dependencies

**External Packages**:
- `polars` - Fast DataFrame library for data manipulation
- `kagglehub` - Dataset download and access
- `matplotlib` / `seaborn` - Data visualization
- `pandas` - Secondary support if needed for specific operations

**Internal Dependencies**:
- Kaggle API authentication configured
- Databricks environment set up with required packages

## 5. ✅ Implementation Tasks

### Data Extraction
- ⬜ Configure Kaggle API credentials in Databricks
- ⬜ Download dataset using kagglehub: `weekly-infectious-disease-bulletin-cases.csv`
- ⬜ Load data into Polars DataFrame
- ⬜ Verify file size, record count (16,066 expected)

### Data Preprocessing
- ⬜ Parse `epi_week` column to extract year and week number
- ⬜ Convert `no._of_cases` to integer type
- ⬜ Standardize disease names (merge "Hand, Foot Mouth Disease" + "HFMD")
- ⬜ Create datetime column for temporal analysis

### Data Quality Validation
- ⬜ Check for missing values (expect 0%)
- ⬜ Validate temporal continuity (all weeks 2012-2020 present)
- ⬜ Identify outliers using IQR method
- ⬜ Document data quality findings

### Data Profiling
- ⬜ Calculate summary statistics for all 45 diseases
- ⬜ Generate detailed profiles for Dengue Fever and HFMD
- ⬜ Create case count distribution histograms
- ⬜ Visualize temporal coverage by disease

### Documentation
- ⬜ Create data profiling report with key findings
- ⬜ Document data quality assessment results
- ⬜ List any anomalies or concerns identified
- ⬜ Save clean dataset for subsequent analysis

## 6. Notes

**Focus Diseases Rationale**:
- **Dengue Fever**: 126,642 total cases (2nd highest burden)
- **HFMD**: 73,927 + 161,482 = 235,409 total cases (highest burden when combined)
- Both diseases show strong seasonal patterns suitable for forecasting

**Data Quality Expectation**: MOH surveillance data is high quality with 100% completeness and standardized reporting protocols. Any issues found should be documented but are not expected to block analysis.

**2020 COVID-19 Consideration**: 2020 data may show anomalies due to COVID-19 public health measures affecting disease transmission. This will be analyzed in exploratory phase.
