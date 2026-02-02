# Prompt: Generate End-to-End Programming Implementation Plan

## Role
You are a senior data analyst with expertise in building production-grade analytics pipelines. Your task is to generate a comprehensive, executable programming implementation plan for a data science project based on the provided execution plan and project context.

---

## Input Documents

You will receive the following documents:

1. **Execution Plan** (`execution_plan.md`): Contains the phased breakdown of data flows, dependencies, timelines, and deliverables
2. **Project Context** (files in `project_context/`): Contains:
   - `tech_stack.md`: Technical infrastructure, platforms, and tool preferences
   - `data_sources.md`: Database schemas, table structures, and data characteristics
   - `data_connections.md`: Connection strings, authentication methods, and API specifications
3. **Data Flow Specifications**: Detailed specifications for each user story/data flow (referenced in execution plan)

---

## Your Task

Generate a **complete, production-ready implementation plan** that includes:

### 1. Project Structure
- Directory structure for code organization
- File naming conventions
- Module architecture
- Configuration file structure
- Separation of concerns (data/models/scripts/tests/utils)

### 2. Core Implementation Modules

For each phase in the execution plan, provide:

#### a) Data Extraction & Loading
- **Module**: `src/data_processing/`
- **Components**:
  - Database connection manager with retry logic
  - Data extraction functions (SQL queries, API calls)
  - Incremental extraction logic with checkpoint management
  - Data validation framework (schema validation, quality checks)
  - Error handling and logging
- **Outputs**: Specify file formats, storage locations, partitioning strategy

#### b) Feature Engineering & Transformation
- **Module**: `src/features/`
- **Components**:
  - Feature calculation functions (aggregations, time-windows, ratios)
  - Data transformation pipeline (scaling, encoding, imputation)
  - Feature store/caching mechanism
  - Feature versioning and metadata tracking
- **Outputs**: Feature datasets with documentation

#### c) Analysis & Modeling
- **Module**: `src/analysis/` and `src/models/`
- **Components**:
  - Statistical analysis functions
  - Model training pipelines (with hyperparameter tuning)
  - Model evaluation framework (metrics, validation)
  - Model persistence and versioning
  - Reproducibility mechanisms (random seeds, environment specs)
- **Outputs**: Trained models, evaluation metrics, analysis results

#### d) Visualization & Reporting
- **Module**: `src/visualization/`
- **Components**:
  - Plotting utility functions
  - Dashboard components (if applicable)
  - Report generation scripts (PDF/PowerPoint automation)
  - Interactive visualization exports
- **Outputs**: Charts, dashboards, executive reports

#### e) Orchestration & Scheduling
- **Module**: `scripts/`
- **Components**:
  - Main execution scripts for each phase
  - Dependency management (execution order)
  - Error recovery mechanisms
  - Notification system (success/failure alerts)
- **Outputs**: Orchestration logs, execution summaries

#### f) Testing & Quality Assurance
- **Module**: `tests/`
- **Components**:
  - Unit tests for each module (target >80% coverage)
  - Integration tests for end-to-end flows
  - Data quality tests (great_expectations or similar)
  - Mock data generators for testing
- **Outputs**: Test reports, coverage reports

---

### 3. Technology-Specific Implementation Details

Based on the tech stack provided:

- **Language**: Specify Python/R/SQL based on tech_stack.md preferences
- **Computing Platform**: Databricks/CDSW/local - include platform-specific optimizations
- **Distributed Computing**: If using Spark, provide Spark-specific implementations
- **Database Interactions**: Include connection pooling, transaction management
- **Package Dependencies**: List all required libraries with version specifications

---

### 4. Configuration Management

Provide structure for:
- **Database configs** (`config/database.yml`): Connection strings, credentials management
- **Analysis configs** (`config/analysis.yml`): Model hyperparameters, thresholds, feature lists
- **Platform configs** (`config/platform.yml`): Cluster specs, resource allocation
- **Query templates** (`config/queries.yml` or `sql/`): Parameterized SQL queries

---

### 5. Execution Sequence

For each phase in the execution plan:

1. **Entry Point**: Main script to run (e.g., `python scripts/run_phase_1.py`)
2. **Dependencies**: Prerequisites from previous phases
3. **Execution Steps**: Ordered list of module calls
4. **Checkpoints**: Intermediate validation points
5. **Expected Outputs**: File paths, data volumes, quality metrics
6. **Estimated Runtime**: Approximate execution time
7. **Resource Requirements**: Memory, CPU, storage needs

---

### 6. Data Pipeline Architecture

