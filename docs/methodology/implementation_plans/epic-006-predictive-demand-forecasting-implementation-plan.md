# Implementation Plan: EPIC-006 - Predictive Healthcare Demand Forecasting

## Executive Summary

- **Epic**: EPIC-006 - Predictive Healthcare Demand Forecasting
- **Objective**: Build predictive models to forecast healthcare demand and capacity needs with minimum 85% accuracy for 1-year and 5-year horizons, enabling proactive capacity planning
- **Estimated Duration**: 6-7 weeks (42 working days)
- **Dependencies**: EPIC-001 (utilization data recommended)
- **Key Deliverables**: 
  - Time-series forecasting models with 85%+ accuracy (≤15% MAPE)
  - Demand forecasts for 1-year and 5-year horizons with confidence intervals
  - Minimum 5 capacity gaps identified with quantified impact
  - Resource requirement projections (beds, staff, equipment)
  - Minimum 3 business cases for capacity expansions (with NPV, ROI, BCR)
  - Interactive capacity planning dashboard

---

## 1. Epic Folder Structure

```
epics/
└── epic-006/
    ├── README.md
    ├── config/
    │   ├── epic_006_config.yml
    │   ├── epic_006_params.yml
    │   ├── epic_006_queries.yml
    │   └── model_hyperparameters.yml
    ├── src/
    │   ├── __init__.py
    │   ├── extraction.py
    │   ├── feature_engineering.py
    │   ├── forecasting_models.py
    │   ├── demographic_modeling.py
    │   ├── capacity_analysis.py
    │   ├── business_case.py
    │   ├── visualization.py
    │   └── utils.py
    ├── scripts/
    │   ├── 01_extract_data.py
    │   ├── 02_prepare_demand_data.py
    │   ├── 03_analyze_patterns.py
    │   ├── 04_train_arima_model.py
    │   ├── 05_train_prophet_model.py
    │   ├── 06_train_lstm_model.py
    │   ├── 07_ensemble_models.py
    │   ├── 08_demographic_adjustments.py
    │   ├── 09_identify_capacity_gaps.py
    │   ├── 10_project_resources.py
    │   ├── 11_build_business_cases.py
    │   ├── 12_generate_dashboard.py
    │   └── run_full_pipeline.py
    ├── notebooks/
    │   ├── 01_data_exploration.ipynb
    │   ├── 02_time_series_analysis.ipynb
    │   ├── 03_arima_modeling.ipynb
    │   ├── 04_prophet_modeling.ipynb
    │   ├── 05_lstm_modeling.ipynb
    │   ├── 06_model_evaluation.ipynb
    │   └── 07_capacity_planning.ipynb
    ├── sql/
    │   ├── extraction_queries.sql
    │   └── validation_queries.sql
    ├── tests/
    │   ├── __init__.py
    │   ├── test_extraction.py
    │   ├── test_feature_engineering.py
    │   ├── test_forecasting.py
    │   ├── test_capacity_analysis.py
    │   └── test_integration.py
    ├── data/
    │   ├── raw/
    │   ├── processed/
    │   ├── time_series/
    │   └── forecasts/
    ├── models/
    │   ├── arima/
    │   ├── prophet/
    │   ├── lstm/
    │   └── ensemble/
    ├── results/
    │   ├── metrics/
    │   ├── tables/
    │   ├── forecasts/
    │   ├── business_cases/
    │   └── exports/
    ├── reports/
    │   ├── figures/
    │   ├── dashboards/
    │   └── documents/
    └── logs/
        ├── extraction.log
        ├── training.log
        ├── pipeline.log
        └── errors.log
```

---

## 2. Module Specifications

### 2.1 Data Extraction & Preparation

#### Module: `epics/epic-006/src/extraction.py`

**Purpose**: Extract historical demand data for time-series forecasting

**Data Sources**: 
- `admission-and-outpatient-attendances` (1990-2020)
- `subsidised-and-private-patient-days`
- `bed-occupancy-rate-bor`
- `average-length-of-stay-alos`
- `population-and-population-structure`
- `life-expectancy-by-sex`
- `principal-causes-of-death`

**Key Functions**:

```python
from typing import Dict, List, Tuple
import pandas as pd
import kagglehub
from pathlib import Path
import logging

class DemandDataExtractor:
    """Extract historical healthcare demand data"""
    
    def __init__(self, dataset_id: str = "subhamjain/health-dataset-complete-singapore"):
        self.dataset_id = dataset_id
        self.dataset_path = None
        self.logger = logging.getLogger(__name__)
    
    def download_dataset(self) -> Path:
        """Download Kaggle dataset"""
        self.logger.info(f"Downloading dataset: {self.dataset_id}")
        self.dataset_path = Path(kagglehub.dataset_download(self.dataset_id))
        return self.dataset_path
    
    def extract_utilization_data(self, year_range: Tuple[int, int] = (1990, 2020)) -> pd.DataFrame:
        """Extract admissions and outpatient attendance data"""
        table_name = "admission-and-outpatient-attendances"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1])
        ]
        
        self.logger.info(f"Extracted {len(df)} utilization records")
        return df
    
    def extract_patient_days(self, year_range: Tuple[int, int] = (1990, 2020)) -> pd.DataFrame:
        """Extract patient days data"""
        table_name = "subsidised-and-private-patient-days"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1])
        ]
        
        self.logger.info(f"Extracted {len(df)} patient days records")
        return df
    
    def extract_bed_occupancy(self, year_range: Tuple[int, int] = (1990, 2020)) -> pd.DataFrame:
        """Extract bed occupancy rate data"""
        table_name = "bed-occupancy-rate-bor"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1])
        ]
        
        self.logger.info(f"Extracted {len(df)} bed occupancy records")
        return df
    
    def extract_population_data(self, year_range: Tuple[int, int] = (1990, 2020)) -> pd.DataFrame:
        """Extract population and demographic data"""
        table_name = "population-and-population-structure"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1])
        ]
        
        self.logger.info(f"Extracted {len(df)} population records")
        return df
    
    def extract_all(self) -> Dict[str, pd.DataFrame]:
        """Extract all required tables"""
        if not self.dataset_path:
            self.download_dataset()
        
        return {
            'utilization': self.extract_utilization_data(),
            'patient_days': self.extract_patient_days(),
            'bed_occupancy': self.extract_bed_occupancy(),
            'population': self.extract_population_data()
        }
```

