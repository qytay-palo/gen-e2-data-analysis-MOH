# Prompt: Generate End-to-End Programming Implementation Plan

## Role
You are a senior data analyst with expertise in building production-grade analytics pipelines. Your task is to generate comprehensive, executable programming implementation plans for a data analyst project.

---

## Context & Input Files

#**** it might run the implementation plan blindly, must make sure it is specific enough
#******* should still have implementation plan, also good for agent to check if progress was done or not (TODO LIST) - it anchor (as model generate and generate, then summarise then alot data is loss => so need implementation plan)
#***** the prompt to will look at user story for implementation plan, then run an execute to run the code!!!!**
#****** the implementation PLAN MUST BE CLEAR CUT, GO TO THE ENDPOINT AND TAKE THE API 
#******* THE EXECUETION PLAN SHOULD NOT BE VAGUE, MUST BE CLEAR ALRDY
#******** MODIFY INGESTION METHOD for step 4
#********* refine the prompt 

This prompt is designed to work with a workspace that contains:

### Required Input Documents

1. **Execution Plan**: Located at `docs/methodology/data_flows/execution_plan.md`
   - Contains phased breakdown of all data flows
   - Specifies dependencies, timelines, and deliverables
   - Lists all data flows in the project

2. **Data Flow Specifications**: Located at `docs/methodology/data_flows/`
   - Individual data flow documents (e.g., `epic-001-facility-utilization-bottleneck-analysis-flow.md`)
   - Each data flow document contains detailed specifications, data sources, transformations, analysis requirements, and machine learning model specifications
   - `shared_components.md` (reusable utilities across data flows)

3. **Project Context**: Located at `docs/project_context/`
   - `tech_stack.md`: Technical infrastructure and tool preferences
   - `data_sources.md`: dataset specifications, table structures, and data characteristics

---

## Execution Instructions

1. **Read all input files** from the locations specified above:
   - Start with `execution_plan.md` to understand the overall project structure
   - Read each data flow specification document from `docs/methodology/data_flows/`
   - Review project context files (`tech_stack.md`, `data_sources.md`)

2. **Identify all data flows** from the existing data flow documents:
   - Look for files matching pattern: `*-flow.md` in `docs/methodology/data_flows/`
   - Extract the data flow identifier from each document (e.g., `epic-001`, `flow-001`, or whatever convention is used)
   - Extract the data flow name/title
   - **Note**: "Epic" is used as an example identifier. Use the actual naming convention from the data flow documents.

3. **For EACH data flow document**, generate a complete implementation plan based on:
   - The detailed specifications in the data flow document
   - Requirements and objectives stated in the flow
   - Data sources and transformations specified
   - Analysis methods and expected outputs described

4. **Create output files** using the same identifier as the data flow:
   - Format: `docs/methodology/implementation_plans/[flow-id]-implementation-plan.md`
   - Example: If data flow is `epic-001-facility-utilization-bottleneck-analysis-flow.md`, create `epic-001-facility-utilization-bottleneck-analysis-implementation-plan.md`

5. **Create an index file** at: `docs/methodology/implementation_plans/README.md`
   - List all generated implementation plans
   - Provide links to each implementation plan
   - Include brief descriptions

If any input files are missing or unclear, use the information available and note any assumptions made.

---

## Output Requirements

Generate a **complete, production-ready implementation plan** for EACH data flow that includes:

### 1. Data-Flow-Specific Folder Structure

**CRITICAL**: Create a dedicated folder structure for each data flow to organize all related code, configurations, and outputs.

**Note**: The examples below use "epic-XXX" as the identifier format, but you should use whatever naming convention is specified in the actual data flow documents (e.g., `epic-001`, `flow-001`, `analysis-001`, etc.).

