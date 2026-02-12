# MOH Infectious Disease Analytics Documentation Hub

**Welcome to the central documentation hub for the MOH Infectious Disease Temporal Analysis & Forecasting project.**

This index provides navigation to all project documentation, organized by workflow phase and purpose.

**Last Updated:** 9 February 2026  
**Project Status:** Phase 1 - Active Development  
**Focus:** Seasonal pattern analysis, outbreak forecasting, and resource optimization

---

## 📋 Quick Links

- [README (Project Overview)](../README.md)
- [Project Objectives](#project-objectives)
- [Data Dictionary](#data-dictionary)
- [Problem Statements](#problem-statements)
- [Data Sources](#data-sources)
- [Technical Stack](#technical-stack)
- [TODO List](../TODO.md)

---

## 🎯 Project Objectives

**Location**: [`docs/objectives/`](objectives/)

Strategic goals, success metrics, and stakeholder expectations for infectious disease analysis.

### Key Documents
- **[Infectious Disease Temporal Analysis](objectives/infectious_disease_temporal_analysis.md)**: Primary feature objectives
- **[Business Objectives](project_context/business-objectives.md)**: MOH strategic goals and mission

### Project Focus Areas
1. **Temporal Pattern Analysis**: Identify seasonal trends in 45 infectious diseases
2. **Outbreak Forecasting**: Predict case volumes 8-12 weeks ahead for Dengue, HFMD
3. **Disease Burden Assessment**: Rank diseases for resource prioritization
4. **Resource Optimization**: Evidence-based allocation recommendations

### Success Metrics
- ✓ Seasonal patterns identified for ≥3 diseases (p < 0.05)
- ✓ Forecasting accuracy ≥70% (MAPE)
- ✓ Disease burden ranking completed for all 45 diseases
- ✓ Stakeholder adoption: ≥50% of facilities use forecasts

---

## 📚 Data Dictionary

**Location**: [`docs/data_dictionary/`](data_dictionary/)

Comprehensive reference for infectious disease datasets, fields, and data quality.

### Primary Dataset
**[Weekly Infectious Disease Bulletin](data_dictionary/infectious_disease_bulletin.md)**
- **Period**: 2012-2020 (470 weeks)
- **Records**: 16,066 weekly case counts
- **Diseases**: 45 notifiable infectious diseases
- **Data Quality**: 100% complete, no missing values

### Top Diseases by Case Volume:
| Disease | Total Cases (2012-2020) |
|---------|-------------------------|
| Hand, Foot Mouth Disease + HFMD | 235,409 |
| Dengue Fever | 126,642 |
| Salmonellosis | 16,497 |
| Mumps | 4,213 |

### Additional Documentation
- **[Data Sources](project_context/data-sources.md)**: Kaggle API access, ETL pipelines
- **[Comprehensive Data Catalog](data_dictionary/COMPREHENSIVE_DATA_CATALOG.md)**: Full MOH dataset reference
- **[Table Quick Reference](data_dictionary/TABLE_QUICK_REFERENCE.md)**: Fast lookup guide

---

## 🔍 Problem Statements

**Location**: [`docs/problem_statements.md`](problem_statements.md)

Analytics opportunities and research questions driving this project.

### Key Problem Areas
1. **Infectious Disease Seasonal Analysis** (Primary Focus)
   - Which diseases show strong seasonal patterns?
   - Can we forecast outbreaks 8-12 weeks in advance?
   - How should resources be allocated across disease programs?

2. **Disease Outbreak Detection** (Related)
   - Early warning systems for potential outbreaks
   - Syndromic surveillance approaches

3. **Healthcare Capacity Planning** (Related)
   - Seasonal demand forecasting for hospital resources
   - Staff scheduling optimization

### Target Stakeholders
- **MOH Policy Makers**: Budget allocation, strategic planning
- **Healthcare Facility Committees**: Operational planning, resource management
- **Public Health Surveillance Teams**: Outbreak response, monitoring

---

## 📊 Data Sources

**Location**: [`docs/project_context/data-sources.md`](project_context/data-sources.md)

Detailed documentation of data access, authentication, and integration points.

### Primary Source
- **Dataset**: Kaggle Health Dataset (Singapore)
- **ID**: `subhamjain/health-dataset-complete-singapore`
- **Access**: Kaggle Hub API
- **Original Source**: Ministry of Health Singapore (data.gov.sg)

### Authentication Setup
```bash
# Install Kaggle API key
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

### Quick Data Load
```python
import kagglehub
dataset_path = kagglehub.dataset_download(
    "subhamjain/health-dataset-complete-singapore"
)
```

---

## 🛠️ Technical Stack

**Location**: [`docs/project_context/tech-stack.md`](project_context/tech-stack.md)

Approved technologies, platforms, and tools for this project.

### Platform Configuration
- **Environment**: HEALIX/Databricks (GCC Cloud)
- **Primary Language**: Python 3.9+
- **Version Control**: Git/GitHub

### Key Technologies

**Data Processing:**
- pandas 2.1.4, numpy 1.26.2
- PySpark 3.5.0 (Databricks)

**Time Series & Forecasting:**
- statsmodels 0.14.1 (SARIMA, seasonal decomposition)
- prophet 1.1.5 (Facebook forecasting)
- pmdarima 2.0.4 (Auto ARIMA)
- xgboost 2.0.3 (ML forecasting)

**Visualization:**
- matplotlib 3.8.2, seaborn 0.13.0
- plotly 5.18.0, dash 2.14.2

**ML & Tracking:**
- scikit-learn 1.3.2
- mlflow 2.9.2

**Data Access:**
- kagglehub 0.2.9

See [`requirements.txt`](../requirements.txt) for complete dependencies.

---

## 📖 Methodology & Frameworks

**Location**: [`docs/methodology/`](methodology/)

Statistical methods and analytical frameworks for infectious disease analysis.

### Planned Methodologies

**Time Series Analysis:**
- Seasonal decomposition (trend, seasonality, residuals)
- Autocorrelation analysis (ACF/PACF)
- Spectral analysis for periodicity detection
- Statistical significance testing (Mann-Kendall, Kruskal-Wallis)

**Forecasting Approaches:**
- SARIMA (Seasonal ARIMA) models
- Prophet (business time series with seasonality)
- XGBoost with lagged features
- Ensemble methods for robust predictions

**Burden Assessment:**
- Multi-metric disease ranking (volume, growth, outbreak frequency)
- Trend analysis (2012-2020 evolution)
- Severity weighting (where data available)

**Resource Optimization:**
- Decision matrix for allocation
- Cost-benefit analysis of intervention timing
- Scenario planning tools

---

## 🚀 Getting Started

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/your-org/gen-e2-data-analysis-MOH.git
cd gen-e2-data-analysis-MOH

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Kaggle API
```bash
# Set up API credentials (see data-sources.md for details)
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

### 3. Explore Data
```bash
# Run data scope analysis
python3 scripts/analyze_infectious_disease_scope.py
```

### 4. Start Analysis
```bash
# Launch Jupyter
jupyter lab

# Open: notebooks/1_exploratory/
```

---

## 📁 Project Structure

```
.
├── docs/                    # 📚 Documentation (you are here)
│   ├── index.md             # This file
│   ├── problem_statements.md
│   ├── objectives/          # Feature objectives
│   ├── data_dictionary/     # Data schemas & definitions
│   ├── project_context/     # Business context & data sources
│   └── methodology/         # Statistical methods
│
├── data/                    # 💾 Data storage
│   ├── 1_raw/               # Original source data
│   ├── 4_processed/         # Analysis-ready datasets
│   └── schemas/             # Data contracts
│
├── notebooks/               # 📓 Interactive analysis
│   ├── 1_exploratory/       # EDA & data profiling
│   └── 2_analysis/          # Deep-dive analysis
│
├── src/                     # 🐍 Production code
│   ├── data_processing/     # ETL pipelines
│   ├── analysis/            # Statistical analysis
│   ├── models/              # Forecasting models
│   └── visualization/       # Plotting utilities
│
├── scripts/                 # ⚙️ Automation
│   ├── analyze_infectious_disease_scope.py
│   └── auto_analyze.py
│
├── results/                 # 📈 Analysis outputs
├── reports/                 # 📄 Stakeholder deliverables
├── models/                  # 🤖 Trained models
└── tests/                   # 🧪 Quality assurance
```

---

## 🗓️ Project Timeline

### Phase 1: Foundation (Weeks 3-5)
- Data extraction & quality assessment
- Exploratory data analysis
- Seasonal pattern identification

### Phase 2: Modeling (Weeks 6-8)
- Forecasting model development
- Model validation & tuning
- Disease burden analysis

### Phase 3: Insights & Tools (Weeks 9-12)
- Resource allocation framework
- Interactive dashboard
- Executive reports & presentations

---

## 👥 Team & Contacts

**Project Lead:** Data Analytics Team, MOH  
**Stakeholders:**
- MOH Policy Makers
- Healthcare Facility Committees
- Public Health Surveillance Teams

**Documentation Questions:** Open an issue in this repository  
**Technical Support:** [Contact internal support team]

---

## 🔗 Related Resources

- **MOH Website:** https://www.moh.gov.sg/
- **Data Source (Kaggle):** https://www.kaggle.com/datasets/subhamjain/health-dataset-complete-singapore
- **HEALIX Platform:** [Internal documentation]
- **Databricks Workspace:** [Access portal]

---

**Last Updated:** 9 February 2026  
**Document Owner:** Project Manager  
**Next Review:** Weekly during Phase 1

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
