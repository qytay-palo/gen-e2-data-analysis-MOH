# PS-002: Disease Burden Assessment & Resource Prioritization

```yaml
problem_statement_id: PS-002
title: Disease Burden Assessment & Resource Prioritization
analysis_category: Descriptive
dependencies: None
```

---

## Problem Statement (Executive Summary)

Currently, MOH policy makers struggle to objectively prioritize resource allocation across 45 different infectious disease programs due to lack of comprehensive burden assessment that considers multiple dimensions (case volume, growth trends, outbreak frequency, seasonality). By conducting systematic disease burden analysis using 9 years of surveillance data across multiple metrics, we can enable evidence-based budget allocation and program prioritization decisions, resulting in optimized resource distribution aligned with actual disease impact and improved public health outcomes through targeted interventions on highest-burden diseases.

---

## Problem Statement Hypothesis

We believe that creating a comprehensive disease burden ranking framework for MOH policy makers will enable evidence-based prioritization of infectious disease programs and resource allocation. We'll know we're successful when we see:
- Policy makers citing burden analysis results in budget allocation decisions
- Clear consensus on top 10-15 priority diseases based on data (replacing subjective assessments)
- Measurable shift in resource allocation toward evidence-identified high-burden diseases
- Stakeholder confidence in prioritization methodology and transparency in criteria

---

## Objectives

1. **Quantify disease burden across multiple dimensions** including case volume, growth rate, outbreak frequency, and seasonal intensity for all 45 diseases
2. **Develop composite prioritization framework** that ranks diseases using weighted multi-criteria scoring system aligned with MOH strategic goals
3. **Identify emerging threats and declining diseases** through trend analysis to inform program expansion or reduction decisions
4. **Enable transparent, defensible resource allocation** through data-driven prioritization that stakeholders understand and trust

---

## Problem Statement Acceptance Criteria

- ✅ Disease burden rankings validated by epidemiologists and accepted by policy leadership
- ✅ Prioritization methodology clearly documented with rationale for weighting criteria
- ✅ Resource allocation recommendations directly inform next budget cycle planning
- ✅ Stakeholders can articulate why top-priority diseases matter and justify funding decisions
- ✅ Framework is reproducible and can be updated annually as new surveillance data arrives

---

## Stakeholders and Value Proposition

**Primary Stakeholders:**
- MOH Policy Makers & Strategic Planning Teams (Budget Allocation)
- Disease Control Program Managers (Program Justification)
- Public Health Surveillance Leadership (Monitoring Strategy)
- Healthcare Finance Committees (Cost-Benefit Analysis)

**Business Value:**
- **Decision enabled**: Objective prioritization of disease programs for budget allocation
- **Efficiency gain**: Focus resources on highest-impact diseases (avoid spreading thin)
- **Quality improvement**: Better population health outcomes through targeted interventions
- **Risk reduction**: Early identification of emerging disease threats
- **Accountability**: Transparent, data-driven justification for funding decisions to Parliament/public

---

## Data Requirements

**Critical Considerations:**
- **Data availability**: ✅ Weekly surveillance data for 45 diseases (2012-2020, 470 weeks) documented in data_sources.md
- **Data completeness**: ✅ 100% complete, all diseases reported consistently throughout period
- **Data quality concerns**: ✅ Standardized official surveillance data, validated by MOH
- **Privacy/security considerations**: ✅ Aggregated counts (no individual data), public health surveillance exception

**Data Sources Used:**
- Primary: `weekly-infectious-disease-bulletin-cases.csv`
  - All 45 diseases with weekly case counts (2012-2020)
  - Key metrics derivable: total cases, average weekly rate, peak cases, outbreak frequency, growth rates
  - Diseases range from high-burden (Dengue: 126,642 cases) to rare (various diseases <100 total cases)

**Note**: Business stakeholders need understand data spans 2012-2020 surveillance. Detailed statistical calculations and outbreak definitions will be developed during Sprint 1 exploration.

---

## Initial Considerations

**Analytical Approach:**
- Descriptive epidemiological analysis across multiple burden metrics
- Comparative analysis to identify relative importance and trends
- Clustering/segmentation to group diseases by characteristics (high-volume/low-outbreak vs. low-volume/high-severity)
- Sensitivity analysis on weighting criteria to test robustness of rankings
- Visualization of burden across multiple dimensions for stakeholder communication

**Feasibility Check:** (Reference: [tech_stack.md](../../project_context/tech-stack.md))
- ✅ **Achievable with current stack**:
  - Python/R on Databricks or CDSW for data analysis
  - Standard analytics libraries (pandas, numpy, matplotlib, seaborn)
  - STATA available for epidemiological rate calculations if needed
  - Spark available for processing if dataset grows
- ✅ **No specialized tools required**
- ✅ **Platform choice**: Recommend Databricks for collaborative notebook development and visualization

**Constraints:**
- Burden assessment based solely on case counts (no severity/mortality data available)
- National-level only (cannot assess geographic distribution of burden)
- Limited to notifiable diseases (excludes non-reportable conditions)

---

## Expected Outcomes and Deliverables

