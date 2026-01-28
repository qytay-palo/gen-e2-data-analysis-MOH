# MOH Polyclinic Queue Optimization & Visitation Analysis - Documentation Hub

## Project Overview

**Objective**: Analyze polyclinic visitation patterns across time and location to design effective queue management systems.

**Key Stakeholders**: 
- **Patients**: Improved wait times and service experience
- **CEO/Leadership**: Data-driven operational insights and resource optimization

**Platform**: HEALIX (GCC Databricks) | **Languages**: Python, R, STATA

---

## 🎯 Project Objectives

### Primary Goals
- [ML & Analytics Opportunities](objectives/opportunities.md) - Machine learning and analytical approaches
- Problem framing, modeling methods, and evaluation metrics
- Temporal and geographic analysis strategies

---

## 📊 Data Documentation

### Data Sources & Context
- [Data Sources](project_context/data_sources.md) - MOH polyclinic data via API (complete schema)
- [Tech Stack](project_context/tech_stack.md) - Approved technologies and platform specifications

---

## 🔬 Analysis Focus Areas

### 1. Temporal Pattern Analysis
- **Objectives**: Understand how visitation varies by time
- **Methods**: Time-series decomposition, seasonality analysis, trend detection
- **Deliverables**: Peak hour identification, seasonal forecasts, demand curves

### 2. Geographic Analysis
- **Objectives**: Understand spatial demand distribution
- **Methods**: Geographic clustering, catchment analysis, accessibility metrics
- **Deliverables**: Regional demand maps, facility utilization rates, equity analysis

### 3. Queue Optimization
- **Objectives**: Design effective queue management systems
- **Methods**: Queuing theory, discrete-event simulation, optimization algorithms
- **Deliverables**: Wait time reduction strategies, capacity planning recommendations

### 4. Predictive Modeling
- **Objectives**: Forecast future demand and optimize resources
- **Methods**: Time-series forecasting (ARIMA, Prophet), ML regression, ensemble methods
- **Deliverables**: Demand forecasts, resource allocation models, scenario planning tools

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
