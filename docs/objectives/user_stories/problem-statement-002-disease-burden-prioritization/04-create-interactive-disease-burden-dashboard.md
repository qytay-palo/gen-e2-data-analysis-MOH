# User Story: 4 - Create Interactive Disease Burden Dashboard

**As an** MOH policy maker,
**I want** an interactive dashboard displaying disease burden rankings, trends, and multi-dimensional profiles,
**so that** I can explore burden data, justify budget decisions, and communicate priorities to stakeholders with visual evidence.

## 1. 🎯 Acceptance Criteria

1. **Disease Ranking Visualization**
   - Sortable table showing all 45 diseases with burden scores and tier assignments
   - Bar chart of top 20 diseases by composite burden score
   - Ability to sort by different metrics (volume, trend, outbreak, volatility)
   - Downloadable rankings table (CSV/Excel)

2. **Multi-Dimensional Disease Profiles**
   - Spider/radar charts showing burden across multiple dimensions for selected diseases
   - Comparison mode: overlay 2-3 diseases on same radar chart
   - Disease profile cards for top 15 diseases (key metrics, trend direction, tier)

3. **Trend Analysis Views**
   - Time series plots for top diseases showing 9-year trends
   - Emerging threats section highlighting diseases with increasing trends
   - Declining diseases section showing successful control
   - Year-over-year growth comparison

4. **Interactive Filters and Controls**
   - Filter diseases by tier (High, Medium, Low)
   - Filter by category (vector-borne, foodborne, vaccine-preventable)
   - Search diseases by name
   - Adjust weighting sliders to see ranking changes in real-time

5. **Sensitivity Analysis Visualizations**
   - Ranking stability chart showing how rankings change under different weightings
   - Scenario comparison table (base case vs. alternative weightings)
   - Consensus priority indicators (diseases consistently top-ranked)

6. **Export and Reporting**
   - PDF export of dashboard for presentations
   - Data download (rankings, metrics, trends)
   - Generate automated burden assessment report

## 2. 🔒 Technical Constraints

- **Platform**: Databricks dashboard or Plotly Dash web app
- **Performance**: Dashboard load time <5 seconds; smooth interactions
- **Accessibility**: Authorized MOH personnel only
- **Responsive Design**: Works on desktop and tablet
- **Data Refresh**: Support annual updates with new surveillance data

## 3. 📚 Domain Knowledge References

- [Disease Burden Assessment Methodology](../../../domain_knowledge/disease-burden-assessment-methodology.md) - Visualization best practices, dashboard design principles
- [Infectious Disease Epidemiology Terminology](../../../domain_knowledge/infectious-disease-epidemiology-terminology-glossary.md) - Disease categories, terminology for labels

**Dashboard Design Principles**:
- **Clarity**: Focus on key insights; avoid cluttered visualizations
- **Actionability**: Link burden rankings to resource allocation decisions
- **Transparency**: Show how rankings are calculated; build stakeholder trust
- **Interactivity**: Enable exploration and customization

## 4. 📦 Dependencies

**External Packages**:
- `plotly` / `dash` - Interactive visualizations and dashboard framework
- `matplotlib` / `seaborn` - Static visualizations for PDF exports
- `polars` / `pandas` - Data manipulation for dashboard backend

**Internal Dependencies**:
- Disease burden metrics from User Story 2
- Prioritization framework and rankings from User Story 3
- Historical disease surveillance data for trend plots

## 5. ✅ Implementation Tasks

### Dashboard Design and Architecture
- ⬜ Design dashboard layout with wireframes
- ⬜ Define dashboard sections: Rankings, Profiles, Trends, Sensitivity
- ⬜ Create mockups for stakeholder review
- ⬜ Select dashboard framework (Databricks vs. Dash)