**Stakeholder Outcomes:**
- Outcome 1: Policy makers can justify budget allocations with evidence-based disease rankings
- Outcome 2: Disease program managers understand their program's relative priority and can advocate accordingly
- Outcome 3: Strategic planning teams identify emerging threats requiring new program investment
- Outcome 4: Finance committees have transparent methodology for evaluating program funding requests

**Concrete Deliverables:**

1. **📊 Disease Burden Dashboard** (Interactive)
   - Ranked list of all 45 diseases across multiple metrics
   - Interactive filters (sort by different criteria, time period selection)
   - Visualizations: burden heatmap, trend lines, outbreak timeline
   - Downloadable rankings for budget planning documents

2. **📋 Prioritization Framework Report** (Analytical)
   - Multi-criteria scoring methodology with rationale
   - Top 15 priority diseases with detailed profiles
   - Emerging threats analysis (diseases with increasing trends)
   - Recommendations for program expansion/reduction
   - Executive summary (2-3 pages) for leadership

3. **📈 Disease Profile Cards** (Reference)
   - One-page profile for each of top 15 diseases
   - Key metrics: total cases, trends, seasonality, outbreak history
   - Comparison to other diseases (percentile ranking)
   - Visual risk indicators (traffic light system)

4. **📑 Annual Update Methodology** (Reproducible)
   - Python/R scripts to regenerate rankings with new data
   - Documentation for maintaining framework over time
   - Template for annual burden assessment reports

**Delivery Format:**
- Dashboard: Databricks notebook or Tableau (interactive, accessible to stakeholders)
- Report: PDF with executive summary + technical appendix
- Profile cards: PowerPoint deck for budget presentation
- Methodology: Version-controlled code + documentation

---

## Dependencies and Assumptions

**Problem Statement Dependencies:**
- Depends on: **None** (independent analysis)
- Blocks: **None** (but informs PS-003 resource optimization)
- Related to: PS-001 (forecasting may use burden rankings to prioritize forecast development)

**Key Assumptions:**
- **Case counts reflect burden**: Assume reported cases are reasonable proxy for disease burden (acknowledging underreporting varies by disease)
- **Weighting criteria**: Assume policy makers value high case volume, increasing trends, and outbreak frequency as primary burden indicators
- **Stakeholder engagement**: Assume policy makers will engage in defining/validating weighting criteria during Sprint 1
- **Annual updates**: Assume MOH wants repeatable annual assessment (not one-time analysis)

**External Factors:**
- Public/political attention on specific diseases (e.g., Zika outbreak) may override data-driven priorities
- International disease threats (e.g., pandemic preparedness) require consideration beyond domestic surveillance data
- Severity and mortality data (not available in this dataset) may shift priorities if incorporated

---

## Risks and Open Questions

**Potential Blockers:**
- **Risk**: Case counts alone may not capture severity (e.g., rare but deadly disease ranks low)
  - *Mitigation*: Include outbreak frequency and peak magnitude; document limitations; recommend incorporating severity data if available
- **Risk**: Stakeholder disagreement on weighting criteria (volume vs. growth vs. outbreak frequency)
  - *Mitigation*: Conduct sensitivity analysis showing rankings under different weighting schemes; facilitate stakeholder workshop to build consensus
- **Risk**: Rankings may challenge existing program funding (political resistance)
  - *Mitigation*: Frame as decision support tool (not mandate); emphasize transparency and evidence-based approach

**Open Questions:**
- Should weighting criteria differ for resource types (e.g., surveillance vs. treatment programs)?
- How to incorporate diseases with short-term spikes (e.g., Zika 2016) vs. sustained burden?
- Should endemic diseases (consistently present) be weighted differently than epidemic-prone diseases?
- How to account for prevention program success (e.g., low case count because vaccination works)?

---

## Problem Statement Readiness

**This problem statement is ready for refinement session when:**
- [x] Problem statement validated with key stakeholders (policy makers, program managers identified)
- [x] Data sources explicitly listed from data_sources.md (`weekly-infectious-disease-bulletin-cases.csv`)
- [x] Business value and acceptance criteria clear (evidence-based prioritization, transparent methodology)
- [x] No critical blockers prevent team from starting exploration (data available, tools confirmed)

**Status**: ✅ **READY FOR SPRINT PLANNING**

**Recommended Sprint 1 Focus:**
- Calculate basic burden metrics for all 45 diseases (total cases, trends, peaks)
- Stakeholder workshop: Define/validate burden criteria and weighting preferences
- Prototype ranking visualization with multiple sorting options
- Identify diseases with interesting patterns for detailed profiling

**When to Update:**
- ✅ Annual update when new surveillance data available
- ✅ If severity/mortality data becomes available (major enhancement)
- ✅ Stakeholder feedback on weighting criteria after first use in budget cycle
- ✅ New diseases added to surveillance or existing diseases de-notified

**Continuous Improvement:**
- Review methodology annually before budget cycle
- Incorporate stakeholder feedback on usability and decision usefulness
- Consider expanding to include economic burden (healthcare costs) if data available
