# MOH Healthcare Analytics: Policy & Operations Insights

**Project Type:** Healthcare Data Analysis  
**Platform:** HEALIX/Databricks (GCC Cloud Environment)  
**Languages:** Python, R, SQL  
**Last Updated:** 4 February 2026  
**Status:** Active Development - Phase 0 (Initialization)

---

## 🎯 Project Overview

This project analyzes Singapore's healthcare system data to support evidence-based policymaking and operational improvements across polyclinics and hospitals. The analysis focuses on identifying bottlenecks, intervention opportunities, and process improvements to ensure accessible, efficient, and sustainable healthcare delivery.

### Key Outcomes

1. **Disease Outbreak Detection**: Identify potential disease outbreaks through syndromic surveillance and trend analysis
2. **Clinic Visitation Distribution**: Understand visitation patterns and capacity utilization across polyclinics and healthcare facilities
3. **Policy Intervention Identification**: Identify areas requiring government intervention or policy implementation
4. **Healthcare Process Optimization**: Analyze potential improvements in hospitalization and polyclinic user processes

### Success Metrics

The project's success will be measured by:
- ✅ **Bottleneck Identification**: Pinpoint operational bottlenecks in patient flow, resource allocation, and service delivery
- ✅ **Intervention Opportunities**: Identify specific areas where government intervention is needed
- ✅ **Improvement Opportunities**: Discover actionable opportunities for process and service improvements
- ✅ **Evidence-Based Decision Making**: Enable data-driven policy decisions with comprehensive insights

### Stakeholders

- **Primary Audience**: 
  - MOH Business Decision Makers
  - MOH Policy Makers
- **Expected Impact**: Support comprehensive, well-rounded policy decisions with data-driven evidence

---

## 🗂️ Project Structure

```
.
├── .env.example          # Environment variables template (credentials, API keys)
├── .gitignore            # Git exclusions
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── environment.yml       # Conda environment specification
│
├── .github/              # CI/CD and automation
│   └── workflows/
│       ├── data_quality_checks.yml
│       └── scheduled_extraction.yml
│
├── docs/                 # 📚 Documentation & Context
│   ├── index.md          # Documentation navigation hub
│   ├── objectives/       # Project goals and success criteria
│   ├── data_dictionary/  # Data schemas, field definitions, lineage
│   ├── methodology/      # Statistical methods, analytical frameworks
│   └── project_context/  # Business context, tech stack, data sources
│
├── config/               # ⚙️ Configuration Files
│   ├── databricks.yml    # Databricks cluster and job configs
│   ├── data_sources.yml  # Data connection configurations
│   └── logging.yml       # Logging configuration
│
├── sql/                  # 🗄️ Database Scripts
│   ├── views/            # SQL views for common queries
│   ├── procedures/       # Stored procedures
│   └── extractions/      # Data extraction queries
│
├── data/                 # 📊 Data Pipeline
│   ├── 1_raw/            # Original immutable source data
│   ├── 2_external/       # External reference data
│   ├── 3_interim/        # Intermediate transformation outputs
│   ├── 4_processed/      # Final analysis-ready datasets
│   └── schemas/          # Data schemas and lineage docs
│
├── notebooks/            # 📓 Interactive Analysis
│   ├── 1_exploratory/    # EDA, data profiling, hypothesis generation
│   ├── 2_analysis/       # Deep-dive analysis, insights documentation
│   └── 3_feature_engineering/  # Feature creation, transformations
│
├── src/                  # 🔧 Production Code
│   ├── utils/            # Helper functions, common utilities
│   ├── data_processing/  # ETL, cleaning, validation
│   ├── features/         # Feature engineering
│   ├── analysis/         # Statistical analysis algorithms
│   ├── visualization/    # Chart generation, plotting utilities
│   └── models/           # Model training, hyperparameter tuning
│
├── tests/                # ✅ Quality Assurance
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── data/             # Data validation tests
│
├── models/               # 🤖 Model Artifacts
│   └── *.pkl, *.joblib   # Trained models, serialized objects
│
├── results/              # 📈 Analysis Outputs
│   ├── tables/           # Summary statistics, analytical tables
│   ├── metrics/          # Performance KPIs, evaluation metrics
│   └── exports/          # Stakeholder-ready data exports
│
├── reports/              # 📑 Stakeholder Communication
│   ├── figures/          # Static visualizations (PNG/PDF)
│   ├── dashboards/       # Interactive dashboards (HTML/Streamlit)
│   └── presentations/    # Executive summaries (PPTX/PDF)
│
├── logs/                 # 📝 Execution Logs
│   ├── etl/              # ETL pipeline logs
│   ├── errors/           # Error logs and stack traces
│   └── audit/            # Data access and change audit trails
│
└── scripts/              # 🚀 Automation & Deployment
    └── *.py, *.sh        # End-to-end pipelines, automation scripts
```

