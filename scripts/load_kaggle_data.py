#!/usr/bin/env python3
"""
Kaggle Data Loader Script
Load Singapore health dataset from Kaggle for MOH analysis

Usage:
    python scripts/load_kaggle_data.py
    python scripts/load_kaggle_data.py --validate
    python scripts/load_kaggle_data.py --save-metadata
    python scripts/load_kaggle_data.py --output data/processed/kaggle_health.parquet
"""

import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_processing.kaggle_connector import KaggleDataConnector
from src.utils.logging_config import setup_logging


def main():
    """Main execution function."""
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Load Singapore health dataset from Kaggle"
    )
    parser.add_argument(
        '--dataset-id',
        default='subhamjain/health-dataset-complete-singapore',
        help='Kaggle dataset identifier'
    )
    parser.add_argument(
        '--output',
        default='data/raw/kaggle/health_data.parquet',
        help='Output file path (supports .csv, .parquet, .pkl)'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Run data validation checks'
    )
    parser.add_argument(
        '--save-metadata',
        action='store_true',
        help='Save metadata to YAML file'
    )
    parser.add_argument(
        '--force-download',
        action='store_true',
        help='Force re-download from Kaggle (bypass cache)'
    )
    parser.add_argument(
        '--sample',
        type=int,
        help='Load only a sample of N rows (for testing)'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 80)
    logger.info("KAGGLE DATA LOADER - START")
    logger.info("=" * 80)
    logger.info(f"Dataset: {args.dataset_id}")
    logger.info(f"Output: {args.output}")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    
    try:
        # Initialize connector
        logger.info("Initializing Kaggle connector...")
        connector = KaggleDataConnector(dataset_id=args.dataset_id)
        
        # Check connection status
        status = connector.get_connection_status()
        logger.info(f"Connection status: {status['authentication']}")
        
        # Load dataset
        logger.info("Loading dataset from Kaggle...")
        df = connector.load_dataset()
        
        logger.info(f"✓ Dataset loaded successfully: {df.shape[0]:,} rows × {df.shape[1]} columns")
        
        # Sample if requested
        if args.sample:
            logger.info(f"Sampling {args.sample} rows...")
            df = df.sample(n=min(args.sample, len(df)), random_state=42)
            logger.info(f"✓ Sampled to {len(df):,} rows")
        
        # Validate if requested
        if args.validate:
            logger.info("Running data validation...")
            validation = connector.validate_dataset(df)
            logger.info(f"Validation status: {validation['validation_status']}")
            
            if validation['validation_status'] != 'PASSED':
                logger.warning("Data quality issues detected:")
                for check_name, check_result in validation['checks'].items():
                    if check_result.get('status') != 'PASSED':
                        logger.warning(f"  - {check_name}: {check_result}")
        
        # Save metadata if requested
        if args.save_metadata:
            logger.info("Saving metadata...")
            metadata_path = Path("data/metadata/kaggle") / f"kaggle_load_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yml"
            connector.save_metadata(str(metadata_path))
            logger.info(f"✓ Metadata saved to: {metadata_path}")
        
        # Save dataset to output path
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Saving dataset to: {output_path}")
        
        if output_path.suffix == '.csv':
            df.to_csv(output_path, index=False)
        elif output_path.suffix == '.parquet':
            df.to_parquet(output_path, index=False, compression='snappy')
        elif output_path.suffix == '.pkl':
            df.to_pickle(output_path)
        else:
            logger.error(f"Unsupported file format: {output_path.suffix}")
            logger.error("Supported formats: .csv, .parquet, .pkl")
            return 1
        
        logger.info(f"✓ Dataset saved successfully")
        
        # Print summary
        logger.info("=" * 80)
        logger.info("SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Rows loaded: {df.shape[0]:,}")
        logger.info(f"Columns: {df.shape[1]}")
        logger.info(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        logger.info(f"Output file: {output_path}")
        logger.info(f"File size: {output_path.stat().st_size / 1024**2:.2f} MB")
        
        # Print column overview
        logger.info("\nColumn Overview:")
        metadata = connector.get_metadata()
        for col in df.columns[:10]:  # First 10 columns
            col_info = metadata['columns'][col]
            logger.info(
                f"  {col:30s} | {col_info['dtype']:10s} | "
                f"{col_info['non_null_count']:,} non-null | "
                f"{col_info['unique_values']:,} unique"
            )
        if len(df.columns) > 10:
            logger.info(f"  ... and {len(df.columns) - 10} more columns")
        
        logger.info("=" * 80)
        logger.info("KAGGLE DATA LOADER - COMPLETE")
        logger.info("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error("=" * 80)
        logger.error("ERROR OCCURRED")
        logger.error("=" * 80)
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {str(e)}")
        logger.error("", exc_info=True)
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
