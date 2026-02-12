# Data Cleaning Steps - Dynamic Dataset Processing

**Processing Framework**: Polars (primary), Pandas (compatibility)  
**Last Updated**: 11 February 2026

---

## Overview

This guide provides systematic data cleaning steps for any dataset. The process automatically adapts to the specific dataset structure, columns, and characteristics discovered during exploration.

### Dataset Context (Auto-Populated)

<!-- AI AGENT: Before running the cleaning pipeline, analyze the dataset and populate the following:
- Dataset source and location
- Number of files/tables to process
- Key characteristics (temporal range, entities covered, geographic scope)
- Known data quality issues from exploration phase
- Specific validation rules based on domain knowledge
-->

**Current Dataset**: {DATASET_NAME}  
**Source**: {DATA_SOURCE}  
**Files to Process**: {FILE_COUNT}  
**Temporal Coverage**: {START_DATE} to {END_DATE}  
**Domain**: {DOMAIN_TYPE} (e.g., Financial, E-commerce, IoT, Healthcare, Social Media)  
**Key Entities**: {KEY_ENTITIES} (e.g., products, customers, transactions, sensors, users)

---

## Pre-Cleaning Setup

```python
import polars as pl
import polars.selectors as cs
from pathlib import Path
from datetime import datetime
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define data paths (use project structure)
PROJECT_ROOT = Path(__file__).parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data/1_raw"
INTERIM_DATA_PATH = PROJECT_ROOT / "data/3_interim"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data/4_processed"
SCHEMAS_PATH = PROJECT_ROOT / "data/schemas"

# Load dataset exploration metadata if available
def load_dataset_context():
    """Load dataset exploration results to inform cleaning strategy"""
    # Search for any exploration/metadata JSON files in data directory
    context_files = list(PROJECT_ROOT.glob("data/*_scope.json")) + \
                   list(PROJECT_ROOT.glob("data/*_exploration.json")) + \
                   list(PROJECT_ROOT.glob("data/*_metadata.json"))
    
    context = {}
    for file in context_files:
        if file.exists():
            with open(file, 'r') as f:
                context[file.stem] = json.load(f)
    
    return context

# Get dataset context
DATASET_CONTEXT = load_dataset_context()
```

---

## Stage 1: Initial Data Loading & Inspection

### 1.1 Dynamic Schema Detection

```python
def detect_file_type_and_load(file_path: Path) -> pl.DataFrame:
    """
    Intelligently load data files based on extension and content.
    Adapts to CSV, Parquet, JSON, or Excel formats.
    """
    suffix = file_path.suffix.lower()
    
    if suffix == '.csv':
        # Auto-detect delimiter and encoding
        return pl.read_csv(
            file_path,
            infer_schema_length=10000,
            null_values=["NA", "N/A", "null", "", "-", "na", "NaN"],
            try_parse_dates=True,
            ignore_errors=False
        )
    elif suffix == '.parquet':
        return pl.read_parquet(file_path)
    elif suffix == '.json':
        return pl.read_json(file_path)
    elif suffix in ['.xlsx', '.xls']:
        return pl.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")

def auto_detect_dataset_structure(data_path: Path) -> dict:
    """
    Scan data directory and detect dataset structure.
    Returns metadata about files, schemas, and relationships.
    """
    structure = {
        "files": [],
        "total_files": 0,
        "formats": set(),
        "common_columns": set(),
        "temporal_columns": [],
        "categorical_columns": []
    }
    
    # Find all data files
    for pattern in ['*.csv', '*.parquet', '*.json']:
        files = list(data_path.rglob(pattern))
        structure["files"].extend(files)
        structure["formats"].add(pattern.split('.')[-1])
    
    structure["total_files"] = len(structure["files"])
    
    # Analyze first few files to detect common patterns
    for file in structure["files"][:5]:
        try:
            df = detect_file_type_and_load(file)
            
            # Detect temporal columns
            temporal_patterns = ['date', 'time', 'week', 'month', 'year', 'period']
            structure["temporal_columns"].extend([
                col for col in df.columns 
                if any(pattern in col.lower() for pattern in temporal_patterns)
            ])
            
            # Detect categorical columns
            for col in df.columns:
                if df[col].dtype == pl.Categorical or df[col].n_unique() < 50:
                    structure["categorical_columns"].append(col)
                    
        except Exception as e:
            logger.warning(f"Could not analyze {file}: {e}")
    
    # Remove duplicates
    structure["temporal_columns"] = list(set(structure["temporal_columns"]))
    structure["categorical_columns"] = list(set(structure["categorical_columns"]))
    
    return structure
```