```
[data_flows]/                            # Root folder for all data flows
└── [flow_id]/                           # Use the identifier from the data flow document
    ├── README.md                        # Data flow overview and quick start guide
    ├── config/
    │   ├── [flow_id]_config.yml        # Flow-specific configuration
    │   ├── [flow_id]_params.yml        # Analysis parameters
    │   └── [flow_id]_queries.yml       # Query configurations
    ├── src/
    │   ├── __init__.py
    │   ├── extraction.py                # Data extraction module
    │   ├── features.py                  # Feature engineering module
    │   ├── analysis.py                  # Statistical analysis module
    │   ├── modeling.py                  # Machine learning modeling module
    │   ├── evaluation.py                # Model evaluation and validation
    │   ├── visualization.py             # Visualization module
    │   └── utils.py                     # Epic-specific utilities
    ├── scripts/
    │   ├── 01_extract_data.py          # Step 1: Extract data
    │   ├── 02_engineer_features.py     # Step 2: Feature engineering
    │   ├── 03_run_analysis.py          # Step 3: Run statistical analysis
    │   ├── 04_train_models.py          # Step 4: Train ML models
    │   ├── 05_evaluate_models.py       # Step 5: Evaluate models
    │   ├── 06_generate_visualizations.py  # Step 6: Create visualizations
    │   ├── 07_generate_reports.py      # Step 7: Generate reports
    │   └── run_full_pipeline.py        # Orchestration script
    ├── notebooks/
    │   ├── 01_exploration.ipynb        # Data exploration
    │   ├── 02_feature_analysis.ipynb   # Feature analysis
    │   ├── 03_modeling.ipynb           # ML model development
    │   ├── 04_model_tuning.ipynb       # Hyperparameter tuning
    │   ├── 05_model_evaluation.ipynb   # Model performance evaluation
    │   └── 06_results_viz.ipynb        # Results visualization
    ├── sql/
    │   ├── extraction_queries.sql      # Data extraction SQL
    │   ├── validation_queries.sql      # Data validation SQL
    │   └── aggregation_queries.sql     # Aggregation queries
    ├── tests/
    │   ├── __init__.py
    │   ├── test_extraction.py          # Tests for extraction module
    │   ├── test_features.py            # Tests for features module
    │   ├── test_analysis.py            # Tests for analysis module
    │   ├── test_modeling.py            # Tests for ML modeling module
    │   ├── test_evaluation.py          # Tests for model evaluation
    │   └── test_integration.py         # End-to-end integration tests
    ├── data/
    │   ├── raw/                        # Raw extracted data
    │   ├── processed/                  # Processed data
    │   ├── features/                   # Feature datasets
    │   ├── train/                      # Training datasets
    │   ├── validation/                 # Validation datasets
    │   └── test/                       # Test datasets
    ├── results/
    │   ├── metrics/                    # Analysis metrics
    │   ├── model_performance/          # ML model performance metrics
    │   ├── predictions/                # Model predictions
    │   ├── tables/                     # Result tables
    │   └── exports/                    # Exported data
    ├── models/
    │   ├── trained/                    # Trained model artifacts
    │   ├── checkpoints/                # Training checkpoints
    │   └── metadata/                   # Model metadata and versioning
    ├── reports/
    │   ├── figures/                    # Generated charts/plots
    │   ├── dashboards/                 # Dashboard files
    │   └── documents/                  # Final reports (PDF/PowerPoint)
    └── logs/
        ├── extraction.log              # Extraction logs
        ├── pipeline.log                # Pipeline execution logs
        └── errors.log                  # Error logs
```

### 2. Implementation Plan Document Structure

For each data flow, create a markdown document with the following sections:

**Note**: Replace `[flow_id]` and `[Flow Name]` with the actual identifier and name from the data flow document. The term "Epic" is used as a reference in examples, but use the terminology from your data flow documents.

