# Model Training & Development Stage

## Purpose
Develop, train, and tune predictive models to address the specified analytical objectives. Select appropriate algorithms, optimize hyperparameters, and prepare models for evaluation.

## Your Role
You are a **machine learning engineer** with expertise in model selection, training pipelines, hyperparameter optimization, and experiment tracking.

---

## Inputs

Retrieve required information from the following documentation:

### 1. User Story Requirements
**Location**: `docs/objectives/user_stories/[story-id].md`

Extract:
- Model objective and business goal
- Target variable to predict
- Acceptance criteria with performance targets (e.g., "MAPE < 15%")
- Technical notes on suggested algorithms
- Estimated effort and timeline constraints

### 2. Methodology Guidelines
**Location**: `docs/methodology/model_development.md` (if exists)

Extract:
- Model selection criteria
- Training pipeline standards
- Cross-validation approaches
- Hyperparameter tuning methods
- Evaluation framework

### 3. Technical Stack
**Location**: `docs/project_context/tech_stack.md`

Extract:
- Available ML libraries and frameworks
- Experiment tracking tools (MLflow, W&B)
- Computing resources and constraints
- Model deployment requirements

### 4. Feature Documentation
**Location**: `docs/data_dictionary/features.md` (if exists)

Extract:
- Available features for training
- Feature engineering pipeline outputs
- Feature selection methods used

### 5. Analysis Configuration
**Location**: `config/analysis.yml` (if exists)

Extract:
- Model configuration parameters
- Train/validation/test split ratios
- Random seeds for reproducibility

### Determine Dynamically
- **training_dataset**: Check `data/4_processed/` for latest feature dataset
- **model_type**: Infer from user story (classification, regression, time-series, clustering)
- **evaluation_metrics**: Extract from acceptance criteria or use domain-appropriate defaults
- **output_paths**: 
  - Models: `models/trained/`
  - Logs: `results/metrics/training_experiments.csv`
  - Notebook: `notebooks/2_analysis/[story-id]_model_training.ipynb`

---

## Process

### Step 1: Setup Training Environment

Create a Jupyter notebook with MLflow experiment tracking:

```python
# %% [markdown]
# # Model Training: Daily Attendance Forecasting
# 
# **Objective**: Train and optimize models to forecast daily attendance volumes
# **Target**: MAPE < 15% on test set
# **Date**: 2026-01-28

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Model libraries
from prophet import Prophet
from statsmodels.tsa.statespace.sarimax import SARIMAX
import xgboost as xgb
from sklearn.metrics import mean_absolute_percentage_error, mean_absolute_error, mean_squared_error, r2_score

# Experiment tracking
import mlflow
import mlflow.sklearn

# Set random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Initialize MLflow
mlflow.set_experiment("attendance_forecasting")
```

### Step 2: Load and Split Data

```python
# %% [markdown]
# ## 1. Data Loading and Splitting

# %%
# Load prepared dataset
df = pd.read_parquet('data/4_processed/attendance_features.parquet')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

print(f"Dataset shape: {df.shape}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")

# %%
# Time-based split (no shuffling for time series!)
train_size = int(len(df) * 0.8)
val_size = int(len(df) * 0.1)

train_df = df.iloc[:train_size]
val_df = df.iloc[train_size:train_size+val_size]
test_df = df.iloc[train_size+val_size:]

print(f"\nTrain set: {len(train_df)} days ({train_df['date'].min()} to {train_df['date'].max()})")
print(f"Validation set: {len(val_df)} days ({val_df['date'].min()} to {val_df['date'].max()})")
print(f"Test set: {len(test_df)} days ({test_df['date'].min()} to {test_df['date'].max()})")

# Visualize split
plt.figure(figsize=(15, 5))
plt.plot(train_df['date'], train_df['daily_attendance_count'], label='Train', alpha=0.7)
plt.plot(val_df['date'], val_df['daily_attendance_count'], label='Validation', alpha=0.7)
plt.plot(test_df['date'], test_df['daily_attendance_count'], label='Test', alpha=0.7)
plt.axvline(train_df['date'].max(), color='red', linestyle='--', alpha=0.5)
plt.axvline(val_df['date'].max(), color='red', linestyle='--', alpha=0.5)
plt.xlabel('Date')
plt.ylabel('Daily Attendance')
plt.title('Train/Validation/Test Split')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('reports/figures/data_split.png', dpi=300)
plt.show()
```

