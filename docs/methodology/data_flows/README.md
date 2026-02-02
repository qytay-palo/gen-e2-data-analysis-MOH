# Data Flow Strategy Documentation

**Purpose**: Index and navigation guide for all data flow specifications across epics and user stories.

**Last Updated**: 2 February 2026

---

## Overview

This directory contains comprehensive data flow strategies for the MOH Healthcare Data Analysis project. Each epic has a detailed data flow document that traces the complete end-to-end pipeline from raw data extraction to final deliverables.

**Project Scope**: 6 epics, 40+ user stories, covering descriptive, diagnostic, predictive, and prescriptive analytics for Singapore's healthcare system.

---

## Document Index

### Core Data Flow Documents

| Document | Purpose | Epic Coverage | Status |
|----------|---------|---------------|--------|
| [epic-001-facility-utilization-bottleneck-analysis-flow.md](epic-001-facility-utilization-bottleneck-analysis-flow.md) | Complete data flow for facility utilization analysis (8 user stories) | EPIC-001 | ✅ Complete |
| [epic-002-disease-outbreak-surveillance-system-flow.md](epic-002-disease-outbreak-surveillance-system-flow.md) | Complete data flow for disease surveillance (7 user stories) | EPIC-002 | ✅ Complete |
| [epic-003-healthcare-system-gap-analysis-flow.md](epic-003-healthcare-system-gap-analysis-flow.md) | Complete data flow for system gap analysis (9 user stories) | EPIC-003 | ✅ Complete |
| [epic-004-process-optimization-improvement-flow.md](epic-004-process-optimization-improvement-flow.md) | Complete data flow for process improvements (8 user stories) | EPIC-004 | ✅ Complete |
| [epic-005-geographic-access-equity-flow.md](epic-005-geographic-access-equity-flow.md) | Complete data flow for access equity analysis (7 user stories) | EPIC-005 | ✅ Complete |
| [epic-006-predictive-demand-forecasting-flow.md](epic-006-predictive-demand-forecasting-flow.md) | Complete data flow for predictive models (8 user stories) | EPIC-006 | ✅ Complete |

### Cross-Cutting Documents

| Document | Purpose | Status |
|----------|---------|--------|
| [shared_components.md](shared_components.md) | Reusable components across all epics (extraction, transformation, visualization) | ✅ Complete |
| [execution_plan.md](execution_plan.md) | Project timeline, dependencies, resource allocation | ✅ Complete |

---

## Quick Navigation by Epic

### EPIC-001: Healthcare Facility Utilization & Bottleneck Analysis

**Business Objective**: Analyze facility utilization patterns and identify operational bottlenecks to enable evidence-based resource allocation.

**User Stories Covered**:
1. e01-s01: Extract and Validate Facility Data
2. e01-s02: Calculate Utilization Rates
3. e01-s03: Profile Facility Performance
4. e01-s04: Detect and Quantify Bottlenecks
5. e01-s05: Develop Severity Scoring
6. e01-s06: Root Cause Analysis
7. e01-s07: Improvement Recommendations
8. e01-s08: Interactive Dashboard

**Key Deliverables**: Facility utilization dashboard, bottleneck inventory (10+), improvement recommendations

**Priority**: CRITICAL | **Duration**: 2-3 weeks

📄 **[View Full Data Flow →](epic-001-facility-utilization-bottleneck-analysis-flow.md)**

---

### EPIC-002: Disease Outbreak Detection & Surveillance System

**Business Objective**: Implement automated disease surveillance to detect outbreaks 7-14 days earlier than traditional methods.

**User Stories Covered**:
1. e02-s01: Extract and Prepare Disease Data
2. e02-s02: Establish Disease Baselines
3. e02-s03: Anomaly Detection Algorithms
4. e02-s04: Spatial Clustering Analysis
5. e02-s05: Epidemic Forecasting Models
6. e02-s06: Risk Scoring System
7. e02-s07: Surveillance Dashboard

**Key Deliverables**: Real-time surveillance dashboard, outbreak alert system, forecasting models (≤15% MAPE)

