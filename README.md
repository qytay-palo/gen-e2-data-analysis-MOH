# MOH Infectious Disease Temporal Analysis & Forecasting

**Project Status:** 🟢 Active Development (Phase 1)  
**Last Updated:** 9 February 2026  
**Platform:** HEALIX/Databricks  
**Language:** Python 3.9+

---

## 📋 Project Overview

This data analytics project analyzes **9 years of weekly infectious disease surveillance data** (2012-2020) from Singapore's Ministry of Health to:

1. **Identify seasonal patterns** across 45 infectious diseases
2. **Forecast outbreak periods** 8-12 weeks in advance for high-burden diseases (Dengue, HFMD)
3. **Rank disease burden** to prioritize resource allocation
4. **Optimize public health resources** through proactive planning

### Business Impact

**Target Stakeholders:**
- MOH Policy Makers (budget allocation, strategic planning)
- Healthcare Facility Committees (operational planning, staff scheduling)
- Public Health Surveillance Teams (outbreak response)

**Expected Outcomes:**
- Proactive vs reactive resource deployment
- Improved outbreak response times (target: 20% faster)
- Evidence-based policy decisions for program funding
- Optimized healthcare capacity during predictable disease peaks

---

## 🎯 Project Objectives

### 1. Temporal Pattern Analysis
Identify which diseases exhibit strong seasonal patterns and when they peak

**Key Deliverable:** Seasonal disease calendar showing high-risk periods

### 2. Outbreak Forecasting
Predict future case volumes with 70%+ accuracy for Dengue Fever and HFMD

**Key Deliverable:** 8-12 week ahead forecasts with confidence intervals

### 3. Disease Burden Assessment
Rank all 45 diseases by case volume, growth rate, and outbreak frequency

**Key Deliverable:** Prioritized disease list for resource allocation

### 4. Resource Optimization
Provide evidence-based recommendations for allocating resources across disease programs

**Key Deliverable:** Decision matrix and budget allocation framework

---

## 📊 Data Sources

### Primary Dataset: Weekly Infectious Disease Bulletin
- **Source:** Ministry of Health Singapore (via Kaggle)
- **Dataset ID:** `subhamjain/health-dataset-complete-singapore`
- **Coverage:** 2012-2020 (470 weeks)
- **Records:** 16,066 weekly case counts across 45 diseases
- **Key Diseases:**
  - Dengue Fever: 126,642 total cases
  - HFMD (Hand, Foot, Mouth Disease): 73,927+ cases
  - Salmonellosis: 16,497 cases
  - Mumps: 4,213 cases

**Data Quality:** ✅ Complete (no missing values), consistent weekly reporting

See [Data Sources Documentation](docs/project_context/data-sources.md) for details.

---

## 🏗️ Project Structure

