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

Structure your response as follows:

```markdown
# Implementation Plan: [Project Name]

## 1. Project Structure
[Directory tree and organization]

## 2. Module Specifications

### Phase 1: [Phase Name]
#### Module: [Module Name]
- **Purpose**: [What it does]
- **Location**: [File path]
- **Dependencies**: [Prerequisites]
- **Key Functions**: [Function signatures]
- **Inputs**: [Data sources]
- **Outputs**: [Generated artifacts]
- **Code Skeleton**: [Example code]

[Repeat for each module in each phase]

## 3. Configuration Files
[Configuration structure and examples]

## 4. Execution Workflow
[Step-by-step execution instructions]

## 5. Testing Strategy
[Testing approach and examples]

## 6. Deployment Guide
[How to deploy and operationalize]

## 7. Monitoring & Maintenance
[Ongoing monitoring strategy]
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
