"""
Burden metrics calculation module for disease prioritization.

This module provides functions for calculating volume metrics, variability metrics,
normalization, and composite burden scores.
"""

import polars as pl
import numpy as np
import logging
from typing import List, Dict, Optional
from sklearn.preprocessing import MinMaxScaler

from src.config import (
    SINGAPORE_POPULATION,
    MIN_NON_ZERO_WEEKS,
    TREND_SIGNIFICANCE_LEVEL,
    VOLUME_WEIGHT,
    TREND_WEIGHT,
    OUTBREAK_WEIGHT,
    VARIABILITY_WEIGHT
)

logger = logging.getLogger(__name__)


def calculate_volume_metrics(df: pl.DataFrame) -> pl.DataFrame:
    """
    Calculate volume metrics for each disease.
    
    Parameters
    ----------
    df : pl.DataFrame
        Cleaned disease surveillance data with columns:
        - disease_name (str): Standardized disease name
        - case_count (int): Weekly case count
        - year (int): Year of observation
        
    Returns
    -------
    pl.DataFrame
        Volume metrics per disease with columns:
        - disease_name (str)
        - total_cases (int)
        - annual_avg_cases (float)
        - peak_weekly_cases (int)
        - incidence_rate_per_100k (float)
        
    Raises
    ------
    ValueError
        If required columns are missing from input DataFrame
    RuntimeError
        If calculation fails unexpectedly
        
    Examples
    --------
    >>> df = pl.DataFrame({
    ...     "disease_name": ["Dengue"]*3,
    ...     "case_count": [100, 200, 150],
    ...     "year": [2012, 2013, 2014]
    ... })
    >>> volume = calculate_volume_metrics(df)
    >>> volume["total_cases"][0]
    450
    """
    try:
        # Input validation
        required_cols = ["disease_name", "case_count"]
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Missing required columns: {required_cols}")
        
        logger.info("Calculating volume metrics for %d diseases", df["disease_name"].n_unique())
        
        # Group by disease_name and calculate metrics
        volume_metrics = df.group_by("disease_name").agg([
            pl.col("case_count").sum().alias("total_cases"),
            (pl.col("case_count").sum() / 9).alias("annual_avg_cases"),
            pl.col("case_count").max().alias("peak_weekly_cases"),
            ((pl.col("case_count").sum() / SINGAPORE_POPULATION) * 100_000).alias("incidence_rate_per_100k")
        ])
        
        logger.info("Volume metrics calculated for %d diseases", volume_metrics.height)
        return volume_metrics
        
    except ValueError as e:
        logger.error(f"Validation error in calculate_volume_metrics: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in calculate_volume_metrics: {e}")
        raise RuntimeError(f"Failed to calculate volume metrics: {e}") from e


def calculate_variability_metrics(df: pl.DataFrame) -> pl.DataFrame:
    """
    Calculate variability metrics for each disease.
    
    Parameters
    ----------
    df : pl.DataFrame
        Disease data with columns: disease_name, case_count
        
    Returns
    -------
    pl.DataFrame
        Variability metrics with columns:
        - disease_name
        - coefficient_variation
        - iqr
        - std_dev
        - mean_cases
        
    Examples
    --------
    >>> df = pl.DataFrame({
    ...     "disease_name": ["Dengue"]*5,
    ...     "case_count": [10, 12, 15, 11, 13]
    ... })
    >>> var_metrics = calculate_variability_metrics(df)
    >>> var_metrics["coefficient_variation"][0] > 0
    True
    """
    try:
        logger.info("Calculating variability metrics")
        
        variability_metrics = df.group_by("disease_name").agg([
            pl.col("case_count").mean().alias("mean_cases"),
            pl.col("case_count").std().alias("std_dev"),
            ((pl.col("case_count").std() / pl.col("case_count").mean()) * 100).alias("coefficient_variation"),
            (pl.col("case_count").quantile(0.75) - pl.col("case_count").quantile(0.25)).alias("iqr")
        ])
        
        logger.info("Variability metrics calculated for %d diseases", variability_metrics.height)
        return variability_metrics
        
    except Exception as e:
        logger.error(f"Failed to calculate variability metrics: {e}")
        raise RuntimeError(f"Variability metrics calculation failed: {e}") from e


