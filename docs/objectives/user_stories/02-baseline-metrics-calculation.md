# Story 02: Baseline Performance Metrics Calculation

## Overview and Statement

To measure the impact of future optimization initiatives, we need to establish current baseline performance metrics for polyclinic operations. This story captures the calculation of key operational KPIs that will serve as benchmarks for improvement.

**As a** Healthcare Operations Manager  
**I want** to see current baseline metrics for waiting times, occupancy rates, and no-show rates across all polyclinics  
**So that** I can understand current performance levels and set improvement targets

### Acceptance Criteria
- [ ] Calculate average waiting time by polyclinic, day of week, and time of day
- [ ] Compute daily attendance volumes per polyclinic (mean, median, 95th percentile)
- [ ] Calculate no-show rates by appointment type (walk-in vs scheduled)
- [ ] Determine peak hours and peak days for each polyclinic
- [ ] Generate summary statistics table showing:
  - Top 20% highest-volume polyclinics
  - Polyclinics with longest average waiting times
  - Visit type distribution (acute, chronic, preventive)
- [ ] Results saved as CSV/Excel for stakeholder review
- [ ] Visualization (bar charts, heatmaps) showing baseline metrics

### Technical Notes
- SQL queries via HUE or Python/Spark aggregation on Databricks
- Time period: Last 12 months to capture seasonality
- Group by: polyclinic_id, day_of_week, hour_of_day, appointment_type
- Handle missing waiting_time_minutes gracefully (report % missing)
- Export results to `results/metrics/baseline_performance.csv`

### Estimated Effort
5-8 days

### Priority
High

## Dependencies
- [Story 01: Data Quality Validation](#01-data-quality-validation.md) - Must complete data validation first
- Access to POLYCLINIC_ATTENDANCES and PATIENT_DEMOGRAPHICS tables
