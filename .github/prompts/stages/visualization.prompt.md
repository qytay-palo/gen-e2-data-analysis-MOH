---
description: Visualization and Reporting Stage with MCP Integration
stage: Visualization & Reporting
---

# Stage Prompt: Visualization and Reporting

## Objective

Create compelling visualizations and comprehensive reports that communicate analysis findings to stakeholders. Leverage MCP tools for efficient data access, visualization generation, and report delivery.

## Required MCP Tools

- **Filesystem Server** (REQUIRED): For reading analysis results, saving visualizations, and creating report outputs
- **SQLite Server** (when applicable): For querying data for visualizations directly from databases

## Input Requirements

The following inputs MUST be available before proceeding:

1. **Analysis Results**: 
   - `results/tables/{epic_id}/` - Summary statistics, analytical tables
   - `results/metrics/{epic_id}_metrics.json` - KPIs and performance metrics
   - `notebooks/2_analysis/{epic_id}/` - Analysis notebooks with findings

2. **Data for Visualization**:
   - `data/4_processed/{epic_id}/` - Clean datasets
   - `data/3_interim/{epic_id}/` - Intermediate processed data
   - Database tables (if using SQLite)

3. **Reporting Requirements**: From user story or stakeholder specs
   - Target audience (executives, analysts, clinicians)
   - Report format (dashboard, PDF, presentation)
   - Key messages to convey
   - Deadline and delivery format

4. **Design Specifications**:
   - Brand colors and style guide (if applicable)
   - Chart types required
   - Interactivity requirements
   - Accessibility requirements

## Output Requirements

The visualization and reporting MUST produce:

1. **Static Visualizations**: `reports/figures/{epic_id}/`
   - High-resolution charts and plots (PNG, PDF)
   - Publication-quality graphics (300 DPI)
   - Properly labeled with titles, axes, legends
   - Accessible color schemes

2. **Interactive Dashboards**: `reports/dashboards/{epic_id}/`
   - HTML dashboards (Plotly, Bokeh)
   - Power BI files (.pbix) if applicable
   - Streamlit/Dash apps
   - Jupyter Dashboard notebooks

3. **Reports**: `reports/presentations/{epic_id}/`
   - Executive summaries (PDF)
   - Slide decks (PPTX)
   - Technical reports (Markdown/PDF)
   - Infographics

4. **Visualization Documentation**: `reports/{epic_id}/visualization_guide.md`
   - Description of each visualization
   - Data sources and calculations
   - Interpretation guidance
   - Update procedures

## Execution Steps

### Step 1: Visualization Planning (using MCP filesystem tools)

```
1. Use filesystem tools to create visualization directories:
   - reports/figures/{epic_id}/
   - reports/dashboards/{epic_id}/
   - reports/presentations/{epic_id}/

2. Use filesystem tools to read analysis results:
   - Read results/metrics/{epic_id}_metrics.json
   - Read results/tables/{epic_id}/*.csv
   - Read analysis summary from results/{epic_id}/analysis_summary.md

3. Identify key findings to visualize:
   - Most important metrics and KPIs
   - Trends and patterns discovered
   - Comparisons and relationships
   - Outliers and anomalies

4. Select appropriate chart types for each finding
```

**Example MCP Commands**:
- "Use filesystem tools to create directory reports/figures/epic-001/"
- "Use filesystem tools to read results/metrics/epic-001_metrics.json"
- "Use filesystem tools to read results/epic-001/analysis_summary.md"

### Step 2: Time Series Visualizations (using MCP tools)

```
For temporal data and trends:

1. Line Charts:
   - Daily/weekly/monthly trends
   - Multiple series comparisons
   - Confidence intervals or prediction bands
   - Annotations for significant events

2. Area Charts:
   - Cumulative trends
   - Stacked area for composition over time
   - Fill between for ranges or thresholds

3. Heat Maps:
   - Day-of-week × Hour-of-day patterns
   - Calendar heatmaps for daily values
   - Correlation matrices over time

4. Apply best practices:
   - Clear title describing what is shown
   - X-axis: Time with appropriate granularity
   - Y-axis: Labeled with units
   - Legend if multiple series
   - Grid lines for readability
   - Appropriate date formatting

5. Use filesystem tools to save visualizations
```

**Example MCP Commands**:
- "Create line chart showing monthly emergency visit trends over 2 years"
- "Add confidence intervals and annotate flu season peaks"
- "Use filesystem tools to save to reports/figures/epic-001/monthly_visit_trends.png at 300 DPI"

### Step 3: Distribution Visualizations (using MCP tools)

