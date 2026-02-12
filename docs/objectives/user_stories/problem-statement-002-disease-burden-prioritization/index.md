# User Stories Index: PS-002 Disease Burden Assessment & Resource Prioritization

## Problem Statement Overview

**PS-002: Disease Burden Assessment & Resource Prioritization**

Conduct systematic disease burden analysis using 9 years of surveillance data across multiple metrics to enable evidence-based budget allocation and program prioritization decisions for all 45 infectious diseases.

**Target Outcome**: Clear consensus on top 10-15 priority diseases based on data, transparent prioritization methodology, and measurable shift in resource allocation toward evidence-identified high-burden diseases.

---

## User Stories by Data Analysis Lifecycle

### Stage 1-2: Data Extraction & Preparation

#### [User Story 1: Extract and Profile All Infectious Disease Data](01-extract-and-profile-all-disease-data.md)
- **Status**: ⬜ Not Started
- **Description**: Extract and comprehensively profile all 45 infectious diseases, establish complete burden inventory, assess data quality
- **Key Deliverables**: Disease inventory, data profiling report, disease categorization
- **Estimated Effort**: 1 week
- **Dependencies**: Kaggle API access, Databricks environment

### Stage 3: Exploratory & Feature Engineering

#### [User Story 2: Calculate Multi-Dimensional Burden Metrics](02-calculate-multi-dimensional-burden-metrics.md)
- **Status**: ⬜ Not Started
- **Description**: Calculate comprehensive burden metrics (volume, trends, outbreaks, volatility) for all 45 diseases
- **Key Deliverables**: Comprehensive burden metrics dataset, normalized metrics, burden profile report
- **Estimated Effort**: 2 weeks
- **Dependencies**: User Story 1 (clean disease dataset)

### Stage 4-5: Analysis & Methodology Development

#### [User Story 3: Develop Multi-Criteria Prioritization Framework](03-develop-multi-criteria-prioritization-framework.md)
- **Status**: ⬜ Not Started
- **Description**: Develop transparent, evidence-based framework for ranking diseases using weighted multi-criteria scoring
- **Key Deliverables**: Prioritization methodology, disease rankings, sensitivity analysis, stakeholder validation
- **Estimated Effort**: 2-3 weeks
- **Dependencies**: User Story 2 (burden metrics), stakeholder workshop

### Stage 7: Visualization & Communication

#### [User Story 4: Create Interactive Disease Burden Dashboard](04-create-interactive-disease-burden-dashboard.md)
- **Status**: ⬜ Not Started
- **Description**: Create interactive dashboard displaying disease burden rankings, trends, and multi-dimensional profiles
- **Key Deliverables**: Burden dashboard, disease profile cards, sensitivity analysis visualizations, export capabilities
- **Estimated Effort**: 2-3 weeks
- **Dependencies**: User Story 3 (prioritization framework and rankings)

---

## Overall Progress

**Total User Stories**: 4  
**Completed**: 0  
**In Progress**: 0  
**Not Started**: 4  
**Progress**: 0%

---

## Key Reusable Components

- **Disease data extraction pipeline**: Kaggle dataset loading and harmonization
- **Disease name standardization**: HFMD and other variant resolution
- **Burden metric calculations**: Volume, trend, outbreak, volatility metrics
- **Multi-criteria scoring framework**: Weighted composite scoring methodology
- **Disease categorization**: Transmission mode classification
- **Sensitivity analysis**: Ranking robustness under different weightings
- **Disease profile cards**: One-page disease summary templates
- **Burden dashboard template**: Interactive Plotly/Dash disease exploration dashboard

---

## Dependencies and Cross-References

### External Dependencies
- Kaggle dataset: `subhamjain/health-dataset-complete-singapore`
- Required data: `weekly-infectious-disease-bulletin-cases.csv`

### Internal Dependencies
- Sequential lifecycle stages (each story builds on previous)
- Stakeholder engagement required for User Story 3 (weighting validation)
- Domain knowledge references:
  - [Infectious Disease Bulletin Data Dictionary](../../data_dictionary/infectious_disease_bulletin.md)
  - [Infectious Disease Epidemiology Terminology](../../domain_knowledge/infectious-disease-epidemiology-terminology-glossary.md)
  - [Disease Burden Assessment Methodology](../../domain_knowledge/disease-burden-assessment-methodology.md)

### Related Problem Statements
- **PS-001**: Forecasting may use burden rankings to prioritize forecast development
- **PS-003**: Workforce planning informed by disease burden priorities

---

## Prioritization Criteria (Proposed)

Based on domain knowledge and stakeholder validation:

1. **Case Volume** (40% weight): Total/annual average cases
2. **Trend** (25% weight): CAGR, trend direction (emerging threats)
3. **Outbreak Risk** (20% weight): Outbreak frequency and intensity
4. **Volatility** (15% weight): Coefficient of variation (predictability)

**Alternative weighting scenarios** will be tested in sensitivity analysis (User Story 3).

---

## Expected Top Priority Diseases

Based on preliminary data exploration:
1. **HFMD (combined)**: ~235,000 cases (highest volume)
2. **Dengue Fever**: ~127,000 cases (frequent outbreaks, increasing trend)
3. **Salmonellosis**: ~16,000 cases (stable, sustained burden)
4. **Mumps**: ~4,000 cases (vaccine-preventable, periodic outbreaks)
5. **Campylobacter variants**: ~4,000 cases (foodborne threat)

---

## Notes

**Prioritization Philosophy**: Evidence-based, transparent, stakeholder-informed, flexible to evolving priorities.

**Stakeholder Value**: Enable objective prioritization of disease programs for budget allocation, focus resources on highest-impact diseases, early identification of emerging threats.

**Key Success Factors**:
- Comprehensive burden metrics beyond simple case counts (User Story 2)
- Stakeholder buy-in on prioritization criteria and weights (User Story 3)
- Transparent, reproducible methodology (all user stories)
- User-friendly dashboard for exploration and communication (User Story 4)

**Implementation Timeline**: ~6-9 weeks for full lifecycle (data extraction through dashboard deployment)

**Maintenance Plan**: Annual update with new surveillance data; weighting review every 2-3 years
