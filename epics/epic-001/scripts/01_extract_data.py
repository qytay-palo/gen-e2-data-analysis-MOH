#!/usr/bin/env python3
"""
Script: Extract Data for Epic 001
Description: Extract facility utilization data from Kaggle dataset
Inputs: Kaggle dataset via API
Outputs: Raw CSV files in data/raw/
Dependencies: kagglehub, pandas
"""

import argparse
import sys
from pathlib import Path

# Add src to path
epic_root = Path(__file__).parent.parent
sys.path.insert(0, str(epic_root / 'src'))

from extraction import FacilityDataExtractor
from utils import load_config, setup_logging, Timer


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Extract facility utilization data from Kaggle"
    )
    parser.add_argument(
        '--config',
        type=str,
        default=str(epic_root / 'config' / 'epic_001_config.yml'),
        help='Path to configuration file'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default=str(epic_root / 'data' / 'raw'),
        help='Output directory for raw data'
    )
    parser.add_argument(
        '--year-start',
        type=int,
        default=2006,
        help='Start year for data extraction'
    )
    parser.add_argument(
        '--year-end',
        type=int,
        default=2020,
        help='End year for data extraction'
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
    log_dir.mkdir(parents=True, exist_ok=True)
    logger = setup_logging(
        log_level=args.log_level,
        log_file=log_dir / 'extraction.log'
    )
    
    logger.info("=" * 80)
    logger.info("EPIC-001: Data Extraction Phase")
    logger.info("=" * 80)
    logger.info(f"Configuration: {args.config}")
    logger.info(f"Output directory: {args.output_dir}")
    logger.info(f"Year range: {args.year_start}-{args.year_end}")
    
    # Start timer
    timer = Timer(logger)
    timer.start("Starting data extraction")
    
    try:
        # Initialize extractor
        dataset_id = config['data_source']['dataset_id']
        logger.info(f"Dataset ID: {dataset_id}")
        
        extractor = FacilityDataExtractor(dataset_id=dataset_id, logger=logger)
        
        # Extract all data
        year_range = (args.year_start, args.year_end)
        data_tables = extractor.extract_all(year_range=year_range)
        
        logger.info(f"Successfully extracted {len(data_tables)} tables:")
        for table_name, df in data_tables.items():
            logger.info(f"  - {table_name}: {len(df)} records, {len(df.columns)} columns")
        
        # Save extracted data
        output_dir = Path(args.output_dir)
        saved_files = extractor.save_extracted_data(
            data_tables,
            output_dir,
            file_format='csv'
        )
        
        logger.info(f"Saved {len(saved_files)} files to {output_dir}")
        for table_name, file_path in saved_files.items():
            logger.info(f"  - {file_path}")
        
        timer.stop("Data extraction completed")
        logger.info("=" * 80)
        logger.info("Data extraction phase completed successfully!")
        logger.info("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Error during data extraction: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
