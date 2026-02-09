---
description: Model Training Stage with MCP Integration
stage: Model Training & Machine Learning
---

# Stage Prompt: Model Training and Machine Learning

## Objective

Develop, train, and evaluate machine learning models to make predictions, classify outcomes, or detect patterns. Leverage MCP tools for efficient data access, model persistence, and results documentation.

## Required MCP Tools

- **Filesystem Server** (REQUIRED): For reading feature datasets, saving trained models, and managing experiment results
- **SQLite Server** (when applicable): For querying training data directly from databases

## Input Requirements

The following inputs MUST be available before proceeding:

1. **Feature Datasets**: `data/4_processed/{epic_id}/features/`
   - Training set (features + target)
   - Validation set (if available)
   - Test set (for final evaluation)
   - Feature documentation

2. **Modeling Requirements**: From user story or analysis objectives
   - Problem type (classification, regression, clustering, anomaly detection)
   - Target variable (what to predict)
   - Success metrics (accuracy, F1, RMSE, etc.)
   - Model interpretability requirements
   - Performance constraints (speed, memory)

3. **Modeling Specifications**:
   - Algorithms to try (baseline + candidates)
   - Hyperparameter search strategy
   - Cross-validation approach
   - Class imbalance handling (if applicable)

4. **Project Context** (REQUIRED - read before modeling):
   - **Business objectives**: `docs/project_context/business-objectives.md` (understand what to optimize)
   - **Tech stack**: `docs/project_context/tech_stack.md` (deployment constraints)
   - **Domain knowledge**: For interpreting feature importance and model decisions
   - Previous models (if improving existing)
   
   **Use MCP filesystem tools to read these files** to understand:
   - What the model should optimize (business metric)
   - What deployment constraints exist (speed, interpretability)
   - What technical platform will host the model

## Output Requirements

The model training MUST produce:

1. **Trained Models**: `models/{epic_id}/`
   - Serialized model files (.pkl, .joblib, .h5)
   - Model metadata (hyperparameters, features used)
   - Preprocessing pipelines (scalers, encoders)
   - Model versioning information

2. **Model Training Notebooks**: `notebooks/2_analysis/{epic_id}/` or `notebooks/models/`
   - Data preparation and splitting
   - Baseline model training
   - Model experimentation
   - Hyperparameter tuning
   - Final model training and evaluation

3. **Model Evaluation Results**: `results/metrics/{epic_id}_model_performance.json`
   - Training metrics
   - Validation metrics
   - Test metrics
   - Cross-validation scores
   - Confusion matrix (classification)
   - Feature importance scores

4. **Model Visualizations**: `reports/figures/{epic_id}/model/`
   - ROC curves (classification)
   - Precision-recall curves
   - Feature importance plots
   - Learning curves
   - Residual plots (regression)
   - Confusion matrices

5. **Model Documentation**: `models/{epic_id}/model_card.md`
   - Model description and purpose
   - Training data details
   - Performance metrics
   - Limitations and biases
   - Intended use and deployment notes

## Execution Steps

### Step 1: Model Training Setup (using MCP filesystem tools)

```
1. Use filesystem tools to create model directories:
   - models/{epic_id}/
   - notebooks/models/ (if not exists)
   - reports/figures/{epic_id}/model/

2. Use filesystem tools to read feature datasets:
   - Read data/4_processed/{epic_id}/features/train_features.csv
   - Read data/4_processed/{epic_id}/features/test_features.csv
   - Read feature documentation

3. Verify data quality:
   - Check for missing values
   - Verify feature dtypes
   - Confirm target variable exists
   - Check class balance (for classification)

4. Split features (X) and target (y)
```

**Example MCP Commands**:
- "Use filesystem tools to create directory models/epic-001/"
- "Use filesystem tools to read data/4_processed/epic-001/features/train_features.csv"
- "Use filesystem tools to read data/schemas/epic-001/feature_dictionary.md"

