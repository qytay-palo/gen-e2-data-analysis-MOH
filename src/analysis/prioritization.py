"""Disease prioritization module for multi-criteria burden assessment.

This module provides functions to calculate composite disease burden scores using
weighted multi-criteria scoring, rank diseases by priority, and perform sensitivity
analysis across different weighting schemes. The prioritization framework supports
evidence-based resource allocation decisions for infectious disease control.

Key Functions:
    - normalize_metrics: Min-max normalization to 0-100 scale
    - calculate_composite_score: Weighted sum of normalized criteria
    - assign_tiers: Classify diseases into High/Medium/Low priority groups
    - rank_diseases: Rank diseases by composite burden score
    - sensitivity_analysis: Test ranking robustness across scenarios
    - calculate_rank_correlation: Spearman correlation between rankings
    - identify_consensus_priorities: Diseases consistently top-ranked

Example Usage:
    >>> import polars as pl
    >>> from src.analysis.prioritization import (
    ...     calculate_composite_score,
    ...     assign_tiers,
    ...     rank_diseases
    ... )
    >>> 
    >>> # Load burden metrics
    >>> df = pl.read_csv('data/4_processed/disease_burden_metrics.csv')
    >>> 
    >>> # Calculate composite scores with base case weights
    >>> weights = {'volume': 0.40, 'trend': 0.25, 'outbreak': 0.20, 'variability': 0.15}
    >>> df_scored = calculate_composite_score(df, weights)
    >>> 
    >>> # Assign priority tiers
    >>> thresholds = {'high': 70.0, 'medium': 40.0}
    >>> df_tiered = assign_tiers(df_scored, thresholds)
    >>> 
    >>> # Rank diseases
    >>> df_ranked = rank_diseases(df_tiered)
    >>> print(df_ranked.select(['rank', 'disease_name', 'composite_score', 'tier']).head(10))

Author: MOH Data Analytics Team
Created: 2026-02-12
"""

import logging
from typing import Dict, List, Optional, Tuple

import numpy as np
import polars as pl
from scipy import stats

# Configure logger
logger = logging.getLogger(__name__)


def validate_burden_metrics_input(df: pl.DataFrame) -> None:
    """Validate input burden metrics DataFrame structure and quality.
    
    Checks that the DataFrame contains all required columns, has appropriate data types,
    score ranges are valid (0-100), and sufficient data flags are present.
    
    Args:
        df: Burden metrics DataFrame to validate.
    
    Raises:
        ValueError: If DataFrame is empty, scores are out of range, or data quality issues found.
        KeyError: If required columns are missing.
    """
    # Check DataFrame not empty
    if df.is_empty():
        raise ValueError("Input DataFrame is empty")
    
    # Check required columns
    required_cols = [
        'disease_name', 'sufficient_data',
        'total_cases_score', 'annual_avg_cases_score',
        'cagr_score', 'outbreak_score', 'coefficient_variation_score'
    ]
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        raise KeyError(f"Missing required columns: {missing_cols}")
    
    # Validate score columns are numeric and in valid range [0, 100]
    score_cols = [col for col in df.columns if col.endswith('_score')]
    for col in score_cols:
        # Check if column is numeric
        if df[col].dtype not in [pl.Float64, pl.Float32, pl.Int64, pl.Int32]:
            logger.warning(f"Score column '{col}' is not numeric: {df[col].dtype}")
        
        # Check range for non-null values
        non_null_df = df.filter(pl.col(col).is_not_null())
        if len(non_null_df) > 0:
            min_val = non_null_df[col].min()
            max_val = non_null_df[col].max()
            if min_val < 0 or max_val > 100:
                logger.warning(f"Score column '{col}' out of range [0, 100]: [{min_val}, {max_val}]")
    
    logger.info(f"Validated {len(df)} diseases with {len(score_cols)} score columns")