```
.
├── README.md                # This file
├── requirements.txt         # Python dependencies
├── environment.yml          # Conda environment specification
├── pyproject.toml           # Project metadata and build configuration
│
├── .gitignore               # Version control exclusions
├── .env.example             # Template for environment variables
│
├── config/                  # 📝 Configuration Files
│   ├── auto_analysis.yml    # Automated analysis settings
│   ├── data_sources.yml     # Data source configurations
│   ├── databricks.yml       # HEALIX/Databricks settings
│   └── logging.yml          # Logging configuration
│
├── docs/                    # 📚 Documentation
│   ├── index.md             # Documentation hub
│   ├── problem_statements.md # Analytics opportunities
│   ├── project_context/     # Business context
│   │   ├── business-objectives.md
│   │   ├── data-sources.md
│   │   └── tech-stack.md
│   ├── objectives/          # Feature objectives
│   │   └── infectious_disease_temporal_analysis.md
│   └── data_dictionary/     # Data schemas and definitions
│
├── data/                    # 💾 Data Storage
│   ├── 1_raw/               # Original immutable source data
│   ├── 2_external/          # External reference data
│   ├── 3_interim/           # Intermediate transformation outputs
│   ├── 4_processed/         # Final cleaned datasets (analysis-ready)
│   └── schemas/             # Data contracts and lineage
│
├── notebooks/               # 📓 Interactive Analysis
│   ├── 1_exploratory/       # Initial EDA, data profiling
│   ├── 2_analysis/          # Deep-dive analysis, insights
│   │   └── automated_analysis_demo.ipynb
│   └── 3_feature_engineering/ # Feature creation
│
├── src/                     # 🐍 Production Code
│   ├── data_processing/     # ETL, cleaning, validation
│   ├── features/            # Feature engineering
│   ├── analysis/            # Statistical analysis algorithms
│   ├── visualization/       # Chart generation, plotting
│   ├── models/              # Model training, tuning
│   └── utils/               # Helper functions
│       ├── config_loader.py
│       └── logger.py
│
├── scripts/                 # ⚙️ Automation Scripts
│   ├── explore_infectious_disease_data.py  # Kaggle dataset exploration
│   ├── analyze_infectious_disease_scope.py # Data scope analysis
│   ├── auto_analyze.py      # Automated analysis runner
│   └── run_scheduled_analysis.py
│
├── tests/                   # 🧪 Quality Assurance
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── data/                # Data validation tests
│
├── models/                  # 🤖 Trained Models
│   └── *.pkl, *.joblib      # Serialized model artifacts
│
├── results/                 # 📈 Analysis Outputs
│   ├── tables/              # Summary statistics (CSV/Excel)
│   ├── metrics/             # Performance KPIs (JSON/CSV)
│   └── exports/             # Stakeholder-ready exports
│
├── reports/                 # 📄 Stakeholder Communication
│   ├── figures/             # Static visualizations (PNG/PDF)
│   ├── dashboards/          # Interactive dashboards (HTML)
│   └── presentations/       # Executive summaries (PPTX/PDF)
│
├── logs/                    # 📝 Execution Logs
│   ├── etl/                 # ETL pipeline logs
│   ├── errors/              # Error logs and stack traces
│   └── audit/               # Audit trails
│
└── sql/                     # 🗄️ SQL Queries (if using databases)
    ├── views/               # SQL views
    ├── procedures/          # Stored procedures
    └── extractions/         # Data extraction queries
```

---

## 🚀 Quick Start

### Prerequisites

- **Python:** 3.9 or higher
- **Conda:** Recommended for environment management
- **Kaggle Account:** For dataset access
- **HEALIX/Databricks:** Access credentials (for production deployment)

### 1. Clone Repository

```bash
git clone https://github.com/your-org/gen-e2-data-analysis-MOH.git
cd gen-e2-data-analysis-MOH
```

### 2. Set Up Environment

**Option A: Using Conda (Recommended)**
```bash
conda env create -f environment.yml
conda activate moh-infectious-disease
```

**Option B: Using venv**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Kaggle API

**Generate API Key:**
1. Log in to Kaggle → Account Settings
2. Click "Create New API Token"
3. Download `kaggle.json`

**Install API Key:**
```bash
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

### 4. Explore the Data

```bash
# Analyze infectious disease data scope
python3 scripts/analyze_infectious_disease_scope.py
```

**Output:**
- Disease coverage summary
- Temporal span analysis
- Priority diseases for forecasting
- Saved results in `data/infectious_disease_scope.json`

### 5. Run Exploratory Analysis

```bash
# Launch Jupyter Lab
jupyter lab

# Open: notebooks/1_exploratory/
```

---

## 📦 Dependencies

### Core Libraries

**Data Processing:**
- pandas >= 2.0.0
- numpy >= 1.24.0
- polars >= 0.17.0 (optional, for large datasets)

**Time Series Analysis:**
- statsmodels >= 0.14.0
- prophet >= 1.1.0
- pmdarima >= 2.0.0

**Machine Learning:**
- scikit-learn >= 1.2.0
- xgboost >= 1.7.0
- mlflow >= 2.3.0

**Visualization:**
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- plotly >= 5.14.0

**Data Acquisition:**
- kagglehub >= 0.2.0

**Platform:**
- pyspark >= 3.3.0 (Databricks)
- databricks-connect (for local development)

See [requirements.txt](requirements.txt) for complete list.

---

## 🔧 Configuration

### Environment Variables

Create `.env` file (copy from `.env.example`):

```bash
# Kaggle API
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_api_key

