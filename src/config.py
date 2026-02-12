"""Project configuration constants."""
import logging
from pathlib import Path
from typing import Any, Dict, Final

import yaml

# Configure logger
logger = logging.getLogger(__name__)

# Reproducibility
RANDOM_STATE: Final[int] = 42

# Data source configuration
DATASET_ID: Final[str] = "subhamjain/health-dataset-complete-singapore"
DATA_FILE: Final[str] = "weekly-infectious-disease-bulletin-cases/weekly-infectious-disease-bulletin-cases.csv"

# Expected data characteristics (for validation)
EXPECTED_RECORDS: Final[int] = 16066
EXPECTED_DISEASES: Final[int] = 45
EXPECTED_WEEKS: Final[int] = 470

# Data quality thresholds
OUTLIER_IQR_THRESHOLD: Final[float] = 1.5
OUTLIER_ZSCORE_THRESHOLD: Final[float] = 3.0

# Output paths
RAW_DATA_DIR: Final[str] = "data/1_raw/kaggle"
INTERIM_DATA_DIR: Final[str] = "data/3_interim"
PROCESSED_DATA_DIR: Final[str] = "data/4_processed"
RESULTS_TABLES_DIR: Final[str] = "results/tables"
RESULTS_FIGURES_DIR: Final[str] = "results/figures"

# Burden Metrics Constants (User Story 2)
BURDEN_METRICS_PATH: Final[str] = "data/4_processed/disease_burden_metrics.csv"
OUTBREAK_THRESHOLD_MULTIPLIER: Final[float] = 2.0
TREND_SIGNIFICANCE_LEVEL: Final[float] = 0.05
MIN_NON_ZERO_WEEKS: Final[int] = 52
SINGAPORE_POPULATION: Final[int] = 5_700_000

# Composite Burden Score Weights
VOLUME_WEIGHT: Final[float] = 0.40
TREND_WEIGHT: Final[float] = 0.25
OUTBREAK_WEIGHT: Final[float] = 0.20
VARIABILITY_WEIGHT: Final[float] = 0.15


def load_prioritization_config(config_path: str = "config/prioritization.yml") -> Dict[str, Any]:
    """Load disease prioritization framework configuration from YAML file.
    
    This function reads the prioritization configuration which includes weighting schemes,
    tier thresholds, and alternative scenarios for sensitivity analysis. The configuration
    is validated to ensure all weights sum to 1.0 (100%) and required keys are present.
    
    Args:
        config_path: Path to the prioritization configuration YAML file.
                    Defaults to 'config/prioritization.yml'.
    
    Returns:
        Dictionary containing prioritization configuration with keys:
            - base_case: Base weighting scheme and tier thresholds
            - scenarios: Alternative weighting scenarios for sensitivity analysis  
            - metrics: Mapping of criteria to burden metric columns
            - scoring: Composite score calculation settings
            - data_filters: Data quality filtering criteria
            - output: Output file paths and settings
            - logging: Logging configuration
    
    Raises:
        FileNotFoundError: If config file doesn't exist at specified path.
        ValueError: If configuration is invalid (weights don't sum to 1.0, 
                   missing required keys, invalid threshold ordering).
        yaml.YAMLError: If YAML file is malformed or unreadable.
    
    Example:
        >>> config = load_prioritization_config()
        >>> base_weights = config['base_case']['weights']
        >>> print(f"Volume weight: {base_weights['volume']}")
        Volume weight: 0.4
        >>> print(f"High priority threshold: {config['base_case']['tier_thresholds']['high']}")
        High priority threshold: 70.0
    """
    config_file = Path(config_path)
    
    # Check file exists
    if not config_file.exists():
        error_msg = f"Configuration file not found: {config_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    # Load YAML configuration
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Successfully loaded configuration from {config_path}")
    except yaml.YAMLError as e:
        error_msg = f"Failed to parse YAML configuration: {e}"
        logger.error(error_msg)
        raise yaml.YAMLError(error_msg)
    except Exception as e:
        error_msg = f"Error reading configuration file: {e}"
        logger.error(error_msg)
        raise
    
    # Validate required top-level keys
    required_keys = ['base_case', 'scenarios', 'metrics']
    missing_keys = set(required_keys) - set(config.keys())
    if missing_keys:
        error_msg = f"Missing required configuration keys: {missing_keys}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    # Validate base case weights
    base_weights = config['base_case']['weights']
    weight_sum = sum(base_weights.values())
    if abs(weight_sum - 1.0) > 0.001:
        error_msg = (f"Base case weights sum to {weight_sum:.3f}, must equal 1.0 (±0.001). "
                    f"Current weights: {base_weights}")
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    # Validate tier thresholds
    thresholds = config['base_case']['tier_thresholds']
    if thresholds['high'] <= thresholds['medium']:
        error_msg = (f"Invalid tier thresholds: high ({thresholds['high']}) must be > "
                    f"medium ({thresholds['medium']})")
        logger.error(error_msg)
        raise ValueError(error_msg)
    if thresholds['medium'] <= 0:
        error_msg = f"Invalid tier thresholds: medium ({thresholds['medium']}) must be > 0"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    # Validate all scenario weights
    for scenario_name, scenario_config in config['scenarios'].items():
        scenario_weights = scenario_config['weights']
        scenario_sum = sum(scenario_weights.values())
        if abs(scenario_sum - 1.0) > 0.001:
            error_msg = (f"Scenario '{scenario_name}' weights sum to {scenario_sum:.3f}, "
                        f"must equal 1.0 (±0.001). Current weights: {scenario_weights}")
            logger.error(error_msg)
            raise ValueError(error_msg)
    
    logger.info(f"Configuration validated successfully: {len(config['scenarios'])} scenarios loaded")
    return config
