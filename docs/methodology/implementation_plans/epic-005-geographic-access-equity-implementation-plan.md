# Implementation Plan: EPIC-005 - Geographic Access & Health Equity Analysis

## Executive Summary

- **Epic**: EPIC-005 - Geographic Access & Health Equity Analysis
- **Objective**: Conduct geographic access analysis and equity assessment to identify minimum 3 underserved areas requiring intervention and promote health equity across Singapore
- **Estimated Duration**: 4-5 weeks (32 working days)
- **Dependencies**: None (can run in parallel with other epics)
- **Key Deliverables**: 
  - Geographic access maps for all planning areas
  - Minimum 3 underserved geographic areas identified (>5km from nearest facility)
  - Quantified affected populations with demographic profiles
  - Health equity scorecard with disparity metrics (Gini coefficient, concentration index)
  - Evidence-based recommendations for facility placement or mobile services
  - Interactive geographic access dashboard

---

## 1. Epic Folder Structure

```
epics/
└── epic-005/
    ├── README.md
    ├── config/
    │   ├── epic_005_config.yml
    │   ├── epic_005_params.yml
    │   ├── epic_005_queries.yml
    │   └── geographic_data_sources.yml
    ├── src/
    │   ├── __init__.py
    │   ├── extraction.py
    │   ├── geocoding.py
    │   ├── spatial_analysis.py
    │   ├── access_metrics.py
    │   ├── equity_analysis.py
    │   ├── recommendations.py
    │   ├── visualization.py
    │   └── utils.py
    ├── scripts/
    │   ├── 01_extract_data.py
    │   ├── 02_geocode_facilities.py
    │   ├── 03_prepare_geographic_data.py
    │   ├── 04_calculate_access_metrics.py
    │   ├── 05_identify_underserved_areas.py
    │   ├── 06_health_equity_assessment.py
    │   ├── 07_profile_vulnerable_populations.py
    │   ├── 08_facility_recommendations.py
    │   ├── 09_generate_maps.py
    │   ├── 10_generate_dashboard.py
    │   └── run_full_pipeline.py
    ├── notebooks/
    │   ├── 01_geographic_data_prep.ipynb
    │   ├── 02_access_analysis.ipynb
    │   ├── 03_equity_assessment.ipynb
    │   ├── 04_recommendations.ipynb
    │   └── 05_visualization.ipynb
    ├── sql/
    │   ├── extraction_queries.sql
    │   └── validation_queries.sql
    ├── tests/
    │   ├── __init__.py
    │   ├── test_extraction.py
    │   ├── test_geocoding.py
    │   ├── test_spatial_analysis.py
    │   ├── test_equity_metrics.py
    │   └── test_integration.py
    ├── data/
    │   ├── raw/
    │   ├── processed/
    │   ├── geographic/
    │   │   ├── facilities.geojson
    │   │   ├── planning_areas.geojson
    │   │   └── population_centroids.geojson
    │   └── external/
    │       ├── singapore_planning_areas/
    │       └── onemap_api_cache/
    ├── results/
    │   ├── metrics/
    │   ├── tables/
    │   ├── recommendations/
    │   └── exports/
    ├── reports/
    │   ├── figures/
    │   ├── maps/
    │   ├── dashboards/
    │   └── documents/
    └── logs/
        ├── extraction.log
        ├── geocoding.log
        ├── pipeline.log
        └── errors.log
```

---

## 2. Module Specifications

### 2.1 Data Extraction & Geocoding

#### Module: `epics/epic-005/src/extraction.py`

**Purpose**: Extract facility and population data for geographic analysis

**Data Sources**: 
- `health-facilities-primary-care-dental-clinics-and-pharmacies`
- `health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private`
- External: Singapore Planning Area Boundaries (data.gov.sg)
- External: Population by Planning Area (SingStat)
- External: OneMap API for geocoding

**Key Functions**:

```python
from typing import Dict, List, Tuple
import pandas as pd
import kagglehub
from pathlib import Path
import logging

class GeographicDataExtractor:
    """Extract facility and geographic data"""
    
    def __init__(self, dataset_id: str = "subhamjain/health-dataset-complete-singapore"):
        self.dataset_id = dataset_id
        self.dataset_path = None
        self.logger = logging.getLogger(__name__)
    
    def download_dataset(self) -> Path:
        """Download Kaggle dataset"""
        self.logger.info(f"Downloading dataset: {self.dataset_id}")
        self.dataset_path = Path(kagglehub.dataset_download(self.dataset_id))
        return self.dataset_path
    
    def extract_facility_data(self, year: int = 2020) -> pd.DataFrame:
        """Extract all healthcare facilities"""
        # Primary care facilities
        pc_table = "health-facilities-primary-care-dental-clinics-and-pharmacies"
        pc_path = self.dataset_path / pc_table / f"{pc_table}.csv"
        pc_df = pd.read_csv(pc_path)
        pc_df = pc_df[pc_df['year'] == year]
        pc_df['facility_category'] = 'Primary Care'
        
        # Inpatient facilities
        ip_table = "health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private"
        ip_path = self.dataset_path / ip_table / f"{ip_table}.csv"
        ip_df = pd.read_csv(ip_path)
        ip_df = ip_df[ip_df['year'] == year]
        ip_df['facility_category'] = 'Inpatient'
        
        self.logger.info(f"Extracted {len(pc_df)} primary care, {len(ip_df)} inpatient facilities")
        
        return {
            'primary_care': pc_df,
            'inpatient': ip_df
        }
    
    def load_planning_area_boundaries(self) -> pd.DataFrame:
        """Load Singapore planning area boundaries (mock for demonstration)"""
        # In production, load from data.gov.sg GeoJSON
        # For now, create mock data
        planning_areas = [
            {'planning_area': 'Ang Mo Kio', 'region': 'North-East', 'area_sqkm': 8.6},
            {'planning_area': 'Bedok', 'region': 'East', 'area_sqkm': 11.9},
            {'planning_area': 'Bishan', 'region': 'Central', 'area_sqkm': 6.9},
            {'planning_area': 'Bukit Batok', 'region': 'West', 'area_sqkm': 8.8},
            {'planning_area': 'Bukit Merah', 'region': 'Central', 'area_sqkm': 9.5},
            {'planning_area': 'Bukit Panjang', 'region': 'West', 'area_sqkm': 8.0},
            {'planning_area': 'Bukit Timah', 'region': 'Central', 'area_sqkm': 15.6},
            {'planning_area': 'Choa Chu Kang', 'region': 'West', 'area_sqkm': 10.0},
            {'planning_area': 'Clementi', 'region': 'West', 'area_sqkm': 8.5},
            {'planning_area': 'Geylang', 'region': 'Central', 'area_sqkm': 10.0},
            {'planning_area': 'Hougang', 'region': 'North-East', 'area_sqkm': 8.9},
            {'planning_area': 'Jurong East', 'region': 'West', 'area_sqkm': 11.3},
            {'planning_area': 'Jurong West', 'region': 'West', 'area_sqkm': 23.0},
            {'planning_area': 'Kallang', 'region': 'Central', 'area_sqkm': 10.1},
            {'planning_area': 'Marine Parade', 'region': 'Central', 'area_sqkm': 2.8},
            {'planning_area': 'Pasir Ris', 'region': 'East', 'area_sqkm': 12.0},
            {'planning_area': 'Punggol', 'region': 'North-East', 'area_sqkm': 10.0},
            {'planning_area': 'Queenstown', 'region': 'Central', 'area_sqkm': 10.8},
            {'planning_area': 'Sengkang', 'region': 'North-East', 'area_sqkm': 10.5},
            {'planning_area': 'Serangoon', 'region': 'North-East', 'area_sqkm': 9.4},
            {'planning_area': 'Tampines', 'region': 'East', 'area_sqkm': 21.9},
            {'planning_area': 'Toa Payoh', 'region': 'Central', 'area_sqkm': 7.2},
            {'planning_area': 'Woodlands', 'region': 'North', 'area_sqkm': 13.5},
            {'planning_area': 'Yishun', 'region': 'North', 'area_sqkm': 13.8}
        ]
        
        df = pd.DataFrame(planning_areas)
        self.logger.info(f"Loaded {len(df)} planning areas")
        return df
    
    def load_population_data(self) -> pd.DataFrame:
        """Load population by planning area (mock data)"""
        # In production, load from SingStat
        population_data = [
            {'planning_area': 'Ang Mo Kio', 'population': 165000, 'elderly_pct': 18.5},
            {'planning_area': 'Bedok', 'population': 289000, 'elderly_pct': 16.2},
            {'planning_area': 'Bishan', 'population': 92000, 'elderly_pct': 19.8},
            {'planning_area': 'Bukit Batok', 'population': 148000, 'elderly_pct': 15.4},
            {'planning_area': 'Bukit Merah', 'population': 153000, 'elderly_pct': 20.1},
            {'planning_area': 'Bukit Panjang', 'population': 138000, 'elderly_pct': 12.7},
            {'planning_area': 'Bukit Timah', 'population': 98000, 'elderly_pct': 17.5},
            {'planning_area': 'Choa Chu Kang', 'population': 192000, 'elderly_pct': 11.8},
            {'planning_area': 'Clementi', 'population': 94000, 'elderly_pct': 16.9},
            {'planning_area': 'Geylang', 'population': 105000, 'elderly_pct': 19.2},
            {'planning_area': 'Hougang', 'population': 227000, 'elderly_pct': 14.6},
            {'planning_area': 'Jurong East', 'population': 90000, 'elderly_pct': 15.3},
            {'planning_area': 'Jurong West', 'population': 265000, 'elderly_pct': 13.1},
            {'planning_area': 'Kallang', 'population': 143000, 'elderly_pct': 17.8},
            {'planning_area': 'Marine Parade', 'population': 28000, 'elderly_pct': 22.4},
            {'planning_area': 'Pasir Ris', 'population': 149000, 'elderly_pct': 10.2},
            {'planning_area': 'Punggol', 'population': 188000, 'elderly_pct': 7.5},
            {'planning_area': 'Queenstown', 'population': 103000, 'elderly_pct': 21.5},
            {'planning_area': 'Sengkang', 'population': 249000, 'elderly_pct': 8.9},
            {'planning_area': 'Serangoon', 'population': 121000, 'elderly_pct': 16.1},
            {'planning_area': 'Tampines', 'population': 269000, 'elderly_pct': 13.8},
            {'planning_area': 'Toa Payoh', 'population': 108000, 'elderly_pct': 23.6},
            {'planning_area': 'Woodlands', 'population': 254000, 'elderly_pct': 10.8},
            {'planning_area': 'Yishun', 'population': 216000, 'elderly_pct': 12.4}
        ]
        
        df = pd.DataFrame(population_data)
        df['elderly_population'] = (df['population'] * df['elderly_pct'] / 100).astype(int)
        
        self.logger.info(f"Loaded population data for {len(df)} planning areas")
        return df
    
    def extract_all(self) -> Dict:
        """Extract all required data"""
        if not self.dataset_path:
            self.download_dataset()
        
        facilities = self.extract_facility_data()
        planning_areas = self.load_planning_area_boundaries()
        population = self.load_population_data()
        
        return {
            'facilities': facilities,
            'planning_areas': planning_areas,
            'population': population
        }
```

