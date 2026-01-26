"""
ETL Pipeline Orchestrator for MOH Polyclinic Data
Version: 1.0
Created: 2026-01-26

This module orchestrates the complete ETL pipeline:
- Extract data from multiple sources
- Validate data quality
- Transform and clean data
- Load data to target locations
- Generate reports and notifications
"""

import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import pandas as pd

from .db_connector import DatabaseConnector
from .data_extractor import DataExtractor
from .data_validator import DataValidator


logger = logging.getLogger(__name__)


class ETLPipeline:
    """
    Orchestrates the complete ETL workflow for MOH polyclinic data.
    """
    
    def __init__(
        self,
        db_config_path: str = 'config/database.yml',
        query_config_path: str = 'config/queries.yml'
    ):
        """
        Initialize ETL pipeline.
        
        Args:
            db_config_path: Path to database configuration
            query_config_path: Path to query templates
        """
        self.extractor = DataExtractor(db_config_path, query_config_path)
        self.validator = DataValidator(db_config_path)
        self.db_config = self.extractor.db_config
        
        self.run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.execution_log = []
        self.extracted_data = {}
        self.validation_results = {}
    
    def run_extraction(
        self,
        sources: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        incremental: bool = True,
        save_raw: bool = True
    ) -> Dict[str, pd.DataFrame]:
        """
        Run data extraction phase.
        
        Args:
            sources: List of sources to extract (None = all)
            start_date: Start date for extraction
            end_date: End date for extraction
            incremental: Whether to do incremental extraction
            save_raw: Whether to save raw extracted data
            
        Returns:
            Dictionary of extracted DataFrames
        """
        logger.info(f"=== Starting Extraction Phase (Run ID: {self.run_id}) ===")
        
        start_time = datetime.now()
        
        try:
            # Extract all sources
            self.extracted_data = self.extractor.extract_all_sources(
                sources=sources,
                start_date=start_date,
                end_date=end_date,
                incremental=incremental
            )
            
            # Log extraction summary
            total_rows = sum(len(df) for df in self.extracted_data.values())
            logger.info(
                f"Extraction complete: {len(self.extracted_data)} sources, "
                f"{total_rows:,} total rows"
            )
            
            # Save raw data if requested
            if save_raw:
                for source, df in self.extracted_data.items():
                    if not df.empty:
                        output_formats = self.db_config['output'].get('formats', ['parquet'])
                        for fmt in output_formats:
                            self.extractor.save_extracted_data(df, source, fmt)
            
            # Log execution
            self._log_execution(
                phase='extraction',
                status='success',
                duration=(datetime.now() - start_time).total_seconds(),
                details={
                    'sources': list(self.extracted_data.keys()),
                    'total_rows': total_rows,
                    'incremental': incremental
                }
            )
            
            return self.extracted_data
            
        except Exception as e:
            logger.error(f"Extraction failed: {str(e)}")
            self._log_execution(
                phase='extraction',
                status='failed',
                duration=(datetime.now() - start_time).total_seconds(),
                error=str(e)
            )
            raise
    
    def run_validation(
        self,
        data: Optional[Dict[str, pd.DataFrame]] = None,
        stop_on_failure: bool = False
    ) -> Dict[str, Dict[str, Any]]:
        """
        Run data validation phase.
        
        Args:
            data: Dictionary of DataFrames to validate (uses extracted_data if None)
            stop_on_failure: Whether to stop pipeline on validation failure
            
        Returns:
            Dictionary of validation results per source
        """
        logger.info("=== Starting Validation Phase ===")
        
        start_time = datetime.now()
        
        if data is None:
            data = self.extracted_data
        
        if not data:
            logger.warning("No data available for validation")
            return {}
        
        try:
            # Collect reference data for integrity checks
            reference_data = {}
            for source, df in data.items():
                source_config = self.db_config['data_sources'].get(source, {})
                if not source_config.get('incremental', False):
                    reference_data[source] = df
            
            # Validate each source
            for source, df in data.items():
                if df.empty:
                    logger.info(f"Skipping validation for empty source: {source}")
                    continue
                
                logger.info(f"Validating {source}...")
                results = self.validator.validate_all(df, source, reference_data)
                
                summary = self.validator.get_validation_summary()
                self.validation_results[source] = summary
                
                # Log validation results
                logger.info(
                    f"{source}: {summary['passed']}/{summary['total_checks']} "
                    f"checks passed ({summary['success_rate']:.1f}%)"
                )
                
                # Check for critical failures
                if stop_on_failure and self.validator.has_critical_failures():
                    raise ValueError(
                        f"Critical validation failures detected for {source}. "
                        "Pipeline stopped."
                    )
            
            # Overall summary
            total_checks = sum(r['total_checks'] for r in self.validation_results.values())
            total_passed = sum(r['passed'] for r in self.validation_results.values())
            
            logger.info(
                f"Validation complete: {total_passed}/{total_checks} checks passed overall"
            )
            
            # Log execution
            self._log_execution(
                phase='validation',
                status='success',
                duration=(datetime.now() - start_time).total_seconds(),
                details={
                    'sources_validated': len(self.validation_results),
                    'total_checks': total_checks,
                    'total_passed': total_passed
                }
            )
            
            return self.validation_results
            
        except Exception as e:
            logger.error(f"Validation failed: {str(e)}")
            self._log_execution(
                phase='validation',
                status='failed',
                duration=(datetime.now() - start_time).total_seconds(),
                error=str(e)
            )
            raise
    
    def run_transformation(
        self,
        data: Optional[Dict[str, pd.DataFrame]] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Run data transformation phase.
        
        Args:
            data: Dictionary of DataFrames to transform
            
        Returns:
            Dictionary of transformed DataFrames
        """
        logger.info("=== Starting Transformation Phase ===")
        
        start_time = datetime.now()
        
        if data is None:
            data = self.extracted_data
        
        transformed_data = {}
        
        try:
            for source, df in data.items():
                if df.empty:
                    logger.info(f"Skipping transformation for empty source: {source}")
                    transformed_data[source] = df
                    continue
                
                logger.info(f"Transforming {source}...")
                
                # Basic transformations
                df_transformed = df.copy()
                
                # 1. Remove exact duplicates
                initial_rows = len(df_transformed)
                df_transformed = df_transformed.drop_duplicates()
                dropped = initial_rows - len(df_transformed)
                if dropped > 0:
                    logger.info(f"Removed {dropped} duplicate rows from {source}")
                
                # 2. Convert date columns
                date_cols = [col for col in df_transformed.columns if 'date' in col.lower()]
                for col in date_cols:
                    try:
                        df_transformed[col] = pd.to_datetime(df_transformed[col], errors='coerce')
                    except Exception as e:
                        logger.warning(f"Could not convert {col} to datetime: {str(e)}")
                
                # 3. Standardize column names
                df_transformed.columns = [col.lower().replace(' ', '_') 
                                         for col in df_transformed.columns]
                
                # 4. Add metadata columns
                df_transformed['extraction_date'] = datetime.now()
                df_transformed['run_id'] = self.run_id
                
                transformed_data[source] = df_transformed
                
                logger.info(
                    f"{source}: Transformed {len(df_transformed):,} rows, "
                    f"{len(df_transformed.columns)} columns"
                )
            
            # Log execution
            self._log_execution(
                phase='transformation',
                status='success',
                duration=(datetime.now() - start_time).total_seconds(),
                details={
                    'sources_transformed': len(transformed_data),
                    'total_rows': sum(len(df) for df in transformed_data.values())
                }
            )
            
            return transformed_data
            
        except Exception as e:
            logger.error(f"Transformation failed: {str(e)}")
            self._log_execution(
                phase='transformation',
                status='failed',
                duration=(datetime.now() - start_time).total_seconds(),
                error=str(e)
            )
            raise
    
    def run_load(
        self,
        data: Dict[str, pd.DataFrame],
        output_formats: Optional[List[str]] = None
    ) -> Dict[str, List[str]]:
        """
        Run data loading phase.
        
        Args:
            data: Dictionary of DataFrames to load
            output_formats: List of output formats ('parquet', 'csv', 'excel')
            
        Returns:
            Dictionary mapping sources to output file paths
        """
        logger.info("=== Starting Load Phase ===")
        
        start_time = datetime.now()
        output_paths = {}
        
        if output_formats is None:
            output_formats = self.db_config['output'].get('formats', ['parquet'])
        
        try:
            for source, df in data.items():
                if df.empty:
                    logger.info(f"Skipping load for empty source: {source}")
                    continue
                
                logger.info(f"Loading {source}...")
                
                paths = []
                for fmt in output_formats:
                    # Save to processed directory
                    base_path = self.db_config['output']['paths']['processed']
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    
                    filename = self.db_config['output']['naming_pattern'].format(
                        source=source,
                        date=datetime.now().strftime('%Y%m%d'),
                        timestamp=timestamp,
                        format=fmt
                    )
                    
                    output_path = Path(base_path) / filename
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Save based on format
                    if fmt == 'parquet':
                        df.to_parquet(output_path, compression='gzip', index=False)
                    elif fmt == 'csv':
                        df.to_csv(output_path, compression='gzip', index=False)
                    elif fmt == 'excel':
                        df.to_excel(output_path, index=False)
                    
                    paths.append(str(output_path))
                    logger.info(f"Saved to: {output_path}")
                
                output_paths[source] = paths
            
            # Log execution
            self._log_execution(
                phase='load',
                status='success',
                duration=(datetime.now() - start_time).total_seconds(),
                details={
                    'sources_loaded': len(output_paths),
                    'output_formats': output_formats,
                    'output_paths': output_paths
                }
            )
            
            return output_paths
            
        except Exception as e:
            logger.error(f"Load failed: {str(e)}")
            self._log_execution(
                phase='load',
                status='failed',
                duration=(datetime.now() - start_time).total_seconds(),
                error=str(e)
            )
            raise
    
    def run_full_pipeline(
        self,
        sources: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        incremental: bool = True,
        stop_on_validation_failure: bool = False
    ) -> Dict[str, Any]:
        """
        Run the complete ETL pipeline.
        
        Args:
            sources: List of sources to process
            start_date: Start date for extraction
            end_date: End date for extraction
            incremental: Whether to do incremental extraction
            stop_on_validation_failure: Stop if validation fails
            
        Returns:
            Dictionary with pipeline execution summary
        """
        pipeline_start = datetime.now()
        
        logger.info(f"\n{'='*70}")
        logger.info(f"ETL PIPELINE STARTED - Run ID: {self.run_id}")
        logger.info(f"{'='*70}\n")
        
        try:
            # Phase 1: Extract
            extracted_data = self.run_extraction(
                sources=sources,
                start_date=start_date,
                end_date=end_date,
                incremental=incremental,
                save_raw=True
            )
            
            # Phase 2: Validate
            validation_results = self.run_validation(
                data=extracted_data,
                stop_on_failure=stop_on_validation_failure
            )
            
            # Phase 3: Transform
            transformed_data = self.run_transformation(data=extracted_data)
            
            # Phase 4: Load
            output_paths = self.run_load(transformed_data)
            
            # Generate summary
            pipeline_duration = (datetime.now() - pipeline_start).total_seconds()
            
            summary = {
                'run_id': self.run_id,
                'start_time': pipeline_start.isoformat(),
                'end_time': datetime.now().isoformat(),
                'duration_seconds': pipeline_duration,
                'status': 'success',
                'sources_processed': len(extracted_data),
                'total_rows_extracted': sum(len(df) for df in extracted_data.values()),
                'total_rows_loaded': sum(len(df) for df in transformed_data.values()),
                'validation_summary': {
                    source: {
                        'passed': results['passed'],
                        'total': results['total_checks'],
                        'success_rate': results['success_rate']
                    }
                    for source, results in validation_results.items()
                },
                'output_paths': output_paths,
                'execution_log': self.execution_log
            }
            
            # Save summary
            self._save_pipeline_summary(summary)
            
            logger.info(f"\n{'='*70}")
            logger.info(f"ETL PIPELINE COMPLETED SUCCESSFULLY")
            logger.info(f"Duration: {pipeline_duration:.1f} seconds")
            logger.info(f"Rows processed: {summary['total_rows_loaded']:,}")
            logger.info(f"{'='*70}\n")
            
            return summary
            
        except Exception as e:
            pipeline_duration = (datetime.now() - pipeline_start).total_seconds()
            
            summary = {
                'run_id': self.run_id,
                'start_time': pipeline_start.isoformat(),
                'end_time': datetime.now().isoformat(),
                'duration_seconds': pipeline_duration,
                'status': 'failed',
                'error': str(e),
                'execution_log': self.execution_log
            }
            
            self._save_pipeline_summary(summary)
            
            logger.error(f"\n{'='*70}")
            logger.error(f"ETL PIPELINE FAILED")
            logger.error(f"Error: {str(e)}")
            logger.error(f"{'='*70}\n")
            
            raise
    
    def _log_execution(
        self,
        phase: str,
        status: str,
        duration: float,
        details: Optional[Dict] = None,
        error: Optional[str] = None
    ):
        """Log pipeline execution details."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'phase': phase,
            'status': status,
            'duration_seconds': round(duration, 2),
            'details': details or {},
            'error': error
        }
        self.execution_log.append(log_entry)
    
    def _save_pipeline_summary(self, summary: Dict[str, Any]):
        """Save pipeline execution summary."""
        # Save to results directory
        output_dir = Path('results/metrics')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"etl_summary_{self.run_id}.json"
        
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"Pipeline summary saved to: {output_file}")
