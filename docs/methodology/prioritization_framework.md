# Multi-Criteria Disease Burden Prioritization Framework

**Document Version**: 1.0  
**Last Updated**: 2026-02-12  
**Authors**: MOH Data Analytics Team  
**Review Cycle**: Annual

## Executive Summary

This document describes the Multi-Criteria Disease Burden Prioritization Framework developed to support evidence-based resource allocation decisions at the Ministry of Health (MOH). The framework employs a transparent, quantitative approach using weighted multi-criteria decision analysis (MCDA) to rank infectious diseases based on four key burden dimensions: volume, trend, outbreak propensity, and variability.

**Key Outcomes**:
- Ranked 27 diseases with sufficient surveillance data
- Identified 2 Medium Priority diseases (Dengue Fever, Hand-Foot-Mouth Disease)
- 6 diseases maintain Top 10 ranking across all weighting scenarios (consensus priorities)
- High ranking stability (mean Spearman correlation: 0.934) across sensitivity scenarios

## 1. Background & Objectives

### 1.1 Problem Statement

MOH manages surveillance and intervention programs for 44+ notifiable infectious diseases. Limited resources require strategic prioritization to maximize public health impact. Historically, prioritization has been subjective and vulnerable to recency bias following outbreaks.

### 1.2 Objectives

1. **Transparency**: Develop an explicit, defensible prioritization methodology
2. **Multi-Dimensional Assessment**: Capture disease burden across volume, trend, outbreak risk, and variability
3. **Reproducibility**: Enable annual updates with new surveillance data
4. **Stakeholder Engagement**: Provide framework for expert input on weighting schemes
5. **Sensitivity Analysis**: Test ranking robustness to alternative weighting assumptions

## 2. Methodology

### 2.1 Input Data Requirements

**Data Source**: Weekly Infectious Disease Bulletin surveillance data (2015-2023)

**Required Metrics** (per disease):
- `total_cases`: Cumulative cases over study period
- `annual_avg_cases`: Mean annual case count
- `cagr`: Compound Annual Growth Rate (%)
- `outbreak_frequency`: Number of weeks exceeding epidemic threshold
- `coefficient_variation`: Standard deviation / mean (volatility measure)
- `sufficient_data`: Boolean flag (requires ≥52 weeks of data, ≥10 total cases)

**Exclusion Criteria**:
- Diseases with <52 weeks of surveillance data
- Diseases with <10 total cases (insufficient for trend estimation)

**2023 Data Summary**:
- 44 diseases surveilled
- 27 diseases met inclusion criteria (61%)
- 17 diseases excluded (rare/emerging diseases with limited data)

### 2.2 Scoring Normalization

All raw metrics are normalized to 0-100 scale using min-max normalization:

```
normalized_score = ((value - min) / (max - min)) * 100
```

**Rationale**: Enables comparison across metrics with different units and ranges.

**Edge Cases**:
- If all values identical (max = min): assign score of 50
- Missing values: Disease excluded from analysis

### 2.3 Composite Score Calculation

**Base Case Weighting Scheme**:

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| **Volume** | 40% | Cases volume drives resource requirements (surveillance, diagnostics, treatment) |
| **Trend** | 25% | Emerging threats require proactive capacity building |
| **Outbreak** | 20% | Epidemic potential necessitates surge response capacity |
| **Variability** | 15% | Predictability enables efficient resource planning |

**Calculation**:
```
composite_score = (volume_criterion × 0.40) +
                  (trend_criterion × 0.25) +
                  (outbreak_criterion × 0.20) +
                  (variability_criterion × 0.15)
```

**Criteria Definitions**:

1. **Volume Criterion**: Average of `total_cases_score` and `annual_avg_cases_score`
   - Captures both cumulative and sustained burden

2. **Trend Criterion**: `cagr_score`
   - Higher scores indicate faster growth (emerging threats)
   - Captures temporal evolution of disease burden

3. **Outbreak Criterion**: `outbreak_score`
   - Based on frequency of epidemic threshold exceedance
   - Reflects unpredictable surge demand

4. **Variability Criterion**: `coefficient_variation_score`
   - Lower CV = more predictable = higher score (inverted scoring)
   - Enables efficient resource planning

