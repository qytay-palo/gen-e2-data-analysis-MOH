# EPIC-001: Healthcare Facility Utilization & Bottleneck Analysis

```yaml
epic_id: EPIC-001
title: Healthcare Facility Utilization & Bottleneck Analysis
category: Descriptive & Diagnostic
priority: CRITICAL
complexity: MEDIUM
estimated_duration: 2-3 weeks
dependencies: None
status: Ready
```

---

## Problem Statement (Executive Summary)

Currently, healthcare administrators and policy makers lack comprehensive visibility into facility utilization patterns and operational bottlenecks across Singapore's healthcare network. This prevents data-driven capacity planning, resource optimization, and identification of systemic inefficiencies. By analyzing patient distribution patterns, service utilization rates, and process bottlenecks, we can enable evidence-based resource allocation and operational improvements, resulting in improved patient access, reduced wait times, and optimized healthcare delivery.

---

## Objectives

1. **Profile Facility Utilization**: Analyze patient visit patterns, capacity utilization rates, and service delivery metrics across all healthcare facilities (hospitals, polyclinics, specialty centers)

2. **Identify Operational Bottlenecks**: Detect and quantify minimum 10 critical bottlenecks in patient flow, service delivery, and resource utilization

3. **Benchmark Performance**: Compare facility performance across key metrics (throughput, wait times, efficiency) to identify high and low performers

4. **Quantify Impact**: Measure the business impact of each bottleneck (patient volume affected, wait time increase, throughput reduction, cost implications)

5. **Prioritize Interventions**: Rank bottlenecks and improvement opportunities by severity score combining volume, impact, and feasibility of resolution

---

## Success Criteria

✅ **Comprehensive Coverage**: Profile 100% of healthcare facilities in dataset (hospitals, polyclinics, clinics)

✅ **Bottleneck Identification**: Identify minimum 10 critical operational bottlenecks with documented root causes

✅ **Impact Quantification**: Quantify impact metrics for each bottleneck:
- Patient volume affected per day/week
- Average wait time increase (minutes)
- Throughput reduction (patients per hour)
- Estimated cost impact

✅ **Severity Scoring**: Develop and apply bottleneck severity framework (1-5 scale) considering:
- Volume of patients affected
- Magnitude of impact
- Frequency of occurrence
- Implementation feasibility

✅ **Top 5 Root Cause Analysis**: Complete detailed root cause analysis for top 5 most severe bottlenecks using fishbone diagrams and data-driven evidence

✅ **Actionable Recommendations**: Deliver minimum 5 high-priority improvement recommendations with implementation roadmaps

✅ **Executive Dashboard**: Create interactive dashboard showing facility performance, bottlenecks, and improvement opportunities

---

## Stakeholders and Value Proposition

### Primary Stakeholders

**Business Decision Makers**:
- Healthcare administrators (facility-level and system-level)
- Hospital executives and operational managers
- Capacity planning teams
- Operations improvement teams

**Policy Makers**:
- Ministry of Health resource allocation planners
- Healthcare system strategic planning teams

### Business Value

**Decision Enabled**:
- Resource reallocation across facilities
- Capacity expansion or redistribution decisions
- Operational process improvements
- Staffing optimization

**Efficiency Gains**:
- Reduce patient wait times by identifying and addressing bottlenecks
- Improve facility throughput and capacity utilization
- Optimize resource allocation (staff, equipment, space)
- Reduce operational costs through efficiency improvements

**Quality Improvement**:
- Enhanced patient experience through reduced wait times
- Better access to care through optimized capacity
- Improved care delivery through streamlined processes

**Risk Reduction**:
- Mitigate overcrowding and safety risks
- Prevent access barriers from capacity constraints
- Reduce patient dissatisfaction and complaints

---

## Data Requirements

### Required Datasets

**Primary Tables** (from [data_sources.md](../../project_context/data_sources.md)):

1. **Healthcare Utilization Tables**:
   - `admission-and-outpatient-attendances-by-restructured-hospitals` - Hospital attendance patterns (2006-2020)
   - `admission-and-outpatient-attendances` - General attendance data (2006-2020)
   - Required fields: year, type_of_attendance, attendances_no

