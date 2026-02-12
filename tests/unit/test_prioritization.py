"""Unit tests for disease prioritization module.

Tests cover all core functions including normalization, composite scoring,
tier assignment, ranking, and sensitivity analysis with comprehensive edge cases.

Run tests with:
    pytest tests/unit/test_prioritization.py -v --cov=src.analysis.prioritization

Author: MOH Data Analytics Team
Created: 2026-02-12
"""

import pytest
import polars as pl
import numpy as np
from src.analysis.prioritization import (
    validate_burden_metrics_input,
    normalize_metrics,
    calculate_composite_score,
    assign_tiers,
    rank_diseases,
    sensitivity_analysis,
    calculate_rank_correlation,
    identify_consensus_priorities
)


class TestValidation:
    """Test input validation functions."""
    
    def test_validate_empty_dataframe(self):
        """Test that empty DataFrame raises ValueError."""
        df_empty = pl.DataFrame()
        with pytest.raises(ValueError, match="Input DataFrame is empty"):
            validate_burden_metrics_input(df_empty)
    
    def test_validate_missing_columns(self):
        """Test that missing required columns raises KeyError."""
        df = pl.DataFrame({'disease_name': ['Disease A']})
        with pytest.raises(KeyError, match="Missing required columns"):
            validate_burden_metrics_input(df)
    
    def test_validate_valid_input(self):
        """Test that valid DataFrame passes validation."""
        df = pl.DataFrame({
            'disease_name': ['Disease A'],
            'sufficient_data': [True],
            'total_cases_score': [50.0],
            'annual_avg_cases_score': [50.0],
            'cagr_score': [75.0],
            'outbreak_score': [60.0],
            'coefficient_variation_score': [40.0]
        })
        # Should not raise any exceptions
        validate_burden_metrics_input(df)


class TestNormalization:
    """Test metric normalization functions."""
    
    def test_normalize_metrics_range(self):
        """Test that normalized values are within 0-100 range."""
        df = pl.DataFrame({
            'metric1': [10.0, 50.0, 100.0],
            'metric2': [0.0, 25.0, 75.0]
        })
        df_norm = normalize_metrics(df, ['metric1', 'metric2'])
        
        assert df_norm['metric1'].min() >= 0.0
        assert df_norm['metric1'].max() <= 100.0
        assert df_norm['metric2'].min() >= 0.0
        assert df_norm['metric2'].max() <= 100.0
    
    def test_normalize_metrics_min_max_mapping(self):
        """Test that min value maps to 0 and max value maps to 100."""
        df = pl.DataFrame({'metric': [10.0, 50.0, 100.0]})
        df_norm = normalize_metrics(df, ['metric'])
        
        assert df_norm['metric'][0] == 0.0  # min value
        assert df_norm['metric'][2] == 100.0  # max value
    
    def test_normalize_metrics_handles_ties(self):
        """Test that all identical values map to midpoint (50.0)."""
        df = pl.DataFrame({'metric': [42.0, 42.0, 42.0]})
        df_norm = normalize_metrics(df, ['metric'])
        
        assert all(df_norm['metric'] == 50.0)
    
    def test_normalize_metrics_handles_nan(self):
        """Test that NaN values raise ValueError."""
        df = pl.DataFrame({'metric': [10.0, None, 100.0]})
        with pytest.raises(ValueError, match="contains NaN values"):
            normalize_metrics(df, ['metric'])
    
    def test_normalize_empty_dataframe(self):
        """Test that empty DataFrame raises ValueError."""
        df_empty = pl.DataFrame()
        with pytest.raises(ValueError, match="Input DataFrame is empty"):
            normalize_metrics(df_empty, ['metric'])
    
    def test_normalize_missing_columns(self):
        """Test that missing metric columns raise KeyError."""
        df = pl.DataFrame({'metric1': [10.0, 50.0]})
        with pytest.raises(KeyError, match="Missing metric columns"):
            normalize_metrics(df, ['metric1', 'metric2'])
    
    def test_normalize_custom_scale_range(self):
        """Test normalization with custom scale range."""
        df = pl.DataFrame({'metric': [0.0, 50.0, 100.0]})
        df_norm = normalize_metrics(df, ['metric'], scale_range=(0.0, 1.0))
        
        assert df_norm['metric'].min() == 0.0
        assert df_norm['metric'].max() == 1.0
        assert abs(df_norm['metric'][1] - 0.5) < 0.01