### Step 2: Baseline Model (using MCP tools)

```
Create simple baseline model for comparison:

For Classification:
- Majority class classifier (always predict most common class)
- Random classifier
- Simple logistic regression (no tuning)

For Regression:
- Mean predictor (always predict mean of target)
- Median predictor
- Simple linear regression (no feature engineering)

For Clustering:
- Random clustering
- Single-feature clustering

For Anomaly Detection:
- Z-score based (statistical threshold)
- Simple percentile-based

1. Train baseline model
2. Evaluate on validation/test set
3. Record baseline metrics
4. Use filesystem tools to save baseline results
```

**Example MCP Commands**:
- "Train baseline majority class classifier"
- "Evaluate on test set: accuracy = 0.65"
- "Use filesystem tools to save baseline_results.json to results/metrics/epic-001/"

### Step 3: Model Selection and Training (using MCP tools)

```
Train multiple candidate models:

For Classification:
- Logistic Regression (interpretable, fast)
- Random Forest (robust, feature importance)
- Gradient Boosting (XGBoost, LightGBM, CatBoost)
- Support Vector Machines (kernel tricks)
- Neural Networks (for complex patterns)

For Regression:
- Linear Regression (interpretable baseline)
- Ridge/Lasso Regression (regularization)
- Random Forest Regressor
- Gradient Boosting Regressor
- Neural Networks

For Clustering:
- K-Means (centroid-based)
- DBSCAN (density-based)
- Hierarchical clustering
- Gaussian Mixture Models

For Anomaly Detection:
- Isolation Forest
- One-Class SVM
- Autoencoder (neural network)
- Local Outlier Factor (LOF)

1. For each model type:
   a. Initialize with default hyperparameters
   b. Train on training set
   c. Evaluate on validation set
   d. Record training time and memory usage
   e. Calculate performance metrics
   
2. Compare all models on validation set
3. Select top 2-3 performing models for tuning
```

**Example MCP Commands**:
- "Train Random Forest, XGBoost, and Logistic Regression classifiers"
- "Evaluate all models on validation set"
- "Compare F1-scores: RF=0.78, XGB=0.82, LR=0.71"
- "Select XGBoost and Random Forest for hyperparameter tuning"

### Step 4: Hyperparameter Tuning (using MCP tools)

```
Optimize top-performing models:

1. Define hyperparameter search space:
   - Learning rate, max depth, n_estimators (tree models)
   - C, penalty (logistic regression)
   - Number of layers, neurons, dropout (neural networks)

2. Choose search strategy:
   - Grid Search (exhaustive, small space)
   - Random Search (efficient, large space)
   - Bayesian Optimization (smarter search)
   - Optuna, Hyperopt (advanced frameworks)

3. Cross-validation strategy:
   - K-fold CV (k=5 or k=10)
   - Stratified K-fold (for imbalanced classes)
   - Time series split (for temporal data)

4. Run hyperparameter tuning:
   - Set scoring metric (accuracy, F1, ROC-AUC, RMSE)
   - Fit tuning algorithm
   - Track all trials and results
   
5. Select best hyperparameters
6. Use filesystem tools to save tuning results
```

**Example MCP Commands**:
- "Perform RandomizedSearchCV on XGBoost with 100 iterations"
- "Best parameters: max_depth=7, learning_rate=0.05, n_estimators=200"
- "Best CV F1-score: 0.85"
- "Use filesystem tools to save tuning_results.json to models/epic-001/"

### Step 5: Final Model Training (using MCP tools)

```
Train final model with best hyperparameters:

1. Retrain on full training set (train + validation):
   - Use best hyperparameters from tuning
   - Fit on combined train+validation data
   - Save training metrics

2. Handle class imbalance (if applicable):
   - SMOTE (Synthetic Minority Over-sampling)
   - Class weights
   - Undersampling majority class
   - Ensemble methods

3. Feature selection (if beneficial):
   - Remove low-importance features
   - Recursive feature elimination
   - L1 regularization

4. Train final model
5. Use filesystem tools to save trained model
```

