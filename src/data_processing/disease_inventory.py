"""Disease inventory and categorization module."""
from typing import Dict, List
import polars as pl
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Disease name standardization mappings
DISEASE_NAME_MAPPINGS = {
    "HFMD": "Hand, Foot and Mouth Disease",
    "Hand, Foot Mouth Disease": "Hand, Foot and Mouth Disease",
    "Hand Foot and Mouth Disease": "Hand, Foot and Mouth Disease",
}

# Disease categorization by transmission mode
DISEASE_CATEGORIES = {
    "Vector-borne": [
        "Dengue Fever",
        "Dengue Haemorrhagic Fever",
        "Zika Virus Infection",
        "Chikungunya Fever",
        "Malaria",
        "Japanese Encephalitis"
    ],
    "Foodborne": [
        "Salmonellosis",
        "Campylobacter Enteritis",
        "Cholera",
        "Typhoid",
        "Paratyphoid"
    ],
    "Vaccine-preventable": [
        "Measles",
        "Mumps",
        "Rubella",
        "Diphtheria",
        "Pertussis",
        "Poliomyelitis",
        "Pneumococcal Disease (Invasive)"
    ],
    "Respiratory": [
        "Influenza A",
        "Influenza B",
        "Meningococcal Infection"
    ],
    "Other": []  # Will be populated with remaining diseases
}


def standardize_disease_names(
    df: pl.DataFrame,
    disease_column: str = "disease"
) -> pl.DataFrame:
    """Standardize disease names using predefined mappings.
    
    Args:
        df: DataFrame containing disease column
        disease_column: Name of the disease column
        
    Returns:
        DataFrame with standardized disease names
    """
    logger.info("Standardizing disease names...")
    
    # Log before counts
    before_unique = df[disease_column].n_unique()
    logger.info(f"Unique diseases before standardization: {before_unique}")
    
    # Apply mappings using replace_strict in Polars 0.19.0
    df_clean = df.with_columns([
        pl.col(disease_column).map_dict(DISEASE_NAME_MAPPINGS, default=pl.col(disease_column)).alias(disease_column)
    ])
    
    # Log after counts
    after_unique = df_clean[disease_column].n_unique()
    logger.info(f"Unique diseases after standardization: {after_unique}")
    logger.info(f"Merged {before_unique - after_unique} disease name variants")
    
    return df_clean


def categorize_diseases(disease_list: List[str]) -> Dict[str, str]:
    """Assign transmission mode categories to diseases.
    
    Args:
        disease_list: List of standardized disease names
        
    Returns:
        Dictionary mapping disease names to categories
    """
    logger.info("Categorizing diseases by transmission mode...")
    
    categorization = {}
    
    # Assign predefined categories
    for category, diseases in DISEASE_CATEGORIES.items():
        if category != "Other":
            for disease in diseases:
                if disease in disease_list:
                    categorization[disease] = category
    
    # Assign remaining diseases to "Other"
    for disease in disease_list:
        if disease not in categorization:
            categorization[disease] = "Other"
            logger.debug(f"Assigned '{disease}' to 'Other' category")
    
    # Log category distribution
    category_counts = {}
    for category in categorization.values():
        category_counts[category] = category_counts.get(category, 0) + 1
    
    logger.info("Disease category distribution:")
    for category, count in sorted(category_counts.items()):
        logger.info(f"  {category}: {count} diseases")
    
    return categorization


def calculate_disease_metrics(
    df: pl.DataFrame,
    disease_column: str = "disease",
    case_column: str = "no._of_cases"
) -> pl.DataFrame:
    """Calculate comprehensive metrics for each disease.
    
    Args:
        df: DataFrame with disease surveillance data
        disease_column: Name of disease column
        case_column: Name of case count column
        
    Returns:
        DataFrame with disease metrics
    """
    logger.info("Calculating disease metrics...")
    
    metrics = df.group_by(disease_column).agg([
        pl.col(case_column).sum().alias("total_cases"),
        pl.col(case_column).mean().alias("mean_weekly_cases"),
        pl.col(case_column).median().alias("median_weekly_cases"),
        pl.col(case_column).std().alias("std_weekly_cases"),
        pl.col(case_column).min().alias("min_cases"),
        pl.col(case_column).max().alias("max_cases"),
        (pl.col(case_column) == 0).sum().alias("weeks_with_zero_cases"),
        pl.col(case_column).count().alias("total_weeks")
    ]).with_columns([
        # Coefficient of variation
        (pl.col("std_weekly_cases") / pl.col("mean_weekly_cases")).alias("cv")
    ]).sort("total_cases", descending=True)
    
    # Add rank
    metrics = metrics.with_row_count("rank", offset=1)
    
    logger.info(f"Calculated metrics for {metrics.height} diseases")
    
    return metrics


def classify_burden_tier(total_cases: int) -> str:
    """Classify disease into burden tier based on total cases.
    
    Args:
        total_cases: Total case count
        
    Returns:
        Burden tier classification
    """
    if total_cases >= 1000:
        return "High"
    elif total_cases >= 100:
        return "Mid"
    else:
        return "Rare"


def create_disease_inventory(
    df: pl.DataFrame,
    disease_column: str = "disease",
    case_column: str = "no._of_cases"
) -> pl.DataFrame:
    """Create comprehensive disease inventory with all metrics and categories.
    
    Args:
        df: Raw disease surveillance DataFrame
        disease_column: Name of disease column
        case_column: Name of case count column
        
    Returns:
        Complete disease inventory DataFrame
    """
    logger.info("Creating disease inventory...")
    
    # Step 1: Standardize names
    df_clean = standardize_disease_names(df, disease_column)
    
    # Step 2: Calculate metrics
    metrics = calculate_disease_metrics(df_clean, disease_column, case_column)
    
    # Step 3: Add categories
    unique_diseases = metrics[disease_column].to_list()
    disease_to_category = categorize_diseases(unique_diseases)
    
    # Map categories
    category_mapping = pl.DataFrame({
        disease_column: list(disease_to_category.keys()),
        "disease_category": list(disease_to_category.values())
    })
    
    inventory = metrics.join(category_mapping, on=disease_column, how="left")
    
    # Step 4: Add burden tier
    inventory = inventory.with_columns([
        pl.col("total_cases").map_elements(
            classify_burden_tier,
            return_dtype=pl.Utf8
        ).alias("burden_tier")
    ])
    
    logger.info("Disease inventory created successfully")
    logger.info(f"Total diseases: {inventory.height}")
    
    # Log tier distribution
    tier_counts = inventory.group_by("burden_tier").agg(pl.count().alias("count"))
    logger.info("Burden tier distribution:")
    for row in tier_counts.iter_rows(named=True):
        logger.info(f"  {row['burden_tier']}: {row['count']} diseases")
    
    return inventory


def get_top_diseases(
    inventory: pl.DataFrame,
    n: int = 15,
    by: str = "total_cases"
) -> pl.DataFrame:
    """Get top N diseases by specified metric.
    
    Args:
        inventory: Disease inventory DataFrame
        n: Number of top diseases to return
        by: Column to sort by
        
    Returns:
        DataFrame with top N diseases
    """
    return inventory.sort(by, descending=True).head(n)


def get_diseases_by_category(
    inventory: pl.DataFrame,
    category: str
) -> pl.DataFrame:
    """Filter diseases by transmission category.
    
    Args:
        inventory: Disease inventory DataFrame
        category: Category name to filter by
        
    Returns:
        Filtered DataFrame
    """
    return inventory.filter(pl.col("disease_category") == category)
