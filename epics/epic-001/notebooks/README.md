# Epic 001: Exploratory Notebook Template

This notebook template is provided for ad-hoc exploration and analysis.

## Usage

```python
import sys
from pathlib import Path

# Add src to path
epic_root = Path.cwd().parent
sys.path.insert(0, str(epic_root / 'src'))

# Import modules
from extraction import FacilityDataExtractor
from features import UtilizationFeatureEngineer
from analysis import FacilityAnalyzer
from visualization import UtilizationVisualizer
from utils import load_config

# Load configuration
config = load_config(epic_root / 'config' / 'epic_001_config.yml')
```

## Example Notebooks

Create Jupyter notebooks in this directory for:

1. **01_exploration.ipynb**: Initial data exploration
2. **02_feature_analysis.ipynb**: Feature distribution analysis
3. **03_modeling.ipynb**: Experimental modeling
4. **04_results_viz.ipynb**: Results visualization

## Starting Jupyter

```bash
jupyter notebook notebooks/
```