```
For showing data distributions and spread:

1. Histograms:
   - Frequency distributions
   - Appropriate bin sizes (Sturges' rule or Freedman-Diaconis)
   - Overlay normal distribution curve if relevant

2. Box Plots:
   - Show median, quartiles, outliers
   - Compare distributions across groups
   - Violin plots for distribution shape

3. Density Plots:
   - Smooth distribution curves
   - Multiple overlapping distributions
   - Kernel density estimation (KDE)

4. Q-Q Plots:
   - Test for normality
   - Compare to theoretical distributions

5. Apply best practices:
   - Clear title and axis labels
   - Show sample sizes
   - Mark mean/median if relevant
   - Highlight outliers or thresholds
   - Use consistent color schemes

6. Use filesystem tools to save visualizations
```

**Example MCP Commands**:
- "Create box plot comparing wait times across 5 departments"
- "Use filesystem tools to save to reports/figures/epic-001/wait_time_distributions.png"

### Step 4: Comparison Visualizations (using MCP tools)

```
For comparing groups, categories, or time periods:

1. Bar Charts:
   - Vertical bars for categories
   - Horizontal bars for long labels
   - Grouped bars for multi-category comparison
   - Sorted by value for emphasis

2. Grouped/Stacked Bar Charts:
   - Compare multiple metrics across categories
   - Show composition within categories
   - Use stacking wisely (100% stacked for proportions)

3. Bullet Charts:
   - Performance vs targets
   - Show actual, target, and ranges
   - Compact comparison format

4. Small Multiples:
   - Same chart type for each category
   - Consistent scales for comparison
   - Faceted/panel charts

5. Apply best practices:
   - Start bars at zero
   - Maintain consistent colors across charts
   - Order categories meaningfully
   - Include data labels for precision
   - Show comparison baselines

6. Use filesystem tools to save visualizations
```

**Example MCP Commands**:
- "Create grouped bar chart comparing utilization rates across facilities and departments"
- "Use filesystem tools to save to reports/figures/epic-001/facility_utilization_comparison.png"

### Step 5: Relationship Visualizations (using MCP tools)

```
For showing correlations and relationships:

1. Scatter Plots:
   - Relationship between two variables
   - Add regression line or LOESS curve
   - Color points by category or third variable
   - Size points by magnitude

2. Correlation Heat Maps:
   - Show correlation coefficients
   - Use diverging color scheme (red-white-blue)
   - Annotate with correlation values
   - Hierarchical clustering of variables

3. Bubble Charts:
   - Three dimensions: X, Y, bubble size
   - Optional: color for fourth dimension
   - Include legend for bubble sizes

4. Network Diagrams:
   - Show relationships between entities
   - Node size by importance
   - Edge width by strength

5. Apply best practices:
   - Show correlation coefficient (R² value)
   - Include reference lines (y=x, trend)
   - Highlight significant relationships
   - Label outliers
   - Use transparency for overlapping points

6. Use filesystem tools to save visualizations
```

**Example MCP Commands**:
- "Create scatter plot of capacity vs wait time with regression line"
- "Use filesystem tools to save to reports/figures/epic-001/capacity_waittime_relationship.png"

### Step 6: Geographic Visualizations (using MCP tools)

```
For spatial data and geographic patterns:

1. Choropleth Maps:
   - Color regions by metric value
   - Use appropriate color scales
   - Include legend with value ranges
   - Label key regions

2. Point Maps:
   - Show facility locations
   - Size by metric (visits, capacity)
   - Color by category or performance

3. Heat Maps (Spatial):
   - Density of events or facilities
   - Hot spots and cold spots
   - Gradient overlay on map

4. Apply best practices:
   - Use appropriate map projection
   - Include scale and north arrow
   - Label major landmarks or regions
   - Choose colorblind-safe palettes
   - Provide context (boundaries, cities)

5. Use filesystem tools to save visualizations
```

**Example MCP Commands**:
- "Create choropleth map showing emergency visit rates by region"
- "Use filesystem tools to save to reports/figures/epic-001/regional_visit_rates_map.png"

### Step 7: Composition Visualizations (using MCP tools)

```
For showing part-to-whole relationships:

1. Pie Charts (use sparingly):
   - Maximum 5-7 slices
   - Order slices by size
   - Pull out most important slice
   - Show percentages

2. Donut Charts:
   - Similar to pie but with center space
   - Can show total in center
   - Better for multiple rings

3. Treemaps:
   - Hierarchical composition
   - Size by value
   - Color by category or metric
   - Interactive drill-down

4. Stacked Area Charts:
   - Composition over time
   - Show cumulative total
   - Smooth or stepped

5. Apply best practices:
   - Use only when showing parts of whole
   - Ensure parts add to 100%
   - Limit number of categories
   - Use bar charts if comparison needed
   - Include actual values, not just %

6. Use filesystem tools to save visualizations
```

**Example MCP Commands**:
- "Create treemap showing patient distribution by department and diagnosis category"
- "Use filesystem tools to save to reports/figures/epic-001/patient_distribution_treemap.png"