**Example MCP Commands**:
- "Retrain XGBoost on full training set with optimized hyperparameters"
- "Apply SMOTE to balance classes (ratio 1:2)"
- "Use filesystem tools to save trained model to models/epic-001/xgboost_final.pkl"
- "Use filesystem tools to save preprocessing pipeline to models/epic-001/preprocessing_pipeline.pkl"

### Step 6: Model Evaluation (using MCP tools)

```
Comprehensively evaluate final model:

For Classification:
- Accuracy, Precision, Recall, F1-score
- ROC-AUC score
- Confusion matrix
- Classification report (per-class metrics)
- Precision-Recall curve
- Calibration plot (predicted vs actual probabilities)

For Regression:
- R² score
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE), RMSE
- Mean Absolute Percentage Error (MAPE)
- Residual plots
- Actual vs Predicted plot

For Clustering:
- Silhouette score
- Davies-Bouldin index
- Calinski-Harabasz score
- Cluster size distribution
- Within-cluster sum of squares

For Anomaly Detection:
- Precision, Recall, F1 (if labels available)
- False positive rate
- Detection rate
- ROC-AUC
- Anomaly score distribution

1. Evaluate on held-out test set
2. Calculate all relevant metrics
3. Create evaluation visualizations
4. Use filesystem tools to save evaluation results
```

**Example MCP Commands**:
- "Evaluate final XGBoost model on test set"
- "Test F1-score: 0.84, ROC-AUC: 0.91, Accuracy: 0.87"
- "Create confusion matrix and ROC curve"
- "Use filesystem tools to save evaluation metrics to results/metrics/epic-001_model_performance.json"
- "Use filesystem tools to save ROC curve to reports/figures/epic-001/model/roc_curve.png"

### Step 7: Feature Importance Analysis (using MCP tools)

```
Understand which features drive predictions:

1. Calculate feature importance:
   - Tree-based: Gini importance, split count
   - Permutation importance (model-agnostic)
   - SHAP values (Shapley Additive Explanations)
   - Coefficients (for linear models)

2. Visualize feature importance:
   - Bar chart of top 20 features
   - SHAP summary plot
   - SHAP dependence plots (feature interactions)
   - Partial dependence plots

3. Interpret results:
   - Which features are most predictive?
   - Do results align with domain knowledge?
   - Are there unexpected important features?
   - Feature interactions discovered?

4. Use filesystem tools to save feature importance
```

**Example MCP Commands**:
- "Calculate SHAP values for final XGBoost model"
- "Create feature importance bar chart (top 20 features)"
- "Use filesystem tools to save to reports/figures/epic-001/model/feature_importance.png"
- "Use filesystem tools to save importance scores to results/metrics/epic-001_feature_importance.csv"

### Step 8: Model Interpretation and Validation (using MCP tools)

```
Ensure model is reliable and trustworthy:

1. Model interpretation:
   - Explain individual predictions (LIME, SHAP)
   - Identify decision boundaries
   - Understand model behavior in edge cases
   - Check for spurious correlations

2. Bias and fairness checks:
   - Performance across demographic groups
   - Disparate impact analysis
   - Equalized odds assessment
   - Check for protected attribute leakage

3. Robustness checks:
   - Performance on different data slices
   - Sensitivity to input perturbations
   - Out-of-distribution detection
   - Adversarial examples (if applicable)

4. Learning curves:
   - Training vs validation performance
   - Check for overfitting/underfitting
   - Estimate value of more data

5. Use filesystem tools to save validation results
```

**Example MCP Commands**:
- "Generate SHAP explanations for 10 sample predictions"
- "Create learning curve showing train/val performance vs sample size"
- "Check model performance across age groups and facilities"
- "Use filesystem tools to save interpretation results to models/epic-001/model_interpretation.md"