2. **Healthcare Facilities Tables**:
   - `number-of-hospital-beds` - Bed capacity by hospital (2009-2020)
   - `facilities-in-the-registry-of-medical-clinics-and-dental-clinics` - Clinic facility information (2020)
   - Required fields: year, hospital, beds_no (for capacity analysis)

3. **Healthcare Workforce Tables** (for capacity context):
   - `number-of-doctors` - Doctor availability (2006-2019)
   - `number-of-nurses` - Nurse availability (2006-2019)
   - Required fields: year, doctors_no, nurses_no

### Data Granularity
- **Temporal**: Annual data (2006-2020)
- **Geographic**: Facility-level and aggregated system-level
- **Service**: By attendance type (inpatient, outpatient, emergency)

### Time Period
- **Historical Analysis**: 2006-2020 (15 years)
- **Trend Analysis**: 2015-2020 (recent 5 years)
- **Baseline Period**: 2015-2017 (pre-recent-trends)

### Data Quality Requirements
- **Completeness**: 100% for facility identifiers and attendance counts
- **Consistency**: Year-over-year data must be comparable
- **Timeliness**: Dataset coverage through 2020 is acceptable for historical analysis

### External Data (Optional)
- Singapore population growth data for demand context
- Facility operating hours and service types
- Regional demographic data for demand modeling

---

## Technical Approach

### Analytical Methods

**Descriptive Statistics**:
- Facility utilization rate calculation: (Actual Visits / Capacity) × 100%
- Visit volume profiling by facility, time period, service type
- Distribution analysis of wait times and service times

**Benchmarking Analysis**:
- Comparative performance analysis across facilities
- Percentile ranking (top 10%, bottom 10% performers)
- Identification of statistical outliers (high/low performers)

**Bottleneck Detection**:
- Capacity utilization threshold analysis (>90% = overcrowded, <50% = underutilized)
- Time-series analysis to detect persistent bottlenecks
- Queuing theory metrics (arrival rate, service rate, wait time)

**Root Cause Analysis**:
- Correlation analysis between utilization and outcomes
- Fishbone diagram construction for top bottlenecks
- Comparative analysis (high performers vs. low performers)

**Severity Scoring**:
- Multi-criteria scoring framework:
  - Volume Impact Score (1-5): Number of patients affected
  - Time Impact Score (1-5): Magnitude of wait time increase
  - Frequency Score (1-5): How often bottleneck occurs
  - Overall Severity = (Volume + Time + Frequency) / 3

### Tools and Platforms

**Primary Platform**: Python on HEALIX/Databricks

**Key Libraries**:
- Data processing: `pandas`, `numpy`
- Statistical analysis: `scipy.stats`, `statsmodels`
- Visualization: `matplotlib`, `seaborn`, `plotly`
- Dashboard: `plotly.dash` or Databricks notebooks

**Alternative**: R for statistical analysis if preferred

### Implementation Steps

**Phase 1: Data Preparation** (Week 1, Days 1-2)
1. Extract facility utilization and capacity data from Kaggle dataset
2. Clean and validate data (missing values, outliers, consistency checks)
3. Create unified facility utilization dataset
4. Calculate capacity metrics (utilization rates, throughput)

**Phase 2: Facility Profiling** (Week 1, Days 3-5)
5. Profile each facility's utilization patterns
6. Calculate summary statistics (mean, median, percentiles)
7. Create facility performance scorecards
8. Identify high and low performers

**Phase 3: Bottleneck Identification** (Week 2, Days 1-3)
9. Apply bottleneck detection algorithms
10. Calculate severity scores for each bottleneck
11. Rank bottlenecks by priority
12. Select top 10 critical bottlenecks

**Phase 4: Root Cause Analysis** (Week 2, Days 4-5)
13. Conduct detailed analysis for top 5 bottlenecks
14. Create fishbone diagrams
15. Identify contributing factors
16. Develop evidence-based hypotheses

