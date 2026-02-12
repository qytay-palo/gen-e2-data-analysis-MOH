# Problem Statements & Analytics Opportunities

**Project**: MOH Healthcare Policy & Operations Insights  
**Last Updated**: 4 February 2026  
**Status**: Active Development

---

## Overview

This document outlines the key problem statements, analytics opportunities, and research questions that guide our analysis of Singapore's healthcare system data. Each problem statement is linked to specific business objectives and expected outcomes.

---

## 1. Disease Outbreak Detection & Early Warning

### Problem Statement

**Challenge**: Traditional disease surveillance systems rely on laboratory confirmations and manual reporting, leading to delays in outbreak detection. By the time an outbreak is officially confirmed, community transmission may already be widespread.

**Impact**:
- Delayed public health response
- Increased disease transmission
- Higher healthcare system burden
- Greater economic and social costs

**Opportunity**: Leverage healthcare utilization data (polyclinic visits, hospital admissions, emergency department visits) as early indicators of potential disease outbreaks.

### Research Questions

1. Can we detect unusual patterns in healthcare visits before laboratory-confirmed cases spike?
2. What syndromic indicators best predict different types of disease outbreaks?
3. How many days of advance warning can we achieve compared to traditional surveillance?
4. What geographic granularity is optimal for outbreak detection?
5. How do we balance sensitivity (early detection) with specificity (avoiding false alarms)?

### Data Requirements

- **Primary**: Polyclinic attendances, hospital admissions, emergency department visits
- **Temporal**: Daily or weekly aggregations with multi-year historical baseline
- **Geographic**: Clinic/hospital location, patient residence (if available)
- **Clinical**: Chief complaints, diagnosis codes (if available)

### Analytical Approaches

- **Time Series Analysis**: ARIMA, Prophet, seasonal decomposition
- **Anomaly Detection**: Statistical process control, machine learning outlier detection
- **Spatial Analysis**: Geographic clustering, hotspot identification
- **Syndromic Surveillance**: Pattern recognition for respiratory illness, gastroenteritis, etc.

### Success Criteria

- Detect outbreaks 3-7 days earlier than traditional methods
- Maintain false positive rate below 5%
- Provide actionable alerts to public health teams
- Enable targeted investigation and response

---

## 2. Clinic Visitation Distribution & Accessibility

### Problem Statement

**Challenge**: Healthcare demand is unevenly distributed across polyclinics, leading to:
- Long wait times at popular clinics
- Underutilization of some facilities
- Accessibility barriers for certain populations
- Inefficient resource allocation

**Impact**:
- Poor patient experience (long waits)
- Missed prevention opportunities (delayed care-seeking)
- Healthcare inequity across regions
- Suboptimal return on infrastructure investment

**Opportunity**: Analyze visitation patterns to optimize clinic capacity, inform new facility placement, and improve accessibility.

### Research Questions

1. Which polyclinics are consistently over/under capacity?
2. What factors drive clinic selection (proximity, reputation, specific services)?
3. Are there geographic areas underserved by primary care facilities?
4. How do visitation patterns vary by time (day of week, season, time of day)?
5. What is the relationship between population demographics and clinic utilization?
6. Can we predict future demand to inform capacity planning?

### Data Requirements

- **Primary**: Polyclinic attendances by location, number of polyclinics
- **Supporting**: Population distribution, demographic data, geographic boundaries
- **External**: Public transport accessibility, clinic operating hours
- **Temporal**: Multi-year trends to identify patterns

### Analytical Approaches

- **Spatial Analysis**: Catchment area mapping, accessibility modeling
- **Capacity Planning**: Utilization rates, queuing theory, demand forecasting
- **Comparative Analysis**: Performance benchmarking across clinics
- **Demographic Analysis**: Population needs assessment

### Success Criteria

- Identify top 5 overutilized and underutilized facilities
- Map accessibility gaps (areas >30 min travel time to nearest clinic)
- Provide evidence-based recommendations for capacity adjustments
- Inform site selection for future clinic expansion

---

## 3. Policy Intervention Prioritization

### Problem Statement

