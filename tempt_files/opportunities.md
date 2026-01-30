# Machine Learning & Analytics Opportunities
## Polyclinic Visitation Analysis & Queue Optimization

**Last Updated**: 28 January 2026  
**Project**: MOH Polyclinic Data Analysis - Gen-E2  
**Platform**: HEALIX (GCC Databricks) | **Languages**: Python, R, STATA

---

## Executive Summary

This document identifies machine learning and analytics opportunities for analyzing polyclinic visitation patterns across time and location to design effective queue management systems. The analysis delivers actionable insights to improve patient experience and optimize operational efficiency.

**Primary Objectives**:
1. **Analyze how polyclinic visitation varies across time and location**
2. **Design effective queue management systems to mitigate wait times**

**Key Stakeholders**:
- **Patients**: Reduced wait times, improved service experience
- **CEO/Leadership**: Data-driven operational insights, resource optimization

Based on available polyclinic data (attendances, demographics, diagnoses), we prioritize opportunities by expected impact and technical feasibility.

---

## Opportunity 1: Temporal Visitation Pattern Analysis

### Problem Framing
**Objective**: Understand how polyclinic visitation varies across different time dimensions to identify peak periods and seasonal trends.

**Business Question**: When do patients visit polyclinics, what are the peak hours/days/seasons, and how do these patterns inform resource allocation?

### Target Variables
- **Visit Volume**: Count of attendances by time period (hourly, daily, weekly, monthly)
- **Peak Hours**: Time periods with highest visitation (e.g., 9-11 AM)
- **Seasonality Index**: Relative demand by season/month
- **Trend Component**: Long-term growth/decline in visitation

### Potential Features
**Temporal Features**:
- `attendance_date`, `attendance_time` → Hour of day, day of week, month, public holidays
- Time-lagged features (previous day/week attendance volumes)

**Polyclinic Characteristics**:
- `polyclinic_id`, historical capacity, staffing levels
- Geographic location (`planning_area`, `region`)

**Demand Patterns**:
- `visit_type` (acute, chronic, preventive, follow-up)
- `appointment_type` (walk-in vs appointment)
- `visit_status` (completed, cancelled, no-show)
- `referring_source` (self, GP, hospital)

**Patient Demographics**:
- `age_group`, `chronic_conditions_count`
- `healthier_sg_enrolled` (national program impact)
- `residential_status`, `postal_code` (catchment area)

### Recommended Analytical Methods

**1. Descriptive Analytics** (High Priority)
- **Method**: Exploratory Data Analysis (EDA) with time-series aggregations
- **Tools**: Python (pandas, matplotlib, seaborn), SQL (via HUE)
- **Outputs**:
  - Heatmaps of attendance by polyclinic, hour, and day of week
  - Distribution of waiting times by polyclinic
  - Peak hour identification (9-11 AM, 2-4 PM patterns)
  - No-show rate analysis by appointment type
- **Timeline**: 2-3 weeks
- **Impact**: Immediate operational insights

**2. Predictive Analytics - Occupancy Forecasting** (High Priority)
- **Method**: Time-series forecasting models
- **Algorithms**: 
  - Prophet (Facebook) for trend/seasonality decomposition
  - ARIMA/SARIMA for short-term forecasts
  - LSTM (if sufficient temporal data)
- **Prediction Target**: Daily/hourly attendance volumes per polyclinic
- **Platform**: Databricks (Python: scikit-learn, statsmodels, Prophet)
- **Timeline**: 4-6 weeks
- **Impact**: Enable proactive staffing and resource planning

**3. Clustering & Segmentation** (Medium Priority)
- **Method**: Unsupervised learning - polyclinic clustering
- **Algorithms**: K-means, Hierarchical clustering, DBSCAN
- **Clustering Basis**: Attendance patterns, waiting times, patient demographics
- **Output**: Polyclinic typologies (e.g., "High-volume urban", "Senior-focused suburban")
- **Platform**: Databricks (PySpark MLlib)
- **Timeline**: 3-4 weeks
- **Impact**: Tailored operational strategies per cluster

