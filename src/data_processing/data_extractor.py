"""
Data Extractor Module for MOH Polyclinic Data
Version: 1.0
Created: 2026-01-26

This module handles data extraction from databases with:
- Incremental and full extraction modes
- Batch processing
- Retry logic
- Progress tracking
- Query template management
"""

import os
import logging
import json
import yaml
import pandas as pd
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from pathlib import Path
import time
from functools import wraps

from .db_connector import DatabaseConnector


logger = logging.getLogger(__name__)


def retry_on_failure(max_retries: int = 3, delay: int = 5):
    """Decorator to retry function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Attempt {attempt + 1} failed: {str(e)}. "
                            f"Retrying in {delay} seconds..."
                        )
                        time.sleep(delay)
                    else:
                        logger.error(f"All {max_retries} attempts failed")
                        raise
        return wrapper
    return decorator


class DataExtractor:
    """
    Handles data extraction from MOH databases.
    Supports incremental extraction, batch processing, and multiple output formats.
    """
    
    def __init__(
        self,
        db_config_path: str = 'config/database.yml',
        query_config_path: str = 'config/queries.yml'
    ):
        """
        Initialize data extractor.
        
        Args:
            db_config_path: Path to database configuration
            query_config_path: Path to query templates configuration
        """
        self.db_connector = DatabaseConnector(db_config_path)
        self.db_config = self.db_connector.config
        self.queries = self._load_queries(query_config_path)
        self.extraction_config = self.db_config['extraction']
        self.data_sources = self.db_config['data_sources']
        self.checkpoint_file = self.extraction_config['incremental']['checkpoint_file']
        self.checkpoints = self._load_checkpoints()
    
    def _load_queries(self, query_config_path: str) -> Dict[str, Any]:
        """Load SQL query templates from YAML file."""
        with open(query_config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _load_checkpoints(self) -> Dict[str, Any]:
        """Load extraction checkpoints from file."""
        checkpoint_path = Path(self.checkpoint_file)
        if checkpoint_path.exists():
            with open(checkpoint_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_checkpoint(self, source: str, checkpoint_date: datetime):
        """Save extraction checkpoint."""
        self.checkpoints[source] = checkpoint_date.isoformat()
        
        # Create directory if it doesn't exist
        checkpoint_path = Path(self.checkpoint_file)
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(checkpoint_path, 'w') as f:
            json.dump(self.checkpoints, f, indent=2)
        
        logger.info(f"Checkpoint saved for {source}: {checkpoint_date}")
    
    def get_last_extraction_date(self, source: str) -> Optional[datetime]:
        """Get the last successful extraction date for a data source."""
        if source in self.checkpoints:
            return datetime.fromisoformat(self.checkpoints[source])
        return None
    
    @retry_on_failure(max_retries=3, delay=5)
    def extract_data(
        self,
        source: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        incremental: Optional[bool] = None,
        db_name: str = 'polyclinic_db'
    ) -> pd.DataFrame:
        """
        Extract data from a specified source.
        
        Args:
            source: Data source name (e.g., 'attendances', 'patients')
            start_date: Start date for extraction (YYYY-MM-DD)
            end_date: End date for extraction (YYYY-MM-DD)
            incremental: Whether to do incremental extraction
            db_name: Database name
            
        Returns:
            DataFrame with extracted data
        """
        logger.info(f"Starting extraction for source: {source}")
        
        # Get source configuration
        source_config = self.data_sources.get(source)
        if not source_config:
            raise ValueError(f"Unknown data source: {source}")
        
        # Determine if incremental extraction should be used
        if incremental is None:
            incremental = source_config.get('incremental', False) and \
                         self.extraction_config['incremental']['enabled']
        
        # Get query template
        query_template = self.queries['queries'].get(source)
        if not query_template:
            raise ValueError(f"No query template found for source: {source}")
        
        # Determine date range
        if incremental and not start_date:
            last_extraction = self.get_last_extraction_date(source)
            if last_extraction:
                start_date = last_extraction.strftime('%Y-%m-%d')
            else:
                # Default to 30 days ago for first incremental run
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Select appropriate query
        if incremental and 'incremental_query' in query_template:
            query = query_template['incremental_query']
        elif 'full_query' in query_template:
            query = query_template['full_query']
        else:
            query = query_template.get('query', '')
        
        if not query:
            raise ValueError(f"No valid query found for source: {source}")
        
        # Extract data in batches
        all_data = []
        batch_size = self.extraction_config['batch_size']
        batch_offset = 0
        
        while True:
            # Format query with parameters
            formatted_query = query.format(
                start_date=start_date,
                end_date=end_date,
                batch_size=batch_size,
                batch_offset=batch_offset
            )
            
            logger.debug(f"Extracting batch at offset {batch_offset}")
            
            # Execute query
            with self.db_connector.get_connection(db_name) as conn:
                df_batch = pd.read_sql(formatted_query, conn)
            
            if df_batch.empty:
                logger.info(f"No more data to extract for {source}")
                break
            
            all_data.append(df_batch)
            batch_offset += batch_size
            
            logger.info(
                f"Extracted {len(df_batch)} rows "
                f"(total: {sum(len(df) for df in all_data)} rows)"
            )
            
            # Break if less than batch size returned (last batch)
            if len(df_batch) < batch_size:
                break
        
        # Combine all batches
        if all_data:
            df_final = pd.concat(all_data, ignore_index=True)
            logger.info(
                f"Extraction complete for {source}: "
                f"{len(df_final)} total rows"
            )
            
            # Save checkpoint
            if incremental:
                self._save_checkpoint(source, datetime.now())
            
            return df_final
        else:
            logger.warning(f"No data extracted for {source}")
            return pd.DataFrame()
    
    def extract_reference_data(
        self,
        source: str,
        db_name: str = 'polyclinic_db'
    ) -> pd.DataFrame:
        """
        Extract reference/master data (non-incremental).
        
        Args:
            source: Reference data source name
            db_name: Database name
            
        Returns:
            DataFrame with reference data
        """
        logger.info(f"Extracting reference data: {source}")
        
        query_template = self.queries['queries'].get(source)
        if not query_template:
            raise ValueError(f"No query template found for source: {source}")
        
        query = query_template.get('query', '')
        if not query:
            raise ValueError(f"No query found for reference source: {source}")
        
        with self.db_connector.get_connection(db_name) as conn:
            df = pd.read_sql(query, conn)
        
        logger.info(f"Reference data extraction complete: {len(df)} rows")
        return df
    
    def extract_all_sources(
        self,
        sources: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        incremental: bool = True
    ) -> Dict[str, pd.DataFrame]:
        """
        Extract data from multiple sources.
        
        Args:
            sources: List of source names (None = all sources)
            start_date: Start date for extraction
            end_date: End date for extraction
            incremental: Whether to do incremental extraction
            
        Returns:
            Dictionary mapping source names to DataFrames
        """
        if sources is None:
            sources = list(self.data_sources.keys())
        
        results = {}
        for source in sources:
            try:
                source_config = self.data_sources[source]
                if source_config.get('incremental', False):
                    df = self.extract_data(
                        source,
                        start_date=start_date,
                        end_date=end_date,
                        incremental=incremental
                    )
                else:
                    df = self.extract_reference_data(source)
                
                results[source] = df
            except Exception as e:
                logger.error(f"Failed to extract {source}: {str(e)}")
                results[source] = pd.DataFrame()  # Empty DataFrame on failure
        
        return results
    
    def save_extracted_data(
        self,
        data: pd.DataFrame,
        source: str,
        output_format: str = 'parquet',
        output_path: Optional[str] = None
    ) -> str:
        """
        Save extracted data to file.
        
        Args:
            data: DataFrame to save
            source: Data source name
            output_format: Output format ('parquet', 'csv', 'excel')
            output_path: Custom output path (optional)
            
        Returns:
            Path to saved file
        """
        if data.empty:
            logger.warning(f"No data to save for {source}")
            return ""
        
        # Determine output path
        if not output_path:
            output_config = self.db_config['output']
            base_path = output_config['paths']['raw']
            
            # Create filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = output_config['naming_pattern'].format(
                source=source,
                date=datetime.now().strftime('%Y%m%d'),
                timestamp=timestamp,
                format=output_format
            )
            
            output_path = os.path.join(base_path, filename)
        
        # Create directory if needed
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save based on format
        compression = self.db_config['output'].get('compression', 'gzip')
        
        if output_format == 'parquet':
            data.to_parquet(output_path, compression=compression, index=False)
        elif output_format == 'csv':
            data.to_csv(output_path, compression=compression, index=False)
        elif output_format == 'excel':
            data.to_excel(output_path, index=False)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
        
        logger.info(f"Data saved to: {output_path}")
        return output_path
    
    def get_extraction_stats(self, source: str) -> Dict[str, Any]:
        """
        Get extraction statistics for a data source.
        
        Args:
            source: Data source name
            
        Returns:
            Dictionary with extraction statistics
        """
        last_extraction = self.get_last_extraction_date(source)
        
        return {
            'source': source,
            'last_extraction_date': last_extraction.isoformat() if last_extraction else None,
            'incremental_enabled': self.data_sources[source].get('incremental', False),
            'table': self.data_sources[source].get('table', 'N/A')
        }
