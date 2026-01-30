# MOH Polyclinic Patient Analysis & Policy Intelligence - Documentation Hub

## Project Overview

**Objective**: Analyze and understand polyclinic patient populations (demographics, distribution, temporal trends) to identify healthcare problems requiring policy intervention and governance.

### Main Goals
- **Understand Patient Population**: Comprehensive analysis of patient demographics, distribution patterns, and temporal trends across Singapore polyclinics
- **Identify Policy Intervention Needs**: Detect healthcare problems, service gaps, and governance issues requiring regulatory or policy intervention

### Measurable Success Criteria
- **Patient Understanding**: Complete demographic profiling covering 100% of polyclinic patients with distribution analysis by age, gender, ethnicity, and socioeconomic status
- **Trend Detection**: Identify and quantify temporal trends in disease prevalence, service utilization, and patient access patterns
- **Policy Problem Identification**: Detect and prioritize at least 5 high-impact policy intervention opportunities with quantified impact assessments
- **Evidence Quality**: Deliver statistically significant findings with confidence intervals for all key metrics

### Business Decisions Informed
- **Policy Development**: Evidence-based healthcare policies, regulatory interventions, and governance frameworks
- **Resource Allocation**: Strategic planning for polyclinic capacity, staffing, and service distribution
- **Health Equity**: Targeted interventions to address geographic and demographic healthcare disparities
- **Program Effectiveness**: Assessment of existing healthcare initiatives (e.g., Healthier SG program)

**Key Stakeholders**: 
- **Government Agencies**: Ministry of Health policy makers, healthcare regulators, and public health officials requiring evidence for governance decisions
- **Business Decision Makers**: Healthcare administrators, hospital executives, and operational leaders requiring strategic insights for planning and resource allocation

**Platform**: HEALIX (GCC Databricks) | **Languages**: Python, R, STATA

---

## 🎯 Project Objectives

### Primary Goals
- [Analytics Opportunities Overview](objectives/opportunities.md) - Machine learning and analytical approaches
- Problem framing, modeling methods, and evaluation metrics
- Temporal and geographic analysis strategies

### Strategic Epics
**Policy-Driven Analytics Initiatives** (Prioritized by Impact & Feasibility)

1. **[EPIC-001: Patient Population Segmentation](objectives/epics/epic-001-patient-segmentation.md)** ⭐ CRITICAL
   - Comprehensive demographic profiling and patient segmentation
   - Complexity: MEDIUM | Duration: 4-6 weeks
   - **Foundation epic** - Required for downstream analyses

2. **[EPIC-002: Temporal Trend Detection](objectives/epics/epic-002-temporal-trends.md)** ⭐ HIGH
   - Disease prevalence trends and healthcare utilization patterns (2015-2026)
   - Complexity: HIGH | Duration: 6-8 weeks
   - Depends on: EPIC-001

3. **[EPIC-003: Geographic Health Equity Analysis](objectives/epics/epic-003-geographic-equity.md)** ⭐ CRITICAL
   - Spatial accessibility, disparity quantification, and underserved area identification
   - Complexity: MEDIUM-HIGH | Duration: 5-7 weeks
   - Independent - Can run in parallel

---

## 📊 Data Documentation

### Data Sources & Context
- [Data Sources Overview](project_context/data_sources.md) - Complete schema documentation for all MOH polyclinic tables
- [Tech Stack Specifications](project_context/tech_stack.md) - Approved technologies (HEALIX/Databricks, Python, R, STATA)
- [Data Connections Guide](project_context/data_connections.md) - API and database connectivity

### Data Dictionary (Comprehensive)
- **[Master Index](data_dictionary/00_master_index.md)** - Complete data dictionary navigation
- [Patient Demographics Table](data_dictionary/06_patient_demographics.md) - Demographic information, segmentation fields
- [Polyclinic Attendances Table](data_dictionary/01_polyclinic_attendances.md) - Visit records, waiting times, operational metrics
- Additional tables: Diagnoses, Procedures, Medications, Lab Results, Polyclinic Master (see Master Index)

---

## 🔬 Analysis Focus Areas

### 1. Patient Demographics & Distribution Analysis
- **Objectives**: Understand patient population characteristics and distribution patterns
- **Methods**: Descriptive statistics, cohort analysis, demographic segmentation
- **Deliverables**: Patient profiles, population pyramids, socioeconomic distributions

### 2. Disease Burden & Health Trends
- **Objectives**: Analyze chronic disease prevalence, comorbidities, and temporal trends
- **Methods**: Epidemiological analysis, time-series trend detection, disease clustering
- **Deliverables**: Disease prevalence reports, trend forecasts, risk stratification models

### 3. Geographic Health Equity Analysis
- **Objectives**: Identify regional disparities and access gaps requiring policy intervention
- **Methods**: Spatial analysis, equity metrics, accessibility modeling
- **Deliverables**: Health equity maps, underserved area identification, disparity quantification