### 1.2 Context-Aware Quality Checks

```python
def inspect_data_quality(df: pl.DataFrame, table_name: str, dataset_context: dict = None) -> dict:
    """
    Generate comprehensive data quality report.
    Uses dataset context to identify domain-specific issues.
    """
    report = {
        "table": table_name,
        "rows": df.height,
        "columns": df.width,
        "null_counts": df.null_count().to_dicts()[0],
        "dtypes": {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)},
        "duplicate_rows": df.is_duplicated().sum(),
        "memory_usage_mb": df.estimated_size("mb")
    }
    
    # Add domain-specific checks based on context
    if dataset_context:
        # Check for expected entities/categories dynamically
        for key, value in dataset_context.items():
            if isinstance(value, list) and len(value) > 0:
                # Look for matching column in dataframe
                matching_col = next((col for col in df.columns if key.lower() in col.lower()), None)
                if matching_col:
                    expected_values = [item if isinstance(item, str) else item.get("name", item.get("id", str(item))) 
                                     for item in value]
                    found_values = df[matching_col].unique().to_list()
                    report[f"{key}_coverage"] = {
                        "expected": len(expected_values),
                        "found": len(found_values),
                        "missing": list(set(expected_values) - set(found_values))
                    }
        
        # Check temporal coverage
        if "temporal_coverage" in dataset_context:
            expected_range = dataset_context["temporal_coverage"]
            temporal_col = next((col for col in df.columns if 'year' in col.lower() or 'date' in col.lower()), None)
            if temporal_col:
                actual_min = df[temporal_col].min()
                actual_max = df[temporal_col].max()
                report["temporal_alignment"] = {
                    "expected_start": expected_range.get("start_year", expected_range.get("start_date")),
                    "expected_end": expected_range.get("end_year", expected_range.get("end_date")),
                    "actual_start": actual_min,
                    "actual_end": actual_max
                }
    
    return report
```

---

## Stage 2: Column Standardization

### 2.1 Standardize Column Names

**Known Issues**: Inconsistent capitalization, spacing, special characters

```python
def standardize_column_names(df: pl.DataFrame) -> pl.DataFrame:
    """Convert to snake_case and remove special characters"""
    import re
    
    def to_snake_case(text: str) -> str:
        # Remove special characters
        text = re.sub(r'[^\w\s-]', '', text)
        # Replace spaces/hyphens with underscore
        text = re.sub(r'[-\s]+', '_', text)
        # Convert to lowercase
        text = text.lower()
        # Remove leading/trailing underscores
        return text.strip('_')
    
    return df.rename({col: to_snake_case(col) for col in df.columns})
```

### 2.2 Dynamic Temporal Column Standardization

```python
def standardize_temporal_columns(df: pl.DataFrame) -> pl.DataFrame:
    """
    Intelligently detect and standardize temporal columns.
    Handles: year, dates, week_ending, month, period, financial_year, etc.
    """
    
    # Detect all temporal-like columns
    temporal_patterns = {
        'year': ['year', 'yr', 'fiscal_year', 'financial_year', 'calendar_year', 'data_year'],
        'date': ['date', 'dt', 'timestamp'],
        'week': ['week', 'week_ending', 'week_ending_date', 'epiweek'],
        'month': ['month', 'mth', 'month_year'],
        'quarter': ['quarter', 'qtr', 'fiscal_quarter']
    }
    
    standardized_cols = {}
    
    for col in df.columns:
        col_lower = col.lower()
        
        # Check which temporal type this column matches
        for standard_name, variants in temporal_patterns.items():
            if any(variant in col_lower for variant in variants):
                standardized_cols[col] = standard_name
                break
    
    # Rename columns to standardized names
    for original, standard in standardized_cols.items():
        if standard in df.columns and original != standard:
            # Column already exists, create a derived column
            df = df.rename({original: f"{standard}_alt"})
        else:
            df = df.rename({original: standard})
    
    # Convert to appropriate types
    if 'year' in df.columns:
        df = df.with_columns(
            pl.col("year").cast(pl.Int32, strict=False)
        )
    
    if 'date' in df.columns:
        df = df.with_columns(
            pl.col("date").str.to_date(strict=False)
        )
    
    if 'week_ending' in df.columns or 'week' in df.columns:
        week_col = 'week_ending' if 'week_ending' in df.columns else 'week'
        df = df.with_columns(
            pl.col(week_col).str.to_date(strict=False)
        )
    
    return df
```