### Step 3: Baseline Model

Always start with a simple baseline for comparison:

```python
# %% [markdown]
# ## 2. Baseline Model
# 
# Establish performance baseline using simple methods:
# - Naive: Use previous day's value
# - Seasonal Naive: Use same day-of-week from previous week
# - Moving Average: Simple 7-day moving average

# %%
def evaluate_predictions(y_true, y_pred, model_name):
    """Calculate and return evaluation metrics."""
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    
    metrics = {
        'model': model_name,
        'MAPE': mape,
        'MAE': mae,
        'RMSE': rmse,
        'R2': r2
    }
    
    print(f"\n{model_name} Performance:")
    print(f"  MAPE: {mape:.2f}%")
    print(f"  MAE: {mae:.2f}")
    print(f"  RMSE: {rmse:.2f}")
    print(f"  R²: {r2:.4f}")
    
    return metrics

# Baseline 1: Seasonal Naive (use last week's value)
baseline_pred = []
for i in range(len(test_df)):
    lookback_idx = train_size + val_size + i - 7
    if lookback_idx >= 0:
        baseline_pred.append(df.iloc[lookback_idx]['daily_attendance_count'])
    else:
        baseline_pred.append(train_df['daily_attendance_count'].mean())

baseline_metrics = evaluate_predictions(
    test_df['daily_attendance_count'].values, 
    baseline_pred, 
    'Baseline (Seasonal Naive)'
)

# Store baseline for comparison
baseline_mape = baseline_metrics['MAPE']
```

### Step 4: Train Candidate Models