```markdown
# Implementation Plan: [Flow ID] - [Flow Name]

## Executive Summary
- **Data Flow**: [Flow ID and Name from the data flow document]
- **Objective**: [Brief description from data flow document]
- **Estimated Duration**: [Timeline from execution plan]
- **Dependencies**: [Prerequisites from other data flows]
- **Key Deliverables**: [Main outputs specified in the data flow]

## 1. Data Flow Folder Structure
[Copy and customize the folder structure above, using the actual flow identifier]

## 2. Module Specifications

### 2.1 Data Extraction & Loading
#### Module: `[data_flows]/[flow_id]/src/extraction.py`
- **Purpose**: [What data this flow extracts - from the data flow document]
- **Data Sources**: [Specific tables/sources for THIS flow from data_sources.md and the data flow document]
- **Key Functions**: [Function signatures with type hints]
- **Extraction Logic**: [Pseudocode or SQL queries based on the data flow specifications]
- **Validation Rules**: [Data quality checks specified in the data flow]
- **Code Skeleton**: 
```python
# Provide skeleton code here based on data flow requirements
```

### 2.2 Feature Engineering & Transformation
#### Module: `[data_flows]/[flow_id]/src/features.py`
[Similar structure - extract requirements from data flow document]

### 2.3 Statistical Analysis
#### Module: `[data_flows]/[flow_id]/src/analysis.py`
[Similar structure - extract statistical analysis methods from data flow document]

### 2.4 Machine Learning Modeling
#### Module: `[data_flows]/[flow_id]/src/modeling.py`
- **Purpose**: [ML objectives for this flow from the data flow document]
- **Model Types**: [Classification/Regression/Clustering/Time Series - based on requirements]
- **Algorithms**: [Specific algorithms to implement]
- **Key Functions**: [Function signatures with type hints]
- **Training Logic**: [Training pipeline, cross-validation strategy]
- **Hyperparameter Tuning**: [Grid search, random search, or Bayesian optimization]
- **Model Persistence**: [Model serialization and versioning]
- **Code Skeleton**: 
```python
# Provide skeleton code for ML modeling
```

### 2.5 Model Evaluation & Validation
#### Module: `[data_flows]/[flow_id]/src/evaluation.py`
- **Purpose**: [Model evaluation objectives]
- **Metrics**: [Accuracy, Precision, Recall, F1, AUC-ROC, RMSE, MAE, etc.]
- **Validation Strategy**: [Cross-validation, holdout, time-series split]
- **Key Functions**: [Function signatures for evaluation]
- **Interpretation**: [Feature importance, SHAP values, model explainability]
- **Code Skeleton**: 
```python
# Provide skeleton code for model evaluation
```

### 2.6 Visualization & Reporting
#### Module: `[data_flows]/[flow_id]/src/visualization.py`
[Similar structure - extract visualization requirements from data flow document]
- Include ML-specific visualizations: confusion matrices, ROC curves, learning curves, feature importance plots, residual plots

## 3. Configuration Files

### `epics/[epic_id]/config/[epic_id]_config.yml`
```yaml
# Configuration specific to this data flow
epic_id: [epic-id]
epic_name: [epic-name]
data_sources:
  # Reference data_sources.md for connection details
  primary_source: [source name from data_sources.md]
  tables:
    - [table names from data flow spec]
output_paths:
  raw_data: epics/[epic_id]/data/raw/
  processed_data: epics/[epic_id]/data/processed/
  train_data: epics/[epic_id]/data/train/
  validation_data: epics/[epic_id]/data/validation/
  test_data: epics/[epic_id]/data/test/
  models: epics/[epic_id]/models/trained/
  results: epics/[epic_id]/results/
ml_config:
  problem_type: [classification|regression|clustering|time_series]
  target_variable: [target column name]
  feature_selection: [auto|manual]
  train_test_split: 0.8
  validation_split: 0.2
  random_state: 42
  cross_validation_folds: 5
```

### `epics/[epic_id]/config/[epic_id]_model_params.yml`
```yaml
# Machine learning model parameters
models:
  model_1:
    algorithm: [e.g., RandomForest, XGBoost, LogisticRegression]
    hyperparameters:
      [param1]: [value1]
      [param2]: [value2]
    tuning:
      method: [grid_search|random_search|bayesian]
      param_grid:
        [param1]: [[value1, value2, value3]]
        [param2]: [[value1, value2]]
      scoring: [accuracy|f1|roc_auc|rmse]
  model_2:
    # Additional models to compare

evaluation:
  metrics:
    - [metric1: e.g., accuracy, precision, recall]
    - [metric2: e.g., f1_score, roc_auc]
  threshold_optimization: [true|false]
  feature_importance: [true|false]
  model_explainability:
    shap_values: [true|false]
    permutation_importance: [true|false]
```

### `epics/[epic_id]/sql/extraction_queries.sql`
```sql
-- SQL queries specific to this data flow
-- [Provide actual queries from the data flow specification]
```

## 4. Execution Workflow

### Step-by-Step Commands
```bash
# Navigate to epic directory
cd epics/[epic_id]/

# Step 1: Extract data
python scripts/01_extract_data.py

# Step 2: Engineer features
python scripts/02_engineer_features.py

# Step 3: Run statistical analysis
python scripts/03_run_analysis.py

# Step 4: Train ML models
python scripts/04_train_models.py

# Step 5: Evaluate models
python scripts/05_evaluate_models.py

# Step 6: Generate visualizations
python scripts/06_generate_visualizations.py

# Step 7: Create reports
python scripts/07_generate_reports.py

