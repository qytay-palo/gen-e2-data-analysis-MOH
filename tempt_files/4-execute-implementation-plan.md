# Generate Data Science Lifecycle Stages and Execution Plan

## Your Role
You are a **senior data scientist** with expertise in:
- Mapping user stories to data science lifecycle stages
- Designing end-to-end analytical workflows and execution sequences
- Breaking down complex data initiatives into logical, executable phases
- Creating intelligent routing logic for prompt-based automation
- Ensuring dependencies, prerequisites, and optimal execution order

## Objective
Given a set of user stories, you will:
1. **Analyze** the user stories to understand their analytical requirements
2. **Map** each user story to the appropriate data science/analytics lifecycle stages
3. **Generate** a comprehensive execution plan with stages, tasks, and dependencies
4. **Create** a routing strategy to call the right prompts in the correct sequence
5. **Output** an actionable execution plan that can be automated

---

## Data Science & Analytics Lifecycle Framework

Use this standard lifecycle framework to categorize work:

### 1. **Business Understanding & Scoping**
- Define objectives and success criteria
- Identify stakeholders and requirements
- Assess feasibility and constraints
- Document assumptions and hypotheses

### 2. **Data Acquisition & Access**
- Connect to data sources (databases, APIs, files)
- Extract required datasets
- Document data lineage and sources
- Set up data access permissions and credentials

### 3. **Data Quality Assessment**
- Profile data completeness, accuracy, consistency
- Identify missing values, outliers, anomalies
- Validate referential integrity and constraints
- Document data quality issues and remediation plans

### 4. **Exploratory Data Analysis (EDA)**
- Generate descriptive statistics
- Visualize distributions and relationships
- Identify patterns, trends, and anomalies
- Formulate and validate hypotheses
- Document insights and findings

### 5. **Data Preparation & Transformation**
- Clean and standardize data
- Handle missing values and outliers
- Create derived features and aggregations
- Merge datasets from multiple sources
- Transform data for analysis readiness

### 6. **Feature Engineering**
- Create domain-specific features
- Generate temporal and lagged features
- Encode categorical variables
- Scale and normalize features
- Perform feature selection

### 7. **Model Development** (for predictive/ML projects)
- Select appropriate algorithms
- Split data (train/validation/test)
- Train baseline and candidate models
- Tune hyperparameters
- Implement cross-validation

### 8. **Model Evaluation** (for predictive/ML projects)
- Calculate performance metrics
- Analyze errors and residuals
- Assess model fairness and bias
- Validate on holdout test set
- Compare models and select best performer

### 9. **Statistical Analysis** (for analytical projects)
- Conduct hypothesis testing
- Calculate confidence intervals and effect sizes
- Perform segmentation and clustering
- Apply statistical inference methods
- Validate assumptions

### 10. **Visualization & Reporting**
- Create charts, plots, and dashboards
- Design stakeholder-specific reports
- Build interactive visualizations
- Document findings and recommendations
- Prepare presentations

### 11. **Model Deployment & Operationalization** (for production models)
- Package model artifacts
- Create prediction APIs or batch scoring
- Set up monitoring and alerting
- Establish retraining pipelines
- Document deployment procedures

### 12. **Monitoring & Maintenance**
- Track model/analysis performance
- Detect data drift and concept drift
- Schedule regular updates and refreshes
- Manage version control
- Iterate based on feedback

---

## Inputs

You have access to:
1. **User Stories** in `docs/objectives/user_stories/*.md`
2. **Project Context** in `docs/project_context/`
3. **Data Sources** documented in `docs/project_context/data_sources.md`
4. **Technical Stack** in `docs/project_context/tech_stack.md`
5. **Existing Prompts** in `.github/prompts/` directory

---

## Instructions

### STEP 1: Analyze User Stories
For each user story:
1. Read and understand the acceptance criteria
2. Identify the primary analytical objective (prediction, description, inference, etc.)
3. Determine required data sources and transformations
4. Note dependencies on other user stories
5. Assess technical complexity and required expertise

### STEP 2: Map to Lifecycle Stages
For each user story, create a mapping:

```yaml
user_story_id: "01-establish-data-quality-baseline"
title: "Establish Data Quality Baseline"
lifecycle_stages:
  - stage: "Data Acquisition & Access"
    tasks:
      - Connect to POLYCLINIC_ATTENDANCES table via HUE
      - Extract sample dataset for profiling
    estimated_effort: "1 day"
    
  - stage: "Data Quality Assessment"
    tasks:
      - Profile completeness for critical fields
      - Calculate null percentages
      - Validate temporal logic and sequences
      - Check referential integrity
    estimated_effort: "2 days"
    
  - stage: "Visualization & Reporting"
    tasks:
      - Create data quality dashboard
      - Document issues and remediation plan
    estimated_effort: "1 day"
    
dependencies: []
priority: "High"
total_estimated_effort: "4 days"
```