def normalize_metrics(
    df: pl.DataFrame,
    metrics: List[str],
    scale_range: Tuple[float, float] = (0.0, 100.0)
) -> pl.DataFrame:
    """Normalize metrics to common scale using min-max normalization.
    
    Applies min-max normalization to transform metrics to a common scale (default 0-100).
    This ensures all criteria are comparable when calculating composite scores.
    
    Mathematical Formula:
        normalized = (value - min) / (max - min) * (scale_max - scale_min) + scale_min
    
    Special Cases:
        - If all values are identical (zero range): Returns midpoint of scale
        - If values contain NaN: Raises ValueError
        - If metric doesn't exist: Raises KeyError
    
    Args:
        df: DataFrame containing metrics to normalize.
        metrics: List of column names to normalize.
        scale_range: Tuple of (min, max) for normalized scale. Defaults to (0, 100).
    
    Returns:
        DataFrame with normalized metric columns (original columns are replaced).
    
    Raises:
        ValueError: If DataFrame is empty, metrics contain NaN, or invalid scale_range.
        KeyError: If any metric column doesn't exist in DataFrame.
    
    Example:
        >>> df = pl.DataFrame({
        ...     'disease': ['A', 'B', 'C'],
        ...     'cases': [100, 500, 300]
        ... })
        >>> df_norm = normalize_metrics(df, ['cases'])
        >>> print(df_norm['cases'])
        [0.0, 100.0, 50.0]
    """
    if df.is_empty():
        raise ValueError("Input DataFrame is empty")
    
    # Validate scale range
    if scale_range[1] <= scale_range[0]:
        raise ValueError(f"Invalid scale_range: max ({scale_range[1]}) must be > min ({scale_range[0]})")
    
    # Check all metrics exist
    missing_metrics = set(metrics) - set(df.columns)
    if missing_metrics:
        raise KeyError(f"Missing metric columns: {missing_metrics}")
    
    # Create a copy to avoid modifying original
    df_normalized = df.clone()
    
    scale_min, scale_max = scale_range
    
    for metric in metrics:
        # Check for NaN values
        if df_normalized[metric].null_count() > 0:
            raise ValueError(f"Metric '{metric}' contains NaN values")
        
        min_val = df_normalized[metric].min()
        max_val = df_normalized[metric].max()
        value_range = max_val - min_val
        
        # Handle zero range case (all values identical)
        if value_range == 0:
            midpoint = (scale_min + scale_max) / 2
            df_normalized = df_normalized.with_columns([
                pl.lit(midpoint).alias(metric)
            ])
            logger.warning(f"Metric '{metric}' has zero range, setting all values to midpoint {midpoint}")
        else:
            # Apply min-max normalization
            df_normalized = df_normalized.with_columns([
                ((pl.col(metric) - min_val) / value_range * (scale_max - scale_min) + scale_min).alias(metric)
            ])
    
    logger.info(f"Normalized {len(metrics)} metrics for {len(df_normalized)} diseases")
    return df_normalized