### Disease Ranking Visualizations
- ⬜ Create sortable, filterable table of all 45 diseases
- ⬜ Add columns: Rank, Disease, Burden Score, Tier, Key Metrics
- ⬜ Create horizontal bar chart (top 20 diseases by burden score)
- ⬜ Color-code by tier (High=red, Medium=yellow, Low=green)
- ⬜ Add tooltips with detailed metrics on hover

### Multi-Dimensional Profile Views
- ⬜ Create spider/radar chart component for disease profiles
- ⬜ Display 4-6 dimensions: Volume, Trend, Outbreak, Volatility, etc.
- ⬜ Implement disease comparison mode (overlay multiple diseases)
- ⬜ Create disease profile cards for top 15 diseases
- ⬜ Include key stats, trend indicators, tier assignment in cards

### Trend Analysis Visualizations
- ⬜ Create time series plots for top diseases (2012-2020)
- ⬜ Add trend lines and growth rates
- ⬜ Create "Emerging Threats" section (diseases with increasing trends)
- ⬜ Create "Declining Diseases" section (successful control examples)
- ⬜ Add year-over-year growth comparison chart

### Interactive Filters and Controls
- ⬜ Add tier filter dropdown (High, Medium, Low, All)
- ⬜ Add category filter (Vector-borne, Foodborne, etc.)
- ⬜ Add disease name search box
- ⬜ Implement weight adjustment sliders (Volume, Trend, Outbreak, Volatility)
- ⬜ Update rankings and charts in real-time when weights change

### Sensitivity Analysis Visualizations
- ⬜ Create ranking stability chart (show rank changes across scenarios)
- ⬜ Build scenario comparison table (base case vs. alternatives)
- ⬜ Highlight consensus priorities (consistently high-ranked)
- ⬜ Flag sensitive diseases (ranking varies significantly)

### Export and Reporting Features
- ⬜ Add PDF export button (dashboard snapshot)
- ⬜ Add CSV download for rankings table
- ⬜ Add Excel download for full burden metrics
- ⬜ Generate automated summary report template

### Dashboard Deployment
- ⬜ Deploy dashboard on Databricks or host Dash web app
- ⬜ Configure access controls
- ⬜ Set up data refresh pipeline for annual updates
- ⬜ Test performance and usability
- ⬜ Conduct user acceptance testing

### Documentation and Training
- ⬜ Create dashboard user guide
- ⬜ Add help tooltips throughout dashboard
- ⬜ Document how to interpret rankings and metrics
- ⬜ Provide training session for stakeholders

## 6. Notes

**Dashboard Use Cases**:
- **Budget Planning**: Policy makers use rankings to justify program funding
- **Program Evaluation**: Disease managers see their program's relative priority
- **Emerging Threat Monitoring**: Surveillance teams track diseases with increasing trends
- **Stakeholder Communication**: Visual evidence for transparent prioritization

**Interactive Features Value**:
- **Weight sliders**: Show how different priorities (volume vs. trend) affect rankings
- **Disease comparison**: Understand trade-offs between different diseases
- **Filtering**: Focus on specific disease categories or priority tiers

**Expected Insights**:
- **Top priorities**: HFMD, Dengue, Salmonellosis likely in top 5
- **Emerging threats**: Diseases with high CAGR but currently lower volume
- **Stable endemic**: High volume but stable trends (sustained effort needed)
- **Declining success stories**: Diseases with decreasing trends (effective control)

**Stakeholder Engagement**:
- Demo dashboard to policy makers and program managers
- Gather feedback on usability and desired features
- Iterate based on user needs
- Use dashboard in budget planning meetings

**Dashboard Maintenance**:
- **Annual refresh**: Update with new surveillance data each year
- **Weight review**: Revisit weighting scheme every 2-3 years
- **Feature enhancements**: Add new visualizations based on stakeholder requests

**Technical Considerations**:
- **Databricks**: Easier for MOH internal users with existing access
- **Dash web app**: More flexible; requires hosting and security setup
- **Performance**: Optimize for fast load times; pre-compute heavy calculations
