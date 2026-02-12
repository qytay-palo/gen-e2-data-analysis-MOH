# User Story: 3 - Correlate Workforce Capacity with Disease Burden

**As a** healthcare capacity planner,
**I want** to analyze the relationship between healthcare workforce levels and infectious disease burden over time,
**so that** I can assess whether workforce capacity is aligned with population health needs and identify gaps.

## 1. 🎯 Acceptance Criteria

1. **Workforce-to-Disease-Burden Ratios Calculated**
   - Workforce per 1,000 disease cases calculated for each profession
   - Ratios analyzed over time (2012-2019, overlap period with disease data)
   - Correlation between workforce growth and disease burden assessed
   - Adequacy benchmarks defined or researched

2. **Disease Burden Integration**
   - Total infectious disease cases aggregated by year (2012-2019)
   - High-burden diseases (Dengue, HFMD, Salmonellosis) analyzed specifically
   - Outbreak year impacts on workforce adequacy assessed
   - Seasonal demand patterns considered

3. **Capacity Gap Analysis**
   - Periods of potential workforce shortfall identified
   - Workforce adequacy during peak disease years assessed
   - Gap quantified (if workforce-to-burden ratio falls below threshold)
   - Profession-specific gaps highlighted (e.g., nurses during outbreaks)

4. **Correlation Analysis Report**
   - Statistical correlation between workforce and disease burden documented
   - Visualizations showing workforce vs. disease trends
   - Key insights on workforce-disease alignment
   - Recommendations for capacity optimization

## 2. 🔒 Technical Constraints

- **Data Integration**: Combine annual workforce data with aggregated disease surveillance data
- **Time Period**: Analysis limited to 2012-2019 (overlap of both datasets)
- **Statistical Methods**: Correlation analysis, ratio calculations, threshold-based gap assessment
- **Output**: Integrated analysis report

## 3. 📚 Domain Knowledge References

- [Healthcare Workforce Metrics and KPIs](../../../domain_knowledge/healthcare-workforce-metrics-kpis.md) - Workforce-to-disease-burden ratios, capacity metrics
- [Disease Burden Assessment Methodology](../../../domain_knowledge/disease-burden-assessment-methodology.md) - Disease burden metrics
- [Infectious Disease Epidemiology Terminology](../../../domain_knowledge/infectious-disease-epidemiology-terminology-glossary.md) - Disease burden interpretation

**Key Metrics**:
- **Workforce-to-Disease-Burden Ratio**: Healthcare workers per 1,000 disease cases
- **Correlation Coefficient**: Measure of relationship between workforce growth and disease burden changes
- **Capacity Adequacy**: Assess whether workforce scales appropriately with disease burden

## 4. 📦 Dependencies

**External Packages**:
- `polars` - Data integration and calculations
- `scipy` - Correlation analysis, statistical tests
- `matplotlib` / `seaborn` - Visualization

**Internal Dependencies**:
- Workforce datasets from User Stories 1 and 2
- Disease surveillance data (from PS-001/PS-002 analysis)
- Disease burden metrics (total cases, outbreak frequencies)

## 5. ✅ Implementation Tasks

### Data Integration
- ⬜ Aggregate disease surveillance data to annual totals (2012-2019)
- ⬜ Calculate total infectious disease cases per year
- ⬜ Identify high-burden disease years (e.g., 2013 Dengue outbreak)
- ⬜ Merge workforce data with annual disease burden data

### Workforce-to-Burden Ratio Calculation
- ⬜ Calculate doctors per 1,000 infectious disease cases
- ⬜ Calculate nurses per 1,000 infectious disease cases
- ⬜ Calculate pharmacists per 1,000 infectious disease cases
- ⬜ Analyze ratio trends over time (2012-2019)

### Disease-Specific Analysis
- ⬜ Focus on high-burden diseases (Dengue, HFMD, Salmonellosis)
- ⬜ Calculate workforce-to-burden ratios for specific disease categories
- ⬜ Analyze workforce adequacy during outbreak years vs. normal years
- ⬜ Identify disease-specific workforce needs

### Correlation Analysis
- ⬜ Calculate Pearson correlation between workforce growth and disease burden growth
- ⬜ Test correlation significance (p-values)
- ⬜ Analyze time-lagged correlations (workforce growth preceding/following disease burden changes)
- ⬜ Compare correlations across professions

### Capacity Gap Assessment
- ⬜ Define workforce adequacy thresholds (research-based or stakeholder-defined)
- ⬜ Identify years where workforce-to-burden ratio falls below threshold
- ⬜ Quantify capacity gaps (shortfall in workforce relative to disease burden)
- ⬜ Assess profession-specific gaps (e.g., nursing shortages during outbreaks)

### Scenario Analysis
- ⬜ Model workforce needs for different disease burden scenarios
- ⬜ Estimate workforce required for 10%, 20% increase in disease burden
- ⬜ Assess impact of outbreak years on workforce adequacy
- ⬜ Project future workforce needs based on disease burden forecasts (if available from PS-001)

### Visualization
- ⬜ Create dual-axis plots (workforce and disease burden over time)
- ⬜ Generate scatter plots (workforce vs. disease burden with correlation)
- ⬜ Build ratio trend line charts
- ⬜ Create capacity gap visualizations (years with shortfalls)

### Report Generation
- ⬜ Write correlation analysis report with key findings
- ⬜ Document workforce-disease burden alignment
- ⬜ Highlight capacity gaps and implications
- ⬜ Provide recommendations for workforce scaling

## 6. Notes

**Analysis Rationale**:
This analysis addresses a key question: **Is healthcare workforce growing proportionally with disease burden?** If workforce is static but disease burden increases, capacity gaps emerge.

**Expected Insights**:
- **Positive correlation**: Workforce growth should ideally track with disease burden growth (proactive planning)
- **Negative correlation or no correlation**: May indicate reactive workforce planning or inadequate scaling
- **Outbreak years**: 2013 Dengue outbreak, 2016 Zika outbreak should show workforce strain

**Capacity Adequacy Thresholds**:
No universal standard for workforce-to-disease-burden ratio exists. Options:
1. **Benchmark to best year**: Use year with lowest case-to-workforce ratio as target
2. **Stakeholder-defined**: Healthcare operations managers define acceptable thresholds
3. **International comparison**: Research similar healthcare systems' ratios

**Limitations**:
- **Causality unclear**: Correlation doesn't imply causation; workforce growth may be driven by factors other than disease burden (population growth, aging, chronic diseases)
- **Annual granularity**: Can't analyze seasonal workforce-disease mismatches within years
- **Profession-specific**: Different professions have different roles in infectious disease management (nurses more directly involved than pharmacists)

**Implications for Workforce Planning**:
- **Proactive scaling**: If workforce-to-burden ratio declining, increase recruitment
- **Surge capacity**: Outbreak years require temporary staffing augmentation
- **Specialization**: Consider infectious disease specialist workforce (subset of doctors)
- **Allied health**: Analysis limited to three professions; allied health (lab techs, epidemiologists) also critical

**Integration with PS-001 Forecasts**:
If disease burden forecasts available from PS-001 (Dengue, HFMD predictions), can project future workforce needs:
- "Forecast predicts 20% increase in Dengue cases → Need X% more nurses to maintain workforce-to-burden ratio"