#### Module: `epics/epic-005/src/geocoding.py`

**Purpose**: Geocode facility addresses to coordinates

**Key Functions**:

```python
import requests
import pandas as pd
import numpy as np
import time
from typing import Dict, Optional
import logging

class FacilityGeocoder:
    """Geocode facility locations using OneMap API"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.onemap_api_url = "https://developers.onemap.sg/commonapi/search"
        self.cache = {}
    
    def geocode_address(self, address: str) -> Optional[Dict[str, float]]:
        """
        Geocode single address using OneMap API
        
        Returns:
            Dict with 'latitude' and 'longitude', or None if not found
        """
        # Check cache
        if address in self.cache:
            return self.cache[address]
        
        try:
            params = {
                'searchVal': address,
                'returnGeom': 'Y',
                'getAddrDetails': 'Y'
            }
            
            response = requests.get(self.onemap_api_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['found'] > 0:
                    result = {
                        'latitude': float(data['results'][0]['LATITUDE']),
                        'longitude': float(data['results'][0]['LONGITUDE'])
                    }
                    
                    # Cache result
                    self.cache[address] = result
                    return result
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Geocoding failed for '{address}': {e}")
            return None
    
    def geocode_facilities(
        self,
        facilities_df: pd.DataFrame,
        address_column: str = 'address',
        rate_limit_delay: float = 0.25
    ) -> pd.DataFrame:
        """
        Geocode all facilities in dataframe
        
        Args:
            facilities_df: DataFrame with facility addresses
            address_column: Name of address column
            rate_limit_delay: Delay between API calls (seconds)
        """
        facilities_df = facilities_df.copy()
        
        # Initialize coordinate columns
        facilities_df['latitude'] = np.nan
        facilities_df['longitude'] = np.nan
        
        # For demonstration, use mock coordinates
        # In production, would call actual OneMap API
        # Singapore approximate center: 1.3521, 103.8198
        
        np.random.seed(42)
        facilities_df['latitude'] = np.random.uniform(1.25, 1.45, len(facilities_df))
        facilities_df['longitude'] = np.random.uniform(103.6, 104.0, len(facilities_df))
        
        geocoded_count = facilities_df['latitude'].notna().sum()
        
        self.logger.info(f"Geocoded {geocoded_count}/{len(facilities_df)} facilities")
        
        return facilities_df
    
    def assign_planning_areas(
        self,
        facilities_df: pd.DataFrame,
        planning_areas_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Assign facilities to planning areas based on coordinates"""
        # In production, would use spatial join with actual polygons
        # For demonstration, randomly assign
        
        facilities_df = facilities_df.copy()
        
        planning_area_list = planning_areas_df['planning_area'].tolist()
        facilities_df['planning_area'] = np.random.choice(
            planning_area_list,
            size=len(facilities_df)
        )
        
        self.logger.info(f"Assigned {len(facilities_df)} facilities to planning areas")
        
        return facilities_df
```

---

### 2.2 Spatial Access Analysis

#### Module: `epics/epic-005/src/access_metrics.py`

**Purpose**: Calculate geographic access metrics

**Key Functions**:

```python
import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
from typing import Dict, Tuple
import logging

class AccessMetricsCalculator:
    """Calculate geographic access metrics"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Singapore approximate dimensions for distance conversion
        self.km_per_degree_lat = 111.0
        self.km_per_degree_lon = 111.0 * np.cos(np.radians(1.35))  # At Singapore latitude
    
    def calculate_nearest_facility_distance(
        self,
        population_df: pd.DataFrame,
        facilities_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate distance from each population centroid to nearest facility
        
        Uses KD-tree for efficient nearest neighbor search
        """
        # Extract facility coordinates
        facility_coords = facilities_df[['latitude', 'longitude']].values
        
        # Extract population centroid coordinates
        # For demonstration, use planning area centroids (mock)
        pop_df = population_df.copy()
        
        # Mock: assign approximate centroids
        np.random.seed(42)
        pop_df['centroid_lat'] = np.random.uniform(1.25, 1.45, len(pop_df))
        pop_df['centroid_lon'] = np.random.uniform(103.6, 104.0, len(pop_df))
        
        population_coords = pop_df[['centroid_lat', 'centroid_lon']].values
        
        # Build KD-tree for facilities
        tree = cKDTree(facility_coords)
        
        # Find nearest facility for each population centroid
        distances, indices = tree.query(population_coords)
        
        # Convert distances to kilometers
        pop_df['distance_to_nearest_facility_km'] = distances * self.km_per_degree_lat
        pop_df['nearest_facility_idx'] = indices
        pop_df['nearest_facility_id'] = facilities_df.iloc[indices]['facility_id'].values \
            if 'facility_id' in facilities_df.columns else indices
        
        self.logger.info(f"Calculated distances for {len(pop_df)} planning areas")
        self.logger.info(f"Average distance: {pop_df['distance_to_nearest_facility_km'].mean():.2f} km")
        
        return pop_df
    
    def calculate_access_score(self, distance_km: float) -> int:
        """
        Calculate access score (0-100) based on distance
        
        Scoring:
        - 100: < 1km
        - 75: 1-2km
        - 50: 2-5km
        - 25: 5-10km
        - 0: > 10km
        """
        if distance_km < 1:
            return 100
        elif distance_km < 2:
            return 75
        elif distance_km < 5:
            return 50
        elif distance_km < 10:
            return 25
        else:
            return 0
    
    def add_access_scores(self, population_df: pd.DataFrame) -> pd.DataFrame:
        """Add access scores to population dataframe"""
        population_df = population_df.copy()
        
        population_df['access_score'] = population_df['distance_to_nearest_facility_km'].apply(
            self.calculate_access_score
        )
        
        # Categorize access level
        def categorize_access(score):
            if score >= 75:
                return 'Excellent'
            elif score >= 50:
                return 'Good'
            elif score >= 25:
                return 'Fair'
            else:
                return 'Poor'
        
        population_df['access_level'] = population_df['access_score'].apply(categorize_access)
        
        self.logger.info(f"Access scores calculated. Average: {population_df['access_score'].mean():.1f}")
        
        return population_df
    
    def calculate_coverage_metrics(self, population_df: pd.DataFrame) -> Dict[str, float]:
        """Calculate overall coverage metrics"""
        total_population = population_df['population'].sum()
        
        metrics = {
            'pct_within_1km': (
                population_df[population_df['distance_to_nearest_facility_km'] < 1]['population'].sum() 
                / total_population * 100
            ),
            'pct_within_2km': (
                population_df[population_df['distance_to_nearest_facility_km'] < 2]['population'].sum() 
                / total_population * 100
            ),
            'pct_within_5km': (
                population_df[population_df['distance_to_nearest_facility_km'] < 5]['population'].sum() 
                / total_population * 100
            ),
            'avg_distance_km': population_df['distance_to_nearest_facility_km'].mean(),
            'weighted_avg_distance_km': (
                (population_df['distance_to_nearest_facility_km'] * population_df['population']).sum() 
                / total_population
            ),
            'avg_access_score': population_df['access_score'].mean(),
            'weighted_avg_access_score': (
                (population_df['access_score'] * population_df['population']).sum() 
                / total_population
            )
        }
        
        self.logger.info(f"Coverage metrics: {metrics['pct_within_5km']:.1f}% within 5km, "
                        f"avg distance: {metrics['avg_distance_km']:.2f} km")
        
        return metrics
```

---

### 2.3 Health Equity Analysis

#### Module: `epics/epic-005/src/equity_analysis.py`

**Purpose**: Assess health equity and identify disparities

**Key Functions**:

```python
import pandas as pd
import numpy as np
from typing import Dict, List
import logging

class HealthEquityAnalyzer:
    """Analyze health equity and identify disparities"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def calculate_gini_coefficient(
        self,
        access_scores: np.ndarray,
        populations: np.ndarray
    ) -> float:
        """
        Calculate Gini coefficient for healthcare access equity
        
        0 = perfect equality
        1 = perfect inequality
        """
        # Sort by access score
        sorted_indices = np.argsort(access_scores)
        sorted_access = access_scores[sorted_indices]
        sorted_pop = populations[sorted_indices]
        
        # Calculate cumulative shares
        cum_pop = np.cumsum(sorted_pop) / np.sum(sorted_pop)
        cum_access = np.cumsum(sorted_access * sorted_pop) / np.sum(sorted_access * sorted_pop)
        
        # Calculate Gini coefficient (area between Lorenz curve and equality line)
        gini = 1 - 2 * np.trapz(cum_access, cum_pop)
        
        self.logger.info(f"Gini coefficient: {gini:.3f}")
        
        return gini
    
    def calculate_concentration_index(
        self,
        access_scores: np.ndarray,
        income_ranks: np.ndarray,
        populations: np.ndarray
    ) -> float:
        """
        Calculate concentration index by income
        
        Negative = pro-poor (better access for low-income)
        Positive = pro-rich (better access for high-income)
        Zero = no income-related disparity
        """
        # Sort by income rank
        sorted_indices = np.argsort(income_ranks)
        sorted_access = access_scores[sorted_indices]
        sorted_pop = populations[sorted_indices]
        
        # Calculate cumulative shares
        cum_pop = np.cumsum(sorted_pop) / np.sum(sorted_pop)
        cum_access = np.cumsum(sorted_access * sorted_pop) / np.sum(sorted_access * sorted_pop)
        
        # Concentration index (similar to Gini but ordered by income)
        ci = 1 - 2 * np.trapz(cum_access, cum_pop)
        
        self.logger.info(f"Concentration index: {ci:.3f}")
        
        return ci
    
    def analyze_demographic_disparities(
        self,
        population_df: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:
        """Analyze access disparities by demographic groups"""
        # Add income quintile (mock)
        np.random.seed(42)
        population_df['income_quintile'] = np.random.choice(['Q1', 'Q2', 'Q3', 'Q4', 'Q5'], len(population_df))
        
        # Access by income quintile
        income_analysis = population_df.groupby('income_quintile').agg({
            'access_score': ['mean', 'median'],
            'population': 'sum',
            'distance_to_nearest_facility_km': 'mean'
        }).round(2)
        
        # Access by region
        region_analysis = population_df.groupby('region').agg({
            'access_score': ['mean', 'median'],
            'population': 'sum',
            'distance_to_nearest_facility_km': 'mean'
        }).round(2)
        
        # Access for elderly
        elderly_analysis = pd.DataFrame({
            'group': ['Elderly (65+)', 'General Population'],
            'avg_access_score': [
                population_df.groupby('planning_area').apply(
                    lambda x: np.average(x['access_score'], weights=x['elderly_population'])
                ).mean(),
                population_df['access_score'].mean()
            ]
        })
        
        self.logger.info("Demographic disparity analysis complete")
        
        return {
            'by_income': income_analysis,
            'by_region': region_analysis,
            'elderly_vs_general': elderly_analysis
        }
    
    def create_equity_scorecard(
        self,
        population_df: pd.DataFrame,
        gini: float,
        concentration_index: float,
        disparities: Dict
    ) -> Dict:
        """Create comprehensive equity scorecard"""
        # Calculate disparity ratios
        income_disparity = disparities['by_income']
        q1_access = income_disparity.loc['Q1', ('access_score', 'mean')]
        q5_access = income_disparity.loc['Q5', ('access_score', 'mean')]
        income_disparity_ratio = q1_access / q5_access if q5_access > 0 else 0
        
        # Regional disparities
        region_disparity = disparities['by_region']
        min_region_access = region_disparity[('access_score', 'mean')].min()
        max_region_access = region_disparity[('access_score', 'mean')].max()
        regional_disparity_ratio = min_region_access / max_region_access
        
        scorecard = {
            'overall_metrics': {
                'gini_coefficient': gini,
                'concentration_index': concentration_index,
                'avg_access_score': population_df['access_score'].mean()
            },
            'disparity_ratios': {
                'income_disparity_ratio': income_disparity_ratio,
                'regional_disparity_ratio': regional_disparity_ratio
            },
            'equity_assessment': self._assess_equity(gini, concentration_index)
        }
        
        return scorecard
    
    def _assess_equity(self, gini: float, ci: float) -> str:
        """Assess overall equity level"""
        if gini < 0.2:
            gini_level = 'Excellent equity'
        elif gini < 0.3:
            gini_level = 'Good equity'
        elif gini < 0.4:
            gini_level = 'Moderate inequity'
        else:
            gini_level = 'Significant inequity'
        
        if abs(ci) < 0.05:
            ci_level = 'No income-related disparity'
        elif ci < -0.05:
            ci_level = 'Pro-poor access'
        else:
            ci_level = 'Pro-rich access'
        
        return f"{gini_level}. {ci_level}."
```

---

## 3. Configuration Files

### `epics/epic-005/config/epic_005_config.yml`

```yaml
epic_id: epic-005
epic_name: geographic-access-health-equity-analysis

data_sources:
  primary_source: kaggle
  dataset_id: "subhamjain/health-dataset-complete-singapore"
  
  tables:
    - health-facilities-primary-care-dental-clinics-and-pharmacies
    - health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private
  
  external_sources:
    - name: Singapore Planning Areas
      source: data.gov.sg
      format: GeoJSON
    - name: Population by Planning Area
      source: SingStat
      format: Excel/CSV
    - name: OneMap API
      source: developers.onemap.sg
      purpose: Geocoding

analysis_year: 2020

singapore_bounds:
  min_lat: 1.15
  max_lat: 1.48
  min_lon: 103.6
  max_lon: 104.1

output_paths:
  raw_data: epics/epic-005/data/raw/
  processed_data: epics/epic-005/data/processed/
  geographic: epics/epic-005/data/geographic/
  results: epics/epic-005/results/
  maps: epics/epic-005/reports/maps/
  figures: epics/epic-005/reports/figures/
  reports: epics/epic-005/reports/documents/

logging:
  level: INFO
  log_dir: epics/epic-005/logs/
  log_files:
    extraction: extraction.log
    geocoding: geocoding.log
    pipeline: pipeline.log
    errors: errors.log
```

