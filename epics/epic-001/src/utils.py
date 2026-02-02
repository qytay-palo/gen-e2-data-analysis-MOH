"""
Epic 001: Utility Module
Common utility functions for configuration, logging, and file management
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Optional, Union
import sys


def load_config(config_path: Union[str, Path]) -> Dict:
    """
    Load YAML configuration file
    
    Args:
        config_path: Path to YAML config file
        
    Returns:
        Dictionary with configuration
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        try:
            config = yaml.safe_load(f)
            return config
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing config file: {e}")


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        log_format: Custom log format string (optional)
        
    Returns:
        Configured logger instance
    """
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logger = logging.getLogger('epic-001')
    
    # Add file handler if log file specified
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(file_handler)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(console_handler)
    
    return logger


def validate_paths(config: Dict) -> bool:
    """
    Validate that required paths exist in configuration
    
    Args:
        config: Configuration dictionary
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If required paths are missing
    """
    required_paths = ['paths']
    
    for path_key in required_paths:
        if path_key not in config:
            raise ValueError(f"Missing required configuration key: {path_key}")
    
    return True


def create_output_directories(config: Dict, epic_root: Path):
    """
    Create all output directories specified in config
    
    Args:
        config: Configuration dictionary
        epic_root: Root path for epic directory
    """
    if 'paths' not in config:
        return
    
    paths = config['paths']
    
    for path_key, path_value in paths.items():
        full_path = epic_root / path_value
        full_path.mkdir(parents=True, exist_ok=True)


def format_number(num: float, decimals: int = 2) -> str:
    """
    Format number with thousands separator
    
    Args:
        num: Number to format
        decimals: Number of decimal places
        
    Returns:
        Formatted string
    """
    return f"{num:,.{decimals}f}"


def format_percentage(num: float, decimals: int = 1) -> str:
    """
    Format number as percentage
    
    Args:
        num: Number to format (e.g., 85.5 for 85.5%)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{num:.{decimals}f}%"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
        default: Value to return if division by zero
        
    Returns:
        Result of division or default value
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ZeroDivisionError):
        return default


def get_epic_root() -> Path:
    """
    Get the root directory of the epic
    
    Returns:
        Path to epic root directory
    """
    # Assume this file is in src/, so go up one level
    return Path(__file__).parent.parent


def get_project_root() -> Path:
    """
    Get the root directory of the project
    
    Returns:
        Path to project root directory
    """
    # Epic is at project_root/epics/epic-001, so go up two levels from epic root
    return get_epic_root().parent.parent


class ProgressTracker:
    """Track progress of multi-step operations"""
    
    def __init__(self, total_steps: int, logger: Optional[logging.Logger] = None):
        """
        Initialize progress tracker
        
        Args:
            total_steps: Total number of steps
            logger: Logger instance
        """
        self.total_steps = total_steps
        self.current_step = 0
        self.logger = logger or logging.getLogger(__name__)
    
    def update(self, step_name: str, increment: int = 1):
        """
        Update progress
        
        Args:
            step_name: Name of current step
            increment: Number of steps to increment
        """
        self.current_step += increment
        progress_pct = (self.current_step / self.total_steps) * 100
        self.logger.info(
            f"Progress: {self.current_step}/{self.total_steps} ({progress_pct:.1f}%) - {step_name}"
        )
    
    def complete(self):
        """Mark as complete"""
        self.current_step = self.total_steps
        self.logger.info(f"Progress: Complete (100%)")


class Timer:
    """Simple timer for measuring execution time"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize timer
        
        Args:
            logger: Logger instance
        """
        import time
        self.time = time
        self.start_time = None
        self.logger = logger or logging.getLogger(__name__)
    
    def start(self, message: str = "Starting timer"):
        """Start the timer"""
        self.start_time = self.time.time()
        self.logger.info(message)
    
    def stop(self, message: str = "Elapsed time"):
        """Stop the timer and log elapsed time"""
        if self.start_time is None:
            self.logger.warning("Timer was not started")
            return
        
        elapsed = self.time.time() - self.start_time
        self.logger.info(f"{message}: {elapsed:.2f} seconds")
        return elapsed