**Priority**: CRITICAL | **Duration**: 4-5 weeks

📄 **[View Full Data Flow →](epic-002-disease-outbreak-surveillance-system-flow.md)**

---

### EPIC-003: Healthcare System Gap Analysis & Policy Recommendations

**Business Objective**: Identify minimum 8 healthcare system gaps requiring policy intervention with quantified impact.

**User Stories**: 9 stories (e03-s01 through e03-s09)

**Key Deliverables**: Gap analysis report, policy recommendations, cost-benefit analysis

**Priority**: CRITICAL | **Duration**: 3-4 weeks

📄 **[View Full Data Flow](epic-003-healthcare-system-gap-analysis-flow.md)** ✅

---

### EPIC-004: Process Optimization & Improvement Opportunities

**Business Objective**: Document minimum 15 validated improvement opportunities with quantified business value.

**User Stories**: 8 stories (e04-s01 through e04-s08)

**Key Deliverables**: Patient journey maps, wait time analysis, improvement briefs (15+), best practice playbooks

**Priority**: HIGH | **Duration**: 3-4 weeks | **Depends On**: EPIC-001 (recommended)

📄 **[View Full Data Flow](epic-004-process-optimization-improvement-flow.md)** ✅

---

### EPIC-005: Geographic Access & Health Equity Analysis

**Business Objective**: Identify minimum 3 underserved areas and quantify health equity disparities.

**User Stories**: 7 stories (e05-s01 through e05-s07)

**Key Deliverables**: Geographic access maps, healthcare desert identification, equity scorecard

**Priority**: HIGH | **Duration**: 3-4 weeks

📄 **[View Full Data Flow](epic-005-geographic-access-equity-flow.md)** ✅

---

### EPIC-006: Predictive Demand Forecasting for Capacity Planning

**Business Objective**: Predict patient visits 1-year and 5-years ahead with ≤15% MAPE to enable proactive capacity planning.

**User Stories**: 8 stories (e06-s01 through e06-s08)

**Key Deliverables**: Demand forecasting models, capacity gap analysis, business cases for expansions

**Priority**: MEDIUM | **Duration**: 4-5 weeks | **Depends On**: EPIC-001 (required)

📄 **[View Full Data Flow](epic-006-predictive-demand-forecasting-flow.md)** ✅

---

## Data Flow Structure

Each epic data flow document follows this standard structure:

### 1. Epic Overview
- Epic ID and business objective
- Success criteria
- List of user stories included

### 2. End-to-End Pipeline Visualization
- Mermaid diagram showing data flow
- Execution sequence table

### 3. User Story Details (for each story)
- **Story Context**: ID, dependencies, complexity
- **Data Extraction Specification**: Source tables, fields, filters, validation
- **Data Transformation Pipeline**: Step-by-step transformations with Mermaid diagrams
- **Analysis Specification**: Methods, visualizations, statistical tests
- **Output Specification**: Deliverables, consumers, formats
- **Implementation Metadata**: Tech stack, code files to generate, effort estimates

### 4. Epic Integration & Artifacts
- Shared components used
- Epic-level outputs
- Quality gates

---

## How to Use This Documentation

### For Code Generation

Each user story section contains:
- **Exact table names and field names** from data dictionary
- **SQL-like filter conditions** ready to implement
- **Python code hints** with specific libraries and functions
- **YAML specifications** parseable by code generators
- **File paths** following project structure

### For Understanding Dependencies

- **Execution Sequence Tables**: Show the order to build user stories
- **Dependencies Graph (Mermaid)**: Visual representation of epic dependencies
- **Shared Components**: Identify reusable code across stories

### For Project Planning

- **Effort Estimates**: Days required per user story
- **Complexity Ratings**: LOW/MEDIUM/HIGH
- **Priority Levels**: CRITICAL/HIGH/MEDIUM
- **Execution Plan**: Comprehensive timeline with resource allocation

---

## Shared Components

All epics leverage shared components to reduce duplication:

### Data Extraction Components
- `kaggle_base_extraction`: Standard Kaggle API connection
- `facility_data_extraction`: Hospital and clinic data
- `disease_data_extraction`: Disease surveillance data
- `workforce_data_extraction`: Healthcare workforce data

### Transformation Components
- `column_standardization`: Consistent naming conventions
- `temporal_feature_engineering`: Time series features
- `facility_categorization`: Standardized facility types
- `disease_name_standardization`: Unified disease taxonomy
- `data_quality_validation`: Comprehensive validation framework

### Analysis Components
- `utilization_rate_calculation`: Facility efficiency metrics
- `percentile_ranking`: Performance benchmarking
- `time_series_baseline`: Statistical baselines
- `anomaly_detection`: Outbreak detection algorithms
- `forecasting_pipeline`: Predictive models (ARIMA, Prophet)

### Visualization Components
- `plotly_templates`: Standard chart styling
- `dashboard_components`: Reusable Dash components
- `report_generator`: PDF report generation

📄 **[View Full Shared Components Documentation →](shared_components.md)**

---

## Execution Strategy

### Recommended Phased Approach

**Phase 1 (Weeks 1-5)**: Foundation - Execute EPIC-001, EPIC-002, EPIC-003 in parallel
**Phase 2 (Weeks 6-10)**: Optimization - Execute EPIC-004, EPIC-005 in parallel
**Phase 3 (Weeks 11-16)**: Prediction - Execute EPIC-006
**Phase 4 (Weeks 17-22)**: Integration and finalization

**Total Duration**: 22 weeks (~5.5 months) with resource optimization

📄 **[View Full Execution Plan →](execution_plan.md)**

---

## Data Sources

All data flows extract from the **Kaggle Singapore Health Dataset**:

- **Dataset ID**: `subhamjain/health-dataset-complete-singapore`
- **Source**: Ministry of Health Singapore (via data.gov.sg)
- **Total Tables**: 35 CSV files
- **Time Coverage**: 1990-2020 (varies by table)
- **Data Quality**: 100% completeness (no missing values)

**Key Table Categories**:
- Healthcare Workforce (7 tables)
- Healthcare Facilities (4 tables)
- Health Outcomes & Mortality (3 tables)
- Public Health & Prevention (6 tables)
- Healthcare Utilization (3 tables)
- Healthcare Expenditure (1 table)

📄 **[View Data Sources Documentation →](../../project_context/data_sources.md)**

📄 **[View Data Dictionary →](../../data_dictionary/COMPREHENSIVE_DATA_CATALOG.md)**

---

## Technology Stack

### Core Technologies
- **Python 3.9+**: Primary language
- **Pandas**: Data manipulation
- **Kaggle Hub API**: Data extraction
- **Plotly/Dash**: Interactive dashboards
- **SciPy/Statsmodels**: Statistical analysis
- **scikit-learn/Prophet**: Machine learning and forecasting

### Platform Options (MOH Environment)
- **HEALIX (GCC Cloud)**: Databricks with R/Python
- **MCDR (On-Premise)**: Cloudera CDSW with Spark

📄 **[View Tech Stack Details →](../../project_context/tech_stack.md)**

---

## Quality Standards

All data flows must meet these quality gates:

### Data Quality
- ✅ >95% completeness for critical fields
- ✅ Schema validation passed
- ✅ Range validation passed
- ✅ No duplicate primary keys

### Code Quality
- ✅ Unit tests with >80% coverage
- ✅ Code review completed
- ✅ Documentation complete
- ✅ Follows PEP 8 style guide

### Deliverable Quality
- ✅ Acceptance criteria met
- ✅ Stakeholder demo approved
- ✅ User documentation complete
- ✅ Production deployment successful

---

## Getting Started

### For New Team Members

1. **Read Project Context**:
   - [Project Objectives](../../objectives/project_objectives.md)
   - [Data Sources](../../project_context/data_sources.md)
   - [Tech Stack](../../project_context/tech_stack.md)

