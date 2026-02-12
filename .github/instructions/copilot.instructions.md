# Copilot Instructions for Data Analysis Project

## Package Management

- **Always use `uv` for Python package management** instead of pip or conda
  - Install packages with: `uv pip install <package>`
  - Create virtual environments with: `uv venv`
  - Sync dependencies with: `uv pip sync requirements.txt`
  - Add new dependencies with: `uv pip install <package> && uv pip freeze > requirements.txt`

## Data Processing

- **Always use Polars (imported as `pl`) for DataFrame operations** instead of pandas
  - Use `import polars as pl` for all data processing tasks
  - Prefer Polars' lazy evaluation (`pl.scan_csv()`) for large datasets
  - Leverage Polars' expression API for efficient transformations
  - Use Polars for CSV, Parquet, and JSON file operations
  - Only use pandas if specific functionality is not available in Polars

## Code Examples

### Installing Dependencies
```bash
# Install a new package
uv pip install polars

# Install from requirements.txt
uv pip install -r requirements.txt
```

### Data Processing with Polars
```python
import polars as pl

# Read data
df = pl.read_csv("data.csv")

# Lazy evaluation for large files
df = pl.scan_csv("large_data.csv").collect()

# Efficient transformations
result = df.filter(pl.col("value") > 100).group_by("category").agg(pl.col("value").sum())
```