### 2.4 Tier Assignment

Diseases are classified into three priority tiers based on composite score thresholds:

| Tier | Threshold | Interpretation | Recommended Action |
|------|-----------|----------------|-------------------|
| **High** | >70 | Extreme burden across multiple dimensions | Substantial resource allocation, enhanced surveillance, proactive intervention |
| **Medium** | 40-70 | Moderate burden requiring sustained attention | Maintained surveillance, responsive intervention capacity |
| **Low** | <40 | Limited burden or insufficient data | Basic surveillance, ad-hoc response as needed |

**Threshold Rationale**:
- Thresholds set to approximate tertile distribution in typical disease portfolios
- Can be adjusted based on budget constraints or strategic priorities
- Current data (2023): No High Priority diseases, 2 Medium (7.4%), 25 Low (92.6%)

### 2.5 Ranking Procedure

Diseases are ranked in descending order by `composite_score`. Ties are resolved using:
1. Higher `volume_criterion` (primary)
2. Higher `trend_criterion` (secondary)
3. Alphabetical order (tertiary)

**Stable Sorting**: Ensures reproducibility across repeated analyses.

## 3. Sensitivity Analysis

### 3.1 Alternative Weighting Scenarios

To assess ranking robustness, three alternative scenarios were tested:

#### Scenario 1: Volume-Focused (60/20/10/10)
- **Context**: Resource-constrained settings prioritizing current burden over future risk
- **Weights**: Volume 60%, Trend 20%, Outbreak 10%, Variability 10%
- **Expected Impact**: High-volume diseases (HFMD) rise in ranking

#### Scenario 2: Emerging Threat-Focused (30/50/15/5)
- **Context**: Proactive strategy emphasizing early detection of growing threats
- **Weights**: Volume 30%, Trend 50%, Outbreak 15%, Variability 5%
- **Expected Impact**: Rapidly growing diseases (Dengue Fever, Hepatitis C) prioritized

#### Scenario 3: Stability-Focused (30/20/30/20)
- **Context**: Emphasis on predictability and outbreak risk mitigation
- **Weights**: Volume 30%, Trend 20%, Outbreak 30%, Variability 20%
- **Expected Impact**: Outbreak-prone diseases (DHF, Measles) gain prominence

### 3.2 Rank Correlation Analysis

**Method**: Spearman rank correlation coefficient (ρ) between scenario pairs
- ρ = 1.0: Identical rankings
- ρ = 0.0: No correlation
- ρ = -1.0: Opposite rankings

**2023 Results**:

| Scenario Pair | Spearman ρ | Interpretation |
|---------------|-----------|----------------|
| Base vs Volume-Focused | 0.988 | Nearly identical |
| Base vs Emerging-Threat | 0.903 | High stability |
| Base vs Stability-Focused | 0.983 | Nearly identical |
| Volume vs Emerging-Threat | 0.922 | High stability |
| Volume vs Stability | 0.953 | Very high stability |
| Emerging vs Stability | 0.855 | Moderate-high stability |

**Mean Correlation**: 0.934 (very high stability)

**Interpretation**: Rankings are robust to weighting assumptions. Core priorities remain stable, with minor reordering at margins.

### 3.3 Consensus Priorities

**Definition**: Diseases appearing in Top 10 across all 4 scenarios (base case + 3 alternatives)

**2023 Consensus Top 10** (6 diseases):
1. Dengue Fever
2. Hand, Foot and Mouth Disease
3. Dengue Haemorrhagic Fever
4. Acute Viral Hepatitis B
5. Acute Viral Hepatitis C
6. Measles

**Strategic Implication**: These diseases warrant prioritization regardless of weighting philosophy. Resource allocation for these diseases is defensible under diverse strategic assumptions.

## 4. Results Interpretation

### 4.1 Top 10 Priority Diseases (Base Case)