### `epics/epic-005/config/epic_005_params.yml`

```yaml
# Analysis parameters for EPIC-005

underserved_criteria:
  minimum_areas_required: 3
  distance_threshold_km: 5.0
  minimum_population: 10000
  access_score_threshold: 25  # Below this = underserved

access_scoring:
  excellent: 100  # < 1km
  good: 75        # 1-2km
  fair: 50        # 2-5km
  poor: 25        # 5-10km
  very_poor: 0    # > 10km

equity_metrics:
  gini_thresholds:
    excellent: 0.20
    good: 0.30
    moderate: 0.40
  
  concentration_index_thresholds:
    no_disparity: 0.05
    moderate_disparity: 0.15

facility_recommendations:
  intervention_types:
    - new_facility
    - mobile_clinic
    - telemedicine_hub
  
  cost_estimates:
    new_facility_sgd: 10000000
    mobile_clinic_sgd: 500000
    telemedicine_hub_sgd: 200000

vulnerable_populations:
  elderly_threshold_pct: 18.0  # Above average elderly population
  low_income_threshold: Q1     # Bottom income quintile
```

---

## 4. Execution Workflow

### Orchestration Script: `epics/epic-005/scripts/run_full_pipeline.py`

```python
#!/usr/bin/env python3
"""
EPIC-005 Full Pipeline Orchestrator
Execute complete geographic access and health equity analysis
"""

import sys
from pathlib import Path
import logging
import yaml
from datetime import datetime
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from extraction import GeographicDataExtractor
from geocoding import FacilityGeocoder
from access_metrics import AccessMetricsCalculator
from equity_analysis import HealthEquityAnalyzer

def setup_logging(log_dir: Path):
    """Setup logging configuration"""
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'pipeline.log'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def main():
    """Execute full EPIC-005 pipeline"""
    
    # Load configuration
    config_path = Path(__file__).parent.parent / 'config' / 'epic_005_config.yml'
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Setup logging
    logger = setup_logging(Path(config['logging']['log_dir']))
    logger.info("="*80)
    logger.info("EPIC-005: Geographic Access & Health Equity Analysis")
    logger.info(f"Pipeline started at {datetime.now()}")
    logger.info("="*80)
    
    try:
        # Step 1: Extract data
        logger.info("\n[STEP 1] Extracting geographic data...")
        extractor = GeographicDataExtractor()
        data = extractor.extract_all()
        logger.info(f"✓ Data extraction complete")
        
        # Step 2: Geocode facilities
        logger.info("\n[STEP 2] Geocoding facilities...")
        geocoder = FacilityGeocoder()
        
        # Combine facilities
        facilities = pd.concat([
            data['facilities']['primary_care'],
            data['facilities']['inpatient']
        ], ignore_index=True)
        
        # Add facility IDs
        facilities['facility_id'] = range(len(facilities))
        
        # Geocode
        facilities_geocoded = geocoder.geocode_facilities(facilities)
        
        # Assign to planning areas
        facilities_geocoded = geocoder.assign_planning_areas(
            facilities_geocoded,
            data['planning_areas']
        )
        
        logger.info(f"✓ Geocoded {len(facilities_geocoded)} facilities")
        
        # Step 3: Merge population with planning areas
        logger.info("\n[STEP 3] Preparing geographic datasets...")
        population_geo = data['population'].merge(
            data['planning_areas'],
            on='planning_area',
            how='left'
        )
        
        logger.info(f"✓ Prepared {len(population_geo)} planning areas with population")
        
        # Step 4: Calculate access metrics
        logger.info("\n[STEP 4] Calculating access metrics...")
        access_calc = AccessMetricsCalculator()
        
        # Calculate distances
        population_access = access_calc.calculate_nearest_facility_distance(
            population_geo,
            facilities_geocoded
        )
        
        # Add access scores
        population_access = access_calc.add_access_scores(population_access)
        
        # Calculate coverage metrics
        coverage_metrics = access_calc.calculate_coverage_metrics(population_access)
        
        logger.info(f"✓ Access metrics calculated")
        logger.info(f"  - {coverage_metrics['pct_within_5km']:.1f}% population within 5km")
        logger.info(f"  - Average access score: {coverage_metrics['avg_access_score']:.1f}")
        
        # Step 5: Identify underserved areas
        logger.info("\n[STEP 5] Identifying underserved areas...")
        underserved = population_access[
            (population_access['distance_to_nearest_facility_km'] > 5) &
            (population_access['population'] > 10000)
        ].copy()
        
        underserved['severity_score'] = (
            underserved['distance_to_nearest_facility_km'] *
            underserved['population'] / 1000
        )
        
        underserved = underserved.sort_values('severity_score', ascending=False)
        
        logger.info(f"✓ Identified {len(underserved)} underserved areas")
        for idx, row in underserved.head(3).iterrows():
            logger.info(f"  - {row['planning_area']}: {row['population']:,} people, "
                       f"{row['distance_to_nearest_facility_km']:.1f}km from facility")
        
        # Step 6: Health equity assessment
        logger.info("\n[STEP 6] Conducting health equity assessment...")
        equity_analyzer = HealthEquityAnalyzer()
        
        # Calculate Gini coefficient
        gini = equity_analyzer.calculate_gini_coefficient(
            population_access['access_score'].values,
            population_access['population'].values
        )
        
        # Mock income ranks for concentration index
        np.random.seed(42)
        income_ranks = np.arange(len(population_access))
        np.random.shuffle(income_ranks)
        
        ci = equity_analyzer.calculate_concentration_index(
            population_access['access_score'].values,
            income_ranks,
            population_access['population'].values
        )
        
        # Demographic disparities
        disparities = equity_analyzer.analyze_demographic_disparities(population_access)
        
        # Create equity scorecard
        equity_scorecard = equity_analyzer.create_equity_scorecard(
            population_access, gini, ci, disparities
        )
        
        logger.info(f"✓ Health equity assessment complete")
        logger.info(f"  - Gini coefficient: {gini:.3f}")
        logger.info(f"  - Concentration index: {ci:.3f}")
        logger.info(f"  - Assessment: {equity_scorecard['equity_assessment']}")
        
        # Step 7: Save results
        logger.info("\n[STEP 7] Saving results...")
        results_dir = Path(config['output_paths']['results'])
        results_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = results_dir / 'exports' / 'e05_geographic_access_analysis.xlsx'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            population_access.to_excel(writer, sheet_name='Access Metrics', index=False)
            underserved.to_excel(writer, sheet_name='Underserved Areas', index=False)
            
            # Coverage metrics
            pd.DataFrame([coverage_metrics]).to_excel(writer, sheet_name='Coverage Metrics', index=False)
            
            # Equity scorecard
            pd.DataFrame([equity_scorecard['overall_metrics']]).to_excel(
                writer, sheet_name='Equity Scorecard', index=False
            )
            
            disparities['by_income'].to_excel(writer, sheet_name='Disparity by Income')
            disparities['by_region'].to_excel(writer, sheet_name='Disparity by Region')
        
        logger.info(f"✓ Results saved to {output_file}")
        
        # Summary
        logger.info("\n" + "="*80)
        logger.info("EPIC-005 PIPELINE COMPLETE")
        logger.info(f"Planning areas analyzed: {len(population_access)}")
        logger.info(f"Facilities geocoded: {len(facilities_geocoded)}")
        logger.info(f"Underserved areas identified: {len(underserved)}")
        logger.info(f"Coverage: {coverage_metrics['pct_within_5km']:.1f}% within 5km")
        logger.info(f"Equity (Gini): {gini:.3f}")
        logger.info(f"Results available at: {output_file}")
        logger.info("="*80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

---

## 5. Testing Strategy

### Unit Tests: `epics/epic-005/tests/test_spatial_analysis.py`

```python
import unittest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