**Challenge**: Limited government resources and political capital must be allocated to maximize public health impact. Policy makers struggle to:
- Identify which health issues require urgent intervention
- Determine where policy changes will have greatest effect
- Quantify expected impact of different interventions
- Balance competing priorities across multiple health domains

**Impact**:
- Suboptimal policy outcomes
- Resources spread too thin across too many initiatives
- Reactive rather than proactive policymaking
- Difficulty building consensus among stakeholders

**Opportunity**: Develop data-driven framework for identifying and prioritizing policy intervention opportunities.

### Research Questions

1. What are the largest gaps between current state and desired health outcomes?
2. Which health issues have the highest population impact (mortality, morbidity, cost)?
3. Where are health inequities most pronounced?
4. What interventions have highest potential ROI (cost per QALY gained)?
5. Which issues are worsening and require urgent attention?
6. What are the root causes vs. symptoms of observed health challenges?

### Data Requirements

- **Primary**: Health outcomes (mortality, life expectancy), healthcare utilization, expenditure
- **Supporting**: International benchmarks, intervention cost-effectiveness studies
- **Demographic**: Age, gender, socioeconomic indicators
- **Temporal**: Trend analysis over 5-10 years

### Analytical Approaches

- **Gap Analysis**: Current vs. target performance comparison
- **Trend Analysis**: Identifying deteriorating vs. improving metrics
- **Equity Assessment**: Comparing outcomes across population subgroups
- **Impact Modeling**: Estimating potential impact of interventions
- **Root Cause Analysis**: Drilling down from symptoms to underlying causes

### Success Criteria

- Prioritized list of top 10 intervention opportunities
- Quantified impact potential for each opportunity
- Evidence-based rationale for prioritization
- Actionable recommendations with implementation considerations

---

## 4. Healthcare Process Improvement & Bottleneck Identification

### Problem Statement

**Challenge**: Patient flow through hospitals and polyclinics involves multiple touchpoints, each with potential for delays and inefficiencies:
- Registration and check-in
- Triage and assessment
- Consultation and examination
- Diagnostic tests and procedures
- Pharmacy and discharge

**Impact**:
- Long patient wait times
- Poor patient satisfaction
- Staff burnout from managing patient frustration
- Reduced throughput (fewer patients served)
- Increased operational costs

**Opportunity**: Identify process bottlenecks and implement targeted improvements to optimize patient flow and resource utilization.

### Research Questions

1. Where in the patient journey do the longest waits occur?
2. How does process efficiency vary across different facilities?
3. What distinguishes high-performing from low-performing facilities?
4. Are there specific times (hour, day, season) when bottlenecks are worst?
5. What is the relationship between staffing levels and wait times?
6. Can we predict daily demand to optimize staffing and resource allocation?

### Data Requirements

- **Primary**: Hospital admissions, polyclinic visits, length of stay, bed occupancy
- **Process**: Wait times, service times, throughput metrics (if available)
- **Resources**: Staffing levels, bed capacity, equipment availability
- **Temporal**: High-resolution time data (hourly) to identify peak periods

### Analytical Approaches

- **Process Mining**: Mapping patient flows and identifying bottlenecks
- **Queuing Theory**: Modeling wait times and service capacity
- **Benchmarking**: Comparing performance across facilities
- **Simulation Modeling**: Testing "what-if" scenarios for improvements
- **Time Series Analysis**: Predicting demand patterns

### Success Criteria

- Identify top 3 process bottlenecks with quantified impact
- Benchmark facilities and identify best practices
- Recommend specific, actionable process improvements
- Estimate expected benefits (reduced wait time, increased throughput)

---

## Cross-Cutting Themes

### Data-Driven Decision Making

All problem statements share a common goal: **Enable comprehensive, well-rounded policy decisions** by providing integrated insights that connect multiple data sources and health domains.

**Key Challenges Addressed**:
1. **Fragmentation**: Connecting healthcare workforce, facilities, utilization, and outcomes data
2. **Complexity**: Identifying systemic patterns across multiple variables
3. **Prioritization**: Quantifying relative importance of different issues
4. **Uncertainty**: Providing confidence intervals and risk assessments

### Stakeholder Value Proposition

**For Policy Makers**:
- Evidence-based recommendations grounded in data
- Prioritized action plans with expected impact
- Risk assessment for different policy options
- Monitoring dashboards to track progress