2. **Review Epic Priority**:
   - Start with [Execution Plan](execution_plan.md)
   - Understand dependencies and sequencing

3. **Deep Dive into Epic**:
   - Select an epic based on assigned workstream
   - Read complete data flow document
   - Review user story acceptance criteria

4. **Setup Development Environment**:
   - Install Python and required libraries
   - Configure Kaggle API authentication
   - Clone project repository

5. **Begin Implementation**:
   - Follow user story sequence
   - Use code hints and specifications
   - Leverage shared components

### For Code Generation

Each user story section is structured to enable automated or AI-assisted code generation:

1. **Extract Specifications**: YAML blocks contain structured data ready for parsing
2. **Code Hints**: Python code snippets show the intended implementation approach
3. **File Paths**: Exact paths where code should be generated
4. **Dependencies**: Clear indication of required libraries and imports

---

## Validation Checklist

Before considering an epic complete, verify:

- [ ] All user stories have data flow specifications
- [ ] Every specification includes exact table names and fields
- [ ] All dependencies between user stories are documented
- [ ] Shared components are identified and referenced
- [ ] Epic integration flow shows end-to-end pipeline
- [ ] Quality gates are defined
- [ ] Effort estimates are realistic
- [ ] Code file paths follow project structure

---

## Maintenance and Updates

### When to Update This Documentation

- **New epic added**: Create new epic flow document
- **User story modified**: Update affected sections in epic flow
- **Shared component created**: Add to shared_components.md
- **Dependencies changed**: Update execution_plan.md
- **New data sources**: Update data extraction specifications

### Version Control

- All changes tracked in Git
- Document version numbers in metadata
- Change log maintained in each document

---

## Support and Contact

**Project Lead**: Lead Data Analyst  
**Documentation Owner**: Data Analysis Team  
**Last Review**: 2 February 2026  
**Next Review**: End of Phase 1 (Week 5)

---

## Document Status Legend

| Symbol | Status | Description |
|--------|--------|-------------|
| ✅ | Complete | Document fully written and reviewed |
| 🔄 | In Progress | Document actively being developed |
| 🔲 | Planned | Document planned but not yet started |
| ⚠️ | Needs Review | Document needs validation or updates |

---

## Quick Links

### Epic Data Flows
- [EPIC-001: Facility Utilization](epic-001-facility-utilization-bottleneck-analysis-flow.md) ✅
- [EPIC-002: Disease Surveillance](epic-002-disease-outbreak-surveillance-system-flow.md) ✅
- [EPIC-003: Gap Analysis](epic-003-healthcare-system-gap-analysis-flow.md) ✅
- [EPIC-004: Process Optimization](epic-004-process-optimization-improvement-flow.md) ✅
- [EPIC-005: Geographic Equity](epic-005-geographic-access-equity-flow.md) ✅
- [EPIC-006: Demand Forecasting](epic-006-predictive-demand-forecasting-flow.md) ✅

### Supporting Documents
- [Shared Components](shared_components.md) ✅
- [Execution Plan](execution_plan.md) ✅
- [Project Objectives](../../objectives/project_objectives.md)
- [Data Sources](../../project_context/data_sources.md)
- [Data Dictionary](../../data_dictionary/COMPREHENSIVE_DATA_CATALOG.md)
- [Tech Stack](../../project_context/tech_stack.md)

### User Stories by Epic
- [EPIC-001 User Stories](../../objectives/user_stories/epic-001-facility-utilization/)
- [EPIC-002 User Stories](../../objectives/user_stories/epic-002-disease-surveillance/)
- [EPIC-003 User Stories](../../objectives/user_stories/epic-003-gap-analysis/)
- [EPIC-004 User Stories](../../objectives/user_stories/epic-004-process-optimization/)
- [EPIC-005 User Stories](../../objectives/user_stories/epic-005-geographic-equity/)
- [EPIC-006 User Stories](../../objectives/user_stories/epic-006-demand-forecasting/)

---

**🎯 Ready to build implementation-ready code from these specifications!**
