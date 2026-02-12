"""
Outbreak detection module for disease burden metrics.

This module provides functions for identifying and quantifying outbreak episodes
based on statistical thresholds and temporal patterns.
"""

import polars as pl
import numpy as np
import logging
from typing import List, Dict, Tuple, Optional

from src.config import OUTBREAK_THRESHOLD_MULTIPLIER

logger = logging.getLogger(__name__)


def define_outbreak_threshold(
    series: pl.Series, 
    multiplier: float = OUTBREAK_THRESHOLD_MULTIPLIER
) -> float:
    """
    Define outbreak threshold as mean + multiplier × SD.
    
    Parameters
    ----------
    series : pl.Series
        Time series of case counts
    multiplier : float, default=2.0
        Standard deviation multiplier for threshold
        
    Returns
    -------
    float
        Outbreak threshold value
        
    Examples
    --------
    >>> series = pl.Series([10, 12, 11, 13, 10])
    >>> threshold = define_outbreak_threshold(series)
    >>> threshold > 11  # Should be above mean
    True
    """
    mean = series.mean()
    std = series.std()
    
    if std == 0 or std is None:
        # No variation - use arbitrary threshold above mean
        threshold = mean * 1.5 if mean > 0 else 1.0
        logger.warning(f"Zero variance detected, using threshold: {threshold}")
        return threshold
    
    threshold = mean + multiplier * std
    return float(threshold)


def identify_outbreak_episodes(
    df: pl.DataFrame, 
    disease: str, 
    threshold: float,
    min_duration: int = 2
) -> List[Dict]:
    """
    Identify outbreak episodes as consecutive weeks above threshold.
    
    Parameters
    ----------
    df : pl.DataFrame
        Disease data with columns: disease_name, case_count, epidemiological_week
    disease : str
        Disease name to analyze
    threshold : float
        Outbreak threshold value
    min_duration : int, default=2
        Minimum consecutive weeks to qualify as outbreak
        
    Returns
    -------
    List[Dict]
        List of outbreak episodes with keys:
        - start_week: First week of outbreak
        - end_week: Last week of outbreak
        - duration: Number of weeks
        - peak_cases: Maximum cases during outbreak
        - mean_cases: Average cases during outbreak
        
    Examples
    --------
    >>> df = pl.DataFrame({
    ...     "disease_name": ["Dengue"]*10,
    ...     "case_count": [5, 5, 50, 60, 55, 5, 5, 45, 50, 5],
    ...     "epidemiological_week": [f"2020-W{i:02d}" for i in range(1, 11)]
    ... })
    >>> episodes = identify_outbreak_episodes(df, "Dengue", threshold=20)
    >>> len(episodes)
    2
    """
    disease_data = df.filter(pl.col("disease_name") == disease).sort("epidemiological_week")
    
    # Flag weeks above threshold
    above_threshold = (disease_data["case_count"] > threshold).to_numpy()
    weeks = disease_data["epidemiological_week"].to_list()
    case_counts = disease_data["case_count"].to_numpy()
    
    episodes = []
    in_outbreak = False
    outbreak_start = None
    outbreak_weeks = []
    outbreak_cases = []
    
    for i, (is_above, week, cases) in enumerate(zip(above_threshold, weeks, case_counts)):
        if is_above:
            if not in_outbreak:
                # Start new outbreak
                in_outbreak = True
                outbreak_start = week
                outbreak_weeks = [week]
                outbreak_cases = [cases]
            else:
                # Continue outbreak
                outbreak_weeks.append(week)
                outbreak_cases.append(cases)
        else:
            if in_outbreak:
                # End outbreak
                if len(outbreak_weeks) >= min_duration:
                    episodes.append({
                        "start_week": outbreak_start,
                        "end_week": outbreak_weeks[-1],
                        "duration": len(outbreak_weeks),
                        "peak_cases": int(max(outbreak_cases)),
                        "mean_cases": float(np.mean(outbreak_cases))
                    })
                in_outbreak = False
    
    # Handle outbreak that extends to end of data
    if in_outbreak and len(outbreak_weeks) >= min_duration:
        episodes.append({
            "start_week": outbreak_start,
            "end_week": outbreak_weeks[-1],
            "duration": len(outbreak_weeks),
            "peak_cases": int(max(outbreak_cases)),
            "mean_cases": float(np.mean(outbreak_cases))
        })
    
    return episodes