**For Healthcare Administrators**:
- Operational insights to improve efficiency
- Benchmarking to identify improvement opportunities
- Capacity planning support
- Resource allocation guidance

**For Public Health Leaders**:
- Early warning systems for health threats
- Health equity monitoring
- Program effectiveness evaluation
- Population health trend tracking

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- Data acquisition and validation
- Exploratory data analysis
- Data quality assessment
- Infrastructure setup

### Phase 2: Problem-Specific Analysis (Weeks 3-6)
- **Week 3**: Disease outbreak detection analysis
- **Week 4**: Clinic distribution and accessibility analysis
- **Week 5**: Policy intervention prioritization
- **Week 6**: Process improvement and bottleneck analysis

### Phase 3: Integration & Insights (Weeks 7-8)
- Cross-cutting insights across problem areas
- Integrated recommendations
- Dashboard development
- Stakeholder presentations

---

## Expected Deliverables

### Analytical Outputs
1. **Disease Outbreak Report**: Early warning indicators and alert thresholds
2. **Clinic Accessibility Map**: Geographic analysis of service coverage
3. **Policy Priority Matrix**: Ranked intervention opportunities
4. **Process Improvement Guide**: Bottleneck analysis and recommendations

### Decision Support Tools
1. **Outbreak Surveillance Dashboard**: Real-time monitoring
2. **Capacity Planning Tool**: Clinic utilization forecasting
3. **Policy Impact Calculator**: Intervention ROI estimator
4. **Benchmarking Dashboard**: Facility performance comparison

### Strategic Recommendations
1. Executive summary for senior leadership
2. Technical report with detailed methodology
3. Implementation roadmap for priority initiatives
4. Monitoring and evaluation framework

---

## Success Metrics for Overall Project

### Immediate Outcomes (0-3 months)
- ✅ 4 comprehensive analytical reports delivered
- ✅ 3+ actionable recommendations per problem area
- ✅ Stakeholder approval of findings and recommendations

### Medium-Term Outcomes (3-12 months)
- ✅ At least 2 policy recommendations adopted
- ✅ Measurable improvement in 1+ targeted metric
- ✅ Monitoring dashboards in active use

### Long-Term Impact (12+ months)
- ✅ Improved health outcomes in targeted areas
- ✅ More efficient healthcare resource utilization
- ✅ Enhanced capability for evidence-based policymaking
- ✅ Sustainable data analytics infrastructure established

---

## 7. Infectious Disease Seasonal Analysis & Outbreak Forecasting

### Problem Statement

**Challenge**: Healthcare facilities and public health agencies often operate reactively, responding to disease outbreaks after they occur rather than preparing proactively. Without understanding seasonal patterns and forecast capabilities, resources are distributed evenly throughout the year rather than concentrated during high-risk periods, leading to:

- **Overwhelmed Healthcare Capacity**: Emergency rooms and clinics flooded during unexpected disease surges (Dengue outbreaks, HFMD seasons)
- **Inefficient Resource Allocation**: Staff, supplies, and budgets spread evenly rather than optimized for predictable peaks
- **Missed Prevention Opportunities**: Vector control campaigns, vaccination drives, and public awareness initiatives poorly timed
- **Policy Uncertainty**: Budget allocation decisions lack data-driven justification for disease-specific programs

**Impact**:
- Healthcare system strain during outbreaks (longer wait times, staff burnout)
- Higher treatment costs from reactive vs preventive care
- Preventable disease burden due to missed intervention windows
- Budget inefficiencies from mis-timed resource deployment

**Opportunity**: Leverage 9 years (2012-2020) of weekly infectious disease surveillance data to:
- Identify which diseases exhibit strong seasonal patterns
- Forecast high-risk outbreak periods 8-12 weeks in advance
- Prioritize diseases for resource allocation based on burden metrics
- Enable proactive healthcare planning and intervention timing

### Research Questions

#### Temporal Pattern Analysis
1. Which infectious diseases show statistically significant seasonal patterns?
2. What are the peak months/weeks for Dengue Fever, HFMD, and respiratory infections?
3. Are there multi-year epidemic cycles beyond annual seasonality?
4. How consistent are seasonal patterns year-over-year?
5. Do different diseases have overlapping peak periods (compounding system strain)?

