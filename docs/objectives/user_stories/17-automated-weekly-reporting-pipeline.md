# Story 17: Automated Weekly Stakeholder Reporting Pipeline

## Overview and Statement

Stakeholders require regular updates on operational metrics to monitor performance and make timely decisions. This story automates the generation and distribution of weekly performance reports containing key operational KPIs and trend analysis.

**As a** Healthcare CEO  
**I want** to receive automated weekly reports showing polyclinic performance metrics and trends  
**So that** I can monitor system performance and make informed strategic decisions

### Acceptance Criteria
- [ ] Automated pipeline that runs every Monday morning to generate reports
- [ ] Report includes:
  - Key metrics: average waiting time, daily volumes, no-show rates, occupancy rates
  - Week-over-week comparison and trend indicators
  - Top performers and areas of concern (flagged in red)
  - Forecasted volumes for upcoming week
  - Alerts for anomalies (e.g., sudden spike in no-shows)
- [ ] Multiple output formats:
  - PDF executive summary for leadership
  - Excel detailed tables for operations teams
  - Interactive HTML dashboard for self-service exploration
- [ ] Email distribution to stakeholder list
- [ ] Archive historical reports in `reports/weekly/` directory

### Technical Notes
- Use Python for report generation (pandas, matplotlib, reportlab for PDF)
- Schedule with cron job or Databricks Jobs
- Query latest 7 days of data from POLYCLINIC_ATTENDANCES
- Template-based reporting for consistent formatting
- Platform: Databricks with scheduled notebook execution
- Email integration using SMTP or cloud email services

### Estimated Effort
10-13 days

### Priority
High

## Dependencies
- [Story 02: Baseline Metrics Calculation](#02-baseline-metrics-calculation.md) - Metrics definitions
- [Story 05: Occupancy Forecasting Model](#05-occupancy-forecasting-model.md) - Weekly forecasts
- Stable data pipeline with reliable incremental loads
- Email distribution list and SMTP configuration