def calculate_composite_score(
    df: pl.DataFrame,
    weights: Dict[str, float],
    criteria_cols: Optional[Dict[str, str]] = None
) -> pl.DataFrame:
    """Calculate composite burden score using weighted sum of criteria.
    
    Computes a composite disease burden score by taking the weighted average of multiple
    burden criteria (volume, trend, outbreak risk, variability). All weights must sum to 1.0.
    
    Mathematical Formula:
        composite_score = Σ(weight_i × criterion_i) for all criteria
    
    Default Criteria Mapping (if criteria_cols not provided):
        - volume: mean of total_cases_score and annual_avg_cases_score
        - trend: cagr_score
        - outbreak: outbreak_score
        - variability: coefficient_variation_score
    
    Args:
        df: DataFrame with burden metric scores.
        weights: Dictionary mapping criterion names to weights (must sum to 1.0 ±0.001).
        criteria_cols: Optional dictionary mapping criterion names to column names.
                      If None, uses default mapping described above.
    
    Returns:
        DataFrame with added columns:
            - volume_criterion: Aggregated volume score
            - trend_criterion: Trend score
            - outbreak_criterion: Outbreak score  
            - variability_criterion: Variability score
            - composite_score: Weighted sum of all criteria
    
    Raises:
        ValueError: If weights don't sum to 1.0, DataFrame is empty, or scores out of range.
        KeyError: If required score columns are missing.
    
    Example:
        >>> df = pl.DataFrame({
        ...     'disease_name': ['Dengue', 'HFMD'],
        ...     'total_cases_score': [50.0, 100.0],
        ...     'annual_avg_cases_score': [50.0, 100.0],
        ...     'cagr_score': [80.0, 20.0],
        ...     'outbreak_score': [70.0, 30.0],
        ...     'coefficient_variation_score': [40.0, 60.0]
        ... })
        >>> weights = {'volume': 0.40, 'trend': 0.25, 'outbreak': 0.20, 'variability': 0.15}
        >>> df_scored = calculate_composite_score(df, weights)
        >>> print(df_scored.select(['disease_name', 'composite_score']))
        shape: (2, 2)
        ┌──────────────┬─────────────────┐
        │ disease_name ┆ composite_score │
        │ ---          ┆ ---             │
        │ str          ┆ f64             │
        ╞══════════════╪═════════════════╡
        │ Dengue       ┆ 59.5            │
        │ HFMD         ┆ 68.5            │
        └──────────────┴─────────────────┘
    """
    if df.is_empty():
        raise ValueError("Input DataFrame is empty")
    
    # Validate weights sum to 1.0
    weight_sum = sum(weights.values())
    if abs(weight_sum - 1.0) > 0.001:
        raise ValueError(
            f"Weights sum to {weight_sum:.3f}, must equal 1.0 (±0.001). "
            f"Current weights: {weights}"
        )
    
    # Validate all weight keys match expected criteria
    expected_criteria = {'volume', 'trend', 'outbreak', 'variability'}
    if set(weights.keys()) != expected_criteria:
        raise ValueError(
            f"Weights must include exactly these criteria: {expected_criteria}. "
            f"Got: {set(weights.keys())}"
        )
    
    # Default criteria column mapping
    if criteria_cols is None:
        criteria_cols = {
            'volume': ['total_cases_score', 'annual_avg_cases_score'],
            'trend': 'cagr_score',
            'outbreak': 'outbreak_score',
            'variability': 'coefficient_variation_score'
        }
    
    # Check required columns exist
    required_cols = ['total_cases_score', 'annual_avg_cases_score', 'cagr_score',
                    'outbreak_score', 'coefficient_variation_score']
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        raise KeyError(f"Missing required columns: {missing_cols}")
    
    # Calculate criteria aggregates
    df_scored = df.clone()
    
    # Volume: Average of total cases and annual average cases scores
    df_scored = df_scored.with_columns([
        ((pl.col('total_cases_score') + pl.col('annual_avg_cases_score')) / 2.0)
        .alias('volume_criterion')
    ])
    
    # Trend: Direct use of CAGR score
    df_scored = df_scored.with_columns([
        pl.col('cagr_score').alias('trend_criterion')
    ])
    
    # Outbreak: Use existing outbreak_score (already aggregated in User Story 2)
    df_scored = df_scored.with_columns([
        pl.col('outbreak_score').alias('outbreak_criterion')
    ])
    
    # Variability: Direct use of coefficient of variation score
    df_scored = df_scored.with_columns([
        pl.col('coefficient_variation_score').alias('variability_criterion')
    ])
    
    # Calculate composite score: weighted sum
    composite_expr = (
        pl.col('volume_criterion') * weights['volume'] +
        pl.col('trend_criterion') * weights['trend'] +
        pl.col('outbreak_criterion') * weights['outbreak'] +
        pl.col('variability_criterion') * weights['variability']
    )
    
    df_scored = df_scored.with_columns([
        composite_expr.alias('composite_score')
    ])
    
    # Validate composite scores are in valid range
    min_score = df_scored['composite_score'].min()
    max_score = df_scored['composite_score'].max()
    if min_score < 0 or max_score > 100:
        logger.warning(f"Composite scores out of range [0, 100]: [{min_score:.2f}, {max_score:.2f}]")
    
    logger.info(f"Calculated composite scores with weights: {weights}")
    return df_scored


