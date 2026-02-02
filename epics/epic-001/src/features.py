"""
Epic 001: Feature Engineering Module
Calculate utilization rates, performance metrics, and bottleneck indicators
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging


class UtilizationFeatureEngineer:
    """Engineer features for facility utilization analysis"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize feature engineer
        
        Args:
            logger: Logger instance (creates new if None)
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize DataFrame column names
        
        Args:
            df: DataFrame to standardize
            
        Returns:
            DataFrame with standardized column names
        """
        df = df.copy()
        df.columns = (
            df.columns
            .str.lower()
            .str.replace(' ', '_')
            .str.replace('-', '_')
            .str.replace('[^a-z0-9_]', '', regex=True)
        )
        self.logger.debug(f"Standardized {len(df.columns)} column names")
        return df
    
    def calculate_utilization_rate(
        self, 
        attendances_df: pd.DataFrame, 
        beds_df: pd.DataFrame,
        days_per_year: int = 365
    ) -> pd.DataFrame:
        """
        Calculate utilization rates
        
        Formula: utilization_rate = (actual_attendances / capacity) × 100
        
        Args:
            attendances_df: DataFrame with attendance data
            beds_df: DataFrame with bed capacity data
            days_per_year: Days per year for capacity calculation
            
        Returns:
            DataFrame with utilization rates
        """
        # Standardize column names
        attendances_df = self.standardize_column_names(attendances_df)
        beds_df = self.standardize_column_names(beds_df)
        
        # Merge attendance and capacity data
        merged = pd.merge(
            attendances_df,
            beds_df,
            on=['year', 'hospital'],
            how='inner',
            suffixes=('_attend', '_beds')
        )
        
        # Calculate annual capacity (beds × days per year)
        merged['annual_capacity'] = merged['beds_no'] * days_per_year
        
        # Calculate utilization rate
        merged['utilization_rate_pct'] = (
            merged['attendances_no'] / merged['annual_capacity'] * 100
        )
        
        # Cap at 100% for reporting purposes (some may exceed due to day patients)
        merged['utilization_rate_capped'] = merged['utilization_rate_pct'].clip(upper=100)
        
        # Calculate excess/deficit capacity
        merged['capacity_gap'] = merged['attendances_no'] - merged['annual_capacity']
        merged['capacity_gap_pct'] = (
            merged['capacity_gap'] / merged['annual_capacity'] * 100
        )
        
        self.logger.info(
            f"Calculated utilization rates for {len(merged)} facility-years "
            f"(mean: {merged['utilization_rate_pct'].mean():.1f}%)"
        )
        return merged
    
    def categorize_utilization_level(
        self, 
        utilization_rate: float,
        thresholds: Optional[Dict[str, float]] = None
    ) -> str:
        """
        Categorize utilization into performance tiers
        
        Args:
            utilization_rate: Utilization rate percentage
            thresholds: Custom thresholds (optional)
            
        Returns:
            Utilization category string
        """
        if thresholds is None:
            thresholds = {
                'underutilized': 50.0,
                'optimal_low': 70.0,
                'optimal_high': 85.0,
                'high_utilization': 90.0
            }
        
        if utilization_rate < thresholds['underutilized']:
            return 'Underutilized'
        elif utilization_rate < thresholds['optimal_low']:
            return 'Below Optimal'
        elif utilization_rate <= thresholds['optimal_high']:
            return 'Optimal'
        elif utilization_rate < thresholds['high_utilization']:
            return 'High Utilization'
        else:
            return 'Overutilized'
    
    def calculate_facility_percentiles(
        self, 
        df: pd.DataFrame, 
        metric_col: str
    ) -> pd.DataFrame:
        """
        Calculate percentile rankings for facilities
        
        Args:
            df: DataFrame with facilities and metrics
            metric_col: Column name for metric to rank
            
        Returns:
            DataFrame with percentile columns added
        """
        df = df.copy()
        
        # Calculate percentile ranking
        df[f'{metric_col}_percentile'] = df[metric_col].rank(pct=True) * 100
        
        # Assign performance tier
        df['performance_tier'] = df[f'{metric_col}_percentile'].apply(
            lambda x: 'Top Performer' if x >= 90 else
                     'High Performer' if x >= 75 else
                     'Average Performer' if x >= 25 else
                     'Below Average' if x >= 10 else
                     'Low Performer'
        )
        
        self.logger.info(f"Calculated percentiles for {metric_col}")
        return df
    
    def identify_bottlenecks(
        self, 
        df: pd.DataFrame, 
        threshold: float = 90.0,
        recent_years_only: bool = True,
        recent_year_threshold: int = 2015
    ) -> pd.DataFrame:
        """
        Identify facilities operating at bottleneck levels
        
        Args:
            df: DataFrame with utilization data
            threshold: Utilization threshold for bottleneck (%)
            recent_years_only: Only consider recent years
            recent_year_threshold: Year threshold for recent data
            
        Returns:
            DataFrame with bottleneck facilities
        """
        # Filter to recent years if specified
        if recent_years_only:
            df = df[df['year'] >= recent_year_threshold].copy()
            self.logger.info(f"Filtering to years >= {recent_year_threshold}")
        
        # Identify overutilized facilities
        bottlenecks = df[df['utilization_rate_pct'] >= threshold].copy()
        
        # Calculate severity score
        # Severity = (utilization - threshold) × log(patient volume)
        bottlenecks['severity_score'] = (
            (bottlenecks['utilization_rate_pct'] - threshold) * 
            np.log1p(bottlenecks['attendances_no'])
        )
        
        # Calculate impact metrics
        bottlenecks['excess_demand'] = bottlenecks['capacity_gap']
        bottlenecks['patients_affected_annually'] = bottlenecks['excess_demand'].clip(lower=0)
        
        # Sort by severity
        bottlenecks = bottlenecks.sort_values('severity_score', ascending=False)
        
        self.logger.info(
            f"Identified {len(bottlenecks)} bottleneck facilities "
            f"(threshold: {threshold}%)"
        )
        return bottlenecks
    
    def create_temporal_features(
        self, 
        df: pd.DataFrame, 
        date_col: str = 'year'
    ) -> pd.DataFrame:
        """
        Create temporal features for time series analysis
        
        Args:
            df: DataFrame with temporal data
            date_col: Column name for date/year
            
        Returns:
            DataFrame with temporal features added
        """
        df = df.copy()
        
        # Convert to datetime
        df['year_date'] = pd.to_datetime(df[date_col].astype(str) + '-01-01')
        
        # Days since epoch (for modeling)
        df['days_since_2000'] = (df['year_date'] - pd.Timestamp('2000-01-01')).dt.days
        
        # Recent data flag
        df['is_recent'] = df[date_col] >= 2015
        
        # Year-over-year calculations (if multiple years per facility)
        if 'hospital' in df.columns:
            df = df.sort_values(['hospital', date_col])
            df['utilization_yoy_change'] = df.groupby('hospital')['utilization_rate_pct'].diff()
            df['attendances_yoy_change'] = df.groupby('hospital')['attendances_no'].pct_change() * 100
        
        self.logger.info("Created temporal features")
        return df
    
    def calculate_growth_rates(
        self, 
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate growth rates for key metrics
        
        Args:
            df: DataFrame with time series data
            
        Returns:
            DataFrame with growth rates
        """
        df = df.copy()
        
        if 'hospital' not in df.columns or 'year' not in df.columns:
            self.logger.warning("Missing required columns for growth calculation")
            return df
        
        # Sort by facility and year
        df = df.sort_values(['hospital', 'year'])
        
        # Calculate compound annual growth rate (CAGR) per facility
        growth_stats = []
        
        for hospital in df['hospital'].unique():
            hospital_data = df[df['hospital'] == hospital].sort_values('year')
            
            if len(hospital_data) >= 2:
                first_year = hospital_data.iloc[0]
                last_year = hospital_data.iloc[-1]
                years_span = last_year['year'] - first_year['year']
                
                if years_span > 0 and first_year['attendances_no'] > 0:
                    cagr = (
                        (last_year['attendances_no'] / first_year['attendances_no']) ** 
                        (1 / years_span) - 1
                    ) * 100
                    
                    growth_stats.append({
                        'hospital': hospital,
                        'attendance_cagr': cagr,
                        'years_analyzed': years_span,
                        'first_year': first_year['year'],
                        'last_year': last_year['year']
                    })
        
        growth_df = pd.DataFrame(growth_stats)
        
        # Merge back to main dataframe
        if not growth_df.empty:
            df = pd.merge(df, growth_df, on='hospital', how='left')
        
        self.logger.info(f"Calculated growth rates for {len(growth_stats)} facilities")
        return df
    
    def engineer_all_features(
        self, 
        attendances_df: pd.DataFrame, 
        beds_df: pd.DataFrame,
        config: Optional[Dict] = None
    ) -> pd.DataFrame:
        """
        Run complete feature engineering pipeline
        
        Args:
            attendances_df: DataFrame with attendance data
            beds_df: DataFrame with bed capacity data
            config: Configuration dictionary (optional)
            
        Returns:
            DataFrame with all engineered features
        """
        self.logger.info("Starting feature engineering pipeline...")
        
        # Step 1: Calculate utilization rates
        utilization_df = self.calculate_utilization_rate(attendances_df, beds_df)
        
        # Step 2: Add utilization categories
        thresholds = config.get('thresholds') if config else None
        utilization_df['utilization_category'] = utilization_df['utilization_rate_pct'].apply(
            lambda x: self.categorize_utilization_level(x, thresholds)
        )
        
        # Step 3: Add performance tiers
        utilization_df = self.calculate_facility_percentiles(
            utilization_df, 
            'utilization_rate_pct'
        )
        
        # Step 4: Add temporal features
        utilization_df = self.create_temporal_features(utilization_df)
        
        # Step 5: Calculate growth rates
        utilization_df = self.calculate_growth_rates(utilization_df)
        
        self.logger.info(
            f"Feature engineering complete: {len(utilization_df)} records, "
            f"{len(utilization_df.columns)} features"
        )
        
        return utilization_df
