# E01-S02: Calculate Facility Utilization Metrics

**Story ID**: E01-S02  
**Epic**: EPIC-001 - Healthcare Facility Utilization & Bottleneck Analysis

## Parent Epic
Healthcare Facility Utilization & Bottleneck Analysis - Analyzing patient distribution patterns, service utilization rates, and process bottlenecks to enable evidence-based resource allocation and operational improvements.

## Overview and Statement

Calculate comprehensive utilization metrics for all healthcare facilities including utilization rates, throughput, and capacity metrics to establish baseline performance indicators.

**As a** healthcare operations analyst  
**I want to** calculate standardized utilization metrics across all facilities  
**So that** I can compare performance and identify capacity constraints

### Acceptance Criteria
- [ ] Calculate facility utilization rate: (Actual Visits / Capacity) × 100% for all facilities
- [ ] Compute throughput metrics (patients per day/week/month)
- [ ] Calculate average service time and wait time estimates where data permits
- [ ] Generate summary statistics (mean, median, standard deviation, percentiles) by facility
- [ ] Create time-series of utilization metrics (2006-2020)
- [ ] Identify facilities with >90% utilization (overcrowded) and <50% utilization (underutilized)
- [ ] Document methodology and formulas used for all calculations

### Technical Notes
- Define capacity based on bed counts, operating hours, and staffing levels
- Handle missing capacity data with reasonable assumptions (document all assumptions)
- Calculate rolling averages to smooth temporal fluctuations
- Create reusable functions for metric calculations

### Estimated Effort
4 days

### Priority
High

## Dependencies
- E01-S01: Requires cleaned facility utilization data