### Data Requirements
- **Tables**: `POLYCLINIC_ATTENDANCES`, `PATIENT_DEMOGRAPHICS`, `POLYCLINIC_MASTER` (if exists)
- **Temporal Range**: Minimum 12 months for seasonality detection (2 years preferred)
- **Data Quality**: Complete `attendance_date`, `attendance_time`, `waiting_time_minutes`, `polyclinic_id`
- **Validation**: Check for missing timestamps, negative waiting times, outliers

### Evaluation Metrics
- **Forecast Accuracy**: MAPE (Mean Absolute Percentage Error) < 15%, RMSE
- **Business KPIs**: 
  - Reduction in average waiting time (target: 20% improvement)
  - Identification of top 20% high-occupancy polyclinics
  - Peak hour prediction accuracy (F1-score > 0.85)

---

## Opportunity 2: Intelligent Queue Management System

### Problem Framing
**Objective**: Develop a dynamic queue management system that optimizes patient flow, reduces waiting times, and improves patient experience.

**Business Question**: How can we predict queue lengths, optimize appointment scheduling, and reduce no-shows?

### Target Variables
- **Queue Length**: Number of patients waiting at any given time
- **Waiting Time**: `waiting_time_minutes` (actual vs predicted)
- **No-Show Probability**: Binary classification (show = 0, no-show = 1)
- **Optimal Appointment Time**: Recommended time slot to minimize overall waiting

### Potential Features
**Patient-Level Features**:
- `age_group`, `gender`, `chronic_conditions_count`
- `appointment_type` (walk-in vs scheduled)
- `visit_type` (acute, chronic, preventive)
- Historical no-show rate (patient-specific)
- `healthier_sg_enrolled`, `subsidy_category`

**Attendance Patterns**:
- `attendance_time` (scheduled time)
- `arrival_time` (punctuality history)
- Day of week, time of day, public holidays
- Weather conditions (external API integration)

**Operational Features**:
- `polyclinic_id`, current queue length (real-time)
- `consultation_duration_minutes` (by visit type)
- Staff availability, number of active consultation rooms

### Recommended Analytical Methods

**1. No-Show Prediction Model** (High Priority)
- **Method**: Binary classification
- **Algorithms**:
  - Logistic Regression (baseline)
  - Gradient Boosting (XGBoost, LightGBM) - best for tabular data
  - Random Forest
- **Features**: Historical no-show rate, age, visit type, appointment lead time, day of week
- **Platform**: Databricks (Python: scikit-learn, XGBoost)
- **Timeline**: 4-5 weeks
- **Impact**: Enable overbooking strategies to maximize clinic utilization

**2. Waiting Time Prediction** (High Priority)
- **Method**: Regression modeling
- **Algorithms**: 
  - Linear Regression (baseline)
  - Gradient Boosting Regression (XGBoost)
  - Neural Networks (if large dataset)
- **Prediction**: Expected waiting time given current queue state, patient characteristics, and time of day
- **Platform**: Databricks (Python: scikit-learn, TensorFlow)
- **Timeline**: 5-6 weeks
- **Impact**: Real-time waiting time estimates for patient communication

**3. Appointment Optimization** (Medium Priority)
- **Method**: Mathematical optimization / Simulation
- **Techniques**: 
  - Linear Programming (LP) for slot allocation
  - Discrete Event Simulation (SimPy) to model queue dynamics
  - Reinforcement Learning (Q-learning) for adaptive scheduling
- **Objective Function**: Minimize total waiting time + no-show penalties
- **Constraints**: Clinic capacity, staff availability, patient preferences
- **Platform**: Databricks (Python: PuLP, SimPy, OR-Tools)
- **Timeline**: 6-8 weeks
- **Impact**: Optimized appointment slots reduce congestion by 15-25%

