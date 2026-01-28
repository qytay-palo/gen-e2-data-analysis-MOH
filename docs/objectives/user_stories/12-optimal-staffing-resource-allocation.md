# Story 12: Optimal Staffing Model for Resource Allocation

## Overview and Statement

Staffing levels must align with forecasted demand to maintain service quality while controlling costs. This story builds a capacity planning model that recommends optimal staffing levels by polyclinic and time period based on predicted patient volumes.

**As a** Workforce Planning Director  
**I want** to determine the optimal number of doctors and nurses needed at each polyclinic during different time periods  
**So that** I can maintain target service levels while minimizing staffing costs

### Acceptance Criteria
- [ ] Build queueing theory model (M/M/c or similar) to calculate required staff
- [ ] Inputs include:
  - Forecasted attendance volumes (from Story 05)
  - Target service level (e.g., 90% of patients seen within 30 minutes)
  - Average consultation duration by visit type
  - Staff cost data (hourly wages)
- [ ] Optimize staffing to minimize costs subject to service level constraints
- [ ] Generate recommended staffing schedules by:
  - Polyclinic
  - Day of week
  - Hour of day
- [ ] Calculate expected utilization rates (target 85-90%)
- [ ] Scenario analysis: impact of adding/removing staff on waiting times
- [ ] Cost-benefit analysis showing ROI of optimized staffing

### Technical Notes
- Use PuLP or OR-Tools for optimization (Python)
- Queueing theory calculations using queue library or custom implementation
- Consider part-time staff and shift constraints
- Incorporate minimum staffing requirements for safety/quality
- Platform: Databricks with Python (PuLP, numpy, scipy)
- Generate Excel-based staffing schedule templates

### Estimated Effort
20-25 days

### Priority
Medium

## Dependencies
- [Story 05: Occupancy Forecasting Model](#05-occupancy-forecasting-model.md) - Demand forecasts drive staffing needs
- [Story 11: Consultation Duration Analysis](#11-consultation-duration-analysis.md) - Service time estimates
- Staff cost data and availability constraints