```python
# %% [markdown]
# ## 3. Model Training

# %%
# Dictionary to store all trained models and metrics
models = {}
all_metrics = [baseline_metrics]

# %% [markdown]
# ### 3.1 Facebook Prophet

# %%
with mlflow.start_run(run_name="prophet_default"):
    # Prepare data for Prophet (requires 'ds' and 'y' columns)
    prophet_train = train_df[['date', 'daily_attendance_count']].rename(
        columns={'date': 'ds', 'daily_attendance_count': 'y'}
    )
    
    # Initialize and fit Prophet
    model_prophet = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.05,
        seasonality_prior_scale=10.0
    )
    
    # Add custom regressors if available (e.g., holidays, weather)
    # model_prophet.add_regressor('is_holiday')
    
    model_prophet.fit(prophet_train)
    
    # Make predictions on validation set
    future_val = val_df[['date']].rename(columns={'date': 'ds'})
    forecast_val = model_prophet.predict(future_val)
    
    # Evaluate on validation set
    val_metrics = evaluate_predictions(
        val_df['daily_attendance_count'].values,
        forecast_val['yhat'].values,
        'Prophet (Validation)'
    )
    
    # Make predictions on test set
    future_test = test_df[['date']].rename(columns={'date': 'ds'})
    forecast_test = model_prophet.predict(future_test)
    
    # Evaluate on test set
    test_metrics = evaluate_predictions(
        test_df['daily_attendance_count'].values,
        forecast_test['yhat'].values,
        'Prophet (Test)'
    )
    
    # Log to MLflow
    mlflow.log_params({
        'model_type': 'Prophet',
        'changepoint_prior_scale': 0.05,
        'seasonality_prior_scale': 10.0
    })
    mlflow.log_metrics({
        'val_mape': val_metrics['MAPE'],
        'test_mape': test_metrics['MAPE'],
        'test_mae': test_metrics['MAE'],
        'test_rmse': test_metrics['RMSE']
    })
    mlflow.prophet.log_model(model_prophet, "model")
    
    # Store model and metrics
    models['prophet'] = model_prophet
    all_metrics.append(test_metrics)

# %% [markdown]
# ### 3.2 SARIMA

# %%
with mlflow.start_run(run_name="sarima_default"):
    # Fit SARIMA model
    # Order (p,d,q) and seasonal order (P,D,Q,s)
    # Start with reasonable defaults, then tune
    model_sarima = SARIMAX(
        train_df['daily_attendance_count'],
        order=(1, 1, 1),
        seasonal_order=(1, 1, 1, 7),  # weekly seasonality
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    
    sarima_fit = model_sarima.fit(disp=False, maxiter=100)
    
    # Forecast on test set
    forecast_sarima = sarima_fit.forecast(steps=len(test_df))
    
    # Evaluate
    test_metrics = evaluate_predictions(
        test_df['daily_attendance_count'].values,
        forecast_sarima.values,
        'SARIMA (Test)'
    )
    
    # Log to MLflow
    mlflow.log_params({
        'model_type': 'SARIMA',
        'order': '(1,1,1)',
        'seasonal_order': '(1,1,1,7)'
    })
    mlflow.log_metrics({
        'test_mape': test_metrics['MAPE'],
        'test_mae': test_metrics['MAE'],
        'test_rmse': test_metrics['RMSE']
    })
    
    models['sarima'] = sarima_fit
    all_metrics.append(test_metrics)

# %% [markdown]
# ### 3.3 XGBoost (with feature engineering)

# %%
with mlflow.start_run(run_name="xgboost_default"):
    # Prepare features (lag features, day of week, etc.)
    def create_time_series_features(df):
        df = df.copy()
        df['dayofweek'] = df['date'].dt.dayofweek
        df['quarter'] = df['date'].dt.quarter
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        df['dayofyear'] = df['date'].dt.dayofyear
        df['weekofyear'] = df['date'].dt.isocalendar().week
        
        # Lag features
        for lag in [1, 7, 14, 28]:
            df[f'lag_{lag}'] = df['daily_attendance_count'].shift(lag)
        
        # Rolling statistics
        for window in [7, 14, 28]:
            df[f'rolling_mean_{window}'] = df['daily_attendance_count'].shift(1).rolling(window).mean()
            df[f'rolling_std_{window}'] = df['daily_attendance_count'].shift(1).rolling(window).std()
        
        return df
    
    # Create features for all sets
    train_features = create_time_series_features(train_df).dropna()
    val_features = create_time_series_features(
        pd.concat([train_df, val_df])
    ).iloc[len(train_df):].dropna()
    test_features = create_time_series_features(
        pd.concat([train_df, val_df, test_df])
    ).iloc[len(train_df) + len(val_df):].dropna()
    
    # Define feature columns
    feature_cols = [col for col in train_features.columns 
                   if col not in ['date', 'daily_attendance_count']]
    
    # Train XGBoost
    model_xgb = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=RANDOM_SEED
    )
    
    model_xgb.fit(
        train_features[feature_cols],
        train_features['daily_attendance_count']
    )
    
    # Predict on test set
    xgb_pred = model_xgb.predict(test_features[feature_cols])
    
    # Evaluate
    test_metrics = evaluate_predictions(
        test_features['daily_attendance_count'].values,
        xgb_pred,
        'XGBoost (Test)'
    )
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model_xgb.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 Important Features:")
    print(feature_importance.head(10))
    
    # Log to MLflow
    mlflow.log_params({
        'model_type': 'XGBoost',
        'n_estimators': 100,
        'max_depth': 5,
        'learning_rate': 0.1
    })
    mlflow.log_metrics({
        'test_mape': test_metrics['MAPE'],
        'test_mae': test_metrics['MAE'],
        'test_rmse': test_metrics['RMSE']
    })
    mlflow.xgboost.log_model(model_xgb, "model")
    
    models['xgboost'] = model_xgb
    all_metrics.append(test_metrics)
```

### Step 5: Hyperparameter Tuning

For the best-performing model, conduct hyperparameter optimization:

```python
# %% [markdown]
# ## 4. Hyperparameter Tuning
# 
# Using Bayesian Optimization (Optuna) to tune the best model

# %%
import optuna

def objective(trial):
    """Optuna objective function for Prophet."""
    # Suggest hyperparameters
    changepoint_prior_scale = trial.suggest_float('changepoint_prior_scale', 0.001, 0.5)
    seasonality_prior_scale = trial.suggest_float('seasonality_prior_scale', 0.01, 10.0)
    
    # Train model
    prophet_train = train_df[['date', 'daily_attendance_count']].rename(
        columns={'date': 'ds', 'daily_attendance_count': 'y'}
    )
    
    model = Prophet(
        changepoint_prior_scale=changepoint_prior_scale,
        seasonality_prior_scale=seasonality_prior_scale,
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )
    model.fit(prophet_train)
    
    # Evaluate on validation set
    future_val = val_df[['date']].rename(columns={'date': 'ds'})
    forecast = model.predict(future_val)
    
    # Calculate MAPE
    mape = mean_absolute_percentage_error(
        val_df['daily_attendance_count'].values,
        forecast['yhat'].values
    ) * 100
    
    return mape

# Run optimization
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=50, show_progress_bar=True)

print(f"\nBest MAPE: {study.best_value:.2f}%")
print(f"Best parameters: {study.best_params}")

# Train final model with best parameters
with mlflow.start_run(run_name="prophet_optimized"):
    prophet_train = train_df[['date', 'daily_attendance_count']].rename(
        columns={'date': 'ds', 'daily_attendance_count': 'y'}
    )
    
    model_prophet_opt = Prophet(
        **study.best_params,
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )
    model_prophet_opt.fit(prophet_train)
    
    # Evaluate on test set
    future_test = test_df[['date']].rename(columns={'date': 'ds'})
    forecast_test = model_prophet_opt.predict(future_test)
    
    test_metrics = evaluate_predictions(
        test_df['daily_attendance_count'].values,
        forecast_test['yhat'].values,
        'Prophet Optimized (Test)'
    )
    
    mlflow.log_params({'model_type': 'Prophet_Optimized', **study.best_params})
    mlflow.log_metrics({
        'test_mape': test_metrics['MAPE'],
        'test_mae': test_metrics['MAE'],
        'test_rmse': test_metrics['RMSE']
    })
    mlflow.prophet.log_model(model_prophet_opt, "model")
    
    models['prophet_optimized'] = model_prophet_opt
    all_metrics.append(test_metrics)
```

### Step 6: Model Comparison and Selection

```python
# %% [markdown]
# ## 5. Model Comparison

# %%
# Create comparison table
metrics_df = pd.DataFrame(all_metrics)
metrics_df = metrics_df.sort_values('MAPE')

print("\n" + "="*60)
print("MODEL PERFORMANCE COMPARISON")
print("="*60)
print(metrics_df.to_string(index=False))
print("="*60)

# Visualize comparison
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# MAPE comparison
axes[0].barh(metrics_df['model'], metrics_df['MAPE'], color='skyblue', edgecolor='black')
axes[0].axvline(15, color='red', linestyle='--', label='Target (15%)')
axes[0].set_xlabel('MAPE (%)')
axes[0].set_title('Model Comparison - MAPE')
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis='x')

# Multiple metrics
metrics_df_subset = metrics_df[metrics_df['model'] != 'Baseline (Seasonal Naive)']
x = np.arange(len(metrics_df_subset))
width = 0.2

axes[1].bar(x - width, metrics_df_subset['MAPE']/10, width, label='MAPE/10')
axes[1].bar(x, metrics_df_subset['MAE']/100, width, label='MAE/100')
axes[1].bar(x + width, metrics_df_subset['RMSE']/100, width, label='RMSE/100')
axes[1].set_xticks(x)
axes[1].set_xticklabels(metrics_df_subset['model'], rotation=45, ha='right')
axes[1].set_ylabel('Normalized Score')
axes[1].set_title('Multi-Metric Comparison (Normalized)')
axes[1].legend()
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('reports/figures/model_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Select best model
best_model_name = metrics_df.iloc[0]['model']
best_mape = metrics_df.iloc[0]['MAPE']

print(f"\n🏆 BEST MODEL: {best_model_name}")
print(f"   Test MAPE: {best_mape:.2f}%")
print(f"   Target achieved: {'✅ YES' if best_mape < 15 else '❌ NO'}")
```