### 2.3 Dynamic Category Standardization

```python
def standardize_categories(df: pl.DataFrame, dataset_context: dict = None) -> pl.DataFrame:
    """
    Standardize categorical values based on discovered patterns.
    Uses dataset context and common variations.
    """boolean/binary variations
        "status": {
            "active": "Active", "Active": "Active", "ACTIVE": "Active",
            "inactive": "Inactive", "Inactive": "Inactive", "INACTIVE": "Inactive",
            "yes": "Yes", "YES": "Yes", "Y": "Yes",
            "no": "No", "NO": "No", "N": "No",
            "true": "True", "TRUE": "True", "1": "True",
            "false": "False", "FALSE": "False", "0": "False"
        },
        # Common gender variations
        "gender": {
            "M": "Male", "m": "Male", "male": "Male",
            "F": "Female", "f": "Female", "female": "Female"
        },
        "sex": {
            "M": "Male", "m": "Male", "male": "Male",
            "F": "Female", "f": "Female", "female": "Female"
        }
    }
    
    # Add domain-specific mappings from context
    if dataset_context:
        for context_key, context_value in dataset_context.items():
            if isinstance(context_value, dict) and "mappings" in context_value:
                # Use provided mappings from context
                category_mappings[context_key] = context_value["mappings"]
            elif isinstance(context_value, list) and len(context_value) > 0:
                # Auto-generate case-insensitive mappings
                standardization = {}
                for item in context_value:
                    canonical = item if isinstance(item, str) else str(item)
                    # Add common variations
                    standardization[canonical.lower()] = canonical
                    standardization[canonical.upper()] = canonical
                    standardization[canonical.title()] = canonical
                if standardization:
                    category_mappings[context_key] = standardization] = "HFMD"
                disease_variations["Hand Foot Mouth Disease"] = "HFMD"
        
        if disease_variations:
            category_mappings["disease"] = disease_variations
    
    # Apply standardization to matching columns
    for col in df.columns:
        col_lower = col.lower()
        
        # Find matching category type
        for category_type, mapping in category_mappings.items():
            if category_type in col_lower:
                df = df.with_columns(
                    pl.col(col)
                    .str.strip_chars()
                    .replace(mapping, default=pl.col(col))
                )
                break
    
    return df
```

---

## Stage 3: Data Type Validation & Conversion

### 3.1 Enforce Data Types

```python
def enforce_data_types(df: pl.DataFrame, table_name: str) -> pl.DataFrame:
    """Apply appropriate data types based on column patterns"""
    
    # Year columns → Int32
    year_cols = [c for c in df.columns if "year" in c.lower()]
    if year_cols:
        df = df.with_columns([
            pl.col(c).cast(pl.Int32, strict=False) for c in year_cols
        ])
    
    # Count/number columns → Int64
    count_cols = [c for c in df.columns 
                  if any(term in c.lower() for term in ["count", "number", "total"])]
    if count_cols:
        df = df.with_columns([
            pl.col(c).cast(pl.Int64, strict=False) for c in count_cols
        ])
    
    # Rate/percentage columns → Float64
    rate_cols = [c for c in df.columns 
                 if any(term in c.lower() for term in ["rate", "ratio", "percentage", "percent"])]
    if rate_cols:
        df = df.with_columns([
            pl.col(c).cast(pl.Float64, strict=False) for c in rate_cols
        ])
    
    # Categorical columns → Categorical
    categorical_cols = [c for c in df.columns 
                       if any(term in c.lower() for term in ["sector", "level", "type", "category", "sex", "gender", "race"])]
    if categorical_cols:
        df = df.with_columns([
            pl.col(c).cast(pl.Categorical) for c in categorical_cols
        ])
    
    return df
```

### 3.2 Validate Numeric Ranges

```python
def validate_numeric_ranges(df: pl.DataFrame) -> pl.DataFrame:
    """Ensure numeric values are within expected ranges"""
    
    # Percentage/rate validation (0-100 or 0-1 depending on scale)
    for col in df.columns:
        if "percentage" in col.lower() or "percent" in col.lower():
            df = df.with_columns(
                pl.when(
                    (pl.col(col) < 0) | (pl.col(col) > 100)
                ).then(None)
                .otherwise(pl.col(col))
                .alias(col)
            )
        
        # Year validation (1900-2030)
        if "year" in col.lower():
            df = df.with_columns(
                pl.when(
                    (pl.col(col) < 1900) | (pl.col(col) > 2030)
                ).then(None)
                .otherwise(pl.col(col))
                .alias(col)
            )
        
        # Count validation (non-negative)
        if any(term in col.lower() for term in ["count", "number", "total"]):
            df = df.with_columns(
                pl.when(pl.col(col) < 0)
                .then(None)
                .otherwise(pl.col(col))
                .alias(col)
            )
    
    return df
```

