# MOH Healthcare Analytics Documentation Hub

**Welcome to the central documentation hub for the MOH Healthcare Policy & Operations Insights project.**

This index provides navigation to all project documentation, organized by workflow phase and purpose.

**Last Updated:** 4 February 2026  
**Project Status:** Phase 0 - Initialization Complete

---

## 📋 Quick Links

- [README (Project Overview)](../README.md)
- [Project Objectives](#project-objectives)
- [Data Dictionary](#data-dictionary)
- [Methodology & Frameworks](#methodology--frameworks)
- [Technical Stack](#technical-stack)
- [Problem Statements](#problem-statements)
- [Data Sources](#data-sources)

---

## 🎯 Project Objectives

**Location**: [`docs/objectives/`](objectives/)

Strategic goals, success metrics, and stakeholder expectations for this analytics initiative.

### Key Documents
- **Business Objectives**: Core mission and strategic goals *(See: [business-objectives.md](project_context/business-objectives.md))*
- **Success Metrics**: How we measure project success
- **Stakeholder Requirements**: Decision-maker expectations and pain points

### Quick Summary
- **Primary Goal**: Enable evidence-based healthcare policymaking
- **Target Outcomes**: 
  1. Disease outbreak detection
  2. Clinic distribution optimization
  3. Policy intervention identification
  4. Process improvement opportunities

---

## 📚 Data Dictionary

**Location**: [`docs/data_dictionary/`](data_dictionary/)

Comprehensive reference for all datasets, fields, data types, and data lineage.

### Coverage Areas
- **Healthcare Workforce** (7 tables, 2006-2019)
- **Healthcare Facilities** (4 tables, 2009-2020)
- **Health Outcomes & Mortality** (3 tables, 1990-2019)
- **Public Health & Prevention** (6 tables, 2003-2020)
- **Healthcare Utilization** (3 tables, 2006-2020)
- **Healthcare Expenditure** (1 table, 2006-2018)
- **Nutrition Surveys** (3 tables, 2004-2010)

### Primary Data Source
- **Source**: Kaggle Health Dataset (Singapore MOH Data)
- **Total Tables**: 35 CSV files
- **Data Quality**: 100% completeness
- **Reference**: [data-sources.md](project_context/data-sources.md)

---

## 🔬 Methodology & Frameworks

**Location**: [`docs/methodology/`](methodology/)

Statistical methods, analytical frameworks, and research approaches used in this project.

### Planned Methodologies
- **Time Series Analysis**: Disease outbreak detection, trend identification
- **Spatial Analysis**: Clinic distribution and accessibility mapping
- **Capacity Planning**: Utilization analysis and bottleneck identification
- **Statistical Process Control**: Quality monitoring and anomaly detection
- **Comparative Analysis**: Benchmarking across facilities and time periods

---

## 🛠️ Technical Stack

**Location**: [`docs/project_context/tech-stack.md`](project_context/tech-stack.md)

Approved technologies, platforms, and tools for this project.

### Platform Configuration
- **Environment**: HEALIX (GCC Cloud)
- **Analytics Platform**: Databricks
- **Languages**: Python, R
- **Additional Tools**: STATA

### Key Technologies
- **Data Processing**: PySpark, pandas, dplyr
- **Visualization**: matplotlib, seaborn, plotly, ggplot2
- **Statistical Analysis**: scipy, statsmodels, scikit-learn
- **Data Access**: kagglehub, Databricks SQL Connector

---

## 🎯 Problem Statements

**Location**: [`docs/problem_statements.md`](problem_statements.md)

Detailed analytics opportunities, use cases, and research questions.

### Core Problem Areas

#### 1. Disease Outbreak Detection
- **Challenge**: Early identification of potential disease outbreaks
- **Approach**: Syndromic surveillance, anomaly detection, trend analysis
- **Stakeholder Value**: Enable rapid public health response

#### 2. Clinic Visitation Distribution
- **Challenge**: Understanding capacity utilization and access patterns
- **Approach**: Spatial-temporal analysis, utilization metrics
- **Stakeholder Value**: Optimize resource allocation and accessibility

#### 3. Policy Intervention Identification
- **Challenge**: Determining where government intervention is needed
- **Approach**: Gap analysis, equity assessment, comparative benchmarking
- **Stakeholder Value**: Target policy efforts for maximum impact

#### 4. Process Improvement
- **Challenge**: Identifying bottlenecks in hospital/polyclinic workflows
- **Approach**: Process mining, wait time analysis, throughput optimization
- **Stakeholder Value**: Improve patient experience and operational efficiency

---

## 📊 Data Sources

**Location**: [`docs/project_context/data-sources.md`](project_context/data-sources.md)

Detailed information about data sources, access methods, and data acquisition processes.

### Primary Dataset
- **Name**: Singapore Health Dataset (Complete)
- **Source**: Kaggle / data.gov.sg
- **Access**: Kaggle Hub API
- **Size**: ~3.5 MB (35 tables)
- **Time Span**: 1990-2020

---

## 📁 Project Structure

### Workflow Phases

**Phase 0: Setup**
- `.env.example`, `.gitignore`, `requirements.txt`
- GitHub Actions for CI/CD

**Phase 1: Context & Understanding** (Current)
- Documentation review
- Data dictionary compilation
- Methodology definition

**Phase 2: Configuration**
- `config/` - Project parameters and settings

**Phase 3: Data Acquisition**
- `data/1_raw/` - Source data
- `data/2_external/` - Reference data
- Data validation and lineage

**Phase 4: Exploration**
- `notebooks/1_exploratory/` - EDA and profiling

**Phase 5: Analysis**
- `notebooks/2_analysis/` - Deep-dive analysis
- `src/analysis/` - Production analytics code

**Phase 6: Insights**
- `results/` - Analytical outputs
- `reports/` - Stakeholder communications

---

## 🚦 Project Status

**Current Phase**: Phase 1 - Context & Understanding  
**Last Updated**: 4 February 2026  
**Status**: Development / Setup Complete

### Next Steps
1. Complete data dictionary for all 35 tables
2. Download and validate source data
3. Begin exploratory data analysis
4. Define specific analytical methodologies

---

## 🔗 Additional Resources

### Internal Documentation
- [Tech Stack Reference](project_context/tech-stack.md)
- [Business Objectives](project_context/business-objectives.md)
- [Data Sources](project_context/data-sources.md)

### External References
- [Kaggle Dataset](https://www.kaggle.com/datasets/subhamjain/health-dataset-complete-singapore)
- [Singapore Data.gov.sg](https://data.gov.sg)
- [MOH Singapore](https://www.moh.gov.sg)

---

## 📞 Support & Contact

For questions about this documentation or the project:
- **Project Team**: MOH Analytics Team
- **Technical Issues**: Raise in project repository
- **Data Questions**: Refer to data dictionary

---

**Navigation**: [Top](#moh-healthcare-analytics-documentation-hub) | [README](../README.md)
