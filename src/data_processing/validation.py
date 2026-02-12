"""Data quality validation module for infectious disease data."""
import re
from typing import Dict, List, Optional, Tuple
import polars as pl
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def validate_schema(
    df: pl.DataFrame,
    expected_columns: List[str],
    expected_dtypes: Optional[Dict[str, pl.DataType]] = None
) -> Tuple[bool, List[str]]:
    """Validate DataFrame schema against expected structure.
    
    Args:
        df: DataFrame to validate
        expected_columns: List of expected column names
        expected_dtypes: Optional dict mapping column names to expected data types
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Check columns
    actual_columns = set(df.columns)
    expected_columns_set = set(expected_columns)
    
    missing_cols = expected_columns_set - actual_columns
    if missing_cols:
        errors.append(f"Missing columns: {missing_cols}")
    
    extra_cols = actual_columns - expected_columns_set
    if extra_cols:
        errors.append(f"Unexpected columns: {extra_cols}")
    
    # Check data types if provided
    if expected_dtypes:
        for col, expected_dtype in expected_dtypes.items():
            if col in df.columns:
                actual_dtype = df[col].dtype
                if actual_dtype != expected_dtype:
                    errors.append(
                        f"Column '{col}' has type {actual_dtype}, expected {expected_dtype}"
                    )
    
    is_valid = len(errors) == 0
    return is_valid, errors


def check_missing_values(df: pl.DataFrame) -> Dict[str, float]:
    """Calculate missing value percentage for each column.
    
    Args:
        df: DataFrame to check
        
    Returns:
        Dictionary mapping column names to missing percentage
    """
    total_rows = df.height
    missing_pct = {}
    
    for col in df.columns:
        null_count = df[col].null_count()
        missing_pct[col] = (null_count / total_rows) * 100
    
    return missing_pct


def validate_epi_week_format(df: pl.DataFrame, column: str = "epi_week") -> Tuple[bool, int]:
    """Validate epidemiological week format (YYYY-Wxx).
    
    Args:
        df: DataFrame containing epi_week column
        column: Name of the epi_week column
        
    Returns:
        Tuple of (all_valid, invalid_count)
    """
    pattern = r'^\d{4}-W\d{2}$'
    
    # Check format using regex
    is_valid = df[column].str.contains(pattern)
    invalid_count = (~is_valid).sum()
    
    all_valid = invalid_count == 0
    return all_valid, invalid_count


def validate_value_ranges(
    df: pl.DataFrame,
    column: str,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None
) -> Tuple[bool, int]:
    """Validate that column values are within expected range.
    
    Args:
        df: DataFrame to validate
        column: Column name to check
        min_val: Minimum allowed value (inclusive)
        max_val: Maximum allowed value (inclusive)
        
    Returns:
        Tuple of (all_valid, violations_count)
    """
    violations = 0
    
    if min_val is not None:
        violations += (df[column] < min_val).sum()
    
    if max_val is not None:
        violations += (df[column] > max_val).sum()
    
    all_valid = violations == 0
    return all_valid, violations


def validate_temporal_completeness(
    df: pl.DataFrame,
    group_column: str,
    time_column: str,
    expected_periods: int
) -> pl.DataFrame:
    """Check temporal completeness for each group.
    
    Args:
        df: DataFrame with time series data
        group_column: Column to group by (e.g., 'disease')
        time_column: Time period column (e.g., 'epi_week')
        expected_periods: Expected number of time periods per group
        
    Returns:
        DataFrame with completeness report
    """
    completeness = df.group_by(group_column).agg(
        pl.col(time_column).n_unique().alias("actual_periods"),
        pl.lit(expected_periods).alias("expected_periods")
    ).with_columns([
        ((pl.col("actual_periods") / pl.col("expected_periods")) * 100).alias("completeness_pct"),
        (pl.col("expected_periods") - pl.col("actual_periods")).alias("missing_periods")
    ])
    
    return completeness


def generate_quality_report(
    df: pl.DataFrame,
    validations: Dict[str, any]
) -> Dict[str, any]:
    """Generate comprehensive data quality report.
    
    Args:
        df: DataFrame that was validated
        validations: Dictionary of validation results
        
    Returns:
        Dictionary containing quality report
    """
    report = {
        "total_records": df.height,
        "total_columns": len(df.columns),
        "missing_values": check_missing_values(df),
        "validations": validations,
        "quality_score": calculate_quality_score(validations)
    }
    
    return report


def calculate_quality_score(validations: Dict[str, any]) -> float:
    """Calculate overall quality score from validation results.
    
    Args:
        validations: Dictionary of validation results
        
    Returns:
        Quality score between 0-100
    """
    total_checks = len(validations)
    if total_checks == 0:
        return 100.0
    
    passed_checks = sum(1 for v in validations.values() if v.get('passed', False))
    score = (passed_checks / total_checks) * 100
    
    return score


def validate_disease_data(df: pl.DataFrame) -> Dict[str, any]:
    """Comprehensive validation for infectious disease dataset.
    
    Args:
        df: Disease surveillance DataFrame
        
    Returns:
        Dictionary containing all validation results
    """
    logger.info("Starting comprehensive data validation...")
    
    validations = {}
    
    # Schema validation
    expected_cols = ["epi_week", "disease", "no._of_cases"]
    schema_valid, schema_errors = validate_schema(df, expected_cols)
    validations["schema"] = {
        "passed": schema_valid,
        "errors": schema_errors
    }
    logger.info(f"Schema validation: {'PASSED' if schema_valid else 'FAILED'}")
    
    # Missing values check
    missing_vals = check_missing_values(df)
    has_no_missing = all(pct == 0 for pct in missing_vals.values())
    validations["missing_values"] = {
        "passed": has_no_missing,
        "percentages": missing_vals
    }
    logger.info(f"Missing values check: {'PASSED' if has_no_missing else 'FAILED'}")
    
    # Epi week format validation
    epi_valid, epi_invalid_count = validate_epi_week_format(df)
    validations["epi_week_format"] = {
        "passed": epi_valid,
        "invalid_count": epi_invalid_count
    }
    logger.info(f"Epi week format: {'PASSED' if epi_valid else 'FAILED'}")
    
    # Case count range validation (non-negative)
    if "no._of_cases" in df.columns:
        range_valid, violations = validate_value_ranges(df, "no._of_cases", min_val=0)
        validations["case_count_range"] = {
            "passed": range_valid,
            "negative_values": violations
        }
        logger.info(f"Case count range: {'PASSED' if range_valid else 'FAILED'}")
    
    # Record count validation
    from src.config import EXPECTED_RECORDS
    record_count_valid = df.height == EXPECTED_RECORDS
    validations["record_count"] = {
        "passed": record_count_valid,
        "actual": df.height,
        "expected": EXPECTED_RECORDS
    }
    logger.info(f"Record count: {'PASSED' if record_count_valid else 'FAILED'}")
    
    # Generate final report
    report = generate_quality_report(df, validations)
    logger.info(f"Data quality score: {report['quality_score']:.1f}%")
    
    return report
