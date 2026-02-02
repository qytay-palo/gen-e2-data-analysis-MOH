# Implementation Plan: EPIC-001 - Facility Utilization & Bottleneck Analysis

## Executive Summary

- **Epic**: EPIC-001 - Facility Utilization & Bottleneck Analysis
- **Objective**: Analyze patient distribution patterns, service utilization rates, and process bottlenecks across Singapore's healthcare network to enable evidence-based resource allocation and operational improvements
- **Estimated Duration**: 2-3 weeks (15 working days)
- **Dependencies**: None (foundational epic)
- **Key Deliverables**: 
  - Facility performance profiles for 100% of facilities
  - Minimum 10 critical bottleneck identifications with quantified impact
  - Severity scoring framework
  - Root cause analysis reports
  - Actionable improvement recommendations
  - Interactive utilization dashboard

---

## 1. Epic Folder Structure

```
epics/
└── epic-001/
    ├── README.md
    ├── config/
    │   ├── epic_001_config.yml
    │   ├── epic_001_params.yml
    │   └── epic_001_queries.yml
    ├── src/
    │   ├── __init__.py
    │   ├── extraction.py
    │   ├── features.py
    │   ├── analysis.py
    │   ├── visualization.py
    │   └── utils.py
    ├── scripts/
    │   ├── 01_extract_data.py
    │   ├── 02_engineer_features.py
    │   ├── 03_run_analysis.py
    │   ├── 04_generate_visualizations.py
    │   ├── 05_generate_reports.py
    │   └── run_full_pipeline.py
    ├── notebooks/
    │   ├── 01_exploration.ipynb
    │   ├── 02_feature_analysis.ipynb
    │   ├── 03_modeling.ipynb
    │   └── 04_results_viz.ipynb
    ├── sql/
    │   ├── extraction_queries.sql
    │   ├── validation_queries.sql
    │   └── aggregation_queries.sql
    ├── tests/
    │   ├── __init__.py
    │   ├── test_extraction.py
    │   ├── test_features.py
    │   ├── test_analysis.py
    │   └── test_integration.py
    ├── data/
    │   ├── raw/
    │   ├── processed/
    │   └── features/
    ├── results/
    │   ├── metrics/
    │   ├── tables/
    │   └── exports/
    ├── reports/
    │   ├── figures/
    │   ├── dashboards/
    │   └── documents/
    └── logs/
        ├── extraction.log
        ├── pipeline.log
        └── errors.log
```

---

## 2. Module Specifications

### 2.1 Data Extraction & Loading

#### Module: `epics/epic-001/src/extraction.py`

**Purpose**: Extract and validate facility utilization data from Kaggle dataset

**Data Sources**: 
- `admission-and-outpatient-attendances-by-restructured-hospitals`
- `admission-and-outpatient-attendances`
- `number-of-hospital-beds`
- `facilities-in-the-registry-of-medical-clinics-and-dental-clinics`

**Key Functions**:

```python
from typing import Dict, List, Tuple
import pandas as pd
import kagglehub
from pathlib import Path
import logging

class FacilityDataExtractor:
    """Extract facility utilization data from Kaggle dataset"""
    
    def __init__(self, dataset_id: str = "subhamjain/health-dataset-complete-singapore"):
        self.dataset_id = dataset_id
        self.dataset_path = None
        self.logger = logging.getLogger(__name__)
    
    def download_dataset(self) -> Path:
        """Download entire dataset (cached locally)"""
        self.logger.info(f"Downloading dataset: {self.dataset_id}")
        self.dataset_path = Path(kagglehub.dataset_download(self.dataset_id))
        return self.dataset_path
    
    def extract_attendance_data(self, year_range: Tuple[int, int] = (2006, 2020)) -> pd.DataFrame:
        """Extract hospital attendance data"""
        table_name = "admission-and-outpatient-attendances-by-restructured-hospitals"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1]) &
            (df['attendances_no'].notna())
        ]
        
        self.logger.info(f"Extracted {len(df)} attendance records")
        return df
    
    def extract_bed_capacity_data(self, year_range: Tuple[int, int] = (2009, 2020)) -> pd.DataFrame:
        """Extract hospital bed capacity data"""
        table_name = "number-of-hospital-beds"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1]) &
            (df['beds_no'] > 0)
        ]
        
        self.logger.info(f"Extracted {len(df)} bed capacity records")
        return df
    
    def extract_clinic_registry(self) -> pd.DataFrame:
        """Extract clinic registry data"""
        table_name = "facilities-in-the-registry-of-medical-clinics-and-dental-clinics"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        self.logger.info(f"Extracted {len(df)} clinic records")
        return df
    
    def validate_extracted_data(self, df: pd.DataFrame, required_columns: List[str]) -> bool:
        """Validate that extracted data meets requirements"""
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            self.logger.error(f"Missing required columns: {missing_cols}")
            return False
        
        if len(df) == 0:
            self.logger.error("Extracted dataframe is empty")
            return False
        
        return True
    
    def extract_all(self) -> Dict[str, pd.DataFrame]:
        """Extract all required tables"""
        if not self.dataset_path:
            self.download_dataset()
        
        return {
            'attendance_by_hospitals': self.extract_attendance_data(),
            'bed_capacity': self.extract_bed_capacity_data(),
            'clinic_registry': self.extract_clinic_registry()
        }
```

**Extraction Logic**:
1. Download Kaggle dataset using kagglehub API
2. Load specific CSV tables
3. Apply filters (year range, null checks)
4. Validate data quality
5. Return cleaned DataFrames

**Validation Rules**:
- Year range: 2006-2020
- No null values in critical fields (attendances_no, beds_no)
- Positive values for capacity metrics
- Required columns present in each table

---

### 2.2 Feature Engineering & Transformation

#### Module: `epics/epic-001/src/features.py`

**Purpose**: Calculate utilization rates, performance metrics, and bottleneck indicators

**Key Functions**:

```python
import pandas as pd
import numpy as np
from typing import Dict, List
import logging

class UtilizationFeatureEngineer:
    """Engineer features for facility utilization analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def standardize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize DataFrame column names"""
        df.columns = (
            df.columns
            .str.lower()
            .str.replace(' ', '_')
            .str.replace('-', '_')
            .str.replace('[^a-z0-9_]', '', regex=True)
        )
        return df
    
    def calculate_utilization_rate(
        self, 
        attendances_df: pd.DataFrame, 
        beds_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate utilization rates
        
        Formula: utilization_rate = (actual_attendances / capacity) × 100
        """
        # Merge attendance and capacity data
        merged = pd.merge(
            attendances_df,
            beds_df,
            on=['year', 'hospital'],
            how='inner'
        )
        
        # Calculate daily capacity (beds × 365 days)
        merged['annual_capacity'] = merged['beds_no'] * 365
        
        # Calculate utilization rate
        merged['utilization_rate_pct'] = (
            merged['attendances_no'] / merged['annual_capacity'] * 100
        )
        
        # Cap at 100% for reporting purposes
        merged['utilization_rate_capped'] = merged['utilization_rate_pct'].clip(upper=100)
        
        self.logger.info(f"Calculated utilization rates for {len(merged)} facility-years")
        return merged
    
    def categorize_utilization_level(self, utilization_rate: float) -> str:
        """Categorize utilization into performance tiers"""
        if utilization_rate < 50:
            return 'Underutilized'
        elif utilization_rate < 70:
            return 'Optimal'
        elif utilization_rate < 90:
            return 'High Utilization'
        else:
            return 'Overutilized'
    
    def calculate_facility_percentiles(self, df: pd.DataFrame, metric_col: str) -> pd.DataFrame:
        """Calculate percentile rankings for facilities"""
        df[f'{metric_col}_percentile'] = df[metric_col].rank(pct=True) * 100
        
        # Assign performance tier
        df['performance_tier'] = df[f'{metric_col}_percentile'].apply(
            lambda x: 'Top Performer' if x >= 90 else
                     'High Performer' if x >= 75 else
                     'Average Performer' if x >= 25 else
                     'Below Average' if x >= 10 else
                     'Low Performer'
        )
        
        return df
    
    def identify_bottlenecks(self, df: pd.DataFrame, threshold: float = 90.0) -> pd.DataFrame:
        """Identify facilities operating at bottleneck levels"""
        bottlenecks = df[df['utilization_rate_pct'] >= threshold].copy()
        
        # Calculate severity score
        bottlenecks['severity_score'] = (
            (bottlenecks['utilization_rate_pct'] - threshold) * 
            bottlenecks['attendances_no'] / 1000
        )
        
        # Sort by severity
        bottlenecks = bottlenecks.sort_values('severity_score', ascending=False)
        
        self.logger.info(f"Identified {len(bottlenecks)} bottleneck facilities")
        return bottlenecks
    
    def create_temporal_features(self, df: pd.DataFrame, date_col: str = 'year') -> pd.DataFrame:
        """Create temporal features for time series analysis"""
        df['year_month'] = pd.to_datetime(df[date_col].astype(str) + '-01-01')
        df['days_since_epoch'] = (df['year_month'] - pd.Timestamp('2000-01-01')).dt.days
        df['is_recent'] = df[date_col] >= 2015
        
        return df
    
    def engineer_all_features(
        self, 
        attendances_df: pd.DataFrame, 
        beds_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Run complete feature engineering pipeline"""
        # Standardize columns
        attendances_df = self.standardize_column_names(attendances_df)
        beds_df = self.standardize_column_names(beds_df)
        
        # Calculate utilization rates
        utilization_df = self.calculate_utilization_rate(attendances_df, beds_df)
        
        # Add performance tiers
        utilization_df = self.calculate_facility_percentiles(
            utilization_df, 
            'utilization_rate_pct'
        )
        
        # Add temporal features
        utilization_df = self.create_temporal_features(utilization_df)
        
        # Add utilization category
        utilization_df['utilization_category'] = utilization_df['utilization_rate_pct'].apply(
            self.categorize_utilization_level
        )
        
        return utilization_df
```

