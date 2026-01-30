---
description: Gen-E2 Data Analysis Project Initialization
model: claude-sonnet-4.5
---

<!-- Metadata:
Stage: Development
Rule Name: start-gen-e2-data-analysis-project
Rule Version: latest
-->

Your prompt instructions start here:

We will be starting a new Gen-e2 Project

Ask the following questions before proceeding:
## Questions to Ask
1. **Project Objectives**: 
   - What are the main goals and measurable success criteria?
   - What business decisions will this analysis inform?

2. **Stakeholders**: 
   - Who are the key stakeholders, and what are their expectations?

## Actions Based on Answers
1. **Update Project Folder Structure**:
Below is the base folder structure:
```
.
├── .env.example      # [PHASE 0] Template for environment variables (DB credentials, API keys)
├── .gitignore        # [PHASE 0] Files to exclude from version control
├── README.md         # [PHASE 0] Project overview and setup instructions
├── requirements.txt  # [PHASE 0] Python dependencies
├── environment.yml   # [PHASE 0] Conda environment (optional)
├── .github/          # [PHASE 0] GitHub Actions & CI/CD
│   └── workflows/
│       ├── data_quality_checks.yml  # → Automated data validation
│       └── scheduled_extraction.yml # → Scheduled ETL jobs
├── docs/             # [PHASE 1] Context & Understanding
│   ├── index.md         # → 1: Central documentation hub (navigation)
│   ├── objectives/      # → 2: PROJECT GOALS: What to achieve
│   ├── data_dictionary/ # → 3: Understand data: schemas, fields, definitions
│   └── methodology/     # → 4: Understand approach: statistical methods, frameworks
|   └── problem_statements.md #→ Analytics opportunities and use cases
├── config/           # [PHASE 2] Project Configuration
│   └── *.yml, *.json       # → Parameters, settings, environment configs
├── sql/              # [PHASE 2] SQL Queries & Database Scripts
│   ├── views/         # → SQL views for common queries
│   ├── procedures/    # → Stored procedures
│   └── extractions/   # → Data extraction queries
├── data/             # [PHASE 3] Data Acquisition & Preparation
│   ├── 1_raw/         # → 1: Original immutable source data
│   ├── 2_external/    # → 2: External reference data (demographics, benchmarks)
│   ├── 3_interim/     # → 3: Intermediate transformation outputs
│   ├── 4_processed/   # → 4: Final cleaned datasets (analysis-ready)
│   └── schemas/       # → Data schemas, contracts, and lineage documentation
├── notebooks/        # [PHASE 4] Interactive Exploration & Analysis
│   ├── 1_exploratory/   # → 1: Initial EDA, data profiling, hypothesis generation
│   └── 2_analysis/      # → 2: Deep-dive analysis, final insights, documentation
│   └── 3_feature_engineering/ # → 3: Feature creation, variable transformations 
├── src/              # [PHASE 5] Production Code Development
│   ├── utils/           # → Foundation: Helper functions, common utilities
│   ├── data_processing/ # → Pipeline 1: ETL, cleaning, validation
│   ├── features/        # → Pipeline 2: Feature engineering, variable transformations
│   ├── analysis/        # → Pipeline 3: Statistical analysis, algorithms
│   ├── visualization/   # → Pipeline 4: Chart generation, plotting utilities
│   └── models/          # → Pipeline 5: Model training, hyperparameter tuning
├── tests/            # [PHASE 6] Quality Assurance
│   ├── unit/          # → Unit tests for individual functions
│   ├── integration/   # → Integration tests for pipelines
│   └── data/          # → Data validation tests
├── models/           # [PHASE 7] Model Development & Storage
│   └── *.pkl, *.h5, *.joblib # → Trained models, model artifacts, serialized objects
├── results/          # [PHASE 8] Analysis Outputs
│   ├── tables/        # → Output 1: Summary statistics, analytical tables (CSV/Excel)
│   ├── metrics/       # → Output 2: Performance KPIs, evaluation metrics (JSON/CSV)
│   └── exports/       # → Output 3: Stakeholder-ready data exports
├── reports/          # [PHASE 9] Stakeholder Communication
│   ├── figures/       # → Component 1: Static visualizations (PNG/PDF)
│   ├── dashboards/    # → Component 2: Interactive dashboards (HTML/Streamlit)
│   └── presentations/ # → Component 3: Executive summaries (PPTX/PDF)
├── logs/             # [PHASE 10] Execution Logs & Audit Trails
│   ├── etl/           # → ETL pipeline execution logs
│   ├── errors/        # → Error logs and stack traces
│   └── audit/         # → Audit trails for data access and changes
└── scripts/          # [PHASE 10] Automation & Deployment
    └── *.py, *.R, *.sh  # → End-to-end pipelines, deployment scripts, automation
```
   - update the project structure based on the answers
   - Update the README.md file, docs/index.md, and create necessary configuration files in the config/ directory to reflect the technical environment and project specifics.

