"""Data profiling module for statistical analysis."""
from typing import Optional, Tuple
import numpy as np
import polars as pl
from src.utils.logger import setup_logger
from src.config import OUTLIER_IQR_THRESHOLD, OUTLIER_ZSCORE_THRESHOLD

logger = setup_logger(__name__)


def calculate_summary_statistics(
    df: pl.DataFrame,
    group_by_column: str,
    value_column: str
) -> pl.DataFrame:
    """Calculate comprehensive summary statistics by group.
    
    Args:
        df: Input DataFrame
        group_by_column: Column to group by
        value_column: Column to calculate statistics for
        
    Returns:
        DataFrame with summary statistics
    """
    logger.info(f"Calculating summary statistics for {value_column} grouped by {group_by_column}")
    
    stats = df.group_by(group_by_column).agg([
        pl.col(value_column).count().alias("count"),
        pl.col(value_column).mean().alias("mean"),
        pl.col(value_column).median().alias("median"),
        pl.col(value_column).std().alias("std"),
        pl.col(value_column).min().alias("min"),
        pl.col(value_column).max().alias("max"),
        pl.col(value_column).quantile(0.25).alias("q25"),
        pl.col(value_column).quantile(0.75).alias("q75")
    ]).with_columns([
        # Coefficient of variation
        (pl.col("std") / pl.col("mean")).alias("cv"),
        # Interquartile range
        (pl.col("q75") - pl.col("q25")).alias("iqr")
    ])
    
    return stats


def identify_outliers_iqr(
    df: pl.DataFrame,
    value_column: str,
    group_by_column: Optional[str] = None,
    threshold: float = OUTLIER_IQR_THRESHOLD
) -> pl.DataFrame:
    """Identify outliers using IQR method.
    
    Args:
        df: Input DataFrame
        value_column: Column to check for outliers
        group_by_column: Optional column to group by for group-specific outliers
        threshold: IQR multiplier (default: 1.5)
        
    Returns:
        DataFrame with outlier flag added
    """
    logger.info(f"Identifying outliers using IQR method (threshold={threshold})")
    
    if group_by_column:
        # Calculate outlier bounds per group
        bounds = df.group_by(group_by_column).agg([
            pl.col(value_column).quantile(0.25).alias("q25"),
            pl.col(value_column).quantile(0.75).alias("q75")
        ]).with_columns([
            (pl.col("q75") - pl.col("q25")).alias("iqr")
        ]).with_columns([
            (pl.col("q25") - threshold * pl.col("iqr")).alias("lower_bound"),
            (pl.col("q75") + threshold * pl.col("iqr")).alias("upper_bound")
        ])
        
        # Join bounds and flag outliers
        df_with_outliers = df.join(bounds, on=group_by_column, how="left").with_columns([
            (
                (pl.col(value_column) < pl.col("lower_bound")) |
                (pl.col(value_column) > pl.col("upper_bound"))
            ).alias("is_outlier")
        ]).drop(["q25", "q75", "iqr", "lower_bound", "upper_bound"])
        
    else:
        # Global outlier detection
        q25 = df[value_column].quantile(0.25)
        q75 = df[value_column].quantile(0.75)
        iqr = q75 - q25
        lower_bound = q25 - threshold * iqr
        upper_bound = q75 + threshold * iqr
        
        df_with_outliers = df.with_columns([
            (
                (pl.col(value_column) < lower_bound) |
                (pl.col(value_column) > upper_bound)
            ).alias("is_outlier")
        ])
    
    outlier_count = df_with_outliers["is_outlier"].sum()
    outlier_pct = (outlier_count / df_with_outliers.height) * 100
    logger.info(f"Outliers detected: {outlier_count} ({outlier_pct:.2f}%)")
    
    return df_with_outliers


def identify_outliers_zscore(
    df: pl.DataFrame,
    value_column: str,
    group_by_column: Optional[str] = None,
    threshold: float = OUTLIER_ZSCORE_THRESHOLD
) -> pl.DataFrame:
    """Identify outliers using Z-score method.
    
    Args:
        df: Input DataFrame
        value_column: Column to check for outliers
        group_by_column: Optional column to group by
        threshold: Z-score threshold (default: 3.0)
        
    Returns:
        DataFrame with Z-score and outlier flag added
    """
    logger.info(f"Identifying outliers using Z-score method (threshold={threshold})")
    
    if group_by_column:
        # Calculate group-specific z-scores
        stats = df.group_by(group_by_column).agg([
            pl.col(value_column).mean().alias("group_mean"),
            pl.col(value_column).std().alias("group_std")
        ])
        
        df_with_z = df.join(stats, on=group_by_column, how="left").with_columns([
            ((pl.col(value_column) - pl.col("group_mean")) / pl.col("group_std")).alias("z_score")
        ]).with_columns([
            (pl.col("z_score").abs() > threshold).alias("is_outlier_zscore")
        ]).drop(["group_mean", "group_std"])
        
    else:
        # Global z-score
        mean = df[value_column].mean()
        std = df[value_column].std()
        
        df_with_z = df.with_columns([
            ((pl.col(value_column) - mean) / std).alias("z_score")
        ]).with_columns([
            (pl.col("z_score").abs() > threshold).alias("is_outlier_zscore")
        ])
    
    outlier_count = df_with_z["is_outlier_zscore"].sum()
    outlier_pct = (outlier_count / df_with_z.height) * 100
    logger.info(f"Z-score outliers detected: {outlier_count} ({outlier_pct:.2f}%)")
    
    return df_with_z