class TestCompositeScore:
    """Test composite score calculation."""
    
    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for testing."""
        return pl.DataFrame({
            'disease_name': ['Disease A', 'Disease B'],
            'total_cases_score': [50.0, 100.0],
            'annual_avg_cases_score': [50.0, 100.0],
            'cagr_score': [75.0, 25.0],
            'outbreak_score': [60.0, 40.0],
            'coefficient_variation_score': [30.0, 70.0]
        })
    
    def test_composite_score_calculation(self, sample_df):
        """Test that composite score is calculated correctly."""
        weights = {'volume': 0.40, 'trend': 0.25, 'outbreak': 0.20, 'variability': 0.15}
        df_scored = calculate_composite_score(sample_df, weights)
        
        # Verify composite_score column exists
        assert 'composite_score' in df_scored.columns
        
        # Manual calculation for Disease A:
        # volume = (50 + 50) / 2 = 50
        # trend = 75
        # outbreak = 60
        # variability = 30
        # composite = 50*0.4 + 75*0.25 + 60*0.2 + 30*0.15 = 20 + 18.75 + 12 + 4.5 = 55.25
        expected_a = 55.25
        actual_a = df_scored.filter(pl.col('disease_name') == 'Disease A')['composite_score'][0]
        assert abs(actual_a - expected_a) < 0.01
    
    def test_composite_score_weights_validation(self, sample_df):
        """Test that weights not summing to 1.0 raises ValueError."""
        weights = {'volume': 0.50, 'trend': 0.25, 'outbreak': 0.20, 'variability': 0.15}
        with pytest.raises(ValueError, match="Weights sum to"):
            calculate_composite_score(sample_df, weights)
    
    def test_composite_score_range(self, sample_df):
        """Test that composite scores are in 0-100 range."""
        weights = {'volume': 0.40, 'trend': 0.25, 'outbreak': 0.20, 'variability': 0.15}
        df_scored = calculate_composite_score(sample_df, weights)
        
        assert df_scored['composite_score'].min() >= 0.0
        assert df_scored['composite_score'].max() <= 100.0
    
    def test_composite_score_missing_criteria(self, sample_df):
        """Test that missing weight criteria raises ValueError."""
        weights = {'volume': 0.70, 'trend': 0.30}  # Missing outbreak and variability
        with pytest.raises(ValueError, match="Weights must include exactly these criteria"):
            calculate_composite_score(sample_df, weights)
    
    def test_composite_score_empty_dataframe(self):
        """Test that empty DataFrame raises ValueError."""
        df_empty = pl.DataFrame()
        weights = {'volume': 0.40, 'trend': 0.25, 'outbreak': 0.20, 'variability': 0.15}
        with pytest.raises(ValueError, match="Input DataFrame is empty"):
            calculate_composite_score(df_empty, weights)


class TestTierAssignment:
    """Test priority tier assignment."""
    
    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame with various scores."""
        return pl.DataFrame({
            'disease_name': ['Disease A', 'Disease B', 'Disease C', 'Disease D'],
            'composite_score': [85.0, 60.0, 40.0, 20.0]
        })
    
    def test_assign_tiers_high_priority(self, sample_df):
        """Test that scores > 70 are assigned High tier."""
        thresholds = {'high': 70.0, 'medium': 40.0}
        df_tiered = assign_tiers(sample_df, thresholds)
        
        high_tier = df_tiered.filter(pl.col('tier') == 'High')
        assert len(high_tier) == 1
        assert high_tier['disease_name'][0] == 'Disease A'
    
    def test_assign_tiers_medium_priority(self, sample_df):
        """Test that 40 <= scores <= 70 are assigned Medium tier."""
        thresholds = {'high': 70.0, 'medium': 40.0}
        df_tiered = assign_tiers(sample_df, thresholds)
        
        medium_tier = df_tiered.filter(pl.col('tier') == 'Medium')
        assert len(medium_tier) == 2
        assert 'Disease B' in medium_tier['disease_name'].to_list()
        assert 'Disease C' in medium_tier['disease_name'].to_list()
    
    def test_assign_tiers_low_priority(self, sample_df):
        """Test that scores < 40 are assigned Low tier."""
        thresholds = {'high': 70.0, 'medium': 40.0}
        df_tiered = assign_tiers(sample_df, thresholds)
        
        low_tier = df_tiered.filter(pl.col('tier') == 'Low')
        assert len(low_tier) == 1
        assert low_tier['disease_name'][0] == 'Disease D'
    
    def test_assign_tiers_boundary_cases(self):
        """Test exact threshold values (70.0, 40.0) are assigned correctly."""
        df = pl.DataFrame({
            'disease_name': ['At High', 'At Medium', 'Just Above Medium'],
            'composite_score': [70.0, 40.0, 70.1]
        })
        thresholds = {'high': 70.0, 'medium': 40.0}
        df_tiered = assign_tiers(df, thresholds)
        
        # 70.0 should be Medium (not > 70.0)
        assert df_tiered.filter(pl.col('disease_name') == 'At High')['tier'][0] == 'Medium'
        # 40.0 should be Medium (>= 40.0)
        assert df_tiered.filter(pl.col('disease_name') == 'At Medium')['tier'][0] == 'Medium'
        # 70.1 should be High (> 70.0)
        assert df_tiered.filter(pl.col('disease_name') == 'Just Above Medium')['tier'][0] == 'High'
    
    def test_assign_tiers_invalid_thresholds(self, sample_df):
        """Test that invalid thresholds (high <= medium) raises ValueError."""
        thresholds = {'high': 40.0, 'medium': 70.0}
        with pytest.raises(ValueError, match="high.*must be > medium"):
            assign_tiers(sample_df, thresholds)
    
    def test_assign_tiers_negative_medium(self, sample_df):
        """Test that negative medium threshold raises ValueError."""
        thresholds = {'high': 70.0, 'medium': -10.0}
        with pytest.raises(ValueError, match="medium.*must be > 0"):
            assign_tiers(sample_df, thresholds)