#### Outbreak Forecasting
6. Can we forecast disease case volumes 8-12 weeks in advance with ≥70% accuracy?
7. What forecasting methods work best for different disease types?
8. How do we distinguish between normal seasonal peaks vs true outbreak surges?
9. What early warning indicators (lead time) can we achieve?
10. How should confidence intervals be communicated to stakeholders?

#### Disease Burden Assessment
11. Which diseases contribute most to overall infectious disease burden?
12. How do we balance high-volume diseases (HFMD) vs high-severity diseases (Dengue Haemorrhagic Fever)?
13. Which diseases show increasing vs decreasing trends over time?
14. What are the fastest-growing infectious disease threats?
15. How has the disease burden mix shifted from 2012-2020?

#### Resource Optimization
16. How should public health resources be allocated across disease surveillance programs?
17. What is the optimal timing for preventive interventions (vector control, vaccination campaigns)?
18. How can healthcare facilities adjust staffing levels based on forecasts?
19. What cost-benefit tradeoffs exist between prevention and treatment resource allocation?
20. Can we quantify the value of proactive vs reactive resource deployment?

### Data Requirements

- **Primary Dataset**: Weekly Infectious Disease Bulletin (2012-2020)
  - 16,066 records across 45 notifiable diseases
  - 470 weeks of continuous surveillance data
  - Key diseases: Dengue Fever (126,642 cases), HFMD (73,927+ cases), Salmonellosis (16,497 cases), Mumps (4,213 cases)

- **Supplementary Data** (Future Enhancement):
  - Weather data (temperature, rainfall) for environmental correlations
  - Population demographics for rate calculations
  - Healthcare capacity metrics (beds, staff) for resource optimization
  - Intervention timing (campaigns, policies) for impact evaluation

### Analytical Approaches

#### Time Series Analysis
- **Seasonal Decomposition**: Isolate trend, seasonal, and residual components
- **Autocorrelation Analysis**: Identify temporal dependencies and lag structures
- **Spectral Analysis**: Detect dominant periodicities and cycles
- **Statistical Tests**: Mann-Kendall trend test, Kruskal-Wallis for seasonal differences

#### Forecasting Models
- **SARIMA (Seasonal ARIMA)**: Classical statistical approach for seasonal time series
- **Prophet**: Facebook's forecasting tool designed for business time series with seasonality
- **XGBoost with Lagged Features**: Machine learning approach incorporating past values
- **Ensemble Methods**: Combine multiple models for robust predictions

#### Burden Metrics
- **Absolute Burden**: Total case counts, cumulative incidence
- **Relative Burden**: Year-over-year growth rates, outbreak frequency
- **Severity Indicators**: Hospitalization rates, mortality (where available)
- **Composite Scoring**: Weighted index combining multiple burden dimensions

### Expected Deliverables

#### 1. Seasonal Disease Profiles
- Visual calendar showing peak periods for each major disease
- Statistical significance testing results for seasonal patterns
- Comparative analysis across diseases (which seasons have highest combined burden)

#### 2. Outbreak Forecasting System
- 8-12 week ahead forecasts for Dengue Fever and HFMD
- Confidence intervals and prediction accuracy metrics
- Early warning alerts when forecasts exceed thresholds
- Model validation reports on historical data

#### 3. Disease Burden Ranking
- Comprehensive ranking of all 45 diseases by multiple metrics
- Trend analysis (2012-2020) showing disease evolution
- Identification of top 10 highest-burden diseases for resource prioritization

#### 4. Resource Allocation Framework
- Decision matrix for distributing resources across diseases and time periods
- Recommended staffing levels by season for healthcare facilities
- Budget allocation recommendations by disease category
- Cost-benefit analysis of intervention timing (e.g., pre-season vector control)

#### 5. Interactive Dashboard
- Real-time monitoring of current disease levels vs forecasts
- Historical trend visualizations
- Scenario planning tools ("what if" resource allocation)

### Target Stakeholders & Use Cases

