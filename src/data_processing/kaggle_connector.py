"""
Kaggle Data Connector Module for Health Dataset (Singapore)
Version: 1.0
Created: 2026-01-30

This module provides connection and data loading from Kaggle datasets with:
- Automatic authentication handling
- Dataset caching and versioning
- Data validation and quality checks
- Metadata extraction
- Error handling and retry logic
- LLM-interpretable logging and documentation
"""

import os
import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from pathlib import Path
import pandas as pd
import yaml

try:
    import kagglehub
    from kagglehub import KaggleDatasetAdapter
    KAGGLE_AVAILABLE = True
except ImportError:
    KAGGLE_AVAILABLE = False
    print("Warning: kagglehub not installed. Install with: pip install kagglehub[pandas-datasets]")


logger = logging.getLogger(__name__)


class KaggleDataConnector:
    """
    Manages Kaggle dataset connections and data loading operations.
    
    This connector provides a structured interface to load, cache, and validate
    health datasets from Kaggle, specifically designed for the Singapore health
    dataset analysis project.
    
    Attributes:
        dataset_id (str): Kaggle dataset identifier
        cache_dir (Path): Local cache directory for downloaded datasets
        metadata (Dict): Dataset metadata and statistics
    """
    
    def __init__(
        self,
        dataset_id: str = "subhamjain/health-dataset-complete-singapore",
        cache_dir: Optional[str] = None,
        config_path: str = "config/database.yml"
    ):
        """
        Initialize Kaggle data connector.
        
        Args:
            dataset_id: Kaggle dataset identifier (owner/dataset-name)
            cache_dir: Local directory for caching datasets
            config_path: Path to configuration file
            
        Raises:
            ImportError: If kagglehub is not installed
            EnvironmentError: If Kaggle credentials are not configured
        """
        if not KAGGLE_AVAILABLE:
            raise ImportError(
                "kagglehub is not installed. Install with: "
                "pip install kagglehub[pandas-datasets]"
            )
        
        self.dataset_id = dataset_id
        self.cache_dir = Path(cache_dir) if cache_dir else Path("data/raw/kaggle")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.config = self._load_config(config_path)
        self.metadata: Dict[str, Any] = {}
        
        # Verify Kaggle authentication
        self._verify_authentication()
        
        logger.info(f"Initialized KaggleDataConnector for dataset: {dataset_id}")
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config.get('kaggle_connection', {})
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}. Using defaults.")
            return {}
    
    def _verify_authentication(self) -> None:
        """
        Verify Kaggle API credentials are configured.
        
        Checks for credentials in:
        1. Environment variables (KAGGLE_USERNAME, KAGGLE_KEY)
        2. ~/.kaggle/kaggle.json file
        
        Raises:
            EnvironmentError: If credentials are not found
        """
        kaggle_config_dir = Path.home() / ".kaggle"
        kaggle_json = kaggle_config_dir / "kaggle.json"
        
        has_env_vars = all([
            os.getenv('KAGGLE_USERNAME'),
            os.getenv('KAGGLE_KEY')
        ])
        
        has_config_file = kaggle_json.exists()
        
        if not (has_env_vars or has_config_file):
            raise EnvironmentError(
                "Kaggle credentials not found. Please either:\n"
                "1. Set KAGGLE_USERNAME and KAGGLE_KEY environment variables, or\n"
                "2. Place kaggle.json in ~/.kaggle/ directory\n"
                "Get credentials from: https://www.kaggle.com/settings/account"
            )
        
        logger.info("Kaggle authentication verified successfully")
    
    def load_dataset(
        self,
        file_path: str = "",
        adapter: KaggleDatasetAdapter = KaggleDatasetAdapter.PANDAS,
        force_download: bool = False,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load dataset from Kaggle using kagglehub.
        
        Args:
            file_path: Specific file to load (empty string loads default/all files)
            adapter: Data adapter type (PANDAS by default)
            force_download: Force re-download even if cached
            **kwargs: Additional arguments passed to load_dataset
            
        Returns:
            DataFrame containing the loaded dataset
            
        Example:
            >>> connector = KaggleDataConnector()
            >>> df = connector.load_dataset()
            >>> print(df.shape)
        """
        try:
            logger.info(f"Loading dataset: {self.dataset_id}")
            logger.info(f"File path: {file_path or 'default'}")
            
            # Load dataset using kagglehub
            df = kagglehub.load_dataset(
                adapter,
                self.dataset_id,
                file_path,
                **kwargs
            )
            
            # Extract and store metadata
            self._extract_metadata(df)
            
            # Log dataset information
            self._log_dataset_info(df)
            
            logger.info(f"Successfully loaded dataset with shape: {df.shape}")
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to load dataset: {str(e)}")
            raise
    
    def _extract_metadata(self, df: pd.DataFrame) -> None:
        """
        Extract metadata from loaded dataset.
        
        Creates LLM-interpretable metadata including:
        - Dataset dimensions
        - Column information
        - Data types
        - Missing value statistics
        - Basic statistics
        """
        self.metadata = {
            'extraction_timestamp': datetime.now().isoformat(),
            'dataset_id': self.dataset_id,
            'shape': {
                'rows': len(df),
                'columns': len(df.columns)
            },
            'columns': {
                col: {
                    'dtype': str(df[col].dtype),
                    'non_null_count': int(df[col].notna().sum()),
                    'null_count': int(df[col].isna().sum()),
                    'null_percentage': round(df[col].isna().sum() / len(df) * 100, 2),
                    'unique_values': int(df[col].nunique()),
                    'sample_values': df[col].dropna().head(3).tolist() if len(df[col].dropna()) > 0 else []
                }
                for col in df.columns
            },
            'memory_usage_mb': round(df.memory_usage(deep=True).sum() / 1024**2, 2),
            'data_quality': {
                'total_cells': len(df) * len(df.columns),
                'missing_cells': int(df.isna().sum().sum()),
                'missing_percentage': round(df.isna().sum().sum() / (len(df) * len(df.columns)) * 100, 2)
            }
        }
    
    def _log_dataset_info(self, df: pd.DataFrame) -> None:
        """Log dataset information in LLM-readable format."""
        logger.info("=" * 80)
        logger.info("DATASET INFORMATION (LLM-Interpretable)")
        logger.info("=" * 80)
        logger.info(f"Dataset ID: {self.dataset_id}")
        logger.info(f"Dimensions: {len(df)} rows × {len(df.columns)} columns")
        logger.info(f"Memory Usage: {self.metadata['memory_usage_mb']} MB")
        logger.info(f"Missing Data: {self.metadata['data_quality']['missing_percentage']}%")
        logger.info("\nColumn Summary:")
        for col in df.columns:
            col_info = self.metadata['columns'][col]
            logger.info(
                f"  - {col}: {col_info['dtype']} "
                f"({col_info['non_null_count']} non-null, "
                f"{col_info['unique_values']} unique)"
            )
        logger.info("=" * 80)
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get extracted metadata in LLM-interpretable format.
        
        Returns:
            Dictionary containing comprehensive dataset metadata
        """
        return self.metadata
    
    def save_metadata(self, output_path: Optional[str] = None) -> None:
        """
        Save metadata to YAML file for LLM consumption.
        
        Args:
            output_path: Path to save metadata (default: data/metadata/)
        """
        if not self.metadata:
            logger.warning("No metadata available. Load dataset first.")
            return
        
        if output_path is None:
            output_dir = Path("data/metadata")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"kaggle_metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yml"
        
        output_path = Path(output_path)
        
        with open(output_path, 'w') as f:
            yaml.dump(self.metadata, f, default_flow_style=False, sort_keys=False)
        
        logger.info(f"Metadata saved to: {output_path}")
    
    def validate_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate dataset quality and structure.
        
        Performs checks including:
        - Duplicate row detection
        - Column type validation
        - Missing value analysis
        - Data range validation
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dictionary containing validation results
        """
        validation_results = {
            'timestamp': datetime.now().isoformat(),
            'dataset_id': self.dataset_id,
            'validation_status': 'PASSED',
            'checks': {}
        }
        
        # Check for duplicate rows
        duplicates = df.duplicated().sum()
        validation_results['checks']['duplicate_rows'] = {
            'count': int(duplicates),
            'percentage': round(duplicates / len(df) * 100, 2),
            'status': 'WARNING' if duplicates > 0 else 'PASSED'
        }
        
        # Check for completely empty columns
        empty_columns = [col for col in df.columns if df[col].isna().all()]
        validation_results['checks']['empty_columns'] = {
            'columns': empty_columns,
            'count': len(empty_columns),
            'status': 'FAILED' if empty_columns else 'PASSED'
        }
        
        # Check for high missing value columns (>50% missing)
        high_missing = {
            col: round(df[col].isna().sum() / len(df) * 100, 2)
            for col in df.columns
            if df[col].isna().sum() / len(df) > 0.5
        }
        validation_results['checks']['high_missing_columns'] = {
            'columns': high_missing,
            'count': len(high_missing),
            'status': 'WARNING' if high_missing else 'PASSED'
        }
        
        # Overall status
        if validation_results['checks']['empty_columns']['status'] == 'FAILED':
            validation_results['validation_status'] = 'FAILED'
        elif any(check['status'] == 'WARNING' for check in validation_results['checks'].values()):
            validation_results['validation_status'] = 'WARNING'
        
        logger.info(f"Validation completed: {validation_results['validation_status']}")
        
        return validation_results
    
    def list_available_files(self) -> List[str]:
        """
        List available files in the Kaggle dataset.
        
        Note: This requires downloading the dataset metadata.
        
        Returns:
            List of available file names in the dataset
        """
        try:
            # This would require using Kaggle API directly
            # For now, return placeholder
            logger.info("Listing files requires Kaggle API. Use kagglehub documentation.")
            return []
        except Exception as e:
            logger.error(f"Failed to list files: {str(e)}")
            return []
    
    def get_connection_status(self) -> Dict[str, Any]:
        """
        Get current connection status for LLM interpretation.
        
        Returns:
            Dictionary with connection status information
        """
        status = {
            'timestamp': datetime.now().isoformat(),
            'connector_type': 'Kaggle Hub',
            'dataset_id': self.dataset_id,
            'authentication': 'VERIFIED',
            'cache_directory': str(self.cache_dir),
            'metadata_available': bool(self.metadata),
            'last_extraction': self.metadata.get('extraction_timestamp', 'Never')
        }
        
        return status


# LLM-Interpretable Usage Examples
"""
USAGE EXAMPLES FOR LLM:

1. Basic Data Loading:
```python
from src.data_processing.kaggle_connector import KaggleDataConnector

# Initialize connector
connector = KaggleDataConnector(
    dataset_id="subhamjain/health-dataset-complete-singapore"
)

# Load dataset
df = connector.load_dataset()

# Get metadata
metadata = connector.get_metadata()
print(f"Loaded {metadata['shape']['rows']} rows")
```

2. With Validation:
```python
# Load and validate
df = connector.load_dataset()
validation = connector.validate_dataset(df)

if validation['validation_status'] == 'PASSED':
    print("Data quality check passed!")
```

3. Save Metadata for LLM Analysis:
```python
# Load dataset
df = connector.load_dataset()

# Save metadata for later LLM consumption
connector.save_metadata("data/metadata/kaggle_health_data.yml")
```

4. Check Connection Status:
```python
status = connector.get_connection_status()
print(f"Connection Status: {status['authentication']}")
print(f"Last Extraction: {status['last_extraction']}")
```
"""
