"""
Epic 001: Test Feature Engineering Module
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
epic_root = Path(__file__).parent.parent
sys.path.insert(0, str(epic_root / 'src'))

from features import UtilizationFeatureEngineer


@pytest.fixture
def sample_attendance_data():
    """Fixture providing sample attendance data"""
    return pd.DataFrame({
        'year': [2018, 2019, 2020] * 2,
        'hospital': ['Hospital A'] * 3 + ['Hospital B'] * 3,
        'attendances_no': [10000, 11000, 12000, 8000, 8500, 9000]
    })


@pytest.fixture
def sample_beds_data():
    """Fixture providing sample beds data"""
    return pd.DataFrame({
        'year': [2018, 2019, 2020] * 2,
        'hospital': ['Hospital A'] * 3 + ['Hospital B'] * 3,
        'beds_no': [30, 32, 35, 25, 25, 26]
    })


@pytest.fixture
def engineer():
    """Fixture providing UtilizationFeatureEngineer instance"""
    return UtilizationFeatureEngineer()


class TestUtilizationFeatureEngineer:
    """Test suite for UtilizationFeatureEngineer"""
    
    def test_standardize_column_names(self, engineer):
        """Test column name standardization"""
        df = pd.DataFrame({
            'Year': [2020],
            'Hospital Name': ['Test'],
            'Number-of-Beds': [30]
        })
        
        result = engineer.standardize_column_names(df)
        
        assert 'year' in result.columns
        assert 'hospital_name' in result.columns
        assert 'numberofbeds' in result.columns
    
    def test_calculate_utilization_rate(self, engineer, sample_attendance_data, sample_beds_data):
        """Test utilization rate calculation"""
        result = engineer.calculate_utilization_rate(
            sample_attendance_data,
            sample_beds_data
        )
        
        # Check that key columns exist
        assert 'utilization_rate_pct' in result.columns
        assert 'annual_capacity' in result.columns
        assert 'capacity_gap' in result.columns
        
        # Check that utilization rates are calculated
        assert result['utilization_rate_pct'].notna().all()
        assert (result['utilization_rate_pct'] >= 0).all()
        
        # Check annual capacity calculation (beds × 365)
        expected_capacity = result['beds_no'] * 365
        assert (result['annual_capacity'] == expected_capacity).all()
    
    def test_categorize_utilization_level(self, engineer):
        """Test utilization level categorization"""
        assert engineer.categorize_utilization_level(40.0) == 'Underutilized'
        assert engineer.categorize_utilization_level(65.0) == 'Below Optimal'
        assert engineer.categorize_utilization_level(75.0) == 'Optimal'
        assert engineer.categorize_utilization_level(88.0) == 'High Utilization'
        assert engineer.categorize_utilization_level(95.0) == 'Overutilized'
    
    def test_calculate_facility_percentiles(self, engineer):
        """Test percentile calculation"""
        df = pd.DataFrame({
            'hospital': ['A', 'B', 'C', 'D', 'E'],
            'utilization_rate_pct': [50, 70, 80, 90, 95]
        })
        
        result = engineer.calculate_facility_percentiles(df, 'utilization_rate_pct')
        
        assert 'utilization_rate_pct_percentile' in result.columns
        assert 'performance_tier' in result.columns
        assert result['utilization_rate_pct_percentile'].max() == 100.0
        assert result['utilization_rate_pct_percentile'].min() == 20.0  # 1/5 = 20%
    
    def test_identify_bottlenecks(self, engineer):
        """Test bottleneck identification"""
        df = pd.DataFrame({
            'year': [2019, 2020] * 3,
            'hospital': ['A', 'A', 'B', 'B', 'C', 'C'],
            'utilization_rate_pct': [92, 95, 85, 87, 91, 93],
            'attendances_no': [10000, 11000, 8000, 8500, 9000, 9500],
            'annual_capacity': [9000, 9500, 9000, 9500, 9000, 9500],
            'capacity_gap': [1000, 1500, -1000, -1000, 0, 0]
        })
        
        result = engineer.identify_bottlenecks(df, threshold=90.0, recent_years_only=False)
        
        assert len(result) > 0
        assert 'severity_score' in result.columns
        assert (result['utilization_rate_pct'] >= 90.0).all()
    
    def test_create_temporal_features(self, engineer):
        """Test temporal feature creation"""
        df = pd.DataFrame({
            'year': [2018, 2019, 2020],
            'hospital': ['A', 'A', 'A'],
            'utilization_rate_pct': [70, 75, 80]
        })
        
        result = engineer.create_temporal_features(df)
        
        assert 'year_date' in result.columns
        assert 'days_since_2000' in result.columns
        assert 'is_recent' in result.columns
        assert result['is_recent'].dtype == bool


def test_engineer_all_features_integration(engineer, sample_attendance_data, sample_beds_data):
    """Integration test for complete feature engineering pipeline"""
    result = engineer.engineer_all_features(
        sample_attendance_data,
        sample_beds_data
    )
    
    # Check all expected features are present
    expected_columns = [
        'utilization_rate_pct',
        'utilization_category',
        'performance_tier',
        'year_date',
        'is_recent'
    ]
    
    for col in expected_columns:
        assert col in result.columns, f"Missing column: {col}"
    
    # Check data quality
    assert len(result) > 0
    assert result['utilization_rate_pct'].notna().all()
