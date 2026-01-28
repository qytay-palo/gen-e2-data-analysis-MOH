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
   - What are the main goals and deliverables of this project?

2. **Data Sources**: 
   - What datasets will be used, and where are they located?
   - How will we connect to the datasets (APIs, databases, files)?

3. **Stakeholders**: 
   - Who are the key stakeholders, and what are their expectations?

4. **Tools & Technologies**: 
   - What tools, libraries, or platforms will be utilized for analysis?

## Actions Based on Answers
1. **Update Project Folder Structure**:
Below is the base folder structure:
```
.
├── README.md
├── requirements.txt  # [PHASE 0] Python dependencies
├── environment.yml   # [PHASE 0] Conda environment (optional)
├── docs/             # [PHASE 1] Context & Understanding
│   ├── index.md         # → 1: Central documentation hub (navigation)
│   ├── objectives/      # → 2: PROJECT GOALS: What to achieve
│   ├── data_dictionary/ # → 3: Understand data: schemas, fields, definitions
│   └── methodology/     # → 4: Understand approach: statistical methods, frameworks
├── config/           # [PHASE 2] Project Configuration
│   └── *.yml, *.json       # → Parameters, settings, environment configs
├── data/             # [PHASE 3] Data Acquisition & Preparation
│   ├── raw/           # → 1: Original immutable source data
│   ├── external/      # → 2: External reference data (demographics, benchmarks)
│   ├── interim/       # → 3: Intermediate transformation outputs
│   └── processed/     # → 4: Final cleaned datasets (analysis-ready)
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
│   ├── tables/        # → Output 1: Summary statistics, analytical tables (CSV/Excel)
│   ├── metrics/       # → Output 2: Performance KPIs, evaluation metrics (JSON/CSV)
│   └── exports/       # → Output 3: Stakeholder-ready data exports
├── reports/          # [PHASE 9] Stakeholder Communication
│   ├── figures/       # → Component 1: Static visualizations (PNG/PDF)
│   ├── dashboards/    # → Component 2: Interactive dashboards (HTML/Streamlit)
│   └── presentations/ # → Component 3: Executive summaries (PPTX/PDF)
└── scripts/          # [PHASE 10] Automation & Deployment
    └── *.py, *.R, *.sh  # → End-to-end pipelines, deployment scripts, automation
```
   - update the project structure based on the answers
   - Update the README.md file, docs/index.md, and create necessary configuration files in the config/ directory to reflect the technical environment and project specifics.

2. **Identification of Machine Learning & Analytics Opportunities**:
   - identify relevant machine learning and analytics opportunities. Specify the problem framing, target variable, potential features, recommended modeling or analytical methods, data requirements, and evaluation metrics. Prioritize opportunities by expected impact and technical feasibility.
   - Document these opportunities in `docs/objectives/opportunities.md`.

3.**Technical Stack Reference**
   - Preferred Technologies:** 
      - Consult [docs/project_context/tech_stack.md](../../docs/project_context/tech_stack.md) for approved platforms and tools

   -Technology Selection Criteria:**
      1. **Default**: Use technologies from the approved tech stack when they meet project requirements
      2. **Exception**: Propose alternatives only when the approved stack has clear limitations for specific use cases (e.g., specialized libraries, performance constraints, integration requirements)
      3. **Justification Required**: When suggesting alternatives, explicitly state why the approved stack is insufficient and how the alternative addresses the gap

   -Implementation:
      - Update project dependencies, environment setup, and documentation based on selected technologies
      - Ensure compatibility with target deployment environment (HEALIX/GCC or MCDR/on-premise)
      - set up appropriate configuration files for the chosen technologies
      - document the chosen platform in README.md and docs/index.md
      - include language specific dependencies in requirements.txt or environment.yml

4. **Data Dictionary Creation**:
   - Compile a comprehensive data dictionary in `docs/data_dictionary/` that details all datasets, including field definitions, data types, value ranges, and any relevant notes on data quality or transformations needed.
   - Ensure the data dictionary is easily navigable and linked from the main documentation index.
   
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