2. **Identification of Machine Learning & Analytics Opportunities**:
  1. Review all documentation in [`docs/project_context/data_sources.md`](../docs/project_context/data_sources.md) for available data assets and approved technical stack in [`docs/project_context/tech_stack.md`](../docs/project_context/tech_stack.md).
  2. Identify potential strategic epics that leverage existing infrastructure that captures end-to-end data life cycle from ingestion to actionable insights meeting goals defined above, each formatted as: 
      (1) Epic title and business objective, 
      (2) Specific data requirements citing actual tables/fields
      (3) Technical approach using only approved tools
      (4) Measurable success criteria
      (5) Estimated complexity and dependencies. 
  3. Ensure each epic is independent, prioritized by impact and feasibility, and detailed enough for a data analyst to begin implementation planning without requiring additional clarification. 
  4. Create separate markdown files for each problem statements. Save the output in `docs/objectives/epics` folder. 


3.**Technical Stack Reference**
   - Preferred Technologies:** 
      - Consult [docs/project_context/tech_stack.md](../../docs/project_context/tech_stack.md) for approved platforms and tools

   -Technology Selection Criteria:**
      1. **Default**: Use technologies from the approved tech stack when they meet project requirements
      2. **Exception**: Propose alternatives only when the approved stack has clear limitations for specific use cases (e.g., specialized libraries, performance constraints, integration requirements)
      3. **Justification Required**: When suggesting alternatives, explicitly state why the approved stack is insufficient and how the alternative addresses the gap

   -Actions:
      - Update project dependencies, environment setup, and documentation based on selected technologies
      - Ensure compatibility with target deployment environment (HEALIX/GCC or MCDR/on-premise)
      - set up appropriate configuration files for the chosen technologies
      - document the chosen platform in README.md and docs/index.md
      - include language specific dependencies in requirements.txt or environment.yml

4. **Data Dictionary Creation**:
   - Compile a comprehensive data dictionary in `docs/data_dictionary/` that details all datasets, including:
     - Field definitions, data types, and value ranges
     - Data quality notes and known limitations
     - Lineage tracking (source system → transformations → final table)
     - Business owners or subject matter experts for each data domain
     - Refresh frequency and update schedules
     - Sample data and example values
   - Create a master index file that links to individual data dictionary files for each major data domain
   - Ensure the data dictionary is easily navigable and linked from the main documentation index (docs/index.md)

---

## Final Steps
1. **Update Project Structure**:
   - Reorganize folders following the numbered workflow sequence above
   - Update README.md with project overview, workflow guidance, and technical stack specifications
   - Update docs/index.md to reflect the new structure and technical environment
   - Create environment-specific configuration files based on identified tools and platforms

2. **Install Project Dependencies**:
   - Install all necessary packages and libraries as per the chosen technical stack
   - Document installation steps in README.md and requirements.txt/environment.yml