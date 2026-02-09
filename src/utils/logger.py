"""
Logging Setup Utility

This module provides standardized logging configuration for the project.
"""

import logging
import logging.config
from pathlib import Path

import yaml


def setup_logging(
    default_path: str = "config/logging.yml",
    default_level: int = logging.INFO,
    env_key: str = "LOG_CFG"
) -> None:
    """
    Setup logging configuration.
    
    Args:
        default_path: Path to logging configuration file
        default_level: Default logging level if config file not found
        env_key: Environment variable name for config file path override
    """
    import os
    
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    
    config_path = Path(path)
    
    if config_path.exists():
        with open(config_path, "rt") as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
        logging.warning(f"Logging config file not found: {config_path}. Using basic config.")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Name for the logger (typically __name__)
    
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