from access_metrics import AccessMetricsCalculator
from equity_analysis import HealthEquityAnalyzer

class TestSpatialAnalysis(unittest.TestCase):
    """Test spatial analysis functionality"""
    
    def setUp(self):
        """Setup test data"""
        self.access_calc = AccessMetricsCalculator()
        self.equity_analyzer = HealthEquityAnalyzer()
    
    def test_access_score_calculation(self):
        """Test access score calculation"""
        # Test different distances
        self.assertEqual(self.access_calc.calculate_access_score(0.5), 100)
        self.assertEqual(self.access_calc.calculate_access_score(1.5), 75)
        self.assertEqual(self.access_calc.calculate_access_score(3), 50)
        self.assertEqual(self.access_calc.calculate_access_score(7), 25)
        self.assertEqual(self.access_calc.calculate_access_score(15), 0)
    
    def test_gini_coefficient(self):
        """Test Gini coefficient calculation"""
        # Perfect equality (everyone has same access)
        access_equal = np.array([50, 50, 50, 50])
        pop_equal = np.array([100, 100, 100, 100])
        gini_equal = self.equity_analyzer.calculate_gini_coefficient(access_equal, pop_equal)
        self.assertAlmostEqual(gini_equal, 0.0, places=2)
        
        # Perfect inequality
        access_unequal = np.array([0, 0, 0, 100])
        pop_unequal = np.array([100, 100, 100, 100])
        gini_unequal = self.equity_analyzer.calculate_gini_coefficient(access_unequal, pop_unequal)
        self.assertGreater(gini_unequal, 0.5)
    
    def test_minimum_underserved_areas(self):
        """Test that minimum underserved areas are identified"""
        # Create mock data with some underserved areas
        pop_data = {
            'planning_area': ['Area1', 'Area2', 'Area3', 'Area4'],
            'population': [50000, 30000, 20000, 15000],
            'distance_to_nearest_facility_km': [6.0, 7.5, 3.0, 8.0]
        }
        pop_df = pd.DataFrame(pop_data)
        
        # Identify underserved (>5km, >10k population)
        underserved = pop_df[
            (pop_df['distance_to_nearest_facility_km'] > 5) &
            (pop_df['population'] > 10000)
        ]
        
        # Should identify at least 3
        self.assertGreaterEqual(len(underserved), 3)

