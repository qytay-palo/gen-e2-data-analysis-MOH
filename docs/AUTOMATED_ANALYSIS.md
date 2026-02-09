# Automated LLM-Driven Data Analysis System

Automated data analysis framework that implements the `knowledge-work-plugins/data` patterns for healthcare analytics.

## 🚀 Features

- **Automated Data Exploration** (`/explore-data`) - Profile datasets, detect missing values, assess quality
- **Pattern Analysis** (`/analyze`) - Identify trends, correlations, outliers, and temporal patterns  
- **Data Validation** (`/validate`) - Quality checks, duplicate detection, completeness assessment
- **Batch Processing** - Analyze multiple datasets automatically
- **Auto-Generated Reports** - JSON metrics and Markdown reports
- **Scheduled Execution** - Configure analyses to run automatically

## 📁 Project Structure

```
scripts/
├── auto_analyze.py           # Core automated analyzer class
└── run_scheduled_analysis.py # Scheduled analysis runner

config/
└── auto_analysis.yml         # Analysis schedules and parameters

notebooks/2_analysis/
└── automated_analysis_demo.ipynb  # Interactive demos

reports/                      # Auto-generated markdown reports
results/metrics/             # JSON analysis results
```

## 🛠️ Installation

```bash
# Install required packages
pip install pandas pyyaml

# Verify installation
python scripts/auto_analyze.py --help
```

## 📖 Usage

### Command Line

#### Single Dataset Analysis

```bash
# Explore a dataset
python scripts/auto_analyze.py \
  --dataset data/1_raw/kaggle/weekly-infectious-disease-bulletin-cases.csv \
  --type explore

# Validate data quality
python scripts/auto_analyze.py \
  --dataset data/1_raw/kaggle/doctors_by_age_group_and_sex.csv \
  --type validate

# Analyze patterns
python scripts/auto_analyze.py \
  --dataset data/1_raw/kaggle/principal_causes_of_death.csv \
  --type analyze
```

#### Batch Processing

```bash
# Analyze all CSVs in a directory
python scripts/auto_analyze.py \
  --batch data/1_raw/kaggle \
  --batch-types explore validate analyze
```

#### Scheduled Analysis

```bash
# Run all configured analyses
python scripts/run_scheduled_analysis.py
```

### Python API

```python
from auto_analyze import AutomatedAnalyzer

# Initialize
analyzer = AutomatedAnalyzer()

# Single dataset
results = analyzer.analyze_dataset(
    "data/1_raw/kaggle/dataset.csv",
    analysis_type="explore"
)

# Batch processing
batch_results = analyzer.batch_analyze(
    "data/1_raw/kaggle",
    analysis_types=['explore', 'validate']
)
```

### Jupyter Notebook

Open `notebooks/2_analysis/automated_analysis_demo.ipynb` for interactive examples.

## ⚙️ Configuration

Edit `config/auto_analysis.yml` to configure:

- **Analysis Schedules** - Which datasets to analyze and when
- **Analysis Types** - explore, analyze, validate
- **Parameters** - Thresholds for warnings and detection
- **Output Settings** - JSON, Markdown, visualization options

Example configuration:

```yaml
analysis_schedules:
  workforce_analysis:
    enabled: true
    datasets:
      - "data/1_raw/kaggle/doctors_by_age_group_and_sex.csv"
      - "data/1_raw/kaggle/nurses_by_age_group_and_sex.csv"
    analysis_types:
      - explore
      - validate
    output_format:
      - json
      - markdown

parameters:
  missing_value_warning_threshold: 20.0
  correlation_threshold: 0.7
  outlier_method: "iqr"
```

## 📊 Analysis Types

### 1. Explore (`--type explore`)

Implements the `/explore-data` command:

- **Data profiling**: Shape, data types, memory usage
- **Missing values**: Detection and percentage calculation
- **Summary statistics**: Numeric columns (mean, median, std, etc.)
- **Cardinality**: Unique value counts and distributions
- **Quality flags**: Automatic issue detection

**Output**: 
- JSON: `results/metrics/{dataset}_explore_{timestamp}.json`
- Markdown: `reports/{dataset}_explore_{timestamp}.md`

### 2. Analyze (`--type analyze`)

Implements the `/analyze` command:

- **Temporal analysis**: Date range detection and coverage
- **Correlations**: Strong correlations (|r| > 0.7) between numeric variables
- **Outlier detection**: IQR method for anomaly identification
- **Pattern recognition**: Trends and relationships

**Output**:
- JSON: `results/metrics/{dataset}_analyze_{timestamp}.json`
- Markdown: `reports/{dataset}_analyze_{timestamp}.md`

### 3. Validate (`--type validate`)

Implements the `/validate` command:

- **Completeness checks**: Missing value analysis per column
- **Duplicate detection**: Exact row duplicates
- **Consistency checks**: Single-value columns, cardinality issues
- **Recommendations**: Actionable suggestions for data improvement

