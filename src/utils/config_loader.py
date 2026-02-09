"""
Configuration Loader Utility

This module provides functions to load and parse configuration files
from the config/ directory.
"""

import os
from pathlib import Path
from typing import Any, Dict

import yaml


def load_config(config_name: str, config_dir: str = "config") -> Dict[str, Any]:
    """
    Load a YAML configuration file.
    
    Args:
        config_name: Name of the config file (without .yml extension)
        config_dir: Directory containing config files (default: "config")
    
    Returns:
        Dictionary containing configuration parameters
    
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is malformed
    """
    project_root = Path(__file__).parent.parent.parent
    config_path = project_root / config_dir / f"{config_name}.yml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    return config


def get_data_paths() -> Dict[str, Path]:
    """
    Get standardized data directory paths.
    
    Returns:
        Dictionary with keys: raw, external, interim, processed, schemas
    """
    project_root = Path(__file__).parent.parent.parent
    
    return {
        "raw": project_root / "data" / "1_raw",
        "external": project_root / "data" / "2_external",
        "interim": project_root / "data" / "3_interim",
        "processed": project_root / "data" / "4_processed",
        "schemas": project_root / "data" / "schemas",
    }


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path to project root
    """
    return Path(__file__).parent.parent.parent
