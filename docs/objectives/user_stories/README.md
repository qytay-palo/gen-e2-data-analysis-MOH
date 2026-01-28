# User Stories: Polyclinic Analytics and Queue Optimization

**Project**: MOH Polyclinic Data Analysis - Gen-E2  
**Last Updated**: 28 January 2026  
**Total Stories**: 22  
**Estimated Total Effort**: 270-330 days

---

## Overview

This directory contains user stories derived from the [Opportunities Document](../opportunities.md), structured to guide incremental development of a comprehensive polyclinic analytics and queue optimization system. Each story represents an actionable work item that delivers specific value to stakeholders while building toward the project's strategic objectives.

### Project Objectives
1. Analyze how polyclinic visitation varies across time and location
2. Design effective queue management systems to mitigate wait times
3. Optimize resource allocation and operational efficiency
4. Improve patient experience through data-driven interventions

---

## User Stories Index

### Phase 1: Foundation & Quick Wins (Stories 1-3, 19, 22)
**Timeline**: Months 1-2 | **Estimated Effort**: 45-60 days  
**Focus**: Data infrastructure, quality validation, baseline metrics, and security

| # | Story Title | Priority | Effort | Key Stakeholder |
|---|-------------|----------|--------|-----------------|
| 01 | [Data Quality Validation Pipeline](01-data-quality-validation.md) | High | 3-5 days | Data Scientist |
| 02 | [Baseline Performance Metrics Calculation](02-baseline-metrics-calculation.md) | High | 5-8 days | Operations Manager |
| 03 | [Temporal Visitation Pattern Exploratory Analysis](03-temporal-visitation-eda.md) | High | 8-10 days | Planning Director |
| 19 | [Data Pipeline Infrastructure Setup](19-data-pipeline-infrastructure-setup.md) | High | 15-20 days | Data Engineer |
| 22 | [Security and Privacy Compliance Review](22-security-privacy-compliance.md) | High | 8-10 days | Data Protection Officer |

**Deliverables**: Clean data pipeline, baseline KPIs, initial temporal insights, security framework

---

### Phase 2: Predictive Models & Analytics (Stories 4-7, 11)
**Timeline**: Months 2-4 | **Estimated Effort**: 90-115 days  
**Focus**: Machine learning models for forecasting, prediction, and classification

| # | Story Title | Priority | Effort | Key Stakeholder |
|---|-------------|----------|--------|-----------------|
| 04 | [Polyclinic Clustering and Segmentation](04-polyclinic-clustering-segmentation.md) | Medium | 10-13 days | Policy Analyst |
| 05 | [Daily Occupancy Forecasting Model](05-occupancy-forecasting-model.md) | High | 15-20 days | Operations Manager |
| 06 | [Patient No-Show Prediction Model](06-no-show-prediction-model.md) | High | 18-22 days | Appointment Scheduler |
| 07 | [Real-Time Waiting Time Prediction Model](07-waiting-time-prediction-model.md) | High | 18-22 days | Patient |
| 11 | [Consultation Duration Analysis and Prediction](11-consultation-duration-analysis.md) | Medium | 13-16 days | Clinical Operations Manager |

**Deliverables**: Occupancy forecasts, no-show predictions, waiting time estimates, polyclinic typologies

---

### Phase 3: Optimization & Real-Time Systems (Stories 8, 9, 12, 17)
**Timeline**: Months 4-6 | **Estimated Effort**: 67-88 days  
**Focus**: Real-time dashboards, optimization models, automated reporting

| # | Story Title | Priority | Effort | Key Stakeholder |
|---|-------------|----------|--------|-----------------|
| 08 | [Real-Time Queue Monitoring Dashboard](08-real-time-queue-monitoring-dashboard.md) | High | 12-15 days | Operations Supervisor |
| 09 | [Appointment Slot Optimization Model](09-appointment-slot-optimization.md) | Medium | 20-25 days | Operations Planner |
| 12 | [Optimal Staffing Model for Resource Allocation](12-optimal-staffing-resource-allocation.md) | Medium | 20-25 days | Workforce Planning Director |
| 17 | [Automated Weekly Stakeholder Reporting Pipeline](17-automated-weekly-reporting-pipeline.md) | High | 10-13 days | Healthcare CEO |

