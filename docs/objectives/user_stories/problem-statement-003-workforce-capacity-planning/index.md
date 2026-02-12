# User Stories Index: PS-003 Healthcare Workforce Capacity Planning & Optimization

## Problem Statement Overview

**PS-003: Healthcare Workforce Capacity Planning & Optimization**

Analyze 13+ years of workforce data (2006-2019) for doctors, nurses, and pharmacists alongside disease surveillance trends to develop evidence-based workforce capacity recommendations that optimize staffing across healthcare sectors.

**Target Outcome**: Workforce projections used in multi-year hiring/training planning, measurable improvement in workforce-to-burden alignment, evidence-based recommendations informing policy on immigration, training, and retention.

---

## User Stories by Data Analysis Lifecycle

### Stage 1-2: Data Extraction & Preparation

#### [User Story 1: Extract and Profile Healthcare Workforce Data](01-extract-and-profile-workforce-data.md)
- **Status**: ⬜ Not Started
- **Description**: Extract and comprehensively profile workforce data for doctors, nurses, pharmacists across sectors (2006-2019)
- **Key Deliverables**: Workforce profiling report, sector distribution analysis, data quality assessment
- **Estimated Effort**: 1 week
- **Dependencies**: Kaggle API access, Databricks environment

### Stage 3: Trend Analysis

#### [User Story 2: Analyze Workforce Supply Trends and Sector Distribution](02-analyze-workforce-supply-trends-sector-distribution.md)
- **Status**: ⬜ Not Started
- **Description**: Analyze multi-year workforce trends, growth patterns, and public-private sector shifts
- **Key Deliverables**: Trend analysis report, workforce projections (3-5 years), sector migration analysis
- **Estimated Effort**: 2 weeks
- **Dependencies**: User Story 1 (clean workforce datasets)

### Stage 4: Correlation Analysis

#### [User Story 3: Correlate Workforce Capacity with Disease Burden](03-correlate-workforce-with-disease-burden.md)
- **Status**: ⬜ Not Started
- **Description**: Analyze relationship between healthcare workforce levels and infectious disease burden over time
- **Key Deliverables**: Workforce-to-burden ratio analysis, capacity gap assessment, correlation report
- **Estimated Effort**: 2 weeks
- **Dependencies**: User Story 2 (workforce trends), disease surveillance data (from PS-001/PS-002)

### Stage 5: Prescriptive Recommendations

#### [User Story 4: Develop Workforce Capacity Recommendations and Optimization Strategy](04-develop-workforce-capacity-recommendations.md)
- **Status**: ⬜ Not Started
- **Description**: Develop evidence-based recommendations for workforce recruitment, training, and retention strategies
- **Key Deliverables**: Workforce gap analysis, recruitment/training/retention recommendations, optimization framework, implementation roadmap
- **Estimated Effort**: 2-3 weeks
- **Dependencies**: User Stories 2-3 (trends and capacity analysis)

### Stage 7: Visualization & Communication

#### [User Story 5: Create Workforce Capacity Planning Dashboard](05-create-workforce-capacity-dashboard.md)
- **Status**: ⬜ Not Started
- **Description**: Create interactive dashboard displaying workforce trends, sector distribution, capacity gaps, and recommendations
- **Key Deliverables**: Workforce dashboard, gap tracking, alert system, export capabilities
- **Estimated Effort**: 2-3 weeks
- **Dependencies**: User Story 4 (recommendations and optimization strategy)

---

## Overall Progress

**Total User Stories**: 5  
**Completed**: 0  
**In Progress**: 0  
**Not Started**: 5  
**Progress**: 0%

---

## Key Reusable Components