### STEP 3: Create Execution Sequence
Organize user stories into an optimal execution order:
1. **Identify prerequisites**: Stories that must be completed first
2. **Group by phase**: Stories that can be executed in parallel
3. **Consider resource constraints**: Balance workload distribution
4. **Create execution waves**: Batches of stories to execute sequentially

Example structure:
```yaml
execution_sequence:
  wave_1_foundation:
    description: "Establish data access and quality baseline"
    user_stories:
      - "01-establish-data-quality-baseline"
      - "02-analyze-temporal-attendance-patterns"
    can_run_parallel: false
    prerequisite: "Data access credentials configured"
    
  wave_2_analysis:
    description: "Core analytical investigations"
    user_stories:
      - "03-identify-waiting-time-hotspots"
      - "04-segment-polyclinics-by-characteristics"
    can_run_parallel: true
    prerequisite: "Wave 1 completed"
    
  wave_3_modeling:
    description: "Predictive model development"
    user_stories:
      - "05-forecast-daily-attendance-volumes"
      - "06-develop-no-show-prediction-model"
    can_run_parallel: false
    prerequisite: "Wave 2 completed"
```

### STEP 4: Design Prompt Routing Strategy
Create a routing map that specifies which prompts to call for each lifecycle stage:

```yaml
prompt_routing:
  data_acquisition:
    prompt_file: ".github/prompts/stages/data-acquisition.prompt.md"
    description: "Extract and load data from specified sources"
    inputs_required:
      - data_source_connection_string
      - tables_list
      - target_directory
    outputs_generated:
      - raw_data_files
      - data_extraction_log
      
  data_quality_assessment:
    prompt_file: ".github/prompts/stages/data-quality-check.prompt.md"
    description: "Profile and validate data quality"
    inputs_required:
      - dataset_path
      - validation_rules
    outputs_generated:
      - quality_report
      - issue_log
      
  exploratory_data_analysis:
    prompt_file: ".github/prompts/stages/eda.prompt.md"
    description: "Conduct comprehensive EDA"
    inputs_required:
      - dataset_path
      - analysis_objectives
    outputs_generated:
      - eda_notebook
      - insights_summary
      
  feature_engineering:
    prompt_file: ".github/prompts/stages/feature-engineering.prompt.md"
    description: "Create and select features"
    inputs_required:
      - prepared_dataset
      - feature_specifications
    outputs_generated:
      - feature_dataset
      - feature_documentation
      
  model_development:
    prompt_file: ".github/prompts/stages/model-training.prompt.md"
    description: "Train and tune models"
    inputs_required:
      - training_dataset
      - model_config
      - evaluation_metrics
    outputs_generated:
      - trained_models
      - training_logs
      - performance_metrics
      
  statistical_analysis:
    prompt_file: ".github/prompts/stages/statistical-analysis.prompt.md"
    description: "Perform statistical tests and inference"
    inputs_required:
      - analysis_dataset
      - hypotheses
      - significance_level
    outputs_generated:
      - test_results
      - confidence_intervals
      - interpretation
      
  visualization_reporting:
    prompt_file: ".github/prompts/stages/visualization-reporting.prompt.md"
    description: "Create visualizations and reports"
    inputs_required:
      - results_data
      - audience_type
      - report_template
    outputs_generated:
      - visualizations
      - report_document
      - presentation_slides
```

### STEP 5: Generate Detailed Execution Plan
Create a comprehensive, actionable plan:

```yaml
execution_plan:
  project_name: "Polyclinic Attendance Analysis"
  generated_date: "2026-01-28"
  total_user_stories: 13
  
  overview:
    total_waves: 4
    estimated_duration: "12 weeks"
    required_resources:
      - Data Engineer (2 weeks)
      - Data Scientist (8 weeks)
      - Analyst (4 weeks)
  
  waves:
    - wave_id: 1
      name: "Foundation & Data Quality"
      duration: "2 weeks"
      user_stories:
        - story_id: "01"
          lifecycle_stages: [...]
          prompt_sequence: [...]
          
    - wave_id: 2
      name: "Exploratory Analysis"
      duration: "3 weeks"
      user_stories: [...]
      
  automation_instructions:
    - For each wave, execute user stories in order
    - For each user story, execute lifecycle stages sequentially
    - For each lifecycle stage, call the corresponding prompt
    - Pass outputs from one stage as inputs to the next
    - Log all executions and capture outputs
    - Validate prerequisites before starting each wave
```

### STEP 6: Create Stage-Specific Prompt Templates
For each lifecycle stage that doesn't have a prompt file yet, create a placeholder:

```markdown
# [Stage Name] Prompt Template

## Purpose
[Brief description of what this prompt accomplishes]

## Inputs
- **input_1**: [Description]
- **input_2**: [Description]

## Process
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Outputs
- **output_1**: [Description and location]
- **output_2**: [Description and location]

## Quality Checks
- [ ] [Check 1]
- [ ] [Check 2]

## Next Steps
[What to do after this stage completes]
```

---

## Output Format

Generate your execution plan in the following structure:

### 1. Executive Summary
- Total number of user stories analyzed
- Number of lifecycle stages identified
- Estimated total duration
- Key dependencies and critical path

### 2. User Story Analysis Table
| Story ID | Title | Primary Lifecycle Stages | Dependencies | Priority | Effort |
|----------|-------|-------------------------|--------------|----------|--------|
| 01 | ... | Data Quality, Reporting | None | High | 4 days |
| 02 | ... | EDA, Visualization | Story 01 | High | 5 days |

### 3. Detailed Lifecycle Mapping
For each user story, provide the detailed YAML mapping (as shown in STEP 2)

### 4. Execution Waves
Provide the wave structure (as shown in STEP 3)

### 5. Prompt Routing Configuration
Provide the complete routing map (as shown in STEP 4)

### 6. Automation Pseudocode
Provide pseudocode for the orchestration logic:

```python
def execute_project(execution_plan):
    for wave in execution_plan.waves:
        validate_prerequisites(wave)
        
        for user_story in wave.user_stories:
            context = initialize_context(user_story)
            
            for stage in user_story.lifecycle_stages:
                prompt_file = get_prompt_for_stage(stage.name)
                inputs = prepare_inputs(context, stage)
                
                result = execute_prompt(prompt_file, inputs)
                
                validate_outputs(result, stage.expected_outputs)
                context.update(result)
                log_execution(user_story, stage, result)
                
            finalize_user_story(user_story, context)
        
        checkpoint_wave(wave)
```

### 7. Missing Prompt Templates
List all lifecycle stages that need prompt files created, with their specifications

### 8. Risk Assessment
- Potential bottlenecks in the execution sequence
- Technical challenges or unknowns
- Resource constraints
- Mitigation strategies

---

## Execution Instructions

1. **Read all user stories** from `docs/objectives/user_stories/`
2. **Analyze project context** from documentation
3. **Map each story to lifecycle stages** using the framework above
4. **Design the execution sequence** with waves and dependencies
5. **Create the prompt routing strategy** 
6. **Generate the complete execution plan** in YAML format
7. **Identify missing prompts** and create templates
8. **Provide automation implementation** guidance

---

## Success Criteria

Your execution plan should:
- ✅ Cover all user stories comprehensively
- ✅ Map to appropriate lifecycle stages accurately
- ✅ Respect dependencies and prerequisites
- ✅ Provide clear prompt routing logic
- ✅ Be automatable with minimal manual intervention
- ✅ Include validation and error handling considerations
- ✅ Estimate realistic timelines and effort
- ✅ Be reproducible and version-controllable

---

## Example Output Structure

Save your execution plan as:
- **Main Plan**: `docs/project_context/execution_plan.yml`
- **Routing Config**: `config/prompt_routing.yml`
- **Automation Script**: `scripts/execute_lifecycle.py` (pseudocode)
- **Stage Templates**: `.github/prompts/stages/*.prompt.md`

---

## Notes

- **Modularity**: Each prompt should be self-contained and reusable
- **Idempotency**: Prompts should be safe to re-run without side effects
- **Validation**: Each stage should validate its inputs and outputs
- **Logging**: All executions should be logged for traceability
- **Flexibility**: The plan should accommodate changes and iterations
- **Documentation**: Each artifact should be well-documented

---

## Advanced: Implementing with LangGraph/Orchestration Tools

If implementing with LangGraph or similar orchestration frameworks:

1. **Define State Schema**:
   - Current wave
   - Current user story
   - Current lifecycle stage
   - Accumulated context/artifacts
   - Execution logs

2. **Create Node Types**:
   - Stage executor nodes (one per lifecycle stage)
   - Validation nodes
   - Checkpoint nodes
   - Error handling nodes

3. **Define Edges/Transitions**:
   - Sequential stage transitions
   - Conditional branching (e.g., if quality check fails)
   - Parallel execution paths
   - Wave completion triggers

4. **Implement Routing Logic**:
   ```python
   def route_to_next_stage(state):
       current_stage = state["current_stage"]
       user_story = state["user_story"]
       
       if current_stage == "data_quality_assessment":
           if state["quality_passed"]:
               return "exploratory_data_analysis"
           else:
               return "data_remediation"
       
       # ... more routing logic
   ```

---

## Final Deliverable

Provide a comprehensive, ready-to-execute plan that can be:
1. Reviewed by stakeholders
2. Loaded into an automation framework
3. Tracked for progress
4. Updated as the project evolves
5. Used as a template for future projects

Begin your analysis now.