### Step 7: Save Models and Generate Report

```python
# %% [markdown]
# ## 6. Save Models and Artifacts

# %%
import joblib
from datetime import datetime

# Save best model
best_model_key = best_model_name.lower().replace(' ', '_').replace('(', '').replace(')', '')
best_model = models[best_model_key]

model_filename = f"models/trained/attendance_forecasting_best_{datetime.now().strftime('%Y%m%d')}.pkl"
joblib.dump(best_model, model_filename)
print(f"✅ Best model saved to: {model_filename}")

# Save metrics
metrics_df.to_csv('results/metrics/model_training_results.csv', index=False)
print(f"✅ Metrics saved to: results/metrics/model_training_results.csv")

# %% [markdown]
# ## 7. Key Findings
# 
# ### Training Summary
# - **Models trained**: 4 (Baseline, Prophet, SARIMA, XGBoost)
# - **Best model**: Prophet (Optimized)
# - **Best test MAPE**: 12.3% ✅ (Target: < 15%)
# - **Training duration**: 45 minutes
# 
# ### Model Insights
# 1. **Prophet performed best** due to strong seasonality handling
# 2. **XGBoost competitive** with lag features (MAPE: 13.8%)
# 3. **SARIMA struggled** with complex multi-seasonality patterns
# 4. **Hyperparameter tuning** improved Prophet from 14.2% to 12.3% MAPE
# 
# ### Feature Importance (XGBoost)
# Top drivers of attendance:
# 1. lag_7 (last week same day)
# 2. rolling_mean_7 (7-day average)
# 3. dayofweek (day of week effect)
# 4. lag_1 (previous day)
# 
# ### Next Steps
# 1. ✅ Proceed to model evaluation with detailed error analysis
# 2. Test model on individual polyclinics (currently aggregate)
# 3. Incorporate external features (holidays, weather) for further improvement
# 4. Set up automated retraining pipeline
```

---

## Outputs

You will produce:

1. **Training Notebook**:
   - `notebooks/2_analysis/03_model_training.ipynb`
   - Complete with all experiments and results

2. **Trained Models** in `models/trained/`:
   - `attendance_forecasting_best_20260128.pkl` (best model)
   - `attendance_forecasting_prophet_20260128.pkl`
   - `attendance_forecasting_xgboost_20260128.pkl`

3. **Training Metrics**:
   - `results/metrics/model_training_results.csv`
   - `results/metrics/feature_importance.csv` (if applicable)

4. **MLflow Experiment Logs**:
   - Tracked in MLflow UI (accessible via `mlflow ui`)

5. **Visualizations**:
   - `reports/figures/data_split.png`
   - `reports/figures/model_comparison.png`
   - `reports/figures/training_curves.png` (if applicable)

6. **Model Cards** (documentation):
   - `models/trained/model_card_best.md`

---

## Quality Checks

Before marking this stage as complete, verify:

- [ ] Baseline model established for comparison
- [ ] Multiple candidate algorithms trained
- [ ] Hyperparameter tuning performed on best model(s)
- [ ] All models evaluated on held-out test set
- [ ] Test performance meets target criteria (or documented if not)
- [ ] Models saved in standardized format
- [ ] Training process logged and reproducible
- [ ] Experiment tracking configured (MLflow/W&B)
- [ ] Model comparison visualizations created
- [ ] Feature importance analyzed (if applicable)
- [ ] Best model selected with clear justification
- [ ] Model artifacts saved with metadata
- [ ] Training duration documented

---

## Next Steps

After model training:
1. Proceed to **Model Evaluation** for detailed error analysis
2. Interpret model predictions and residuals
3. Assess model fairness and robustness
4. Prepare model for deployment
5. Document model limitations and assumptions

---

## Example Execution

```bash
# Run training notebook
jupyter nbconvert --to notebook --execute notebooks/2_analysis/03_model_training.ipynb

# View MLflow experiments
mlflow ui --port 5000

# Check saved models
ls -lh models/trained/

# Review metrics
cat results/metrics/model_training_results.csv
```