| Rank | Disease | Score | Tier | Volume | Trend | Outbreak | Variability |
|------|---------|-------|------|--------|-------|----------|-------------|
| 1 | Dengue Fever | 49.4 | Medium | 53.8 | 98.7 | 13.5 | 3.3 |
| 2 | Hand, Foot & Mouth Disease | 42.8 | Medium | 100.0 | 0.0 | 12.7 | 2.0 |
| 3 | Dengue Haemorrhagic Fever | 31.4 | Low | 0.2 | 82.4 | 50.0 | 5.3 |
| 4 | Acute Viral Hepatitis C | 30.9 | Low | 0.1 | 100.0 | 18.8 | 14.1 |
| 5 | Measles | 26.7 | Low | 0.3 | 66.3 | 45.7 | 5.7 |
| 6 | Salmonellosis (non-enteric) | 24.6 | Low | 7.0 | 77.2 | 12.5 | 0.0 |
| 7 | Malaria | 23.9 | Low | 0.2 | 56.7 | 44.6 | 4.6 |
| 8 | Acute Viral Hepatitis B | 22.9 | Low | 0.2 | 73.3 | 19.8 | 3.7 |
| 9 | Melioidosis | 22.8 | Low | 0.2 | 78.5 | 12.9 | 3.9 |
| 10 | Paratyphoid | 22.7 | Low | 0.1 | 61.6 | 31.2 | 6.8 |

### 4.2 Key Findings