# Databricks (HEALIX)
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=your_token

# Project Settings
PROJECT_ENV=development  # or: staging, production
LOG_LEVEL=INFO
```

### Configuration Files

- **`config/data_sources.yml`**: Dataset connections
- **`config/databricks.yml`**: Platform settings
- **`config/logging.yml`**: Logging configuration
- **`config/auto_analysis.yml`**: Automated analysis parameters

---

## 📈 Usage Examples

### Load Infectious Disease Data

```python
import kagglehub
import pandas as pd
from pathlib import Path

# Download dataset
dataset_path = kagglehub.dataset_download(
    "subhamjain/health-dataset-complete-singapore"
)

# Load infectious disease data
disease_file = Path(dataset_path) / "weekly-infectious-disease-bulletin-cases" / "weekly-infectious-disease-bulletin-cases.csv"
df = pd.read_csv(disease_file)

# Preview
print(df.head())
print(f"Total records: {len(df):,}")
print(f"Diseases tracked: {df['disease'].nunique()}")
```

### Analyze Seasonal Patterns

```python
from src.analysis.temporal_patterns import SeasonalAnalyzer

# Initialize analyzer
analyzer = SeasonalAnalyzer(df)

# Identify seasonal diseases
seasonal_diseases = analyzer.detect_seasonality(
    p_value_threshold=0.05,
    min_observations=100
)

# Visualize Dengue Fever seasonality
analyzer.plot_seasonal_decomposition("Dengue Fever")
```

### Forecast Future Cases

```python
from src.models.forecasting import DiseaseForecaster

# Train forecasting model
forecaster = DiseaseForecaster(method='prophet')
forecaster.fit(df, disease="Dengue Fever")

# Generate 12-week forecast
forecast = forecaster.predict(horizon=12, include_confidence=True)

# Visualize
forecaster.plot_forecast(forecast)
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run unit tests only
pytest tests/unit/

# Run with coverage
pytest --cov=src tests/
```

---

## 📝 Documentation

- **[Project Context](docs/project_context/)**: Business objectives, data sources, tech stack
- **[Objectives](docs/objectives/)**: Detailed feature specifications
- **[Problem Statements](docs/problem_statements.md)**: Analytics opportunities
- **[Data Dictionary](docs/data_dictionary/)**: Schemas, field definitions
- **[Index](docs/index.md)**: Documentation navigation hub

---

## 🗺️ Project Roadmap

### ✅ Phase 0: Setup & Discovery (Week 1-2)
- [x] Data source identification
- [x] Scope definition
- [x] Environment setup
- [x] Documentation structure

### 🚧 Phase 1: Foundation (Week 3-5)
- [ ] Data extraction pipeline
- [ ] Quality assessment & validation
- [ ] Exploratory data analysis
- [ ] Seasonal pattern identification

### 📅 Phase 2: Modeling (Week 6-8)
- [ ] Forecasting model development
- [ ] Model validation & tuning
- [ ] Disease burden analysis
- [ ] Statistical significance testing

### 📅 Phase 3: Insights & Tools (Week 9-12)
- [ ] Resource allocation framework
- [ ] Interactive dashboard
- [ ] Executive reports & policy briefs
- [ ] Stakeholder presentations

---

## 👥 Team & Contributors

**Project Lead:** Data Analytics Team, MOH  
**Stakeholders:** 
- MOH Policy Makers
- Healthcare Facility Committees
- Public Health Surveillance Teams

**Technical Contributors:** [Add team members]

---

## 📄 License

[Specify license - typically internal/proprietary for government projects]

---

## 🔗 Related Resources

- **MOH Website:** https://www.moh.gov.sg/
- **Data Source (Kaggle):** https://www.kaggle.com/datasets/subhamjain/health-dataset-complete-singapore
- **HEALIX Platform:** [Internal documentation]

---

## 📞 Contact & Support

**Project Email:** [project-email@moh.gov.sg]  
**Documentation Issues:** Open an issue in this repository  
**Technical Support:** [Contact internal support team]

---

**Last Updated:** 9 February 2026  
**Version:** 1.0.0  
**Status:** 🟢 Active Development