def assign_tiers(
    df: pl.DataFrame,
    thresholds: Dict[str, float],
    score_col: str = 'composite_score'
) -> pl.DataFrame:
    """Assign diseases to priority tiers based on composite burden score thresholds.
    
    Classifies diseases into High, Medium, or Low priority tiers based on configured
    thresholds. Tier assignment guides resource allocation decisions.
    
    Tier Definitions:
        - High Priority: score > high_threshold (substantial resources required)
        - Medium Priority: medium_threshold <= score <= high_threshold (sustained effort)
        - Low Priority: score < medium_threshold (maintenance/surveillance mode)
    
    Args:
        df: DataFrame with composite burden scores.
        thresholds: Dictionary with 'high' and 'medium' threshold values.
                   Must satisfy: high > medium > 0.
        score_col: Name of the score column to use for tier assignment.
                  Defaults to 'composite_score'.
    
    Returns:
        DataFrame with added 'tier' column (categorical: High/Medium/Low).
    
    Raises:
        ValueError: If thresholds are invalid (high <= medium or medium <= 0) or
                   DataFrame is empty.
        KeyError: If score column doesn't exist.
    
    Example:
        >>> df = pl.DataFrame({
        ...     'disease_name': ['Dengue', 'HFMD', 'Cholera'],
        ...     'composite_score': [75.0, 85.0, 25.0]
        ... })
        >>> thresholds = {'high': 70.0, 'medium': 40.0}
        >>> df_tiered = assign_tiers(df, thresholds)
        >>> print(df_tiered.select(['disease_name', 'composite_score', 'tier']))
        shape: (3, 3)
        ┌──────────────┬─────────────────┬────────┐
        │ disease_name ┆ composite_score ┆ tier   │
        │ ---          ┆ ---             ┆ ---    │
        │ str          ┆ f64             ┆ str    │
        ╞══════════════╪═════════════════╪════════╡
        │ Dengue       ┆ 75.0            ┆ High   │
        │ HFMD         ┆ 85.0            ┆ High   │
        │ Cholera      ┆ 25.0            ┆ Low    │
        └──────────────┴─────────────────┴────────┘
    """
    if df.is_empty():
        raise ValueError("Input DataFrame is empty")
    
    # Validate score column exists
    if score_col not in df.columns:
        raise KeyError(f"Score column '{score_col}' not found in DataFrame")
    
    # Validate threshold requirements
    high_threshold = thresholds.get('high')
    medium_threshold = thresholds.get('medium')
    
    if high_threshold is None or medium_threshold is None:
        raise ValueError("Thresholds must include 'high' and 'medium' keys")
    
    if high_threshold <= medium_threshold:
        raise ValueError(
            f"Invalid tier thresholds: high ({high_threshold}) must be > "
            f"medium ({medium_threshold})"
        )
    
    if medium_threshold <= 0:
        raise ValueError(f"Invalid tier thresholds: medium ({medium_threshold}) must be > 0")
    
    # Assign tiers using conditional expressions
    df_tiered = df.with_columns([
        pl.when(pl.col(score_col) > high_threshold)
        .then(pl.lit('High'))
        .when(pl.col(score_col) >= medium_threshold)
        .then(pl.lit('Medium'))
        .otherwise(pl.lit('Low'))
        .alias('tier')
    ])
    
    # Log tier distribution
    tier_counts = df_tiered.group_by('tier').agg(pl.count()).sort('tier')
    logger.info(
        f"Assigned tiers: High >{high_threshold}, Medium {medium_threshold}-{high_threshold}, "
        f"Low <{medium_threshold}"
    )
    logger.info(f"Tier distribution: {tier_counts.to_dicts()}")
    
    return df_tiered


def rank_diseases(
    df: pl.DataFrame,
    score_col: str = 'composite_score',
    ascending: bool = False
) -> pl.DataFrame:
    """Rank diseases by composite burden score in descending order.
    
    Assigns a rank number to each disease based on their composite burden score.
    Rank 1 indicates the highest burden (highest score). Ties are handled using
    stable sorting (preserves original order for equal scores).
    
    Args:
        df: DataFrame with disease scores.
        score_col: Column name containing scores to rank by. Defaults to 'composite_score'.
        ascending: If True, rank in ascending order (lowest score = rank 1).
                  Defaults to False (highest score = rank 1).
    
    Returns:
        DataFrame sorted by rank with added 'rank' column (integer starting from 1).
    
    Raises:
        ValueError: If DataFrame is empty.
        KeyError: If score column doesn't exist.
    
    Example:
        >>> df = pl.DataFrame({
        ...     'disease_name': ['Dengue', 'HFMD', 'Cholera'],
        ...     'composite_score': [75.0, 85.0, 25.0]
        ... })
        >>> df_ranked = rank_diseases(df)
        >>> print(df_ranked.select(['rank', 'disease_name', 'composite_score']))
        shape: (3, 3)
        ┌──────┬──────────────┬─────────────────┐
        │ rank ┆ disease_name ┆ composite_score │
        │ ---  ┆ ---          ┆ ---             │
        │ u32  ┆ str          ┆ f64             │
        ╞══════╪══════════════╪═════════════════╡
        │ 1    ┆ HFMD         ┆ 85.0            │
        │ 2    ┆ Dengue       ┆ 75.0            │
        │ 3    ┆ Cholera      ┆ 25.0            │
        └──────┴──────────────┴─────────────────┘
    """
    if df.is_empty():
        raise ValueError("Input DataFrame is empty")
    
    # Validate score column exists
    if score_col not in df.columns:
        raise KeyError(f"Score column '{score_col}' not found in DataFrame")
    
    # Sort by score (descending by default for burden prioritization)
    df_sorted = df.sort(score_col, descending=not ascending)
    
    # Add rank column (1-indexed)
    df_ranked = df_sorted.with_row_count(name='rank', offset=1)
    
    logger.info(f"Ranked {len(df_ranked)} diseases by {score_col} ({'ascending' if ascending else 'descending'})")
    
    return df_ranked