---

### 2.3 Analysis & Modeling

#### Module: `epics/epic-001/src/analysis.py`

**Purpose**: Perform facility performance profiling, bottleneck detection, and root cause analysis

**Key Functions**:

```python
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple
import logging

class FacilityAnalyzer:
    """Analyze facility performance and bottlenecks"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def profile_facility_performance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate comprehensive facility performance profiles"""
        profiles = df.groupby('hospital').agg({
            'attendances_no': ['sum', 'mean', 'std'],
            'beds_no': 'mean',
            'utilization_rate_pct': ['mean', 'min', 'max', 'std'],
            'year': 'count'
        }).reset_index()
        
        # Flatten column names
        profiles.columns = ['_'.join(col).strip('_') for col in profiles.columns.values]
        
        # Rename for clarity
        profiles.rename(columns={
            'hospital_': 'hospital',
            'year_count': 'years_in_dataset'
        }, inplace=True)
        
        self.logger.info(f"Generated profiles for {len(profiles)} facilities")
        return profiles
    
    def detect_bottlenecks(
        self, 
        df: pd.DataFrame, 
        min_severity: int = 5
    ) -> pd.DataFrame:
        """Detect and quantify operational bottlenecks"""
        # Filter to recent years for current bottlenecks
        recent_df = df[df['is_recent'] == True].copy()
        
        # Identify overutilized facilities
        bottlenecks = recent_df[
            recent_df['utilization_rate_pct'] >= 90
        ].copy()
        
        # Calculate impact metrics
        bottlenecks['excess_demand'] = (
            bottlenecks['attendances_no'] - 
            bottlenecks['annual_capacity'] * 0.85  # Assume 85% is optimal
        )
        
        bottlenecks['patients_affected_annually'] = bottlenecks['excess_demand']
        
        # Calculate severity score
        bottlenecks['severity_score'] = (
            bottlenecks['utilization_rate_pct'] - 90
        ) * np.log1p(bottlenecks['attendances_no'])
        
        # Filter by minimum severity
        bottlenecks = bottlenecks[
            bottlenecks['severity_score'] >= min_severity
        ].sort_values('severity_score', ascending=False)
        
        self.logger.info(f"Detected {len(bottlenecks)} critical bottlenecks")
        return bottlenecks
    
    def root_cause_analysis(
        self, 
        bottleneck: pd.Series, 
        historical_df: pd.DataFrame
    ) -> Dict[str, any]:
        """Perform root cause analysis for a specific bottleneck"""
        hospital = bottleneck['hospital']
        
        # Get historical trend for this hospital
        hospital_history = historical_df[
            historical_df['hospital'] == hospital
        ].sort_values('year')
        
        # Calculate growth rate
        if len(hospital_history) >= 2:
            years = hospital_history['year'].values
            utilization = hospital_history['utilization_rate_pct'].values
            
            slope, intercept, r_value, p_value, std_err = stats.linregress(years, utilization)
            annual_growth_rate = slope
        else:
            annual_growth_rate = None
        
        # Identify potential causes
        causes = []
        
        if annual_growth_rate and annual_growth_rate > 2:
            causes.append({
                'cause': 'Rapid demand growth',
                'evidence': f'Utilization growing at {annual_growth_rate:.2f}% per year',
                'priority': 'HIGH'
            })
        
        if bottleneck['beds_no'] < hospital_history['beds_no'].median():
            causes.append({
                'cause': 'Insufficient capacity',
                'evidence': f"Current beds ({bottleneck['beds_no']}) below historical median",
                'priority': 'HIGH'
            })
        
        return {
            'hospital': hospital,
            'current_utilization': bottleneck['utilization_rate_pct'],
            'annual_growth_rate': annual_growth_rate,
            'root_causes': causes,
            'years_analyzed': len(hospital_history)
        }
    
    def benchmark_against_peers(
        self, 
        df: pd.DataFrame, 
        facility_id: str
    ) -> Dict[str, float]:
        """Benchmark a facility against peer facilities"""
        facility_data = df[df['hospital'] == facility_id]['utilization_rate_pct'].mean()
        peer_avg = df['utilization_rate_pct'].mean()
        peer_median = df['utilization_rate_pct'].median()
        
        return {
            'facility_utilization': facility_data,
            'peer_average': peer_avg,
            'peer_median': peer_median,
            'gap_vs_average': facility_data - peer_avg,
            'percentile_rank': (df['utilization_rate_pct'] < facility_data).sum() / len(df) * 100
        }
    
    def generate_recommendations(self, bottleneck_df: pd.DataFrame) -> List[Dict]:
        """Generate improvement recommendations for bottlenecks"""
        recommendations = []
        
        for idx, row in bottleneck_df.iterrows():
            rec = {
                'hospital': row['hospital'],
                'current_utilization': row['utilization_rate_pct'],
                'recommendation_type': None,
                'recommendation_text': None,
                'expected_impact': None,
                'implementation_complexity': None
            }
            
            if row['utilization_rate_pct'] > 95:
                rec['recommendation_type'] = 'Capacity Expansion'
                rec['recommendation_text'] = f"Increase bed capacity by {int((row['utilization_rate_pct'] - 85) / 85 * row['beds_no'])} beds"
                rec['expected_impact'] = 'Reduce utilization to 85%'
                rec['implementation_complexity'] = 'HIGH'
            elif row['utilization_rate_pct'] > 90:
                rec['recommendation_type'] = 'Process Optimization'
                rec['recommendation_text'] = "Optimize patient flow and discharge processes"
                rec['expected_impact'] = 'Reduce utilization by 5-10%'
                rec['implementation_complexity'] = 'MEDIUM'
            
            recommendations.append(rec)
        
        return recommendations
```