# OR run the entire pipeline
python scripts/run_full_pipeline.py
```

### Main Orchestration Script
```python
# epics/[epic_id]/scripts/run_full_pipeline.py
# [Provide skeleton code]
```

## 5. Testing Strategy

### Unit Tests
```python
# epics/[epic_id]/tests/test_extraction.py
# [Provide test examples]

# epics/[epic_id]/tests/test_modeling.py
# Test ML model training, prediction, and serialization

# epics/[epic_id]/tests/test_evaluation.py
# Test model evaluation metrics and validation
```

### Model Validation Tests
```python
# Test model performance against baseline
# Test for overfitting/underfitting
# Test feature importance calculations
# Test model predictions on edge cases
# Test model serialization and loading
```

### Running Tests
```bash
cd epics/[epic_id]/

# Run all tests with coverage
pytest tests/ -v --cov=src

# Run ML-specific tests
pytest tests/test_modeling.py tests/test_evaluation.py -v

# Run integration tests
pytest tests/test_integration.py -v
```

## 6. Outputs & Deliverables

### Data Outputs
- **Location**: `epics/[epic_id]/data/`
- **Files**: [List specific output files]

### Analysis Results
- **Location**: `epics/[epic_id]/results/`
- **Files**: [List metrics and tables]

### ML Models
- **Location**: `epics/[epic_id]/models/trained/`
- **Files**: 
  - Trained model artifacts (.pkl, .joblib, .h5, .onnx)
  - Model metadata (version, training date, parameters)
  - Feature lists and preprocessing pipelines

### Model Performance
- **Location**: `epics/[epic_id]/results/model_performance/`
- **Files**:
  - Performance metrics (accuracy, precision, recall, F1, AUC-ROC, RMSE, MAE)
  - Cross-validation results
  - Confusion matrices
  - Feature importance rankings
  - SHAP values and explainability reports

### Predictions
- **Location**: `epics/[epic_id]/results/predictions/`
- **Files**: 
  - Test set predictions
  - Prediction probabilities
  - Prediction confidence intervals

### Visualizations
- **Location**: `epics/[epic_id]/reports/figures/`
- **Files**: [List charts]
  - ML-specific: ROC curves, precision-recall curves, learning curves, confusion matrices, feature importance plots, residual plots

### Reports
- **Location**: `epics/[epic_id]/reports/documents/`
- **Files**: [List reports]

## 7. Monitoring & Alerts

### Key Metrics to Track
[Metrics specific to this flow]

### ML Model Monitoring Metrics
- Training metrics: loss, accuracy per epoch
- Validation metrics: validation loss, validation accuracy
- Model performance: precision, recall, F1-score, AUC-ROC
- Inference time and latency
- Model drift detection (if applicable)
- Feature distribution shifts

### Logging Configuration
```yaml
# Logging setup for this epic
logging:
  model_training:
    level: INFO
    file: epics/[epic_id]/logs/training.log
    metrics_tracking: true
  model_evaluation:
    level: INFO
    file: epics/[epic_id]/logs/evaluation.log
  predictions:
    level: INFO
    file: epics/[epic_id]/logs/predictions.log
```

## 8. Dependencies & Integration

### Upstream Dependencies
[What this flow depends on]

### Downstream Consumers
[What depends on this flow's outputs]

### Shared Components
- Reference: `docs/methodology/data_flows/shared_components.md`
- Modules: [List reusable components from shared_components.md]

## 9. Timeline & Milestones

[Timeline from execution_plan.md]

## 10. Success Criteria

[From the data flow specification]
```

---

## 3. Create Index File

After generating all individual epic implementation plans, create:

**File**: `docs/methodology/implementation_plans/README.md`

```markdown
# Implementation Plans Index

This directory contains detailed implementation plans for all data flows/epics in the project.

## Epic Implementation Plans

| Epic ID | Title | Plan Document | Status | Priority |
|---------|-------|---------------|--------|----------|
| [Generate rows for each epic found in execution_plan.md] | [Epic Title] | [epic-id-epic-name-implementation-plan.md] | Ready | [Priority] |

## Shared Components

Refer to [Shared Components](../data_flows/shared_components.md) for reusable utilities across multiple epics.

## How to Use

1. Review the execution plan: `docs/methodology/data_flows/execution_plan.md`
2. Select an epic to implement
3. Open the corresponding implementation plan
4. Follow the step-by-step instructions
5. Run tests to validate implementation

## Tech Stack

Refer to [Tech Stack](../project_context/tech_stack.md) for detailed technology specifications.
```

