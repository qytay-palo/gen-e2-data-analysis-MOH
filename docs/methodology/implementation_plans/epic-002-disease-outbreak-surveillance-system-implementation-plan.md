# Implementation Plan: EPIC-002 - Disease Outbreak Detection & Surveillance System

## Executive Summary

- **Epic**: EPIC-002 - Disease Outbreak Detection & Surveillance System
- **Objective**: Implement automated disease surveillance with anomaly detection algorithms and geographic clustering to identify potential outbreaks 7-14 days earlier than traditional methods
- **Estimated Duration**: 4-5 weeks (25 working days)
- **Dependencies**: None (can run parallel to EPIC-001)
- **Key Deliverables**: 
  - Monitor minimum 10 key diseases
  - Outbreak detection 7-14 days earlier
  - <5% false positive rate for alerts
  - Interactive disease risk maps
  - Minimum 5 significant disease clusters per quarter
  - Forecasting models with ≤15% MAPE
  - Real-time surveillance dashboard

---

## 1. Epic Folder Structure

```
epics/
└── epic-002/
    ├── README.md
    ├── config/
    │   ├── epic_002_config.yml
    │   ├── epic_002_params.yml
    │   ├── epic_002_queries.yml
    │   └── disease_mappings.yml
    ├── src/
    │   ├── __init__.py
    │   ├── extraction.py
    │   ├── features.py
    │   ├── analysis.py
    │   ├── anomaly_detection.py
    │   ├── spatial_clustering.py
    │   ├── forecasting.py
    │   ├── visualization.py
    │   └── utils.py
    ├── scripts/
    │   ├── 01_extract_data.py
    │   ├── 02_engineer_features.py
    │   ├── 03_establish_baselines.py
    │   ├── 04_detect_anomalies.py
    │   ├── 05_spatial_clustering.py
    │   ├── 06_build_forecasting_models.py
    │   ├── 07_generate_risk_scores.py
    │   ├── 08_generate_dashboard.py
    │   └── run_full_pipeline.py
    ├── notebooks/
    │   ├── 01_exploration.ipynb
    │   ├── 02_baseline_analysis.ipynb
    │   ├── 03_anomaly_detection.ipynb
    │   ├── 04_spatial_clustering.ipynb
    │   ├── 05_forecasting_models.ipynb
    │   └── 06_results_viz.ipynb
    ├── sql/
    │   ├── extraction_queries.sql
    │   ├── validation_queries.sql
    │   └── aggregation_queries.sql
    ├── tests/
    │   ├── __init__.py
    │   ├── test_extraction.py
    │   ├── test_anomaly_detection.py
    │   ├── test_forecasting.py
    │   └── test_integration.py
    ├── data/
    │   ├── raw/
    │   ├── processed/
    │   ├── features/
    │   └── baselines/
    ├── results/
    │   ├── metrics/
    │   ├── tables/
    │   ├── alerts/
    │   └── exports/
    ├── reports/
    │   ├── figures/
    │   ├── dashboards/
    │   └── documents/
    └── logs/
        ├── extraction.log
        ├── detection.log
        ├── pipeline.log
        └── errors.log
```

---

## 2. Module Specifications

### 2.1 Data Extraction & Loading

#### Module: `epics/epic-002/src/extraction.py`

**Purpose**: Extract and unify disease surveillance data from multiple sources

**Data Sources**:
- `principal-causes-of-death` - Mortality data
- `communicable-diseases-quarterly-crude-rates` - Quarterly disease surveillance
- `reportable-infectious-diseases` - Annual reportable diseases

**Key Functions**:

