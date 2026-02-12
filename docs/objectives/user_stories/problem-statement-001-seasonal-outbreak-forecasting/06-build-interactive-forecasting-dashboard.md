# User Story: 6 - Build Interactive Forecasting Dashboard for Stakeholders

**As a** healthcare operations manager,
**I want** an interactive dashboard displaying historical disease trends and 8-12 week forecasts with confidence intervals,
**so that** I can monitor outbreak risk, plan staffing levels, and make proactive resource allocation decisions 2-3 months in advance.

## 1. 🎯 Acceptance Criteria

1. **Historical Trends Visualization**
   - Interactive time series plots for Dengue Fever and HFMD (2012-2020)
   - Ability to zoom, pan, and select date ranges
   - Overlay of 4-week, 8-week, 12-week moving averages
   - Outbreak periods highlighted with annotations

2. **Forecast Display**
   - 4-week, 8-week, and 12-week ahead forecasts displayed
   - Point forecasts with 80% and 95% confidence intervals (shaded bands)
   - Forecast accuracy metrics shown (MAE, MAPE from validation)
   - Forecast generation date and next update date displayed

3. **Seasonal Pattern Insights**
   - Seasonal subseries plots showing typical patterns by month/quarter
   - Year-over-year comparison views
   - Peak and trough period indicators

4. **Interactive Filters and Controls**
   - Disease selector (Dengue, HFMD, or both)
   - Forecast horizon selector (4-week, 8-week, 12-week)
   - Time period selector (custom date ranges)
   - Confidence interval toggle (show/hide uncertainty bands)

5. **Actionable Alerts and Indicators**
   - Risk indicator: Low/Medium/High based on forecast thresholds
   - Alert if forecast exceeds historical 90th percentile (outbreak risk)
   - Color-coded indicators for decision support
   - Recommended actions for different risk levels

6. **Stakeholder Accessibility**
   - Dashboard accessible via Databricks or web interface
   - Responsive design (works on desktop, tablet)
   - User guide and interpretation notes included
   - Export capabilities (PDF report, data download)

## 2. 🔒 Technical Constraints

- **Platform Options**: 
  - Databricks dashboard (internal MOH access)
  - Plotly Dash web app (if external hosting approved)
  - Tableau/Power BI integration (if preferred by stakeholders)
- **Data Refresh**: Dashboard should support weekly data updates
- **Performance**: Load time < 5 seconds; smooth interactions
- **Security**: Restrict access to authorized MOH personnel
- **Styling**: Clean, professional design aligned with MOH standards

## 3. 📚 Domain Knowledge References

- [Infectious Disease Epidemiology Terminology](../../../domain_knowledge/infectious-disease-epidemiology-terminology-glossary.md) - Outbreak definitions, risk levels
- [Time Series Forecasting Best Practices](../../../domain_knowledge/time-series-forecasting-best-practices.md) - Forecast interpretation, confidence intervals

**Dashboard Design Principles**:
- **Clarity**: Avoid clutter; focus on key insights
- **Actionability**: Link forecasts to decisions (e.g., "High risk → consider temporary staff")
- **Transparency**: Show uncertainty clearly; don't overstate confidence
- **User-centered**: Design for non-technical users (operations managers, not data scientists)

## 4. 📦 Dependencies

**External Packages**:
- `plotly` / `dash` - Interactive visualizations and web dashboard (if web app)
- `streamlit` - Alternative lightweight dashboard framework
- `matplotlib` / `seaborn` - Static visualizations for PDF exports
- `polars` / `pandas` - Data manipulation for dashboard backend

**Internal Dependencies**:
- Validated forecasting models from User Stories 4 and 5
- Historical disease surveillance data
- Forecast accuracy metrics for display

## 5. ✅ Implementation Tasks

### Dashboard Design and Specification
- ⬜ Define dashboard layout and components with stakeholder input
- ⬜ Create wireframes/mockups for review
- ⬜ Identify key metrics and visualizations needed
- ⬜ Determine data refresh frequency (weekly recommended)

