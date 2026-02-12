# PS-003: Healthcare Workforce Capacity Planning & Optimization

```yaml
problem_statement_id: PS-003
title: Healthcare Workforce Capacity Planning & Optimization
analysis_category: Prescriptive
dependencies: None
```

---

## Problem Statement (Executive Summary)

Currently, MOH workforce planning teams struggle to project future healthcare workforce needs (doctors, nurses, pharmacists) to meet evolving disease burden and population health demands, often relying on linear extrapolations that don't account for workforce trends, sectoral shifts (public vs. private), or changing disease epidemiology. By analyzing 13+ years of workforce data (2006-2019) alongside disease surveillance trends, we can develop evidence-based workforce capacity recommendations that optimize staffing across healthcare sectors, resulting in reduced workforce shortages during peak demand periods, improved healthcare system resilience, and better alignment of workforce distribution with population health needs.

---

## Problem Statement Hypothesis

We believe that integrating workforce trend analysis with disease burden patterns for MOH workforce planning teams and healthcare facility administrators will enable proactive capacity planning and optimize workforce allocation across public and private sectors. We'll know we're successful when we see:
- Workforce projections used in multi-year hiring and training pipeline planning
- Measurable improvement in workforce-to-burden alignment (e.g., infectious disease nurses scaled to anticipated case volumes)
- Reduction in workforce shortage incidents during predictable disease peak periods
- Evidence-based recommendations informing policy discussions on workforce immigration, training slots, and retention programs

---

## Objectives

1. **Analyze workforce supply trends** across healthcare professions (doctors, nurses, pharmacists) and sectors (public vs. private) to identify gaps and growth patterns
2. **Correlate workforce capacity with disease burden** to assess adequacy of current staffing and project future needs based on epidemiological trends
3. **Identify workforce distribution imbalances** across sectors and specialties that may impact outbreak response and routine care capacity
4. **Develop capacity optimization recommendations** for workforce allocation, training priorities, and recruitment strategies aligned with anticipated disease burden

---

## Problem Statement Acceptance Criteria

- ✅ Workforce projections validated by HR leadership and clinical operations managers
- ✅ Capacity gap analysis clearly identifies shortfall areas (profession, sector, timeframe)
- ✅ Recommendations directly inform workforce development strategies (training slots, immigration quotas, retention incentives)
- ✅ Analysis integrates with infectious disease burden findings to show workforce-disease alignment
- ✅ Reproducible methodology enables annual workforce needs assessment updates

---

## Stakeholders and Value Proposition

**Primary Stakeholders:**
- MOH Workforce Planning & Development Teams (Strategic Planning)
- Healthcare Facility HR & Operations Managers (Staffing Optimization)
- Medical/Nursing Education Institutions (Training Pipeline Planning)
- Healthcare Sector Regulators (Licensing & Immigration Policy)
- MOH Finance Committees (Workforce Budget Allocation)

**Business Value:**
- **Decision enabled**: Evidence-based workforce recruitment, training, and retention strategies
- **Efficiency gain**: Optimize workforce distribution across public/private sectors to reduce shortages
- **Quality improvement**: Adequate staffing to maintain care quality during disease outbreaks
- **Risk reduction**: Proactive identification of workforce gaps before shortages become critical
- **Financial impact**: Informed budget planning for workforce costs (largest healthcare expenditure category)

---

## Data Requirements

**Critical Considerations:**
- **Data availability**: ✅ Multiple workforce datasets spanning 2006-2019 documented in data_sources.md
  - Doctors: 78 records (2006-2019)
  - Nurses & Midwives: 126 records (2008-2019)
  - Pharmacists: 42 records (2006-2019)
- **Data completeness**: ✅ 100% complete, annual breakdowns by sector (public, private, not-for-profit)
- **Data quality concerns**: ✅ Official workforce registry data from MOH
- **Privacy/security considerations**: ✅ Aggregated counts by sector (no individual identifiers)