---

### 2.4 Visualization & Reporting

#### Module: `epics/epic-001/src/visualization.py`

**Purpose**: Create visualizations and interactive dashboard

**Key Functions**:

```python
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List
import logging

# Standard MOH color palette
MOH_COLORS = {
    'primary': '#003366',
    'secondary': '#0066CC',
    'accent': '#FF6600',
    'success': '#00CC66',
    'warning': '#FFCC00',
    'danger': '#CC0000',
    'neutral': '#666666'
}

class UtilizationVisualizer:
    """Create visualizations for utilization analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.template = self._create_template()
    
    def _create_template(self):
        """Create standard Plotly template"""
        return go.layout.Template(
            layout=go.Layout(
                font={'family': 'Arial, sans-serif', 'size': 12},
                title={'font': {'size': 18, 'color': MOH_COLORS['primary']}},
                paper_bgcolor='white',
                plot_bgcolor='#F5F5F5'
            )
        )
    
    def plot_utilization_trend(
        self, 
        df: pd.DataFrame, 
        facility_id: str = None
    ) -> go.Figure:
        """Plot utilization trend over time"""
        if facility_id:
            plot_df = df[df['hospital'] == facility_id]
            title = f"Utilization Trend: {facility_id}"
        else:
            # Aggregate across all facilities
            plot_df = df.groupby('year')['utilization_rate_pct'].mean().reset_index()
            title = "Average Utilization Trend (All Facilities)"
        
        fig = px.line(
            plot_df,
            x='year',
            y='utilization_rate_pct',
            title=title,
            labels={'utilization_rate_pct': 'Utilization Rate (%)', 'year': 'Year'},
            template=self.template
        )
        
        # Add optimal range
        fig.add_hrect(
            y0=70, y1=85,
            fillcolor=MOH_COLORS['success'],
            opacity=0.1,
            annotation_text="Optimal Range",
            annotation_position="top left"
        )
        
        return fig
    
    def plot_facility_ranking(self, profiles_df: pd.DataFrame) -> go.Figure:
        """Plot facility ranking by utilization"""
        sorted_df = profiles_df.sort_values('utilization_rate_pct_mean', ascending=True)
        
        # Color code by utilization level
        colors = sorted_df['utilization_rate_pct_mean'].apply(
            lambda x: MOH_COLORS['danger'] if x > 90 else
                     MOH_COLORS['warning'] if x > 70 else
                     MOH_COLORS['success']
        )
        
        fig = go.Figure(go.Bar(
            x=sorted_df['utilization_rate_pct_mean'],
            y=sorted_df['hospital'],
            orientation='h',
            marker=dict(color=colors),
            text=sorted_df['utilization_rate_pct_mean'].round(1),
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Facility Utilization Ranking",
            xaxis_title="Average Utilization Rate (%)",
            yaxis_title="Facility",
            template=self.template
        )
        
        return fig
    
    def plot_bottleneck_severity(self, bottleneck_df: pd.DataFrame) -> go.Figure:
        """Visualize bottleneck severity"""
        fig = px.scatter(
            bottleneck_df,
            x='utilization_rate_pct',
            y='attendances_no',
            size='severity_score',
            color='severity_score',
            hover_data=['hospital'],
            title="Bottleneck Severity Analysis",
            labels={
                'utilization_rate_pct': 'Utilization Rate (%)',
                'attendances_no': 'Annual Attendances',
                'severity_score': 'Severity Score'
            },
            color_continuous_scale='Reds',
            template=self.template
        )
        
        return fig
    
    def create_dashboard_layout(
        self, 
        utilization_df: pd.DataFrame,
        bottleneck_df: pd.DataFrame,
        profiles_df: pd.DataFrame
    ) -> Dict[str, go.Figure]:
        """Create all dashboard visualizations"""
        return {
            'utilization_trend': self.plot_utilization_trend(utilization_df),
            'facility_ranking': self.plot_facility_ranking(profiles_df),
            'bottleneck_severity': self.plot_bottleneck_severity(bottleneck_df)
        }
```