### Historical Trends Visualization
- ⬜ Create interactive time series plot (Plotly line chart)
- ⬜ Add zoom, pan, and date range selection controls
- ⬜ Overlay moving averages (4-week, 8-week, 12-week)
- ⬜ Highlight outbreak periods with shaded regions or annotations
- ⬜ Add tooltip with week, case count, and contextual info

### Forecast Visualization
- ⬜ Display point forecasts as line extending from current date
- ⬜ Add 80% confidence interval as lighter shaded band
- ⬜ Add 95% confidence interval as even lighter shaded band
- ⬜ Show forecast accuracy metrics (MAE, MAPE) from validation
- ⬜ Display forecast generation date and next update date

### Seasonal Insights Panels
- ⬜ Create seasonal subseries plot (compare same month across years)
- ⬜ Add year-over-year comparison chart
- ⬜ Display peak/trough month indicators
- ⬜ Show seasonal strength metrics

### Interactive Filters and Controls
- ⬜ Add disease selector dropdown (Dengue, HFMD, Both)
- ⬜ Add forecast horizon selector (4-week, 8-week, 12-week)
- ⬜ Add custom date range picker
- ⬜ Add confidence interval toggle (show/hide)
- ⬜ Ensure filters update all visualizations in real-time

### Risk Indicators and Alerts
- ⬜ Define risk thresholds (Low: <50th percentile, Medium: 50-90th, High: >90th)
- ⬜ Calculate current forecast risk level
- ⬜ Display color-coded risk indicator (green/yellow/red)
- ⬜ Add alert if forecast exceeds historical 90th percentile
- ⬜ Provide recommended actions for each risk level

### User Guide and Documentation
- ⬜ Create dashboard user guide (how to interpret forecasts)
- ⬜ Add tooltips and help icons throughout dashboard
- ⬜ Include interpretation notes for confidence intervals
- ⬜ Document recommended actions based on forecasts
- ⬜ Provide contact info for dashboard support

### Dashboard Deployment
- ⬜ Deploy dashboard on Databricks (or Dash/Streamlit if web app)
- ⬜ Configure access controls (authorized MOH personnel only)
- ⬜ Set up automated data refresh pipeline (weekly)
- ⬜ Test dashboard performance and responsiveness
- ⬜ Conduct user acceptance testing with stakeholders
- ⬜ Provide training session for end users

### Export and Reporting Features
- ⬜ Add PDF export functionality (static report with key charts)
- ⬜ Add data download option (CSV of forecasts)
- ⬜ Create weekly email alert option (optional)
- ⬜ Generate automated summary report template

## 6. Notes

**Forecast Interpretation Guidance for Users**:
- **Point Forecast**: Most likely case count for the week
- **80% Confidence Interval**: 80% confident actual cases will fall within this range (narrower band)
- **95% Confidence Interval**: 95% confident actual cases will fall within this range (wider band)
- **Risk Indicator**: Based on forecast exceeding historical thresholds; guides proactive action

**Recommended Actions by Risk Level**:
- **Low Risk (Green)**: Normal operations; routine monitoring
- **Medium Risk (Yellow)**: Review staffing; prepare for potential increase
- **High Risk (Red)**: Activate outbreak response plan; consider temporary staff, increased supplies

**Dashboard Maintenance**:
- **Weekly refresh**: New surveillance data should trigger forecast update
- **Quarterly retraining**: Models should be retrained every 3 months with new data
- **Annual review**: Validate forecast accuracy, update thresholds if needed

**Stakeholder Engagement**:
- Conduct dashboard demo sessions for healthcare facility committees
- Gather feedback on usability and desired features
- Iterate based on user needs
- Provide ongoing support and training

**Technical Considerations**:
- **Databricks dashboard**: Easier for MOH internal users with existing access
- **Web app (Dash/Streamlit)**: More flexible but requires hosting and security setup
- **Tableau/Power BI**: If MOH prefers existing BI tools; requires integration work

**Success Metrics for Dashboard**:
- Stakeholder adoption: % of facility committees using dashboard monthly
- Decision impact: Documented cases where forecasts informed staffing decisions
- User satisfaction: Feedback surveys from dashboard users
- Forecast accuracy: Track actual vs. forecast over time; refine models as needed