**Data Sources Used:**
- Primary Workforce Data:
  - `number-of-doctors.csv` (2006-2019, by sector and year)
  - `number-of-nurses-and-midwives.csv` (2008-2019, by sector and year)
  - `number-of-pharmacists.csv` (2006-2019, by sector and year)
- Secondary (for context):
  - `weekly-infectious-disease-bulletin-cases.csv` (2012-2020) - to correlate workforce with disease burden
  - `health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private.csv` - to assess workforce-to-bed ratios

**Note**: Annual granularity only (no monthly/seasonal workforce data). Detailed workforce-to-population ratios and international benchmarking will be explored during Sprint 1.

---

## Initial Considerations

**Analytical Approach:**
- Time series analysis of workforce growth trends across professions and sectors
- Comparative analysis of workforce distribution (public vs. private sector shifts)
- Ratio analysis (workforce-to-population, workforce-to-beds, workforce-to-disease-burden)
- Projection modeling using historical trends and scenario analysis
- Benchmarking against international standards (e.g., WHO recommendations)
- Integration with disease burden findings from PS-002

**Feasibility Check:** (Reference: [tech_stack.md](../../project_context/tech-stack.md))
- ✅ **Achievable with current stack**:
  - Python/R on Databricks or CDSW for analysis
  - Standard analytics libraries (pandas, statsmodels, scikit-learn)
  - STATA available for econometric modeling of workforce trends
  - Visualization tools for stakeholder communication
- ✅ **No specialized tools required**
- ✅ **Platform choice**: Recommend Databricks for collaborative analysis and report generation

**Constraints:**
- Annual data only (cannot analyze seasonal workforce fluctuations)
- National aggregates (no facility-level or regional workforce distribution)
- Data ends 2019 (workforce impacts of COVID-19 not captured)
- Limited to three professions (doctors, nurses, pharmacists) - other roles (allied health, techs) not available

---

## Expected Outcomes and Deliverables

**Stakeholder Outcomes:**
- Outcome 1: Workforce planning teams can project staffing needs for 3-5 year planning horizon
- Outcome 2: HR managers understand sector-specific workforce trends and competitive dynamics (public vs. private)
- Outcome 3: Education institutions align training capacity with projected workforce gaps
- Outcome 4: Policy makers have evidence base for workforce immigration and retention policies
- Outcome 5: Finance teams can forecast workforce-related expenditures with greater accuracy

**Concrete Deliverables:**

1. **📊 Workforce Capacity Dashboard** (Interactive)
   - Historical trends (2006-2019) across all professions and sectors
   - Workforce-to-population ratios with benchmarks
   - Workforce-to-disease-burden correlations
   - Projected capacity needs (3-5 year scenarios)
   - Gap analysis highlighting shortage areas

2. **📋 Capacity Optimization Report** (Analytical)
   - Workforce supply and demand analysis
   - Sector distribution trends (public/private migration patterns)
   - Correlation between workforce levels and disease burden
   - International benchmarking (Singapore vs. comparable healthcare systems)
   - Recommendations for workforce development strategies
   - Executive summary for leadership (3-5 pages)

3. **📑 Workforce Development Recommendations** (Prescriptive)
   - Priority areas for recruitment (profession, sector)
   - Training pipeline recommendations (medical/nursing school slots)
   - Retention strategy priorities (professions with high attrition)
   - Immigration policy considerations (foreign healthcare worker needs)
   - Resource allocation framework for workforce programs

4. **📈 Annual Update Framework** (Reproducible)
   - Python/R scripts for rerunning analysis with new workforce data
   - Documentation for maintaining projections
   - Template for annual workforce needs assessment

**Delivery Format:**
- Dashboard: Databricks notebook or Tableau for interactive exploration
- Report: PDF with executive summary + detailed analysis + technical appendix
- Recommendations: PowerPoint presentation for workforce planning committees
- Framework: Version-controlled code + methodology documentation

