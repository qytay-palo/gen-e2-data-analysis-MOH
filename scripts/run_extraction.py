"""
Manual Data Extraction Script
Version: 1.0
Created: 2026-01-26

Script for running data extraction manually with command-line options.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.data_processing.etl_pipeline import ETLPipeline
from src.utils.logging_config import setup_logging
from src.utils.monitoring import PerformanceMonitor


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='MOH Polyclinic Data Extraction Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--sources',
        nargs='+',
        help='Data sources to extract (space-separated). Use "all" for all sources.',
        default=['all']
    )
    
    parser.add_argument(
        '--start-date',
        help='Start date for extraction (YYYY-MM-DD)',
        default=None
    )
    
    parser.add_argument(
        '--end-date',
        help='End date for extraction (YYYY-MM-DD)',
        default=None
    )
    
    parser.add_argument(
        '--incremental',
        action='store_true',
        help='Use incremental extraction mode',
        default=True
    )
    
    parser.add_argument(
        '--full',
        action='store_true',
        help='Use full extraction mode (overrides --incremental)',
        default=False
    )
    
    parser.add_argument(
        '--last-n-days',
        type=int,
        help='Extract data from last N days',
        default=None
    )
    
    parser.add_argument(
        '--stop-on-validation-failure',
        action='store_true',
        help='Stop pipeline if validation fails',
        default=False
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Logging level'
    )
    
    parser.add_argument(
        '--config',
        default='config/database.yml',
        help='Path to database configuration file'
    )
    
    parser.add_argument(
        '--queries',
        default='config/queries.yml',
        help='Path to queries configuration file'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(
        log_level=args.log_level,
        log_dir='logs',
        enable_console=True,
        enable_file=True
    )
    
    print("="*70)
    print("MOH Polyclinic Data Extraction")
    print("="*70)
    print()
    
    # Process arguments
    sources = None if 'all' in args.sources else args.sources
    incremental = not args.full and args.incremental
    
    # Calculate date range
    start_date = args.start_date
    end_date = args.end_date
    
    if args.last_n_days:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=args.last_n_days)).strftime('%Y-%m-%d')
    
    # Print configuration
    print(f"Configuration:")
    print(f"  Sources: {sources or 'all'}")
    print(f"  Mode: {'Incremental' if incremental else 'Full'}")
    print(f"  Start Date: {start_date or 'default'}")
    print(f"  End Date: {end_date or 'default'}")
    print(f"  Stop on Validation Failure: {args.stop_on_validation_failure}")
    print()
    
    # Initialize pipeline
    pipeline = ETLPipeline(args.config, args.queries)
    monitor = PerformanceMonitor()
    
    # Run extraction
    try:
        metric = monitor.start_monitoring('full_pipeline')
        
        result = pipeline.run_full_pipeline(
            sources=sources,
            start_date=start_date,
            end_date=end_date,
            incremental=incremental,
            stop_on_validation_failure=args.stop_on_validation_failure
        )
        
        monitor.stop_monitoring(metric, status='success')
        
        # Print summary
        print()
        print("="*70)
        print("EXTRACTION SUMMARY")
        print("="*70)
        print(f"Status: {result['status']}")
        print(f"Duration: {result['duration_seconds']:.1f} seconds")
        print(f"Sources Processed: {result['sources_processed']}")
        print(f"Total Rows Extracted: {result['total_rows_extracted']:,}")
        print(f"Total Rows Loaded: {result['total_rows_loaded']:,}")
        print()
        
        if result.get('validation_summary'):
            print("Validation Results:")
            for source, val_result in result['validation_summary'].items():
                print(f"  {source}:")
                print(f"    Passed: {val_result['passed']}/{val_result['total']}")
                print(f"    Success Rate: {val_result['success_rate']:.1f}%")
        
        print()
        print("Output Files:")
        for source, paths in result.get('output_paths', {}).items():
            print(f"  {source}:")
            for path in paths:
                print(f"    - {path}")
        
        print()
        print("="*70)
        
        # Save performance metrics
        monitor.save_metrics()
        
        return 0
        
    except Exception as e:
        print()
        print("="*70)
        print("EXTRACTION FAILED")
        print("="*70)
        print(f"Error: {str(e)}")
        print()
        
        monitor.stop_monitoring(metric, status='failed', error=str(e))
        monitor.save_metrics()
        
        return 1


if __name__ == '__main__':
    sys.exit(main())
