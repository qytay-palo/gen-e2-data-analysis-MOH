# Story 13: Scenario Planning and What-If Analysis Tool

## Overview and Statement

Decision-makers need to evaluate the impact of operational changes before implementation. This story delivers an interactive scenario analysis tool allowing users to test "what-if" scenarios for changes in staffing, opening hours, or appointment policies.

**As a** Healthcare Policy Maker  
**I want** to simulate the impact of operational changes (e.g., adding staff, extending hours, introducing telemedicine slots)  
**So that** I can make evidence-based decisions about resource investments

### Acceptance Criteria
- [ ] Interactive tool (Streamlit/Dash) allowing users to input scenario parameters:
  - Change in staffing levels (±X doctors/nurses)
  - Change in opening hours (extend by Y hours)
  - Introduction of telemedicine slots (Z% of appointments)
  - Change in appointment slot duration
- [ ] Simulation engine estimates impact on:
  - Average waiting time
  - Daily capacity (patients served)
  - Staff utilization rate
  - Estimated cost change
- [ ] Compare scenario outcomes side-by-side with current baseline
- [ ] Visualize results with charts showing key metrics before/after
- [ ] Export scenario analysis reports as PDF for stakeholder review

### Technical Notes
- Build with Streamlit (Python) or R Shiny
- Use Discrete Event Simulation (SimPy) for complex scenarios
- Leverage forecasting and optimization models from previous stories
- Allow saved scenario configurations for repeated analysis
- Platform: Databricks with Streamlit deployment

### Estimated Effort
15-18 days

### Priority
Medium

## Dependencies
- [Story 05: Occupancy Forecasting Model](#05-occupancy-forecasting-model.md) - Baseline demand forecasts
- [Story 07: Waiting Time Prediction Model](#07-waiting-time-prediction-model.md) - Waiting time estimates
- [Story 12: Optimal Staffing Model](#12-optimal-staffing-resource-allocation.md) - Staffing calculations
