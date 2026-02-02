# Epic 001: Facility Utilization & Bottleneck Analysis

## Overview

This epic analyzes patient distribution patterns, service utilization rates, and process bottlenecks across Singapore's healthcare network to enable evidence-based resource allocation and operational improvements.

**Key Objectives:**
- Profile performance for 100% of healthcare facilities
- Identify minimum 10 critical bottlenecks with quantified impact
- Develop severity scoring framework
- Conduct root cause analysis
- Generate actionable improvement recommendations
- Create interactive utilization dashboard

## Prerequisites

### System Requirements
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space
- Internet connection (for initial Kaggle dataset download)

### Required Software
- Python package manager (pip or conda)
- Kaggle API credentials (free account)

## Installation

### 1. Clone Repository

```bash
cd /path/to/project
cd epics/epic-001
```

### 2. Set Up Python Environment

**Option A: Using pip**

```bash
# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

**Option B: Using conda**

```bash
# Create conda environment
conda create -n epic001 python=3.8

# Activate environment
conda activate epic001

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Kaggle API

**Step 1: Get API Credentials**
1. Create free account at https://www.kaggle.com/
2. Go to Account Settings → API section
3. Click "Create New API Token"
4. Download `kaggle.json` file

**Step 2: Install Credentials**

```bash
# Create Kaggle directory
mkdir -p ~/.kaggle

# Move credentials file
mv ~/Downloads/kaggle.json ~/.kaggle/

# Set permissions (required for security)
chmod 600 ~/.kaggle/kaggle.json
```

**Step 3: Verify Connection**

```python
import kagglehub
dataset_path = kagglehub.dataset_download("subhamjain/health-dataset-complete-singapore")
print(f"✓ Success! Dataset at: {dataset_path}")
```

## Configuration

Configuration files are in `config/`:

- **`epic_001_config.yml`**: Main configuration (data sources, paths, logging)
- **`epic_001_params.yml`**: Analysis parameters (thresholds, weights, filters)

### Key Configuration Parameters

```yaml
# Utilization Thresholds
utilization_thresholds:
  optimal_min: 70      # Optimal range: 70-85%
  optimal_max: 85
  bottleneck: 90       # >90% = bottleneck

# Bottleneck Detection
bottleneck_detection:
  min_utilization_rate: 90.0
  min_severity_score: 5.0
```

## Running the System

### Quick Start (Full Pipeline)

Run the complete analysis end-to-end:

```bash
python scripts/run_full_pipeline.py
```

**What This Does:**
1. Downloads Kaggle dataset (cached locally)
2. Extracts facility attendance and capacity data
3. Engineers utilization features and metrics
4. Detects bottlenecks and generates recommendations
5. Creates visualizations and dashboards
6. Saves all results to `results/` and `reports/`

### Step-by-Step Execution

For granular control, run individual phases:

#### Phase 1: Data Extraction

```bash
python scripts/01_extract_data.py \
  --output-dir data/raw \
  --year-start 2006 \
  --year-end 2020
```

**Outputs:**
- `data/raw/attendance_by_hospitals.csv`
- `data/raw/bed_capacity.csv`
- `data/raw/clinic_registry.csv`

#### Phase 2: Feature Engineering

```bash
python scripts/02_engineer_features.py \
  --input-dir data/raw \
  --output-dir data/features
```

**Outputs:**
- `data/features/utilization_metrics.parquet`
- `data/features/utilization_metrics.csv`
- `data/features/bottlenecks.csv`

#### Phase 3: Analysis

```bash
python scripts/03_run_analysis.py \
  --input-dir data/features \
  --output-dir results
```

**Outputs:**
- `results/tables/facility_profiles.csv`
- `results/tables/bottlenecks.csv`
- `results/tables/recommendations.csv`
- `results/metrics/analysis_summary.json`

#### Phase 4: Visualization

```bash
python scripts/04_generate_visualizations.py \
  --features-dir data/features \
  --results-dir results/tables \
  --output-dir reports/figures \
  --formats html png
```

**Outputs:**
- `reports/figures/utilization_trend.html`
- `reports/figures/facility_ranking.png`
- `reports/figures/bottleneck_severity.html`
- `reports/figures/capacity_gap.png`

### Advanced Options

**Skip data extraction (use cached data):**
```bash
python scripts/run_full_pipeline.py --skip-extraction
```

**Custom year range:**
```bash
python scripts/01_extract_data.py --year-start 2015 --year-end 2020
```

**Debug logging:**
```bash
python scripts/run_full_pipeline.py --log-level DEBUG
```

## Output Locations