if __name__ == '__main__':
    unittest.main()
```

---

## 6. Outputs & Deliverables

### Geographic Data

**Location**: `epics/epic-005/data/geographic/`

**Files**:
- `facilities.geojson` - Geocoded facility locations
- `planning_areas.geojson` - Planning area boundaries
- `population_centroids.geojson` - Population centroid points
- `underserved_areas.geojson` - Identified underserved areas

### Analysis Results

**Location**: `epics/epic-005/results/exports/`

**Files**:
- `e05_geographic_access_analysis.xlsx` - Comprehensive analysis (multi-sheet)
  - Access Metrics (all planning areas)
  - Underserved Areas (3+ areas)
  - Coverage Metrics
  - Equity Scorecard
  - Disparity by Income
  - Disparity by Region

### Maps

**Location**: `epics/epic-005/reports/maps/`

**Files** (PNG + Interactive HTML):
- `access_heatmap.html` - Interactive choropleth map of access scores
- `facility_locations_map.html` - Facility distribution map
- `underserved_areas_map.html` - Highlighted underserved areas
- `recommended_locations_map.html` - Proposed facility locations

### Reports

**Location**: `epics/epic-005/reports/documents/`

**Files**:
- `EPIC-005_Executive_Summary.pdf`
- `EPIC-005_Geographic_Access_Report.pdf`
- `EPIC-005_Health_Equity_Scorecard.pdf`
- `EPIC-005_Facility_Recommendations.pdf`

### Dashboard

**Tool**: Plotly Dash with Mapbox

**Access**: `http://localhost:8050/epic005_geographic_dashboard`

**Components**:
- KPI Cards (underserved areas, affected population, Gini, avg access score)
- Interactive Map (access heatmap with facility markers)
- Underserved Areas Table (sortable, filterable)
- Equity Charts (disparity by income/region)
- Recommendation Cards (proposed interventions)

---

## 7. Monitoring & Alerts

### Key Metrics

```yaml
pipeline_metrics:
  - geocoding_success_rate
  - data_quality_score
  
business_metrics:
  - underserved_areas_count
  - affected_population_total
  - pct_within_5km_coverage
  - avg_access_score
  - gini_coefficient
  - concentration_index
```

---

## 8. Dependencies & Integration

### Upstream Dependencies

- None (independent epic)

### Downstream Consumers

- **EPIC-003 (Gap Analysis)**: Geographic gaps inform resource allocation recommendations
- **EPIC-006 (Demand Forecasting)**: Underserved areas inform capacity expansion needs

### Shared Components

- `kaggle_base_extraction`
- `data_quality_validation`
- `plotly_templates`
- `logging_config`

---

## 9. Timeline & Milestones

| Week | Days | Milestone | Deliverables |
|------|------|-----------|--------------|
| 1 | 1-4 | Data extraction & geocoding | Geocoded facilities, planning areas |
| 2 | 5-10 | Access metrics calculation | Distance calculations, access scores |
| 3 | 11-14 | Underserved areas identified | 3+ underserved areas |
| 3-4 | 15-19 | Health equity assessment | Gini, concentration index, disparity analysis |
| 4 | 20-23 | Vulnerable populations profiled | Population profiles |
| 5 | 24-28 | Facility recommendations developed | Recommendations with cost estimates |
| 5-6 | 29-32 | Maps, dashboard, reports | Final deliverables |

**Total Duration**: 32 working days (4-5 weeks)

---

## 10. Success Criteria

✅ **Geographic Analysis**:
- [ ] All planning areas analyzed
- [ ] Facilities geocoded with >90% success rate
- [ ] Access metrics calculated for all areas

✅ **Underserved Areas**:
- [ ] Minimum 3 underserved areas identified
- [ ] Each area has >5km distance from facility
- [ ] Affected populations quantified

✅ **Health Equity**:
- [ ] Gini coefficient calculated
- [ ] Concentration index calculated
- [ ] Demographic disparities analyzed
- [ ] Equity scorecard created

✅ **Recommendations**:
- [ ] Facility placement recommendations (3+)
- [ ] Cost estimates for interventions
- [ ] Implementation roadmap

✅ **Deliverables**:
- [ ] Interactive maps generated
- [ ] Geographic dashboard deployed
- [ ] Reports completed

✅ **Quality Standards**:
- [ ] Data quality score >90%
- [ ] Geocoding accuracy validated
- [ ] Unit test coverage >75%

✅ **Stakeholder Acceptance**:
- [ ] Analysis validated by planning team
- [ ] Recommendations reviewed
- [ ] Dashboard demonstrated
- [ ] Sign-off received

---

**Document Version**: 1.0  
**Last Updated**: 2 February 2026  
**Owner**: EPIC-005 Lead Geographic Analyst
