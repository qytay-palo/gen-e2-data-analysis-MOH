# E01-S02: Calculate Facility Utilization Rates and Capacity Metrics

**Story ID**: E01-S02  
**Epic**: EPIC-001 - Healthcare Facility Utilization & Bottleneck Analysis

## Parent Epic
Healthcare Facility Utilization & Bottleneck Analysis

## Overview and Statement

Calculate utilization rates and capacity metrics for all healthcare facilities to establish performance baselines.

**As a** healthcare administrator  
**I want** facility utilization rates and capacity metrics calculated  
**So that** I can understand how efficiently each facility is being used relative to its capacity

### Acceptance Criteria
- [ ] Calculate utilization rate: (Actual Visits / Capacity) × 100% for each facility and year
- [ ] Compute throughput metrics (visits per day, visits per provider)
- [ ] Generate time-series of utilization trends (2006-2020)
- [ ] Identify facilities with >90% utilization (overcrowded) and <50% utilization (underutilized)
- [ ] Create facility performance scorecards with key metrics
- [ ] Save processed metrics to `results/tables/facility_utilization_metrics.csv`

### Technical Notes
- Handle missing capacity data with documented assumptions
- Account for different facility types (hospitals, polyclinics)
- Calculate both absolute (visit counts) and relative (utilization %) metrics

### Estimated Effort
3 days

### Priority
**HIGH**

## Dependencies
- E01-S01: Extract and Profile Facility Utilization Data (must be completed first)