**4. Real-Time Queue Monitoring Dashboard** (High Priority)
- **Method**: Live data streaming & visualization
- **Tools**: 
  - Apache Spark Streaming (for real-time data)
  - Streamlit or Dash for interactive dashboards
  - Power BI / Tableau for stakeholder dashboards
- **Metrics**: Current queue length, predicted waiting time, occupancy rate
- **Platform**: Databricks + Streamlit
- **Timeline**: 3-4 weeks
- **Impact**: Operations team can proactively manage queues

### Data Requirements
- **Tables**: `POLYCLINIC_ATTENDANCES` (with `arrival_time`, `consultation_start_time`, `visit_status`)
- **Real-Time Data**: Integration with appointment booking system (if available)
- **Historical Data**: Minimum 12 months for training models
- **Data Quality**: Complete timestamps, accurate `visit_status` (to identify no-shows)

### Evaluation Metrics
- **No-Show Prediction**: AUC-ROC > 0.75, Precision/Recall balance (F1-score > 0.70)
- **Waiting Time Prediction**: MAE < 10 minutes, RMSE < 15 minutes
- **Business KPIs**:
  - Reduction in average waiting time (target: 25%)
  - Decrease in no-show rate (target: 10% reduction)
  - Improved clinic utilization rate (target: 90%+)

---

## Opportunity 3: Patient Flow Optimization

### Problem Framing
**Objective**: Analyze end-to-end patient journey to identify bottlenecks and optimize operational workflows.

**Business Question**: Where do delays occur in the patient journey (arrival → consultation → treatment → discharge)?

### Target Variables
- **Total Visit Duration**: `consultation_end_time` - `arrival_time`
- **Consultation Duration**: `consultation_duration_minutes`
- **Process Bottlenecks**: Time spent in waiting vs consultation vs treatment

### Potential Features
- `visit_type`, `appointment_type`, `referring_source`
- Number of diagnoses, procedures, medications prescribed
- Complexity score (derived from ICD codes, medication count)
- Staff characteristics (seniority, specialization)

### Recommended Analytical Methods

**1. Process Mining** (Medium Priority)
- **Method**: Event log analysis to map patient journey
- **Tools**: Python (pm4py), R (bupaR)
- **Outputs**: Process flowcharts, bottleneck identification, variant analysis
- **Platform**: CDSW (Python/R)
- **Timeline**: 3-4 weeks
- **Impact**: Visual representation of delays for process improvement

**2. Survival Analysis** (Low Priority)
- **Method**: Time-to-event modeling (e.g., Cox Proportional Hazards)
- **Use Case**: Analyze factors influencing time to consultation start
- **Platform**: STATA, R (survival package)
- **Timeline**: 4-5 weeks
- **Impact**: Identify patient/operational factors causing delays

### Data Requirements
- **Tables**: `POLYCLINIC_ATTENDANCES`, `DIAGNOSIS_RECORDS`, `MEDICATION_RECORDS`, `PROCEDURE_RECORDS`
- **Temporal Data**: All timestamp fields (`arrival_time`, `consultation_start_time`, `consultation_end_time`)
- **Data Quality**: No missing timestamps, logical sequence validation

### Evaluation Metrics
- **Process Efficiency**: Reduction in non-value-added time (target: 20%)
- **Consultation Variance**: Standardization of consultation duration by visit type
- **Patient Satisfaction**: Indirect metric (reduced total visit time)

---

## Opportunity 4: Resource Allocation & Capacity Planning

### Problem Framing
**Objective**: Optimize staff scheduling and resource allocation based on predicted demand.

**Business Question**: How many doctors/nurses are needed at each polyclinic during different time periods?

### Target Variables
- **Staffing Requirements**: Number of doctors/nurses needed per hour
- **Capacity Utilization**: Actual attendances / Maximum capacity

### Potential Features
- Predicted attendance volume (from Opportunity 1)
- Average consultation duration by visit type
- Staff availability constraints
- Budget constraints

### Recommended Analytical Methods