```python
from typing import Dict, List
import pandas as pd
import kagglehub
from pathlib import Path
import logging

class DiseaseDataExtractor:
    """Extract disease surveillance data from Kaggle dataset"""
    
    def __init__(self, dataset_id: str = "subhamjain/health-dataset-complete-singapore"):
        self.dataset_id = dataset_id
        self.dataset_path = None
        self.logger = logging.getLogger(__name__)
    
    def download_dataset(self) -> Path:
        """Download dataset (cached locally)"""
        self.logger.info(f"Downloading dataset: {self.dataset_id}")
        self.dataset_path = Path(kagglehub.dataset_download(self.dataset_id))
        return self.dataset_path
    
    def extract_mortality_data(self, year_range: tuple = (2003, 2020)) -> pd.DataFrame:
        """Extract principal causes of death"""
        table_name = "principal-causes-of-death"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1]) &
            (df['deaths_no'].notna())
        ]
        
        df['data_source'] = 'mortality'
        self.logger.info(f"Extracted {len(df)} mortality records")
        return df
    
    def extract_quarterly_surveillance(self, year_range: tuple = (2003, 2020)) -> pd.DataFrame:
        """Extract quarterly communicable disease data"""
        table_name = "communicable-diseases-quarterly-crude-rates"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1]) &
            (df['cases'].notna())
        ]
        
        df['data_source'] = 'surveillance_quarterly'
        self.logger.info(f"Extracted {len(df)} quarterly surveillance records")
        return df
    
    def extract_infectious_diseases(self, year_range: tuple = (2004, 2020)) -> pd.DataFrame:
        """Extract reportable infectious diseases"""
        table_name = "reportable-infectious-diseases"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1]) &
            (df['cases_no'].notna())
        ]
        
        df['data_source'] = 'reportable_diseases'
        self.logger.info(f"Extracted {len(df)} infectious disease records")
        return df
    
    def unify_disease_data(
        self, 
        mortality_df: pd.DataFrame,
        quarterly_df: pd.DataFrame,
        infectious_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Create unified disease dataset"""
        # Standardize column names
        mortality_df = mortality_df.rename(columns={
            'cause_of_death': 'disease',
            'deaths_no': 'cases'
        })
        
        infectious_df = infectious_df.rename(columns={
            'cases_no': 'cases'
        })
        
        quarterly_df = quarterly_df.rename(columns={
            'disease_type': 'disease'
        })
        
        # Concatenate all sources
        unified_df = pd.concat([
            mortality_df[['year', 'disease', 'cases', 'data_source']],
            quarterly_df[['year', 'quarter', 'disease', 'cases', 'crude_rate', 'data_source']],
            infectious_df[['year', 'disease', 'cases', 'data_source']]
        ], ignore_index=True)
        
        self.logger.info(f"Created unified dataset with {len(unified_df)} records")
        return unified_df
    
    def extract_all(self) -> pd.DataFrame:
        """Extract and unify all disease data"""
        if not self.dataset_path:
            self.download_dataset()
        
        mortality_df = self.extract_mortality_data()
        quarterly_df = self.extract_quarterly_surveillance()
        infectious_df = self.extract_infectious_diseases()
        
        return self.unify_disease_data(mortality_df, quarterly_df, infectious_df)
```

---

### 2.2 Feature Engineering & Transformation

#### Module: `epics/epic-002/src/features.py`

**Purpose**: Standardize disease names, calculate crude rates, create temporal features

**Key Functions**:

```python
import pandas as pd
import numpy as np
import yaml
from typing import Dict
import logging

class DiseaseFeatureEngineer:
    """Engineer features for disease surveillance"""
    
    def __init__(self, mapping_file: str = 'config/disease_mappings.yml'):
        self.logger = logging.getLogger(__name__)
        self.disease_mappings = self._load_disease_mappings(mapping_file)
    
    def _load_disease_mappings(self, mapping_file: str) -> dict:
        """Load disease name standardization mappings"""
        with open(mapping_file, 'r') as f:
            return yaml.safe_load(f)
    
    def standardize_disease_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize disease names across sources"""
        def map_disease(disease_name):
            disease_lower = str(disease_name).lower().strip()
            if disease_lower in self.disease_mappings:
                return self.disease_mappings[disease_lower]['standard_name']
            return disease_name.title()
        
        df['disease_standard'] = df['disease'].apply(map_disease)
        
        # Add disease category
        def get_category(disease_name):
            disease_lower = str(disease_name).lower().strip()
            if disease_lower in self.disease_mappings:
                return self.disease_mappings[disease_lower].get('category', 'Other')
            return 'Other'
        
        df['disease_category'] = df['disease'].apply(get_category)
        
        self.logger.info(f"Standardized {df['disease_standard'].nunique()} unique diseases")
        return df
    
    def calculate_crude_rates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate crude rates (per 100,000 population) where missing"""
        # Singapore population by year (approximate)
        singapore_population = {
            2003: 4114826, 2004: 4166664, 2005: 4265762,
            2006: 4401365, 2007: 4588599, 2008: 4839396,
            2009: 4987573, 2010: 5076732, 2011: 5183688,
            2012: 5312400, 2013: 5399162, 2014: 5469724,
            2015: 5535002, 2016: 5607283, 2017: 5612253,
            2018: 5638676, 2019: 5703569, 2020: 5685807
        }
        
        df['population'] = df['year'].map(singapore_population)
        
        # Calculate crude rate if not present
        if 'crude_rate' not in df.columns or df['crude_rate'].isna().any():
            df['crude_rate'] = (df['cases'] / df['population']) * 100000
        
        return df
    
    def create_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create temporal features"""
        # Handle quarterly vs annual data
        df['quarter'] = df['quarter'].fillna(0).astype(int)
        
        # Create year_quarter field
        df['year_quarter'] = df.apply(
            lambda row: f"{row['year']}-Q{row['quarter']}" if row['quarter'] > 0 else f"{row['year']}-Annual",
            axis=1
        )
        
        # Create date field
        quarter_month_map = {1: '01', 2: '04', 3: '07', 4: '10', 0: '01'}
        df['month'] = df['quarter'].map(quarter_month_map)
        df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'] + '-01')
        
        # Days since epoch for modeling
        df['days_since_epoch'] = (df['date'] - pd.Timestamp('2000-01-01')).dt.days
        
        return df
    
    def engineer_all_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Run complete feature engineering pipeline"""
        df = self.standardize_disease_names(df)
        df = self.calculate_crude_rates(df)
        df = self.create_temporal_features(df)
        
        return df
```

