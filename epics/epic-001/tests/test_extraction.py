"""
Epic 001: Test Data Extraction Module
"""

import pytest
import pandas as pd
from pathlib import Path
import sys

# Add src to path
epic_root = Path(__file__).parent.parent
sys.path.insert(0, str(epic_root / 'src'))

from extraction import FacilityDataExtractor


class TestFacilityDataExtractor:
    """Test suite for FacilityDataExtractor"""
    
    def test_extractor_initialization(self):
        """Test extractor initializes correctly"""
        extractor = FacilityDataExtractor()
        assert extractor.dataset_id == "subhamjain/health-dataset-complete-singapore"
        assert extractor.dataset_path is None
    
    def test_validate_extracted_data_valid(self):
        """Test data validation with valid data"""
        extractor = FacilityDataExtractor()
        
        # Create sample valid data
        df = pd.DataFrame({
            'year': [2020, 2021],
            'hospital': ['Hospital A', 'Hospital B'],
            'attendances_no': [1000, 2000]
        })
        
        required_columns = ['year', 'hospital', 'attendances_no']
        result = extractor.validate_extracted_data(df, required_columns)
        assert result == True
    
    def test_validate_extracted_data_missing_columns(self):
        """Test data validation with missing columns"""
        extractor = FacilityDataExtractor()
        
        # Create sample data with missing column
        df = pd.DataFrame({
            'year': [2020, 2021],
            'hospital': ['Hospital A', 'Hospital B']
        })
        
        required_columns = ['year', 'hospital', 'attendances_no']
        
        with pytest.raises(ValueError, match="Missing required columns"):
            extractor.validate_extracted_data(df, required_columns)
    
    def test_validate_extracted_data_empty(self):
        """Test data validation with empty DataFrame"""
        extractor = FacilityDataExtractor()
        
        df = pd.DataFrame()
        required_columns = ['year', 'hospital']
        
        with pytest.raises(ValueError, match="empty"):
            extractor.validate_extracted_data(df, required_columns)


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


def test_sample_data_fixtures(sample_attendance_data, sample_beds_data):
    """Test that fixtures provide valid data"""
    assert len(sample_attendance_data) == 6
    assert len(sample_beds_data) == 6
    assert 'hospital' in sample_attendance_data.columns
    assert 'beds_no' in sample_beds_data.columns