- **Workforce data extraction pipeline**: Multi-file Kaggle dataset loading
- **Workforce growth calculations**: CAGR, year-over-year growth rates
- **Sector distribution analysis**: Public-private-NFP breakdown over time
- **Workforce-to-population ratios**: Benchmarking against WHO/OECD standards
- **Workforce-to-disease-burden ratios**: Capacity adequacy metrics
- **Gap analysis framework**: Current and projected workforce shortfalls
- **Scenario planning templates**: Base/optimistic/pessimistic projections
- **Workforce dashboard template**: Interactive workforce monitoring dashboard

---

## Dependencies and Cross-References

### External Dependencies
- Kaggle dataset: `subhamjain/health-dataset-complete-singapore`
- Required data:
  - `number-of-doctors.csv` (2006-2019)
  - `number-of-nurses-and-midwives.csv` (2008-2019)
  - `number-of-pharmacists.csv` (2006-2019)
- Disease surveillance data for correlation analysis (User Story 3)

### Internal Dependencies
- Sequential lifecycle stages (each story builds on previous)
- Integration with disease burden data from PS-002 (User Story 3)
- Domain knowledge references:
  - [Healthcare Workforce Metrics and KPIs](../../domain_knowledge/healthcare-workforce-metrics-kpis.md)
  - [Disease Burden Assessment Methodology](../../domain_knowledge/disease-burden-assessment-methodology.md)
  - [Data Sources](../../project_context/data-sources.md)

### Related Problem Statements
- **PS-001**: Forecast outputs can inform workforce demand projections
- **PS-002**: Disease burden priorities guide workforce allocation

---

## Key Workforce Metrics

### Workforce Supply
- **Total workforce**: Doctors, nurses, pharmacists by year
- **Growth rates**: CAGR, year-over-year changes
- **Sector distribution**: % public, private, not-for-profit

### Capacity Adequacy
- **Workforce-to-population ratios**: Per 1,000 or 10,000 population
- **Workforce-to-disease-burden ratios**: Workers per 1,000 disease cases
- **Workforce-to-bed ratios**: Staffing intensity per hospital bed (if bed data available)

### Sector Balance
- **Public-to-private ratio**: Balance of workforce across sectors
- **Sector migration trends**: Movement from public to private over time

### Gaps and Projections
- **Current gaps**: Shortfall relative to targets or benchmarks
- **Projected gaps**: 3-year and 5-year workforce shortfalls
- **Gap severity**: Critical (>20%), Moderate (10-20%), Minor (<10%)

---

## Expected Workforce Findings

Based on problem statement context:
- **Public-to-private migration**: Workforce shifting from public to private sector (higher pay, better work-life balance)
- **Growth trends**: Positive growth expected but may not keep pace with disease burden or population aging
- **Nursing shortages**: Likely highest gap due to high demand and turnover
- **Specialty needs**: Infectious disease specialists, public health workforce

---

## Workforce Development Strategies

### Recruitment
- Target numbers by profession and sector
- Foreign healthcare worker needs
- Public sector incentives

### Training Pipeline
- Medical/nursing school expansion needs
- Specialty training priorities
- Timeline to impact (3-6 years)

### Retention
- Public sector retention to reduce private migration
- Salary competitiveness, career development
- Cost-effectiveness vs. recruitment

---

## Notes

**Analysis Period**: 2006-2019 (13-14 years depending on profession)  
**Data Limitation**: COVID-19 workforce impacts (2020+) not captured

**Stakeholder Value**: Enable evidence-based workforce recruitment, training, and retention strategies; optimize workforce distribution across sectors; proactive identification of gaps before critical shortages.

**Key Success Factors**:
- Comprehensive trend analysis identifying sector imbalances (User Story 2)
- Integration with disease burden for capacity adequacy assessment (User Story 3)
- Actionable recommendations aligned with MOH priorities (User Story 4)
- User-friendly dashboard for monitoring and tracking (User Story 5)

**Implementation Timeline**: ~8-12 weeks for full lifecycle (data extraction through dashboard deployment)

**Maintenance Plan**: Annual update with new workforce registry data; quarterly progress tracking on recommendations