---

## Stage 4: Data Quality Validation

### 4.1 Handle Missing Values

```python
def handle_missing_values(df: pl.DataFrame, strategy: str = "flag") -> pl.DataFrame:
    """Handle missing values with explicit strategy"""
    
    if strategy == "flag":
        # Add flag columns for missing data
        for col in df.columns:
            if df[col].null_count() > 0:
                df = df.with_columns(
                    pl.col(col).is_null().alias(f"{col}_is_missing")
                )
    
    elif strategy == "forward_fill":
        # Forward fill for time series (use with caution)
        df = df.with_columns([
            pl.col(c).forward_fill() for c in df.columns
        ])
    
    elif strategy == "interpolate":
        # Linear interpolation for numeric columns
        numeric_cols = df.select(cs.numeric()).columns
        df = df.with_columns([
            pl.col(c).interpolate() for c in numeric_cols
        ])
    
    return df
```

### 4.2 Detect and Handle Duplicates

```python
def handle_duplicates(df: pl.DataFrame, subset: list = None) -> pl.DataFrame:
    """Remove or flag duplicate rows"""
    
    # Log duplicate information
    duplicate_count = df.is_duplicated().sum()
    if duplicate_count > 0:
        logger.warning(f"Found {duplicate_count} duplicate rows")
        
        # Keep first occurrence, remove duplicates
        if subset:
            df = df.unique(subset=subset, keep="first")
        else:
            df = df.unique(keep="first")
    , dataset_context: dict = None) -> pl.DataFrame:
    """Apply domain-specific validation rules dynamically"""
    
    # Common validation: counts should be non-negative
    count_cols = [c for c in df.columns if any(term in c.lower() for term in ["count", "quantity", "amount", "number"])]
    for col in count_cols:
        if df[col].dtype in [pl.Int32, pl.Int64, pl.Float32, pl.Float64]:
            df = df.filter(pl.col(col) >= 0)
    
    # Rate/percentage validation
    rate_cols = [c for c in df.columns if any(term in c.lower() for term in ["rate", "percentage", "percent", "ratio"])]
    for col in rate_cols:
        if df[col].dtype in [pl.Float32, pl.Float64]:
            df = df.filter(pl.col(col) >= 0)
    
    # Temporal consistency
    if "year" in df.columns:
        # Remove future years
        current_year = datetime.now().year
        df = df.filter(pl.col("year") <= current_year)
    
    # Price/currency validation (positive values)
    price_cols = [c for c in df.columns if any(term in c.lower() for term in ["price", "cost", "revenue", "sales", "value"])]
    for col in price_cols:
        if df[col].dtype in [pl.Float32, pl.Float64]:
            df = df.filter(pl.col(col) >= 0)
    
    # Apply custom validation rules from context
    if dataset_context and "validation_rules" in dataset_context:
        for rule in dataset_context["validation_rules"]:
            col = rule.get("column")
            if col in df.columns:
                if "min" in rule:
                    df = df.filter(pl.col(col) >= rule["min"])
                if "max" in rule:
                    df = df.filter(pl.col(col) <= rule["max"])
                if "allowed_values" in rule:
                    df = df.filter(pl.col(col).is_in(rule["allowed_values"])
            df = df.filter(pl.col(col) >= 0)
    
    # Temporal consistency
    if "year" in df.columns:
        # Remove future years
        current_year = datetime.now().year
        df = df.filter(pl.col("year") <= current_year)
    
    return df
```

---

## Stage 5: Rate Standardization

### 5.1 Normalize Rate Bases

**Known Issue**: Mixed rate bases (per 1,000 vs per 10,000 vs per 100,000)

