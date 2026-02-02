# E06-S04: Model Demographic Impact on Demand

**Story ID**: E06-S04  
**Epic**: EPIC-006 - Predictive Demand Forecasting for Capacity Planning

## Parent Epic
Predictive Demand Forecasting for Capacity Planning - Building validated demand forecasting models to predict patient visits and provide evidence-based capacity recommendations for strategic planning.

## Overview and Statement

Develop regression models incorporating demographic factors (population growth, aging, disease prevalence) to understand their impact on future healthcare demand.

**As a** strategic healthcare planner  
**I want to** understand how demographic changes will affect healthcare demand  
**So that** I can plan capacity for an aging and growing population

### Acceptance Criteria
- [ ] Gather demographic data: population growth, age structure changes, disease prevalence trends
- [ ] Build regression models linking demographics to healthcare demand
- [ ] Quantify impact of population growth on demand (elasticity)
- [ ] Model effect of population aging on service utilization
- [ ] Project future demographics (2021-2030) using available sources
- [ ] Generate demand forecasts incorporating demographic projections
- [ ] Create scenario analyses (low, medium, high demographic change)
- [ ] Document demographic impact findings and implications

### Technical Notes
- Use external demographic data (Singapore statistics, UN projections)
- Build multiple regression or machine learning models
- Consider age-specific utilization rates
- Account for changing disease burden with aging
- Create scenario-based projections with assumptions
- Validate demographic models against historical relationships
- Visualize demographic-driven demand scenarios

### Estimated Effort
7 days

### Priority
High

## Dependencies
- E06-S01: Requires demand data
- E06-S02: Requires demand pattern understanding
