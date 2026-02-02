#!/usr/bin/env python3
"""
Script: Run Full Pipeline for Epic 001
Description: Execute complete end-to-end pipeline for facility utilization analysis
Inputs: Kaggle dataset
Outputs: Complete analysis, visualizations, and reports
Dependencies: All epic-001 modules
"""

import argparse
import sys
from pathlib import Path

# Add src to path
epic_root = Path(__file__).parent.parent
sys.path.insert(0, str(epic_root / 'src'))

from utils import load_config, setup_logging, Timer, ProgressTracker
import subprocess


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Run complete Epic 001 analysis pipeline"
    )
    parser.add_argument(
        '--config',
        type=str,
        default=str(epic_root / 'config' / 'epic_001_config.yml'),
        help='Path to configuration file'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level'
    )
    parser.add_argument(
        '--skip-extraction',
        action='store_true',
        help='Skip data extraction (use existing data)'
    )
    parser.add_argument(
        '--skip-features',
        action='store_true',
        help='Skip feature engineering (use existing features)'
    )
    
    return parser.parse_args()


def run_script(script_path: Path, args: list, logger):
    """Run a Python script as subprocess"""
    cmd = [sys.executable, str(script_path)] + args
    logger.info(f"Running: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        logger.error(f"Script failed with return code {result.returncode}")
        logger.error(f"STDERR: {result.stderr}")
        raise RuntimeError(f"Script {script_path.name} failed")
    
    return result


def main():
    """Main execution function"""
    args = parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Setup logging
    log_dir = epic_root / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = setup_logging(
        log_level=args.log_level,
        log_file=log_dir / 'pipeline.log'
    )
    
    logger.info("=" * 80)
    logger.info("EPIC-001: FACILITY UTILIZATION & BOTTLENECK ANALYSIS")
    logger.info("Full Pipeline Execution")
    logger.info("=" * 80)
    
    # Start timer
    timer = Timer(logger)
    timer.start("Starting full pipeline")
    
    # Progress tracker
    total_steps = 5 if not args.skip_extraction and not args.skip_features else \
                  4 if args.skip_extraction or args.skip_features else 3
    progress = ProgressTracker(total_steps, logger)
    
    try:
        scripts_dir = epic_root / 'scripts'
        
        # Phase 1: Data Extraction
        if not args.skip_extraction:
            progress.update("Data Extraction")
            logger.info("Phase 1: Data Extraction")
            run_script(
                scripts_dir / '01_extract_data.py',
                ['--log-level', args.log_level],
                logger
            )
        else:
            logger.info("Skipping data extraction (using existing data)")
        
        # Phase 2: Feature Engineering
        if not args.skip_features:
            progress.update("Feature Engineering")
            logger.info("Phase 2: Feature Engineering")
            run_script(
                scripts_dir / '02_engineer_features.py',
                ['--log-level', args.log_level],
                logger
            )
        else:
            logger.info("Skipping feature engineering (using existing features)")
        
        # Phase 3: Analysis
        progress.update("Analysis")
        logger.info("Phase 3: Analysis")
        run_script(
            scripts_dir / '03_run_analysis.py',
            ['--log-level', args.log_level],
            logger
        )
        
        # Phase 4: Visualization
        progress.update("Visualization")
        logger.info("Phase 4: Visualization")
        run_script(
            scripts_dir / '04_generate_visualizations.py',
            ['--log-level', args.log_level],
            logger
        )
        
        # Phase 5: Summary
        progress.update("Generating Summary")
        logger.info("Phase 5: Generating Summary Report")
        
        # Read key metrics
        import pandas as pd
        import json
        
        summary_file = epic_root / 'results' / 'metrics' / 'analysis_summary.json'
        if summary_file.exists():
            with open(summary_file, 'r') as f:
                summary = json.load(f)
            
            logger.info("\n" + "=" * 80)
            logger.info("PIPELINE EXECUTION SUMMARY")
            logger.info("=" * 80)
            logger.info(f"Total Facilities Analyzed: {summary['total_facilities']}")
            logger.info(f"Critical Bottlenecks Identified: {summary['total_bottlenecks']}")
            logger.info(f"Recommendations Generated: {summary['total_recommendations']}")
            logger.info(f"Average Utilization Rate: {summary['avg_utilization']:.1f}%")
            logger.info(f"Median Utilization Rate: {summary['median_utilization']:.1f}%")
            logger.info("=" * 80)
        
        progress.complete()
        timer.stop("Full pipeline completed")
        
        logger.info("\n" + "=" * 80)
        logger.info("SUCCESS: Epic 001 pipeline completed successfully!")
        logger.info("=" * 80)
        logger.info("\nOutputs:")
        logger.info(f"  - Raw Data: {epic_root / 'data' / 'raw'}")
        logger.info(f"  - Features: {epic_root / 'data' / 'features'}")
        logger.info(f"  - Results: {epic_root / 'results'}")
        logger.info(f"  - Figures: {epic_root / 'reports' / 'figures'}")
        logger.info(f"  - Logs: {epic_root / 'logs'}")
        logger.info("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
