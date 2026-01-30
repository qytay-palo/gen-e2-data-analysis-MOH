# Data Science Lifecycle Automation System - Implementation Summary

## Overview

A comprehensive prompt-based automation system has been created to manage end-to-end data science and analytics projects. This system enables automated execution of complex analytical workflows through a series of coordinated prompts.

## What Was Created

### 1. Planning & Orchestration Prompts

#### [`4-generate-lifecycle-and-execution-plan.prompt.md`](.github/prompts/4-generate-lifecycle-and-execution-plan.prompt.md)
**Purpose**: Analyzes user stories and generates a comprehensive execution plan

**What it does**:
- Maps each user story to appropriate data science lifecycle stages
- Creates an execution sequence organized into "waves" (phases)
- Generates a routing configuration that specifies which prompts to call
- Estimates effort and identifies dependencies
- Produces a detailed, executable project plan

**Inputs**:
- User stories from `docs/objectives/user_stories/`
- Project context documentation
- Data sources and technical stack information

**Outputs**:
- `docs/project_context/execution_plan.yml` - Complete execution plan
- `config/prompt_routing.yml` - Prompt routing configuration
- `scripts/execute_lifecycle.py` - Automation pseudocode

#### [`5-orchestrate-execution.prompt.md`](.github/prompts/5-orchestrate-execution.prompt.md)
**Purpose**: Executes the project according to the generated plan

**What it does**:
- Loads the execution plan and routing configuration
- Orchestrates sequential execution of stages
- Routes to appropriate stage-specific prompts
- Manages context and artifact passing between stages
- Handles errors and provides recovery mechanisms
- Tracks progress and generates execution logs

**Key Features**:
- Checkpointing for recovery from failures
- Input/output validation
- Progress tracking and reporting
- Parallel execution support for independent tasks
- Error handling and recovery procedures

### 2. Stage-Specific Prompt Templates

Three comprehensive stage prompts were created as examples:

#### [`stages/data-acquisition.prompt.md`](.github/prompts/stages/data-acquisition.prompt.md)
**Purpose**: Extract data from source systems

**Covers**:
- Database connections and authentication
- Query execution with batching
- Data validation during extraction
- Metadata and lineage documentation
- Extraction reporting

**Outputs**: Raw datasets, extraction scripts, metadata files, extraction reports

#### [`stages/eda.prompt.md`](.github/prompts/stages/eda.prompt.md)
**Purpose**: Conduct exploratory data analysis

**Covers**:
- Univariate analysis (distributions, statistics)
- Bivariate/multivariate analysis (correlations, relationships)
- Temporal pattern detection
- Statistical testing
- Hypothesis formulation

**Outputs**: EDA notebooks, visualizations, insights summaries

#### [`stages/model-training.prompt.md`](.github/prompts/stages/model-training.prompt.md)
**Purpose**: Train and optimize predictive models

**Covers**:
- Baseline model establishment
- Multiple algorithm training
- Hyperparameter optimization
- Experiment tracking (MLflow)
- Model comparison and selection

**Outputs**: Trained models, training logs, performance metrics, model comparisons

### 3. Documentation

#### [`prompts/README.md`](.github/prompts/README.md)
Comprehensive guide covering:
- System overview and architecture
- Prompt file descriptions and usage
- Detailed workflow instructions
- Examples for different project types
- Best practices for authors and users
- Troubleshooting guide
- Advanced automation patterns (LangGraph integration)

## Data Science Lifecycle Framework

The system is built around 12 standard lifecycle stages:

1. **Business Understanding & Scoping**
2. **Data Acquisition & Access**
3. **Data Quality Assessment**
4. **Exploratory Data Analysis**
5. **Data Preparation & Transformation**
6. **Feature Engineering**
7. **Model Development**
8. **Model Evaluation**
9. **Statistical Analysis**
10. **Visualization & Reporting**
11. **Model Deployment & Operationalization**
12. **Monitoring & Maintenance**

Each stage has:
- Defined inputs and outputs
- Step-by-step process instructions
- Quality checks
- Error handling guidance

## How It Works

### Step-by-Step Execution Flow

```
1. Start with user stories
   ↓
2. Generate Execution Plan (Prompt 4)
   - Analyze user stories
   - Map to lifecycle stages
   - Create execution waves
   - Generate routing config
   ↓
3. Execute Project (Prompt 5)
   - Load execution plan
   - For each wave:
     - For each user story:
       - For each lifecycle stage:
         → Route to stage-specific prompt
         → Execute stage with inputs
         → Validate outputs
         → Pass outputs to next stage
   ↓
4. Generate Reports and Artifacts
   - Final summary report
   - All stage outputs
   - Execution logs
```

### Example: Forecasting User Story Execution

Given user story: "Forecast daily attendance volumes"

**Lifecycle stages identified**:
1. Data Acquisition → Extract attendance history
2. Data Quality Assessment → Validate data completeness
3. Exploratory Data Analysis → Understand temporal patterns
4. Feature Engineering → Create lag and rolling features
5. Model Development → Train time-series models
6. Model Evaluation → Assess forecast accuracy
7. Visualization & Reporting → Create forecast dashboard

**Execution**:
- Orchestrator calls each stage prompt in sequence
- Each stage produces outputs (datasets, notebooks, models)
- Outputs from one stage become inputs to the next
- All execution logged for reproducibility

## Key Features

### 1. Automated Routing
- Intelligent routing based on lifecycle stage
- Configurable prompt file mappings
- Context-aware input preparation