### Step 8: Statistical Visualizations (using MCP tools)

```
For statistical analysis results:

1. Confidence Interval Plots:
   - Show point estimates with error bars
   - 95% confidence intervals
   - Compare across groups

2. Forest Plots:
   - Meta-analysis style
   - Multiple studies or groups
   - Show effect sizes with CI

3. ROC Curves (for classification):
   - True positive vs false positive rate
   - Show AUC score
   - Diagonal reference line

4. Residual Plots:
   - Model diagnostics
   - Scatter of residuals
   - Q-Q plot of residuals

5. Apply best practices:
   - Show p-values or significance
   - Mark significance levels (*, **, ***)
   - Include sample sizes
   - Show statistical test used
   - Provide interpretation guide

6. Use filesystem tools to save visualizations
```

**Example MCP Commands**:
- "Create forest plot showing odds ratios with 95% CI for risk factors"
- "Use filesystem tools to save to reports/figures/epic-001/risk_factor_forest_plot.png"

### Step 9: Interactive Dashboard Creation (using MCP tools)

```
For dynamic, explorable visualizations:

1. Choose dashboard framework:
   - Plotly Dash (Python, web-based)
   - Streamlit (Python, rapid prototyping)
   - Power BI (business intelligence)
   - Jupyter Dashboard (notebook-based)
   - Bokeh (Python, interactive)

2. Dashboard components:
   - Filters and controls (dropdowns, sliders, date pickers)
   - Multiple linked charts (click-to-filter)
   - Metrics cards (KPIs, summary stats)
   - Data tables (sortable, filterable)
   - Update timestamp and refresh button

3. Dashboard layout:
   - Logical organization (top-to-bottom priority)
   - Responsive design (mobile-friendly)
   - Consistent styling
   - Clear navigation

4. Add interactivity:
   - Hover tooltips with details
   - Click to drill-down
   - Zoom and pan for time series
   - Cross-filtering between charts
   - Export functionality (CSV, image)

5. Use filesystem tools to save dashboard files
```

**Example MCP Commands**:
- "Create Streamlit dashboard with emergency department metrics"
- "Add filters for date range, department, and facility"
- "Use filesystem tools to save to reports/dashboards/epic-001/ed_metrics_dashboard.py"

### Step 10: Executive Reports and Presentations (using MCP tools)

```
For stakeholder communication:

1. Executive Summary (1-2 pages):
   - Key findings (3-5 bullet points)
   - Most important visualizations (2-3)
   - Recommendations (actionable steps)
   - Next steps

2. Slide Deck:
   - Title slide (project name, date, authors)
   - Agenda/outline
   - Background and objectives (1-2 slides)
   - Methodology (1 slide)
   - Key findings with visualizations (5-8 slides)
   - Recommendations (2-3 slides)
   - Appendix (detailed tables, technical notes)

3. Technical Report:
   - Complete methodology
   - All visualizations with descriptions
   - Statistical test results
   - Limitations and caveats
   - References and data sources

4. Infographic (for broader audience):
   - Visual storytelling
   - Minimal text, maximum impact
   - Key numbers highlighted
   - Simple, clean design

5. Use filesystem tools to save reports
```

**Example MCP Commands**:
- "Create executive summary PDF for emergency department analysis"
- "Use filesystem tools to save to reports/presentations/epic-001/ed_executive_summary.pdf"

### Step 11: Accessibility and Quality Checks (using MCP tools)

```
Ensure visualizations are accessible and high quality:

1. Color Accessibility:
   - Use colorblind-safe palettes (viridis, ColorBrewer)
   - Don't rely on color alone (use shapes, patterns)
   - Sufficient contrast ratios (WCAG standards)
   - Test with colorblind simulators

2. Text Accessibility:
   - Minimum font size 10pt for print, 12pt for screens
   - High contrast text on backgrounds
   - Clear, readable fonts (avoid decorative fonts)
   - Alt text for all visualizations

3. Data Integrity:
   - Verify data accuracy (spot check values)
   - Consistent units across visualizations
   - Correct calculations (double-check formulas)
   - Appropriate precision (decimal places)

4. Design Quality:
   - Remove chart junk (unnecessary decorations)
   - Maximize data-ink ratio
   - Consistent styling across all charts
   - Professional appearance

5. Use filesystem tools to verify all files created
```

**Example MCP Commands**:
- "Verify all visualizations use colorblind-safe palette"
- "Use filesystem tools to list all PNG files and check they are 300 DPI"

### Step 12: Documentation and Delivery (using MCP filesystem tools)