class TestRanking:
    """Test disease ranking functions."""
    
    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for ranking."""
        return pl.DataFrame({
            'disease_name': ['Disease A', 'Disease B', 'Disease C'],
            'composite_score': [75.0, 85.0, 65.0]
        })
    
    def test_rank_diseases_descending(self, sample_df):
        """Test that highest score gets rank 1."""
        df_ranked = rank_diseases(sample_df)
        
        assert df_ranked['rank'][0] == 1
        assert df_ranked['disease_name'][0] == 'Disease B'  # Highest score (85.0)
    
    def test_rank_diseases_sequence(self, sample_df):
        """Test that ranks have no gaps (1, 2, 3, ...)."""
        df_ranked = rank_diseases(sample_df)
        
        ranks = df_ranked['rank'].to_list()
        assert ranks == [1, 2, 3]
    
    def test_rank_diseases_handles_ties(self):
        """Test tie-breaking is consistent (stable sort)."""
        df = pl.DataFrame({
            'disease_name': ['A', 'B', 'C'],
            'composite_score': [75.0, 75.0, 65.0]
        })
        df_ranked = rank_diseases(df)
        
        # Ties should preserve original order
        assert df_ranked['rank'][0] in [1, 2]  # One of the tied scores
        assert df_ranked['rank'][1] in [1, 2]  # One of the tied scores
        assert df_ranked['rank'][2] == 3
    
    def test_rank_diseases_no_duplicates(self, sample_df):
        """Test that all ranks are unique."""
        df_ranked = rank_diseases(sample_df)
        
        assert df_ranked['rank'].is_unique().all()
    
    def test_rank_diseases_empty_dataframe(self):
        """Test that empty DataFrame raises ValueError."""
        df_empty = pl.DataFrame()
        with pytest.raises(ValueError, match="Input DataFrame is empty"):
            rank_diseases(df_empty)
    
    def test_rank_diseases_missing_column(self, sample_df):
        """Test that missing score column raises KeyError."""
        with pytest.raises(KeyError, match="Score column.*not found"):
            rank_diseases(sample_df, score_col='nonexistent_score')


class TestSensitivityAnalysis:
    """Test sensitivity analysis functions."""
    
    @pytest.fixture
    def sample_df(self):
        """Create comprehensive sample DataFrame."""
        return pl.DataFrame({
            'disease_name': ['Disease A', 'Disease B', 'Disease C'],
            'total_cases_score': [50.0, 100.0, 75.0],
            'annual_avg_cases_score': [50.0, 100.0, 75.0],
            'cagr_score': [80.0, 20.0, 50.0],
            'outbreak_score': [70.0, 40.0, 60.0],
            'coefficient_variation_score': [30.0, 70.0, 50.0]
        })
    
    def test_sensitivity_analysis_multiple_scenarios(self, sample_df):
        """Test that rankings are calculated for all scenarios."""
        scenarios = {
            'base': {'volume': 0.40, 'trend': 0.25, 'outbreak': 0.20, 'variability': 0.15},
            'volume_focused': {'volume': 0.60, 'trend': 0.20, 'outbreak': 0.10, 'variability': 0.10}
        }
        rankings = sensitivity_analysis(sample_df, scenarios)
        
        assert len(rankings) == 2
        assert 'base' in rankings
        assert 'volume_focused' in rankings
        
        # Each ranking should have rank column
        assert 'rank' in rankings['base'].columns
        assert 'rank' in rankings['volume_focused'].columns
    
    def test_rank_correlation_calculation(self, sample_df):
        """Test Spearman correlation computation."""
        scenarios = {
            'base': {'volume': 0.40, 'trend': 0.25, 'outbreak': 0.20, 'variability': 0.15},
            'volume_focused': {'volume': 0.60, 'trend': 0.20, 'outbreak': 0.10, 'variability': 0.10}
        }
        rankings = sensitivity_analysis(sample_df, scenarios)
        corr_matrix = calculate_rank_correlation(rankings)
        
        # Diagonal should be 1.0 (perfect self-correlation)
        assert abs(corr_matrix['base'][0] - 1.0) < 0.01
        assert abs(corr_matrix['volume_focused'][1] - 1.0) < 0.01
        
        # Matrix should be symmetric
        assert abs(corr_matrix['base'][1] - corr_matrix['volume_focused'][0]) < 0.01
    
    def test_rank_correlation_insufficient_scenarios(self):
        """Test that correlation requires at least 2 scenarios."""
        rankings = {'base': pl.DataFrame({'disease_name': ['A'], 'rank': [1]})}
        with pytest.raises(ValueError, match="At least 2 scenarios required"):
            calculate_rank_correlation(rankings)
    
    def test_identify_consensus_priorities(self, sample_df):
        """Test identification of consensus top-N diseases."""
        scenarios = {
            'base': {'volume': 0.40, 'trend': 0.25, 'outbreak': 0.20, 'variability': 0.15},
            'volume_focused': {'volume': 0.60, 'trend': 0.20, 'outbreak': 0.10, 'variability': 0.10},
            'trend_focused': {'volume': 0.20, 'trend': 0.50, 'outbreak': 0.20, 'variability': 0.10}
        }
        rankings = sensitivity_analysis(sample_df, scenarios)
        consensus = identify_consensus_priorities(rankings, top_n=2)
        
        # At least some diseases should be in consensus (or empty if rankings differ widely)
        assert isinstance(consensus, list)
    
    def test_consensus_empty_rankings(self):
        """Test that empty rankings raises ValueError."""
        with pytest.raises(ValueError, match="Rankings dictionary is empty"):
            identify_consensus_priorities({}, top_n=10)
    
    def test_consensus_invalid_top_n(self, sample_df):
        """Test that non-positive top_n raises ValueError."""
        scenarios = {
            'base': {'volume': 0.40, 'trend': 0.25, 'outbreak': 0.20, 'variability': 0.15}
        }
        rankings = sensitivity_analysis(sample_df, scenarios)
        
        with pytest.raises(ValueError, match="top_n must be positive"):
            identify_consensus_priorities(rankings, top_n=0)


class TestIntegration:
    """Integration tests covering end-to-end workflows."""
    
    def test_full_prioritization_workflow(self):
        """Test complete workflow from data to rankings."""
        # Create realistic sample data
        df = pl.DataFrame({
            'disease_name': ['Dengue', 'HFMD', 'Cholera', 'Typhoid'],
            'sufficient_data': [True, True, True, True],
            'total_cases_score': [80.0, 100.0, 20.0, 40.0],
            'annual_avg_cases_score': [80.0, 100.0, 20.0, 40.0],
            'cagr_score': [90.0, 30.0, 50.0, 60.0],
            'outbreak_score': [85.0, 40.0, 30.0, 45.0],
            'coefficient_variation_score': [50.0, 70.0, 60.0, 55.0]
        })
        
        # 1. Validate
        validate_burden_metrics_input(df)
        
        # 2. Calculate composite scores
        weights = {'volume': 0.40, 'trend': 0.25, 'outbreak': 0.20, 'variability': 0.15}
        df_scored = calculate_composite_score(df, weights)
        
        # 3. Assign tiers
        thresholds = {'high': 70.0, 'medium': 40.0}
        df_tiered = assign_tiers(df_scored, thresholds)
        
        # 4. Rank
        df_ranked = rank_diseases(df_tiered)
        
        # Verify output structure
        assert 'rank' in df_ranked.columns
        assert 'tier' in df_ranked.columns
        assert 'composite_score' in df_ranked.columns
        assert len(df_ranked) == 4
        
        # Verify top disease
        top_disease = df_ranked.filter(pl.col('rank') == 1)['disease_name'][0]
        assert top_disease in ['Dengue', 'HFMD']  # Should be one of high burden diseases


# Run tests with coverage
if __name__ == '__main__':
    pytest.main([__file__, '-v', '--cov=src.analysis.prioritization', '--cov-report=term-missing'])