| Output Type | Location | Description |
|-------------|----------|-------------|
| Raw Data | `data/raw/` | Extracted CSV files from Kaggle |
| Features | `data/features/` | Engineered utilization metrics |
| Results | `results/tables/` | Analysis outputs (CSV) |
| Metrics | `results/metrics/` | Summary statistics (JSON) |
| Figures | `reports/figures/` | Visualizations (HTML, PNG) |
| Logs | `logs/` | Execution logs |

## Testing

Run the test suite to verify installation:

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_extraction.py -v
```

**Expected Output:**
```
============================= test session starts ==============================
collected 20 items

tests/test_extraction.py ........                                        [ 40%]
tests/test_features.py ........                                          [ 80%]
tests/test_analysis.py ....                                              [100%]

============================== 20 passed in 2.34s ===============================
```

## Key Outputs & Deliverables

### 1. Facility Performance Profiles

**File:** `results/tables/facility_profiles.csv`

Contains comprehensive metrics for each facility:
- Average utilization rate
- Min/max utilization
- Patient volume statistics
- Performance tier ranking

### 2. Bottleneck Identification

**File:** `results/tables/bottlenecks.csv`

Critical bottleneck facilities with:
- Severity score (quantified impact)
- Excess demand calculation
- Patients affected annually
- Year-over-year trends

### 3. Recommendations

**File:** `results/tables/recommendations.csv`

Actionable recommendations including:
- Recommendation type (capacity expansion, process optimization)
- Expected impact
- Implementation complexity
- Estimated cost level

### 4. Interactive Dashboard

**File:** `reports/figures/*.html`

Interactive Plotly visualizations:
- Utilization trends over time
- Facility ranking charts
- Bottleneck severity analysis
- Capacity gap analysis

## Troubleshooting

### Issue: Kaggle Authentication Failed

**Error:** `OSError: Could not find kaggle.json`

**Solution:**
```bash
# Verify kaggle.json exists
ls ~/.kaggle/kaggle.json

# Check permissions
chmod 600 ~/.kaggle/kaggle.json

# Verify credentials are valid (login to kaggle.com)
```

### Issue: Missing Dependencies

**Error:** `ModuleNotFoundError: No module named 'kagglehub'`

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep kagglehub
```

### Issue: Empty Results

**Problem:** Analysis runs but produces no bottlenecks

**Solution:**
- Check year range includes recent data (2015+)
- Verify utilization threshold in `config/epic_001_params.yml`
- Lower `min_severity_score` threshold

### Issue: Memory Error

**Error:** `MemoryError` during processing

**Solution:**
- Reduce year range to process fewer years
- Use Parquet format (smaller memory footprint)
- Increase system memory or use chunked processing

## Project Structure

```
epic-001/
├── config/                 # Configuration files
│   ├── epic_001_config.yml
│   └── epic_001_params.yml
├── src/                    # Source code modules
│   ├── extraction.py       # Data extraction from Kaggle
│   ├── features.py         # Feature engineering
│   ├── analysis.py         # Bottleneck analysis
│   ├── visualization.py    # Plotting and dashboards
│   └── utils.py            # Utility functions
├── scripts/                # Executable scripts
│   ├── 01_extract_data.py
│   ├── 02_engineer_features.py
│   ├── 03_run_analysis.py
│   ├── 04_generate_visualizations.py
│   └── run_full_pipeline.py
├── tests/                  # Unit tests
│   ├── test_extraction.py
│   ├── test_features.py
│   └── test_analysis.py
├── data/                   # Data directories
│   ├── raw/               # Raw extracted data
│   ├── processed/         # Cleaned data
│   └── features/          # Engineered features
├── results/               # Analysis results
│   ├── tables/           # CSV outputs
│   ├── metrics/          # JSON summaries
│   └── exports/          # Exported datasets
├── reports/              # Reports and visualizations
│   ├── figures/         # Charts and plots
│   ├── dashboards/      # Interactive dashboards
│   └── documents/       # Written reports
├── logs/                # Execution logs
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Documentation

- **Implementation Plan**: `../../docs/methodology/implementation_plans/epic-001-*.md`
- **Data Sources**: `../../docs/project_context/data_sources.md`
- **Tech Stack**: `../../docs/project_context/tech_stack.md`

## Support & Contact

For issues or questions:
1. Check logs in `logs/` directory
2. Review error messages in `logs/errors.log`
3. Consult implementation plan documentation
4. Contact MOH Data Analytics Team

## Version History

- **v1.0.0** (2026-02-02): Initial release
  - Data extraction from Kaggle
  - Utilization rate calculation
  - Bottleneck detection
  - Recommendation generation
  - Interactive visualizations

## License

Internal use only - Ministry of Health Singapore