**1. Dual Leadership**: Dengue Fever (#1) and HFMD (#2) emerge as clear priorities
- Dengue: Driven by exceptional trend growth (98.7) and moderate volume (53.8)
- HFMD: Dominated by case volume (100.0) despite declining trend (0.0)

**2. No High Priority Diseases**: No disease exceeds 70-point threshold
- Possible explanations:
  - Effective surveillance programs reducing individual disease burdens
  - Need for threshold recalibration to match organizational risk appetite
  - Fragmented burden across multiple diseases rather than concentrated threats

**3. Emerging Threats**: Hepatitis C (rank #4) notable for maximal trend score (100.0)
- Low volume but rapid growth signals need for proactive capacity building

**4. Outbreak-Prone Diseases**: DHF (#3), Measles (#5), Malaria (#7) rank highly despite low volume
- High outbreak scores (45-50) reflect epidemic potential
- Require maintained surge response capacity

### 4.3 Recommendations by Tier

#### Medium Priority (2 diseases)
**Dengue Fever, HFMD**

Recommended Actions:
- Allocate substantial resources for sustained surveillance
- Maintain diagnostic and treatment capacity at high readiness
- Consider enhanced vector control (Dengue) and hygiene campaigns (HFMD)
- Annual budget allocation: 60-70% of infectious disease program

#### Low Priority (25 diseases)
**All other diseases**

Recommended Actions:
- Basic surveillance maintained
- Responsive intervention capacity (activated when thresholds breached)
- Opportunistic integration with related programs (e.g., vaccination for Measles)
- Annual budget allocation: 30-40% of infectious disease program distributed proportionally

## 5. Framework Maintenance

### 5.1 Annual Update Procedure

**Timing**: Q1 each year (after prior year surveillance data finalized)

**Steps**:
1. **Data Refresh**: Update burden metrics with new surveillance year
2. **Validation**: Check data quality (sufficient_data flags)
3. **Recalculation**: Rerun prioritization with base case weights
4. **Comparison**: Compare rankings to prior year; investigate major shifts
5. **Stakeholder Review**: Present findings to MOH leadership
6. **Publication**: Update methodology document and disseminate rankings

**Deliverables**:
- Updated `disease_priority_rankings.csv`
- Trend analysis comparing year-over-year ranking changes
- Executive summary for leadership

### 5.2 Weight Recalibration (Every 2-3 Years)

**Trigger Events**:
- Major policy shifts (e.g., new national health priorities)
- Significant epidemiological changes (e.g., pandemic, disease elimination)
- Stakeholder dissatisfaction with current rankings

**Process**:
1. **Stakeholder Workshop**: Convene epidemiologists, clinicians, program managers
2. **Delphi Method** or **Analytical Hierarchy Process (AHP)**: Elicit expert weights
3. **Sensitivity Analysis**: Test new weights against historical data
4. **Validation**: Confirm face validity of resulting rankings
5. **Documentation**: Update configuration files and methodology document

### 5.3 Threshold Adjustment

**Current Thresholds** (High: >70, Medium: 40-70, Low: <40) may require adjustment if:
- Budget constraints change (fewer resources → lower Medium threshold)
- Risk appetite evolves (higher risk tolerance → higher High threshold)
- Disease burden landscape shifts (e.g., elimination of high-burden disease)

**Recommended Approach**:
- Review tier distribution annually
- Target distribution: ~10-15% High, ~30-40% Medium, ~45-60% Low
- Adjust thresholds to approximate targets while maintaining face validity

## 6. Limitations & Considerations

### 6.1 Data Limitations

1. **Surveillance Bias**: Passive surveillance underestimates true burden for asymptomatic/mild diseases
2. **Reporting Delays**: Recent data may be incomplete (lag in outbreak detection)
3. **Testing Availability**: Burden estimates dependent on diagnostic capacity
4. **Population Dynamics**: Immigration/migration affects case volumes independently of transmission

### 6.2 Methodological Limitations

1. **Equal Weighting Assumption**: Within-criterion metrics (e.g., total_cases, annual_avg) equally weighted
2. **Linear Aggregation**: Additive model may not capture non-linear interactions (e.g., high volume + high trend synergies)
3. **Threshold Subjectivity**: Tier cutoffs are policy choices, not statistical derivations
4. **Missing Dimensions**: Framework does not capture:
   - Severity (case fatality rate)
   - Economic impact (DALYs, productivity loss)
   - Health equity (disproportionate impact on vulnerable populations)
   - Prevention availability (vaccine-preventable diseases may warrant different strategies)

### 6.3 Contextual Considerations

- **Framework is Decision Support, Not Decision Replacement**: Rankings inform, not dictate, resource allocation
- **Expert Judgment Remains Essential**: Local context, strategic goals, political feasibility must temper quantitative rankings
- **Dynamic Environment**: Emerging threats (e.g., novel pathogens) may require ad-hoc prioritization outside framework

## 7. Future Enhancements

### 7.1 Short-Term (Next 12 Months)

1. **Severity Integration**: Incorporate case fatality rate, hospitalization rate into volume criterion
2. **Economic Burden**: Add DALYs or cost-of-illness estimates as fifth criterion
3. **Geospatial Analysis**: Sub-national prioritization for targeted resource deployment
4. **Automated Pipeline**: Integrate framework with surveillance database for real-time updates

### 7.2 Long-Term (2-3 Years)

1. **Machine Learning**: Predictive models for trend forecasting (ARIMA, Prophet) to improve trend criterion
2. **Interactive Dashboard**: Web-based tool for stakeholders to explore alternative weights
3. **Health Equity Lens**: Weighting factor for diseases disproportionately affecting vulnerable populations
4. **Regional Harmonization**: Coordinate with WHO/SEARO for cross-country comparability

## 8. References & Appendices

### 8.1 Key Files

- **Configuration**: `config/prioritization.yml`
- **Source Code**: `src/analysis/prioritization.py`
- **Unit Tests**: `tests/unit/test_prioritization.py`
- **Analysis Notebook**: `notebooks/2_analysis/02_disease_prioritization_framework.ipynb`
- **Results**: `results/tables/disease_priority_rankings.csv`

### 8.2 Related Documents

- User Story 2: Burden Metrics Calculation (`docs/objectives/user_stories/us-002-calculate-burden-metrics.md`)
- Data Dictionary: Infectious Disease Bulletin (`docs/data_dictionary/infectious_disease_bulletin.md`)
- Disease Burden Assessment Methodology (`docs/domain_knowledge/disease-burden-assessment-methodology.md`)

### 8.3 Glossary

- **CAGR**: Compound Annual Growth Rate (geometric mean of year-over-year growth)
- **MCDA**: Multi-Criteria Decision Analysis (structured approach to complex decisions)
- **Spearman ρ**: Rank correlation coefficient (measures monotonic relationships)
- **DALYs**: Disability-Adjusted Life Years (burden metric combining mortality and morbidity)

---

**Document Control**:
- Version: 1.0
- Date: 2026-02-12
- Approved By: [Pending Leadership Review]
- Next Review: 2026-Q1 (Annual Update) or upon policy trigger