---

### 2.3 Anomaly Detection

#### Module: `epics/epic-002/src/anomaly_detection.py`

**Purpose**: Implement anomaly detection algorithms for outbreak detection

**Key Algorithms**:
- Z-score method
- CUSUM (Cumulative Sum Control Chart)
- EWMA (Exponentially Weighted Moving Average)
- Isolation Forest (ML-based)

**Key Functions**:

```python
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import IsolationForest
import logging

class OutbreakDetector:
    """Detect disease outbreak anomalies"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def establish_baseline(
        self, 
        df: pd.DataFrame, 
        disease: str,
        baseline_years: int = 5
    ) -> Dict:
        """Establish statistical baseline for a disease"""
        disease_data = df[df['disease_standard'] == disease].copy()
        disease_data = disease_data.sort_values('date')
        
        # Use historical years for baseline
        baseline_data = disease_data[
            disease_data['year'] <= (disease_data['year'].max() - baseline_years)
        ]
        
        baseline = {
            'disease': disease,
            'mean': baseline_data['cases'].mean(),
            'std': baseline_data['cases'].std(),
            'median': baseline_data['cases'].median(),
            'q25': baseline_data['cases'].quantile(0.25),
            'q75': baseline_data['cases'].quantile(0.75),
            'threshold_95': baseline_data['cases'].mean() + 1.96 * baseline_data['cases'].std(),
            'threshold_99': baseline_data['cases'].mean() + 2.58 * baseline_data['cases'].std()
        }
        
        return baseline
    
    def detect_anomalies_zscore(
        self, 
        df: pd.DataFrame,
        baseline: Dict,
        threshold: float = 2.0
    ) -> pd.DataFrame:
        """Detect anomalies using Z-score method"""
        df = df.copy()
        
        # Calculate Z-scores
        df['zscore'] = (df['cases'] - baseline['mean']) / baseline['std']
        
        # Flag anomalies
        df['is_anomaly_zscore'] = df['zscore'].abs() > threshold
        
        # Calculate severity (how many standard deviations above baseline)
        df['severity_zscore'] = df['zscore'].apply(lambda x: max(0, x))
        
        return df
    
    def detect_anomalies_cusum(
        self,
        df: pd.DataFrame,
        baseline: Dict,
        threshold: float = 5.0
    ) -> pd.DataFrame:
        """Detect anomalies using CUSUM method"""
        df = df.copy()
        df = df.sort_values('date')
        
        # Calculate cumulative sum of deviations from mean
        df['deviation'] = df['cases'] - baseline['mean']
        df['cusum'] = df['deviation'].cumsum()
        
        # Reset CUSUM when it goes negative
        df['cusum'] = df['cusum'].clip(lower=0)
        
        # Flag anomalies when CUSUM exceeds threshold
        df['is_anomaly_cusum'] = df['cusum'] > threshold * baseline['std']
        
        return df
    
    def detect_anomalies_isolation_forest(
        self,
        df: pd.DataFrame,
        contamination: float = 0.05
    ) -> pd.DataFrame:
        """Detect anomalies using Isolation Forest (ML-based)"""
        df = df.copy()
        
        # Prepare features for Isolation Forest
        features = df[['cases', 'days_since_epoch']].values
        
        # Train Isolation Forest
        clf = IsolationForest(contamination=contamination, random_state=42)
        df['is_anomaly_ml'] = clf.fit_predict(features) == -1
        df['anomaly_score_ml'] = clf.score_samples(features)
        
        return df
    
    def generate_alerts(
        self,
        df: pd.DataFrame,
        min_severity: float = 2.0
    ) -> pd.DataFrame:
        """Generate outbreak alerts"""
        # Combine multiple detection methods
        df['alert_count'] = (
            df['is_anomaly_zscore'].astype(int) +
            df['is_anomaly_cusum'].astype(int) +
            df['is_anomaly_ml'].astype(int)
        )
        
        # Generate alert if 2+ methods detect anomaly
        df['is_outbreak_alert'] = df['alert_count'] >= 2
        
        # Filter to significant alerts
        alerts = df[
            (df['is_outbreak_alert']) &
            (df['severity_zscore'] >= min_severity)
        ].copy()
        
        alerts = alerts.sort_values('severity_zscore', ascending=False)
        
        self.logger.info(f"Generated {len(alerts)} outbreak alerts")
        return alerts
```