```python
def standardize_rate_base(df: pl.DataFrame, target_base: int = 100000) -> pl.DataFrame:
    """Standardize all rates to common base (default: per 100,000)"""
    
    # Detect rate columns and their bases from metadata/column names
    rate_cols = [c for c in df.columns if "rate" in c.lower()]
    
    for col in rate_cols:
        # Infer base from column name or typical ranges
        if "per_1000" in col.lower() or "per_thousand" in col.lower():
            current_base = 1000
        elif "per_10000" in col.lower() or "per_ten_thousand" in col.lower():
            current_base = 10000
        elif "per_100000" in col.lower() or "per_hundred_thousand" in col.lower():
            current_base = 100000
        else:
            # Infer from data range (heuristic)
            max_val = df[col].max()
            if max_val < 100:
                current_base = 1000
            elif max_val < 1000:
                current_base = 10000
            else:
                current_base = 100000
        
        # Convert to target base
        if current_base != target_base:
            conversion_factor = target_base / current_base
            df = df.with_columns(
                (pl.col(col) * conversion_factor).alias(col)
            )
            
            # Update column name to reflect new base
            new_col_name = col.replace(f"per_{current_base}", f"per_{target_base}")
            df = df.rename({col: new_col_name})
    
    return df
```

---

## Stage 6: Feature Engineering for Consistency

### 6.1 Add Metadata Columns

```python
def add_metadata_columns(df: pl.DataFrame, table_name: str, source: str = "kaggle") -> pl.DataFrame:
    """Add tracking and lineage columns"""
    
    return df.with_columns([
        pl.lit(table_name).alias("source_table"),
        pl.lit(source).alias("data_source"),
        pl.lit(datetime.now()).alias("processed_timestamp"),
        pl.lit(datetime.now().strftime("%Y%m%d")).cast(pl.Int32).alias("processing_batch")
    ])
```

### 6.2 Create Standardized IDs

```python
def create_record_ids(df: pl.DataFrame, key_columns: list) -> pl.DataFrame:
    """Generate unique identifiers for each record"""
    
    # Create composite key
    if key_columns:
        df = df.with_columns(
            pl.concat_str(
                [pl.col(c).cast(pl.Utf8) for c in key_columns],
                separator="_"
            ).alias("record_key")
        )
    
    # Add sequential ID
    df = df.with_row_count(name="record_id", offset=1)
    
    return df
```

---

## Stage 7: Output & Validation

### 7.1 Save Cleaned Data

```python
def save_cleaned_data(df: pl.DataFrame, table_name: str, format: str = "parquet"):
    """Save processed data with validation"""
    
    output_path = PROCESSED_DATA_PATH / f"{table_name}.{format}"
    
    if format == "parquet":
        df.write_parquet(
            output_path,
            compression="zstd",  # Better compression than snappy
            statistics=True,
            use_pyarrow=False
        )
    elif format == "csv":
        df.write_csv(output_path)
    
    logger.info(f"Saved {table_name}: {df.height} rows, {df.width} columns → {output_path}")
    
    return output_path
```

### 7.2 Generate Data Quality Report

```python
def generate_cleaning_report(original_df: pl.DataFrame, cleaned_df: pl.DataFrame, table_name: str) -> dict:
    """Compare before/after statistics"""
    dataset_table(file_path: Path, table_name: str, dataset_context: dict = None) -> pl.DataFrame:
    """
    Complete data cleaning pipeline for any dataset
    
    Args:
        file_path: Path to raw data file
        table_name: Name identifier for the table
        dataset_context: Optional context dictionary with domain-specific rules
        
    Returns:
        Cleaned Polars DataFrame
    """
    
    logger.info(f"Starting cleaning pipeline for: {table_name}")
    
    # Stage 1: Load
    df_original = detect_file_type_and_load(file_path)
    logger.info(f"Loaded {df_original.height} rows, {df_original.width} columns")
    
    # Stage 2: Standardize columns
    df = standardize_column_names(df_original)
    df = standardize_temporal_columns(df)
    df = standardize_categories(df, dataset_context)
    
    # Stage 3: Data types
    df = enforce_data_types(df, table_name)
    df = validate_numeric_ranges(df)
    
    # Stage 4: Quality validation
    df = handle_missing_values(df, strategy="flag")
    df = handle_duplicates(df)
    df = validate_business_rules(df, table_name, dataset_context)
    
    # Stage 5: Rate standardization (if applicable)
    if any("rate" in col.lower() for col in df.columns):
        df = standardize_rate_base(df, target_base=100000)
    
    # Stage 6: Feature engineering
    # Auto-detect key columns for ID generation
    key_cols = []
    for potential_key in ["year", "date", "id", "category", "type", "region", "product_id", "user_id"]:
        if potential_key in df.columns:
            key_cols.append(potential_key)
    
    df = create_record_ids(df, key_cols[:3])  # Limit to 3 key columnsth)
    logger.info(f"Loaded {df_original.height} rows, {df_original.width} columns")
    
    # Stage 2: Standardize columns
    df = standardize_column_names(df_original)
    df = standardize_temporal_columns(df)
    df = standardize_categories(df)
    
    # Stage 3: Data types
    df = enfortables(dataset_path: Path, dataset_context: dict = None) -> dict:
    """Process all data files from dataset"""
    
    results = {}
    
    # Find all supported data files
    data_files = []
    for pattern in ['*.csv', '*.parquet', '*.json']:
        data_files.extend(list(dataset_path.rglob(pattern)))
    
    logger.info(f"Found {len(data_files)} data files to process")
    
    for data_file in data_files:
        table_name = data_file.stem  # Filename without extension
        
        try:
            df_cleaned = clean_dataset_table(data_file, table_name, dataset_context
        key_cols.append("sector")
    df = create_record_ids(df, key_cols)
    df = add_metadata_columns(df, table_name)
    
    # Stage 7: Save and report
    save_cleaned_data(df, table_name, format="parquet")
    report = generate_cleaning_report(df_original, df, table_name)
    logger.info(f"Cleaning complete: {report}")
    
    return df
```