Provide a clear flow diagram (in text/mermaid format) showing:
- Data sources → Extraction → Transformation → Analysis → Outputs
- Dependency arrows between components
- Caching/intermediate storage points
- Parallel vs. sequential execution paths

---

### 7. Error Handling & Monitoring

Include:
- **Logging Strategy**: Log levels, log file organization, structured logging
- **Error Recovery**: Retry logic, checkpoint restart mechanisms
- **Data Quality Alerts**: Automated checks for data anomalies
- **Performance Monitoring**: Execution time tracking, resource utilization
- **Notification System**: Email/Slack alerts for failures

---

### 8. Reproducibility & Version Control

Specify:
- **Environment Management**: `requirements.txt` / `environment.yml` / `Pipfile`
- **Random Seed Management**: How to ensure reproducible results
- **Data Versioning**: DVC or similar for tracking data changes
- **Model Versioning**: MLflow or similar for experiment tracking
- **Documentation**: README files, API documentation standards

---

### 9. Deployment & Operationalization

Include:
- **Scheduling**: Cron jobs / Airflow DAGs / platform-specific schedulers
- **Automation**: Scripts for end-to-end automation
- **Dashboard Deployment**: How to host/deploy interactive dashboards
- **Report Distribution**: Automated report generation and distribution
- **Model Serving**: If applicable, how to serve models for inference

---

### 10. Code Examples

For critical components, provide **skeleton code** showing:
- Function signatures with type hints
- Class structure with key methods
- Configuration file examples
- SQL query templates
- Error handling patterns

**Important**: Focus on architecture and structure, not full implementation. Provide enough detail that a developer can fill in the business logic.

---

## Output Format

**CRITICAL**: Generate a **separate, complete implementation plan for EACH individual data flow** identified in the execution plan. Do not create a single consolidated plan.

For each data flow (e.g., Epic-001, Epic-002, etc.), create a standalone document with the following structure:

### File Naming Convention
Save each implementation plan as:
```
docs/methodology/implementation_plans/[epic-id]-[epic-name]-implementation-plan.md
```

Example:
- `epic-001-facility-utilization-bottleneck-analysis-implementation-plan.md`
- `epic-002-disease-outbreak-surveillance-system-implementation-plan.md`

### Structure for Each Data Flow Implementation Plan

```markdown
# Implementation Plan: [Epic ID] - [Epic Name]

## Executive Summary
- **Epic**: [Epic ID and Name]
- **Objective**: [Brief description from data flow]
- **Estimated Duration**: [Timeline from execution plan]
- **Dependencies**: [Prerequisites from other epics]
- **Key Deliverables**: [Main outputs]

## 1. Data Flow-Specific Project Structure

**CRITICAL**: Create a dedicated folder structure for each epic to organize all related code, configurations, and outputs.

### Epic Folder Structure

```
epics/
└── [epic_id]/                           # e.g., epic-001, epic-002
    ├── README.md                        # Epic overview and quick start guide
    ├── config/
    │   ├── [epic_id]_config.yml        # Epic-specific configuration
    │   ├── [epic_id]_params.yml        # Analysis parameters
    │   └── [epic_id]_queries.yml       # Query configurations
    ├── src/
    │   ├── __init__.py
    │   ├── extraction.py                # Data extraction module
    │   ├── features.py                  # Feature engineering module
    │   ├── analysis.py                  # Analysis and modeling module
    │   ├── visualization.py             # Visualization module
    │   └── utils.py                     # Epic-specific utilities
    ├── scripts/
    │   ├── 01_extract_data.py          # Step 1: Extract data
    │   ├── 02_engineer_features.py     # Step 2: Feature engineering
    │   ├── 03_run_analysis.py          # Step 3: Run analysis
    │   ├── 04_generate_visualizations.py  # Step 4: Create visualizations
    │   ├── 05_generate_reports.py      # Step 5: Generate reports
    │   └── run_full_pipeline.py        # Orchestration script
    ├── notebooks/
    │   ├── 01_exploration.ipynb        # Data exploration
    │   ├── 02_feature_analysis.ipynb   # Feature analysis
    │   ├── 03_modeling.ipynb           # Model development
    │   └── 04_results_viz.ipynb        # Results visualization
    ├── sql/
    │   ├── extraction_queries.sql      # Data extraction SQL
    │   ├── validation_queries.sql      # Data validation SQL
    │   └── aggregation_queries.sql     # Aggregation queries
    ├── tests/
    │   ├── __init__.py
    │   ├── test_extraction.py          # Tests for extraction module
    │   ├── test_features.py            # Tests for features module
    │   ├── test_analysis.py            # Tests for analysis module
    │   └── test_integration.py         # End-to-end integration tests
    ├── data/
    │   ├── raw/                        # Raw extracted data
    │   ├── processed/                  # Processed data
    │   └── features/                   # Feature datasets
    ├── results/
    │   ├── metrics/                    # Analysis metrics
    │   ├── tables/                     # Result tables
    │   └── exports/                    # Exported data
    ├── reports/
    │   ├── figures/                    # Generated charts/plots
    │   ├── dashboards/                 # Dashboard files
    │   └── documents/                  # Final reports (PDF/PowerPoint)
    └── logs/
        ├── extraction.log              # Extraction logs
        ├── pipeline.log                # Pipeline execution logs
        └── errors.log                  # Error logs
