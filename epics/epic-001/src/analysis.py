"""
Epic 001: Analysis Module
Perform facility performance profiling, bottleneck detection, and root cause analysis
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional
import logging


class FacilityAnalyzer:
    """Analyze facility performance and bottlenecks"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize analyzer
        
        Args:
            logger: Logger instance (creates new if None)
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def profile_facility_performance(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate comprehensive facility performance profiles
        
        Args:
            df: DataFrame with utilization data
            
        Returns:
            DataFrame with facility performance profiles
        """
        profiles = df.groupby('hospital').agg({
            'attendances_no': ['sum', 'mean', 'std'],
            'beds_no': 'mean',
            'utilization_rate_pct': ['mean', 'min', 'max', 'std'],
            'year': 'count'
        }).reset_index()
        
        # Flatten column names
        profiles.columns = ['_'.join(col).strip('_') if col[1] else col[0] 
                           for col in profiles.columns.values]
        
        # Rename for clarity
        profiles.rename(columns={
            'year_count': 'years_in_dataset'
        }, inplace=True)
        
        self.logger.info(f"Generated profiles for {len(profiles)} facilities")
        return profiles
    
    def detect_bottlenecks(
        self, 
        df: pd.DataFrame, 
        min_severity: float = 5.0,
        utilization_threshold: float = 90.0,
        recent_years_only: bool = True,
        recent_year_threshold: int = 2015
    ) -> pd.DataFrame:
        """
        Detect and quantify operational bottlenecks
        
        Args:
            df: DataFrame with utilization data
            min_severity: Minimum severity score to include
            utilization_threshold: Minimum utilization % for bottleneck
            recent_years_only: Only consider recent years
            recent_year_threshold: Year threshold for recent data
            
        Returns:
            DataFrame with detected bottlenecks
        """
        # Filter to recent years for current bottlenecks
        if recent_years_only:
            recent_df = df[df['year'] >= recent_year_threshold].copy()
            self.logger.info(f"Analyzing bottlenecks for years >= {recent_year_threshold}")
        else:
            recent_df = df.copy()
        
        # Identify overutilized facilities
        bottlenecks = recent_df[
            recent_df['utilization_rate_pct'] >= utilization_threshold
        ].copy()
        
        # Calculate impact metrics
        bottlenecks['excess_demand'] = (
            bottlenecks['attendances_no'] - 
            bottlenecks['annual_capacity'] * 0.85  # Assume 85% is optimal
        )
        
        bottlenecks['patients_affected_annually'] = bottlenecks['excess_demand'].clip(lower=0)
        
        # Calculate severity score
        # Severity = (utilization - threshold) × log(patient volume)
        bottlenecks['severity_score'] = (
            (bottlenecks['utilization_rate_pct'] - utilization_threshold) *
            np.log1p(bottlenecks['attendances_no'])
        )
        
        # Filter by minimum severity
        bottlenecks = bottlenecks[
            bottlenecks['severity_score'] >= min_severity
        ].sort_values('severity_score', ascending=False)
        
        self.logger.info(
            f"Detected {len(bottlenecks)} critical bottlenecks "
            f"(threshold: {utilization_threshold}%, min severity: {min_severity})"
        )
        return bottlenecks
    
    def root_cause_analysis(
        self, 
        bottleneck: pd.Series, 
        historical_df: pd.DataFrame
    ) -> Dict[str, any]:
        """
        Perform root cause analysis for a specific bottleneck
        
        Args:
            bottleneck: Series representing a single bottleneck
            historical_df: DataFrame with historical data for context
            
        Returns:
            Dictionary with root cause analysis results
        """
        hospital = bottleneck['hospital']
        
        # Get historical trend for this hospital
        hospital_history = historical_df[
            historical_df['hospital'] == hospital
        ].sort_values('year')
        
        # Calculate growth rate using linear regression
        annual_growth_rate = None
        r_squared = None
        
        if len(hospital_history) >= 2:
            years = hospital_history['year'].values
            utilization = hospital_history['utilization_rate_pct'].values
            
            try:
                slope, intercept, r_value, p_value, std_err = stats.linregress(
                    years, utilization
                )
                annual_growth_rate = slope
                r_squared = r_value ** 2
            except Exception as e:
                self.logger.warning(f"Could not calculate growth rate for {hospital}: {e}")
        
        # Identify potential causes
        causes = []
        
        # Rapid demand growth
        if annual_growth_rate and annual_growth_rate > 2:
            causes.append({
                'cause': 'Rapid demand growth',
                'evidence': f'Utilization growing at {annual_growth_rate:.2f}% per year',
                'priority': 'HIGH'
            })
        
        # Insufficient capacity
        if bottleneck['beds_no'] < hospital_history['beds_no'].median():
            causes.append({
                'cause': 'Insufficient capacity',
                'evidence': f"Current beds ({bottleneck['beds_no']:.0f}) below historical median",
                'priority': 'HIGH'
            })
        
        # Consistently high utilization
        if hospital_history['utilization_rate_pct'].min() > 80:
            causes.append({
                'cause': 'Chronically overutilized',
                'evidence': f"Minimum utilization over {len(hospital_history)} years: {hospital_history['utilization_rate_pct'].min():.1f}%",
                'priority': 'CRITICAL'
            })
        
        return {
            'hospital': hospital,
            'current_utilization': bottleneck['utilization_rate_pct'],
            'annual_growth_rate': annual_growth_rate,
            'trend_r_squared': r_squared,
            'root_causes': causes,
            'years_analyzed': len(hospital_history),
            'min_utilization': hospital_history['utilization_rate_pct'].min(),
            'max_utilization': hospital_history['utilization_rate_pct'].max(),
            'avg_utilization': hospital_history['utilization_rate_pct'].mean()
        }
    
    def benchmark_against_peers(
        self, 
        df: pd.DataFrame, 
        facility_id: str
    ) -> Dict[str, float]:
        """
        Benchmark a facility against peer facilities
        
        Args:
            df: DataFrame with all facilities
            facility_id: Hospital identifier to benchmark
            
        Returns:
            Dictionary with benchmarking metrics
        """
        facility_data = df[df['hospital'] == facility_id]['utilization_rate_pct'].mean()
        peer_avg = df['utilization_rate_pct'].mean()
        peer_median = df['utilization_rate_pct'].median()
        peer_std = df['utilization_rate_pct'].std()
        
        # Calculate percentile rank
        percentile_rank = (df['utilization_rate_pct'] < facility_data).sum() / len(df) * 100
        
        # Calculate z-score
        z_score = (facility_data - peer_avg) / peer_std if peer_std > 0 else 0
        
        return {
            'facility': facility_id,
            'facility_utilization': facility_data,
            'peer_average': peer_avg,
            'peer_median': peer_median,
            'peer_std': peer_std,
            'gap_vs_average': facility_data - peer_avg,
            'gap_vs_median': facility_data - peer_median,
            'percentile_rank': percentile_rank,
            'z_score': z_score
        }
    
    def generate_recommendations(
        self, 
        bottleneck_df: pd.DataFrame
    ) -> List[Dict]:
        """
        Generate improvement recommendations for bottlenecks
        
        Args:
            bottleneck_df: DataFrame with bottleneck facilities
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        for idx, row in bottleneck_df.iterrows():
            rec = {
                'hospital': row['hospital'],
                'year': row['year'],
                'current_utilization': row['utilization_rate_pct'],
                'current_beds': row['beds_no'],
                'recommendation_type': None,
                'recommendation_text': None,
                'expected_impact': None,
                'implementation_complexity': None,
                'estimated_cost': None
            }
            
            # Critical overutilization - capacity expansion needed
            if row['utilization_rate_pct'] > 95:
                additional_beds = int((row['utilization_rate_pct'] - 85) / 85 * row['beds_no'])
                rec['recommendation_type'] = 'Capacity Expansion'
                rec['recommendation_text'] = (
                    f"Increase bed capacity by approximately {additional_beds} beds "
                    f"to reduce utilization to optimal 85%"
                )
                rec['expected_impact'] = f"Reduce utilization by {row['utilization_rate_pct'] - 85:.1f}%"
                rec['implementation_complexity'] = 'HIGH'
                rec['estimated_cost'] = 'HIGH'
                
            # High utilization - process optimization
            elif row['utilization_rate_pct'] > 90:
                rec['recommendation_type'] = 'Process Optimization'
                rec['recommendation_text'] = (
                    "Optimize patient flow, discharge processes, and bed turnover "
                    "to increase effective capacity without physical expansion"
                )
                rec['expected_impact'] = 'Reduce utilization by 5-10%'
                rec['implementation_complexity'] = 'MEDIUM'
                rec['estimated_cost'] = 'MEDIUM'
            
            # Growth trend analysis
            if 'attendance_cagr' in row and pd.notna(row['attendance_cagr']):
                if row['attendance_cagr'] > 5:
                    rec['additional_recommendation'] = (
                        f"Attendance growing at {row['attendance_cagr']:.1f}% annually. "
                        "Develop 3-5 year capacity expansion roadmap."
                    )
            
            recommendations.append(rec)
        
        self.logger.info(f"Generated {len(recommendations)} recommendations")
        return recommendations
    
    def analyze_temporal_patterns(
        self, 
        df: pd.DataFrame
    ) -> Dict[str, any]:
        """
        Analyze temporal patterns in utilization
        
        Args:
            df: DataFrame with temporal utilization data
            
        Returns:
            Dictionary with temporal analysis results
        """
        # Overall trend across all facilities
        yearly_avg = df.groupby('year')['utilization_rate_pct'].agg(['mean', 'std', 'count'])
        
        # Calculate overall trend
        years = yearly_avg.index.values
        utilization = yearly_avg['mean'].values
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(years, utilization)
        
        # Identify facilities with significant trends
        facility_trends = []
        for hospital in df['hospital'].unique():
            hospital_data = df[df['hospital'] == hospital].sort_values('year')
            
            if len(hospital_data) >= 3:
                h_years = hospital_data['year'].values
                h_util = hospital_data['utilization_rate_pct'].values
                
                try:
                    h_slope, _, h_r, h_p, _ = stats.linregress(h_years, h_util)
                    
                    if h_p < 0.05:  # Significant trend
                        facility_trends.append({
                            'hospital': hospital,
                            'trend_slope': h_slope,
                            'r_squared': h_r ** 2,
                            'p_value': h_p,
                            'trend_direction': 'Increasing' if h_slope > 0 else 'Decreasing'
                        })
                except:
                    pass
        
        return {
            'overall_trend_slope': slope,
            'overall_trend_r_squared': r_value ** 2,
            'overall_trend_p_value': p_value,
            'overall_trend_direction': 'Increasing' if slope > 0 else 'Decreasing',
            'yearly_statistics': yearly_avg.to_dict(),
            'facilities_with_significant_trends': len(facility_trends),
            'facility_trends': facility_trends
        }
    
    def run_comprehensive_analysis(
        self,
        df: pd.DataFrame,
        config: Optional[Dict] = None
    ) -> Dict[str, any]:
        """
        Run comprehensive analysis pipeline
        
        Args:
            df: DataFrame with utilization data
            config: Configuration dictionary
            
        Returns:
            Dictionary with all analysis results
        """
        self.logger.info("Starting comprehensive analysis...")
        
        # Use default config if none provided
        if config is None:
            config = {
                'bottleneck_threshold': 90.0,
                'min_severity': 5.0
            }
        
        # Performance profiles
        profiles = self.profile_facility_performance(df)
        
        # Bottleneck detection
        bottlenecks = self.detect_bottlenecks(
            df,
            min_severity=config.get('min_severity', 5.0),
            utilization_threshold=config.get('bottleneck_threshold', 90.0)
        )
        
        # Recommendations
        recommendations = self.generate_recommendations(bottlenecks)
        
        # Temporal analysis
        temporal_analysis = self.analyze_temporal_patterns(df)
        
        results = {
            'summary': {
                'total_facilities': len(profiles),
                'total_bottlenecks': len(bottlenecks),
                'total_recommendations': len(recommendations),
                'avg_utilization': df['utilization_rate_pct'].mean(),
                'median_utilization': df['utilization_rate_pct'].median(),
                'std_utilization': df['utilization_rate_pct'].std()
            },
            'profiles': profiles,
            'bottlenecks': bottlenecks,
            'recommendations': recommendations,
            'temporal_analysis': temporal_analysis
        }
        
        self.logger.info("Comprehensive analysis complete")
        return results