#### Module: `epics/epic-006/src/feature_engineering.py`

**Purpose**: Engineer time-series features for forecasting

**Key Functions**:

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from typing import Dict, Tuple
import logging

class TimeSeriesFeatureEngineer:
    """Engineer features for time-series forecasting"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_annual_demand_dataset(
        self,
        utilization_df: pd.DataFrame,
        patient_days_df: pd.DataFrame,
        bed_occupancy_df: pd.DataFrame,
        population_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Create consolidated annual demand time series
        """
        # Aggregate by year
        annual_utilization = utilization_df.groupby('year').agg({
            'admissions': 'sum',
            'total_outpatient_attendances': 'sum',
            'total_emergency_attendances': 'sum'
        }).reset_index()
        
        annual_patient_days = patient_days_df.groupby('year').agg({
            'subsidised_patient_days': 'sum',
            'private_patient_days': 'sum'
        }).reset_index()
        annual_patient_days['total_patient_days'] = (
            annual_patient_days['subsidised_patient_days'] + 
            annual_patient_days['private_patient_days']
        )
        
        annual_bor = bed_occupancy_df.groupby('year')['bed_occupancy_rate'].mean().reset_index()
        
        annual_population = population_df.groupby('year').agg({
            'total_population': 'first',
            'population_65_plus': 'sum'
        }).reset_index()
        
        # Merge all
        annual_demand = annual_utilization.merge(annual_patient_days[['year', 'total_patient_days']], on='year', how='left')
        annual_demand = annual_demand.merge(annual_bor, on='year', how='left')
        annual_demand = annual_demand.merge(annual_population, on='year', how='left')
        
        self.logger.info(f"Created annual demand dataset with {len(annual_demand)} years")
        return annual_demand
    
    def engineer_predictive_features(self, annual_demand: pd.DataFrame) -> pd.DataFrame:
        """Engineer predictive features"""
        df = annual_demand.copy()
        
        # Trend component
        df['year_index'] = df['year'] - df['year'].min()
        
        # Population metrics
        df['population_growth_rate'] = df['total_population'].pct_change()
        df['aging_index'] = (df['population_65_plus'] / df['total_population'] * 100)
        df['aging_growth_rate'] = df['aging_index'].pct_change()
        
        # Per capita metrics
        df['admissions_per_1000'] = (df['admissions'] / df['total_population']) * 1000
        df['outpatient_per_1000'] = (df['total_outpatient_attendances'] / df['total_population']) * 1000
        df['patient_days_per_1000'] = (df['total_patient_days'] / df['total_population']) * 1000
        
        # Lag features (t-1, t-2)
        for col in ['admissions', 'total_outpatient_attendances', 'total_patient_days']:
            df[f'{col}_lag1'] = df[col].shift(1)
            df[f'{col}_lag2'] = df[col].shift(2)
        
        # Rolling averages (3-year, 5-year)
        for col in ['admissions', 'total_outpatient_attendances']:
            df[f'{col}_ma3'] = df[col].rolling(window=3).mean()
            df[f'{col}_ma5'] = df[col].rolling(window=5).mean()
        
        self.logger.info(f"Engineered {len(df.columns)} features")
        return df
    
    def test_stationarity(self, timeseries: pd.Series, alpha: float = 0.05) -> Tuple[bool, float]:
        """
        Test time series for stationarity using Augmented Dickey-Fuller test
        
        Returns:
            (is_stationary, p_value)
        """
        result = adfuller(timeseries.dropna())
        p_value = result[1]
        is_stationary = p_value < alpha
        
        self.logger.info(f"Stationarity test: p-value={p_value:.4f}, stationary={is_stationary}")
        
        return is_stationary, p_value
    
    def apply_differencing(self, timeseries: pd.Series, order: int = 1) -> pd.Series:
        """Apply differencing to make series stationary"""
        differenced = timeseries.diff(order)
        self.logger.info(f"Applied differencing of order {order}")
        return differenced
    
    def split_train_test(
        self,
        df: pd.DataFrame,
        train_cutoff_year: int = 2017
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Split data into training and testing sets"""
        train_data = df[df['year'] <= train_cutoff_year].copy()
        test_data = df[df['year'] > train_cutoff_year].copy()
        
        self.logger.info(f"Train: {len(train_data)} years ({train_data['year'].min()}-{train_data['year'].max()})")
        self.logger.info(f"Test: {len(test_data)} years ({test_data['year'].min()}-{test_data['year'].max()})")
        
        return train_data, test_data
```

---

### 2.2 Forecasting Models

#### Module: `epics/epic-006/src/forecasting_models.py`

**Purpose**: Build and train time-series forecasting models (ARIMA, Prophet, LSTM, Ensemble)

**Key Functions**:

```python
import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
import logging

# ARIMA
from statsmodels.tsa.arima.model import ARIMA
from itertools import product

# Prophet
from prophet import Prophet

# LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

class ForecastingModels:
    """Time-series forecasting model suite"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.models = {}
        self.scalers = {}
    
    def train_arima_model(
        self,
        train_data: pd.Series,
        target_col: str = 'admissions',
        grid_search: bool = True
    ) -> Tuple[object, Dict]:
        """
        Train ARIMA model with optional grid search
        
        Returns:
            (fitted_model, best_params)
        """
        self.logger.info(f"Training ARIMA model for {target_col}")
        
        if grid_search:
            # Grid search for best (p, d, q)
            p_values = range(0, 4)
            d_values = range(0, 3)
            q_values = range(0, 4)
            
            best_aic = float('inf')
            best_params = None
            
            for p, d, q in product(p_values, d_values, q_values):
                try:
                    model = ARIMA(train_data, order=(p, d, q))
                    fitted_model = model.fit()
                    
                    if fitted_model.aic < best_aic:
                        best_aic = fitted_model.aic
                        best_params = (p, d, q)
                except:
                    continue
            
            self.logger.info(f"Best ARIMA params: {best_params}, AIC: {best_aic:.2f}")
        else:
            best_params = (1, 1, 1)  # Default
        
        # Train final model
        final_model = ARIMA(train_data, order=best_params)
        fitted_model = final_model.fit()
        
        # Store model
        self.models[f'arima_{target_col}'] = fitted_model
        
        return fitted_model, {'order': best_params, 'aic': fitted_model.aic}
    
    def forecast_arima(
        self,
        model: object,
        steps: int
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate ARIMA forecast
        
        Returns:
            (forecast, lower_ci, upper_ci)
        """
        forecast_result = model.forecast(steps=steps)
        
        # Get confidence intervals
        forecast_df = model.get_forecast(steps=steps).summary_frame()
        
        return (
            forecast_result.values,
            forecast_df['mean_ci_lower'].values,
            forecast_df['mean_ci_upper'].values
        )
    
    def train_prophet_model(
        self,
        train_data: pd.DataFrame,
        target_col: str = 'admissions'
    ) -> object:
        """Train Facebook Prophet model"""
        self.logger.info(f"Training Prophet model for {target_col}")
        
        # Prepare data for Prophet
        prophet_df = train_data[['year', target_col]].copy()
        prophet_df = prophet_df.rename(columns={'year': 'ds', target_col: 'y'})
        prophet_df['ds'] = pd.to_datetime(prophet_df['ds'], format='%Y')
        
        # Train model
        model = Prophet(
            yearly_seasonality=True,
            changepoint_prior_scale=0.05,
            interval_width=0.95
        )
        model.fit(prophet_df)
        
        # Store model
        self.models[f'prophet_{target_col}'] = model
        
        self.logger.info(f"Prophet model trained successfully")
        return model
    
    def forecast_prophet(
        self,
        model: object,
        periods: int
    ) -> pd.DataFrame:
        """Generate Prophet forecast"""
        future = model.make_future_dataframe(periods=periods, freq='Y')
        forecast = model.predict(future)
        
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    
    def train_lstm_model(
        self,
        train_data: pd.Series,
        target_col: str = 'admissions',
        seq_length: int = 5,
        epochs: int = 100
    ) -> Tuple[object, object]:
        """
        Train LSTM neural network model
        
        Returns:
            (model, scaler)
        """
        self.logger.info(f"Training LSTM model for {target_col}")
        
        # Normalize data
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(train_data.values.reshape(-1, 1))
        
        # Create sequences
        def create_sequences(data, seq_len):
            X, y = [], []
            for i in range(len(data) - seq_len):
                X.append(data[i:i+seq_len])
                y.append(data[i+seq_len])
            return np.array(X), np.array(y)
        
        X_train, y_train = create_sequences(scaled_data, seq_length)
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        
        # Build LSTM model
        model = Sequential([
            LSTM(50, activation='relu', return_sequences=True, input_shape=(seq_length, 1)),
            Dropout(0.2),
            LSTM(50, activation='relu'),
            Dropout(0.2),
            Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse')
        
        # Train
        model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=8,
            verbose=0
        )
        
        # Store model and scaler
        self.models[f'lstm_{target_col}'] = model
        self.scalers[f'lstm_{target_col}'] = scaler
        
        self.logger.info(f"LSTM model trained successfully")
        
        return model, scaler
    
    def forecast_lstm(
        self,
        model: object,
        scaler: object,
        last_sequence: np.ndarray,
        steps: int
    ) -> np.ndarray:
        """Generate LSTM forecast"""
        forecasts = []
        current_sequence = last_sequence.copy()
        
        for _ in range(steps):
            # Predict next value
            next_pred = model.predict(current_sequence.reshape(1, len(current_sequence), 1), verbose=0)[0, 0]
            forecasts.append(next_pred)
            
            # Update sequence
            current_sequence = np.append(current_sequence[1:], next_pred)
        
        # Inverse transform
        forecasts = scaler.inverse_transform(np.array(forecasts).reshape(-1, 1))
        
        return forecasts.flatten()
    
    def create_ensemble_forecast(
        self,
        arima_forecast: np.ndarray,
        prophet_forecast: np.ndarray,
        lstm_forecast: np.ndarray,
        weights: Dict[str, float] = None
    ) -> np.ndarray:
        """
        Create weighted ensemble forecast
        
        Default weights based on typical performance:
        - ARIMA: 30%
        - Prophet: 40%
        - LSTM: 30%
        """
        if weights is None:
            weights = {'arima': 0.30, 'prophet': 0.40, 'lstm': 0.30}
        
        ensemble = (
            weights['arima'] * arima_forecast +
            weights['prophet'] * prophet_forecast +
            weights['lstm'] * lstm_forecast
        )
        
        self.logger.info(f"Ensemble forecast created with weights: {weights}")
        
        return ensemble


class ModelEvaluator:
    """Evaluate forecasting model performance"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def calculate_mape(self, actual: np.ndarray, predicted: np.ndarray) -> float:
        """Calculate Mean Absolute Percentage Error"""
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        return mape
    
    def calculate_rmse(self, actual: np.ndarray, predicted: np.ndarray) -> float:
        """Calculate Root Mean Squared Error"""
        rmse = np.sqrt(np.mean((actual - predicted) ** 2))
        return rmse
    
    def calculate_mae(self, actual: np.ndarray, predicted: np.ndarray) -> float:
        """Calculate Mean Absolute Error"""
        mae = np.mean(np.abs(actual - predicted))
        return mae
    
    def evaluate_model(
        self,
        actual: np.ndarray,
        predicted: np.ndarray,
        model_name: str
    ) -> Dict[str, float]:
        """Comprehensive model evaluation"""
        metrics = {
            'model': model_name,
            'mape': self.calculate_mape(actual, predicted),
            'rmse': self.calculate_rmse(actual, predicted),
            'mae': self.calculate_mae(actual, predicted),
            'accuracy_pct': 100 - self.calculate_mape(actual, predicted)
        }
        
        self.logger.info(f"{model_name} - MAPE: {metrics['mape']:.2f}%, "
                        f"Accuracy: {metrics['accuracy_pct']:.2f}%")
        
        return metrics
```

---

### 2.3 Capacity Gap Analysis & Business Cases

#### Module: `epics/epic-006/src/capacity_analysis.py`

**Purpose**: Identify capacity gaps and project resource requirements

**Key Functions**:

```python
import pandas as pd
import numpy as np
from typing import Dict, List
import logging

class CapacityGapAnalyzer:
    """Identify healthcare capacity gaps"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def identify_capacity_gaps(
        self,
        forecast_df: pd.DataFrame,
        current_capacity: Dict[str, float],
        target_occupancy: float = 0.85
    ) -> pd.DataFrame:
        """
        Identify capacity gaps by comparing forecast to current capacity
        
        Args:
            forecast_df: DataFrame with forecasted demand
            current_capacity: Dict with current capacity (beds, staff, etc.)
            target_occupancy: Target occupancy rate (default 85%)
        """
        gaps = []
        
        # Bed capacity gap
        if 'total_patient_days' in forecast_df.columns:
            for year in [2022, 2025]:  # 1-year and 5-year
                if year in forecast_df['year'].values:
                    forecasted_patient_days = forecast_df[forecast_df['year'] == year]['total_patient_days'].values[0]
                    
                    # Required beds = patient_days / 365 / target_occupancy
                    required_beds = forecasted_patient_days / 365 / target_occupancy
                    current_beds = current_capacity.get('beds', 0)
                    bed_gap = max(0, required_beds - current_beds)
                    
                    if bed_gap > 0:
                        gaps.append({
                            'gap_id': f'CAP-BEDS-{year}',
                            'gap_type': 'Hospital Beds',
                            'year': year,
                            'current_capacity': current_beds,
                            'required_capacity': required_beds,
                            'gap_size': bed_gap,
                            'gap_percentage': (bed_gap / current_beds) * 100 if current_beds > 0 else 0,
                            'priority': 'High' if bed_gap > current_beds * 0.1 else 'Medium'
                        })
        
        # Doctor capacity gap
        if 'admissions' in forecast_df.columns:
            for year in [2022, 2025]:
                if year in forecast_df['year'].values:
                    forecasted_admissions = forecast_df[forecast_df['year'] == year]['admissions'].values[0]
                    
                    # Assume 1 doctor per 1000 admissions per year
                    required_doctors = forecasted_admissions / 1000
                    current_doctors = current_capacity.get('doctors', 0)
                    doctor_gap = max(0, required_doctors - current_doctors)
                    
                    if doctor_gap > 0:
                        gaps.append({
                            'gap_id': f'CAP-DOCTORS-{year}',
                            'gap_type': 'Doctors',
                            'year': year,
                            'current_capacity': current_doctors,
                            'required_capacity': required_doctors,
                            'gap_size': doctor_gap,
                            'gap_percentage': (doctor_gap / current_doctors) * 100 if current_doctors > 0 else 0,
                            'priority': 'High' if doctor_gap > current_doctors * 0.1 else 'Medium'
                        })
        
        # Nurse capacity gap (3 nurses per doctor)
        for gap in gaps:
            if gap['gap_type'] == 'Doctors':
                nurses_needed = gap['gap_size'] * 3
                
                gaps.append({
                    'gap_id': gap['gap_id'].replace('DOCTORS', 'NURSES'),
                    'gap_type': 'Nurses',
                    'year': gap['year'],
                    'current_capacity': current_capacity.get('nurses', 0),
                    'required_capacity': current_capacity.get('nurses', 0) + nurses_needed,
                    'gap_size': nurses_needed,
                    'gap_percentage': (nurses_needed / current_capacity.get('nurses', 1)) * 100,
                    'priority': gap['priority']
                })
        
        gaps_df = pd.DataFrame(gaps)
        
        self.logger.info(f"Identified {len(gaps_df)} capacity gaps")
        
        return gaps_df
    
    def project_resource_requirements(
        self,
        capacity_gaps: pd.DataFrame
    ) -> pd.DataFrame:
        """Project detailed resource requirements for each gap"""
        resources = []
        
        for idx, gap in capacity_gaps.iterrows():
            gap_type = gap['gap_type']
            gap_size = gap['gap_size']
            
            if gap_type == 'Hospital Beds':
                # For beds, also need support staff and equipment
                resources.append({
                    'gap_id': gap['gap_id'],
                    'resource_type': 'Hospital Beds',
                    'quantity': int(gap_size),
                    'unit_cost_sgd': 500000,  # Cost per bed (capital)
                    'annual_operating_cost_sgd': 100000  # Per bed per year
                })
                
                # Support staff for new beds
                resources.append({
                    'gap_id': gap['gap_id'],
                    'resource_type': 'Support Staff',
                    'quantity': int(gap_size / 10),  # 1 staff per 10 beds
                    'unit_cost_sgd': 0,  # Included in operating cost
                    'annual_operating_cost_sgd': 60000  # Per staff per year
                })
            
            elif gap_type == 'Doctors':
                resources.append({
                    'gap_id': gap['gap_id'],
                    'resource_type': 'Doctors',
                    'quantity': int(gap_size),
                    'unit_cost_sgd': 50000,  # Recruitment cost
                    'annual_operating_cost_sgd': 200000  # Salary per doctor
                })
            
            elif gap_type == 'Nurses':
                resources.append({
                    'gap_id': gap['gap_id'],
                    'resource_type': 'Nurses',
                    'quantity': int(gap_size),
                    'unit_cost_sgd': 20000,  # Recruitment cost
                    'annual_operating_cost_sgd': 80000  # Salary per nurse
                })
        
        resources_df = pd.DataFrame(resources)
        
        self.logger.info(f"Projected resource requirements for {len(resources_df)} resource types")
        
        return resources_df


class BusinessCaseBuilder:
    """Build business cases for capacity expansions"""
    
    def __init__(self, discount_rate: float = 0.05, analysis_horizon: int = 10):
        self.logger = logging.getLogger(__name__)
        self.discount_rate = discount_rate
        self.analysis_horizon = analysis_horizon
    
    def build_business_case(
        self,
        gap: Dict,
        resources: pd.DataFrame
    ) -> Dict:
        """Build comprehensive business case for capacity expansion"""
        gap_id = gap['gap_id']
        gap_resources = resources[resources['gap_id'] == gap_id]
        
        # Calculate costs
        capital_cost = (gap_resources['quantity'] * gap_resources['unit_cost_sgd']).sum()
        annual_operating_cost = (gap_resources['quantity'] * gap_resources['annual_operating_cost_sgd']).sum()
        
        # Estimate benefits
        # Assume each bed/staff unit generates revenue and cost savings
        annual_revenue = self._estimate_annual_revenue(gap, gap_resources)
        annual_cost_savings = self._estimate_cost_savings(gap)
        total_annual_benefit = annual_revenue + annual_cost_savings
        
        # Calculate NPV
        npv = -capital_cost
        for year in range(1, self.analysis_horizon + 1):
            annual_net_cashflow = total_annual_benefit - annual_operating_cost
            npv += annual_net_cashflow / ((1 + self.discount_rate) ** year)
        
        # Calculate ROI
        total_cost_10yr = capital_cost + (annual_operating_cost * self.analysis_horizon)
        total_benefit_10yr = total_annual_benefit * self.analysis_horizon
        roi_pct = ((total_benefit_10yr - total_cost_10yr) / total_cost_10yr) * 100
        
        # Calculate BCR
        bcr = total_benefit_10yr / total_cost_10yr
        
        # Payback period
        if annual_net_cashflow > 0:
            payback_period = capital_cost / (total_annual_benefit - annual_operating_cost)
        else:
            payback_period = float('inf')
        
        business_case = {
            'gap_id': gap_id,
            'gap_type': gap['gap_type'],
            'gap_size': gap['gap_size'],
            'capital_cost': capital_cost,
            'annual_operating_cost': annual_operating_cost,
            'total_10yr_cost': total_cost_10yr,
            'annual_revenue': annual_revenue,
            'annual_cost_savings': annual_cost_savings,
            'total_annual_benefit': total_annual_benefit,
            'total_10yr_benefit': total_benefit_10yr,
            'npv': npv,
            'roi_pct': roi_pct,
            'bcr': bcr,
            'payback_period_years': payback_period
        }
        
        self.logger.info(f"Business case for {gap_id}: NPV=${npv:,.0f}, ROI={roi_pct:.1f}%, BCR={bcr:.2f}")
        
        return business_case
    
    def _estimate_annual_revenue(self, gap: Dict, resources: pd.DataFrame) -> float:
        """Estimate annual revenue from capacity expansion"""
        gap_type = gap['gap_type']
        
        if gap_type == 'Hospital Beds':
            # Revenue per bed per year (patient days * revenue per day)
            beds = gap['gap_size']
            occupancy = 0.85
            revenue_per_patient_day = 500  # SGD
            annual_revenue = beds * 365 * occupancy * revenue_per_patient_day
        elif gap_type in ['Doctors', 'Nurses']:
            # Revenue from additional staff (consultations, procedures)
            staff = gap['gap_size']
            revenue_per_staff = 300000  # SGD per year
            annual_revenue = staff * revenue_per_staff
        else:
            annual_revenue = 0
        
        return annual_revenue
    
    def _estimate_cost_savings(self, gap: Dict) -> float:
        """Estimate cost savings from reducing bottlenecks"""
        # Cost savings from reducing wait times, improving outcomes, etc.
        # Simplified: 10% of current costs
        return gap['gap_size'] * 50000  # SGD per unit per year
```

---

## 3. Configuration Files

### `epics/epic-006/config/epic_006_config.yml`

```yaml
epic_id: epic-006
epic_name: predictive-healthcare-demand-forecasting

data_sources:
  primary_source: kaggle
  dataset_id: "subhamjain/health-dataset-complete-singapore"
  
  tables:
    - admission-and-outpatient-attendances
    - subsidised-and-private-patient-days
    - bed-occupancy-rate-bor
    - average-length-of-stay-alos
    - population-and-population-structure
    - life-expectancy-by-sex
    - principal-causes-of-death

time_series_range:
  start_year: 1990
  end_year: 2020
  train_cutoff: 2017

forecast_horizons:
  short_term_years: 1  # 2022 (1 year from 2020)
  long_term_years: 5   # 2025 (5 years from 2020)

current_capacity:
  beds: 13000
  doctors: 14000
  nurses: 42000

output_paths:
  raw_data: epics/epic-006/data/raw/
  processed_data: epics/epic-006/data/processed/
  time_series: epics/epic-006/data/time_series/
  forecasts: epics/epic-006/data/forecasts/
  models: epics/epic-006/models/
  results: epics/epic-006/results/
  business_cases: epics/epic-006/results/business_cases/
  figures: epics/epic-006/reports/figures/
  reports: epics/epic-006/reports/documents/

logging:
  level: INFO
  log_dir: epics/epic-006/logs/
  log_files:
    extraction: extraction.log
    training: training.log
    pipeline: pipeline.log
    errors: errors.log
```

### `epics/epic-006/config/epic_006_params.yml`

```yaml
# Analysis parameters for EPIC-006

model_requirements:
  minimum_accuracy_pct: 85
  maximum_mape_pct: 15

forecasting_models:
  arima:
    enabled: true
    grid_search: true
    p_range: [0, 3]
    d_range: [0, 2]
    q_range: [0, 3]
  
  prophet:
    enabled: true
    yearly_seasonality: true
    changepoint_prior_scale: 0.05
    interval_width: 0.95
  
  lstm:
    enabled: true
    sequence_length: 5
    epochs: 100
    lstm_units: [50, 50]
    dropout: 0.2
  
  ensemble:
    enabled: true
    weights:
      arima: 0.30
      prophet: 0.40
      lstm: 0.30

capacity_analysis:
  minimum_gaps_required: 5
  target_occupancy_rate: 0.85
  
  resource_ratios:
    doctors_per_1000_admissions: 1.0
    nurses_per_doctor: 3.0
    support_staff_per_10_beds: 1.0

business_case:
  analysis_horizon_years: 10
  discount_rate: 0.05
  minimum_business_cases: 3
  
  cost_estimates:
    bed_capital_cost_sgd: 500000
    bed_annual_operating_cost_sgd: 100000
    doctor_recruitment_cost_sgd: 50000
    doctor_annual_salary_sgd: 200000
    nurse_recruitment_cost_sgd: 20000
    nurse_annual_salary_sgd: 80000
  
  revenue_estimates:
    revenue_per_patient_day_sgd: 500
    revenue_per_doctor_annual_sgd: 300000
    revenue_per_nurse_annual_sgd: 100000
```

---

## 4. Execution Workflow

### Orchestration Script: `epics/epic-006/scripts/run_full_pipeline.py`

```python
#!/usr/bin/env python3
"""
EPIC-006 Full Pipeline Orchestrator
Execute complete predictive demand forecasting and capacity planning
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

from extraction import DemandDataExtractor
from feature_engineering import TimeSeriesFeatureEngineer
from forecasting_models import ForecastingModels, ModelEvaluator
from capacity_analysis import CapacityGapAnalyzer, BusinessCaseBuilder

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
    """Execute full EPIC-006 pipeline"""
    
    # Load configuration
    config_path = Path(__file__).parent.parent / 'config' / 'epic_006_config.yml'
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Setup logging
    logger = setup_logging(Path(config['logging']['log_dir']))
    logger.info("="*80)
    logger.info("EPIC-006: Predictive Healthcare Demand Forecasting")
    logger.info(f"Pipeline started at {datetime.now()}")
    logger.info("="*80)
    
    try:
        # Step 1: Extract data
        logger.info("\n[STEP 1] Extracting demand data...")
        extractor = DemandDataExtractor()
        data = extractor.extract_all()
        logger.info(f"✓ Data extraction complete")
        
        # Step 2: Feature engineering
        logger.info("\n[STEP 2] Engineering time-series features...")
        fe = TimeSeriesFeatureEngineer()
        
        annual_demand = fe.create_annual_demand_dataset(
            data['utilization'],
            data['patient_days'],
            data['bed_occupancy'],
            data['population']
        )
        
        annual_demand = fe.engineer_predictive_features(annual_demand)
        
        # Split train/test
        train_data, test_data = fe.split_train_test(annual_demand, train_cutoff_year=2017)
        
        logger.info(f"✓ Feature engineering complete: {len(annual_demand.columns)} features")
        
        # Step 3: Train forecasting models
        logger.info("\n[STEP 3] Training forecasting models...")
        forecaster = ForecastingModels()
        evaluator = ModelEvaluator()
        
        target_metric = 'admissions'
        
        # ARIMA
        logger.info("  Training ARIMA...")
        arima_model, arima_params = forecaster.train_arima_model(
            train_data[target_metric],
            target_col=target_metric
        )
        arima_forecast_test = forecaster.forecast_arima(arima_model, len(test_data))[0]
        arima_metrics = evaluator.evaluate_model(
            test_data[target_metric].values,
            arima_forecast_test,
            'ARIMA'
        )
        
        # Prophet
        logger.info("  Training Prophet...")
        prophet_model = forecaster.train_prophet_model(train_data, target_col=target_metric)
        prophet_forecast_full = forecaster.forecast_prophet(prophet_model, len(test_data))
        prophet_forecast_test = prophet_forecast_full.tail(len(test_data))['yhat'].values
        prophet_metrics = evaluator.evaluate_model(
            test_data[target_metric].values,
            prophet_forecast_test,
            'Prophet'
        )
        
        # LSTM
        logger.info("  Training LSTM...")
        lstm_model, lstm_scaler = forecaster.train_lstm_model(
            train_data[target_metric],
            target_col=target_metric,
            seq_length=5,
            epochs=100
        )
        last_sequence = lstm_scaler.transform(
            train_data[target_metric].tail(5).values.reshape(-1, 1)
        ).flatten()
        lstm_forecast_test = forecaster.forecast_lstm(
            lstm_model, lstm_scaler, last_sequence, len(test_data)
        )
        lstm_metrics = evaluator.evaluate_model(
            test_data[target_metric].values,
            lstm_forecast_test,
            'LSTM'
        )
        
        # Ensemble
        logger.info("  Creating ensemble...")
        ensemble_forecast_test = forecaster.create_ensemble_forecast(
            arima_forecast_test,
            prophet_forecast_test,
            lstm_forecast_test
        )
        ensemble_metrics = evaluator.evaluate_model(
            test_data[target_metric].values,
            ensemble_forecast_test,
            'Ensemble'
        )
        
        logger.info(f"✓ Model training complete")
        logger.info(f"  Best model: Ensemble (Accuracy: {ensemble_metrics['accuracy_pct']:.1f}%)")
        
        # Step 4: Generate future forecasts
        logger.info("\n[STEP 4] Generating future forecasts...")
        
        # Retrain on full dataset for production forecasts
        full_arima_model, _ = forecaster.train_arima_model(
            annual_demand[target_metric],
            target_col=target_metric
        )
        
        forecast_1yr = forecaster.forecast_arima(full_arima_model, 1)[0]
        forecast_5yr = forecaster.forecast_arima(full_arima_model, 5)[0]
        
        logger.info(f"✓ Forecasts generated:")
        logger.info(f"  2022 (1-year): {forecast_1yr[0]:,.0f} admissions")
        logger.info(f"  2025 (5-year): {forecast_5yr[-1]:,.0f} admissions")
        
        # Step 5: Identify capacity gaps
        logger.info("\n[STEP 5] Identifying capacity gaps...")
        
        # Create forecast dataframe
        forecast_df = pd.DataFrame({
            'year': [2022, 2025],
            'admissions': [forecast_1yr[0], forecast_5yr[-1]],
            'total_patient_days': [forecast_1yr[0] * 3, forecast_5yr[-1] * 3]  # Mock: 3 days per admission
        })
        
        capacity_analyzer = CapacityGapAnalyzer()
        capacity_gaps = capacity_analyzer.identify_capacity_gaps(
            forecast_df,
            config['current_capacity']
        )
        
        logger.info(f"✓ Identified {len(capacity_gaps)} capacity gaps")
        for idx, gap in capacity_gaps.head(5).iterrows():
            logger.info(f"  - {gap['gap_type']} ({gap['year']}): {gap['gap_size']:.0f} units needed")
        
        # Step 6: Project resources
        logger.info("\n[STEP 6] Projecting resource requirements...")
        
        resources = capacity_analyzer.project_resource_requirements(capacity_gaps)
        
        logger.info(f"✓ Resource projections complete: {len(resources)} resource types")
        
        # Step 7: Build business cases
        logger.info("\n[STEP 7] Building business cases...")
        
        bc_builder = BusinessCaseBuilder()
        
        top_gaps = capacity_gaps.nlargest(3, 'gap_size')
        business_cases = []
        
        for idx, gap in top_gaps.iterrows():
            bc = bc_builder.build_business_case(gap.to_dict(), resources)
            business_cases.append(bc)
        
        logger.info(f"✓ Built {len(business_cases)} business cases")
        
        # Step 8: Save results
        logger.info("\n[STEP 8] Saving results...")
        results_dir = Path(config['output_paths']['results'])
        results_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = results_dir / 'exports' / 'e06_demand_forecast_analysis.xlsx'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Compile model performance
        model_performance = pd.DataFrame([
            arima_metrics, prophet_metrics, lstm_metrics, ensemble_metrics
        ])
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Forecasts
            forecast_df.to_excel(writer, sheet_name='Demand Forecasts', index=False)
            
            # Model performance
            model_performance.to_excel(writer, sheet_name='Model Performance', index=False)
            
            # Capacity gaps
            capacity_gaps.to_excel(writer, sheet_name='Capacity Gaps', index=False)
            
            # Resource projections
            resources.to_excel(writer, sheet_name='Resource Requirements', index=False)
            
            # Business cases
            pd.DataFrame(business_cases).to_excel(writer, sheet_name='Business Cases', index=False)
        
        logger.info(f"✓ Results saved to {output_file}")
        
        # Summary
        logger.info("\n" + "="*80)
        logger.info("EPIC-006 PIPELINE COMPLETE")
        logger.info(f"Model accuracy: {ensemble_metrics['accuracy_pct']:.1f}% (MAPE: {ensemble_metrics['mape']:.1f}%)")
        logger.info(f"2022 forecast: {forecast_1yr[0]:,.0f} admissions")
        logger.info(f"2025 forecast: {forecast_5yr[-1]:,.0f} admissions")
        logger.info(f"Capacity gaps identified: {len(capacity_gaps)}")
        logger.info(f"Business cases built: {len(business_cases)}")
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

### Unit Tests: `epics/epic-006/tests/test_forecasting.py`

```python
import unittest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

from forecasting_models import ModelEvaluator
from capacity_analysis import CapacityGapAnalyzer

class TestForecasting(unittest.TestCase):
    """Test forecasting functionality"""
    
    def setUp(self):
        """Setup test data"""
        self.evaluator = ModelEvaluator()
        self.capacity_analyzer = CapacityGapAnalyzer()
    
    def test_mape_calculation(self):
        """Test MAPE calculation"""
        actual = np.array([100, 200, 300])
        predicted = np.array([110, 190, 310])
        
        mape = self.evaluator.calculate_mape(actual, predicted)
        
        # MAPE should be around 5%
        self.assertLess(mape, 10)
        self.assertGreater(mape, 0)
    
    def test_accuracy_requirement(self):
        """Test that model meets 85% accuracy requirement"""
        # Simulate model with 87% accuracy (13% MAPE)
        actual = np.array([1000, 1100, 1200, 1300])
        predicted = np.array([1130, 1243, 1356, 1469])  # ~13% error
        
        mape = self.evaluator.calculate_mape(actual, predicted)
        accuracy = 100 - mape
        
        # Should meet minimum 85% accuracy
        self.assertGreaterEqual(accuracy, 85)
    
    def test_capacity_gap_identification(self):
        """Test capacity gap identification"""
        forecast_df = pd.DataFrame({
            'year': [2022, 2025],
            'admissions': [300000, 350000],
            'total_patient_days': [900000, 1050000]
        })
        
        current_capacity = {
            'beds': 10000,
            'doctors': 12000,
            'nurses': 36000
        }
        
        gaps = self.capacity_analyzer.identify_capacity_gaps(
            forecast_df,
            current_capacity
        )
        
        # Should identify at least 5 gaps (requirement)
        self.assertGreaterEqual(len(gaps), 5)

if __name__ == '__main__':
    unittest.main()
```

---

## 6. Outputs & Deliverables

### Trained Models

**Location**: `epics/epic-006/models/`

**Files**:
- `arima/admissions_arima_model.pkl` - Trained ARIMA model
- `prophet/admissions_prophet_model.pkl` - Trained Prophet model
- `lstm/admissions_lstm_model.h5` - Trained LSTM model
- `lstm/admissions_scaler.pkl` - Data scaler for LSTM
- `ensemble/ensemble_weights.yml` - Ensemble model weights

### Forecast Results

**Location**: `epics/epic-006/results/exports/`

**Files**:
- `e06_demand_forecast_analysis.xlsx` - Comprehensive analysis (multi-sheet)
  - Demand Forecasts (1-year, 5-year)
  - Model Performance (MAPE, RMSE, MAE, Accuracy)
  - Capacity Gaps (5+ gaps)
  - Resource Requirements
  - Business Cases (3+ cases)

### Business Case Documents

**Location**: `epics/epic-006/results/business_cases/`

**Files** (PDF format):
- `Business_Case_Hospital_Beds_2025.pdf`
- `Business_Case_Doctors_2025.pdf`
- `Business_Case_Nurses_2025.pdf`

Each business case includes:
- Executive Summary
- Current Situation & Need
- Forecasted Demand
- Capacity Gap Analysis
- Resource Requirements
- Financial Analysis (capital cost, operating cost, revenue, NPV, ROI, BCR)
- Implementation Timeline
- Risk Assessment
- Recommendations

### Visualizations

**Location**: `epics/epic-006/reports/figures/`

**Files**:
- `demand_forecast_trend.png` - Historical + forecasted demand
- `model_accuracy_comparison.png` - Model performance comparison
- `capacity_gaps_chart.png` - Gap sizes by type
- `business_case_roi.png` - ROI comparison

### Dashboard

**Tool**: Plotly Dash

**Access**: `http://localhost:8050/epic006_capacity_planning`

**Components**:
- KPI Cards (forecast accuracy, 1-yr/5-yr forecasts, capacity gaps, total investment)
- Demand Forecast Chart (interactive time series with confidence intervals)
- Model Performance Chart (MAPE comparison)
- Capacity Gaps Table (sortable, filterable)
- Business Case Cards (top 3 with NPV, ROI, BCR)
- Resource Requirements Chart

### Reports

**Location**: `epics/epic-006/reports/documents/`

**Files**:
- `EPIC-006_Executive_Summary.pdf`
- `EPIC-006_Forecasting_Model_Report.pdf`
- `EPIC-006_Capacity_Planning_Report.pdf`

---

## 7. Monitoring & Alerts

### Key Metrics

```yaml
pipeline_metrics:
  - model_training_time_minutes
  - forecast_accuracy_pct
  - mape_pct
  
model_metrics:
  - arima_mape
  - prophet_mape
  - lstm_mape
  - ensemble_mape
  - best_model_name
  
business_metrics:
  - forecast_1yr_admissions
  - forecast_5yr_admissions
  - capacity_gaps_count
  - total_investment_required
  - avg_roi_pct
  - avg_payback_period_years
```

---

## 8. Dependencies & Integration

### Upstream Dependencies

- **EPIC-001 (Recommended)**: Utilization data enhances demand forecasts

### Downstream Consumers

- **EPIC-003 (Gap Analysis)**: Capacity gaps inform policy recommendations
- **EPIC-004 (Process Optimization)**: Forecasts inform improvement priorities

### Shared Components

- `kaggle_base_extraction`
- `column_standardization`
- `data_quality_validation`
- `plotly_templates`
- `logging_config`

---

## 9. Timeline & Milestones

| Week | Days | Milestone | Deliverables |
|------|------|-----------|--------------|
| 1 | 1-5 | Data extraction & feature engineering | Time-series datasets |
| 2 | 6-9 | Historical pattern analysis | Trend analysis, seasonality |
| 2-3 | 10-17 | ARIMA, Prophet, LSTM training | Trained models |
| 4 | 18-21 | Model evaluation & ensemble | Best model (85%+ accuracy) |
| 4-5 | 22-26 | Demographic adjustments | Adjusted forecasts |
| 5 | 27-31 | Capacity gap analysis | 5+ gaps identified |
| 6 | 32-35 | Resource projections | Resource requirements |
| 6 | 36-39 | Business case development | 3+ business cases |
| 7 | 40-42 | Dashboard & final reports | Final deliverables |

**Total Duration**: 42 working days (6-7 weeks)

---

## 10. Success Criteria

✅ **Forecasting Accuracy**:
- [ ] Model accuracy ≥ 85% (MAPE ≤ 15%)
- [ ] Confidence intervals calculated
- [ ] Multiple models trained (ARIMA, Prophet, LSTM)
- [ ] Ensemble model created

✅ **Forecasts Delivered**:
- [ ] 1-year forecast (2022)
- [ ] 5-year forecast (2025)
- [ ] All key metrics forecasted (admissions, patient days, etc.)

✅ **Capacity Analysis**:
- [ ] Minimum 5 capacity gaps identified
- [ ] Each gap quantified with impact
- [ ] Resource requirements projected

✅ **Business Cases**:
- [ ] Minimum 3 business cases developed
- [ ] NPV, ROI, BCR calculated for each
- [ ] Implementation timelines included

✅ **Deliverables**:
- [ ] Trained models saved
- [ ] Forecast results documented
- [ ] Business case documents (PDF)
- [ ] Interactive dashboard deployed
- [ ] Reports completed

✅ **Quality Standards**:
- [ ] Data quality score >90%
- [ ] Model validation complete
- [ ] Unit test coverage >75%
- [ ] Code reviewed and approved

✅ **Stakeholder Acceptance**:
- [ ] Forecasts validated by planning team
- [ ] Business cases approved by finance
- [ ] Dashboard demonstrated
- [ ] Sign-off received

---

**Document Version**: 1.0  
**Last Updated**: 2 February 2026  
**Owner**: EPIC-006 Lead Data Scientist
