# E06-S01: Prepare Historical Demand Data

**Story ID**: E06-S01  
**Epic**: EPIC-006 - Predictive Demand Forecasting for Capacity Planning

## Parent Epic
Predictive Demand Forecasting for Capacity Planning - Building validated demand forecasting models to predict patient visits and provide evidence-based capacity recommendations for strategic planning.

## Overview and Statement

Extract and prepare comprehensive historical healthcare demand data (patient visits, admissions, service utilization) to establish baseline patterns for forecasting models.

**As a** demand forecasting analyst  
**I want to** prepare clean historical demand data with consistent temporal structure  
**So that** I can build accurate forecasting models for future healthcare demand

### Acceptance Criteria
- [ ] Extract historical visit and admission data (2006-2020)
- [ ] Aggregate demand by facility, service type, and time period
- [ ] Create time-series datasets with consistent temporal granularity (monthly/quarterly)
- [ ] Calculate growth rates and trends over time
- [ ] Identify and document seasonality patterns
- [ ] Handle missing values and data gaps
- [ ] Validate data quality and consistency
- [ ] Prepare forecasting-ready datasets in time-series format

### Technical Notes
- Structure data for time-series analysis (datetime index, regular intervals)
- Use data from: `admission-and-outpatient-attendances` tables
- Calculate derived metrics: visits per capita, growth rates
- Document any data transformations or imputations
- Consider creating separate datasets by service type for granular forecasting

### Estimated Effort
4 days

### Priority
Critical

## Dependencies
None - foundational data preparation
