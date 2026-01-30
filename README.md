# MOH Polyclinic Patient Analysis & Policy Intelligence

Comprehensive analysis of polyclinic patient demographics, health trends, and service utilization to identify policy intervention opportunities and inform healthcare governance.

## Overview

This project delivers data-driven insights into Singapore's polyclinic patient population, analyzing distribution patterns, temporal trends, and healthcare utilization to support evidence-based policy development and strategic healthcare planning. Built on Singapore's Ministry of Health polyclinic data, this analysis enables proactive identification of healthcare gaps requiring policy intervention.

### Project Objectives

#### Main Goals
- **Understand Patient Population**: Comprehensive analysis of patient demographics, distribution patterns, and temporal trends across Singapore polyclinics
- **Identify Policy Intervention Needs**: Detect healthcare problems, service gaps, and governance issues requiring regulatory or policy intervention

#### Measurable Success Criteria
- **Patient Understanding**: Complete demographic profiling covering 100% of polyclinic patients with distribution analysis by age, gender, ethnicity, and socioeconomic status
- **Trend Detection**: Identify and quantify temporal trends in disease prevalence, service utilization, and patient access patterns
- **Policy Problem Identification**: Detect and prioritize at least 5 high-impact policy intervention opportunities with quantified impact assessments
- **Evidence Quality**: Deliver statistically significant findings with confidence intervals for all key metrics

#### Business Decisions Informed
- **Policy Development**: Evidence-based healthcare policies, regulatory interventions, and governance frameworks
- **Resource Allocation**: Strategic planning for polyclinic capacity, staffing, and service distribution
- **Health Equity**: Targeted interventions to address geographic and demographic healthcare disparities
- **Program Effectiveness**: Assessment of existing healthcare initiatives (e.g., Healthier SG program)

### Key Stakeholders

- **Government Agencies**: Ministry of Health policy makers, healthcare regulators, and public health officials requiring evidence for governance decisions
- **Business Decision Makers**: Healthcare administrators, hospital executives, and operational leaders requiring strategic insights for planning and resource allocation

### Key Features

- � **Patient Demographics Analysis** - Age, gender, ethnicity, socioeconomic distribution patterns
- 📊 **Disease Burden Assessment** - Chronic condition prevalence, comorbidity analysis, disease trends
- 📍 **Geographic Health Equity** - Regional disparities, access patterns, underserved populations
- 🏥 **Service Utilization Patterns** - Visit frequency, care-seeking behavior, program enrollment trends
- 🎯 **Policy Gap Identification** - Healthcare problems requiring intervention, regulatory opportunities
- 🔄 **Automated ETL** - API-based data extraction with validation and processing
- 📈 **Executive Dashboards** - Interactive visualizations for government and business decision makers

## Quick Start

### 1. Environment Setup

**Option A: Using Conda (Recommended for HEALIX/Databricks)**
```bash
# Clone the repository
git clone <repository-url>
cd gen-e2-data-analysis-MOH

# Create conda environment
conda env create -f environment.yml
conda activate moh-polyclinic-analysis
```

**Option B: Using pip**
```bash
# Clone and install dependencies
git clone <repository-url>
cd gen-e2-data-analysis-MOH
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# - MOH_API_KEY: Your MOH data API key
# - DATABRICKS_HOST: Your Databricks workspace URL
# - DATABRICKS_TOKEN: Your personal access token
nano .env
```

### 3. Configure Data Connection
```bash
# Review and update API configuration
nano config/database.yml

# Update analysis parameters
nano config/analysis.yml
```

### 4. Run Initial Data Extraction
```bash
# Extract recent polyclinic attendance data
python scripts/run_extraction.py --sources attendances --last-n-days 30

# Extract all core data sources
python scripts/run_extraction.py --sources all --start-date 2025-01-01
```

### 5. Explore Data
```bash
# Launch Jupyter for exploratory analysis
jupyter lab

# Navigate to notebooks/1_exploratory/ and open:
# - patient_profiling.ipynb
# - data_quality_check.ipynb
```