---

## 🛠️ Technical Stack

### Platform
- **Cloud Environment**: HEALIX (GCC-Compliant)
- **Analytics Platform**: Databricks
- **Languages**: Python, R
- **Additional Tools**: STATA (statistical analysis)

### Key Libraries (Python)
- **Data Processing**: pandas, numpy, pyspark
- **Visualization**: matplotlib, seaborn, plotly
- **Statistical Analysis**: scipy, statsmodels, scikit-learn
- **Data Access**: kagglehub, databricks-sql-connector

### Data Sources
- **Primary**: Kaggle Health Dataset (Singapore MOH Data)
  - 35 data tables covering healthcare facilities, workforce, utilization, outcomes
  - Time span: 1990-2020
  - Source: data.gov.sg via Kaggle

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Access to HEALIX/Databricks workspace
- Kaggle API credentials (for data download)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gen-e2-data-analysis-MOH
   ```

2. **Set up Python environment**
   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # Using conda
   conda env create -f environment.yml
   conda activate moh-analytics
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Download data**
   ```bash
   python scripts/download_data.py
   ```

---

## 📊 Analysis Workflow

### Phase 1: Context & Understanding
1. Review business objectives and success criteria
2. Study data dictionary and source documentation
3. Understand analytical methodology and frameworks

### Phase 2: Data Acquisition
1. Extract data from Kaggle dataset
2. Validate data quality and completeness
3. Document data lineage and transformations

### Phase 3: Exploratory Analysis
1. Profile data distributions and patterns
2. Identify data quality issues
3. Generate initial hypotheses

### Phase 4: Deep Analysis
1. Disease outbreak pattern analysis
2. Clinic visitation and capacity analysis
3. Process bottleneck identification
4. Policy intervention opportunity mapping

### Phase 5: Insights & Recommendations
1. Synthesize findings into actionable insights
2. Create visualizations and dashboards
3. Prepare stakeholder presentations

---

## 🔐 Security & Compliance

- **GCC Compliance**: All analysis conducted on HEALIX platform
- **Data Privacy**: Aggregate data only, no personally identifiable information
- **Access Control**: Role-based access to sensitive data
- **Audit Trails**: All data access and transformations logged

---

## 📖 Documentation

Comprehensive documentation available in [`docs/index.md`](docs/index.md):
- [Business Objectives](docs/objectives/)
- [Data Dictionary](docs/data_dictionary/)
- [Methodology](docs/methodology/)
- [Technical Stack](docs/project_context/tech-stack.md)
- [Data Sources](docs/project_context/data-sources.md)

---

## 🤝 Contributing

1. Create a feature branch
2. Make your changes with appropriate tests
3. Run code quality checks (`black`, `flake8`, `mypy`)
4. Submit a pull request

---

## 📞 Contact & Support

For questions or support, contact the MOH Analytics Team.

**Project Maintainers**: [Your Team]  
**Last Updated**: 4 February 2026