def normalize_metrics(
    df: pl.DataFrame, 
    metric_columns: List[str]
) -> pl.DataFrame:
    """
    Normalize metrics to 0-100 scale using min-max scaling.
    
    Parameters
    ----------
    df : pl.DataFrame
        DataFrame with metrics to normalize
    metric_columns : List[str]
        Column names to normalize
        
    Returns
    -------
    pl.DataFrame
        DataFrame with additional normalized columns (suffix: _score)
        
    Examples
    --------
    >>> df = pl.DataFrame({
    ...     "disease_name": ["A", "B", "C"],
    ...     "total_cases": [100, 500, 1000]
    ... })
    >>> normalized = normalize_metrics(df, ["total_cases"])
    >>> normalized["total_cases_score"][0]
    0.0
    >>> normalized["total_cases_score"][2]
    100.0
    """
    try:
        logger.info("Normalizing %d metrics", len(metric_columns))
        
        df_pandas = df.to_pandas()
        
        for metric in metric_columns:
            if metric not in df.columns:
                logger.warning(f"Metric {metric} not found, skipping")
                continue
            
            values = df_pandas[metric].values.reshape(-1, 1)
            
            # Handle NA values
            mask = ~np.isnan(values.flatten())
            if not mask.any():
                logger.warning(f"All values are NA for {metric}, setting scores to 0")
                df_pandas[f"{metric}_score"] = 0.0
                continue
            
            # Min-max scaling
            scaler = MinMaxScaler(feature_range=(0, 100))
            normalized_values = np.zeros_like(values.flatten(), dtype=float)  # Force float type
            normalized_values[mask] = scaler.fit_transform(values[mask].reshape(-1, 1)).flatten()
            normalized_values[~mask] = np.nan
            
            df_pandas[f"{metric}_score"] = normalized_values
            
            logger.debug(f"Normalized {metric}: min={np.nanmin(normalized_values):.2f}, max={np.nanmax(normalized_values):.2f}")
        
        return pl.from_pandas(df_pandas)
        
    except Exception as e:
        logger.error(f"Normalization failed: {e}")
        raise RuntimeError(f"Failed to normalize metrics: {e}") from e


def calculate_composite_burden_score(df: pl.DataFrame) -> pl.DataFrame:
    """
    Calculate composite burden score as weighted sum of normalized metrics.
    
    Parameters
    ----------
    df : pl.DataFrame
        DataFrame with normalized metric scores
        
    Returns
    -------
    pl.DataFrame
        DataFrame with composite_burden_score column
        
    Examples
    --------
    >>> df = pl.DataFrame({
    ...     "disease_name": ["Dengue"],
    ...     "volume_score": [80.0],
    ...     "trend_score": [70.0],
    ...     "outbreak_score": [90.0],
    ...     "variability_score": [60.0]
    ... })
    >>> result = calculate_composite_burden_score(df)
    >>> result["composite_burden_score"][0]
    77.0
    """
    try:
        logger.info("Calculating composite burden scores")
        
        # Calculate weighted sum
        df = df.with_columns([
            (
                VOLUME_WEIGHT * pl.col("volume_score") +
                TREND_WEIGHT * pl.col("trend_score") +
                OUTBREAK_WEIGHT * pl.col("outbreak_score") +
                VARIABILITY_WEIGHT * pl.col("variability_score")
            ).alias("composite_burden_score")
        ])
        
        logger.info("Composite scores calculated for %d diseases", df.height)
        return df
        
    except Exception as e:
        logger.error(f"Composite score calculation failed: {e}")
        raise RuntimeError(f"Failed to calculate composite burden score: {e}") from e


def flag_data_quality(
    df: pl.DataFrame,
    cleaned_df: pl.DataFrame
) -> pl.DataFrame:
    """
    Add data quality flags to burden metrics.
    
    Parameters
    ----------
    df : pl.DataFrame
        Burden metrics DataFrame
    cleaned_df : pl.DataFrame
        Original cleaned disease data for quality checks
        
    Returns
    -------
    pl.DataFrame
        DataFrame with quality flags:
        - sufficient_data: >= 52 non-zero weeks
        - trend_reliable: trend p-value < 0.05
        - outbreak_detectable: CV > 20%
        
    Examples
    --------
    >>> metrics_df = pl.DataFrame({
    ...     "disease_name": ["Dengue"],
    ...     "trend_pvalue": [0.001],
    ...     "coefficient_variation": [150.0]
    ... })
    >>> cleaned_df = pl.DataFrame({
    ...     "disease_name": ["Dengue"]*100,
    ...     "case_count": range(100)
    ... })
    >>> flagged = flag_data_quality(metrics_df, cleaned_df)
    >>> flagged["sufficient_data"][0]
    True
    """
    try:
        logger.info("Flagging data quality issues")
        
        # Calculate non-zero weeks per disease
        non_zero_weeks = cleaned_df.filter(
            pl.col("case_count") > 0
        ).group_by("disease_name").agg([
            pl.col("case_count").count().alias("non_zero_weeks")
        ])
        
        # Join with main DataFrame
        df = df.join(non_zero_weeks, on="disease_name", how="left")
        
        # Add flags
        df = df.with_columns([
            (pl.col("non_zero_weeks") >= MIN_NON_ZERO_WEEKS).alias("sufficient_data"),
            (pl.col("trend_pvalue") < TREND_SIGNIFICANCE_LEVEL).alias("trend_reliable"),
            (pl.col("coefficient_variation") > 20).alias("outbreak_detectable")
        ])
        
        # Log summary
        insufficient = df.filter(~pl.col("sufficient_data")).height
        unreliable_trend = df.filter(~pl.col("trend_reliable")).height
        no_outbreaks = df.filter(~pl.col("outbreak_detectable")).height
        
        logger.info(f"Data quality flags: {insufficient} insufficient data, {unreliable_trend} unreliable trends, {no_outbreaks} non-detectable outbreaks")
        
        return df
        
    except Exception as e:
        logger.error(f"Data quality flagging failed: {e}")
        raise RuntimeError(f"Failed to flag data quality: {e}") from e