```

### Example: Epic-001 Structure
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
    │   ├── extraction.py               # Extract facility utilization data
    │   ├── features.py                 # Calculate bottleneck metrics
    │   ├── analysis.py                 # Bottleneck analysis algorithms
    │   ├── visualization.py            # Utilization visualizations
    │   └── utils.py
    ├── scripts/
    │   ├── 01_extract_data.py
    │   ├── 02_engineer_features.py
    │   ├── 03_run_analysis.py
    │   ├── 04_generate_visualizations.py
    │   ├── 05_generate_reports.py
    │   └── run_full_pipeline.py
    ├── notebooks/
    ├── sql/
    ├── tests/
    ├── data/
    ├── results/
    ├── reports/
    └── logs/
```

### Shared Components

For reusable code across all epics, maintain a shared utilities folder:

```
src/
└── shared/
    ├── __init__.py
    ├── db_connector.py                 # Database connection utilities
    ├── data_validator.py               # Common validation functions
    ├── logging_config.py               # Logging configuration
    ├── config_loader.py                # Configuration loader
    └── common_transforms.py            # Reusable transformations
```

## 2. Module Specifications

### 2.1 Data Extraction & Loading
#### Module: `epics/[epic_id]/src/extraction.py`
- **Purpose**: [What data this flow extracts]
- **Data Sources**: [Specific tables/APIs for THIS flow]
- **Key Functions**: [Function signatures]
- **Extraction Logic**: [SQL queries, filters, time windows]
- **Validation Rules**: [Data quality checks specific to this flow]
- **Code Skeleton**: [Example code]

### 2.2 Feature Engineering & Transformation
#### Module: `epics/[epic_id]/src/features.py`
- **Purpose**: [What features this flow creates]
- **Feature List**: [Specific features for THIS analysis]
- **Transformation Logic**: [Calculations, aggregations]
- **Code Skeleton**: [Example code]

### 2.3 Analysis & Modeling
#### Module: `epics/[epic_id]/src/analysis.py`
- **Purpose**: [What analysis this flow performs]
- **Analytical Methods**: [Statistical tests, models specific to this flow]
- **Model Parameters**: [Hyperparameters for THIS flow]
- **Code Skeleton**: [Example code]

### 2.4 Visualization & Reporting
#### Module: `epics/[epic_id]/src/visualization.py`
- **Purpose**: [What visualizations this flow generates]
- **Chart Types**: [Specific to this analysis]
- **Dashboard Components**: [If applicable]
- **Code Skeleton**: [Example code]

## 3. Flow-Specific Configuration Files

### `epics/[epic_id]/config/[epic_id]_config.yml`
[Configuration specific to this data flow]
```yaml
epic_id: [epic-id]
epic_name: [epic-name]
data_sources:
  - [tables/sources specific to this flow]
features:
  - [features specific to this flow]
parameters:
  - [analysis parameters for this flow]
output_paths:
  raw_data: epics/[epic_id]/data/raw/
  processed_data: epics/[epic_id]/data/processed/
  results: epics/[epic_id]/results/
  reports: epics/[epic_id]/reports/
```

### `epics/[epic_id]/sql/extraction_queries.sql`
[SQL queries specific to this data flow]

## 4. Execution Workflow for This Data Flow

### Step-by-Step Execution
```bash
# Navigate to epic directory
cd epics/[epic_id]/

# Step 1: Extract data for this flow
python scripts/01_extract_data.py

# Step 2: Engineer features for this flow
python scripts/02_engineer_features.py

# Step 3: Run analysis for this flow
python scripts/03_run_analysis.py

# Step 4: Generate visualizations for this flow
python scripts/04_generate_visualizations.py

# Step 5: Create reports for this flow
python scripts/05_generate_reports.py

# OR run the entire pipeline at once
python scripts/run_full_pipeline.py
```