**1. Capacity Planning Model** (Medium Priority)
- **Method**: Queueing theory (M/M/c model) + Optimization
- **Algorithms**: Linear Programming (LP), Integer Programming (IP)
- **Platform**: Python (PuLP, OR-Tools), STATA
- **Timeline**: 5-6 weeks
- **Impact**: Optimal staffing schedules reduce idle time and overtime costs

**2. Scenario Analysis** (Medium Priority)
- **Method**: What-if simulation modeling
- **Use Case**: Test impact of adding staff, changing opening hours, introducing telemedicine
- **Tools**: Excel (Power Query), Python (SimPy)
- **Timeline**: 3-4 weeks
- **Impact**: Data-driven decision making for capital investments

### Data Requirements
- **Tables**: `POLYCLINIC_ATTENDANCES`, staffing rosters (if available)
- **External Data**: Polyclinic capacity (number of consultation rooms, max patients/hour)
- **Cost Data**: Staff wages, overhead costs

### Evaluation Metrics
- **Utilization Rate**: Target 85-90% (not over/under-staffed)
- **Cost Efficiency**: Cost per patient visit reduction (target: 10%)
- **Service Level**: 90% of patients seen within target waiting time

---

## Prioritization Matrix

| Opportunity | Expected Impact | Technical Feasibility | Timeline | Priority |
|-------------|-----------------|----------------------|----------|----------|
| **1. Occupancy & Congestion Analysis** | High | High | 2-6 weeks | **HIGH** |
| **2. Queue Management System** | High | Medium | 4-8 weeks | **HIGH** |
| **3. Patient Flow Optimization** | Medium | Medium | 3-5 weeks | **MEDIUM** |
| **4. Resource Allocation** | Medium | Medium | 5-6 weeks | **MEDIUM** |

### Recommended Implementation Sequence

**Phase 1 (Months 1-2)**: Foundation & Quick Wins
1. Occupancy & Congestion Analysis (descriptive analytics)
2. Real-time queue monitoring dashboard
3. Data quality validation and pipeline setup

**Phase 2 (Months 2-4)**: Predictive Models
1. No-show prediction model
2. Waiting time prediction model
3. Occupancy forecasting (time-series models)

**Phase 3 (Months 4-6)**: Optimization & Advanced Analytics
1. Appointment optimization system
2. Resource allocation models
3. Patient flow process mining

---

## Technical Stack Alignment

All opportunities are designed to leverage:
- **Platform**: Databricks (HEALIX/GCC) or CDSW (MCDR)
- **Languages**: Python (primary), R (statistical analysis), SQL (data extraction via HUE)
- **ML Libraries**: scikit-learn, XGBoost, Prophet, PySpark MLlib
- **Visualization**: Streamlit, matplotlib, seaborn, Plotly
- **Computation**: Apache Spark for distributed processing

---

## Success Criteria

**Operational Improvements**:
- 20-25% reduction in average waiting time
- 10% reduction in no-show rate
- 15% improvement in clinic utilization rate
- Identification of top 20% high-occupancy polyclinics

**Technical Deliverables**:
- Occupancy forecasting model with MAPE < 15%
- No-show prediction model with AUC-ROC > 0.75
- Real-time queue monitoring dashboard
- Automated reporting pipeline for weekly/monthly stakeholder updates

**Stakeholder Value**:
- Data-driven resource allocation decisions
- Improved patient satisfaction (reduced waiting times)
- Optimized operational costs
- Proactive capacity planning for population health growth

---

## Next Steps

1. ✅ **Data Validation**: Verify completeness of `POLYCLINIC_ATTENDANCES` table (waiting time, timestamps)
2. ✅ **Baseline Metrics**: Calculate current average waiting times, occupancy rates, no-show rates
3. ✅ **EDA Phase**: Conduct exploratory data analysis to validate hypotheses
4. ⏳ **Model Development**: Start with descriptive analytics, then predictive models
5. ⏳ **Dashboard Deployment**: Build Streamlit dashboard for stakeholder visualization

---

*This document will be updated as the project progresses and new opportunities are identified.*
