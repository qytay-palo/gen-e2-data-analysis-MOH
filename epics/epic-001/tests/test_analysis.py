"""
Epic 001: Test Analysis Module
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
epic_root = Path(__file__).parent.parent
sys.path.insert(0, str(epic_root / 'src'))

from analysis import FacilityAnalyzer


@pytest.fixture
def sample_utilization_data():
    """Fixture providing sample utilization data"""
    return pd.DataFrame({
        'year': [2018, 2019, 2020] * 3,
        'hospital': ['A'] * 3 + ['B'] * 3 + ['C'] * 3,
        'attendances_no': [10000, 11000, 12000, 8000, 8500, 9000, 6000, 6500, 7000],
        'beds_no': [30, 32, 35, 25, 25, 26, 20, 21, 22],
        'utilization_rate_pct': [91.3, 94.0, 93.8, 87.7, 93.2, 94.8, 82.2, 84.8, 87.1],
        'annual_capacity': [10950, 11680, 12775, 9125, 9125, 9490, 7300, 7665, 8030],
        'severity_score': [45.2, 52.1, 50.3, 30.1, 42.3, 48.5, 15.2, 18.9, 22.5]
    })


@pytest.fixture
def analyzer():
    """Fixture providing FacilityAnalyzer instance"""
    return FacilityAnalyzer()


class TestFacilityAnalyzer:
    """Test suite for FacilityAnalyzer"""
    
    def test_profile_facility_performance(self, analyzer, sample_utilization_data):
        """Test facility performance profiling"""
        result = analyzer.profile_facility_performance(sample_utilization_data)
        
        # Check structure
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3  # 3 unique hospitals
        assert 'hospital' in result.columns
        assert 'utilization_rate_pct_mean' in result.columns
        assert 'years_in_dataset' in result.columns
        
        # Check calculations
        hospital_a = result[result['hospital'] == 'A'].iloc[0]
        assert hospital_a['years_in_dataset'] == 3
    
    def test_detect_bottlenecks(self, analyzer, sample_utilization_data):
        """Test bottleneck detection"""
        result = analyzer.detect_bottlenecks(
            sample_utilization_data,
            min_severity=10.0,
            utilization_threshold=90.0,
            recent_years_only=False
        )
        
        # Check that bottlenecks are identified
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert (result['utilization_rate_pct'] >= 90.0).all()
        assert 'severity_score' in result.columns
        assert 'patients_affected_annually' in result.columns
    
    def test_root_cause_analysis(self, analyzer, sample_utilization_data):
        """Test root cause analysis"""
        # Get a bottleneck facility
        bottleneck = sample_utilization_data[
            sample_utilization_data['utilization_rate_pct'] > 90
        ].iloc[0]
        
        result = analyzer.root_cause_analysis(bottleneck, sample_utilization_data)
        
        # Check structure
        assert isinstance(result, dict)
        assert 'hospital' in result
        assert 'current_utilization' in result
        assert 'root_causes' in result
        assert 'years_analyzed' in result
        assert isinstance(result['root_causes'], list)
    
    def test_benchmark_against_peers(self, analyzer, sample_utilization_data):
        """Test peer benchmarking"""
        result = analyzer.benchmark_against_peers(sample_utilization_data, 'A')
        
        # Check structure
        assert isinstance(result, dict)
        assert 'facility' in result
        assert 'facility_utilization' in result
        assert 'peer_average' in result
        assert 'peer_median' in result
        assert 'gap_vs_average' in result
        assert 'percentile_rank' in result
        assert 'z_score' in result
        
        # Check calculations
        assert result['facility'] == 'A'
        assert 0 <= result['percentile_rank'] <= 100
    
    def test_generate_recommendations(self, analyzer, sample_utilization_data):
        """Test recommendation generation"""
        bottlenecks = sample_utilization_data[
            sample_utilization_data['utilization_rate_pct'] >= 90
        ]
        
        result = analyzer.generate_recommendations(bottlenecks)
        
        # Check structure
        assert isinstance(result, list)
        assert len(result) > 0
        
        for rec in result:
            assert 'hospital' in rec
            assert 'recommendation_type' in rec
            assert 'recommendation_text' in rec
            assert 'implementation_complexity' in rec
    
    def test_analyze_temporal_patterns(self, analyzer, sample_utilization_data):
        """Test temporal pattern analysis"""
        result = analyzer.analyze_temporal_patterns(sample_utilization_data)
        
        # Check structure
        assert isinstance(result, dict)
        assert 'overall_trend_slope' in result
        assert 'overall_trend_direction' in result
        assert 'facilities_with_significant_trends' in result
        assert 'facility_trends' in result
    
    def test_run_comprehensive_analysis(self, analyzer, sample_utilization_data):
        """Test comprehensive analysis pipeline"""
        result = analyzer.run_comprehensive_analysis(sample_utilization_data)
        
        # Check structure
        assert isinstance(result, dict)
        assert 'summary' in result
        assert 'profiles' in result
        assert 'bottlenecks' in result
        assert 'recommendations' in result
        assert 'temporal_analysis' in result
        
        # Check summary metrics
        summary = result['summary']
        assert 'total_facilities' in summary
        assert 'total_bottlenecks' in summary
        assert 'avg_utilization' in summary
        assert summary['total_facilities'] == 3


def test_edge_case_no_bottlenecks(analyzer):
    """Test analysis with no bottlenecks"""
    df = pd.DataFrame({
        'year': [2020, 2020],
        'hospital': ['A', 'B'],
        'utilization_rate_pct': [70.0, 75.0],
        'attendances_no': [8000, 9000],
        'beds_no': [30, 32],
        'annual_capacity': [10950, 11680],
        'severity_score': [5.0, 8.0]
    })
    
    result = analyzer.detect_bottlenecks(df, min_severity=20.0, utilization_threshold=90.0)
    
    assert len(result) == 0


def test_edge_case_single_year(analyzer):
    """Test analysis with single year of data"""
    df = pd.DataFrame({
        'year': [2020, 2020],
        'hospital': ['A', 'B'],
        'utilization_rate_pct': [92.0, 88.0],
        'attendances_no': [10000, 9000],
        'beds_no': [30, 28],
        'annual_capacity': [10950, 10220]
    })
    
    result = analyzer.profile_facility_performance(df)
    
    assert len(result) == 2
    assert all(result['years_in_dataset'] == 1)