---

## 3. Configuration Files

### `epics/epic-001/config/epic_001_config.yml`

```yaml
epic_id: epic-001
epic_name: facility-utilization-bottleneck-analysis

data_sources:
  primary_source: kaggle
  dataset_id: "subhamjain/health-dataset-complete-singapore"
  
  tables:
    - admission-and-outpatient-attendances-by-restructured-hospitals
    - admission-and-outpatient-attendances
    - number-of-hospital-beds
    - facilities-in-the-registry-of-medical-clinics-and-dental-clinics

year_range:
  start: 2006
  end: 2020

output_paths:
  raw_data: epics/epic-001/data/raw/
  processed_data: epics/epic-001/data/processed/
  features: epics/epic-001/data/features/
  results: epics/epic-001/results/
  figures: epics/epic-001/reports/figures/
  reports: epics/epic-001/reports/documents/

logging:
  level: INFO
  log_dir: epics/epic-001/logs/
  log_files:
    extraction: extraction.log
    pipeline: pipeline.log
    errors: errors.log
```

### `epics/epic-001/config/epic_001_params.yml`

```yaml
# Analysis parameters for EPIC-001

utilization_thresholds:
  underutilized: 50
  optimal_min: 70
  optimal_max: 85
  high_utilization: 90
  overutilized: 95

bottleneck_detection:
  min_utilization_rate: 90
  min_severity_score: 5
  top_n_bottlenecks: 10

performance_tiers:
  top_performer: 90  # percentile
  high_performer: 75
  average_performer: 25
  below_average: 10

temporal_analysis:
  recent_years_threshold: 2015
  trend_analysis_min_years: 3

validation:
  max_null_percentage: 0
  min_records_per_table: 50
```