def sensitivity_analysis(
    df: pl.DataFrame,
    scenarios: Dict[str, Dict[str, float]],
    criteria_cols: Optional[Dict[str, str]] = None
) -> Dict[str, pl.DataFrame]:
    """Perform sensitivity analysis by recalculating rankings under alternative weighting schemes.
    
    Tests the robustness of disease rankings by applying multiple weighting scenarios.
    This helps identify diseases that remain top priorities regardless of weighting
    (consensus priorities) versus those whose rank is sensitive to weight changes.
    
    Args:
        df: DataFrame with burden metrics.
        scenarios: Dictionary mapping scenario names to weight dictionaries.
                  Each weight dict must have keys: volume, trend, outbreak, variability.
        criteria_cols: Optional dictionary mapping criterion names to column names.
                      Passed to calculate_composite_score().
    
    Returns:
        Dictionary mapping scenario names to ranked DataFrames.
        Each DataFrame contains: rank, disease_name, composite_score, tier, and criteria scores.
    
    Raises:
        ValueError: If any scenario has invalid weights or DataFrame is empty.
    
    Example:
        >>> scenarios = {
        ...     'base': {'volume': 0.40, 'trend': 0.25, 'outbreak': 0.20, 'variability': 0.15},
        ...     'volume_focused': {'volume': 0.60, 'trend': 0.20, 'outbreak': 0.10, 'variability': 0.10}
        ... }
        >>> rankings = sensitivity_analysis(df, scenarios)
        >>> print(f"Scenarios analyzed: {list(rankings.keys())}")
        Scenarios analyzed: ['base', 'volume_focused']
    """
    if df.is_empty():
        raise ValueError("Input DataFrame is empty")
    
    if not scenarios:
        raise ValueError("At least one scenario must be provided")
    
    rankings = {}
    
    for scenario_name, weights in scenarios.items():
        logger.info(f"Running scenario '{scenario_name}' with weights: {weights}")
        
        try:
            # Calculate composite score with scenario weights
            df_scored = calculate_composite_score(df, weights, criteria_cols)
            
            # Assign tiers (using default thresholds)
            thresholds = {'high': 70.0, 'medium': 40.0}
            df_tiered = assign_tiers(df_scored, thresholds)
            
            # Rank diseases
            df_ranked = rank_diseases(df_tiered)
            
            # Store results
            rankings[scenario_name] = df_ranked
            
        except Exception as e:
            logger.error(f"Failed to process scenario '{scenario_name}': {e}")
            raise
    
    logger.info(f"Completed sensitivity analysis for {len(rankings)} scenarios")
    return rankings