### Step 9: Model Comparison and Selection (using MCP tools)

```
Compare all trained models systematically:

1. Create comparison table:
   - Model name
   - Training time
   - Inference speed
   - Memory footprint
   - All evaluation metrics
   - Interpretability score
   - Complexity score

2. Consider trade-offs:
   - Performance vs interpretability
   - Accuracy vs speed
   - Complexity vs maintainability
   - Cost of errors (false positives vs false negatives)

3. Select final production model:
   - Best performance on key metric
   - Meets deployment constraints
   - Acceptable interpretability
   - Stakeholder requirements

4. Use filesystem tools to save comparison results
```

**Example MCP Commands**:
- "Create model comparison table with 5 trained models"
- "Best overall: XGBoost (F1=0.84, inference=20ms, interpretable)"
- "Use filesystem tools to save to results/metrics/epic-001_model_comparison.csv"

### Step 10: Model Persistence (using MCP filesystem tools)

```
Save everything needed to use model in production:

1. Save trained model:
   - Pickle (.pkl) or Joblib (.joblib) for sklearn
   - SavedModel or HDF5 (.h5) for TensorFlow/Keras
   - ONNX (.onnx) for interoperability
   - Include version and timestamp in filename

2. Save preprocessing artifacts:
   - Scalers (StandardScaler, MinMaxScaler)
   - Encoders (LabelEncoder, OneHotEncoder)
   - Imputers (SimpleImputer)
   - Feature selectors
   - Full sklearn Pipeline

3. Save model metadata:
   - Hyperparameters used
   - Feature names and order
   - Target variable name
   - Training data statistics
   - Model version and creation date

4. Create model package:
   - model.pkl (trained model)
   - preprocessing.pkl (preprocessing pipeline)
   - metadata.json (model information)
   - requirements.txt (dependencies)

5. Use filesystem tools to save all artifacts
```

**Example MCP Commands**:
- "Use filesystem tools to save XGBoost model to models/epic-001/xgboost_v1_20260206.pkl"
- "Use filesystem tools to save preprocessing pipeline to models/epic-001/preprocessing_v1.pkl"
- "Use filesystem tools to save model metadata to models/epic-001/metadata.json"
- "Use filesystem tools to save feature list to models/epic-001/features.txt"

### Step 11: Model Documentation (using MCP filesystem tools)

```
Create comprehensive model card:

1. Model Overview:
   - Model name and version
   - Model type and algorithm
   - Purpose and use case
   - Creation date and author

2. Intended Use:
   - Primary use case
   - Target users
   - Out-of-scope uses

3. Training Data:
   - Data sources
   - Date range
   - Sample size
   - Feature descriptions
   - Known biases or limitations

4. Performance:
   - Evaluation metrics on test set
   - Comparison to baseline
   - Performance across subgroups
   - Confidence intervals

5. Limitations:
   - Known failure modes
   - Data quality dependencies
   - Bias and fairness concerns
   - Temporal limitations (data drift)

6. Deployment:
   - Input format
   - Output format
   - Inference speed
   - Resource requirements
   - Monitoring recommendations

7. Use filesystem tools to write model card
```

**Example MCP Commands**:
- "Create comprehensive model card documenting XGBoost classifier"
- "Use filesystem tools to write to models/epic-001/model_card.md"

### Step 12: Model Training Notebook (using MCP filesystem tools)

```
Create reproducible training notebook:

1. Notebook structure:
   - Introduction and objectives
   - Data loading and exploration
   - Feature preparation
   - Baseline model
   - Model experimentation
   - Hyperparameter tuning
   - Final model training
   - Evaluation and visualization
   - Model persistence
   - Conclusions and next steps

2. Best practices:
   - Set random seeds for reproducibility
   - Document all hyperparameters
   - Include markdown explanations
   - Show all evaluation metrics
   - Include visualizations inline

3. Use filesystem tools to save notebook
```

