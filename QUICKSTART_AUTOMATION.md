# Quick Start Guide - Automated Analysis System

## ✅ Installation Complete!

Your automated LLM-driven data analysis system is now set up with the `knowledge-work-plugins/data` patterns.

## 🎯 What You Have

### 1. **Automated Analysis Scripts**
- `scripts/auto_analyze.py` - Core analyzer with `/explore`, `/analyze`, `/validate` commands
- `scripts/run_scheduled_analysis.py` - Batch runner using config
- `scripts/demo_auto_analysis.py` - Demo with sample data

### 2. **Data Plugin Commands** (in `.github/prompts/data-plugin/`)
- `/analyze` - Answer data questions and detect patterns
- `/explore-data` - Profile datasets automatically
- `/write-query` - SQL query generation
- `/create-viz` - Visualization creation
- `/build-dashboard` - Interactive dashboards
- `/validate` - Data quality checks

### 3. **Configuration**
- `config/auto_analysis.yml` - Define analysis schedules and parameters

### 4. **Interactive Notebook**
- `notebooks/2_analysis/automated_analysis_demo.ipynb` - Jupyter demos

## 🚀 Quick Commands

### Run the Demo (Start Here!)
```bash
cd /Users/qytay/Documents/GitHub/gen-e2-data-analysis-MOH
.venv/bin/python scripts/demo_auto_analysis.py
```

### Single Dataset Analysis
```bash
# Explore
.venv/bin/python scripts/auto_analyze.py --dataset data/1_raw/sample_disease_data.csv --type explore

# Validate
.venv/bin/python scripts/auto_analyze.py --dataset data/1_raw/sample_disease_data.csv --type validate

# Analyze patterns
.venv/bin/python scripts/auto_analyze.py --dataset data/1_raw/sample_disease_data.csv --type analyze
```

### Batch Processing
```bash
# Analyze all CSVs in a directory
.venv/bin/python scripts/auto_analyze.py --batch data/1_raw --batch-types explore validate analyze
```

### Scheduled Analysis
```bash
# Run configured schedules
.venv/bin/python scripts/run_scheduled_analysis.py
```

## 📊 What Each Analysis Does

### `/explore` - Data Exploration
✓ Dataset shape and structure  
✓ Missing value detection  
✓ Data type analysis  
✓ Summary statistics  
✓ Quality flags  

**Output**: Reports missing values, cardinality, memory usage

### `/analyze` - Pattern Analysis
✓ Temporal trends  
✓ Correlation detection  
✓ Outlier identification  
✓ Relationship discovery  

**Output**: Reports correlations (|r| > 0.7), outliers, temporal patterns

### `/validate` - Quality Validation
✓ Completeness checks  
✓ Duplicate detection  
✓ Consistency validation  
✓ Actionable recommendations  

**Output**: Quality score, duplicate %, recommendations

## 📁 Where to Find Results

After running analyses, check:

```
reports/
├── sample_disease_data_explore_*.md      # Exploration reports
├── sample_disease_data_analyze_*.md      # Pattern analysis
└── sample_disease_data_validate_*.md     # Validation reports

results/metrics/
├── sample_disease_data_explore_*.json    # Detailed JSON results
├── sample_disease_data_analyze_*.json
├── sample_disease_data_validate_*.json
└── execution_summary_*.yaml              # Batch run summaries
```

## 🔄 LLM Integration Examples

### Option 1: Use Results for LLM Prompts

```python
import json
from auto_analyze import AutomatedAnalyzer

# Run analysis
analyzer = AutomatedAnalyzer()
results = analyzer.analyze_dataset("data.csv", "analyze")

# Send to LLM
prompt = f"""
Analyze this healthcare data and provide insights:

Dataset: {results['dataset']}
Rows: {results['shape']['rows']}
Columns: {results['shape']['columns']}

Correlations found:
{json.dumps(results.get('correlations', {}), indent=2)}

Outliers detected:
{json.dumps(results.get('outliers', {}), indent=2)}

What actionable insights can you provide for healthcare operations?
"""

# Send prompt to your LLM API (OpenAI, Claude, etc.)
```