def calculate_outbreak_frequency(episodes: List[Dict]) -> int:
    """
    Count number of distinct outbreak episodes.
    
    Parameters
    ----------
    episodes : List[Dict]
        List of outbreak episodes
        
    Returns
    -------
    int
        Number of outbreaks
        
    Examples
    --------
    >>> episodes = [{"duration": 3}, {"duration": 5}]
    >>> calculate_outbreak_frequency(episodes)
    2
    """
    return len(episodes)


def calculate_outbreak_duration(episodes: List[Dict]) -> float:
    """
    Calculate average outbreak duration in weeks.
    
    Parameters
    ----------
    episodes : List[Dict]
        List of outbreak episodes with 'duration' key
        
    Returns
    -------
    float
        Mean outbreak duration in weeks, or 0.0 if no outbreaks
        
    Examples
    --------
    >>> episodes = [{"duration": 3}, {"duration": 5}, {"duration": 7}]
    >>> calculate_outbreak_duration(episodes)
    5.0
    """
    if not episodes:
        return 0.0
    
    durations = [ep["duration"] for ep in episodes]
    return float(np.mean(durations))


def calculate_outbreak_intensity(
    df: pl.DataFrame, 
    episodes: List[Dict], 
    disease: str
) -> Optional[float]:
    """
    Calculate outbreak intensity as peak-to-baseline ratio.
    
    Parameters
    ----------
    df : pl.DataFrame
        Disease data with columns: disease_name, case_count
    episodes : List[Dict]
        List of outbreak episodes
    disease : str
        Disease name
        
    Returns
    -------
    float or None
        Mean peak-to-baseline ratio, or None if zero baseline
        
    Examples
    --------
    >>> df = pl.DataFrame({
    ...     "disease_name": ["Dengue"]*10,
    ...     "case_count": [10, 10, 50, 60, 55, 10, 10, 45, 50, 10]
    ... })
    >>> episodes = [{"peak_cases": 60}, {"peak_cases": 50}]
    >>> intensity = calculate_outbreak_intensity(df, episodes, "Dengue")
    >>> intensity > 1.0  # Peak is higher than baseline
    True
    """
    if not episodes:
        return None
    
    disease_data = df.filter(pl.col("disease_name") == disease)
    baseline = disease_data["case_count"].median()
    
    if baseline == 0 or baseline is None:
        logger.warning(f"{disease}: Zero baseline, outbreak intensity = NA")
        return None
    
    intensities = [ep["peak_cases"] / baseline for ep in episodes]
    return float(np.mean(intensities))


def calculate_all_outbreak_metrics(
    df: pl.DataFrame,
    diseases: List[str],
    threshold_multiplier: float = OUTBREAK_THRESHOLD_MULTIPLIER
) -> pl.DataFrame:
    """
    Calculate outbreak metrics for all diseases.
    
    Parameters
    ----------
    df : pl.DataFrame
        Complete disease surveillance data
    diseases : List[str]
        List of disease names to analyze
    threshold_multiplier : float, default=2.0
        Standard deviation multiplier for outbreak threshold
        
    Returns
    -------
    pl.DataFrame
        Outbreak metrics with columns:
        - disease_name
        - outbreak_threshold
        - outbreak_frequency
        - avg_outbreak_duration
        - outbreak_intensity
    """
    results = []
    
    for disease in diseases:
        try:
            disease_data = df.filter(pl.col("disease_name") == disease)
            case_series = disease_data["case_count"]
            
            # Define threshold
            threshold = define_outbreak_threshold(case_series, threshold_multiplier)
            
            # Identify episodes
            episodes = identify_outbreak_episodes(df, disease, threshold)
            
            # Calculate metrics
            frequency = calculate_outbreak_frequency(episodes)
            duration = calculate_outbreak_duration(episodes)
            intensity = calculate_outbreak_intensity(df, episodes, disease)
            
            results.append({
                "disease_name": disease,
                "outbreak_threshold": threshold,
                "outbreak_frequency": frequency,
                "avg_outbreak_duration": duration,
                "outbreak_intensity": intensity
            })
            
            logger.info(f"Outbreak metrics calculated for {disease}: {frequency} outbreaks, avg duration={duration:.1f} weeks")
            
        except Exception as e:
            logger.error(f"Failed to calculate outbreak metrics for {disease}: {e}")
            results.append({
                "disease_name": disease,
                "outbreak_threshold": None,
                "outbreak_frequency": 0,
                "avg_outbreak_duration": 0.0,
                "outbreak_intensity": None
            })
    
    return pl.DataFrame(results)