def calculate_temporal_coverage(
    df: pl.DataFrame,
    group_column: str,
    time_column: str,
    expected_periods: int
) -> pl.DataFrame:
    """Calculate temporal coverage completeness for each group.
    
    Args:
        df: Input DataFrame
        group_column: Column to group by
        time_column: Time period column
        expected_periods: Expected number of periods
        
    Returns:
        DataFrame with coverage metrics
    """
    logger.info(f"Calculating temporal coverage for {group_column}")
    
    coverage = df.group_by(group_column).agg([
        pl.col(time_column).n_unique().alias("actual_periods"),
        pl.lit(expected_periods).alias("expected_periods")
    ]).with_columns([
        ((pl.col("actual_periods") / pl.col("expected_periods")) * 100).alias("completeness_pct"),
        (pl.col("expected_periods") - pl.col("actual_periods")).alias("missing_periods")
    ]).sort("completeness_pct", descending=False)
    
    # Log incomplete groups
    incomplete = coverage.filter(pl.col("completeness_pct") < 100)
    if incomplete.height > 0:
        logger.warning(f"{incomplete.height} groups have incomplete temporal coverage:")
        for row in incomplete.head(10).iter_rows(named=True):
            logger.warning(
                f"  {row[group_column]}: {row['completeness_pct']:.1f}% "
                f"({row['missing_periods']} missing periods)"
            )
    else:
        logger.info("All groups have 100% temporal coverage")
    
    return coverage


def analyze_distribution(
    df: pl.DataFrame,
    column: str,
    bins: int = 30
) -> Tuple[np.ndarray, np.ndarray]:
    """Analyze distribution of a column.
    
    Args:
        df: Input DataFrame
        column: Column to analyze
        bins: Number of histogram bins
        
    Returns:
        Tuple of (counts, bin_edges)
    """
    logger.info(f"Analyzing distribution of {column}")
    
    # Convert to numpy for histogram
    values = df[column].to_numpy()
    
    # Calculate histogram
    counts, bin_edges = np.histogram(values, bins=bins)
    
    # Log distribution characteristics
    logger.info(f"Distribution stats:")
    logger.info(f"  Range: [{values.min():.2f}, {values.max():.2f}]")
    logger.info(f"  Mean: {values.mean():.2f}")
    logger.info(f"  Median: {np.median(values):.2f}")
    logger.info(f"  Std: {values.std():.2f}")
    logger.info(f"  Skewness: {calculate_skewness(values):.2f}")
    
    return counts, bin_edges


def calculate_skewness(values: np.ndarray) -> float:
    """Calculate skewness of a distribution.
    
    Args:
        values: Array of values
        
    Returns:
        Skewness value
    """
    mean = np.mean(values)
    std = np.std(values)
    n = len(values)
    
    if std == 0:
        return 0.0
    
    skewness = (n / ((n - 1) * (n - 2))) * np.sum(((values - mean) / std) ** 3)
    return float(skewness)


def generate_profiling_report(
    df: pl.DataFrame,
    summary_stats: pl.DataFrame,
    outlier_analysis: dict
) -> dict:
    """Generate comprehensive profiling report.
    
    Args:
        df: Original DataFrame
        summary_stats: Summary statistics DataFrame
        outlier_analysis: Dictionary with outlier information
        
    Returns:
        Dictionary containing profiling report
    """
    logger.info("Generating profiling report...")
    
    report = {
        "dataset_info": {
            "total_records": df.height,
            "total_columns": len(df.columns),
            "unique_diseases": df["disease"].n_unique() if "disease" in df.columns else None,
            "date_range": {
                "start": df["epi_week"].min() if "epi_week" in df.columns else None,
                "end": df["epi_week"].max() if "epi_week" in df.columns else None
            }
        },
        "summary_statistics": {
            "total_diseases": summary_stats.height,
            "total_cases_all_diseases": summary_stats["mean"].sum() if "mean" in summary_stats.columns else None
        },
        "outlier_analysis": outlier_analysis,
        "recommendations": []
    }
    
    # Add recommendations based on findings
    if outlier_analysis.get("outlier_pct", 0) > 10:
        report["recommendations"].append(
            "High percentage of outliers detected. Review for data quality issues or genuine outbreaks."
        )
    
    if outlier_analysis.get("outlier_pct", 0) < 1:
        report["recommendations"].append(
            "Very few outliers detected. Data appears stable with minimal extreme events."
        )
    
    logger.info("Profiling report generated successfully")
    
    return report
