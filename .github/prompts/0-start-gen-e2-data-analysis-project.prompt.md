---
description: Gen-E2 Data Analysis Project Initialization (instructive prompts version)
model: claude-sonnet-4.5
---

<!-- Metadata:
Stage: Development
Rule Name: start-gen-e2-data-analysis-project
Rule Version: latest
-->

## Questions to Ask

1. **Project Objectives & Scope**:
- **Primary Goal**: What are the main goals and business problem we are solving? 

2. **Data Sources & Availability**:
   - **Primary Datasets**: What datasets will be used, and where are they located?
   - **Data Access**: How will we connect? (APIs, databases, files, data warehouses)
   - **Data Volume**: Expected data historical depth?

3. **Stakeholders**:
   - Who are the key stakeholders and their roles?

## Actions Based on Answers
1. **Data Discovery & Inventory**:
   - **Catalog Available Data**: Review [project_context/data_sources.md](project_context/data_sources.md) and existing documentation to identify all accessible data sources
   - **Build Data Dictionary**: For each data source, document in `docs/data_dictionary/`:
     - Database/table names and locations
     - Field definitions (name, type, description, business context)
     - Data quality metrics (completeness, accuracy, consistency)
     - Access methods and permission requirements
   - **Organize by Domain**: Structure the data dictionary by business domains for easy reference

2. **Data Assessment & Selection**:
   - **Map to Business Objectives**: Evaluate data dictionary entries against project goals
   - **Data Choices**: Suggest datasets/tables most relevant to each objective
   - **Document Data Requirements**: Create data specification including:
     - Selected tables and fields with rationale
     - Required time periods and granularity
     - Expected data volumes
     - Transformation and processing needs

3. **Define Analytics Approach**:
   - **Frame the Problem**: Translate business objectives into data science and/or analytics problems
   - **Analytical Solution**: For each opportunity, suggest relevant and feasible analytical approaches (like Statistical analysis, Visualisation, Machine Learning)
   - **Assess Feasibility**: Validate that selected data supports the proposed approach
     - Check data completeness for target variables
     - Verify sufficient sample size for statistical power
     - Confirm feature availability for model training
   - **Baseline & Benchmarks**: Define current performance or industry benchmarks to compare against
   - **Prioritize Workstreams**: Rank by business impact, technical feasibility, and resource requirements
   - **Document in `docs/objectives/`**: Include:
     - Problem statement and hypothesis
     - Success criteria and metrics
     - Data-to-insight pathway
     - Expected deliverables and format
     - Validation strategy

4. **Select Technical Stack**:
   - **Reference Standards**: Review [docs/project_context.md/tech_stack.md](docs/project_context.md/tech_stack.md) for recommended platforms
   - **Choose Platform**: Identify tech stack that is needed to configure projects based on information provided above.
   - **Justify Exceptions**: If proposing alternatives, specify:
     - Technical limitations of approved stack
     - Alternative tool and specific capabilities needed
     - Integration and maintenance considerations
   - **Document Dependencies**: List required packages, libraries, and frameworks aligned with analytical approach