**Phase 5: Recommendations & Reporting** (Week 3)
17. Develop improvement recommendations
18. Create implementation roadmaps
19. Build interactive dashboard
20. Prepare executive report and presentation

---

## Deliverables

### Analytical Outputs

- [x] **Facility Utilization Profiles** (`results/tables/facility_utilization_profiles.csv`)
  - Comprehensive utilization metrics for all facilities
  - Time-series trends (2006-2020)
  - Performance benchmarks and rankings

- [x] **Bottleneck Analysis Report** (`results/tables/bottleneck_analysis.csv`)
  - List of 10+ identified bottlenecks
  - Severity scores and rankings
  - Impact quantification (patients, time, cost)
  - Root causes for top 5 bottlenecks

- [x] **Performance Benchmarking** (`results/tables/facility_benchmarking.csv`)
  - Comparative performance metrics
  - Best practice identification
  - Gap analysis (actual vs. target performance)

### Documentation

- [x] **Technical Report** (`reports/epic-001-technical-report.pdf`)
  - Methodology and analytical approach
  - Detailed findings and statistical analysis
  - Appendices with supplementary data

- [x] **Executive Summary** (`reports/epic-001-executive-summary.pdf`)
  - 2-page summary for stakeholders
  - Key findings and recommendations
  - Visual highlights (charts, infographics)

### Code and Artifacts

- [x] **Jupyter Notebooks** (`notebooks/2_analysis/epic-001-facility-utilization/`)
  - `01_data_preparation.ipynb`
  - `02_facility_profiling.ipynb`
  - `03_bottleneck_analysis.ipynb`
  - `04_root_cause_analysis.ipynb`

- [x] **Production Code** (`src/analysis/facility_utilization/`)
  - `facility_profiler.py` - Facility utilization calculation
  - `bottleneck_detector.py` - Bottleneck identification algorithms
  - `severity_scorer.py` - Severity scoring framework

### Stakeholder Materials

- [x] **Interactive Dashboard** (`reports/dashboards/facility-utilization-dashboard.html`)
  - Facility performance overview
  - Bottleneck visualization and drill-down
  - Trend analysis and forecasting
  - Filterable by facility, time period, service type

- [x] **Presentation Slides** (`reports/presentations/epic-001-facility-utilization.pptx`)
  - Executive presentation (15-20 slides)
  - Key findings and insights
  - Recommendations and next steps

- [x] **Improvement Recommendations** (`results/exports/improvement_recommendations.xlsx`)
  - Prioritized list of 5+ recommendations
  - Implementation roadmaps
  - Expected impact and ROI estimates

---

## Dependencies and Prerequisites

### Technical Prerequisites
- ✅ Database access: Kaggle MOH dataset loaded and accessible
- ✅ Compute resources: Standard Databricks cluster (no special requirements)
- ✅ Software installations: Python environment with pandas, numpy, scipy, plotly

### Data Prerequisites
- ✅ Data extraction: Kaggle dataset downloaded and validated
- ✅ Data quality: No major quality issues in facility and utilization tables
- ✅ Reference data: None required (self-contained analysis)

### Epic Dependencies
- **Depends on**: None (foundation epic, no dependencies)
- **Blocks**: EPIC-004 (Process Optimization builds on this analysis)
- **Can run in parallel with**: EPIC-002, EPIC-003, EPIC-005, EPIC-006

---

## Risk Assessment and Mitigation

### Technical Risks

**Risk 1: Limited Data Granularity**
- **Description**: Annual aggregated data may not reveal intra-year bottlenecks
- **Likelihood**: High
- **Impact**: Medium
- **Mitigation**: 
  - Acknowledge limitation in findings
  - Use proxies and comparative analysis
  - Recommend future data collection at finer granularity
  - Focus on persistent, systemic bottlenecks visible in annual data

**Risk 2: Incomplete Facility Coverage**
- **Description**: Dataset may not include all healthcare facilities
- **Likelihood**: Medium
- **Impact**: Medium
- **Mitigation**:
  - Document facility coverage in dataset
  - Focus on major facilities with complete data
  - Acknowledge coverage limitations in reporting

