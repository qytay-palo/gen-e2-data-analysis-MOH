#!/usr/bin/env python3
"""
Script: Run Analysis for Epic 001
Description: Perform facility performance profiling and bottleneck analysis
Inputs: Feature-engineered data from data/features/
Outputs: Analysis results in results/
Dependencies: pandas, scipy, statsmodels
"""

import argparse
import sys
from pathlib import Path
import pandas as pd
import json

# Add src to path
epic_root = Path(__file__).parent.parent
sys.path.insert(0, str(epic_root / 'src'))

from analysis import FacilityAnalyzer
from utils import load_config, setup_logging, Timer


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Run facility utilization and bottleneck analysis"
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
        default=str(epic_root / 'data' / 'features'),
        help='Input directory with feature data'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default=str(epic_root / 'results'),
        help='Output directory for analysis results'
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
    logger.info("EPIC-001: Analysis Phase")
    logger.info("=" * 80)
    
    # Start timer
    timer = Timer(logger)
    timer.start("Starting analysis")
    
    try:
        # Load feature data
        input_dir = Path(args.input_dir)
        logger.info(f"Loading data from {input_dir}")
        
        utilization_file = input_dir / 'utilization_metrics.parquet'
        if not utilization_file.exists():
            utilization_file = input_dir / 'utilization_metrics.csv'
        
        if not utilization_file.exists():
            raise FileNotFoundError(f"Utilization data not found in {input_dir}")
        
        if utilization_file.suffix == '.parquet':
            utilization_df = pd.read_parquet(utilization_file)
        else:
            utilization_df = pd.read_csv(utilization_file)
        
        logger.info(f"Loaded utilization data: {len(utilization_df)} records")
        
        # Initialize analyzer
        analyzer = FacilityAnalyzer(logger=logger)
        
        # Run comprehensive analysis
        analysis_config = {
            'bottleneck_threshold': params.get('bottleneck_detection', {}).get('min_utilization_rate', 90.0),
            'min_severity': params.get('bottleneck_detection', {}).get('min_severity_score', 5.0)
        }
        
        results = analyzer.run_comprehensive_analysis(utilization_df, config=analysis_config)
        
        # Log summary
        summary = results['summary']
        logger.info(f"Analysis Summary:")
        logger.info(f"  - Total facilities analyzed: {summary['total_facilities']}")
        logger.info(f"  - Critical bottlenecks identified: {summary['total_bottlenecks']}")
        logger.info(f"  - Recommendations generated: {summary['total_recommendations']}")
        logger.info(f"  - Average utilization: {summary['avg_utilization']:.1f}%")
        logger.info(f"  - Median utilization: {summary['median_utilization']:.1f}%")
        
        # Save results
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        tables_dir = output_dir / 'tables'
        metrics_dir = output_dir / 'metrics'
        exports_dir = output_dir / 'exports'
        
        for dir_path in [tables_dir, metrics_dir, exports_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Save facility profiles
        profiles_file = tables_dir / 'facility_profiles.csv'
        results['profiles'].to_csv(profiles_file, index=False)
        logger.info(f"Saved facility profiles to {profiles_file}")
        
        # Save bottlenecks
        if len(results['bottlenecks']) > 0:
            bottlenecks_file = tables_dir / 'bottlenecks.csv'
            results['bottlenecks'].to_csv(bottlenecks_file, index=False)
            logger.info(f"Saved bottlenecks to {bottlenecks_file}")
        
        # Save recommendations
        if len(results['recommendations']) > 0:
            recommendations_file = tables_dir / 'recommendations.csv'
            recommendations_df = pd.DataFrame(results['recommendations'])
            recommendations_df.to_csv(recommendations_file, index=False)
            logger.info(f"Saved recommendations to {recommendations_file}")
        
        # Save summary metrics
        summary_file = metrics_dir / 'analysis_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Saved summary metrics to {summary_file}")
        
        # Save temporal analysis
        temporal_file = metrics_dir / 'temporal_analysis.json'
        with open(temporal_file, 'w') as f:
            # Convert DataFrames to dict for JSON serialization
            temporal_export = {
                k: v.to_dict() if isinstance(v, pd.DataFrame) else v
                for k, v in results['temporal_analysis'].items()
                if k != 'facility_trends'
            }
            json.dump(temporal_export, f, indent=2)
        logger.info(f"Saved temporal analysis to {temporal_file}")
        
        # Save facility trends
        if results['temporal_analysis']['facility_trends']:
            trends_file = tables_dir / 'facility_trends.csv'
            trends_df = pd.DataFrame(results['temporal_analysis']['facility_trends'])
            trends_df.to_csv(trends_file, index=False)
            logger.info(f"Saved facility trends to {trends_file}")
        
        timer.stop("Analysis completed")
        logger.info("=" * 80)
        logger.info("Analysis phase completed successfully!")
        logger.info("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