5. **Configure Project Environment**:
   - **Setup Development Environment**: Suggest environment setup based on project requirements (like Databricks workspace, database connections, langauge environments, etc)
   - **Document in docs/**: Include platform choice, setup instructions, and data access procedures
   - **Initialize Version Control**: Configure .gitignore for data files, credentials, and platform-specific artifacts

6. **Update Project Folder Structure**:
Below is the base folder structure:

```
.
├── README.md
├── requirements.txt  # [PHASE 0] Python dependencies
├── environment.yml   # [PHASE 0] Conda environment (optional)
├── docs/             # [PHASE 1] Context & Understanding
│   ├── index.md         # → 1: Central documentation hub (navigation)
│   └── / 
│   ├── objectives/      # → 2: PROJECT GOALS: What to achieve
│   ├── data_dictionary/ # → 3: Understand data: schemas, fields, definitions
│   └── methodology/     # → 4: Understand approach: statistical methods, frameworks
├── config/           # [PHASE 2] Project Configuration
│   └── *.yml, *.json       # → Parameters, settings, environment configs
├── data/             # [PHASE 3] Data Acquisition & Preparation
│   ├── 1_raw/           # → 1: Original immutable source data
│   ├── 2_external/      # → 2: External reference data (demographics, benchmarks)
│   ├── 3_interim/       # → 3: Intermediate transformation outputs
│   └── 4_processed/     # → 4: Final cleaned datasets (analysis-ready)
├── notebooks/        # [PHASE 4] Interactive Exploration & Analysis
│   ├── 1_exploratory/   # → 1: Initial EDA, data profiling, hypothesis generation
│   └── 2_analysis/      # → 2: Deep-dive analysis, final insights, documentation
│   └── 3_feature_engineering/ # → 3: Feature creation, variable transformations 
├── src/              # [PHASE 5] Production Code Development
│   ├── utils/           # → Foundation: Helper functions, common utilities
│   ├── data/            # → Pipeline 1: ETL, cleaning, validation
│   ├── features/        # → Pipeline 2: Feature engineering, variable transformations
│   ├── analysis/        # → Pipeline 3: Statistical analysis, algorithms, visualizations
│   └── models/          # → Pipeline 5: Model training, hyperparameter tuning
├── tests/            # [PHASE 6] Quality Assurance
│   └── *.py             # → Unit tests, integration tests, data validation tests
├── models/           # [PHASE 7] Model Development & Storage
│   └── *.pkl, *.h5, *.joblib # → Trained models, model artifacts, serialized objects
├── results/          # [PHASE 8] Analysis Outputs
│   ├── 1_tables/        # → Output 1: Summary statistics, analytical tables (CSV/Excel)
│   ├── 2_metrics/       # → Output 2: Performance KPIs, evaluation metrics (JSON/CSV)
│   └── 3_exports/       # → Output 3: Stakeholder-ready data exports
├── reports/          # [PHASE 9] Stakeholder Communication
│   ├── 1_figures/       # → Component 1: Static visualizations (PNG/PDF)
│   ├── 2_dashboards/    # → Component 2: Interactive dashboards
│   └── 3_presentations/ # → Component 3: Executive summaries (PPTX/PDF)
└── scripts/          # [PHASE 10] Automation & Deployment
    └── *.py, *.R, *.sh  # → End-to-end pipelines, deployment scripts, automation
```
   - Update the project structure based on the answers and the opportunities identified in Action 1.
   - Update the README.md file, docs/index.md, and create necessary configuration files in the config/ directory to reflect the technical environment and project specifics.

7. **Environment Configuration**:
    - provide guidelines for handling environment variables, secrets management

8. **Code Quality and Standards**:
      - Define coding standards (PEP8 for Python, style guides for R)
      - Set up linters and formatters (like Black, Flake8)
      - Establish unit testing frameworks and coverage targets

9. **CI/CD Pipeline Setup**:
    - suggest CI/CD tools and services based on the chosen tech stack (like GitHub Actions, Jenkins, GitLab CI) 
    - ensuring that code formatting, linting, and tests are automatically run on each commit or pull request
    - **Document in `docs/CI_CD.md`**: Pipeline architecture, trigger conditions, troubleshooting

## Final Steps

After completing all actions above, produce the following deliverables:

1. **Project Initialization Summary**:
   - Create comprehensive `README.md` with:
     - Project overview and business objectives
     - Quick start guide for new team members
     - Folder structure explanation
     - Installation and setup instructions
     - Key contacts and stakeholders
   
2. **Documentation Index** (`docs/index.md`):
   - Central navigation hub linking to all documentation
   - Organized by phase and purpose
   - Include status indicators for each document (planned, in-progress, complete)

3. **Configuration Files**:
   - Environment files (`.env.example` with placeholder values)
   - Dependency management files (requirements.txt, environment.yml)
   - Configuration templates in `config/` directory
   - `.gitignore` configured for the project type

4. **Initial Notebook Templates**:
   - Create starter notebooks in `notebooks/1_exploratory/`:
     - `00-environment-setup.ipynb`: Test installations and connections
     - `01-data-loading.ipynb`: Template for loading data sources
     - `02-initial-eda.ipynb`: Basic exploratory data analysis structure

5. **Core Documentation**:
   - `docs/objectives/project-charter.md`: Business problem, goals, success metrics
   - `docs/data_dictionary/README.md`: Instructions for documenting data sources
   - `docs/methodology/README.md`: Placeholder for analytical approaches
   - `docs/ARCHITECTURE.md`: System architecture and data flow diagrams (if applicable)

6. **Development Guidelines**:
   - `CONTRIBUTING.md`: Code contribution guidelines and review process
   - `docs/CODING_STANDARDS.md`: Language-specific style guides and best practices
   - `docs/TESTING_GUIDE.md`: Testing strategy and framework usage

7. **Project Roadmap**:
   - Document project phases with timeline estimates
   - Identify dependencies and critical path
   - Define milestones and review checkpoints
   - List known risks and mitigation strategies

8. **Stakeholder Communication Plan**:
   - Define reporting frequency and formats
   - Create presentation template in `reports/3_presentations/`
   - Set up initial dashboard wireframes or mockups
   - Schedule kickoff meeting to review all deliverables

9. **Quality Assurance Setup**:
   - Create initial test structure in `tests/`
   - Define data validation rules template
   - Set up code coverage tracking
   - Document QA process and acceptance criteria

10. **Review and Validation**:
    - Review all deliverables with technical lead and stakeholders
    - Validate data access and permissions
    - Confirm technical stack approvals
    - Get sign-off on project charter and roadmap
    - Schedule next steps: data extraction, EDA kickoff, or sprint planning

**Success Criteria**: Project is ready for development when:
- ✅ All team members can clone and run setup successfully
- ✅ Data sources identified and access confirmed
- ✅ Documentation structure is complete and navigable
- ✅ Stakeholders approve objectives and approach
- ✅ Development environment is configured and tested
- ✅ First milestone tasks are clearly defined and assigned

````