---

## 3. Configuration Files

### `epics/epic-002/config/epic_002_config.yml`

```yaml
epic_id: epic-002
epic_name: disease-outbreak-surveillance-system

data_sources:
  primary_source: kaggle
  dataset_id: "subhamjain/health-dataset-complete-singapore"
  
  tables:
    - principal-causes-of-death
    - communicable-diseases-quarterly-crude-rates
    - reportable-infectious-diseases

year_range:
  start: 2003
  end: 2020

priority_diseases:
  - Tuberculosis
  - Dengue Fever
  - Influenza
  - Pneumonia
  - COVID-19
  - Hand Foot Mouth Disease
  - Malaria
  - Chickenpox
  - Measles
  - Hepatitis

output_paths:
  raw_data: epics/epic-002/data/raw/
  processed_data: epics/epic-002/data/processed/
  baselines: epics/epic-002/data/baselines/
  alerts: epics/epic-002/results/alerts/
  results: epics/epic-002/results/
  figures: epics/epic-002/reports/figures/

logging:
  level: INFO
  log_dir: epics/epic-002/logs/
```

### `epics/epic-002/config/epic_002_params.yml`

```yaml
# Analysis parameters for EPIC-002

baseline_estimation:
  lookback_years: 5
  confidence_levels: [95, 99]

anomaly_detection:
  zscore_threshold: 2.0
  cusum_threshold: 5.0
  ml_contamination: 0.05
  min_severity_for_alert: 2.0
  alert_consensus_threshold: 2  # Require 2+ methods to agree

forecasting:
  train_test_split: 0.8
  forecast_horizons: [7, 14, 30, 90]  # days
  max_mape_threshold: 15  # Maximum acceptable MAPE

spatial_clustering:
  algorithm: 'DBSCAN'
  eps: 0.1  # Distance threshold
  min_samples: 3

alert_thresholds:
  low: 2.0  # z-score
  medium: 3.0
  high: 4.0
  critical: 5.0
```

### `epics/epic-002/config/disease_mappings.yml`

```yaml
tuberculosis:
  standard_name: "Tuberculosis"
  icd10: "A15-A19"
  category: "Respiratory"

dengue:
  standard_name: "Dengue Fever"
  icd10: "A90"
  category: "Vector-Borne"

influenza:
  standard_name: "Influenza"
  icd10: "J09-J11"
  category: "Respiratory"

pneumonia:
  standard_name: "Pneumonia"
  icd10: "J12-J18"
  category: "Respiratory"

hand foot mouth disease:
  standard_name: "Hand, Foot and Mouth Disease"
  icd10: "B08.4"
  category: "Viral"

# Add more disease mappings...
```

---

## 4. Execution Workflow

### Step-by-Step Commands