### Batch Processing for All Tables

```python
def clean_all_moh_tables(dataset_path: Path) -> dict:
    """Process all 35 CSV tables from MOH dataset"""
    
    results = {}
    
    # Find all CSV files
    csv_files = list(dataset_path.rglob("*.csv"))
    logger.info(f"Found {len(csv_files)} CSV files to process")
    
    for csv_file in csv_files:
        table_name = csv_file.stem  # Filename without extension
        
        try:
            df_cleaned = clean_moh_table(csv_file, table_name)
            results[table_name] = {
                "status": "success",
                "rows": df_cleaned.height,
                "columns": df_cleaned.width
            }
        except Exception as e:
            logger.error(f"Failed to clean {table_name}: {e}")
            results[table_name] = {
                "status": "failed",
                "error": str(e)
            }
    
    return results
```

---

## Best Practices Summary

### ✓ Do's

1. **Use Polars for large datasets** - 10-100x faster than Pandas
2. **Preserve original data** - Never overwrite raw files
3. **Log all transformations** - Maintain audit trail
4. **Validate after each stage** - Catch issues early
5. **Use lazy evaluation** - Chain operations efficiently with `.lazy()`
6. **Save as Parquet** - Better compression and faster reads
7. **Document assumptions** - Comment business logic
8. **Version control schemas** - Track data structure changes

### ✗ Don'ts

1. **Don't assume no nulls** - Always validate despite "100% completeness" claim
2. **Don't drop data silently** - Log all removals
3. **Don't mix temporal granularities** - Align to common period
4. **Don't ignore data types** - Enforce strict typing
5. **Don't skip validation** - Always run quality checks
6. **Don't hardcode paths** - Use Path objects and config files
7. **Don't process in-place** - Create new columns/dataframes
8. **Don't forget memory management** - Monitor RAM usage for large operations

---

## Performance Optimization Tips

### Memory Efficiency

```python
# Use lazy evaluation for large datasets
df_lazy = pl.scan_csv("large_file.csv")
result = (
    df_lazy
    .select(["year", "sector", "count"])
    .filter(pl.col("year") >= 2015)
    .group_by(["year", "sector"])
    .agg(pl.col("count").sum())
    .collect(streaming=True)  # Process in batches
)
```

### Parallel Processing

```python
from multiprocessing import Pool

def process_table_wrapper(args):
    file_path, table_name = args
    return clean_moh_table(file_path, table_name)

# Process multiple tables in parallel
with Pool(processes=4) as pool:
    results = pool.map(process_table_wrapper, 
                      [(fp, fp.stem) for fp in csv_files])
```

---

## Validation Checklist

Before marking data as "clean", verify:

- [ ] All column names follow snake_case convention
- [ ] Temporal columns aligned (unified "year" column)
- [ ] Categorical values standardized
- [ ] Data types correctly enforced
- [ ] Numeric ranges validated
- [ ] Duplicates removed or flagged
- [ ] Missing values handled explicitly
- [ ] Rate bases standardized
- [ ] Business rules validated
- [ ] Metadata columns added
- [ ] Output saved in efficient format
- [ ] Quality report generated
- [ ] Processing logged

---

**Document Owner**: Data Analytics Team  
**Last Validated**: 9 February 2026  
**Framework**: Polars 0.20+, Python 3.10+