### Data Risks

**Risk 3: Data Recency (2020 cutoff)**
- **Description**: Dataset ends in 2020; may not reflect 2021-2026 changes
- **Likelihood**: High
- **Impact**: Low (historical analysis still valuable)
- **Mitigation**:
  - Clearly state analysis timeframe
  - Focus on structural, persistent bottlenecks
  - Recommend validation with recent data when available

### Timeline Risks

**Risk 4: Scope Creep**
- **Description**: Stakeholders may request additional analyses beyond scope
- **Likelihood**: Medium
- **Impact**: Medium
- **Mitigation**:
  - Clear scope definition and stakeholder alignment
  - Log additional requests for future epics
  - Focus on delivering core deliverables on time

---

## Implementation Plan

### Phase 1: Data Preparation (Week 1, Days 1-2)

**Tasks**:
- Extract facility utilization tables from Kaggle dataset
- Load data into analysis environment (pandas/Spark)
- Perform data quality checks (completeness, consistency, outliers)
- Create derived metrics (utilization rates, capacity calculations)
- Document data issues and assumptions

**Milestone**: Clean, validated dataset ready for analysis

---

### Phase 2: Facility Profiling (Week 1, Days 3-5)

**Tasks**:
- Calculate utilization rates for each facility and time period
- Generate descriptive statistics (mean, median, min, max, percentiles)
- Create time-series visualizations of utilization trends
- Build facility performance scorecards
- Identify top and bottom performers

**Milestone**: Facility utilization profiles complete

---

### Phase 3: Bottleneck Identification (Week 2, Days 1-3)

**Tasks**:
- Define bottleneck detection criteria (utilization thresholds, trend analysis)
- Apply bottleneck detection algorithms
- Calculate severity scores for each identified bottleneck
- Rank bottlenecks by priority
- Select top 10 critical bottlenecks for deep analysis

**Milestone**: Prioritized list of 10+ bottlenecks with severity scores

---

### Phase 4: Root Cause Analysis (Week 2, Days 4-5)

**Tasks**:
- Conduct detailed analysis for top 5 bottlenecks
- Create fishbone diagrams and causal maps
- Analyze contributing factors (capacity, demand, staffing, processes)
- Validate hypotheses with data analysis
- Document root causes with supporting evidence

**Milestone**: Root cause analysis complete for top 5 bottlenecks

---

### Phase 5: Recommendations & Reporting (Week 3)

**Tasks**:
- Develop 5+ improvement recommendations
- Create implementation roadmaps with effort estimates
- Build interactive dashboard with Plotly/Dash
- Write technical report and executive summary
- Prepare presentation slides
- Stakeholder review and feedback incorporation

**Milestone**: All deliverables complete and validated by stakeholders

---

### Final Milestone

**Epic Completion Criteria**:
- ✅ All 10+ bottlenecks identified and documented
- ✅ Top 5 bottlenecks have complete root cause analysis
- ✅ 5+ improvement recommendations delivered with roadmaps
- ✅ Interactive dashboard deployed and accessible
- ✅ Technical report and executive summary approved by stakeholders
- ✅ Presentation delivered to business decision makers and policy makers

---

## Priority Score Calculation

**Impact**: 5/5 (Foundation for operational improvements, directly addresses Success Metric #1)  
**Feasibility**: 5/5 (Data available, standard analytical methods, low technical complexity)  
**Urgency**: 5/5 (Immediate need, foundation for other epics, quick wins possible)

**Priority Score**: 5 × 5 × 5 = **125** → **CRITICAL**

---

## Dependencies Graph

```
EPIC-001 (Foundation)
    ↓
EPIC-004 (Process Optimization)
    ↓
Implementation
```

**Notes**:
- EPIC-001 is a **foundation epic** with no dependencies
- Start immediately to enable downstream epics
- Can run in parallel with all other epics
- Provides baseline metrics for process improvement initiatives

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-02 | Analytics Team | Initial epic definition |
