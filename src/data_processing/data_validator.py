"""
Data Validator Module for MOH Polyclinic Data
Version: 1.0
Created: 2026-01-26

This module performs data quality checks including:
- Row count validation
- Null value detection
- Date range validation
- Duplicate detection
- Referential integrity checks
- Data type validation
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import yaml


logger = logging.getLogger(__name__)


class ValidationResult:
    """Container for validation results."""
    
    def __init__(self, check_name: str, passed: bool, message: str, details: Optional[Dict] = None):
        self.check_name = check_name
        self.passed = passed
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'check_name': self.check_name,
            'passed': self.passed,
            'message': self.message,
            'details': self.details,
            'timestamp': self.timestamp.isoformat()
        }
    
    def __repr__(self) -> str:
        status = "PASSED" if self.passed else "FAILED"
        return f"[{status}] {self.check_name}: {self.message}"


class DataValidator:
    """
    Validates extracted data against quality rules.
    """
    
    def __init__(self, config_path: str = 'config/database.yml'):
        """
        Initialize data validator.
        
        Args:
            config_path: Path to database configuration file
        """
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.quality_config = config.get('quality_checks', {})
        self.data_sources = config.get('data_sources', {})
        self.validation_results = []
    
    def validate_all(
        self,
        data: pd.DataFrame,
        source: str,
        reference_data: Optional[Dict[str, pd.DataFrame]] = None
    ) -> List[ValidationResult]:
        """
        Run all validation checks on a dataset.
        
        Args:
            data: DataFrame to validate
            source: Data source name
            reference_data: Dictionary of reference DataFrames for integrity checks
            
        Returns:
            List of ValidationResult objects
        """
        self.validation_results = []
        
        logger.info(f"Starting validation for source: {source}")
        
        # Row count validation
        if self.quality_config.get('row_count', {}).get('enabled', True):
            self.validation_results.append(self._validate_row_count(data))
        
        # Null value checks
        if self.quality_config.get('null_checks', {}).get('critical_columns'):
            self.validation_results.append(self._validate_null_values(data, source))
        
        # Date range validation
        if self.quality_config.get('date_validation', {}).get('enabled', True):
            self.validation_results.append(self._validate_date_ranges(data, source))
        
        # Duplicate detection
        if self.quality_config.get('duplicate_checks', {}).get('enabled', True):
            self.validation_results.append(self._validate_duplicates(data, source))
        
        # Data type validation
        self.validation_results.append(self._validate_data_types(data, source))
        
        # Value range validation
        self.validation_results.append(self._validate_value_ranges(data, source))
        
        # Referential integrity (if reference data provided)
        if reference_data and self.quality_config.get('referential_integrity', {}).get('enabled', True):
            self.validation_results.extend(
                self._validate_referential_integrity(data, source, reference_data)
            )
        
        # Log summary
        passed = sum(1 for r in self.validation_results if r.passed)
        total = len(self.validation_results)
        logger.info(f"Validation complete: {passed}/{total} checks passed")
        
        return self.validation_results
    
    def _validate_row_count(self, data: pd.DataFrame) -> ValidationResult:
        """Validate minimum row count."""
        min_rows = self.quality_config['row_count'].get('min_rows', 100)
        row_count = len(data)
        
        if row_count >= min_rows:
            return ValidationResult(
                'row_count',
                True,
                f"Row count {row_count} meets minimum threshold {min_rows}",
                {'row_count': row_count, 'min_required': min_rows}
            )
        else:
            return ValidationResult(
                'row_count',
                False,
                f"Row count {row_count} below minimum threshold {min_rows}",
                {'row_count': row_count, 'min_required': min_rows}
            )
    
    def _validate_null_values(self, data: pd.DataFrame, source: str) -> ValidationResult:
        """Validate null values in critical columns."""
        critical_cols = self.quality_config['null_checks'].get('critical_columns', [])
        max_null_pct = self.quality_config['null_checks'].get('max_null_percentage', 5)
        
        issues = []
        for col in critical_cols:
            if col in data.columns:
                null_count = data[col].isnull().sum()
                null_pct = (null_count / len(data)) * 100
                
                if null_pct > max_null_pct:
                    issues.append({
                        'column': col,
                        'null_count': int(null_count),
                        'null_percentage': round(null_pct, 2)
                    })
        
        if not issues:
            return ValidationResult(
                'null_values',
                True,
                f"All critical columns meet null value thresholds",
                {'critical_columns': critical_cols}
            )
        else:
            return ValidationResult(
                'null_values',
                False,
                f"Found {len(issues)} columns exceeding null value threshold",
                {'issues': issues, 'max_null_percentage': max_null_pct}
            )
    
    def _validate_date_ranges(self, data: pd.DataFrame, source: str) -> ValidationResult:
        """Validate date columns are within expected ranges."""
        date_config = self.quality_config.get('date_validation', {})
        min_date = pd.to_datetime(date_config.get('min_date', '2015-01-01'))
        max_date = pd.to_datetime('today') if date_config.get('max_date') == 'today' \
                   else pd.to_datetime(date_config.get('max_date', '2099-12-31'))
        
        # Find date columns
        date_columns = []
        source_config = self.data_sources.get(source, {})
        if 'date_column' in source_config:
            date_columns.append(source_config['date_column'])
        
        # Also check columns with 'date' in the name
        date_columns.extend([col for col in data.columns if 'date' in col.lower()])
        date_columns = list(set(date_columns))  # Remove duplicates
        
        issues = []
        for col in date_columns:
            if col in data.columns:
                try:
                    dates = pd.to_datetime(data[col], errors='coerce')
                    
                    # Check for invalid dates (NaT after conversion)
                    invalid_count = dates.isna().sum() - data[col].isna().sum()
                    if invalid_count > 0:
                        issues.append({
                            'column': col,
                            'issue': 'invalid_format',
                            'count': int(invalid_count)
                        })
                    
                    # Check for dates outside range
                    valid_dates = dates.dropna()
                    if len(valid_dates) > 0:
                        too_early = (valid_dates < min_date).sum()
                        too_late = (valid_dates > max_date).sum()
                        
                        if too_early > 0:
                            issues.append({
                                'column': col,
                                'issue': 'before_min_date',
                                'count': int(too_early),
                                'min_date': min_date.strftime('%Y-%m-%d')
                            })
                        
                        if too_late > 0:
                            issues.append({
                                'column': col,
                                'issue': 'after_max_date',
                                'count': int(too_late),
                                'max_date': max_date.strftime('%Y-%m-%d')
                            })
                except Exception as e:
                    issues.append({
                        'column': col,
                        'issue': 'validation_error',
                        'error': str(e)
                    })
        
        if not issues:
            return ValidationResult(
                'date_ranges',
                True,
                f"All date columns within valid ranges",
                {'validated_columns': date_columns}
            )
        else:
            return ValidationResult(
                'date_ranges',
                False,
                f"Found {len(issues)} date range issues",
                {'issues': issues}
            )
    
    def _validate_duplicates(self, data: pd.DataFrame, source: str) -> ValidationResult:
        """Check for duplicate records."""
        source_config = self.data_sources.get(source, {})
        key_cols = self.quality_config['duplicate_checks'].get('key_columns', [])
        
        # Try to use primary key if available
        if 'primary_key' in source_config:
            pk = source_config['primary_key']
            if pk in data.columns:
                key_cols = [pk]
        
        if not key_cols:
            return ValidationResult(
                'duplicates',
                True,
                "No key columns defined for duplicate checking",
                {'checked': False}
            )
        
        # Filter to only existing columns
        existing_keys = [col for col in key_cols if col in data.columns]
        if not existing_keys:
            return ValidationResult(
                'duplicates',
                True,
                f"Key columns {key_cols} not found in data",
                {'checked': False}
            )
        
        # Check for duplicates
        duplicates = data[data.duplicated(subset=existing_keys, keep=False)]
        duplicate_count = len(duplicates)
        
        if duplicate_count == 0:
            return ValidationResult(
                'duplicates',
                True,
                f"No duplicates found on keys: {existing_keys}",
                {'key_columns': existing_keys, 'duplicate_count': 0}
            )
        else:
            return ValidationResult(
                'duplicates',
                False,
                f"Found {duplicate_count} duplicate records",
                {
                    'key_columns': existing_keys,
                    'duplicate_count': duplicate_count,
                    'sample_duplicates': duplicates.head(5).to_dict('records')
                }
            )
    
    def _validate_data_types(self, data: pd.DataFrame, source: str) -> ValidationResult:
        """Validate data types of columns."""
        issues = []
        
        # Check for columns that should be numeric but aren't
        numeric_indicators = ['id', 'count', 'amount', 'cost', 'charge', 'minutes', 'duration']
        for col in data.columns:
            col_lower = col.lower()
            if any(indicator in col_lower for indicator in numeric_indicators):
                if not pd.api.types.is_numeric_dtype(data[col]):
                    non_numeric = data[~data[col].apply(lambda x: pd.isna(x) or 
                                                        isinstance(x, (int, float, np.number)))]
                    if len(non_numeric) > 0:
                        issues.append({
                            'column': col,
                            'expected_type': 'numeric',
                            'actual_type': str(data[col].dtype),
                            'non_numeric_count': len(non_numeric)
                        })
        
        if not issues:
            return ValidationResult(
                'data_types',
                True,
                "All columns have expected data types",
                {}
            )
        else:
            return ValidationResult(
                'data_types',
                False,
                f"Found {len(issues)} data type issues",
                {'issues': issues}
            )
    
    def _validate_value_ranges(self, data: pd.DataFrame, source: str) -> ValidationResult:
        """Validate that numeric values are within reasonable ranges."""
        issues = []
        
        # Check for negative values in columns that shouldn't have them
        non_negative_cols = [col for col in data.columns 
                           if any(x in col.lower() for x in ['count', 'duration', 'minutes', 'age'])]
        
        for col in non_negative_cols:
            if col in data.columns and pd.api.types.is_numeric_dtype(data[col]):
                negative_count = (data[col] < 0).sum()
                if negative_count > 0:
                    issues.append({
                        'column': col,
                        'issue': 'negative_values',
                        'count': int(negative_count),
                        'min_value': float(data[col].min())
                    })
        
        if not issues:
            return ValidationResult(
                'value_ranges',
                True,
                "All numeric values within expected ranges",
                {}
            )
        else:
            return ValidationResult(
                'value_ranges',
                False,
                f"Found {len(issues)} value range issues",
                {'issues': issues}
            )
    
    def _validate_referential_integrity(
        self,
        data: pd.DataFrame,
        source: str,
        reference_data: Dict[str, pd.DataFrame]
    ) -> List[ValidationResult]:
        """Validate foreign key relationships."""
        results = []
        relationships = self.quality_config['referential_integrity'].get('relationships', [])
        
        for rel in relationships:
            if rel['child'] == source:
                parent_source = rel['parent']
                fk_column = rel['foreign_key']
                
                if parent_source not in reference_data:
                    results.append(ValidationResult(
                        f'referential_integrity_{parent_source}',
                        True,
                        f"Reference data for {parent_source} not provided",
                        {'checked': False}
                    ))
                    continue
                
                if fk_column not in data.columns:
                    results.append(ValidationResult(
                        f'referential_integrity_{parent_source}',
                        True,
                        f"Foreign key column {fk_column} not found",
                        {'checked': False}
                    ))
                    continue
                
                parent_df = reference_data[parent_source]
                parent_config = self.data_sources.get(parent_source, {})
                pk_column = parent_config.get('primary_key', fk_column)
                
                if pk_column not in parent_df.columns:
                    results.append(ValidationResult(
                        f'referential_integrity_{parent_source}',
                        False,
                        f"Primary key column {pk_column} not found in parent table",
                        {'checked': False}
                    ))
                    continue
                
                # Check for orphaned records
                valid_keys = set(parent_df[pk_column].dropna())
                child_keys = set(data[fk_column].dropna())
                orphaned_keys = child_keys - valid_keys
                orphaned_count = len(orphaned_keys)
                
                if orphaned_count == 0:
                    results.append(ValidationResult(
                        f'referential_integrity_{parent_source}',
                        True,
                        f"All {fk_column} values have valid references in {parent_source}",
                        {
                            'parent': parent_source,
                            'foreign_key': fk_column,
                            'orphaned_count': 0
                        }
                    ))
                else:
                    results.append(ValidationResult(
                        f'referential_integrity_{parent_source}',
                        False,
                        f"Found {orphaned_count} orphaned records",
                        {
                            'parent': parent_source,
                            'foreign_key': fk_column,
                            'orphaned_count': orphaned_count,
                            'sample_orphaned_keys': list(orphaned_keys)[:10]
                        }
                    ))
        
        return results if results else [ValidationResult(
            'referential_integrity',
            True,
            "No referential integrity rules configured for this source",
            {}
        )]
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get summary of all validation results."""
        total_checks = len(self.validation_results)
        passed_checks = sum(1 for r in self.validation_results if r.passed)
        failed_checks = total_checks - passed_checks
        
        return {
            'total_checks': total_checks,
            'passed': passed_checks,
            'failed': failed_checks,
            'success_rate': round((passed_checks / total_checks * 100), 2) if total_checks > 0 else 0,
            'results': [r.to_dict() for r in self.validation_results]
        }
    
    def has_critical_failures(self) -> bool:
        """Check if there are any critical validation failures."""
        critical_checks = ['row_count', 'null_values', 'referential_integrity']
        for result in self.validation_results:
            if not result.passed and any(c in result.check_name for c in critical_checks):
                return True
        return False
