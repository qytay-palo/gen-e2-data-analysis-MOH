"""
Burden Metrics Calculation Pipeline

This script executes the complete burden metrics calculation for User Story 2.
It loads cleaned disease data, calculates all metrics, and saves results.
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

import polars as pl
import numpy as np

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import (
    INTERIM_DATA_DIR,
    PROCESSED_DATA_DIR,
    RESULTS_TABLES_DIR,
    RESULTS_FIGURES_DIR,
    BURDEN_METRICS_PATH
)
from src.data_processing.burden_metrics import (
    calculate_volume_metrics,
    calculate_variability_metrics,
    normalize_metrics,
    calculate_composite_burden_score,
    flag_data_quality
)
from src.analysis.trend_analysis import calculate_all_trend_metrics
from src.analysis.outbreak_detection import calculate_all_outbreak_metrics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/burden_metrics_calculation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Execute burden metrics calculation pipeline."""
    
    logger.info("=" * 80)
    logger.info("BURDEN METRICS CALCULATION PIPELINE")
    logger.info("=" * 80)
    
    # 1. Load cleaned data
    logger.info("Step 1: Loading cleaned disease data")
    data_path = Path(INTERIM_DATA_DIR) / "cleaned_disease_data.parquet"
    df = pl.read_parquet(data_path)
    logger.info(f"Loaded {df.height:,} rows, {df['disease_name'].n_unique()} diseases")
    
    # Get list of diseases
    diseases = df['disease_name'].unique().to_list()
    logger.info(f"Diseases to analyze: {len(diseases)}")
    
    # 2. Calculate volume metrics
    logger.info("Step 2: Calculating volume metrics")
    volume_metrics = calculate_volume_metrics(df)
    logger.info(f"Volume metrics calculated for {volume_metrics.height} diseases")
    
    # 3. Calculate trend metrics
    logger.info("Step 3: Calculating trend metrics")
    trend_metrics = calculate_all_trend_metrics(df, diseases)
    logger.info(f"Trend metrics calculated for {trend_metrics.height} diseases")
    
    # 4. Calculate outbreak metrics
    logger.info("Step 4: Calculating outbreak metrics")
    outbreak_metrics = calculate_all_outbreak_metrics(df, diseases)
    logger.info(f"Outbreak metrics calculated for {outbreak_metrics.height} diseases")
    
    # 5. Calculate variability metrics
    logger.info("Step 5: Calculating variability metrics")
    variability_metrics = calculate_variability_metrics(df)
    logger.info(f"Variability metrics calculated for {variability_metrics.height} diseases")
    
    # 6. Merge all metrics
    logger.info("Step 6: Merging all metrics")
    burden_metrics = volume_metrics.join(trend_metrics, on="disease_name", how="left")
    burden_metrics = burden_metrics.join(outbreak_metrics, on="disease_name", how="left")
    burden_metrics = burden_metrics.join(variability_metrics, on="disease_name", how="left")
    logger.info(f"Merged metrics: {burden_metrics.height} rows, {burden_metrics.width} columns")
    
    # 7. Normalize metrics
    logger.info("Step 7: Normalizing metrics")
    metrics_to_normalize = [
        "total_cases",
        "annual_avg_cases",
        "peak_weekly_cases",
        "incidence_rate_per_100k",
        "cagr",
        "outbreak_frequency",
        "outbreak_intensity",
        "coefficient_variation"
    ]
    
    # Create composite scores from normalized metrics
    burden_metrics = normalize_metrics(burden_metrics, metrics_to_normalize)
    
    # Calculate composite burden score components
    burden_metrics = burden_metrics.with_columns([
        (
            (pl.col("total_cases_score") + pl.col("annual_avg_cases_score") + 
             pl.col("peak_weekly_cases_score") + pl.col("incidence_rate_per_100k_score")) / 4
        ).alias("volume_score"),
        (
            (pl.col("cagr_score").fill_null(0))
        ).alias("trend_score"),
        (
            (pl.col("outbreak_frequency_score") + pl.col("outbreak_intensity_score").fill_null(0)) / 2
        ).alias("outbreak_score"),
        pl.col("coefficient_variation_score").alias("variability_score")
    ])
    
    # 8. Calculate composite burden score
    logger.info("Step 8: Calculating composite burden scores")
    burden_metrics = calculate_composite_burden_score(burden_metrics)
    
    # 9. Add data quality flags
    logger.info("Step 9: Adding data quality flags")
    burden_metrics = flag_data_quality(burden_metrics, df)
    
    # 10. Sort by composite burden score
    burden_metrics = burden_metrics.sort("composite_burden_score", descending=True)
    
    # 11. Save results
    logger.info("Step 10: Saving results")
    
    # Create output directories if they don't exist
    Path(PROCESSED_DATA_DIR).mkdir(parents=True, exist_ok=True)
    Path(RESULTS_TABLES_DIR).mkdir(parents=True, exist_ok=True)
    
    # Save complete burden metrics
    output_path = Path(BURDEN_METRICS_PATH)
    burden_metrics.write_csv(output_path)
    logger.info(f"✅ Burden metrics saved to: {output_path}")
    
    # Save summary table (top 20 diseases)
    summary_path = Path(RESULTS_TABLES_DIR) / "burden_metrics_summary.csv"
    burden_metrics.select([
        "disease_name",
        "total_cases",
        "cagr",
        "trend_direction",
        "outbreak_frequency",
        "coefficient_variation",
        "composite_burden_score",
        "sufficient_data",
        "trend_reliable",
        "outbreak_detectable"
    ]).head(20).write_csv(summary_path)
    logger.info(f"✅ Summary table saved to: {summary_path}")
    
    # Print summary statistics
    logger.info("=" * 80)
    logger.info("BURDEN METRICS SUMMARY")
    logger.info("=" * 80)
    
    print("\nTop 10 Diseases by Composite Burden Score:")
    print(burden_metrics.select([
        "disease_name",
        "composite_burden_score",
        "volume_score",
        "trend_score",
        "outbreak_score",
        "variability_score"
    ]).head(10))
    
    print("\nTrend Direction Distribution:")
    print(burden_metrics.group_by("trend_direction").agg([
        pl.count().alias("count")
    ]).sort("count", descending=True))
    
    print("\nData Quality Summary:")
    print(f"Sufficient data: {burden_metrics['sufficient_data'].sum()} / {burden_metrics.height}")
    print(f"Reliable trends: {burden_metrics['trend_reliable'].sum()} / {burden_metrics.height}")
    print(f"Detectable outbreaks: {burden_metrics['outbreak_detectable'].sum()} / {burden_metrics.height}")
    
    logger.info("=" * 80)
    logger.info("✅ BURDEN METRICS CALCULATION COMPLETE")
    logger.info("=" * 80)
    
    return burden_metrics


if __name__ == "__main__":
    try:
        start_time = datetime.now()
        burden_metrics = main()
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Pipeline completed in {duration:.2f} seconds")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        raise