---

## Technology-Specific Requirements

**CRITICAL**: Extract technology specifications from `docs/project_context/tech_stack.md` and `docs/project_context/data_sources.md`

### Required Packages
```python
# Generate requirements.txt based on:
# 1. Languages specified in tech_stack.md
# 2. Data source connection libraries from data_sources.md
# 3. Analytics libraries appropriate for the tech stack
# 4. Machine learning and data science libraries
# 5. Testing and quality frameworks

# Example format:
[package]>=[version]  # [Purpose based on tech stack]

# Machine Learning Libraries (examples - customize based on requirements):
scikit-learn>=1.3.0  # Traditional ML algorithms
xgboost>=2.0.0  # Gradient boosting
lightgbm>=4.0.0  # Light gradient boosting
catboost>=1.2.0  # Categorical boosting
tensorflow>=2.13.0  # Deep learning (if needed)
pytorch>=2.0.0  # Deep learning (if needed)
keras>=2.13.0  # Neural networks API (if needed)
statsmodels>=0.14.0  # Statistical modeling

# Model Interpretation & Explainability:
shap>=0.42.0  # SHAP values for model explainability
eli5>=0.13.0  # Model interpretation
pdpbox>=0.2.1  # Partial dependence plots

# Hyperparameter Tuning:
optuna>=3.3.0  # Bayesian optimization
hyperopt>=0.2.7  # Hyperparameter optimization
sklearn-deap>=0.3.0  # Genetic algorithm tuning

# Model Persistence & Versioning:
joblib>=1.3.0  # Model serialization
cloudpickle>=2.2.0  # Enhanced pickle
mlflow>=2.5.0  # ML experiment tracking (optional)

# Validation & Metrics:
imbalanced-learn>=0.11.0  # Handling imbalanced datasets
scipy>=1.11.0  # Scientific computing
numpy>=1.24.0  # Numerical computing
pandas>=2.0.0  # Data manipulation
```

---

## Quality Criteria

Your implementation plans must:

1. ✅ **Be Executable**: Provide enough detail for immediate implementation
2. ✅ **Be Epic-Specific**: Tailor each plan to the specific epic's requirements
3. ✅ **Reference Actual Data**: Use exact table/source names from `data_sources.md`
4. ✅ **Include Code Skeletons**: Provide function signatures and class structures
5. ✅ **Specify Dependencies**: Reference `shared_components.md` where applicable
6. ✅ **Follow Tech Stack**: Use technologies specified in `tech_stack.md`
7. ✅ **Include Testing**: Unit tests, integration tests, data quality tests
8. ✅ **Be Self-Contained**: Each epic plan should be independently readable
9. ✅ **Match Execution Plan**: Align timelines and dependencies with `execution_plan.md`
10. ✅ **Provide Examples**: Include SQL queries, config files, and script templates

---

## Execution Instructions

When this prompt is invoked:

1. **IMMEDIATELY READ** the following files:
   - `docs/methodology/data_flows/execution_plan.md`
   - All data flow specification files in `docs/methodology/data_flows/` (typically `epic-*.md` pattern)
   - `docs/methodology/data_flows/shared_components.md` (if exists)
   - `docs/project_context/tech_stack.md`
   - `docs/project_context/data_sources.md`

2. **IDENTIFY ALL EPICS/DATA FLOWS**:
   - Parse execution_plan.md to extract list of all epics
   - Locate corresponding data flow specification files
   - Note dependencies and sequencing requirements

3. **CREATE THE OUTPUT DIRECTORY** if it doesn't exist:
   - `docs/methodology/implementation_plans/`

4. **GENERATE IMPLEMENTATION PLANS** for ALL identified epics/data flows in sequence:
   - Process each epic based on the data flow specifications found
   - Follow the naming convention: `[epic-id]-[epic-name]-implementation-plan.md`
   - Ensure each plan is complete and self-contained

5. **CREATE THE INDEX FILE**: `docs/methodology/implementation_plans/README.md`
   - Include table with all generated implementation plans
   - Reference execution plan and shared components
   - List tech stack summary

7. **REPORT COMPLETION** with a summary of:
   - Number of epics/data flows processed
   - List of implementation plan files created
   - Any assumptions made or issues encountered

---

## Begin Execution

Start generating implementation plans now. Process all epics/data flows found in the workspace automatically.
