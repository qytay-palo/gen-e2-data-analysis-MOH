#!/usr/bin/env python3
"""
Script: Engineer Features for Epic 001
Description: Calculate utilization rates and performance metrics
Inputs: Raw CSV files from data/raw/
Outputs: Feature-engineered data in data/features/
Dependencies: pandas, numpy
"""

import argparse
import sys
from pathlib import Path
import pandas as pd

# Add src to path
epic_root = Path(__file__).parent.parent
sys.path.insert(0, str(epic_root / 'src'))

from features import UtilizationFeatureEngineer
from utils import load_config, setup_logging, Timer


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Engineer features for facility utilization analysis"
    )
    parser.add_argument(
        '--config',
        type=str,
        default=str(epic_root / 'config' / 'epic_001_config.yml'),
        help='Path to configuration file'
    )
    parser.add_argument(
        '--params',
        type=str,
        default=str(epic_root / 'config' / 'epic_001_params.yml'),
        help='Path to parameters file'
    )
    parser.add_argument(
        '--input-dir',
        type=str,
        default=str(epic_root / 'data' / 'raw'),
        help='Input directory with raw data'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default=str(epic_root / 'data' / 'features'),
        help='Output directory for features'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level'
    )
    
    return parser.parse_args()


def main():
    """Main execution function"""
    args = parse_args()
    
    # Load configuration
    config = load_config(args.config)
    params = load_config(args.params)
    
    # Setup logging
    log_dir = epic_root / 'logs'
    logger = setup_logging(
        log_level=args.log_level,
        log_file=log_dir / 'pipeline.log'
    )
    
    logger.info("=" * 80)
    logger.info("EPIC-001: Feature Engineering Phase")
    logger.info("=" * 80)
    
    # Start timer
    timer = Timer(logger)
    timer.start("Starting feature engineering")
    
    try:
        # Load raw data
        input_dir = Path(args.input_dir)
        logger.info(f"Loading data from {input_dir}")
        
        attendance_file = input_dir / 'attendance_by_hospitals.csv'
        beds_file = input_dir / 'bed_capacity.csv'
        
        if not attendance_file.exists():
            raise FileNotFoundError(f"Attendance data not found: {attendance_file}")
        if not beds_file.exists():
            raise FileNotFoundError(f"Bed capacity data not found: {beds_file}")
        
        attendance_df = pd.read_csv(attendance_file)
        beds_df = pd.read_csv(beds_file)
        
        logger.info(f"Loaded attendance data: {len(attendance_df)} records")
        logger.info(f"Loaded bed capacity data: {len(beds_df)} records")
        
        # Initialize feature engineer
        engineer = UtilizationFeatureEngineer(logger=logger)
        
        # Engineer all features
        utilization_thresholds = params.get('utilization_analysis', {}).get('thresholds', {})
        feature_config = {'thresholds': utilization_thresholds}
        
        utilization_df = engineer.engineer_all_features(
            attendance_df,
            beds_df,
            config=feature_config
        )
        
        logger.info(f"Feature engineering complete: {len(utilization_df)} records, {len(utilization_df.columns)} features")
        
        # Identify bottlenecks
        bottleneck_config = params.get('bottleneck_detection', {})
        bottlenecks_df = engineer.identify_bottlenecks(
            utilization_df,
            threshold=bottleneck_config.get('min_utilization', 90.0),
            recent_years_only=True,
            recent_year_threshold=bottleneck_config.get('filters', {}).get('min_years_of_data', 2015)
        )
        
        logger.info(f"Identified {len(bottlenecks_df)} bottleneck facilities")
        
        # Save features
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save main features
        utilization_file = output_dir / 'utilization_metrics.parquet'
        utilization_df.to_parquet(utilization_file, index=False)
        logger.info(f"Saved utilization metrics to {utilization_file}")
        
        # Also save as CSV for easy inspection
        utilization_csv = output_dir / 'utilization_metrics.csv'
        utilization_df.to_csv(utilization_csv, index=False)
        
        # Save bottlenecks
        if len(bottlenecks_df) > 0:
            bottlenecks_file = output_dir / 'bottlenecks.csv'
            bottlenecks_df.to_csv(bottlenecks_file, index=False)
            logger.info(f"Saved bottlenecks to {bottlenecks_file}")
        
        timer.stop("Feature engineering completed")
        logger.info("=" * 80)
        logger.info("Feature engineering phase completed successfully!")
        logger.info("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Error during feature engineering: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
