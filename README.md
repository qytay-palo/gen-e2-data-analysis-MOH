# MOH Polyclinic Queue Optimization & Visitation Analysis

Analyzing polyclinic visitation patterns across time and location to design effective queue management systems.

## Overview

This project analyzes how polyclinic visitations vary across time and location to develop data-driven strategies for queue optimization and resource allocation. Built on Singapore's Ministry of Health polyclinic data, this analysis supports improved patient experience, operational efficiency, and healthcare accessibility.

### Project Objectives

- **Primary Goal**: Analyze polyclinic visitation patterns across temporal and geographic dimensions
- **Secondary Goal**: Design and recommend effective queue management systems to reduce wait times
- **Impact**: Improve patient satisfaction, optimize resource utilization, and enhance healthcare service delivery

### Key Stakeholders

- **Patients**: Reduced wait times, improved service experience, better access to care
- **CEO/Leadership**: Data-driven operational insights, strategic resource planning, performance metrics

### Key Features

- 📊 **Temporal Analysis** - Visitation patterns by hour, day, week, month, season
- 📍 **Geographic Analysis** - Location-based demand across 15 polyclinics and planning areas
- ⏱️ **Queue Analytics** - Wait time analysis, bottleneck identification, capacity planning
- 🤖 **Predictive Modeling** - Demand forecasting and resource optimization recommendations
- 🔄 **Automated ETL** - API-based data extraction with validation and processing
- 📈 **Real-time Dashboards** - Interactive visualizations for stakeholder insights

## Quick Start

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd gen-e2-data-analysis-MOH

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Data Connection
```bash
# Set up API configuration
cp config/database.yml.example config/database.yml
# Edit config/database.yml with your API credentials
```

### 3. Run Initial Data Extraction
```bash
# Extract polyclinic data
python scripts/run_extraction.py --sources attendances --last-n-days 30
```

### 4. Explore Data
```bash
# Launch Jupyter for exploratory analysis
jupyter notebook notebooks/1_exploratory/
```

📖 **[Full Documentation](docs/)** | 🎯 **[Project Objectives](docs/objectives/opportunities.md)**

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