**Deliverables**: Live queue dashboard, optimized appointment schedules, staffing recommendations, automated reports

---

### Phase 4: Advanced Analytics & Patient Insights (Stories 10, 13-16)
**Timeline**: Months 6-8 | **Estimated Effort**: 68-86 days  
**Focus**: Process mining, patient segmentation, chronic disease management, scenario planning

| # | Story Title | Priority | Effort | Key Stakeholder |
|---|-------------|----------|--------|-----------------|
| 10 | [Patient Journey Process Mining Analysis](10-patient-journey-process-mining.md) | Medium | 12-15 days | Process Improvement Manager |
| 13 | [Scenario Planning and What-If Analysis Tool](13-scenario-planning-what-if-analysis.md) | Medium | 15-18 days | Policy Maker |
| 14 | [Geographic Access and Catchment Area Analysis](14-geographic-access-catchment-analysis.md) | Medium | 13-16 days | Infrastructure Planner |
| 15 | [Patient Segmentation and Persona Development](15-patient-segmentation-personas.md) | Low | 12-15 days | Service Designer |
| 16 | [Chronic Disease Management Impact Analysis](16-chronic-disease-management-analysis.md) | Medium | 15-18 days | Disease Management Director |

**Deliverables**: Process bottleneck identification, patient personas, geographic insights, chronic care optimization

---

### Phase 5: Operations & Governance (Stories 18, 20, 21)
**Timeline**: Ongoing | **Estimated Effort**: 35-44 days  
**Focus**: Model monitoring, testing, documentation, and long-term sustainability

| # | Story Title | Priority | Effort | Key Stakeholder |
|---|-------------|----------|--------|-----------------|
| 18 | [Model Monitoring and Performance Tracking System](18-model-monitoring-performance-tracking.md) | Medium | 13-16 days | Data Science Team Lead |
| 20 | [Testing Framework for Analytics Code](20-testing-framework-analytics-code.md) | Medium | 10-13 days | Data Science Engineer |
| 21 | [Documentation Repository and Knowledge Management](21-documentation-knowledge-management.md) | Medium | 12-15 days | Project Stakeholder |

**Deliverables**: Model monitoring system, automated tests, comprehensive documentation

---

## Implementation Roadmap

### Recommended Implementation Sequence

**Month 1-2: Foundation**
1. Start with Story 19 (Data Pipeline) - critical infrastructure
2. Parallel: Story 22 (Security) - ensure compliance from day one
3. Story 01 (Data Quality) - validate data before analysis
4. Story 02 (Baseline Metrics) - establish current state
5. Story 03 (Temporal EDA) - quick win with immediate insights

**Month 2-4: Predictive Capabilities**
1. Story 05 (Occupancy Forecasting) - foundational for other models
2. Story 06 (No-Show Prediction) - high business value
3. Story 07 (Waiting Time Prediction) - patient-facing benefit
4. Parallel: Story 04 (Polyclinic Clustering) - enables segmented strategies
5. Story 11 (Consultation Duration) - supports scheduling optimization

**Month 4-6: Optimization & Automation**
1. Story 08 (Real-Time Dashboard) - immediate operational value
2. Story 17 (Weekly Reporting) - stakeholder visibility
3. Story 09 (Appointment Optimization) - complex but high impact
4. Story 12 (Staffing Model) - cost savings opportunity

**Month 6-8: Advanced Analytics**
1. Story 13 (Scenario Planning) - decision support tool
2. Story 10 (Process Mining) - operational insights
3. Story 16 (Chronic Disease) - clinical value
4. Story 14 (Geographic) - strategic planning
5. Story 15 (Patient Personas) - service design

**Ongoing: Operations**
- Story 18 (Model Monitoring) - deploy as models go to production
- Story 20 (Testing) - implement throughout development
- Story 21 (Documentation) - continuous maintenance

---

## Story Statistics

### By Priority
- **High Priority**: 9 stories (41%)
- **Medium Priority**: 12 stories (55%)
- **Low Priority**: 1 story (4%)

### By Estimated Effort
- **Short (< 10 days)**: 4 stories
- **Medium (10-20 days)**: 12 stories
- **Long (> 20 days)**: 6 stories