### Main Orchestration Script
#### `epics/[epic_id]/scripts/run_full_pipeline.py`
[Main orchestration script for this entire data flow]

## 5. Testing Strategy for This Data Flow

### Unit Tests: `epics/[epic_id]/tests/test_*.py`
[Tests specific to this flow's functions]

### Integration Tests: `epics/[epic_id]/tests/test_integration.py`
[End-to-end tests for this flow]

### Data Quality Tests: `epics/[epic_id]/tests/test_data_quality.py`
[Validation tests for this flow's data]

### Running Tests
```bash
cd epics/[epic_id]/
pytest tests/
```

## 6. Outputs & Deliverables for This Data Flow

### Data Outputs
- **Location**: `epics/[epic_id]/data/`
  - `raw/` - Raw extracted data
  - `processed/` - Processed data
  - `features/` - Feature datasets
- **Files**: [Specific output files for this flow]

### Analysis Results
- **Location**: `epics/[epic_id]/results/`
  - `metrics/` - Analysis metrics
  - `tables/` - Result tables
  - `exports/` - Exported data
- **Files**: [Metrics, tables specific to this flow]

### Visualizations
- **Location**: `epics/[epic_id]/reports/figures/`
- **Files**: [Charts specific to this flow]

### Reports
- **Location**: `epics/[epic_id]/reports/documents/`
- **Files**: [Executive reports for this flow]

## 7. Monitoring & Alerts for This Data Flow

### Key Metrics to Track
[Metrics specific to this flow]

### Alert Thresholds
[Data quality thresholds for this flow]

### Logging Configuration
- **Location**: `epics/[epic_id]/logs/`
- **Files**: 
  - `extraction.log` - Data extraction logs
  - `pipeline.log` - Pipeline execution logs
  - `errors.log` - Error logs

## 8. Dependencies & Integration

### Upstream Dependencies
[What this flow depends on from other epics]

### Downstream Consumers
[What other epics depend on this flow's outputs]

### Shared Components
[Reusable modules from `src/shared/`]

### Cross-Epic Data Sharing
```
epics/
├── epic-001/
│   └── results/exports/                 # Exported data for other epics
├── epic-002/
│   └── data/imports/                    # Imported data from other epics
└── shared_data/                         # Common reference data
```

## 9. Timeline & Milestones for This Data Flow

[Specific timeline from execution plan for THIS epic]

## 10. Success Criteria for This Data Flow

[How to measure success for THIS specific analysis]
```

### Implementation Plan Index

After generating all individual data flow implementation plans, create an index file:

**File**: `docs/methodology/implementation_plans/README.md`

```markdown
# Implementation Plans Index

Refer to [Shared Components](../data_flows/shared_components.md) for reusable utilities across multiple epics.
```

---

## Quality Criteria

Your implementation plan must:

1. ✅ **Be Executable**: Provide enough detail that a developer can implement it
2. ✅ **Follow Best Practices**: Use industry-standard patterns (SOLID, DRY, separation of concerns)
3. ✅ **Be Scalable**: Handle the data volumes specified in the execution plan
4. ✅ **Be Maintainable**: Include logging, error handling, and documentation
5. ✅ **Be Reproducible**: Ensure consistent results across runs
6. ✅ **Match Tech Stack**: Use only technologies specified in project context
7. ✅ **Respect Dependencies**: Follow the dependency graph from execution plan
8. ✅ **Include Testing**: Specify unit tests, integration tests, data quality tests
9. ✅ **Handle Failures**: Include retry logic, error recovery, notifications
10. ✅ **Document Thoroughly**: README files, docstrings, inline comments

---

## Key Principles

- **Modularity**: Each component should be independently testable
- **Reusability**: Common functions should be in utility modules
- **Configurability**: Avoid hardcoding - use config files
- **Observability**: Log everything important, track metrics
- **Fail-Fast**: Validate inputs early, fail loudly on errors
- **Idempotency**: Re-running should be safe (checkpoints, upserts)
- **Performance**: Optimize for the data volumes in the execution plan

---

## Notes

- This is an **implementation plan**, not a high-level design document
- Provide **concrete file paths, function names, and module structures**
- Include **skeleton code** for complex components
- Specify **exact package names** for dependencies
- Reference the **specific phases and stories** from the execution plan
- Align with the **tech stack and data sources** from project context

---

## Begin

Now, generate the complete implementation plan based on the execution plan and project context provided.