---

## 4. Execution Workflow

### Step-by-Step Commands

```bash
# Navigate to epic directory
cd epics/epic-001/

# Step 1: Extract data
python scripts/01_extract_data.py

# Step 2: Engineer features
python scripts/02_engineer_features.py

# Step 3: Run analysis
python scripts/03_run_analysis.py

# Step 4: Generate visualizations
python scripts/04_generate_visualizations.py

# Step 5: Create reports
python scripts/05_generate_reports.py

# OR run the entire pipeline
python scripts/run_full_pipeline.py
```

### Main Orchestration Script

```python
# epics/epic-001/scripts/run_full_pipeline.py

import sys
from pathlib import Path

# Add epic src to path
epic_root = Path(__file__).parent.parent
sys.path.insert(0, str(epic_root / 'src'))

from extraction import FacilityDataExtractor
from features import UtilizationFeatureEngineer
from analysis import FacilityAnalyzer
from visualization import UtilizationVisualizer
import logging
import yaml

def setup_logging(log_dir: Path):
    """Configure logging"""
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'pipeline.log'),
            logging.StreamHandler()
        ]
    )

def load_config(config_path: Path) -> dict:
    """Load configuration"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def main():
    # Setup
    config = load_config(epic_root / 'config' / 'epic_001_config.yml')
    params = load_config(epic_root / 'config' / 'epic_001_params.yml')
    setup_logging(Path(config['logging']['log_dir']))
    
    logger = logging.getLogger(__name__)
    logger.info("=" * 80)
    logger.info("Starting EPIC-001 Pipeline: Facility Utilization & Bottleneck Analysis")
    logger.info("=" * 80)
    
    # Step 1: Extract data
    logger.info("Step 1: Extracting data from Kaggle...")
    extractor = FacilityDataExtractor(config['data_sources']['dataset_id'])
    data_dict = extractor.extract_all()
    logger.info(f"Extracted {len(data_dict)} tables")
    
    # Step 2: Engineer features
    logger.info("Step 2: Engineering features...")
    feature_engineer = UtilizationFeatureEngineer()
    utilization_df = feature_engineer.engineer_all_features(
        data_dict['attendance_by_hospitals'],
        data_dict['bed_capacity']
    )
    
    # Save processed data
    output_path = Path(config['output_paths']['processed_data'])
    output_path.mkdir(parents=True, exist_ok=True)
    utilization_df.to_parquet(output_path / 'utilization_metrics.parquet', index=False)
    logger.info(f"Saved processed data to {output_path}")
    
    # Step 3: Analyze
    logger.info("Step 3: Running analysis...")
    analyzer = FacilityAnalyzer()
    
    # Generate performance profiles
    profiles_df = analyzer.profile_facility_performance(utilization_df)
    
    # Detect bottlenecks
    bottlenecks_df = analyzer.detect_bottlenecks(
        utilization_df,
        min_severity=params['bottleneck_detection']['min_severity_score']
    )
    
    # Generate recommendations
    recommendations = analyzer.generate_recommendations(bottlenecks_df)
    
    # Save results
    results_path = Path(config['output_paths']['results'])
    results_path.mkdir(parents=True, exist_ok=True)
    profiles_df.to_csv(results_path / 'tables' / 'facility_profiles.csv', index=False)
    bottlenecks_df.to_csv(results_path / 'tables' / 'bottlenecks.csv', index=False)
    
    logger.info(f"Identified {len(bottlenecks_df)} critical bottlenecks")
    logger.info(f"Generated {len(recommendations)} recommendations")
    
    # Step 4: Visualize
    logger.info("Step 4: Creating visualizations...")
    visualizer = UtilizationVisualizer()
    figures = visualizer.create_dashboard_layout(
        utilization_df,
        bottlenecks_df,
        profiles_df
    )
    
    # Save figures
    figures_path = Path(config['output_paths']['figures'])
    figures_path.mkdir(parents=True, exist_ok=True)
    
    for name, fig in figures.items():
        fig.write_html(figures_path / f'{name}.html')
        fig.write_image(figures_path / f'{name}.png')
    
    logger.info(f"Saved {len(figures)} visualizations")
    
    logger.info("=" * 80)
    logger.info("Pipeline completed successfully!")
    logger.info("=" * 80)

if __name__ == "__main__":
    main()
```

