"""
Logging Configuration for MOH Data Extraction System
Version: 1.0
Created: 2026-01-26

Configures logging with:
- Multiple log files (extraction, errors, audit)
- Log rotation
- Structured logging
- Performance monitoring
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from datetime import datetime
import json


class StructuredFormatter(logging.Formatter):
    """
    Custom formatter that outputs structured JSON logs.
    """
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_data.update(record.extra_fields)
        
        return json.dumps(log_data)


def setup_logging(
    log_level: str = 'INFO',
    log_dir: str = 'logs',
    enable_console: bool = True,
    enable_file: bool = True,
    enable_structured: bool = False
):
    """
    Configure logging for the data extraction system.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files
        enable_console: Enable console logging
        enable_file: Enable file logging
        enable_structured: Use structured JSON logging
    """
    # Create logs directory
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers = []
    
    # Define formatters
    if enable_structured:
        formatter = StructuredFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    if enable_file:
        # Main extraction log (all levels)
        extraction_log = log_path / 'extraction.log'
        extraction_handler = logging.handlers.RotatingFileHandler(
            extraction_log,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=10
        )
        extraction_handler.setLevel(logging.INFO)
        extraction_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(extraction_handler)
        
        # Error log (errors and critical only)
        error_log = log_path / 'errors.log'
        error_handler = logging.handlers.RotatingFileHandler(
            error_log,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=10
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(error_handler)
        
        # Audit log (structured logging for critical operations)
        audit_log = log_path / 'audit.log'
        audit_handler = logging.handlers.RotatingFileHandler(
            audit_log,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=20
        )
        audit_handler.setLevel(logging.INFO)
        audit_handler.setFormatter(StructuredFormatter())
        
        # Create audit logger
        audit_logger = logging.getLogger('audit')
        audit_logger.addHandler(audit_handler)
        audit_logger.propagate = False
    
    logging.info(f"Logging configured: level={log_level}, dir={log_dir}")


def get_audit_logger():
    """Get the audit logger for structured logging."""
    return logging.getLogger('audit')


def log_extraction_start(source: str, parameters: dict):
    """Log the start of a data extraction."""
    audit_logger = get_audit_logger()
    audit_logger.info(
        'extraction_start',
        extra={
            'extra_fields': {
                'event': 'extraction_start',
                'source': source,
                'parameters': parameters
            }
        }
    )


def log_extraction_complete(source: str, row_count: int, duration: float):
    """Log successful extraction completion."""
    audit_logger = get_audit_logger()
    audit_logger.info(
        'extraction_complete',
        extra={
            'extra_fields': {
                'event': 'extraction_complete',
                'source': source,
                'row_count': row_count,
                'duration_seconds': duration
            }
        }
    )


def log_extraction_error(source: str, error: str, parameters: dict):
    """Log extraction error."""
    audit_logger = get_audit_logger()
    audit_logger.error(
        'extraction_error',
        extra={
            'extra_fields': {
                'event': 'extraction_error',
                'source': source,
                'error': error,
                'parameters': parameters
            }
        }
    )


def log_validation_result(source: str, passed: int, failed: int, critical_failure: bool):
    """Log validation results."""
    audit_logger = get_audit_logger()
    audit_logger.info(
        'validation_result',
        extra={
            'extra_fields': {
                'event': 'validation_result',
                'source': source,
                'checks_passed': passed,
                'checks_failed': failed,
                'critical_failure': critical_failure
            }
        }
    )