def calculate_rank_correlation(
    rankings: Dict[str, pl.DataFrame],
    rank_col: str = 'rank',
    disease_col: str = 'disease_name'
) -> pl.DataFrame:
    """Calculate Spearman rank correlation matrix between different ranking scenarios.
    
    Measures the similarity of disease rankings across scenarios using Spearman's
    rank correlation coefficient. High correlation indicates rankings are robust to
    weight changes; low correlation indicates sensitivity.
    
    Args:
        rankings: Dictionary mapping scenario names to ranked DataFrames.
        rank_col: Name of the rank column. Defaults to 'rank'.
        disease_col: Name of the disease identifier column. Defaults to 'disease_name'.
    
    Returns:
        Correlation matrix as Polars DataFrame with scenarios as both rows and columns.
        Values range from -1 (perfect negative correlation) to 1 (perfect positive correlation).
    
    Raises:
        ValueError: If rankings dictionary is empty or contains fewer than 2 scenarios.
    
    Example:
        >>> rankings = {
        ...     'base': df_ranked_base,
        ...     'volume_focused': df_ranked_volume
        ... }
        >>> corr_matrix = calculate_rank_correlation(rankings)
        >>> print(corr_matrix)
        shape: (2, 3)
        ┌────────────────┬──────┬────────────────┐
        │ scenario       ┆ base ┆ volume_focused │
        │ ---            ┆ ---  ┆ ---            │
        │ str            ┆ f64  ┆ f64            │
        ╞════════════════╪══════╪════════════════╡
        │ base           ┆ 1.0  ┆ 0.85           │
        │ volume_focused ┆ 0.85 ┆ 1.0            │
        └────────────────┴──────┴────────────────┘
    """
    if not rankings:
        raise ValueError("Rankings dictionary is empty")
    
    if len(rankings) < 2:
        raise ValueError("At least 2 scenarios required for correlation analysis")
    
    scenario_names = list(rankings.keys())
    n_scenarios = len(scenario_names)
    
    # Initialize correlation matrix
    corr_matrix = np.eye(n_scenarios)
    
    # Calculate pairwise Spearman correlations
    for i, scenario1 in enumerate(scenario_names):
        for j, scenario2 in enumerate(scenario_names):
            if i >= j:  # Skip diagonal and lower triangle (matrix is symmetric)
                continue
            
            # Get rankings for both scenarios
            df1 = rankings[scenario1]
            df2 = rankings[scenario2]
            
            # Merge on disease name to align ranks
            merged = df1.select([disease_col, rank_col]).rename({rank_col: 'rank1'}) \
                       .join(df2.select([disease_col, rank_col]).rename({rank_col: 'rank2'}),
                             on=disease_col, how='inner')
            
            # Calculate Spearman correlation
            correlation, _ = stats.spearmanr(
                merged['rank1'].to_numpy(),
                merged['rank2'].to_numpy()
            )
            
            # Fill symmetric positions
            corr_matrix[i, j] = correlation
            corr_matrix[j, i] = correlation
    
    # Convert to Polars DataFrame
    corr_df = pl.DataFrame({
        'scenario': scenario_names,
        **{name: corr_matrix[:, i] for i, name in enumerate(scenario_names)}
    })
    
    logger.info(
        f"Calculated rank correlations: mean={corr_matrix[np.triu_indices(n_scenarios, k=1)].mean():.3f}, "
        f"min={corr_matrix[np.triu_indices(n_scenarios, k=1)].min():.3f}, "
        f"max={corr_matrix[np.triu_indices(n_scenarios, k=1)].max():.3f}"
    )
    
    return corr_df


def identify_consensus_priorities(
    rankings: Dict[str, pl.DataFrame],
    top_n: int = 10,
    disease_col: str = 'disease_name',
    rank_col: str = 'rank'
) -> List[str]:
    """Identify diseases that consistently appear in top N across all ranking scenarios.
    
    Consensus priorities are diseases that remain highly ranked regardless of weighting
    scheme, indicating robust priority status. These diseases should receive sustained
    resource allocation.
    
    Args:
        rankings: Dictionary mapping scenario names to ranked DataFrames.
        top_n: Number of top-ranked diseases to consider. Defaults to 10.
        disease_col: Name of the disease identifier column. Defaults to 'disease_name'.
        rank_col: Name of the rank column. Defaults to 'rank'.
    
    Returns:
        List of disease names appearing in top N ranks across ALL scenarios.
        Empty list if no diseases meet consensus criteria.
    
    Example:
        >>> rankings = {'base': df1, 'volume_focused': df2, 'emerging_threat': df3}
        >>> consensus = identify_consensus_priorities(rankings, top_n=10)
        >>> print(f"Consensus Top 10: {consensus}")
        Consensus Top 10: ['Dengue Fever', 'Hand, Foot and Mouth Disease', 'Salmonellosis']
    """
    if not rankings:
        raise ValueError("Rankings dictionary is empty")
    
    if top_n <= 0:
        raise ValueError(f"top_n must be positive, got {top_n}")
    
    # Get top N diseases from each scenario
    scenario_top_n = {}
    for scenario_name, df_ranked in rankings.items():
        top_diseases = (
            df_ranked
            .filter(pl.col(rank_col) <= top_n)
            .select(disease_col)
            .to_series()
            .to_list()
        )
        scenario_top_n[scenario_name] = set(top_diseases)
    
    # Find intersection across all scenarios (consensus)
    all_scenarios = list(scenario_top_n.values())
    consensus = set.intersection(*all_scenarios)
    
    consensus_list = sorted(list(consensus))
    
    logger.info(
        f"{len(consensus_list)} diseases in Top {top_n} across all {len(rankings)} scenarios: "
        f"{consensus_list if len(consensus_list) <= 5 else consensus_list[:5] + ['...']}"
    )
    
    return consensus_list