#### 1. MOH Policy Makers
**Use Case**: Evidence-based budget allocation for disease surveillance and prevention programs  
**Key Insights Needed**:
- Which diseases warrant increased funding?
- What is the return on investment for proactive vs reactive programs?
- Long-term trends to inform 3-5 year strategic planning

#### 2. Healthcare Facility Committees
**Use Case**: Operational planning for staffing, supplies, and capacity management  
**Key Insights Needed**:
- When should additional staff be scheduled?
- What supplies need to be stockpiled before peak seasons?
- How to balance resources across multiple simultaneous disease threats?

#### 3. Public Health Surveillance Teams
**Use Case**: Prioritization of surveillance efforts and outbreak response planning  
**Key Insights Needed**:
- Which diseases require enhanced monitoring?
- When to deploy rapid response teams proactively?
- Validation of current surveillance priorities

### Success Metrics

#### Analytical Quality
- Seasonal patterns identified for minimum 3 diseases with statistical significance (p < 0.05)
- Forecasting accuracy ≥70% (MAPE or similar metric) for Dengue and HFMD
- Comprehensive burden ranking for all 45 tracked diseases

#### Stakeholder Impact
- Healthcare facilities use forecasts for planning (adoption by ≥50% of facilities)
- Policy makers cite findings in ≥2 budget allocation decisions
- Public health interventions timed proactively based on forecasts

#### Operational Efficiency
- 20% improvement in outbreak response time (measured by time from forecast alert to intervention deployment)
- 15% reduction in emergency stockpiling costs through better timing
- Measurable reduction in preventable disease burden (long-term metric)

### Technical Implementation

#### Platform
- **Primary**: HEALIX/Databricks environment
- **Languages**: Python 3.9+, SQL, R (optional for specialized statistical methods)
- **Version Control**: Git/GitHub

#### Key Libraries
- **Data Processing**: pandas, numpy, polars
- **Time Series**: statsmodels, prophet, pmdarima
- **Machine Learning**: scikit-learn, xgboost, mlflow
- **Visualization**: matplotlib, seaborn, plotly, dash
- **Big Data**: pyspark (Databricks integration)

#### Deliverable Format
- **Reports**: Markdown, PDF (executive summaries)
- **Dashboards**: Plotly Dash, Streamlit, or Databricks notebooks
- **Code**: Modular Python packages with comprehensive documentation
- **Data Outputs**: CSV exports for stakeholder use

### Timeline

**Phase 1: Foundation** (Weeks 1-4)
- Data extraction, quality assessment, exploratory analysis
- Seasonal pattern identification and statistical testing
- Preliminary visualizations and insights

**Phase 2: Modeling** (Weeks 5-8)
- Forecasting model development and validation
- Disease burden analysis and ranking
- Model tuning and performance optimization

**Phase 3: Insights & Tools** (Weeks 9-12)
- Resource allocation framework development
- Interactive dashboard creation
- Executive reports and policy briefs
- Stakeholder presentations and training

### Risks & Mitigation

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| COVID-19 anomalies distort 2020 data | High | High | Focus on 2012-2019 baseline, separate COVID analysis |
| Forecasting models underperform (<70% accuracy) | High | Medium | Ensemble approach, multiple model types, conservative confidence intervals |
| Stakeholder adoption low (tools not used) | High | Low | Early engagement, user-friendly design, training sessions |
| Data quality issues (gaps, reporting changes) | Medium | Medium | Comprehensive validation, imputation protocols, sensitivity analysis |
| HEALIX/Databricks setup delays | Medium | Low | Begin on local environment, migrate to cloud platform |

### Related Analyses

**Synergies with Existing Problem Statements**:
- **Problem 1 (Disease Outbreak Detection)**: Forecasting complements early warning systems
- **Problem 3 (Healthcare Capacity Planning)**: Seasonal forecasts inform bed/staff planning
- **Problem 5 (Healthcare Expenditure)**: Resource optimization reduces reactive spending

**Future Extensions**:
- Integration with real-time surveillance data feeds
- Regional/district-level forecasting (if granular data becomes available)
- Climate-disease correlation analysis (temperature, rainfall effects)
- Impact evaluation of public health interventions

---

**Document Owner**: MOH Analytics Team  
**Review Frequency**: Quarterly or as project evolves  
**Last Review**: 9 February 2026