```bash
cd epics/epic-002/

# Step 1: Extract disease data
python scripts/01_extract_data.py

# Step 2: Engineer features
python scripts/02_engineer_features.py

# Step 3: Establish baselines
python scripts/03_establish_baselines.py

# Step 4: Detect anomalies
python scripts/04_detect_anomalies.py

# Step 5: Spatial clustering
python scripts/05_spatial_clustering.py

# Step 6: Build forecasting models
python scripts/06_build_forecasting_models.py

# Step 7: Generate risk scores
python scripts/07_generate_risk_scores.py

# Step 8: Generate dashboard
python scripts/08_generate_dashboard.py

# OR run entire pipeline
python scripts/run_full_pipeline.py
```

---

## 5. Testing Strategy

### Unit Tests

```python
# epics/epic-002/tests/test_anomaly_detection.py

import pytest
import pandas as pd
import numpy as np
from src.anomaly_detection import OutbreakDetector

def test_establish_baseline():
    """Test baseline calculation"""
    detector = OutbreakDetector()
    
    # Create sample data
    df = pd.DataFrame({
        'disease_standard': ['Dengue'] * 100,
        'year': list(range(2010, 2020)) * 10,
        'cases': np.random.normal(100, 20, 100),
        'date': pd.date_range('2010-01-01', periods=100, freq='M')
    })
    
    baseline = detector.establish_baseline(df, 'Dengue', baseline_years=5)
    
    assert 'mean' in baseline
    assert 'std' in baseline
    assert baseline['mean'] > 0

def test_detect_anomalies_zscore():
    """Test Z-score anomaly detection"""
    detector = OutbreakDetector()
    
    baseline = {
        'mean': 100,
        'std': 20
    }
    
    df = pd.DataFrame({
        'cases': [100, 150, 200, 90]  # 200 is clearly anomalous
    })
    
    result = detector.detect_anomalies_zscore(df, baseline, threshold=2.0)
    
    assert 'is_anomaly_zscore' in result.columns
    assert result.iloc[2]['is_anomaly_zscore'] == True  # 200 cases
```

### Running Tests

```bash
cd epics/epic-002/
pytest tests/ -v --cov=src
```

---

## 6. Outputs & Deliverables

### Analysis Results

**Location**: `epics/epic-002/results/`

**Files**:
- `baselines/disease_baselines.csv` - Statistical baselines for all monitored diseases
- `alerts/outbreak_alerts_2020.csv` - Generated outbreak alerts
- `tables/anomaly_detection_summary.csv` - Summary of detected anomalies
- `tables/disease_forecasts.csv` - Forecasted case counts
- `metrics/model_performance.json` - Forecasting model accuracy metrics

### Visualizations

**Location**: `epics/epic-002/reports/figures/`

**Files**:
- `disease_trends_dashboard.html` - Interactive time series dashboard
- `outbreak_alerts_map.html` - Geographic map of outbreak clusters
- `risk_heatmap.html` - Disease risk heatmap
- `forecast_accuracy.png` - Model performance charts

---

## 7. Dependencies & Integration

### Upstream Dependencies
- None (can run parallel to other epics)

### Downstream Consumers
- Policy recommendations (EPIC-003)

### Shared Components
- `kaggle_base_extraction`
- `disease_name_standardization`
- `temporal_feature_engineering`
- `anomaly_detection`
- `forecasting_pipeline`

---

## 8. Timeline & Milestones

| Week | Days | Milestone | Deliverables |
|------|------|-----------|--------------|
| 1 | 1-4 | Data extraction and baseline establishment | Unified disease dataset, baselines |
| 2 | 5-9 | Anomaly detection implementation | Outbreak alerts generated |
| 3 | 10-14 | Spatial clustering and forecasting | Cluster maps, forecasting models |
| 4 | 15-19 | Risk scoring system | Risk scores for all diseases |
| 5 | 20-25 | Dashboard and reporting | Real-time surveillance dashboard |

**Total Duration**: 25 working days (5 weeks)

---

## 9. Success Criteria

✅ **Detection Performance**:
- [ ] Monitor minimum 10 key diseases
- [ ] Achieve <5% false positive rate
- [ ] Detect outbreaks 7-14 days earlier

✅ **Forecasting Accuracy**:
- [ ] MAPE ≤15% for 1-month forecasts
- [ ] Confidence intervals calculated

✅ **Spatial Analysis**:
- [ ] Identify minimum 5 disease clusters per quarter

✅ **Deliverables**:
- [ ] Real-time surveillance dashboard deployed
- [ ] Automated alert system functional
- [ ] Documentation and user guides complete

---

**Document Version**: 1.0  
**Last Updated**: 2 February 2026  
**Owner**: EPIC-002 Lead Data Scientist