### By Phase
- **Phase 1 (Foundation)**: 5 stories
- **Phase 2 (Predictive)**: 5 stories
- **Phase 3 (Optimization)**: 4 stories
- **Phase 4 (Advanced)**: 5 stories
- **Phase 5 (Operations)**: 3 stories

---

## Dependencies Map

### Critical Path Stories (Must Complete First)
1. **Story 19**: Data Pipeline Infrastructure - *Enables all analytics*
2. **Story 01**: Data Quality Validation - *Ensures data reliability*
3. **Story 02**: Baseline Metrics - *Establishes benchmarks*

### Story Dependencies
- **Story 03** depends on Story 02
- **Story 04** depends on Story 03
- **Story 05** depends on Story 03
- **Story 06** depends on Story 02
- **Story 07** depends on Story 03
- **Story 08** depends on Story 07
- **Story 09** depends on Stories 05, 06
- **Story 11** depends on none (can run independently)
- **Story 12** depends on Stories 05, 11
- **Story 13** depends on Stories 05, 07, 12
- **Story 17** depends on Stories 02, 05
- **Story 18** depends on Stories 05, 06, 07 (models to monitor)

---

## Success Criteria

### Operational Improvements (Target Outcomes)
- ✅ 20-25% reduction in average waiting time
- ✅ 10% reduction in no-show rate
- ✅ 15% improvement in clinic utilization rate
- ✅ Identification of top 20% high-occupancy polyclinics
- ✅ Proactive staffing aligned with forecasted demand

### Technical Deliverables
- ✅ Occupancy forecasting model with MAPE < 15%
- ✅ No-show prediction model with AUC-ROC > 0.75
- ✅ Waiting time prediction with MAE < 10 minutes
- ✅ Real-time queue monitoring dashboard (5-minute refresh)
- ✅ Automated weekly reporting to stakeholders
- ✅ Comprehensive documentation repository

### Data & Infrastructure
- ✅ Automated daily ETL pipeline with data quality checks
- ✅ Model monitoring and retraining framework
- ✅ Security and privacy compliance certification
- ✅ Test coverage > 70% for critical code

---

## Key Stakeholders

- **Patients**: Reduced wait times, improved experience
- **Polyclinic Operations Managers**: Real-time insights, forecasting tools
- **Healthcare CEO/Leadership**: Strategic insights, performance monitoring
- **Workforce Planning Teams**: Optimized staffing schedules
- **Clinical Teams**: Better resource allocation, chronic care coordination
- **Data Science Team**: Robust infrastructure and models
- **Policy Makers**: Evidence-based decision support

---

## Technical Stack Alignment

All stories are designed to leverage:
- **Platforms**: Databricks (HEALIX/GCC) or CDSW (MCDR)
- **Languages**: Python (primary), R (statistical analysis), SQL (data extraction)
- **ML Libraries**: scikit-learn, XGBoost, Prophet, PySpark MLlib
- **Visualization**: Streamlit, matplotlib, seaborn, Plotly
- **Infrastructure**: Apache Spark for distributed processing, HDFS for storage

---

## Getting Started

### For Project Managers
1. Review Phase 1 stories to understand foundational requirements
2. Assess resource availability (data scientists, engineers, infrastructure)
3. Establish stakeholder communication plan
4. Set up sprint planning using this story backlog

### For Data Scientists
1. Start with [Story 01](01-data-quality-validation.md) to understand data quality
2. Review [Story 02](02-baseline-metrics-calculation.md) for baseline KPIs
3. Familiarize with [Story 03](03-temporal-visitation-eda.md) for initial analysis approach
4. Check dependencies before starting any story

### For Engineers
1. Prioritize [Story 19](19-data-pipeline-infrastructure-setup.md) for infrastructure
2. Implement [Story 22](22-security-privacy-compliance.md) security controls
3. Set up [Story 20](20-testing-framework-analytics-code.md) testing framework early

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| 28 Jan 2026 | 1.0 | Initial user stories created from opportunities document |

---

## Questions or Feedback?

For questions about specific user stories or to propose modifications, please refer to the [project documentation](../../../README.md) or contact the project team.