### 6. Review Strategic Epics
Review prioritized analytics initiatives in `docs/objectives/epics/`:
- **EPIC-001**: Patient Population Segmentation (Foundation - Start here)
- **EPIC-002**: Temporal Trend Detection & Forecasting
- **EPIC-003**: Geographic Health Equity Analysis

📖 **[Full Documentation](docs/)** | 🎯 **[Project Objectives](docs/objectives/)** | 📊 **[Data Dictionary](docs/data_dictionary/)**

## Technical Stack

**Deployment Platform**: HEALIX (GCC Cloud Environment)  
**Analytics Platform**: Databricks  
**Primary Languages**: Python, R  
**Additional Tools**: STATA for statistical analysis

### Development Environment
- Python 3.8+
- Pandas, NumPy, Scikit-learn for data analysis
- Matplotlib, Seaborn, Plotly for visualization
- PySpark for distributed processing (Databricks)
- API client libraries for data extraction

## Usage Examples

### Data Extraction

```bash
# Extract polyclinic attendance data
python scripts/run_extraction.py --sources attendances --last-n-days 30

# Extract all data sources
python scripts/run_extraction.py --sources all --start-date 2025-01-01 --end-date 2025-12-31
```

### Data Analysis (Python)

```python
import pandas as pd
from src.analysis import temporal_patterns, geographic_analysis

# Load processed data
df = pd.read_parquet('data/4_processed/attendances_clean.parquet')

# Analyze temporal patterns
hourly_patterns = temporal_patterns.analyze_by_hour(df)
seasonal_trends = temporal_patterns.analyze_seasonal(df)

# Geographic analysis
polyclinic_demand = geographic_analysis.demand_by_location(df)
```

### Queue Simulation (R)

```r
library(simmer)
library(dplyr)

# Load data
attendances <- read.csv("data/4_processed/attendances_clean.csv")

# Run queue simulation
source("src/models/queue_simulation.R")
results <- simulate_queue_system(attendances, scenario = "optimized")
```

## Project Structure

```
├── config/                 # [PHASE 2] Configuration files
│   ├── database.yml       # API connection and extraction settings
│   └── queries.yml        # Query templates and parameters
├── docs/                  # [PHASE 1] Documentation
│   ├── index.md          # Central documentation hub
│   ├── objectives/       # Project goals and ML opportunities
│   ├── project_context/  # Data sources and tech stack
│   ├── data_dictionary/  # Data schemas and definitions
│   └── methodology/      # Analysis approaches and methods
├── data/                  # [PHASE 3] Data storage
│   ├── 1_raw/           # Original extracted data (immutable)
│   ├── 2_external/      # External reference data
│   ├── 3_interim/       # Intermediate transformations
│   └── 4_processed/     # Final analysis-ready datasets
├── notebooks/             # [PHASE 4] Interactive analysis
│   ├── 1_exploratory/   # EDA and data profiling
│   ├── 2_analysis/      # Deep-dive analysis
│   └── 3_feature_engineering/ # Feature creation
├── src/                   # [PHASE 5] Production code
│   ├── data_processing/ # ETL and data extraction
│   ├── features/        # Feature engineering
│   ├── analysis/        # Statistical analysis modules
│   ├── models/          # ML model training
│   ├── visualization/   # Plotting and dashboards
│   └── utils/           # Helper utilities
├── tests/                # [PHASE 6] Quality assurance
├── models/               # [PHASE 7] Trained model artifacts
├── results/              # [PHASE 8] Analysis outputs
│   ├── tables/          # Summary statistics
│   ├── metrics/         # Performance KPIs
│   └── exports/         # Stakeholder exports
├── reports/              # [PHASE 9] Deliverables
│   ├── figures/         # Static visualizations
│   ├── dashboards/      # Interactive dashboards
│   └── presentations/   # Executive summaries
└── scripts/              # [PHASE 10] Automation
    ├── run_extraction.py # Data extraction runner
    └── run_scheduler.py  # Scheduled automation
```

## Analysis Workflow