---

## 5. Testing Strategy

### Unit Tests

```python
# epics/epic-001/tests/test_extraction.py

import pytest
import pandas as pd
from src.extraction import FacilityDataExtractor

def test_extractor_initialization():
    """Test extractor initializes correctly"""
    extractor = FacilityDataExtractor()
    assert extractor.dataset_id == "subhamjain/health-dataset-complete-singapore"

def test_validate_extracted_data():
    """Test data validation"""
    extractor = FacilityDataExtractor()
    
    # Create sample data
    valid_df = pd.DataFrame({
        'year': [2020],
        'attendances_no': [1000]
    })
    
    assert extractor.validate_extracted_data(valid_df, ['year', 'attendances_no']) == True
    
    # Test with missing column
    invalid_df = pd.DataFrame({
        'year': [2020]
    })
    
    assert extractor.validate_extracted_data(invalid_df, ['year', 'attendances_no']) == False

# epics/epic-001/tests/test_features.py

import pytest
import pandas as pd
from src.features import UtilizationFeatureEngineer

def test_utilization_rate_calculation():
    """Test utilization rate calculation"""
    engineer = UtilizationFeatureEngineer()
    
    attendances_df = pd.DataFrame({
        'year': [2020, 2020],
        'hospital': ['A', 'B'],
        'attendances_no': [100000, 200000]
    })
    
    beds_df = pd.DataFrame({
        'year': [2020, 2020],
        'hospital': ['A', 'B'],
        'beds_no': [500, 800]
    })
    
    result = engineer.calculate_utilization_rate(attendances_df, beds_df)
    
    # Check calculations
    assert 'utilization_rate_pct' in result.columns
    assert 'annual_capacity' in result.columns
    assert result['annual_capacity'].iloc[0] == 500 * 365

def test_categorize_utilization_level():
    """Test utilization level categorization"""
    engineer = UtilizationFeatureEngineer()
    
    assert engineer.categorize_utilization_level(40) == 'Underutilized'
    assert engineer.categorize_utilization_level(75) == 'Optimal'
    assert engineer.categorize_utilization_level(95) == 'Overutilized'
```

### Running Tests

```bash
cd epics/epic-001/

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_extraction.py -v
```

---

## 6. Outputs & Deliverables

### Data Outputs

**Location**: `epics/epic-001/data/`

**Files**:
- `raw/` - Original extracted CSV files
- `processed/utilization_metrics.parquet` - Calculated utilization rates with features
- `features/` - Feature datasets for modeling

### Analysis Results

**Location**: `epics/epic-001/results/`

**Files**:
- `tables/facility_profiles.csv` - Comprehensive performance profiles for all facilities
- `tables/bottlenecks.csv` - Identified bottleneck facilities with severity scores
- `tables/recommendations.csv` - Improvement recommendations
- `metrics/data_quality_report.json` - Data quality metrics

### Visualizations

**Location**: `epics/epic-001/reports/figures/`