### 4. Policy Problem Identification
- **Objectives**: Detect healthcare problems and gaps requiring regulatory intervention
- **Methods**: Outlier detection, pattern recognition, comparative benchmarking
- **Deliverables**: Policy recommendations, intervention priorities, evidence briefs for government

---

## 🚀 Quick Start Guide

1. **Setup Environment**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Access**
   - Edit `config/database.yml` with API credentials
   - Set up query parameters in `config/queries.yml`

3. **Extract Data**
   ```bash
   python scripts/run_extraction.py --sources attendances --last-n-days 30
   ```

4. **Start Analysis**
   - Open `notebooks/1_exploratory/` in Jupyter
   - Review exploratory data analysis templates

5. **Review Opportunities**
   - Read [ML Opportunities](objectives/opportunities.md) for modeling approaches
   - Check [Data Sources](project_context/data_sources.md) for schema details

---

## 📚 Key Documentation

- **[README.md](../README.md)** - Project overview and setup instructions
- **[ML Opportunities](objectives/opportunities.md)** - Detailed analysis and modeling approaches
- **[Data Sources](project_context/data_sources.md)** - Complete data dictionary with 15+ tables
- **[Tech Stack](project_context/tech_stack.md)** - Platform and tool specifications

---

**Platform**: HEALIX (GCC Databricks)  
**Last Updated**: January 2026  
**Status**: Phase 1 - Project Initialization

---

## 📁 Project Workflow

### Phase 1: Context & Understanding (CURRENT)
**Directory**: `docs/`
- Review project objectives and ML opportunities
- Understand data sources and schemas
- Set up technical environment

### Phase 2: Configuration
**Directory**: `config/`
- API connection setup (`database.yml`)
- Query templates and parameters (`queries.yml`)
- Environment variables and secrets

### Phase 3: Data Acquisition
**Directory**: `data/`
- `1_raw/` - Original API extractions (immutable)
- `2_external/` - External reference data (demographics, benchmarks)
- `3_interim/` - Intermediate transformations
- `4_processed/` - Final analysis-ready datasets

### Phase 4: Exploratory Analysis
**Directory**: `notebooks/`
- `1_exploratory/` - Initial EDA, data profiling, hypothesis generation
- `2_analysis/` - Deep-dive temporal and geographic analysis
- `3_feature_engineering/` - Feature creation for modeling

### Phase 5: Production Code
**Directory**: `src/`
- `data_processing/` - ETL pipelines and data extraction
- `features/` - Feature engineering modules
- `analysis/` - Statistical analysis (temporal patterns, geographic clustering)
- `models/` - ML model training (demand forecasting, queue optimization)
- `visualization/` - Plotting functions and dashboard generation
- `utils/` - Helper utilities and logging

### Phase 6: Quality Assurance
**Directory**: `tests/`
- Unit tests for data processing functions
- Integration tests for ETL pipelines
- Data validation tests

### Phase 7: Model Artifacts
**Directory**: `models/`
- Trained forecasting models
- Queue simulation parameters
- Serialized model objects (.pkl, .joblib)

### Phase 8: Analysis Results
**Directory**: `results/`
- `tables/` - Summary statistics, analytical tables (CSV/Excel)
- `metrics/` - Performance KPIs (wait times, capacity utilization)
- `exports/` - Stakeholder-ready data exports

### Phase 9: Stakeholder Deliverables
**Directory**: `reports/`
- `figures/` - Static visualizations (PNG/PDF)
- `dashboards/` - Interactive dashboards (Plotly, Streamlit)
- `presentations/` - Executive summaries (PPTX/PDF)

### Phase 10: Automation
**Directory**: `scripts/`
- `run_extraction.py` - Data extraction automation
- `run_scheduler.py` - Scheduled job orchestration

---

## 🛠️ Technical Documentation

### Configuration
- [Configuration Guide](../config/README.md) - Project configuration and parameters
- [Environment Setup](setup.md) - Development environment setup instructions

### Code Documentation
- [API Reference](api_reference.md) - Source code API documentation
- [Testing Guide](../tests/README.md) - Unit and integration testing documentation

---

## 🤖 AI-Assisted Analysis

### Prompts & Instructions
- [GitHub Copilot Instructions](../.github/instructions/README.md) - AI assistant guidelines
- [Analysis Prompts](../.github/prompts/README.md) - Prompt templates for data analysis

---

## 📝 Change Log & Updates

- [Project Change Log](changelog.md) - Track major changes and updates
- [Version History](version_history.md) - Release notes and versioning

---

## 🔗 Quick Links

- [Main README](../README.md) - Project overview and quick start
- [Contributing Guidelines](contributing.md) - How to contribute to this project
- [Contact Information](contacts.md) - Team contacts and support

---

*Last updated: 23 January 2026*
