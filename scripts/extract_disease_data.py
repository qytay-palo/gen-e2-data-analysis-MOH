"""Data extraction script for infectious disease surveillance data."""
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import polars as pl

try:
    import kagglehub
except ImportError:
    raise ImportError(
        "kagglehub is required. Install with: pip install kagglehub"
    )

from src.config import DATASET_ID, DATA_FILE, RAW_DATA_DIR
from src.utils.logger import setup_logger
from src.data_processing.validation import validate_disease_data

logger = setup_logger(__name__, log_file="logs/data_extraction.log")

def check_kaggle_credentials() -> bool:
    """Verify Kaggle API credentials are configured.
    
    Returns:
        True if credentials exist, False otherwise
    """
    kaggle_json_path = Path.home() / ".kaggle" / "kaggle.json"
    
    if not kaggle_json_path.exists():
        logger.error(
            f"Kaggle credentials not found at {kaggle_json_path}\n"
            "Please set up Kaggle API credentials:\n"
            "1. Go to https://www.kaggle.com/account\n"
            "2. Click 'Create New API Token'\n"
            "3. Save kaggle.json to ~/.kaggle/\n"
            "4. Run: chmod 600 ~/.kaggle/kaggle.json"
        )
        return False
    
    # Check file permissions (should be 600)
    stat_info = kaggle_json_path.stat()
    if oct(stat_info.st_mode)[-3:] != '600':
        logger.warning(
            f"Insecure permissions on {kaggle_json_path}\n"
            "Run: chmod 600 ~/.kaggle/kaggle.json"
        )
    
    return True


def download_dataset(
    dataset_id: str = DATASET_ID,
    force_download: bool = False
) -> Optional[str]:
    """Download dataset from Kaggle with retry logic.
    
    Args:
        dataset_id: Kaggle dataset identifier
        force_download: Force re-download even if cached
        
    Returns:
        Path to downloaded dataset directory, or None if failed
    """
    logger.info(f"Downloading dataset: {dataset_id}")
    
    try:
        # Download using kagglehub (handles caching automatically)
        dataset_path = kagglehub.dataset_download(
            dataset_id,
            force_download=force_download
        )
        
        logger.info(f"Dataset downloaded to: {dataset_path}")
        return dataset_path
        
    except Exception as e:
        logger.error(f"Failed to download dataset: {str(e)}")
        logger.info("Attempting retry in 5 seconds...")
        
        import time
        time.sleep(5)
        
        try:
            dataset_path = kagglehub.dataset_download(dataset_id)
            logger.info(f"Retry successful. Dataset at: {dataset_path}")
            return dataset_path
        except Exception as retry_error:
            logger.error(f"Retry failed: {str(retry_error)}")
            return None


def load_csv_to_polars(
    file_path: str,
    expected_columns: Optional[list] = None
) -> Optional[pl.DataFrame]:
    """Load CSV file into Polars DataFrame with validation.
    
    Args:
        file_path: Path to CSV file
        expected_columns: Optional list of expected column names
        
    Returns:
        Polars DataFrame, or None if loading failed
    """
    logger.info(f"Loading CSV file: {file_path}")
    
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return None
    
    try:
        # Read CSV with Polars
        df = pl.read_csv(file_path)
        logger.info(f"Loaded {df.height} rows, {len(df.columns)} columns")
        
        # Validate columns if expected list provided
        if expected_columns:
            actual_cols = set(df.columns)
            expected_cols = set(expected_columns)
            
            if actual_cols != expected_cols:
                missing = expected_cols - actual_cols
                extra = actual_cols - expected_cols
                
                if missing:
                    logger.warning(f"Missing expected columns: {missing}")
                if extra:
                    logger.warning(f"Unexpected columns found: {extra}")
        
        # Display sample
        logger.info(f"Sample data:\n{df.head()}")
        logger.info(f"Schema: {df.schema}")
        
        return df
        
    except Exception as e:
        logger.error(f"Failed to load CSV: {str(e)}")
        return None


def save_raw_data_with_metadata(
    df: pl.DataFrame,
    output_dir: str = RAW_DATA_DIR,
    filename: str = "disease_data.parquet"
) -> bool:
    """Save raw data with extraction metadata.
    
    Args:
        df: DataFrame to save
        output_dir: Output directory path
        filename: Output filename
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Save data as Parquet
        output_path = Path(output_dir) / filename
        df.write_parquet(output_path)
        logger.info(f"Saved raw data to: {output_path}")
        
        # Save metadata
        metadata = {
            "extraction_timestamp": datetime.now().isoformat(),
            "source_dataset": DATASET_ID,
            "record_count": df.height,
            "column_count": len(df.columns),
            "columns": df.columns,
            "file_path": str(output_path)
        }
        
        metadata_path = Path(output_dir) / "extraction_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"Saved metadata to: {metadata_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to save data: {str(e)}")
        return False


def extract_disease_data(
    force_download: bool = False,
    validate: bool = True
) -> Optional[pl.DataFrame]:
    """Main extraction pipeline: download, load, validate, and save.
    
    Args:
        force_download: Force re-download from Kaggle
        validate: Run data quality validation
        
    Returns:
        Extracted DataFrame, or None if failed
    """
    logger.info("=" * 80)
    logger.info("STARTING DATA EXTRACTION PIPELINE")
    logger.info("=" * 80)
    
    # Step 1: Download dataset
    dataset_path = download_dataset(DATASET_ID, force_download)
    if not dataset_path:
        logger.error("Dataset download failed. Aborting.")
        return None
    
    # Step 2: Construct file path
    csv_path = Path(dataset_path) / DATA_FILE
    if not csv_path.exists():
        logger.error(f"Expected file not found: {csv_path}")
        logger.info("Available files in dataset directory:")
        for item in Path(dataset_path).rglob("*"):
            if item.is_file():
                logger.info(f"  - {item}")
        return None
    
    # Step 3: Load CSV
    expected_cols = ["epi_week", "disease", "no._of_cases"]
    df = load_csv_to_polars(str(csv_path), expected_cols)
    if df is None:
        logger.error("CSV loading failed. Aborting.")
        return None
    
    # Step 4: Validate data quality
    if validate:
        logger.info("Running data quality validation...")
        validation_report = validate_disease_data(df)
        
        # Save validation report
        report_path = Path("results/tables") / "data_quality_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(validation_report, f, indent=2)
        logger.info(f"Validation report saved to: {report_path}")
        
        # Check if critical validations passed
        critical_checks = ["schema", "missing_values", "case_count_range"]
        critical_passed = all(
            validation_report["validations"].get(check, {}).get("passed", False)
            for check in critical_checks
        )
        
        if not critical_passed:
            logger.warning("Critical validation checks failed!")
            logger.info("Review validation report for details.")
    
    # Step 5: Save raw data
    success = save_raw_data_with_metadata(df)
    if not success:
        logger.warning("Failed to save raw data to local storage.")
    
    logger.info("=" * 80)
    logger.info("DATA EXTRACTION COMPLETE")
    logger.info(f"Records extracted: {df.height}")
    logger.info(f"Unique diseases: {df['disease'].n_unique()}")
    logger.info("=" * 80)
    
    return df


if __name__ == "__main__":
    # Run extraction pipeline
    df = extract_disease_data(force_download=False, validate=True)
    
    if df is not None:
        print("\n✅ Data extraction successful!")
        print(f"📊 {df.height} records extracted")
        print(f"🦠 {df['disease'].n_unique()} unique diseases")
    else:
        print("\n❌ Data extraction failed. Check logs for details.")