### 2. Context Management
- Artifacts passed between stages
- Global artifact registry
- State tracking and checkpointing

### 3. Error Handling
- Prerequisite validation
- Output validation
- Recovery procedures
- User intervention prompts

### 4. Progress Tracking
- Real-time progress updates
- Execution logs
- Wave-level checkpoints
- Summary reports

### 5. Flexibility
- Parallel execution support
- Wave-based organization
- Resumable from checkpoints
- Dry-run capability

## Usage Examples

### Simple Descriptive Analysis
```yaml
waves:
  - wave_1:
      user_stories: ["establish-data-quality", "eda"]
      stages: [Data Acquisition, Quality Check, EDA, Reporting]
      duration: "1-2 weeks"
```

### Predictive Modeling Project
```yaml
waves:
  - wave_1_foundation:
      stages: [Data Acquisition, Quality Check]
  - wave_2_analysis:
      stages: [EDA, Data Prep, Feature Engineering]
  - wave_3_modeling:
      stages: [Model Training, Model Evaluation]
  - wave_4_deployment:
      stages: [Visualization, Reporting]
```

## Benefits

### For Data Scientists
- ✅ Structured approach to projects
- ✅ Reduced manual workflow management
- ✅ Reusable stage templates
- ✅ Consistent documentation

### For Teams
- ✅ Standardized processes
- ✅ Clear handoffs between stages
- ✅ Reproducible workflows
- ✅ Knowledge sharing via prompts

### For Organizations
- ✅ Scalable project execution
- ✅ Quality control checkpoints
- ✅ Audit trails and logging
- ✅ Faster project delivery

## Extending the System

### Adding New Stage Prompts

1. Create new prompt file in `stages/`
2. Follow the template structure:
   - Purpose
   - Inputs
   - Process (step-by-step)
   - Outputs
   - Quality checks
   - Next steps

3. Update `config/prompt_routing.yml`:
```yaml
your_new_stage:
  prompt_file: ".github/prompts/stages/your-stage.prompt.md"
  inputs_required: [...]
  outputs_generated: [...]
```

### Creating Custom Execution Plans

Modify the execution plan YAML to:
- Add/remove waves
- Reorder stages
- Adjust parallel execution
- Customize stage parameters

## Production Implementation

### Option 1: Manual Execution
- Execute prompts manually in VS Code
- Use Copilot to interpret and execute instructions
- Track progress manually

### Option 2: Python Orchestrator
```python
# scripts/execute_lifecycle.py
from lifecycle_orchestrator import LifecycleOrchestrator

orchestrator = LifecycleOrchestrator(
    plan_path="docs/project_context/execution_plan.yml",
    routing_config="config/prompt_routing.yml"
)

orchestrator.execute()
```

### Option 3: LangGraph Automation
```python
# Advanced: Full automation with LangGraph
from langgraph.graph import StateGraph
from lifecycle_nodes import create_lifecycle_graph

graph = create_lifecycle_graph(execution_plan)
app = graph.compile()
result = app.invoke(initial_state)
```

## Files Created

```
.github/prompts/
├── 4-generate-lifecycle-and-execution-plan.prompt.md  # NEW
├── 5-orchestrate-execution.prompt.md                   # NEW
├── README.md                                            # NEW
└── stages/                                              # NEW
    ├── data-acquisition.prompt.md                       # NEW
    ├── eda.prompt.md                                    # NEW
    └── model-training.prompt.md                         # NEW
```

## Next Steps

### Immediate
1. ✅ Review the created prompts
2. ✅ Test on a sample user story
3. Generate execution plan for existing user stories

### Short-term
1. Create remaining stage prompts:
   - `data-quality-check.prompt.md`
   - `data-preparation.prompt.md`
   - `feature-engineering.prompt.md`
   - `model-evaluation.prompt.md`
   - `statistical-analysis.prompt.md`
   - `visualization-reporting.prompt.md`

2. Test full workflow on 1-2 user stories

### Long-term
1. Implement Python orchestrator script
2. Integrate with LangGraph for automation
3. Add monitoring and alerting
4. Create prompt library for domain-specific tasks
5. Build web UI for execution tracking

## Validation

To validate the system works:

1. **Test Prompt 4**:
   ```
   Use prompt: 4-generate-lifecycle-and-execution-plan.prompt.md
   Input: Read user stories from docs/objectives/user_stories/
   Expected output: execution_plan.yml and prompt_routing.yml
   ```

2. **Test Prompt 5**:
   ```
   Use prompt: 5-orchestrate-execution.prompt.md
   Input: Load generated execution_plan.yml
   Expected: Sequential execution of stages with logging
   ```

3. **Test Stage Prompt**:
   ```
   Use prompt: stages/eda.prompt.md
   Input: dataset_path, analysis_objectives
   Expected: EDA notebook with visualizations
   ```

## Support and Maintenance

### Documentation
- Main README: `.github/prompts/README.md`
- Individual prompts have embedded documentation
- Examples provided in each prompt file

### Updates
- Version prompts as they evolve
- Document changes in prompt headers
- Maintain backward compatibility

### Troubleshooting
- Check execution logs in `results/execution_logs/`
- Review checkpoint files for state
- Validate prerequisite completion
- Ensure artifact paths are correct

---

**Created**: 2026-01-28  
**Author**: Expert Context Engineer with Data Science Domain Expertise  
**Status**: Ready for testing and deployment