**Example MCP Commands**:
- "Create comprehensive model training notebook"
- "Use filesystem tools to save to notebooks/models/epic-001_model_training.ipynb"

### Step 13: Verification (using MCP filesystem tools)

```
1. Verify all required outputs were created:
   - Use filesystem tools to list files in models/{epic_id}/
   - Use filesystem tools to list files in results/metrics/{epic_id}/
   - Use filesystem tools to verify model_card.md exists
   - Use filesystem tools to verify all evaluation visualizations saved

2. Verify model can be loaded and used:
   - Load saved model from disk
   - Load preprocessing pipeline
   - Make predictions on sample data
   - Verify predictions are reasonable

3. Cross-check against acceptance criteria from user story

4. Document verification results
```

**Example MCP Commands**:
- "Use filesystem tools to list all files in models/epic-001/"
- "Load saved model and preprocessing pipeline"
- "Make predictions on 5 test samples and verify outputs"
- "Use filesystem tools to verify model_card.md contains all required sections"

## Model Training Best Practices

### 1. Avoid Data Leakage
```
❌ Don't use test data during training
❌ Don't use future information to predict past
❌ Don't include target-derived features
✅ Fit preprocessing on training data only
✅ Use proper cross-validation
✅ Keep test set completely held out
```

### 2. Handle Imbalanced Classes
```
✅ Use stratified splitting
✅ Try SMOTE or other sampling techniques
✅ Use class weights
✅ Choose appropriate metrics (F1, ROC-AUC, not accuracy)
✅ Consider ensemble methods
```

### 3. Regularization and Generalization
```
✅ Use cross-validation to detect overfitting
✅ Apply regularization (L1, L2, dropout)
✅ Use early stopping for iterative models
✅ Monitor train vs validation performance
✅ Keep models as simple as possible (Occam's Razor)
```

### 4. Reproducibility
```
✅ Set random seeds (np.random.seed, random.seed)
✅ Document all hyperparameters
✅ Version training data
✅ Save complete environment (requirements.txt)
✅ Use version control for code
```

## Success Criteria

The model training is considered successful when:

- ✅ Trained model(s) saved to `models/{epic_id}/`
- ✅ Model significantly outperforms baseline
- ✅ Evaluation metrics meet user story acceptance criteria
- ✅ Feature importance analyzed and documented
- ✅ Model card created in `models/{epic_id}/model_card.md`
- ✅ Training notebook created
- ✅ All evaluation visualizations saved to `reports/figures/{epic_id}/model/`
- ✅ Model can be loaded and used for predictions
- ✅ No data leakage detected
- ✅ All outputs verified using MCP filesystem tools

## MCP Tools Usage Summary

```markdown
### MCP Tools Used

**Filesystem Server**:
- Directories created:
  - models/epic-001/
  - reports/figures/epic-001/model/
  - notebooks/models/
- Files read:
  - data/4_processed/epic-001/features/train_features.csv
  - data/4_processed/epic-001/features/test_features.csv
  - data/schemas/epic-001/feature_dictionary.md
- Files written:
  - 1 trained model (XGBoost, 2.5 MB)
  - 1 preprocessing pipeline (.pkl)
  - 1 model metadata (.json)
  - 1 model card (.md)
  - 5 evaluation visualizations (PNG)
  - 1 training notebook (.ipynb)
  - Multiple metrics files (.json, .csv)
- Verification: Listed model directory, loaded model, made test predictions
```

## Next Stage

After successful model training, proceed to:
- **Model Deployment**: Deploy model to production environment
- **Monitoring**: Set up performance monitoring and drift detection
- **Iteration**: Retrain with new data or improved features

## References

- Feature Data: `data/4_processed/{epic_id}/features/`
- User Story: `docs/objectives/user_stories/{epic_id}/`
- Tech Stack: `docs/project_context/tech_stack.md`
- Project Structure: `README.md`
