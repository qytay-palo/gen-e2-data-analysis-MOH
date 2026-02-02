"""
Epic 001: Data Extraction Module
Extract facility utilization data from Kaggle dataset
"""

from typing import Dict, List, Tuple, Optional
import pandas as pd
import kagglehub
from pathlib import Path
import logging


class FacilityDataExtractor:
    """Extract facility utilization data from Kaggle dataset"""
    
    def __init__(
        self, 
        dataset_id: str = "subhamjain/health-dataset-complete-singapore",
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize data extractor
        
        Args:
            dataset_id: Kaggle dataset identifier
            logger: Logger instance (creates new if None)
        """
        self.dataset_id = dataset_id
        self.dataset_path: Optional[Path] = None
        self.logger = logger or logging.getLogger(__name__)
    
    def download_dataset(self) -> Path:
        """
        Download entire dataset (cached locally)
        
        Returns:
            Path to downloaded dataset
        """
        self.logger.info(f"Downloading dataset: {self.dataset_id}")
        try:
            self.dataset_path = Path(kagglehub.dataset_download(self.dataset_id))
            self.logger.info(f"Dataset cached at: {self.dataset_path}")
            return self.dataset_path
        except Exception as e:
            self.logger.error(f"Failed to download dataset: {e}")
            raise
    
    def extract_attendance_data(
        self, 
        year_range: Tuple[int, int] = (2006, 2020)
    ) -> pd.DataFrame:
        """
        Extract hospital attendance data
        
        Args:
            year_range: Tuple of (start_year, end_year)
            
        Returns:
            DataFrame with attendance data
        """
        table_name = "admission-and-outpatient-attendances-by-restructured-hospitals"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        self.logger.info(f"Extracting attendance data from {file_path}")
        df = pd.read_csv(file_path)
        
        # Apply filters
        df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1]) &
            (df['attendances_no'].notna())
        ].copy()
        
        self.logger.info(f"Extracted {len(df)} attendance records from {year_range[0]}-{year_range[1]}")
        return df
    
    def extract_bed_capacity_data(
        self, 
        year_range: Tuple[int, int] = (2009, 2020)
    ) -> pd.DataFrame:
        """
        Extract hospital bed capacity data
        
        Args:
            year_range: Tuple of (start_year, end_year)
            
        Returns:
            DataFrame with bed capacity data
        """
        table_name = "number-of-hospital-beds"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        self.logger.info(f"Extracting bed capacity data from {file_path}")
        df = pd.read_csv(file_path)
        
        # Apply filters
        df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1]) &
            (df['beds_no'] > 0)
        ].copy()
        
        self.logger.info(f"Extracted {len(df)} bed capacity records from {year_range[0]}-{year_range[1]}")
        return df
    
    def extract_clinic_registry(self) -> pd.DataFrame:
        """
        Extract clinic registry data
        
        Returns:
            DataFrame with clinic registry data
        """
        table_name = "facilities-in-the-registry-of-medical-clinics-and-dental-clinics"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        self.logger.info(f"Extracting clinic registry from {file_path}")
        df = pd.read_csv(file_path)
        
        self.logger.info(f"Extracted {len(df)} clinic records")
        return df
    
    def validate_extracted_data(
        self, 
        df: pd.DataFrame, 
        required_columns: List[str]
    ) -> bool:
        """
        Validate that extracted data meets requirements
        
        Args:
            df: DataFrame to validate
            required_columns: List of required column names
            
        Returns:
            True if valid, raises exception otherwise
        """
        # Check for missing columns
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            self.logger.error(f"Missing required columns: {missing_cols}")
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Check for empty dataframe
        if len(df) == 0:
            self.logger.error("Extracted dataframe is empty")
            raise ValueError("Extracted dataframe is empty")
        
        self.logger.info(f"Validation passed: {len(df)} records, {len(df.columns)} columns")
        return True
    
    def extract_all(
        self, 
        year_range: Tuple[int, int] = (2006, 2020)
    ) -> Dict[str, pd.DataFrame]:
        """
        Extract all required tables
        
        Args:
            year_range: Tuple of (start_year, end_year)
            
        Returns:
            Dictionary with all extracted DataFrames
        """
        # Download dataset if not already done
        if not self.dataset_path:
            self.download_dataset()
        
        self.logger.info("Extracting all required tables...")
        
        tables = {
            'attendance_by_hospitals': self.extract_attendance_data(year_range),
            'bed_capacity': self.extract_bed_capacity_data(year_range),
            'clinic_registry': self.extract_clinic_registry()
        }
        
        # Validate each table
        self.validate_extracted_data(
            tables['attendance_by_hospitals'],
            ['year', 'hospital', 'attendances_no']
        )
        self.validate_extracted_data(
            tables['bed_capacity'],
            ['year', 'hospital', 'beds_no']
        )
        
        self.logger.info(f"Successfully extracted {len(tables)} tables")
        return tables
    
    def save_extracted_data(
        self, 
        tables: Dict[str, pd.DataFrame], 
        output_dir: Path,
        file_format: str = 'csv'
    ) -> Dict[str, Path]:
        """
        Save extracted data to disk
        
        Args:
            tables: Dictionary of DataFrames to save
            output_dir: Output directory path
            file_format: Output format ('csv', 'parquet', 'excel')
            
        Returns:
            Dictionary mapping table names to file paths
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        saved_files = {}
        
        for table_name, df in tables.items():
            if file_format == 'csv':
                file_path = output_dir / f"{table_name}.csv"
                df.to_csv(file_path, index=False)
            elif file_format == 'parquet':
                file_path = output_dir / f"{table_name}.parquet"
                df.to_parquet(file_path, index=False)
            elif file_format == 'excel':
                file_path = output_dir / f"{table_name}.xlsx"
                df.to_excel(file_path, index=False)
            else:
                raise ValueError(f"Unsupported file format: {file_format}")
            
            saved_files[table_name] = file_path
            self.logger.info(f"Saved {table_name} to {file_path}")
        
        return saved_files
