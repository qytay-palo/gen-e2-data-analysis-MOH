# Python Best Practices for Data Analytics Projects

## 1. Code Organization and Structure

### Project Structure
- Follow a consistent directory structure separating raw data, processed data, notebooks, scripts, and source code
- Use `src/` for reusable modules, `scripts/` for one-off tasks, `notebooks/` for exploratory analysis
- Store parameter files (JSON, YAML) in relevant data folders (e.g., `data/schemas/`, `data/parameters/`)
- Store all outputs (figures, tables, models) in a `results/` or `outputs/` directory

### Module Design
- **Single Responsibility Principle**: Each function/class should do one thing well
- **DRY (Don't Repeat Yourself)**: Extract repeated code into reusable functions
- Use meaningful, descriptive names: `calculate_disease_burden()` not `calc_db()`
- Keep functions short (< 50 lines) and focused on a single task
- Group related functions into modules with clear purposes

### Package Structure
```python
# Good: Clear imports and structure
from src.data_processing.validation import validate_date_range
from src.analysis.trend_analysis import detect_seasonal_patterns

# Avoid: Unclear star imports
from src.data_processing import *
```

## 2. Data Handling Best Practices

### Data Loading and Validation
- **Always validate input data** upon loading
- Check for expected columns, data types, and ranges
- Handle missing values explicitly - never ignore them silently
- Document data assumptions and constraints

```python
def load_disease_data(filepath: str) -> pd.DataFrame:
    """Load and validate disease surveillance data.
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        Validated DataFrame
        
    Raises:
        ValueError: If required columns are missing or data is invalid
    """
    df = pd.read_csv(filepath)
    
    # Validate required columns
    required_cols = ['disease', 'date', 'case_count']
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Validate data types and ranges
    df['date'] = pd.to_datetime(df['date'])
    df['case_count'] = pd.to_numeric(df['case_count'], errors='coerce')
    
    if df['case_count'].isna().any():
        raise ValueError("Invalid case_count values found")
    
    return df
```

### Data Processing Pipeline
- **Immutability**: Avoid modifying DataFrames in-place when possible
- Use method chaining for readability
- Create intermediate checkpoints for complex transformations
- Save processed data with clear versioning

```python
# Good: Clear pipeline with intermediate results
df_processed = (
    df_raw
    .copy()
    .dropna(subset=['critical_column'])
    .assign(
        year=lambda x: x['date'].dt.year,
        month=lambda x: x['date'].dt.month
    )
    .query('year >= 2020')
    .sort_values(['disease', 'date'])
)

# Save intermediate results
df_processed.to_csv('data/3_interim/cleaned_data.csv', index=False)
```

### Memory Management
- Use appropriate data types: `int32` instead of `int64`, `category` for categorical data
- Process large datasets in chunks when memory is constrained
- Delete unnecessary DataFrames explicitly with `del` when done
- Use `pd.read_csv(..., usecols=[...])` to load only needed columns

## 3. Type Hints and Documentation

### Type Annotations
- **Always use type hints** for function parameters and return values
- Use `typing` module for complex types
- Helps catch bugs early and improves code readability

```python
from typing import List, Dict, Optional, Tuple
import pandas as pd
import numpy as np

def calculate_incidence_rate(
    cases: pd.Series,
    population: int,
    multiplier: int = 100_000
) -> np.ndarray:
    """Calculate incidence rate per population."""
    return (cases / population) * multiplier

def aggregate_by_disease(
    df: pd.DataFrame,
    groupby_cols: List[str]
) -> Dict[str, pd.DataFrame]:
    """Aggregate data by disease categories."""
    return {name: group for name, group in df.groupby(groupby_cols)}
```

### Docstrings
- Use **Google or NumPy style docstrings** consistently
- Document parameters, return values, and exceptions
- Include example usage for complex functions
- Explain the "why" not just the "what"

```python
def detect_outbreak(
    time_series: pd.Series,
    threshold_std: float = 2.0,
    window: int = 4
) -> pd.Series:
    """Detect potential disease outbreaks using moving statistics.
    
    Identifies weeks where case counts exceed the moving average by
    more than threshold_std standard deviations, indicating potential
    outbreak conditions.
    
    Args:
        time_series: Weekly case counts indexed by date
        threshold_std: Number of standard deviations above mean to flag
        window: Size of rolling window in weeks for calculating baseline
        
    Returns:
        Boolean series where True indicates potential outbreak week
        
    Raises:
        ValueError: If time_series contains negative values
        
    Example:
        >>> cases = pd.Series([10, 12, 11, 45, 50, 15, 12])
        >>> outbreaks = detect_outbreak(cases, threshold_std=2.0)
        >>> print(outbreaks.sum())  # Count of outbreak weeks
        2
    """
    if (time_series < 0).any():
        raise ValueError("Case counts cannot be negative")
    
    rolling_mean = time_series.rolling(window=window).mean()
    rolling_std = time_series.rolling(window=window).std()
    
    threshold = rolling_mean + (threshold_std * rolling_std)
    return time_series > threshold
```

## 4. Error Handling and Logging

### Exception Handling
- Use specific exception types, not bare `except:`
- Provide informative error messages with context
- Fail fast - validate inputs early
- Use custom exceptions for domain-specific errors

```python
class DataValidationError(Exception):
    """Raised when data validation fails."""
    pass

def process_disease_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process disease surveillance data with validation."""
    try:
        # Validate data structure
        if df.empty:
            raise DataValidationError("Input DataFrame is empty")
        
        if 'date' not in df.columns:
            raise DataValidationError("Missing required 'date' column")
        
        # Process data
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Check for conversion failures
        invalid_dates = df['date'].isna().sum()
        if invalid_dates > 0:
            raise DataValidationError(
                f"Found {invalid_dates} invalid date values"
            )
        
        return df
        
    except pd.errors.ParserError as e:
        raise DataValidationError(f"Failed to parse data: {e}") from e
    except Exception as e:
        # Log unexpected errors for debugging
        logger.error(f"Unexpected error processing data: {e}")
        raise
```

### Logging
- Use Python's `logging` module, not `print()` statements
- Set appropriate log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Include context in log messages (function name, relevant IDs)
- Configure logging from a central location

```python
import logging

# Configure at module level
logger = logging.getLogger(__name__)

def calculate_metrics(disease: str, df: pd.DataFrame) -> Dict:
    """Calculate disease burden metrics."""
    logger.info(f"Calculating metrics for {disease}")
    logger.debug(f"Input data shape: {df.shape}")
    
    try:
        metrics = {
            'total_cases': df['cases'].sum(),
            'mean_weekly': df['cases'].mean()
        }
        logger.info(f"Successfully calculated {len(metrics)} metrics")
        return metrics
        
    except KeyError as e:
        logger.error(f"Missing required column for {disease}: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error calculating metrics: {e}")
        raise
```

## 5. Testing and Quality Assurance

### Unit Testing
- Write tests for all business logic and data transformations
- Use `pytest` for testing framework
- Aim for >80% code coverage
- Test edge cases, not just happy paths

```python
import pytest
import pandas as pd
from src.analysis.trend_analysis import detect_outbreak

def test_detect_outbreak_with_spike():
    """Test outbreak detection identifies clear spike."""
    cases = pd.Series([10, 10, 10, 50, 10, 10])
    result = detect_outbreak(cases, threshold_std=2.0, window=3)
    assert result[3] == True  # Spike should be detected

def test_detect_outbreak_with_negative_values():
    """Test that negative values raise ValueError."""
    cases = pd.Series([10, -5, 10])
    with pytest.raises(ValueError, match="cannot be negative"):
        detect_outbreak(cases)

def test_detect_outbreak_empty_series():
    """Test handling of empty input."""
    cases = pd.Series([], dtype=float)
    result = detect_outbreak(cases)
    assert len(result) == 0
```

### Data Quality Checks
- Implement automated data quality checks in pipelines
- Check for duplicates, nulls, outliers, and inconsistencies
- Document data quality issues and handling strategies
- Create data quality reports

```python
def run_data_quality_checks(df: pd.DataFrame) -> Dict[str, any]:
    """Run comprehensive data quality checks."""
    quality_report = {
        'total_rows': len(df),
        'duplicate_rows': df.duplicated().sum(),
        'missing_values': df.isna().sum().to_dict(),
        'negative_values': (df.select_dtypes(include=[np.number]) < 0).sum().to_dict(),
        'date_range': {
            'min': df['date'].min() if 'date' in df else None,
            'max': df['date'].max() if 'date' in df else None
        }
    }
    
    logger.info(f"Data quality report: {quality_report}")
    return quality_report
```

## 6. Performance Optimization

### Vectorization
- Use vectorized pandas/numpy operations instead of loops
- Avoid `apply()` with lambda functions when vectorization is possible
- Use `@njit` from numba for computationally intensive operations

```python
# Bad: Slow loop
for idx, row in df.iterrows():
    df.at[idx, 'rate'] = (row['cases'] / row['population']) * 100000

# Good: Vectorized operation
df['rate'] = (df['cases'] / df['population']) * 100000

# Even better: Using assign for immutability
df = df.assign(rate=lambda x: (x['cases'] / x['population']) * 100000)
```

### Efficient Data Operations
- Use categorical data types for repeated string values
- Leverage `query()` for faster filtering
- Use `eval()` for complex arithmetic operations on large DataFrames
- Consider `dask` for datasets that don't fit in memory

```python
# Optimize data types
df['disease'] = df['disease'].astype('category')
df['year'] = df['year'].astype('int16')

# Fast filtering with query
high_burden = df.query('case_count > @threshold and year >= 2020')

# Fast arithmetic with eval
df = df.eval('incidence_rate = (cases / population) * 100000')
```

## 7. Parameters and Constants Management

### Define Parameters as Constants or Load from Data Folders
- Store reusable parameters as module-level constants in your code
- For complex parameters, store in JSON/YAML files within data folders (e.g., `data/parameters/`, `data/schemas/`)
- Never hardcode magic numbers without clear naming
- Use environment variables for secrets only
- Document parameter choices and rationale

```python
import json
from pathlib import Path
from typing import Dict

# Module-level constants
BASE_DATA_PATH = Path('data')
OUTBREAK_THRESHOLD_STD = 2.0  # Number of std deviations above baseline
ROLLING_WINDOW_WEEKS = 4  # Window for moving averages
HIGH_INCIDENCE_CUTOFF = 100  # Cases per 100k population (WHO definition)

def load_disease_parameters(disease: str) -> Dict:
    """Load disease-specific parameters from data folder."""
    param_file = BASE_DATA_PATH / 'parameters' / f'{disease.lower()}_params.json'
    
    if not param_file.exists():
        raise FileNotFoundError(f"Parameters not found: {param_file}")
    
    with open(param_file, 'r') as f:
        params = json.load(f)
    
    # Validate required keys
    required_keys = ['incubation_period', 'infectious_period']
    missing = set(required_keys) - set(params.keys())
    if missing:
        raise ValueError(f"Missing required parameters: {missing}")
    
    return params

# Usage
disease_params = load_disease_parameters('COVID-19')
incubation_days = disease_params['incubation_period']
```

## 8. Version Control and Reproducibility

### Git Best Practices
- **Never commit data files** - use `.gitignore`
- Never commit credentials or API keys
- Write clear, descriptive commit messages
- Commit often with logical, atomic changes
- Use branches for new features

### Reproducibility
- Pin all dependencies in `requirements.txt` with versions
- Use virtual environments (`venv`, `conda`)
- Document Python version requirements
- Set random seeds for reproducible results

```python
# Set seeds for reproducibility
import random
import numpy as np

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# requirements.txt format
"""
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
matplotlib==3.7.2
seaborn==0.12.2
"""
```

## 9. Visualization Best Practices

### Clear and Informative Plots
- Always label axes with units
- Include titles and legends
- Use appropriate color schemes (consider colorblind-friendly palettes)
- Save figures in high resolution for publications

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_disease_trend(
    df: pd.DataFrame,
    disease: str,
    save_path: Optional[str] = None
) -> None:
    """Create publication-quality disease trend plot."""
    plt.figure(figsize=(12, 6))
    
    # Use clear styling
    sns.set_style('whitegrid')
    
    # Create plot
    plt.plot(df['date'], df['cases'], linewidth=2, label=disease)
    
    # Add labels and title
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Weekly Case Count', fontsize=12)
    plt.title(f'{disease} Cases Over Time', fontsize=14, fontweight='bold')
    plt.legend(loc='best')
    
    # Format dates
    plt.gcf().autofmt_xdate()
    
    # Save with high DPI
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
```

## 10. Code Style and Formatting

### PEP 8 Compliance
- Follow PEP 8 style guide
- Use tools: `black` (formatter), `flake8` (linter), `isort` (import sorting)
- Maximum line length: 88 (black default) or 100 characters
- Use 4 spaces for indentation (never tabs)

### Naming Conventions
- Variables and functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`
- Be descriptive: `disease_burden_metrics` not `dbm`

```python
# Good naming
MAX_RETRY_ATTEMPTS = 3
DEFAULT_ANALYSIS_WINDOW = 52  # weeks

class DiseaseAnalyzer:
    """Analyzer for infectious disease surveillance data."""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self._cache = {}  # Private attribute
    
    def calculate_burden_metrics(self, disease: str) -> Dict:
        """Calculate disease burden metrics."""
        pass
    
    def _validate_input(self, data: pd.DataFrame) -> bool:
        """Private method for input validation."""
        pass
```

## 11. Data Privacy and Security

### Protected Health Information (PHI)
- Never log or print sensitive data
- Anonymize/aggregate data before sharing
- Use secure file permissions
- Document data handling procedures

```python
def export_aggregated_data(df: pd.DataFrame, output_path: str) -> None:
    """Export aggregated data with no PHI."""
    # Aggregate to prevent re-identification
    aggregated = df.groupby(['disease', 'year', 'week']).agg({
        'case_count': 'sum',
        'population': 'first'
    }).reset_index()
    
    # Remove any potentially identifiable information
    safe_columns = ['disease', 'year', 'week', 'case_count']
    aggregated[safe_columns].to_csv(output_path, index=False)
    
    logger.info(f"Exported aggregated data to {output_path}")
```

## 12. Notebook Best Practices

### Jupyter Notebooks
- Use notebooks for exploration, not production code
- Keep notebooks under 100 cells
- Extract reusable code into modules
- Clear outputs before committing to version control
- Use markdown cells to document analysis workflow

```python
# Cell 1: Imports and setup
import pandas as pd
import numpy as np
from src.data_processing.validation import load_disease_data

# Cell 2: Document objective
"""
## Objective
Analyze seasonal patterns in respiratory diseases for 2020-2023

## Data Source
Weekly surveillance data from MOH infectious disease bulletin
"""

# Cell 3: Load and validate data
df = load_disease_data('data/1_raw/disease_data.csv')
print(f"Loaded {len(df):,} records")

# Cell 4: Basic exploration
df.info()
df.describe()
```

## 13. Dependencies Management

### Requirements Management
- Separate development and production dependencies
- Use `requirements-dev.txt` for testing/linting tools
- Document optional dependencies
- Keep dependencies up to date but test updates thoroughly

```txt
# requirements.txt (production)
pandas>=2.0.0,<3.0.0
numpy>=1.24.0,<2.0.0
pyyaml>=6.0

# requirements-dev.txt (development)
-r requirements.txt
pytest>=7.4.0
black>=23.0.0
flake8>=6.0.0
jupyter>=1.0.0
```

## 14. Documentation

### Project Documentation
- Maintain README.md with project overview and setup instructions
- Document data sources, methodologies, and assumptions
- Create data dictionaries for all datasets
- Keep a CHANGELOG.md for tracking updates

### Code Comments
- Comment the "why" not the "what"
- Avoid redundant comments
- Update comments when code changes
- Use TODO comments for future improvements

```python
# Good: Explains reasoning
# Use 4-week window to smooth out weekly reporting variations
# while still capturing monthly trends
rolling_avg = df['cases'].rolling(window=4).mean()

# Bad: States the obvious
# Calculate rolling average
rolling_avg = df['cases'].rolling(window=4).mean()

# TODO: Implement automated anomaly detection for data quality
# See issue #45 for algorithm selection discussion
```

## 15. Anti-Patterns: What Should NOT Exist

#### ❌ Hardcoded Values
```python
# BAD: Magic numbers and hardcoded paths
df = pd.read_csv('/Users/john/Desktop/data.csv')
threshold = 42  # What does 42 mean?
if cases > 100:  # Why 100?
    flag_outbreak()

# GOOD: Named constants with clear meaning
BASE_DATA_PATH = Path('data/1_raw')
RAW_DATA_FILE = BASE_DATA_PATH / 'surveillance_data.csv'
OUTBREAK_THRESHOLD_CASES = 50  # Historical 95th percentile for this region
HIGH_BURDEN_CUTOFF = 100  # Cases per 100k population (WHO definition)

df = pd.read_csv(RAW_DATA_FILE)
if cases > HIGH_BURDEN_CUTOFF:
    flag_outbreak()
```

#### ❌ Print Statements for Debugging
```python
# BAD: Print debugging left in code
def calculate_metrics(df):
    print("Starting calculation...")
    print(f"DataFrame shape: {df.shape}")
    print(f"Columns: {df.columns}")
    result = df.groupby('disease').sum()
    print(result)  # Debugging print
    return result

# GOOD: Use proper logging
def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    logger.debug(f"Calculating metrics for DataFrame with shape {df.shape}")
    result = df.groupby('disease').sum()
    logger.info(f"Calculated metrics for {len(result)} diseases")
    return result
```

#### ❌ Silencing Errors
```python
# BAD: Bare except that hides problems
try:
    df['date'] = pd.to_datetime(df['date'])
except:
    pass  # What went wrong? We'll never know!

# BAD: Catching all exceptions without action
try:
    process_data()
except Exception:
    pass

# GOOD: Specific error handling with logging
try:
    df['date'] = pd.to_datetime(df['date'])
except (ValueError, TypeError) as e:
    logger.error(f"Failed to parse dates: {e}")
    logger.info("Attempting alternative date format...")
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
```

#### ❌ God Functions and God Classes
```python
# BAD: 500-line function that does everything
def analyze_everything(file1, file2, file3, config):
    # Load data
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    # Clean data
    # Validate data
    # Calculate metrics
    # Create visualizations
    # Generate report
    # Send email
    # ... 450 more lines
    return result

# GOOD: Break into focused, testable functions
def load_and_validate_data(filepath: str) -> pd.DataFrame:
    """Load and validate single data file."""
    pass

def calculate_disease_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate burden metrics for diseases."""
    pass

def generate_visualizations(metrics: pd.DataFrame, output_dir: str) -> List[str]:
    """Create standard visualization suite."""
    pass
```

#### ❌ Mutable Default Arguments
```python
# BAD: Mutable default arguments
def add_disease(disease: str, disease_list=[]):
    disease_list.append(disease)
    return disease_list

# This causes unexpected behavior:
# list1 = add_disease("COVID-19")
# list2 = add_disease("Dengue")  # list2 contains both!

# GOOD: Use None and create new instance
def add_disease(disease: str, disease_list: Optional[List[str]] = None) -> List[str]:
    if disease_list is None:
        disease_list = []
    disease_list.append(disease)
    return disease_list
```

#### ❌ Nested Loops for Data Operations
```python
# BAD: Nested loops on DataFrames
for i in range(len(df)):
    for col in df.columns:
        if df.iloc[i][col] < 0:
            df.iloc[i][col] = 0

# GOOD: Vectorized operations
df[df < 0] = 0
# Or for specific columns
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].clip(lower=0)
```

#### ❌ Ignoring Data Types
```python
# BAD: Everything is object type, wasting memory
df = pd.read_csv('large_file.csv')  # All columns are 'object' type

# BAD: Mixing types in analysis
year = "2023"  # String
cases = "150"   # String
rate = cases / year  # Will fail!

# GOOD: Explicit type specification and conversion
df = pd.read_csv('large_file.csv', dtype={
    'disease': 'category',
    'year': 'int16',
    'week': 'int8',
    'cases': 'int32'
})

year = 2023  # Integer
cases = 150  # Integer
rate = cases / year
```

### Files and Directories That Should NOT Exist

#### ❌ Data Files in Version Control
```bash
# These should be in .gitignore:
data/1_raw/*.csv
data/1_raw/*.xlsx
data/2_external/*.json
data/3_interim/*.parquet
data/4_processed/*.csv
*.db
*.sqlite
```

#### ❌ Credentials and Secrets
```bash
# NEVER commit these:
.env
credentials.json
*.pem
*.key
.aws/credentials
database_passwords.txt
api_keys.txt
secrets/
```

#### ❌ IDE and System Files
```bash
# Should be in .gitignore:
.DS_Store
.vscode/settings.json  # Personal settings
.idea/
*.pyc
__pycache__/
.ipynb_checkpoints/
Thumbs.db
```

#### ❌ Output Files from Runs
```bash
# Should be in .gitignore:
results/figures/*.png
results/tables/*.csv
models/*.pkl
logs/*.log
*.tmp
.cache/
```

#### ❌ Redundant or Deprecated Files
```python
# BAD: Multiple versions cluttering the repo
analysis_v1.py
analysis_v2.py
analysis_final.py
analysis_final_FINAL.py
analysis_final_really_final.py

# GOOD: Use version control properly
# Keep only: analysis.py
# Git history preserves all versions
```

### Code Patterns to Avoid

#### ❌ Copy-Paste Programming
```python
# BAD: Repeated code for each disease
covid_metrics = df[df['disease'] == 'COVID-19'].agg({
    'cases': ['sum', 'mean', 'std']
})

dengue_metrics = df[df['disease'] == 'Dengue'].agg({
    'cases': ['sum', 'mean', 'std']
})

tb_metrics = df[df['disease'] == 'Tuberculosis'].agg({
    'cases': ['sum', 'mean', 'std']
})

# GOOD: Reusable function
def calculate_disease_metrics(df: pd.DataFrame, disease: str) -> pd.DataFrame:
    """Calculate standard metrics for a specific disease."""
    return df[df['disease'] == disease].agg({
        'cases': ['sum', 'mean', 'std']
    })

# Use for all diseases
diseases = ['COVID-19', 'Dengue', 'Tuberculosis']
metrics = {d: calculate_disease_metrics(df, d) for d in diseases}
```

#### ❌ Premature Optimization
```python
# BAD: Over-engineering before understanding requirements
import numba
from multiprocessing import Pool

@numba.jit
def ultra_optimized_mean(arr):
    # Complex optimization for simple operation
    pass

# GOOD: Start simple, optimize if needed
def calculate_mean(df: pd.DataFrame, column: str) -> float:
    """Calculate mean of column."""
    return df[column].mean()

# Profile first, then optimize bottlenecks if necessary
```

#### ❌ Unclear Variable Names
```python
# BAD: Cryptic abbreviations
df1 = pd.read_csv('data.csv')
tmp = df1[df1['x'] > 5]
res = tmp.groupby('y').agg({'z': 'sum'})

# GOOD: Descriptive names
disease_data = pd.read_csv('weekly_surveillance.csv')
high_incidence_cases = disease_data[disease_data['incidence_rate'] > 5]
cases_by_region = high_incidence_cases.groupby('region').agg({
    'case_count': 'sum'
})
```

#### ❌ Modifying DataFrames In-Place Without Intent
```python
# BAD: Unintended side effects
def process_data(df):
    df.drop(columns=['temp_col'], inplace=True)  # Modifies original!
    df['new_col'] = df['old_col'] * 2
    return df

original_df = load_data()
processed_df = process_data(original_df)
# original_df is now modified unexpectedly!

# GOOD: Explicit about mutations
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process data, returns new DataFrame without modifying input."""
    return (
        df.copy()
        .drop(columns=['temp_col'])
        .assign(new_col=lambda x: x['old_col'] * 2)
    )
```

#### ❌ Not Handling Edge Cases
```python
# BAD: Assumes perfect data
def calculate_rate(cases: int, population: int) -> float:
    return (cases / population) * 100000

# What if population is 0? What if cases is negative?

# GOOD: Validate inputs and handle edge cases
def calculate_incidence_rate(
    cases: int,
    population: int
) -> Optional[float]:
    """Calculate incidence rate per 100,000 population.
    
    Returns:
        Incidence rate or None if calculation not possible
    """
    if population <= 0:
        logger.warning(f"Invalid population: {population}")
        return None
    
    if cases < 0:
        raise ValueError(f"Cases cannot be negative: {cases}")
    
    return (cases / population) * 100_000
```

#### ❌ Mixing Analysis and Presentation
```python
# BAD: Analysis code mixed with plotting
df = pd.read_csv('data.csv')
result = df.groupby('disease').sum()
plt.plot(result)  # Visualization in middle of analysis
more_results = result.apply(some_function)
plt.bar(more_results)
final = more_results.merge(other_data)

# GOOD: Separate concerns
# 1. Data loading and preparation
df = load_and_validate_data('data.csv')

# 2. Analysis
disease_totals = calculate_disease_totals(df)
burden_metrics = calculate_burden_metrics(disease_totals)

# 3. Visualization (separate function or notebook)
create_disease_trend_plot(disease_totals, save_path='results/figures/')
create_burden_heatmap(burden_metrics, save_path='results/figures/')
```

#### ❌ Not Using Context Managers
```python
# BAD: File not properly closed if error occurs
f = open('data.csv', 'r')
data = f.read()
process(data)
f.close()  # Might not execute if process() raises error

# GOOD: Context manager ensures cleanup
with open('data.csv', 'r') as f:
    data = f.read()
    process(data)
# File automatically closed even if error occurs
```

#### ❌ Overly Complex Comprehensions
```python
# BAD: Unreadable one-liner
result = [item for sublist in [[x*y for y in range(10) if y%2==0] for x in data if x>5] for item in sublist if item<100]

# GOOD: Break into readable steps
filtered_data = [x for x in data if x > 5]
even_products = []
for x in filtered_data:
    products = [x * y for y in range(10) if y % 2 == 0]
    even_products.extend(products)
result = [item for item in even_products if item < 100]

# Or use functions for clarity
def calculate_products(x: int) -> List[int]:
    return [x * y for y in range(0, 10, 2)]

result = [
    product 
    for x in data if x > 5
    for product in calculate_products(x) if product < 100
]
```

### Documentation Anti-Patterns

#### ❌ No Documentation
```python
# BAD: No docstring, unclear purpose
def proc(d, t=2):
    return d[d.x > t].groupby('y').sum()
```

#### ❌ Outdated Documentation
```python
# BAD: Documentation doesn't match implementation
def calculate_rate(cases, population):
    """Calculate mortality rate per 1000."""  # Says mortality
    return (cases / population) * 100000  # Actually incidence per 100k
```

#### ❌ Redundant Comments
```python
# BAD: Comments that just restate the code
# Loop through each row
for row in df.iterrows():
    # Get the disease name
    disease = row['disease']
    # Add to list
    disease_list.append(disease)
```

### Testing Anti-Patterns

#### ❌ No Tests At All
```python
# If your src/ directory has no corresponding tests/ directory,
# you're accumulating technical debt
```

#### ❌ Tests That Don't Actually Test
```python
# BAD: Test that can never fail
def test_calculate_metrics():
    result = calculate_metrics(df)
    assert result is not None  # Meaningless assertion
    assert True  # Always passes
```

#### ❌ Tests That Depend on External State
```python
# BAD: Test depends on specific file existing
def test_load_data():
    df = load_data('/Users/john/data.csv')  # Fails on other machines
    assert len(df) > 0

# GOOD: Use fixtures or test data
import pytest

@pytest.fixture
def sample_data(tmp_path):
    """Create temporary test data."""
    data_file = tmp_path / "test_data.csv"
    data_file.write_text("disease,cases\nCOVID-19,100\n")
    return str(data_file)

def test_load_data(sample_data):
    df = load_data(sample_data)
    assert len(df) == 1
```

## Summary Checklist

### ✅ Should Exist
- [ ] Project structure follows standard conventions
- [ ] All functions have type hints and docstrings
- [ ] Input validation and error handling implemented
- [ ] Logging configured and used appropriately
- [ ] Unit tests cover key functionality
- [ ] Code follows PEP 8 style guidelines
- [ ] Constants clearly named, no magic numbers
- [ ] Dependencies pinned in requirements.txt
- [ ] .gitignore excludes data files and credentials
- [ ] Documentation up to date
- [ ] Sensitive data handled appropriately
- [ ] Notebook outputs cleared before commit
- [ ] Code reviewed and tested before merging

### ❌ Should NOT Exist
- [ ] Print statements for debugging (use logging instead)
- [ ] Hardcoded absolute file paths or credentials
- [ ] Magic numbers without explanation
- [ ] Bare except clauses that hide errors
- [ ] Functions longer than 100 lines
- [ ] God classes that do too many things
- [ ] Data files committed to version control
- [ ] API keys or passwords in code
- [ ] Commented-out code blocks (use git history)
- [ ] Multiple "final" versions of files
- [ ] Nested loops for DataFrame operations
- [ ] Copy-pasted code repeated across files
- [ ] IDE-specific settings files
- [ ] Generated output files (figures, models)
- [ ] Temporary or debug files
- [ ] Tests that don't actually assert anything

---

**Remember**: Write code that your future self (and colleagues) will thank you for. Prioritize clarity, maintainability, and reproducibility over clever tricks.