### Option 2: Auto-Generate Insights

```python
def generate_llm_insights(dataset_path):
    analyzer = AutomatedAnalyzer()
    
    # Run all analyses
    explore = analyzer.analyze_dataset(dataset_path, "explore")
    validate = analyzer.analyze_dataset(dataset_path, "validate")
    analyze = analyzer.analyze_dataset(dataset_path, "analyze")
    
    # Compile summary
    summary = {
        "quality_score": 100 - validate['duplicate_percentage'],
        "completeness": sum(validate['completeness'].values()) / len(validate['completeness']),
        "insights": []
    }
    
    # Add automated insights
    if analyze.get('correlations', {}).get('strong_correlations'):
        summary['insights'].append(
            f"Found {len(analyze['correlations']['strong_correlations'])} strong correlations"
        )
    
    return summary
```

## 🎓 Example Workflows

### 1. Weekly Disease Surveillance

```bash
# Configure in config/auto_analysis.yml
analysis_schedules:
  disease_surveillance:
    enabled: true
    datasets:
      - "data/1_raw/infectious_diseases.csv"
    analysis_types: [explore, analyze, validate]

# Run weekly
.venv/bin/python scripts/run_scheduled_analysis.py
```

### 2. Healthcare Capacity Monitoring

```bash
# Analyze hospital capacity data
.venv/bin/python scripts/auto_analyze.py \
  --dataset data/1_raw/hospital_beds.csv \
  --type analyze
```

### 3. Data Quality Audits

```bash
# Batch validate all datasets
.venv/bin/python scripts/auto_analyze.py \
  --batch data/1_raw/kaggle \
  --batch-types validate
```

## 🔧 Customization

### Add Custom Analysis Logic

Edit `scripts/auto_analyze.py`:

```python
class AutomatedAnalyzer:
    def _custom_healthcare_analysis(self, df: pd.DataFrame) -> Dict:
        """Your custom healthcare analysis"""
        return {
            "bed_utilization": ...,
            "patient_flow_metrics": ...,
        }
```

### Modify Thresholds

Edit `config/auto_analysis.yml`:

```yaml
parameters:
  missing_value_warning_threshold: 10.0  # More strict
  correlation_threshold: 0.8             # Higher threshold
  duplicate_warning_threshold: 2.0       # Lower tolerance
```

## 📚 Documentation

- Full guide: [docs/AUTOMATED_ANALYSIS.md](docs/AUTOMATED_ANALYSIS.md)
- Data plugin commands: `.github/prompts/data-plugin/commands/`
- Configuration reference: `config/auto_analysis.yml`

## ✨ Next Steps

1. **Try the demo**: `.venv/bin/python scripts/demo_auto_analysis.py`
2. **Open the notebook**: `notebooks/2_analysis/automated_analysis_demo.ipynb`
3. **Download your real data**: Use the Kaggle extraction notebook
4. **Configure schedules**: Edit `config/auto_analysis.yml`
5. **Set up automation**: Add to cron/task scheduler
6. **Integrate with LLM**: Use results as context for GPT-4/Claude

## 🆘 Troubleshooting

### Command not found: python
```bash
# Use full path to Python
/Users/qytay/Documents/GitHub/gen-e2-data-analysis-MOH/.venv/bin/python
```

### No data files
```bash
# Run the demo first to create sample data
.venv/bin/python scripts/demo_auto_analysis.py

# Or download from Kaggle
jupyter notebook notebooks/extract_from_kaggle.ipynb
```

### ModuleNotFoundError
```bash
# Install dependencies
.venv/bin/pip install pandas pyyaml numpy
```

## 🎉 You're Ready!

The automated analysis system is now fully functional. Start with the demo, then configure it for your healthcare data analysis needs!