**Files**:
- `utilization_trend.html` - Interactive time series plot
- `utilization_trend.png` - Static chart for reports
- `facility_ranking.html` - Interactive ranking chart
- `bottleneck_severity.html` - Bottleneck severity scatter plot

### Reports

**Location**: `epics/epic-001/reports/documents/`

**Files**:
- `EPIC-001_Executive_Summary.pdf` - Executive summary report
- `EPIC-001_Technical_Report.pdf` - Detailed technical analysis
- `EPIC-001_Recommendations.pdf` - Improvement recommendations brief

---

## 7. Monitoring & Alerts

### Key Metrics to Track

```yaml
pipeline_metrics:
  - extraction_success_rate
  - data_quality_score
  - processing_time_minutes
  - bottlenecks_identified_count
  
data_quality_metrics:
  - null_percentage_critical_fields
  - duplicate_records_count
  - outlier_percentage
  
business_metrics:
  - avg_utilization_rate_all_facilities
  - facilities_above_90_pct_utilization
  - total_excess_demand_patients
```

### Logging Configuration

```yaml
# epics/epic-001/config/logging.yml

version: 1
disable_existing_loggers: false

formatters:
  standard:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: standard
    stream: ext://sys.stdout
  
  file:
    class: logging.handlers.RotatingFileHandler
    level: INFO
    formatter: detailed
    filename: epics/epic-001/logs/pipeline.log
    maxBytes: 10485760  # 10MB
    backupCount: 5
  
  error_file:
    class: logging.handlers.RotatingFileHandler
    level: ERROR
    formatter: detailed
    filename: epics/epic-001/logs/errors.log
    maxBytes: 10485760
    backupCount: 5

loggers:
  src:
    level: INFO
    handlers: [console, file, error_file]
    propagate: false

root:
  level: INFO
  handlers: [console, file]
```

---

## 8. Dependencies & Integration

### Upstream Dependencies

**None** - This is a foundational epic with no dependencies on other epics.

### Downstream Consumers

- **EPIC-004 (Process Optimization)**: Recommended to complete EPIC-001 first for utilization context
- **EPIC-006 (Demand Forecasting)**: Required baseline utilization data from EPIC-001

### Shared Components

Reference: `docs/methodology/data_flows/shared_components.md`

**Modules Used**:
- `kaggle_base_extraction` - Standard Kaggle data extraction
- `column_standardization` - Consistent column naming
- `temporal_feature_engineering` - Time series features
- `facility_categorization` - Facility type classification
- `data_quality_validation` - Standard validation checks
- `plotly_templates` - Visualization styling
- `logging_config` - Centralized logging

---

## 9. Timeline & Milestones

| Week | Days | Milestone | Deliverables |
|------|------|-----------|--------------|
| 1 | 1-3 | Data extraction & validation complete | Clean datasets, quality reports |
| 1 | 3-5 | Feature engineering complete | Utilization metrics calculated |
| 2 | 6-10 | Analysis complete | Performance profiles, bottleneck identification |
| 2-3 | 11-13 | Recommendations developed | Improvement recommendations |
| 3 | 14-15 | Dashboard & reports complete | Interactive dashboard, final reports |

**Total Duration**: 15 working days (3 weeks)

---

## 10. Success Criteria

✅ **Data Coverage**:
- [ ] 100% of facilities in dataset profiled
- [ ] All years (2006-2020) included in analysis

✅ **Analysis Completeness**:
- [ ] Minimum 10 critical bottlenecks identified
- [ ] Severity scoring framework developed and applied
- [ ] Root cause analysis completed for top 5 bottlenecks

✅ **Deliverables**:
- [ ] Facility performance scorecards generated
- [ ] Improvement recommendations with quantified impact
- [ ] Interactive dashboard deployed and functional

✅ **Quality Standards**:
- [ ] Data quality score >95%
- [ ] Unit test coverage >80%
- [ ] Code reviewed and approved
- [ ] Documentation complete

✅ **Stakeholder Acceptance**:
- [ ] Demo presented to business stakeholders
- [ ] Recommendations validated by domain experts
- [ ] Sign-off received for production deployment

---

**Document Version**: 1.0  
**Last Updated**: 2 February 2026  
**Owner**: EPIC-001 Lead Analyst
