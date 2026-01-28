# Story 03: Temporal Visitation Pattern Exploratory Analysis

## Overview and Statement

Understanding when patients visit polyclinics is critical for resource planning. This story focuses on exploratory data analysis to uncover hourly, daily, weekly, and seasonal attendance patterns that inform staffing and capacity decisions.

**As a** Polyclinic Planning Director  
**I want** to visualize how patient visits vary across different time periods (hour, day, week, month, season)  
**So that** I can identify peak demand periods and allocate resources accordingly

### Acceptance Criteria
- [ ] Generate heatmaps showing attendance volume by:
  - Polyclinic × Hour of Day
  - Polyclinic × Day of Week
  - Month × Year (seasonality)
- [ ] Create time-series line plots showing daily attendance trends over 12-24 months
- [ ] Identify and document peak hours across all polyclinics (e.g., 9-11 AM)
- [ ] Analyze impact of public holidays on attendance volumes
- [ ] Segment analysis by visit_type (acute vs chronic) to understand demand composition
- [ ] Generate PDF report with key findings and visualizations
- [ ] Statistical test for seasonality (e.g., seasonal decomposition, ACF plots)

### Technical Notes
- Use Python (pandas, matplotlib, seaborn) on Databricks/CDSW
- Time-series decomposition using statsmodels (trend, seasonality, residual)
- Create reusable visualization functions for future analysis
- Save high-resolution figures to `reports/figures/temporal_patterns/`
- Consider time zone consistency (Singapore Standard Time)

### Estimated Effort
8-10 days

### Priority
High

## Dependencies
- [Story 02: Baseline Metrics Calculation](#02-baseline-metrics-calculation.md) - Baseline metrics provide context
- Minimum 12 months of attendance data with valid timestamps