```
1. Create visualization guide:
   - Title and description for each visualization
   - Data source and date range
   - Calculation methods
   - Interpretation notes
   - Update procedures for reproducibility

2. Organize deliverables:
   - Group by type (static, interactive, reports)
   - Consistent naming convention
   - Version control (include dates)
   - README for navigation

3. Package for delivery:
   - Create ZIP archive if needed
   - Include data dictionaries
   - Include reproduction scripts
   - Include update instructions

4. Use filesystem tools to write documentation
```

**Example MCP Commands**:
- "Create visualization guide documenting all 15 charts"
- "Use filesystem tools to write to reports/epic-001/visualization_guide.md"
- "Use filesystem tools to list all deliverables in reports/epic-001/"

### Step 13: Verification (using MCP filesystem tools)

```
1. Verify all required outputs were created:
   - Use filesystem tools to list files in reports/figures/{epic_id}/
   - Use filesystem tools to list files in reports/dashboards/{epic_id}/
   - Use filesystem tools to list files in reports/presentations/{epic_id}/

2. Verify visualization quality:
   - All images at required resolution (300 DPI for print)
   - All charts properly labeled
   - All interactive dashboards functional
   - All reports complete with findings

3. Cross-check against acceptance criteria from user story

4. Document verification results
```

**Example MCP Commands**:
- "Use filesystem tools to list all PNG files in reports/figures/epic-001/ and show file sizes"
- "Use filesystem tools to verify visualization_guide.md exists and contains all visualizations"

## Visualization Best Practices

### 1. Choose the Right Chart Type
```
Time series → Line chart
Distribution → Histogram, box plot
Comparison → Bar chart
Relationship → Scatter plot
Composition → Stacked bar, treemap
Geographic → Choropleth map, point map
```

### 2. Design Principles
```
✅ Maximize data-ink ratio
✅ Use consistent colors and styling
✅ Start axes at zero (for bar charts)
✅ Label everything clearly
✅ Include data sources and timestamps
❌ Avoid 3D charts (distort perception)
❌ Avoid pie charts (hard to compare)
❌ Don't overload with information
```

### 3. Storytelling with Data
```
✅ Lead with the key message
✅ Guide the viewer's attention
✅ Use annotations to highlight insights
✅ Provide context (benchmarks, targets)
✅ End with actionable recommendations
```

## Quality Checks

After visualization creation, perform these quality checks:

### 1. Visual Quality
```
- High resolution (300 DPI for print)
- Clear and readable text
- Consistent styling and colors
- Professional appearance
```

### 2. Data Accuracy
```
- Values match source data
- Calculations are correct
- Units are consistent
- Dates and time zones correct
```

### 3. Accessibility
```
- Colorblind-safe palettes
- Sufficient contrast
- Alt text provided
- Screen-reader friendly
```

### 4. Clarity
```
- Message is clear
- Labels are descriptive
- Legend is included
- Source is cited
```

## Error Handling

If visualization creation encounters issues:

1. **Use filesystem tools to write detailed error log** to `logs/errors/visualization_{epic_id}_{timestamp}.log`

2. **Document the specific issue**:
   - Which visualization failed
   - Error message
   - Data issues encountered
   - Suggested remediation

## Success Criteria

The visualization and reporting is considered successful when:

- ✅ All required visualizations created and saved to `reports/figures/{epic_id}/`
- ✅ Interactive dashboards (if applicable) saved to `reports/dashboards/{epic_id}/`
- ✅ Reports and presentations saved to `reports/presentations/{epic_id}/`
- ✅ Visualization guide documented in `reports/{epic_id}/visualization_guide.md`
- ✅ All visualizations are high quality, accurate, and accessible
- ✅ Key findings clearly communicated
- ✅ Acceptance criteria from user story met
- ✅ All outputs verified using MCP filesystem tools

## MCP Tools Usage Summary

```markdown
### MCP Tools Used

**Filesystem Server**:
- Directories created:
  - reports/figures/epic-001/
  - reports/dashboards/epic-001/
  - reports/presentations/epic-001/
- Files read:
  - results/metrics/epic-001_metrics.json
  - results/tables/epic-001/*.csv
  - data/4_processed/epic-001/*.csv
- Files written:
  - 15 static visualizations (PNG, 300 DPI)
  - 3 interactive dashboards (HTML, Python)
  - 2 reports (PDF, PPTX)
  - 1 visualization guide (Markdown)
- Verification: Listed all directories, confirmed file creation, validated resolutions
```

## Next Stage

After successful visualization, proceed to:
- **Stakeholder presentation**: Present findings to decision-makers
- **Implementation**: Act on recommendations
- **Monitoring**: Set up ongoing tracking and dashboards

## References

- Analysis Results: `results/{epic_id}/`
- Style Guide: `docs/style_guide.md` (if exists)
- User Story: `docs/objectives/user_stories/{epic_id}/`
- Project Structure: `README.md`
