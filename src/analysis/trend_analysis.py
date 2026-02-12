"""
Trend analysis module for disease burden metrics.

This module provides functions for calculating linear trends, compound annual growth rates (CAGR),
and classifying trend directions for infectious disease surveillance data.
"""

import polars as pl
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional, Literal
from scipy.stats import linregress, kendalltau

from src.config import TREND_SIGNIFICANCE_LEVEL

logger = logging.getLogger(__name__)

TrendDirection = Literal["Increasing", "Stable", "Decreasing"]


def calculate_linear_trend(
    df: pl.DataFrame, 
    disease: str
) -> Dict[str, float]:
    """
    Calculate linear trend using least squares regression.
    
    Parameters
    ----------
    df : pl.DataFrame
        Disease data with columns: disease_name, case_count, epidemiological_week
    disease : str
        Disease name to analyze
        
    Returns
    -------
    Dict[str, float]
        Dictionary with keys: slope, intercept, r_value, p_value, stderr
        
    Raises
    ------
    ValueError
        If disease not found or insufficient data (<2 points)
    RuntimeError
        If regression fails to converge
        
    Examples
    --------
    >>> df = pl.DataFrame({"disease_name": ["Dengue"]*10, "case_count": range(10)})
    >>> result = calculate_linear_trend(df, "Dengue")
    >>> result["slope"]
    1.0
    """
    try:
        disease_data = df.filter(pl.col("disease_name") == disease)
        
        if disease_data.height < 2:
            raise ValueError(f"Insufficient data for {disease}: {disease_data.height} points")
        
        # Create sequential week numbers (1-470)
        week_numbers = np.arange(1, disease_data.height + 1)
        case_counts = disease_data["case_count"].to_numpy()
        
        # Linear regression
        slope, intercept, r_value, p_value, stderr = linregress(week_numbers, case_counts)
        
        logger.debug(f"{disease}: slope={slope:.4f}, p={p_value:.4f}")
        
        return {
            "slope": float(slope),
            "intercept": float(intercept),
            "r_value": float(r_value),
            "p_value": float(p_value),
            "stderr": float(stderr)
        }
        
    except ValueError as e:
        logger.warning(f"Validation error for {disease}: {e}")
        raise
    except Exception as e:
        logger.error(f"Regression failed for {disease}: {e}")
        raise RuntimeError(f"Trend calculation failed for {disease}") from e


def calculate_cagr(
    df: pl.DataFrame, 
    disease: str, 
    start_year: int = 2012, 
    end_year: int = 2020
) -> Optional[float]:
    """
    Calculate Compound Annual Growth Rate.
    
    Parameters
    ----------
    df : pl.DataFrame
        Disease data with columns: disease_name, case_count, year
    disease : str
        Disease name
    start_year : int, default=2012
        First year for CAGR calculation
    end_year : int, default=2020
        Last year for CAGR calculation
        
    Returns
    -------
    float or None
        CAGR percentage, or None if zero baseline
        
    Examples
    --------
    >>> df = pl.DataFrame({
    ...     "disease_name": ["Dengue"]*18,
    ...     "case_count": [100]*9 + [200]*9,
    ...     "year": [2012]*9 + [2020]*9
    ... })
    >>> cagr = calculate_cagr(df, "Dengue", 2012, 2020)
    >>> round(cagr, 2)
    9.05
    """
    try:
        disease_data = df.filter(pl.col("disease_name") == disease)
        
        first_year_avg = disease_data.filter(
            pl.col("year") == start_year
        )["case_count"].mean()
        
        last_year_avg = disease_data.filter(
            pl.col("year") == end_year
        )["case_count"].mean()
        
        # Handle zero baseline
        if first_year_avg == 0 or first_year_avg is None:
            logger.warning(f"{disease}: Zero baseline, CAGR = NA")
            return None
        
        # CAGR formula
        years = end_year - start_year
        cagr = ((last_year_avg / first_year_avg) ** (1 / years) - 1) * 100
        
        return float(cagr)
        
    except Exception as e:
        logger.error(f"CAGR calculation failed for {disease}: {e}")
        return None