---

## Dependencies and Assumptions

**Problem Statement Dependencies:**
- Depends on: **None** (independent analysis, though enriched by PS-002 disease burden findings)
- Blocks: **None**
- Related to: PS-002 (disease burden informs workforce demand projections)

**Key Assumptions:**
- **Workforce trends continuity**: Assume historical growth/attrition patterns reasonably predict near-term future (absent major policy changes)
- **Disease burden correlation**: Assume workforce needs scale with infectious disease burden (among other factors)
- **Sector mobility**: Assume healthcare workers can shift between public/private sectors based on capacity needs
- **Stakeholder engagement**: Assume workforce planning teams and HR managers will engage in validating projections and recommendations
- **Data updates**: Assume MOH continues annual workforce data collection with consistent methodology

**External Factors:**
- Immigration policy changes may significantly impact workforce supply (especially foreign healthcare workers)
- COVID-19 pandemic may have disrupted workforce trends post-2019 (not captured in data)
- Medical/nursing education capacity constraints may limit ability to address identified gaps
- Salary and working conditions influence workforce retention (data not available for analysis)

---

## Risks and Open Questions

**Potential Blockers:**
- **Risk**: Workforce projections may be inaccurate if major policy changes occur (e.g., immigration restrictions)
  - *Mitigation*: Scenario planning with multiple assumptions (e.g., base case, restricted immigration case, expanded training case)
- **Risk**: Limited to three professions; may miss gaps in allied health professionals, technicians, support staff
  - *Mitigation*: Document limitations; recommend expanding analysis if additional workforce data becomes available
- **Risk**: National aggregates hide facility-level or regional workforce maldistribution
  - *Mitigation*: Acknowledge limitation; recommend facility-level analysis if granular data available
- **Risk**: Stakeholder resistance if recommendations challenge existing workforce policies
  - *Mitigation*: Frame as decision support; use scenarios to show trade-offs; emphasize evidence-based approach

**Open Questions:**
- How to incorporate specialty/subspecialty needs (e.g., infectious disease specialists) vs. general workforce?
- Should projections account for population aging and chronic disease trends (beyond infectious disease focus)?
- How to model impact of technology/automation on future workforce needs (e.g., telemedicine, AI diagnostics)?
- What workforce productivity assumptions should be used (cases per clinician, patients per nurse)?
- How to balance workforce development recommendations with budget constraints?

---

## Problem Statement Readiness

**This problem statement is ready for refinement session when:**
- [x] Problem statement validated with key stakeholders (workforce planning teams, HR managers identified)
- [x] Data sources explicitly listed from data_sources.md (doctors, nurses, pharmacists datasets)
- [x] Business value and acceptance criteria clear (capacity projections, gap identification, evidence-based recommendations)
- [x] No critical blockers prevent team from starting exploration (data available, tools confirmed)

**Status**: ✅ **READY FOR SPRINT PLANNING**

**Recommended Sprint 1 Focus:**
- Calculate workforce growth rates and trends across professions and sectors
- Compute workforce ratios (per capita, per bed, per disease case) and compare to benchmarks
- Visualize sector distribution shifts (public vs. private) over time
- Stakeholder workshop: Define projection scenarios and validation criteria
- Prototype workforce dashboard with key metrics

**When to Update:**
- ✅ Annual update when new workforce data available (typically 1-2 year lag)
- ✅ Major policy changes (immigration, education capacity, workforce incentives)
- ✅ Significant healthcare system changes (major facility openings/closures)
- ✅ Post-pandemic workforce data becomes available (2020+)

**Continuous Improvement:**
- Review projections annually against actual workforce data (calibrate models)
- Gather feedback from workforce planning teams on usability and decision impact
- Incorporate additional professions if data becomes available
- Refine correlation models between workforce and disease burden as more data accumulates