**Output**:
- JSON: `results/metrics/{dataset}_validate_{timestamp}.json`  
- Markdown: `reports/{dataset}_validate_{timestamp}.md`

## 🔄 Automated Workflows

### Cron Job Setup (Unix/Linux/macOS)

```bash
# Edit crontab
crontab -e

# Add scheduled analysis (daily at 2 AM)
0 2 * * * cd /path/to/project && python scripts/run_scheduled_analysis.py

# Add batch processing (every 6 hours)
0 */6 * * * cd /path/to/project && python scripts/auto_analyze.py --batch data/1_raw/kaggle
```

### Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., daily)
4. Set action: `python C:\path\to\scripts\run_scheduled_analysis.py`

## 📈 Example Output

### Explore Results

```json
{
  "timestamp": "2026-02-09T10:30:00",
  "dataset": "weekly-infectious-disease-bulletin-cases.csv",
  "analysis_type": "explore",
  "shape": {"rows": 52000, "columns": 15},
  "missing_percentage": {
    "disease_name": 0.0,
    "week": 0.0,
    "cases": 2.3
  },
  "quality_flags": [
    "cases: Low missing values (2.3%)"
  ]
}
```

### Markdown Report

```markdown
# Automated Analysis Report: Explore

**Generated:** 2026-02-09T10:30:00
**Dataset:** `weekly-infectious-disease-bulletin-cases.csv`
**Shape:** 52000 rows × 15 columns

## Data Profile

- **Memory Usage:** 5.23 MB
- **Columns:** 15

### Missing Values

| Column | Missing % |
|--------|-----------|
| cases  | 2.30%     |

### Data Quality Flags

- cases: Low missing values (2.3%)
```

## 🎯 Healthcare Use Cases

### Disease Outbreak Detection

```bash
# Analyze infectious disease trends
python scripts/auto_analyze.py \
  --dataset data/1_raw/kaggle/weekly-infectious-disease-bulletin-cases.csv \
  --type analyze
```

### Healthcare Workforce Analysis

```bash
# Batch analyze all workforce data
python scripts/auto_analyze.py \
  --batch data/1_raw/kaggle \
  --batch-types explore validate
```

### Data Quality Monitoring

```bash
# Regular validation checks
python scripts/run_scheduled_analysis.py
```

## 🔧 Customization

### Add Custom Analysis Types

Edit `scripts/auto_analyze.py` and add methods to `AutomatedAnalyzer` class:

```python
def _custom_analysis(self, df: pd.DataFrame) -> Dict:
    """Your custom analysis logic"""
    return {
        "custom_metric": calculation,
        "insights": []
    }
```

### Custom Report Formatting

Modify `_generate_markdown_report()` method to customize report output.

### Integration with LLM APIs

```python
# Example: Send results to LLM for insights
import openai

results = analyzer.analyze_dataset("data.csv", "analyze")

prompt = f"""
Analyze this healthcare data:
{json.dumps(results, indent=2)}

Provide insights and recommendations.
"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
```

## 📚 Data Plugin Commands Reference

The automated analyzer implements these commands from `knowledge-work-plugins/data`:

| Command | Script Method | Description |
|---------|---------------|-------------|
| `/explore-data` | `_explore_data()` | Profile and explore dataset |
| `/analyze` | `_analyze_patterns()` | Detect patterns, trends, correlations |
| `/validate` | `_validate_data()` | Quality checks and validation |
| `/write-query` | - | Not implemented (SQL generation) |
| `/create-viz` | - | Not implemented (visualization) |
| `/build-dashboard` | - | Not implemented (dashboard) |

## 🐛 Troubleshooting

### Dataset not found

```bash
# Check if data exists
ls -la data/1_raw/kaggle/

# Run Kaggle extraction first
jupyter notebook notebooks/extract_from_kaggle.ipynb
```

### Missing dependencies

```bash
pip install -r requirements.txt
```

### Permission errors

```bash
# Make scripts executable
chmod +x scripts/*.py
```

## 🚦 Next Steps

1. **Run the demo notebook**: `notebooks/2_analysis/automated_analysis_demo.ipynb`
2. **Configure your schedules**: Edit `config/auto_analysis.yml`
3. **Execute batch analysis**: `python scripts/auto_analyze.py --batch data/1_raw/kaggle`
4. **Review reports**: Check `reports/` directory
5. **Set up automation**: Add to cron or task scheduler

## 📝 Logging

Analysis logs are saved to:
- Audit logs: `logs/audit/auto_analysis.log`
- Execution summaries: `results/metrics/execution_summary_*.yaml`

## 🤝 Integration with Other Tools

- **Power BI/Tableau**: Export JSON results for visualization
- **Jupyter**: Use the Python API in notebooks
- **CI/CD**: Run validation as part of data pipelines
- **LLM APIs**: Send results to GPT-4/Claude for insights

## 📄 License

Part of the gen-e2-data-analysis-MOH project.