def perform_mann_kendall_test(
    series: np.ndarray
) -> Tuple[float, float]:
    """
    Perform Mann-Kendall trend test.
    
    Parameters
    ----------
    series : np.ndarray
        Time series data
        
    Returns
    -------
    Tuple[float, float]
        Kendall's tau statistic and p-value
        
    Examples
    --------
    >>> series = np.array([1, 2, 3, 4, 5])
    >>> tau, pvalue = perform_mann_kendall_test(series)
    >>> tau > 0  # Positive trend
    True
    """
    try:
        # Create sequential indices
        indices = np.arange(len(series))
        
        # Kendall's tau correlation
        tau, p_value = kendalltau(indices, series)
        
        return float(tau), float(p_value)
        
    except Exception as e:
        logger.error(f"Mann-Kendall test failed: {e}")
        return 0.0, 1.0  # Return no trend on failure


def classify_trend_direction(
    slope: float, 
    pvalue: float, 
    alpha: float = TREND_SIGNIFICANCE_LEVEL
) -> TrendDirection:
    """
    Classify trend as Increasing/Stable/Decreasing.
    
    Parameters
    ----------
    slope : float
        Linear trend coefficient
    pvalue : float
        Statistical significance (0-1)
    alpha : float, default=0.05
        Significance threshold
        
    Returns
    -------
    TrendDirection
        One of "Increasing", "Stable", "Decreasing"
        
    Examples
    --------
    >>> classify_trend_direction(5.2, 0.001)
    'Increasing'
    >>> classify_trend_direction(-2.1, 0.003)
    'Decreasing'
    >>> classify_trend_direction(1.5, 0.15)
    'Stable'
    """
    if pvalue < alpha:
        return "Increasing" if slope > 0 else "Decreasing"
    return "Stable"


def calculate_all_trend_metrics(
    df: pl.DataFrame,
    diseases: List[str]
) -> pl.DataFrame:
    """
    Calculate trend metrics for all diseases.
    
    Parameters
    ----------
    df : pl.DataFrame
        Complete disease surveillance data
    diseases : List[str]
        List of disease names to analyze
        
    Returns
    -------
    pl.DataFrame
        Trend metrics with columns:
        - disease_name
        - trend_slope
        - trend_pvalue
        - mann_kendall_tau
        - mann_kendall_pvalue
        - cagr
        - trend_direction
    """
    results = []
    
    for disease in diseases:
        try:
            # Linear trend
            trend = calculate_linear_trend(df, disease)
            
            # CAGR
            cagr = calculate_cagr(df, disease)
            
            # Mann-Kendall test
            disease_data = df.filter(pl.col("disease_name") == disease)
            case_counts = disease_data["case_count"].to_numpy()
            mk_tau, mk_pvalue = perform_mann_kendall_test(case_counts)
            
            # Classify trend direction
            direction = classify_trend_direction(trend["slope"], trend["p_value"])
            
            results.append({
                "disease_name": disease,
                "trend_slope": trend["slope"],
                "trend_pvalue": trend["p_value"],
                "trend_r_value": trend["r_value"],
                "mann_kendall_tau": mk_tau,
                "mann_kendall_pvalue": mk_pvalue,
                "cagr": cagr,
                "trend_direction": direction
            })
            
            logger.info(f"Trend metrics calculated for {disease}: {direction}, CAGR={cagr:.2f}%" if cagr else f"Trend metrics calculated for {disease}: {direction}, CAGR=NA")
            
        except Exception as e:
            logger.error(f"Failed to calculate trends for {disease}: {e}")
            results.append({
                "disease_name": disease,
                "trend_slope": None,
                "trend_pvalue": None,
                "trend_r_value": None,
                "mann_kendall_tau": None,
                "mann_kendall_pvalue": None,
                "cagr": None,
                "trend_direction": None
            })
    
    return pl.DataFrame(results)
