# Story 08: Real-Time Queue Monitoring Dashboard

## Overview and Statement

Operations staff need live visibility into queue status across polyclinics to respond to congestion events. This story delivers an interactive dashboard displaying current queue lengths, predicted waiting times, and occupancy rates.

**As a** Polyclinic Operations Supervisor  
**I want** to see real-time queue metrics for all polyclinics on a single dashboard  
**So that** I can proactively respond to congestion and redistribute resources if needed

### Acceptance Criteria
- [ ] Interactive dashboard (Streamlit or Dash) displaying:
  - Current queue length by polyclinic
  - Average waiting time (last 30 minutes)
  - Predicted waiting time for new arrivals
  - Occupancy rate (current patients / capacity)
  - No-show rate today vs historical average
- [ ] Color-coded alerts (green/yellow/red) for queue congestion levels
- [ ] Historical comparison (today vs same day last week)
- [ ] Auto-refresh every 5 minutes with latest data
- [ ] Drill-down capability to view individual polyclinic details
- [ ] Export snapshot report as PDF for leadership briefings

### Technical Notes
- Build with Streamlit (Python) deployed on Databricks or CDSW
- Data pipeline: Incremental load from POLYCLINIC_ATTENDANCES every 5-10 minutes
- Use Plotly for interactive visualizations
- Cache data to minimize query load on database
- Hosted URL accessible to operations team
- Consider using Spark Streaming if real-time data feed is available

### Estimated Effort
12-15 days

### Priority
High

## Dependencies
- [Story 07: Waiting Time Prediction Model](#07-waiting-time-prediction-model.md) - Dashboard displays predicted waiting times
- Real-time or near-real-time data feed from appointment/attendance system
- Server infrastructure for hosting Streamlit app