### Phase 1: Understanding (CURRENT)
1. Review [project objectives](docs/objectives/opportunities.md)
2. Study [data sources](docs/project_context/data_sources.md)
3. Understand [data dictionary](docs/data_dictionary/)

### Phase 2: Data Acquisition
1. Configure API connection in `config/database.yml`
2. Run data extraction: `python scripts/run_extraction.py`
3. Validate data quality with `src/data_processing/data_validator.py`

### Phase 3: Exploratory Analysis
1. Open `notebooks/1_exploratory/` for EDA
2. Analyze visitation patterns across time and location
3. Identify queue bottlenecks and wait time drivers

### Phase 4: Advanced Analysis
1. Time-series analysis of demand patterns
2. Geographic clustering and resource allocation
3. Queue simulation and optimization modeling

### Phase 5: Deliverables
1. Generate insights in `results/`
2. Create dashboards in `reports/dashboards/`
3. Prepare executive presentations in `reports/presentations/`

## Data Sources

**Source**: MOH Singapore Open Data  
**Access Method**: RESTful API (https://data.gov.sg)  
**Update Frequency**: Daily incremental extraction  
**Temporal Coverage**: 2015-present  

### Key Datasets
- **POLYCLINIC_ATTENDANCES** - Visit records, wait times, consultation duration
- **PATIENT_DEMOGRAPHICS** - Age, gender, location, subsidy status
- **DIAGNOSIS_RECORDS** - Medical diagnoses with ICD-10 codes
- **POLYCLINIC_MASTER** - Facility information, operating hours, capacity

See [Data Sources Documentation](docs/project_context/data_sources.md) for complete schema details.

## Key Analysis Areas

### 1. Temporal Patterns
- **Hourly**: Peak hours, lunch-time dips, end-of-day surges
- **Daily**: Weekday vs weekend patterns
- **Seasonal**: Flu season impacts, holiday effects
- **Trends**: Long-term demand growth

### 2. Geographic Analysis
- **Polyclinic-level**: Individual facility performance
- **Regional**: North, South, East, West, Central demand
- **Planning Areas**: Community-level accessibility
- **Catchment Analysis**: Patient origin and travel patterns

### 3. Queue Optimization
- **Wait Time Drivers**: Identify bottlenecks and delays
- **Capacity Planning**: Staff and resource allocation
- **Appointment Scheduling**: Optimal slot distribution
- **Walk-in vs Appointment**: Access pathway analysis

### 4. Predictive Analytics
- **Demand Forecasting**: Predict future visitation volumes
- **Resource Optimization**: Staff scheduling recommendations
- **Queue Simulation**: Test alternative queue systems
- **Impact Modeling**: Evaluate policy interventions

## Expected Deliverables

### For Patients
- Reduced wait times through optimized scheduling
- Improved transparency of queue status
- Better appointment availability
- Enhanced service experience

### For CEO/Leadership
- **Strategic Insights**: Data-driven understanding of demand patterns
- **Operational Metrics**: KPIs for wait times, capacity utilization, patient flow
- **Resource Optimization**: Evidence-based staffing and facility recommendations
- **Performance Dashboards**: Real-time monitoring of queue performance
- **Forecasting Models**: Predictive tools for capacity planning

## Documentation

- 📖 [Documentation Hub](docs/index.md) - Central navigation
- 🎯 [ML Opportunities](docs/objectives/opportunities.md) - Analysis and modeling opportunities
- 📊 [Data Sources](docs/project_context/data_sources.md) - Complete data dictionary
- 🔧 [Tech Stack](docs/project_context/tech_stack.md) - Technology specifications
- 📈 [Methodology](docs/methodology/) - Analysis approaches

## Getting Help

- Review documentation in `docs/`
- Check data extraction guides in `docs/project_context/`
- Explore example notebooks in `notebooks/1_exploratory/`

---

**Last Updated**: January 2026  
**Platform**: HEALIX (GCC Databricks)  
**Status**: Phase 1 - Project Initialization

## License

Internal MOH use only. Confidential and proprietary.

---

**Version**: 1.0  
**Last Updated**: 2026-01-26  
**Maintained By**: MOH Data Analytics Team
