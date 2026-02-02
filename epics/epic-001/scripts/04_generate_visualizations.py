#!/usr/bin/env python3
"""
Script: Generate Visualizations for Epic 001
Description: Create visualizations and dashboards
Inputs: Feature data and analysis results
Outputs: Figures in reports/figures/
Dependencies: plotly, matplotlib
"""

import argparse
import sys
from pathlib import Path
import pandas as pd

# Add src to path
epic_root = Path(__file__).parent.parent
sys.path.insert(0, str(epic_root / 'src'))

from visualization import UtilizationVisualizer
from utils import load_config, setup_logging, Timer


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Generate visualizations for facility utilization analysis"
    )
    parser.add_argument(
        '--config',
        type=str,
        default=str(epic_root / 'config' / 'epic_001_config.yml'),
        help='Path to configuration file'
    )
    parser.add_argument(
        '--features-dir',
        type=str,
        default=str(epic_root / 'data' / 'features'),
        help='Input directory with feature data'
    )
    parser.add_argument(
        '--results-dir',
        type=str,
        default=str(epic_root / 'results' / 'tables'),
        help='Input directory with analysis results'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default=str(epic_root / 'reports' / 'figures'),
        help='Output directory for figures'
    )
    parser.add_argument(
        '--formats',
        nargs='+',
        default=['html', 'png'],
        choices=['html', 'png', 'pdf', 'svg'],
        help='Output formats for figures'
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
    
    # Setup logging
    log_dir = epic_root / 'logs'
    logger = setup_logging(
        log_level=args.log_level,
        log_file=log_dir / 'pipeline.log'
    )
    
    logger.info("=" * 80)
    logger.info("EPIC-001: Visualization Phase")
    logger.info("=" * 80)
    
    # Start timer
    timer = Timer(logger)
    timer.start("Starting visualization generation")
    
    try:
        # Load data
        features_dir = Path(args.features_dir)
        results_dir = Path(args.results_dir)
        
        logger.info(f"Loading data from {features_dir} and {results_dir}")
        
        # Load utilization data
        utilization_file = features_dir / 'utilization_metrics.parquet'
        if not utilization_file.exists():
            utilization_file = features_dir / 'utilization_metrics.csv'
        
        if utilization_file.suffix == '.parquet':
            utilization_df = pd.read_parquet(utilization_file)
        else:
            utilization_df = pd.read_csv(utilization_file)
        
        logger.info(f"Loaded utilization data: {len(utilization_df)} records")
        
        # Load analysis results
        profiles_file = results_dir / 'facility_profiles.csv'
        bottlenecks_file = results_dir / 'bottlenecks.csv'
        
        profiles_df = pd.read_csv(profiles_file) if profiles_file.exists() else None
        bottlenecks_df = pd.read_csv(bottlenecks_file) if bottlenecks_file.exists() else pd.DataFrame()
        
        if profiles_df is not None:
            logger.info(f"Loaded facility profiles: {len(profiles_df)} facilities")
        if len(bottlenecks_df) > 0:
            logger.info(f"Loaded bottlenecks: {len(bottlenecks_df)} records")
        
        # Initialize visualizer
        visualizer = UtilizationVisualizer(logger=logger)
        
        # Create all visualizations
        if profiles_df is not None:
            figures = visualizer.create_dashboard_layout(
                utilization_df,
                bottlenecks_df,
                profiles_df
            )
        else:
            logger.warning("No profiles data found, creating limited visualizations")
            figures = {
                'utilization_trend': visualizer.plot_utilization_trend(utilization_df),
                'utilization_distribution': visualizer.plot_utilization_distribution(utilization_df)
            }
        
        logger.info(f"Created {len(figures)} visualizations")
        
        # Save figures
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        visualizer.save_figures(figures, output_dir, formats=args.formats)
        
        logger.info(f"Saved {len(figures)} figures in {len(args.formats)} format(s) to {output_dir}")
        
        timer.stop("Visualization generation completed")
        logger.info("=" * 80)
        logger.info("Visualization phase completed successfully!")
        logger.info("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Error during visualization generation: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
