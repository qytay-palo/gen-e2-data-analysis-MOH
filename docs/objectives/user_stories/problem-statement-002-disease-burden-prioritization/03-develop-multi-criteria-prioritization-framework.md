# User Story: 3 - Develop Multi-Criteria Prioritization Framework

**As an** MOH policy maker,
**I want** a transparent, evidence-based framework for ranking diseases using weighted multi-criteria scoring,
**so that** I can justify resource allocation decisions with defensible methodology and stakeholder buy-in.

## 1. 🎯 Acceptance Criteria

1. **Prioritization Criteria Defined**
   - 4-6 burden criteria selected based on stakeholder input
   - Weighting scheme defined (criteria weights sum to 100%)
   - Rationale documented for each criterion and weight
   - Stakeholder validation obtained through workshop or survey

2. **Scoring Methodology Established**
   - Metrics normalized to common 0-100 scale
   - Composite burden score formula defined
   - Scoring approach validated with test cases
   - Edge cases handled (e.g., diseases with missing metrics)

3. **Disease Rankings Calculated**
   - All 45 diseases ranked by composite burden score
   - Diseases grouped into priority tiers (High, Medium, Low)
   - Tier thresholds defined (e.g., High = score >70)
   - Rankings exported as reference table

4. **Sensitivity Analysis Performed**
   - Rankings recalculated under different weighting schemes
   - Robustness of top rankings assessed
   - Scenarios documented (e.g., "volume-focused" vs. "trend-focused")
   - Consensus rankings identified (diseases consistently top-ranked)

5. **Framework Documentation Delivered**
   - Methodology document explaining prioritization approach
   - Transparent justification for criteria and weights
   - Reproducible calculations with code
   - Stakeholder-friendly summary with key insights

## 2. 🔒 Technical Constraints

- **Scoring Approach**: Weighted sum of normalized metrics
- **Transparency**: All calculations must be auditable and reproducible
- **Flexibility**: Framework should support easy weight adjustments
- **Output**: Disease rankings table, tier assignments, sensitivity analysis report

## 3. 📚 Domain Knowledge References

- [Disease Burden Assessment Methodology](../../../domain_knowledge/disease-burden-assessment-methodology.md) - Multi-criteria decision analysis, prioritization frameworks, sensitivity analysis
- [Infectious Disease Epidemiology Terminology](../../../domain_knowledge/infectious-disease-epidemiology-terminology-glossary.md) - Disease burden interpretation

**Recommended Criteria** (from domain knowledge):
1. **Case Volume** (40% weight): Total or annual average cases - measures absolute burden
2. **Trend** (25% weight): CAGR or trend direction - identifies emerging threats
3. **Outbreak Risk** (20% weight): Outbreak frequency and intensity - surge capacity needs
4. **Volatility** (15% weight): Coefficient of variation - predictability

**Alternative Weighting Scenarios**:
- **Volume-focused**: 60% volume, 20% trend, 10% outbreak, 10% volatility
- **Emerging threat-focused**: 30% volume, 50% trend, 15% outbreak, 5% volatility
- **Stability-focused**: 30% volume, 20% trend, 30% outbreak, 20% volatility

## 4. 📦 Dependencies

**External Packages**:
- `polars` - Data manipulation, scoring calculations
- `numpy` - Mathematical operations
- `matplotlib` / `seaborn` - Visualization of rankings
- `scikit-learn` - MinMaxScaler for normalization (if not already done)

**Internal Dependencies**:
- Comprehensive burden metrics dataset from User Story 2
- Normalized metrics (0-100 scale)

## 5. ✅ Implementation Tasks

### Stakeholder Engagement
- ⬜ Design stakeholder workshop or survey to validate criteria
- ⬜ Present proposed criteria (volume, trend, outbreak, volatility) with rationale
- ⬜ Gather feedback on criteria relevance and importance
- ⬜ Facilitate discussion on weighting preferences
- ⬜ Document stakeholder consensus or divergent views

### Criteria and Weight Definition
- ⬜ Finalize 4-6 prioritization criteria based on stakeholder input
- ⬜ Define weighting scheme (e.g., 40% volume, 25% trend, 20% outbreak, 15% volatility)
- ⬜ Document rationale for each criterion and weight
- ⬜ Map criteria to burden metrics calculated in User Story 2

### Scoring Methodology Implementation
- ⬜ Verify all metrics normalized to 0-100 scale
- ⬜ Implement composite score calculation: Σ(weight_i × metric_i)
- ⬜ Handle missing metrics (e.g., diseases with insufficient data for outbreak frequency)
- ⬜ Validate scoring with test cases (e.g., expect Dengue, HFMD in top 5)

### Disease Ranking Calculation
- ⬜ Calculate composite burden score for all 45 diseases
- ⬜ Rank diseases from highest to lowest score
- ⬜ Define priority tiers: High (score >70), Medium (40-70), Low (<40)
- ⬜ Create disease ranking table with scores and tier assignments

### Sensitivity Analysis
- ⬜ Define 3-5 alternative weighting scenarios
- ⬜ Recalculate rankings under each scenario
- ⬜ Compare rankings across scenarios (correlation, rank changes)
- ⬜ Identify consensus top-ranked diseases (consistently high across scenarios)
- ⬜ Identify sensitive diseases (rank varies significantly by weighting)

### Visualization and Reporting
- ⬜ Create bar chart of composite burden scores (top 20 diseases)
- ⬜ Generate tier assignment visualization (grouped bar chart or heatmap)
- ⬜ Create spider/radar charts showing multi-dimensional burden profiles for top diseases
- ⬜ Visualize sensitivity analysis (ranking stability plot)

### Framework Documentation
- ⬜ Write methodology document explaining prioritization approach
- ⬜ Document criteria definitions, metrics, and weighting rationale
- ⬜ Include stakeholder validation process and outcomes
- ⬜ Provide reproducible code for calculations
- ⬜ Create executive summary (2-3 pages) for leadership

## 6. Notes

**Prioritization Philosophy**:
- **Evidence-based**: Decisions grounded in data, not politics or subjective judgment
- **Transparent**: Methodology must be clearly explained and auditable
- **Flexible**: Weights can be adjusted as priorities evolve
- **Stakeholder-informed**: Criteria and weights validated with decision-makers

**Expected Top Priorities**:
Based on preliminary data exploration:
1. **HFMD (combined)**: ~235,000 cases (highest volume), strong seasonality
2. **Dengue Fever**: ~127,000 cases, frequent outbreaks, increasing trend
3. **Salmonellosis**: ~16,000 cases, stable but sustained burden
4. **Mumps**: ~4,000 cases, vaccine-preventable but increasing in some years
5. **Campylobacter variants**: ~4,000 cases, foodborne threat

**Sensitivity Analysis Purpose**:
- Tests robustness of rankings to different stakeholder priorities
- Identifies diseases that remain top priorities regardless of weighting (consensus priorities)
- Reveals diseases whose ranking is sensitive to criteria weighting (requires careful consideration)

**Tier Assignment Rationale**:
- **High Priority (>70)**: Top 10-15 diseases requiring substantial resources
- **Medium Priority (40-70)**: Important diseases requiring sustained effort
- **Low Priority (<40)**: Rare diseases in maintenance/surveillance mode

**Stakeholder Workshop Considerations**:
- Attendees: MOH policy makers, disease program managers, epidemiologists, finance committees
- Agenda: Present burden metrics, discuss criteria relevance, vote on weights
- Outcome: Validated prioritization framework with stakeholder buy-in

**Framework Maintenance**: Prioritization should be updated annually as new surveillance data arrives. Weighting may need periodic review (every 2-3 years) to align with evolving strategic priorities.

---

## Implementation Plan

### 1. Feature Overview

This user story focuses on developing a transparent, evidence-based multi-criteria prioritization framework to rank all 45 infectious diseases by burden using weighted composite scoring. The framework will enable MOH policy makers to make defensible resource allocation decisions based on systematic evaluation of multiple burden dimensions (case volume, trends, outbreak risk, volatility) with stakeholder-validated criteria and weights. Sensitivity analysis will test the robustness of rankings under different weighting scenarios, ensuring that top priorities remain consistent across reasonable assumptions.

**Primary User Role**: MOH policy maker

### 2. Component Analysis & Reuse Strategy

#### Existing Components for Reuse

| Component | Location | Reuse Strategy | Justification |
|-----------|----------|---------------|---------------|
| Burden Metrics Notebook | `notebooks/2_analysis/01_burden_metrics_calculation.ipynb` | **Modify** - Add prioritization calculations | Already calculates comprehensive burden metrics (volume, trend, outbreak, variability); needs scoring and ranking logic |
| Burden Metrics Module | `src/data_processing/burden_metrics.py` | **Reuse as-is** | Provides burden metric calculation functions that feed into prioritization |
| Disease Burden Dataset | `data/4_processed/disease_burden_metrics.csv` | **Reuse as-is** | Contains all required metrics (46 diseases with volume, trend, outbreak, variability dimensions) |
| Logger Utility | `src/utils/logger.py` | **Reuse as-is** | Standard logging for tracking prioritization calculations |
| Config Module | `src/config.py` | **Modify** - Add prioritization config | Needs weighting scheme and tier threshold definitions |

#### New Components Needed

| Component | Location | Responsibility | Rationale |
|-----------|----------|---------------|-----------|
| Prioritization Module | `src/analysis/prioritization.py` | Calculate composite scores, rankings, sensitivity analysis | Core prioritization logic needs dedicated module |
| Prioritization Notebook | `notebooks/2_analysis/02_disease_prioritization_framework.ipynb` | Execute prioritization, visualize rankings, document framework | Separate analytical notebook for prioritization workflow |
| Prioritization Config | `config/prioritization.yml` | Store weighting schemes, tier thresholds, scenarios | Externalize configuration for easy weight adjustments |
| Prioritization Results | `results/tables/disease_priority_rankings.csv` | Disease rankings with scores and tiers | Final output for stakeholder consumption |
| Sensitivity Analysis Report | `results/tables/sensitivity_analysis.csv` | Ranking changes across scenarios | Robustness assessment deliverable |

**Gaps Identified**:
- No existing prioritization or scoring logic in codebase
- No multi-criteria weighting configuration
- No sensitivity analysis capabilities
- No stakeholder engagement documentation template

### 3. Affected Files

#### New Files
- `[CREATE] src/analysis/prioritization.py` - Multi-criteria scoring and ranking module
- `[CREATE] notebooks/2_analysis/02_disease_prioritization_framework.ipynb` - Prioritization workflow notebook
- `[CREATE] config/prioritization.yml` - Weighting schemes and configuration
- `[CREATE] results/tables/disease_priority_rankings.csv` - Final disease rankings output
- `[CREATE] results/tables/sensitivity_analysis.csv` - Ranking robustness analysis
- `[CREATE] results/figures/priority_rankings_bar.png` - Top 20 disease ranking visualization
- `[CREATE] results/figures/priority_tiers_distribution.png` - Tier assignment visualization
- `[CREATE] results/figures/burden_profiles_radar.png` - Multi-dimensional burden profiles
- `[CREATE] results/figures/sensitivity_heatmap.png` - Sensitivity analysis heatmap
- `[CREATE] docs/methodology/prioritization_framework.md` - Framework methodology documentation
- `[CREATE] docs/stakeholder_engagement/prioritization_workshop_summary.md` - Stakeholder validation record
- `[CREATE] tests/unit/test_prioritization.py` - Unit tests for prioritization logic

#### Modified Files
- `[MODIFY] notebooks/2_analysis/01_burden_metrics_calculation.ipynb` - Add note linking to prioritization notebook
- `[MODIFY] src/config.py` - Add prioritization configuration loader
- `[MODIFY] data/4_processed/README.md` - Document new prioritization outputs
- `[MODIFY] docs/objectives/user_stories/problem-statement-002-disease-burden-prioritization/03-develop-multi-criteria-prioritization-framework.md` - Mark implementation tasks complete

### 4. Component Breakdown

#### New Component: `src/analysis/prioritization.py`

**Primary Responsibility**: Multi-criteria disease prioritization engine

**Key Functions**:
- `normalize_metrics(df: pl.DataFrame, metrics: List[str]) -> pl.DataFrame` - Min-max normalization to 0-100 scale
- `calculate_composite_score(df: pl.DataFrame, weights: Dict[str, float]) -> pl.DataFrame` - Weighted sum of normalized metrics
- `assign_tiers(df: pl.DataFrame, thresholds: Dict[str, float]) -> pl.DataFrame` - Classify diseases into High/Medium/Low priority tiers
- `rank_diseases(df: pl.DataFrame, score_col: str) -> pl.DataFrame` - Rank diseases by composite burden score
- `sensitivity_analysis(df: pl.DataFrame, scenarios: Dict[str, Dict[str, float]]) -> pl.DataFrame` - Calculate rankings under multiple weighting schemes
- `calculate_rank_correlation(rankings: Dict[str, pl.DataFrame]) -> pl.DataFrame` - Spearman correlation between scenario rankings
- `identify_consensus_priorities(rankings: Dict[str, pl.DataFrame], top_n: int = 10) -> List[str]` - Diseases consistently top-ranked across scenarios

**Key Parameters**:
- `weighting_scheme`: Dictionary mapping criteria to weights (must sum to 100%)
- `tier_thresholds`: Dictionary with "high" and "medium" score thresholds
- `scenarios`: Dictionary of alternative weighting schemes for sensitivity analysis

**Dependencies**:
- `polars` - DataFrame operations
- `numpy` - Statistical calculations
- `scipy.stats` - Spearman rank correlation

#### New Component: `notebooks/2_analysis/02_disease_prioritization_framework.ipynb`

**Primary Responsibility**: Interactive prioritization workflow and stakeholder documentation

**Key Sections**:
1. **Setup & Data Loading** - Load burden metrics, configure weighting
2. **Metric Normalization** - Transform metrics to 0-100 scale
3. **Base Case Prioritization** - Apply default weights, rank diseases
4. **Tier Assignment** - Classify into High/Medium/Low priority groups
5. **Sensitivity Analysis** - Test 3-5 alternative weighting scenarios
6. **Robustness Assessment** - Identify consensus top priorities
7. **Visualization** - Rankings, tiers, radar charts, sensitivity heatmap
8. **Stakeholder Presentation** - Generate summary for policy makers

**Key Outputs**:
- `disease_priority_rankings.csv` - Final rankings table
- `sensitivity_analysis.csv` - Rankings under all scenarios
- Visualizations (bar charts, heatmaps, radar charts)

#### New Component: `config/prioritization.yml`

**Primary Responsibility**: Externalized configuration for prioritization framework

**Configuration Structure**:
```yaml
base_case:
  weights:
    volume: 0.40
    trend: 0.25
    outbreak: 0.20
    variability: 0.15
  tier_thresholds:
    high: 70.0
    medium: 40.0

scenarios:
  volume_focused:
    weights: {volume: 0.60, trend: 0.20, outbreak: 0.10, variability: 0.10}
  emerging_threat_focused:
    weights: {volume: 0.30, trend: 0.50, outbreak: 0.15, variability: 0.05}
  stability_focused:
    weights: {volume: 0.30, trend: 0.20, outbreak: 0.30, variability: 0.20}

metrics:
  volume_metrics: [total_cases_score, annual_avg_cases_score]
  trend_metrics: [cagr_score]
  outbreak_metrics: [outbreak_frequency_score, outbreak_intensity_score]
  variability_metrics: [coefficient_variation_score]
```

#### Modified Component: `notebooks/2_analysis/01_burden_metrics_calculation.ipynb`

**Required Changes**: Add markdown cell at end linking to prioritization notebook

**Justification**: Establish clear workflow connection between burden metric calculation and prioritization

#### Modified Component: `src/config.py`

**Required Changes**: Add function to load prioritization configuration from YAML

**Justification**: Centralize configuration loading with existing pattern

### 5. Data Pipeline

**CRITICAL**: All implementation is grounded in available data sources documented in [docs/project_context/data-sources.md](../../../docs/project_context/data-sources.md) and feasible with current tech stack in [docs/project_context/tech-stack.md](../../../docs/project_context/tech-stack.md).

#### Data Sources
**Primary Source**: Processed burden metrics dataset
- **Location**: `data/4_processed/disease_burden_metrics.csv`
- **Records**: 46 diseases with comprehensive burden metrics
- **Metrics Available**: 
  - Volume: `total_cases_score`, `annual_avg_cases_score`, `peak_weekly_cases_score`, `incidence_rate_per_100k_score`
  - Trend: `cagr_score`, `trend_direction`
  - Outbreak: `outbreak_frequency_score`, `outbreak_intensity_score`
  - Variability: `coefficient_variation_score`
  - Pre-calculated composite scores: `volume_score`, `trend_score`, `outbreak_score`, `variability_score`

**Data Quality**: All metrics already normalized to 0-100 scale in User Story 2 implementation

#### Data Extraction
**Method**: Direct file reading (no extraction needed)
```python
import polars as pl
df = pl.read_csv('data/4_processed/disease_burden_metrics.csv')
```

**Note**: Use `/write-query` command if future implementation requires SQL-based extraction from database backend.

#### Data Transformation Steps

1. **Data Loading & Validation**
   - Load burden metrics CSV
   - Validate required columns exist (`disease_name`, `*_score` columns, `sufficient_data` flag)
   - Filter to diseases with sufficient data (`sufficient_data == true`)

2. **Criteria Aggregation**
   - **Volume Criterion**: Average of normalized volume metrics
     - Formula: `(total_cases_score + annual_avg_cases_score) / 2`
   - **Trend Criterion**: Use existing `trend_score` (based on CAGR)
   - **Outbreak Criterion**: Use existing `outbreak_score` (frequency + intensity)
   - **Variability Criterion**: Use existing `variability_score` (CV-based)

3. **Composite Score Calculation**
   - Apply weighting scheme: `Composite = 0.40*Volume + 0.25*Trend + 0.20*Outbreak + 0.15*Variability`
   - Validate score range: 0-100
   - Handle missing values: Diseases with insufficient data excluded from ranking

4. **Ranking & Tier Assignment**
   - Rank diseases by composite score (descending)
   - Assign tiers:
     - High Priority: Score > 70
     - Medium Priority: Score 40-70
     - Low Priority: Score < 40
   - Add rank column (1 = highest burden)

5. **Sensitivity Analysis**
   - Repeat steps 2-4 for each alternative weighting scenario
   - Calculate Spearman rank correlation between scenarios
   - Identify diseases in Top 10 across all scenarios (consensus priorities)
   - Calculate rank volatility: Standard deviation of rank across scenarios

#### Target Consumption Layer
- **Primary**: CSV files for stakeholder review (`results/tables/`)
- **Secondary**: Markdown documentation with embedded tables (`docs/methodology/`)
- **Tertiary**: Interactive visualizations (PNG figures in `results/figures/`)

#### Orchestration & Scheduling
- **Execution Order**: 
  1. Load burden metrics → 2. Normalize/aggregate → 3. Score/rank → 4. Sensitivity analysis → 5. Visualize
- **Incremental vs. Full Refresh**: Full refresh (entire prioritization recalculated when burden metrics updated)
- **Error Handling**: 
  - Validate weights sum to 100%
  - Check for missing score columns
  - Handle diseases with insufficient data gracefully (exclude from ranking with warning)
- **Monitoring**: Log number of diseases ranked, tier distribution, top 5 priorities
- **Data Lineage**: Record burden metrics file timestamp, config version, execution date in output metadata

### 6. Domain-Driven Feature Engineering & Analysis Strategy

**CRITICAL PREREQUISITE: Data Source Alignment Validation**

Before proceeding with domain-driven feature engineering, verify that all proposed features are computable from available data sources:

- [ ] **Cross-Reference with Data Sources Documentation**: Review [docs/project_context/data-sources.md](../../../docs/project_context/data-sources.md)
- [ ] **Verify Input Data Availability**: Confirm `data/4_processed/disease_burden_metrics.csv` contains all required fields
- [ ] **Validate Granularity Match**: Weekly case data (2012-2020) supports annual/multi-year aggregations
- [ ] **Check Feature Computability**:
  - Volume features: ✓ Total cases, annual averages computable from weekly data
  - Trend features: ✓ CAGR calculable from multi-year time series
  - Outbreak features: ✓ Outbreak detection possible from weekly counts
  - Variability features: ✓ Coefficient of variation derivable from weekly data
- [ ] **Identify Data Gaps**: No known gaps for prioritization features (all metrics calculated in User Story 2)
- [ ] **Document Assumptions**: Prioritization based on 2012-2020 data; post-2020 patterns not reflected

#### Step 1: Identify Relevant Domain Knowledge

**Selected Domain Document**: [Disease Burden Assessment Methodology](../../../docs/domain_knowledge/disease-burden-assessment-methodology.md)

**Key Applicable Concepts**:

1. **Multi-Criteria Decision Analysis (MCDA)** (Lines 28-37)
   - Weighted scoring approach for disease prioritization
   - Balancing multiple, often conflicting criteria (volume vs. trends vs. outbreaks)
   - Stakeholder-validated weighting schemes
   - **Applicable Metrics**: Composite burden score, criterion weights, tier thresholds

2. **Burden Metrics** (Lines 39-58)
   - Absolute burden: Total impact (case volume)
   - Relative burden: Cross-disease comparison
   - Trend-based burden: Trajectory over time (emerging vs. declining)
   - Outbreak burden: Epidemic potential and surge capacity needs
   - **Applicable Metrics**: Volume score, trend score, outbreak score, variability score

3. **Multi-Criteria Prioritization Framework** (Lines 189-211)
   - Step 1: Define 4-6 criteria with stakeholder input
   - Step 2: Normalize metrics to 0-100 scale (min-max normalization)
   - Step 3: Calculate composite score using weighted sum
   - Step 4: Rank and assign tiers (High >70, Medium 40-70, Low <40)
   - Step 5: Sensitivity analysis to test robustness
   - **Applicable Methods**: Normalization formula, composite scoring, tiering logic, sensitivity testing

4. **Common Pitfalls and Best Practices** (Lines 268-292)
   - Use multiple metrics (avoid single-metric bias)
   - Normalize for comparison (0-100 scale standardization)
   - Validate with stakeholders (epidemiologist review)
   - Document methodology transparently (reproducibility)
   - Scenario analysis (test ranking robustness)
   - **Applicable Practices**: Sensitivity analysis, stakeholder validation, transparent documentation

#### Step 2: Validate Data Availability

**Cross-Reference with Available Data Sources**: `data/4_processed/disease_burden_metrics.csv`

| Domain Concept | Required Data Fields | Available in Dataset? | Data Quality | Notes |
|----------------|---------------------|----------------------|--------------|-------|
| Absolute Burden (Case Volume) | `total_cases`, `annual_avg_cases` | ✅ Yes | Complete, normalized to 0-100 (`total_cases_score`, `annual_avg_cases_score`) | From User Story 2 |
| Trend-Based Burden | `cagr`, `trend_direction` | ✅ Yes | Complete, normalized to 0-100 (`cagr_score`) | Statistical trend analysis performed |
| Outbreak Burden | `outbreak_frequency`, `outbreak_intensity` | ✅ Yes | Complete, normalized to 0-100 (`outbreak_frequency_score`, `outbreak_intensity_score`) | Threshold-based outbreak detection |
| Variability Burden | `coefficient_variation` | ✅ Yes | Complete, normalized to 0-100 (`coefficient_variation_score`) | CV calculated from weekly data |
| Sufficient Data Flag | `sufficient_data` | ✅ Yes | Boolean flag | Identifies diseases with adequate data for reliable metrics |

**Data Gaps**: None. All required domain-driven features are computable from available data.

**Data Granularity**: 
- Temporal: Weekly case data aggregated to multi-year metrics (2012-2020)
- Geographic: National level (Singapore)
- Categorical: 45 diseases with standardized names

#### Step 3: Select Applicable Features

**Selected Features for Prioritization** (all domain-aligned, data-validated):

1. **Volume Composite Score**
   - **Domain Terminology**: Absolute Burden Metric
   - **Calculation Method** (from domain knowledge): Average of normalized volume metrics
   - **Formula**: `volume_criterion = (total_cases_score + annual_avg_cases_score) / 2`
   - **Required Input Fields**: `total_cases_score`, `annual_avg_cases_score` (from `disease_burden_metrics.csv`)
   - **Expected Value Range**: 0-100 (normalized)
   - **Domain Validation**: Aligns with "absolute burden" concept (lines 44-47 in domain doc)

2. **Trend Score**
   - **Domain Terminology**: Trend-Based Burden Metric
   - **Calculation Method** (from domain knowledge): CAGR-based trend assessment
   - **Formula**: Use existing `cagr_score` (already calculated in User Story 2)
   - **Required Input Fields**: `cagr_score` (from `disease_burden_metrics.csv`)
   - **Expected Value Range**: 0-100 (0 = strong decline, 50 = stable, 100 = strong growth)
   - **Domain Validation**: Aligns with "emerging threats may have low current burden but high future risk" (line 54)

3. **Outbreak Risk Score**
   - **Domain Terminology**: Outbreak Burden Metric
   - **Calculation Method** (from domain knowledge): Composite of outbreak frequency and intensity
   - **Formula**: Use existing `outbreak_score` (average of `outbreak_frequency_score` and `outbreak_intensity_score`)
   - **Required Input Fields**: `outbreak_score` (from `disease_burden_metrics.csv`)
   - **Expected Value Range**: 0-100 (0 = no outbreaks, 100 = frequent severe outbreaks)
   - **Domain Validation**: Aligns with "outbreak-prone diseases strain healthcare capacity unpredictably" (line 56)

4. **Variability Score**
   - **Domain Terminology**: Predictability Metric (inverse of volatility)
   - **Calculation Method** (from domain knowledge): Coefficient of Variation (CV) normalized
   - **Formula**: Use existing `coefficient_variation_score` (inverse-normalized CV)
   - **Required Input Fields**: `coefficient_variation_score` (from `disease_burden_metrics.csv`)
   - **Expected Value Range**: 0-100 (0 = highly volatile, 100 = stable)
   - **Domain Validation**: Aligns with "higher CV = more volatile, unpredictable" (lines 125-132)

5. **Composite Burden Score**
   - **Domain Terminology**: Multi-Criteria Burden Score
   - **Calculation Method** (from domain knowledge): Weighted sum of normalized criteria
   - **Formula**: `Composite = 0.40*Volume + 0.25*Trend + 0.20*Outbreak + 0.15*Variability`
   - **Required Input Fields**: All four criterion scores above
   - **Expected Value Range**: 0-100 (composite of weighted components)
   - **Domain Validation**: Exact formula from domain doc lines 201-203

6. **Priority Tier**
   - **Domain Terminology**: Tier Classification for Resource Allocation
   - **Calculation Method** (from domain knowledge): Threshold-based classification
   - **Formula**: 
     - High Priority: `composite_score > 70`
     - Medium Priority: `40 <= composite_score <= 70`
     - Low Priority: `composite_score < 40`
   - **Required Input Fields**: `composite_burden_score`
   - **Expected Value Range**: Categorical (High, Medium, Low)
   - **Domain Validation**: Exact thresholds from domain doc lines 206-209

**Analytical Approach**:

- **Descriptive Statistics**: Distribution of composite scores, tier counts, top 10 rankings
- **Sensitivity Analysis**: Recalculate rankings under 3 alternative weighting scenarios (volume-focused, emerging threat-focused, stability-focused per domain doc lines 198-200)
- **Robustness Assessment**: Spearman rank correlation between scenarios, identify consensus priorities (diseases in Top 10 across all scenarios)
- **Domain-Specific Validation**: 
  - Compare top-ranked diseases against epidemiological expectations (e.g., Dengue, HFMD expected in top 5 based on domain knowledge)
  - Validate tier distribution aligns with policy capacity (~10-15 high priority diseases per domain guidance)
  - Check trend score alignment with known disease trajectories (e.g., Zika should have high trend score during 2016 emergence)

**Interpretation Guidelines** (using domain context):
- **High Priority Diseases** (Score >70): Require substantial, sustained resources; major drivers of infectious disease burden
- **Medium Priority Diseases** (Score 40-70): Important but manageable with existing programs; candidates for efficiency improvements
- **Low Priority Diseases** (Score <40): Minimal surveillance and response capacity; maintenance mode
- **Emerging Threats** (High Trend + Low Volume): Diseases with growing burden despite currently low absolute cases; require proactive investment
- **Outbreak-Prone Diseases** (High Outbreak + High Variability): Require surge capacity and flexible resource allocation

### 7. API Endpoints & Data Contracts

**Not Applicable**: This user story does not involve API development. Outputs are file-based (CSV tables, PNG visualizations, Markdown documentation).

### 8. Styling & Visualization

#### Data Plugin Accelerators
- Use `/create-viz` command for generating publication-quality Python visualizations
- Reference: `.github/prompts/data-plugin/skills/data-visualization/SKILL.md` for chart selection best practices

#### Visualization Requirements

**1. Priority Rankings Bar Chart** (`results/figures/priority_rankings_bar.png`)
- **Chart Type**: Horizontal bar chart (Top 20 diseases)
- **X-Axis**: Composite Burden Score (0-100)
- **Y-Axis**: Disease names (sorted by score, descending)
- **Color Coding**: 
  - High Priority (>70): `#D32F2F` (Red)
  - Medium Priority (40-70): `#FFA726` (Orange)
  - Low Priority (<40): `#66BB6A` (Green)
- **Title**: "Top 20 Infectious Diseases by Composite Burden Score"
- **Annotations**: Score values at end of bars, tier boundary lines at 70 and 40

**2. Priority Tiers Distribution** (`results/figures/priority_tiers_distribution.png`)
- **Chart Type**: Grouped bar chart or stacked bar
- **X-Axis**: Priority Tier (High, Medium, Low)
- **Y-Axis**: Number of diseases
- **Color Coding**: Same as above (Red, Orange, Green)
- **Title**: "Disease Distribution Across Priority Tiers"
- **Annotations**: Disease count labels on bars, percentage of total

**3. Burden Profiles Radar Charts** (`results/figures/burden_profiles_radar.png`)
- **Chart Type**: Radar/spider chart (multiple subplots for Top 5-10 diseases)
- **Axes**: Volume, Trend, Outbreak, Variability (4 dimensions)
- **Scale**: 0-100 for all axes
- **Color**: Unique color per disease (use `seaborn` color palette)
- **Title**: "Multi-Dimensional Burden Profiles: Top Priority Diseases"
- **Purpose**: Show relative strengths/weaknesses across criteria

**4. Sensitivity Analysis Heatmap** (`results/figures/sensitivity_heatmap.png`)
- **Chart Type**: Heatmap
- **Rows**: Diseases (Top 20)
- **Columns**: Weighting scenarios (Base Case, Volume-Focused, Emerging Threat, Stability-Focused)
- **Cell Color**: Rank number (darker = higher rank/priority)
- **Color Scale**: `viridis` or `RdYlGn_r` (red for top ranks)
- **Title**: "Ranking Stability Across Weighting Scenarios"
- **Annotations**: Rank numbers in cells, highlight consensus top-10 diseases

#### Chart Design Standards
- **Font Family**: Arial or Helvetica (clean, professional)
- **Font Sizes**: 
  - Title: 14pt bold
  - Axis labels: 11pt
  - Tick labels: 10pt
  - Annotations: 9pt
- **Figure Size**: 10x8 inches (suitable for reports)
- **DPI**: 300 (high-resolution for print)
- **Grid**: Light gray gridlines for quantitative charts
- **Legend**: Position outside plot area (right or bottom) when needed

#### Implementation Libraries
- `matplotlib` - Base plotting
- `seaborn` - Statistical visualizations and color palettes
- `polars` / `pandas` - Data preparation for plotting

### 9. Testing Strategy

#### Analysis Quality Assurance
- Use `/validate` command to QA analysis before stakeholder delivery
- Reference: `.github/prompts/data-plugin/skills/data-validation/SKILL.md` for pre-delivery QA checklist

#### Unit Tests: `tests/unit/test_prioritization.py`

**Test Coverage Areas**:

1. **Metric Normalization Tests**
   - `test_normalize_metrics_range()`: Verify all normalized values in 0-100 range
   - `test_normalize_metrics_min_max()`: Verify min value → 0, max value → 100
   - `test_normalize_metrics_handles_ties()`: Test behavior when multiple diseases have same value
   - `test_normalize_metrics_handles_nan()`: Verify missing values handled appropriately

2. **Composite Score Calculation Tests**
   - `test_composite_score_weights_sum_to_one()`: Validate weight normalization
   - `test_composite_score_calculation()`: Verify weighted sum formula
   - `test_composite_score_range()`: Ensure composite score in 0-100 range
   - `test_composite_score_with_default_weights()`: Test base case (40/25/20/15)

3. **Tier Assignment Tests**
   - `test_assign_tiers_high_priority()`: Verify score >70 → "High"
   - `test_assign_tiers_medium_priority()`: Verify 40 <= score <= 70 → "Medium"
   - `test_assign_tiers_low_priority()`: Verify score <40 → "Low"
   - `test_assign_tiers_boundary_cases()`: Test exact threshold values (70.0, 40.0)

4. **Ranking Tests**
   - `test_rank_diseases_descending()`: Verify highest score gets rank 1
   - `test_rank_diseases_handles_ties()`: Test tie-breaking logic
   - `test_rank_diseases_no_duplicates()`: Ensure unique ranks assigned

5. **Sensitivity Analysis Tests**
   - `test_sensitivity_analysis_multiple_scenarios()`: Verify rankings calculated for all scenarios
   - `test_rank_correlation_calculation()`: Test Spearman correlation computation
   - `test_identify_consensus_priorities()`: Verify top-N consensus logic
   - `test_alternative_weighting_schemes()`: Validate scenario weight configurations

6. **Edge Cases & Error Handling**
   - `test_empty_dataframe_handling()`: Graceful handling of empty input
   - `test_missing_score_columns()`: Error when required columns absent
   - `test_invalid_weights_sum()`: Error when weights don't sum to 100%
   - `test_insufficient_data_exclusion()`: Diseases with `sufficient_data=false` excluded

**Test Data**: 
- Create synthetic burden metrics DataFrame with known values for deterministic test outcomes
- Include edge cases: all zeros, all 100s, missing values, ties

**Assertions**:
- Schema validation: Output columns present and correct types
- Mathematical correctness: Manual calculation of expected composite scores
- Boundary validation: Scores/tiers at thresholds behave correctly
- Consistency: Same input produces same output (reproducibility)

#### Data Quality Tests

**Burden Metrics Input Validation** (in notebook):
- Check `sufficient_data` flag: Only include diseases with `sufficient_data == true`
- Verify score columns exist: `*_score` columns present and non-null for included diseases
- Validate score ranges: All input scores in 0-100 range
- Check disease count: Expect ~40-45 diseases with sufficient data

**Prioritization Output Validation** (in notebook):
- Verify all ranked diseases have composite score
- Check tier distribution: Expect ~10-15 high, ~15-25 medium, ~5-10 low priority diseases
- Validate rank sequence: No gaps in rank numbers (1, 2, 3, ...)
- Consistency check: Diseases with higher scores have lower rank numbers

**Sensitivity Analysis Validation** (in notebook):
- Verify rankings calculated for all scenarios
- Check correlation matrix: All pairwise correlations between scenarios calculated
- Validate consensus priorities: Top-N list length matches expected value
- Robustness check: Expect top 5 diseases relatively stable across scenarios

#### End-to-End Pipeline Testing

**Manual Testing Workflow**:
1. Run burden metrics notebook to generate input data
2. Execute prioritization notebook with base case weights
3. Verify output files created: `disease_priority_rankings.csv`, visualizations
4. Check top 10 rankings align with domain expectations (Dengue, HFMD in top 5)
5. Run sensitivity analysis scenarios
6. Compare rankings across scenarios for consistency

**Expected Outcomes**:
- Dengue Fever in Top 3 (high volume, outbreak frequency)
- Hand, Foot and Mouth Disease in Top 3 (highest volume)
- Salmonellosis in Top 10 (sustained high burden)
- Rare diseases (Cholera, Plague) in Low Priority tier
- Consensus top-10 includes major endemic diseases (stable across weighting variations)

### 10. Implementation Steps

#### Phase 1: Setup & Configuration

**1. Environment Setup:**
- [x] Python environment already configured (from User Story 2)
- [x] Dependencies installed: `polars`, `numpy`, `scipy`, `matplotlib`, `seaborn`
- [ ] Verify Python version compatibility (3.9+ required for type hints)
- [ ] Run code quality checks: `flake8`, `mypy`, `pylint` installed and configured
- [ ] Create prioritization configuration file: `config/prioritization.yml`
- [ ] Define base case weighting scheme: Volume 40%, Trend 25%, Outbreak 20%, Variability 15%
- [ ] Define tier thresholds: High >70, Medium 40-70, Low <40
- [ ] Define 3 alternative weighting scenarios for sensitivity analysis
- [ ] Set up `.env` file template (do NOT commit actual credentials)
- [ ] Add config files to `.gitignore` if containing any sensitive paths

**2. Configuration Implementation:**
- [ ] Create `config/prioritization.yml` with base case and scenario configurations
- [ ] **SECURITY**: Ensure no hardcoded credentials or sensitive paths in config
- [ ] Modify `src/config.py` to add `load_prioritization_config()` function with:
  - Type hints: `def load_prioritization_config(config_path: str) -> Dict[str, Any]`
  - Comprehensive docstring (Google style) with Args, Returns, Raises
  - Input validation: Check file exists, is valid YAML, has required keys
  - Error handling: Raise `FileNotFoundError` with clear message if config missing
  - Logging: INFO level for successful load, ERROR for failures
- [ ] Test configuration loading in Python console with sample scenarios
- [ ] Validate weight constraints: All weights sum to 100% (±0.001 tolerance) for each scenario
- [ ] Add unit test: `tests/unit/test_config.py::test_load_prioritization_config`
- [ ] Document configuration structure in `config/prioritization.yml` header comments

#### Phase 2: Core Prioritization Logic

**3. Prioritization Module Development:**
- [ ] Create `src/analysis/prioritization.py` module with module-level docstring
- [ ] Add module imports following best practices:
  ```python
  # Standard library
  import logging
  from typing import List, Dict, Any, Optional
  
  # Third-party
  import polars as pl
  import numpy as np
  from scipy import stats
  
  # Initialize logger
  logger = logging.getLogger(__name__)
  ```
- [ ] **DATA VALIDATION**: Before implementing functions, verify input data availability:
  - Confirm `data/4_processed/disease_burden_metrics.csv` exists and contains:
    - Required score columns: `total_cases_score`, `annual_avg_cases_score`, `cagr_score`, `outbreak_score`, `coefficient_variation_score`
    - `sufficient_data` boolean flag column
    - Minimum 40 diseases with `sufficient_data == True`
  - If data missing, block implementation until User Story 2 completed
- [ ] Implement `normalize_metrics()` function: Min-max normalization to 0-100 scale
  - Type hints: `def normalize_metrics(df: pl.DataFrame, metrics: List[str]) -> pl.DataFrame`
  - Comprehensive docstring (Google style, 15-20 lines) with:
    - Brief summary and mathematical formula: `normalized = (value - min) / (max - min) * 100`
    - Args section with parameter types and descriptions
    - Returns section with output structure description
    - Raises section: `ValueError` (invalid ranges), `KeyError` (missing columns)
    - Example section with runnable code snippet and expected output
  - **Defensive programming**:
    - Check DataFrame not empty: `if df.is_empty(): raise ValueError("Input DataFrame is empty")`
    - Validate metrics exist: `missing = set(metrics) - set(df.columns); if missing: raise KeyError(...)`
    - Ensure non-negative values before normalization
    - Handle zero range case (all values identical)
  - Return new DataFrame (don't modify input)
  - Log INFO: "Normalizing {len(metrics)} metrics for {len(df)} diseases"
- [ ] Implement `calculate_composite_score()` function: Weighted sum with validation
  - Type hints: `def calculate_composite_score(df: pl.DataFrame, weights: Dict[str, float]) -> pl.DataFrame`
  - Validate weights sum to 1.0 (±0.001 tolerance): `if abs(sum(weights.values()) - 1.0) > 0.001: raise ValueError(...)`
  - Validate all weight keys match available criteria in DataFrame
  - Include docstring with mathematical formula and worked example
  - Log INFO: "Calculating composite scores with weights: {weights}"
- [ ] Implement `assign_tiers()` function: Threshold-based classification
  - Type hints: `def assign_tiers(df: pl.DataFrame, thresholds: Dict[str, float]) -> pl.DataFrame`
  - Validate thresholds: high > medium > 0, raise `ValueError` with clear message
  - Add comprehensive docstring explaining tier definitions
  - Log INFO: "Assigning tiers: High >{high}, Medium {medium}-{high}, Low <{medium}"
- [ ] Implement `rank_diseases()` function: Descending rank by score
  - Type hints: `def rank_diseases(df: pl.DataFrame, score_col: str = 'composite_score') -> pl.DataFrame`
  - Check score column exists: `if score_col not in df.columns: raise KeyError(...)`
  - Handle ties consistently (use stable sorting)
  - Log INFO: "Ranked {len(df)} diseases by {score_col}"
- [ ] Add module-level validation function:
  ```python
  def validate_burden_metrics_input(df: pl.DataFrame) -> None:
      """Validate input burden metrics DataFrame structure and quality."""
      required_cols = ['disease_name', 'sufficient_data', 'total_cases_score', ...]
      # Check columns, types, ranges, nulls
  ```
- [ ] **CODE QUALITY CHECKPOINT**:
  - Run `flake8 src/analysis/prioritization.py` - ensure PEP 8 compliance
  - Run `mypy src/analysis/prioritization.py` - verify type hints correct
  - Check function length: All functions <50 lines (refactor if longer)
  - Verify all functions have comprehensive docstrings (Google style)
  - Ensure consistent error messages with context
  - Use module-level logger: `logger = logging.getLogger(__name__)`

**4. Unit Testing & Code Quality:**
- [ ] Create `tests/unit/test_prioritization.py` with proper test structure:
  ```python
  import pytest
  import polars as pl
  import numpy as np
  from src.analysis.prioritization import (
      normalize_metrics,
      calculate_composite_score,
      assign_tiers,
      rank_diseases
  )
  
  class TestNormalization:
      # Normalization test cases
      
  class TestCompositeScore:
      # Composite score test cases
  ```
- [ ] Write normalization tests:
  - `test_normalize_metrics_range()`: Verify all normalized values in 0-100 range
  - `test_normalize_metrics_min_max()`: Verify min value → 0, max value → 100
  - `test_normalize_metrics_handles_ties()`: All identical values → 50 (midpoint)
  - `test_normalize_metrics_handles_nan()`: Raise `ValueError` for NaN inputs
  - Test edge cases: Empty DataFrame, single value, all zeros, all 100s
  - Test error handling: Missing columns, non-numeric values
- [ ] Write composite score tests:
  - `test_composite_score_formula()`: Manual calculation matches function output
  - `test_composite_score_weights_validation()`: Sum != 1.0 raises `ValueError`
  - `test_composite_score_range()`: Output scores in 0-100 range
  - `test_composite_score_with_default_weights()`: Base case (40/25/20/15) works
  - Test with known inputs and expected outputs for determinism
  - Test weight validation: Negative weights, missing criteria keys
- [ ] Write tier assignment tests:
  - `test_assign_tiers_high_priority()`: Score >70 → "High"
  - `test_assign_tiers_medium_priority()`: 40 ≤ score ≤ 70 → "Medium"
  - `test_assign_tiers_low_priority()`: Score <40 → "Low"
  - `test_assign_tiers_boundary_cases()`: Exact 70.0 and 40.0 assigned correctly
  - Test threshold validation: high < medium, non-positive thresholds
- [ ] Write ranking tests:
  - `test_rank_diseases_descending()`: Highest score gets rank 1
  - `test_rank_diseases_handles_ties()`: Consistent tie-breaking
  - `test_rank_diseases_no_duplicates()`: All ranks unique
  - `test_rank_diseases_sequence()`: No gaps in rank numbers (1, 2, 3, ...)
  - Test error handling: Missing score column, empty DataFrame
- [ ] **Execute tests and validate coverage**:
  - Run: `pytest tests/unit/test_prioritization.py -v --cov=src.analysis.prioritization --cov-report=html --cov-report=term-missing`
  - **Validation Gate**: All tests must pass before proceeding
  - **Coverage Gate**: Achieve ≥90% code coverage
  - Review coverage report: `open htmlcov/index.html`
  - If coverage <90%: Identify uncovered lines and add tests
- [ ] Run code quality checks:
  - PEP 8 compliance: `flake8 src/analysis/prioritization.py --max-line-length=100`
  - Type checking: `mypy src/analysis/prioritization.py --strict`
  - Code complexity: `radon cc src/analysis/prioritization.py -a -nb` (target: A-B grade)
  - Security scan: `bandit -r src/analysis/prioritization.py`
- [ ] Fix any failing tests, linting errors, or type errors identified
- [ ] Document test results:
  - Save test output: `pytest tests/unit/test_prioritization.py -v > test_results.txt`
  - Save coverage report for documentation
  - Note any skipped tests with justification
  - Document known limitations or edge cases not covered

#### Phase 3: Stakeholder Engagement (Optional but Recommended)

**5. Stakeholder Workshop Preparation:**
- [ ] Create workshop presentation deck explaining proposed criteria and weights
- [ ] Include domain knowledge rationale for each criterion (volume, trend, outbreak, variability)
- [ ] Prepare example disease comparisons showing how weighting affects rankings
- [ ] Create survey or voting mechanism for weight validation
- [ ] Schedule workshop with MOH policy makers, disease program managers, epidemiologists

**6. Stakeholder Feedback Collection:**
- [ ] Conduct stakeholder workshop or distribute survey
- [ ] Present proposed criteria: Volume, Trend, Outbreak Risk, Variability
- [ ] Gather feedback on criteria relevance and completeness
- [ ] Facilitate discussion on weighting preferences (optional group consensus exercise)
- [ ] Document stakeholder input, consensus areas, and divergent views
- [ ] Adjust weighting scheme if strong stakeholder consensus differs from base case
- [ ] Create `docs/stakeholder_engagement/prioritization_workshop_summary.md`

#### Phase 4: Prioritization Execution

**7. Prioritization Notebook Development:**
- [ ] **PRE-NOTEBOOK VALIDATION** (CRITICAL - complete before creating notebook):
  - Test data loading code in terminal/REPL:
    ```python
    import polars as pl
    df = pl.read_csv('data/4_processed/disease_burden_metrics.csv')
    print(df.shape, df.columns)
    ```
  - Verify all import statements work (polars, numpy, scipy, matplotlib, seaborn)
  - Test config loading function executes without errors
  - Confirm all file paths exist and are accessible
  - Run sample calculations to verify logic before adding to notebook
  - **DO NOT create notebook if any validation fails** - fix issues first
- [ ] Create `notebooks/2_analysis/02_disease_prioritization_framework.ipynb`
- [ ] **Section 1: Setup & Data Loading**
  - Add markdown cell explaining notebook purpose and user story context
  - Import libraries with error handling:
    ```python
    try:
        import polars as pl
        import numpy as np
        from scipy import stats
        # ... other imports
    except ImportError as e:
        print(f"Missing dependency: {e}. Install with: pip install <package>")
        raise
    ```
  - Configure logging with appropriate format and level:
    ```python
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    ```
  - Load burden metrics with validation:
    ```python
    df = pl.read_csv('data/4_processed/disease_burden_metrics.csv')
    logger.info(f"Loaded {len(df)} diseases from burden metrics")
    assert not df.is_empty(), "DataFrame is empty"
    ```
  - Load configuration with error handling:
    ```python
    try:
        config = load_prioritization_config('config/prioritization.yml')
    except FileNotFoundError:
        logger.error("Config file not found. Create config/prioritization.yml first.")
        raise
    ```
  - Display dataset shape, columns, and preview (first 5 rows)
- [ ] **Section 2: Data Validation**
  - Filter to diseases with sufficient data: `df_valid = df.filter(pl.col('sufficient_data') == True)`
  - Log filtered count: `logger.info(f"Filtered to {len(df_valid)} diseases with sufficient data")`
  - Verify required score columns present:
    ```python
    required_cols = ['total_cases_score', 'annual_avg_cases_score', 'cagr_score', ...]
    missing = set(required_cols) - set(df_valid.columns)
    if missing:
        raise KeyError(f"Missing required columns: {missing}")
    ```
  - Validate score ranges (0-100):
    ```python
    for col in required_cols:
        min_val, max_val = df_valid[col].min(), df_valid[col].max()
        if min_val < 0 or max_val > 100:
            logger.warning(f"{col} out of range: [{min_val}, {max_val}]")
    ```
  - Check for null values in critical columns
  - Display data quality summary: Shape, null counts, score distributions

**8. Base Case Prioritization:**
- [ ] **Section 3: Metric Aggregation**
  - Calculate Volume criterion: Average of `total_cases_score` and `annual_avg_cases_score`
  - Use existing Trend criterion: `cagr_score`
  - Use existing Outbreak criterion: `outbreak_score`
  - Use existing Variability criterion: `coefficient_variation_score`
  - Validate all criteria in 0-100 range
- [ ] **Section 4: Composite Score Calculation**
  - Apply base case weights: `Composite = 0.40*Volume + 0.25*Trend + 0.20*Outbreak + 0.15*Variability`
  - Calculate composite burden score for all diseases
  - Validate composite score range (0-100)
  - Display distribution statistics (mean, median, min, max)
- [ ] **Section 5: Ranking & Tier Assignment**
  - Rank diseases by composite score (descending)
  - Assign tiers: High (>70), Medium (40-70), Low (<40)
  - Create rankings table with columns: `rank`, `disease_name`, `composite_score`, `tier`, `volume`, `trend`, `outbreak`, `variability`
  - Display Top 20 ranked diseases
  - Display tier distribution summary

**9. Prioritization Results Export:**
- [ ] Export rankings to `results/tables/disease_priority_rankings.csv`
- [ ] Include all diseases (not just top 20) in export
- [ ] Add metadata columns: `analysis_date`, `weighting_scheme`, `tier_threshold_high`, `tier_threshold_medium`
- [ ] Validate CSV format: No missing values, proper headers, correct data types
- [ ] Log export success and file path

#### Phase 5: Sensitivity Analysis

**10. Sensitivity Analysis Implementation:**
- [ ] Add `sensitivity_analysis()` function to `src/analysis/prioritization.py`
  - Type hints: `def sensitivity_analysis(df: pl.DataFrame, scenarios: Dict[str, Dict[str, float]]) -> Dict[str, pl.DataFrame]`
  - Return dictionary mapping scenario names to ranked DataFrames
  - Log INFO for each scenario: "Running scenario '{name}' with weights: {weights}"
  - Include comprehensive docstring with example showing multiple scenarios
- [ ] Add `calculate_rank_correlation()` function for Spearman correlation
  - Type hints: `def calculate_rank_correlation(rankings: Dict[str, pl.DataFrame]) -> pl.DataFrame`
  - Use `scipy.stats.spearmanr` for pairwise correlations
  - Return correlation matrix as DataFrame (scenarios × scenarios)
  - Log INFO: "Calculated rank correlations: mean={mean:.3f}, min={min:.3f}, max={max:.3f}"
- [ ] Add `identify_consensus_priorities()` function to find stable top-N diseases
  - Type hints: `def identify_consensus_priorities(rankings: Dict[str, pl.DataFrame], top_n: int = 10) -> List[str]`
  - Return list of diseases appearing in top-N across all scenarios
  - Log INFO: "{len(consensus)} diseases in Top {top_n} across all {len(rankings)} scenarios"
  - Include docstring explaining consensus definition
- [ ] Write unit tests for sensitivity analysis functions:
  - Test with 2-3 mock scenarios with known rankings
  - Verify correlation matrix is symmetric and diagonal = 1.0
  - Test consensus priorities with edge cases (no consensus, full consensus)
- [ ] Run tests to validate sensitivity analysis logic: `pytest tests/unit/test_prioritization.py::TestSensitivityAnalysis -v`

**11. Sensitivity Analysis Execution:**
- [ ] **Section 6: Sensitivity Analysis** (in notebook)
  - Load alternative weighting scenarios from `config/prioritization.yml`
  - For each scenario:
    - Calculate composite score with scenario weights
    - Rank diseases
    - Store rankings in dictionary `{scenario_name: rankings_df}`
  - Create consolidated sensitivity table: Diseases × Scenarios with rank values
  - Calculate Spearman rank correlation matrix between all scenarios
  - Identify consensus Top 10 diseases (in Top 10 across all scenarios)
  - Calculate rank volatility: Standard deviation of rank across scenarios per disease
- [ ] Display sensitivity analysis summary:
  - Correlation matrix heatmap
  - Consensus priorities list
  - Diseases with high rank volatility (sensitive to weights)
- [ ] Export sensitivity analysis to `results/tables/sensitivity_analysis.csv`

**12. Robustness Assessment:**
- [ ] Analyze correlation matrix: Expect correlations >0.70 between similar scenarios
- [ ] Validate consensus priorities: Expect Dengue, HFMD consistently in Top 10
- [ ] Identify weight-sensitive diseases: Diseases with high rank volatility
- [ ] Document robustness findings in notebook markdown cell
- [ ] Compare against domain expectations (e.g., major endemic diseases stable, emerging threats may vary)

#### Phase 6: Visualization

**13. Visualization Development:**
- [ ] **Section 7: Visualizations** (in notebook)
- [ ] Use `/create-viz` command to generate publication-quality charts
- [ ] Reference chart selection best practices: `.github/prompts/data-plugin/skills/data-visualization/SKILL.md`
- [ ] **Visualization 1: Priority Rankings Bar Chart**
  - Create horizontal bar chart of Top 20 diseases by composite score
  - Color-code bars by tier (Red >70, Orange 40-70, Green <40)
  - Add score annotations at bar ends
  - Add vertical lines at tier thresholds (70, 40)
  - Title: "Top 20 Infectious Diseases by Composite Burden Score"
  - Save to `results/figures/priority_rankings_bar.png` (300 DPI)
- [ ] **Visualization 2: Tier Distribution**
  - Create grouped bar chart of disease counts by tier
  - Color-code bars by tier
  - Add count and percentage annotations
  - Title: "Disease Distribution Across Priority Tiers"
  - Save to `results/figures/priority_tiers_distribution.png`

**14. Advanced Visualizations:**
- [ ] **Visualization 3: Burden Profiles Radar Charts**
  - Select Top 5 diseases
  - Create radar chart for each with 4 axes: Volume, Trend, Outbreak, Variability
  - Use subplots (2×3 grid) for multiple diseases
  - Normalize all axes to 0-100 scale
  - Title: "Multi-Dimensional Burden Profiles: Top Priority Diseases"
  - Save to `results/figures/burden_profiles_radar.png`
- [ ] **Visualization 4: Sensitivity Heatmap**
  - Create heatmap: Diseases (Top 20) × Scenarios (4 columns)
  - Cell color represents rank (darker = higher priority)
  - Annotate cells with rank numbers
  - Highlight consensus Top 10 diseases (e.g., bold border)
  - Title: "Ranking Stability Across Weighting Scenarios"
  - Save to `results/figures/sensitivity_heatmap.png`
- [ ] Validate all visualizations render correctly
- [ ] Check figure resolution (300 DPI) and sizing (10×8 inches)

#### Phase 7: Documentation & Reporting

**15. Framework Documentation:**
- [ ] Create `docs/methodology/prioritization_framework.md`
- [ ] **Section 1: Overview**
  - Purpose of prioritization framework
  - User roles and use cases
  - High-level methodology summary
- [ ] **Section 2: Criteria Selection & Rationale**
  - Define 4 criteria: Volume, Trend, Outbreak Risk, Variability
  - Explain why each criterion matters for resource allocation
  - Reference domain knowledge sources
  - Document stakeholder validation process (if workshop conducted)
- [ ] **Section 3: Weighting Scheme**
  - Present base case weights: 40/25/20/15
  - Justify weight distribution
  - Explain sensitivity scenarios tested
  - Document stakeholder input on weights (if applicable)
- [ ] **Section 4: Scoring Methodology**
  - Explain normalization approach (min-max to 0-100)
  - Detail composite score formula
  - Describe tier assignment thresholds
  - Include worked example for one disease
- [ ] **Section 5: Results & Rankings**
  - Embed Top 20 rankings table
  - Include tier distribution summary
  - Present consensus Top 10 priorities
  - Highlight key insights (e.g., emerging threats vs. endemic burden)

**16. Executive Summary:**
- [ ] **Section 6: Sensitivity Analysis Findings**
  - Summarize rank stability across scenarios
  - Identify consensus priorities (robust to weight changes)
  - Identify weight-sensitive diseases requiring careful consideration
  - Present correlation matrix
- [ ] **Section 7: Reproducibility**
  - Link to prioritization notebook
  - Link to configuration file
  - Link to prioritization module code
  - Include step-by-step instructions to reproduce rankings
- [ ] **Section 8: Recommendations**
  - Provide policy implications for High/Medium/Low priority tiers
  - Suggest resource allocation strategies per tier
  - Recommend annual framework updates
  - Suggest periodic weight re-validation (every 2-3 years)
- [ ] Proofread documentation for clarity, accuracy, completeness
- [ ] Add metadata: Author, creation date, version, last updated

**17. Stakeholder Presentation Materials:**
- [ ] Create executive summary (2-3 pages) for leadership
  - Key findings: Top 10 priorities, tier distribution, consensus diseases
  - Visualizations: Rankings bar chart, sensitivity heatmap
  - Actionable recommendations: Resource allocation by tier
- [ ] Create data dictionary for prioritization outputs
  - Define all columns in `disease_priority_rankings.csv`
  - Explain score interpretation (0-100 scale)
  - Define tier categories
- [ ] Update `data/4_processed/README.md` with new output file descriptions
- [ ] Add cross-references to methodology document in notebook and README files

#### Phase 8: Quality Assurance & Validation

**18. Analysis Quality Assurance:**
- [ ] Use `/validate` command to QA analysis before stakeholder delivery
- [ ] Follow pre-delivery QA checklist: `.github/prompts/data-plugin/skills/data-validation/SKILL.md`
- [ ] **Data Quality Checks**:
  - Verify input data completeness: All expected ~45 diseases present
  - Validate metric calculations: Manually calculate composite score for 3 sample diseases
  - Check for logical consistency: Higher scores → lower rank numbers
  - Verify no duplicate disease names in output
  - Confirm all output scores in valid range (0-100)
  - Check for null values in critical columns (should be none)
- [ ] **Methodology Validation**:
  - Confirm weighting scheme matches configuration: Parse config and compare
  - Verify tier thresholds applied correctly: Spot-check 5 diseases at boundaries
  - Cross-check sensitivity scenarios executed as defined: Count scenarios, verify names
  - Validate correlation calculations: Check Spearman correlation formula
- [ ] **Domain Validation**:
  - Compare Top 10 against epidemiological expectations documented in domain knowledge
  - Validate Dengue and HFMD in Top 5 (highest burden diseases per preliminary data)
  - Check Salmonellosis in Top 10 (sustained burden)
  - Verify rare diseases (Cholera, Plague, Avian Influenza) in Low Priority tier
  - Confirm vector-borne diseases (Dengue, Chikungunya) have high outbreak scores
  - Validate vaccine-preventable diseases with declining trends have lower trend scores
- [ ] **Statistical Validation**:
  - Check rank correlations are in valid range [-1, 1]
  - Verify consensus priorities list has expected length (Top 10)
  - Validate tier distribution is reasonable (~10-15 High, ~15-25 Medium, ~5-10 Low)
  - Confirm no mathematical errors in weighted sum calculations
- [ ] **Bias & Limitations Check**:
  - Document that framework only considers case volume (not severity, mortality, economic cost, DALYs)
  - Note surveillance biases: Underreporting varies by disease, reporting completeness may differ
  - Acknowledge subjectivity in weighting scheme: Weights based on stakeholder input, not empirical optimization
  - Identify diseases with insufficient data excluded from ranking: List specific diseases
  - Note temporal limitations: Data only through 2020, recent outbreaks (post-2020) not reflected
  - Document aggregation effects: Combined disease categories (e.g., HFMD subtypes) may mask individual variations
- [ ] **Reproducibility Check**:
  - Re-run entire notebook from clean kernel to verify reproducibility
  - Confirm same input data produces same rankings (deterministic)
  - Verify all random seeds set if any stochastic operations used
  - Check all file paths are relative (not absolute) for portability
- [ ] **Code Quality Final Review**:
  - Run `flake8` on all Python modules created: No PEP 8 violations
  - Run `mypy` for type checking: No type errors
  - Verify all functions have docstrings: 100% coverage
  - Check test coverage: ≥90% for prioritization module
  - Review error messages: All are informative with context

**19. Code Review & Peer Review:**
- [ ] **Code Review** (before peer review):
  - Run automated checks:
    - `flake8 src/analysis/prioritization.py notebooks/2_analysis/02_disease_prioritization_framework.ipynb` (PEP 8)
    - `mypy src/analysis/prioritization.py` (type checking)
    - `pytest tests/unit/test_prioritization.py --cov --cov-report=html` (test coverage)
  - Review code quality:
    - Functions have comprehensive docstrings with examples
    - Type hints on all function signatures
    - Error handling with specific exceptions and messages
    - Logging at appropriate levels (INFO, WARNING, ERROR)
    - No hardcoded values (use config or constants)
  - Check notebook quality:
    - Markdown cells explain each section clearly
    - Code cells are well-commented
    - Outputs are visible and interpretable
    - No debugging code or commented-out blocks
  - Address all linting errors and type issues before proceeding
- [ ] **Domain Expert Review**:
  - Request epidemiologist review of rankings
  - Validate methodology with domain expert (disease program manager)
  - Present criteria, weights, and top 10 rankings for feedback
  - Discuss any surprising rankings or omissions
- [ ] **Incorporate Feedback**:
  - Document all reviewer comments in GitHub issues or review notes
  - Prioritize feedback: Critical (must fix), Important (should fix), Nice-to-have
  - Make revisions to weights, criteria, or interpretations as needed
  - Re-run analysis with updated parameters
  - Document changes in methodology document with rationale
- [ ] **Response Documentation**:
  - Create review response document listing all feedback and actions taken
  - For rejected suggestions, document why (out of scope, data limitations, etc.)
  - Update implementation plan status to reflect review completion

**20. Final Validation:**
- [ ] Re-run all notebooks end-to-end to ensure reproducibility
- [ ] Verify all output files present and correctly formatted
- [ ] Check all visualizations render correctly
- [ ] Run unit tests: `pytest tests/unit/test_prioritization.py -v`
- [ ] Validate all tests pass
- [ ] Perform spot-checks on output data (random sample of 5 diseases)
- [ ] Confirm top 10 rankings stable across notebook re-runs
- [ ] Log final validation completion date and approver

#### Phase 9: Deployment & Knowledge Transfer

**21. Security & Privacy Final Check:**
- [ ] **Credential Management Audit**:
  - Scan all code files for hardcoded credentials: `grep -r "password\|api_key\|token" src/ scripts/ notebooks/`
  - Verify no credentials in config files committed to version control
  - Check `.gitignore` includes: `.env`, `*credentials*`, `*secrets*`, `config/*local*`
  - Validate environment variables used for any external service connections
- [ ] **Code Security Review**:
  - No SQL injection vulnerabilities (use parameterized queries if any database access)
  - No command injection vulnerabilities (avoid `os.system()`, use `subprocess` with arguments list)
  - Input validation for all user-supplied parameters (config file paths, disease names)
  - Error messages don't expose sensitive paths or internal system details
- [ ] **Data Privacy Compliance**:
  - Confirm analysis uses aggregated data only (no individual patient records)
  - Verify no PII/PHI in outputs (rankings, visualizations, documentation)
  - Check logging doesn't capture sensitive information
  - Validate file permissions restrict access to authorized users only

**22. Results Delivery:**
- [ ] Package deliverables:
  - `disease_priority_rankings.csv` (full rankings)
  - `sensitivity_analysis.csv` (robustness assessment)
  - All visualizations (4 PNG files)
  - `prioritization_framework.md` (methodology documentation)
  - `prioritization_workshop_summary.md` (stakeholder engagement record, if applicable)
- [ ] Share results with MOH policy makers
- [ ] Present findings in stakeholder meeting (optional)
- [ ] Provide executive summary for leadership decision-making
- [ ] Archive raw outputs and analysis date for audit trail

**22. Knowledge Transfer:**
- [ ] Document framework maintenance procedures
  - How to update weights (edit `config/prioritization.yml`)
  - How to re-run prioritization (execute notebook)
  - When to update framework (annually with new surveillance data)
- [ ] Train handoff recipient on notebook execution
- [ ] Demonstrate configuration changes and sensitivity analysis
- [ ] Provide troubleshooting guidance for common issues
- [ ] Document contact information for technical questions

**23. Framework Maintenance Planning:**
- [ ] Schedule annual prioritization update (e.g., Q1 each year with prior year data)
- [ ] Schedule periodic weight re-validation workshop (every 2-3 years)
- [ ] Define process for ad-hoc prioritization (e.g., if new outbreak emerges)
- [ ] Document version control approach for configuration changes
- [ ] Establish data retention policy for historical rankings (compare year-over-year)

**24. Finalization:**
- [ ] Update user story status: Mark implementation complete
- [ ] Close all related GitHub issues or project tracking items
- [ ] Archive project documentation in shared repository
- [ ] Celebrate successful completion! 🎉

---

### Data Quality & Validation Strategy

#### Pipeline-Stage Data Quality Checks

**Stage 1: Input Data Validation** (Burden Metrics)
- **Completeness**: All 45-46 diseases present in input file
- **Required Columns**: Verify presence of `disease_name`, `sufficient_data`, `*_score` columns
- **Score Range**: All input scores in 0-100 range (normalized in User Story 2)
- **Sufficient Data Flag**: Only process diseases with `sufficient_data == true` (expect ~40-45 diseases)
- **Missing Values**: No null values in required score columns for included diseases
- **Data Freshness**: Check input file timestamp (should be from User Story 2 execution)

**Stage 2: Criteria Aggregation Validation**
- **Volume Criterion**: Verify average of `total_cases_score` and `annual_avg_cases_score` in 0-100 range
- **Score Completeness**: All four criteria (Volume, Trend, Outbreak, Variability) populated for all diseases
- **Statistical Checks**: 
  - Mean criterion score ~50 (normalized scale)
  - No criterion score >100 or <0
  - Standard deviation >0 (criteria should vary across diseases)

**Stage 3: Composite Score Validation**
- **Weighting Constraint**: Weights sum to 100% (validated in configuration loading)
- **Score Calculation**: Spot-check 3 diseases manually: Calculate weighted sum, compare to computed score
- **Score Range**: All composite scores in 0-100 range
- **Distribution**: Expect relatively normal distribution of composite scores (not all near 0 or 100)

**Stage 4: Ranking & Tier Validation**
- **Rank Sequence**: No gaps in rank numbers (1, 2, 3, ..., N)
- **Rank-Score Consistency**: Higher composite score → lower rank number (rank 1 = highest score)
- **Tier Assignment**: 
  - All High Priority diseases have score >70
  - All Medium Priority diseases have score 40-70
  - All Low Priority diseases have score <40
  - Boundary cases (exact 70.0, 40.0) assigned correctly
- **Tier Distribution**: Expect ~10-15 High, ~15-25 Medium, ~5-10 Low priority diseases (based on domain guidance)

**Stage 5: Sensitivity Analysis Validation**
- **Scenario Completeness**: Rankings calculated for all defined scenarios (Base Case + 3 alternatives)
- **Correlation Matrix**: All pairwise correlations computed, expect >0.70 for similar scenarios
- **Consensus Priorities**: Top-N list has expected length, contains major endemic diseases (Dengue, HFMD)
- **Rank Volatility**: Standard deviation of rank calculated for all diseases

**Stage 6: Output Validation**
- **File Creation**: All expected output files created (`disease_priority_rankings.csv`, `sensitivity_analysis.csv`, 4 PNG figures)
- **CSV Schema**: Verify column names and data types in output CSVs
- **Visualization Rendering**: All figures display correctly (no blank images, correct labels)
- **Data Completeness**: Output files contain all expected diseases and scenarios

#### Testability Requirements

**Code Design for Testability**:
- **Modular Functions**: Each prioritization step (normalization, scoring, ranking, tier assignment) in separate function
  - Functions should be <50 lines, single responsibility
  - Avoid nested functions or complex lambda expressions
- **Clear Inputs/Outputs**: Functions accept DataFrames and config dicts, return DataFrames
  - Use type hints for all parameters and return values
  - Document input/output shapes and expected columns in docstrings
- **No Side Effects**: Functions don't modify input DataFrames (use `.clone()` in Polars)
  - All transformations return new DataFrames
  - No global variable modifications
  - No file I/O within core logic functions (separate I/O functions)
- **Configuration-Driven**: Weights and thresholds from config, not hardcoded
  - All magic numbers externalized to config file or constants module
  - Default values specified in function signatures
- **Structured Logging**: Use module-level logger with appropriate levels
  - **INFO**: Function entry/exit, data loaded, calculations completed
  - **WARNING**: Data quality issues, diseases excluded, assumptions made
  - **ERROR**: Validation failures, processing errors, exceptions
  - Include context in log messages: counts, values, parameters
- **Comprehensive Error Handling**: 
  - **Input Validation Errors**:
    - `ValueError(f"Weights sum to {sum(weights.values()):.3f}, must equal 1.0 (±0.001)")` if weights invalid
    - `KeyError(f"Missing required columns: {set(required) - set(df.columns)}")` if columns missing
    - `ValueError(f"Scores out of range [0,100] in columns: {out_of_range}")` if invalid scores
  - **Data Quality Warnings**:
    - `logger.warning(f"Excluding {n_excluded} diseases with insufficient data")` for filtered records
    - `logger.warning(f"Found {n_ties} tied scores at rank {rank}")` for ranking ties
  - **Exception Handling in Notebooks**:
    - Wrap file operations in try-except blocks
    - Log exceptions with traceback: `logger.exception("Failed to load data")`
    - Provide helpful error messages for common issues (file not found, permission denied)
- **Defensive Programming**:
  - Check for empty DataFrames before processing: `if df.is_empty(): raise ValueError("Input DataFrame is empty")`
  - Validate numeric ranges before calculations: `assert (df['score'] >= 0).all() and (df['score'] <= 100).all()`
  - Use `.get()` for dictionary access with defaults: `weight = weights.get('volume', 0.4)`

**Unit Test Assertions**:
- **Schema Validation**: `assert set(df.columns) == expected_columns`
- **Range Validation**: `assert df['composite_score'].min() >= 0 and df['composite_score'].max() <= 100`
- **Mathematical Correctness**: `assert abs(computed_score - expected_score) < 1e-6` (manual calculation)
- **Tier Assignment**: `assert (df.filter(pl.col('tier') == 'High')['composite_score'] > 70).all()`
- **Rank Uniqueness**: `assert df['rank'].is_unique().all()`
- **Consistency**: Same input → same output across runs (deterministic calculations)

**Data Quality Checks** (in notebook):
```python
# Example validation code snippets
assert df.filter(pl.col('sufficient_data') == True).shape[0] >= 40, "Insufficient diseases with adequate data"
assert df['composite_score'].min() >= 0 and df['composite_score'].max() <= 100, "Score out of range"
assert df.filter(pl.col('tier') == 'High').shape[0] < df.shape[0] / 2, "Too many high priority diseases"
```

#### Domain-Specific Validation Criteria

**Expected Top Priorities** (from domain knowledge and preliminary exploration):
1. **Hand, Foot and Mouth Disease**: Highest volume (~235K cases)
2. **Dengue Fever**: High volume (~127K cases), frequent outbreaks
3. **Salmonellosis**: Sustained high burden (~16K cases), stable trend
4. **Dengue Haemorrhagic Fever**: Severe form, high outbreak intensity
5. **Campylobacter variants**: Foodborne threat, consistent cases

**Validation Checks**:
- HFMD and Dengue in Top 5 (if not, investigate scoring logic)
- Rare diseases (Cholera, Plague, Avian Influenza) in Low Priority tier
- Vector-borne diseases (Dengue, Chikungunya, Zika) have high outbreak scores
- Vaccine-preventable diseases with declining trends (Measles, Rubella) have lower trend scores
- High-variability diseases (Dengue, Zika) have lower variability scores (CV-based)

**Threshold Validation**:
- High Priority tier (~10-15 diseases): Manageable focus for policy attention
- If <5 High Priority: Thresholds too strict, consider lowering high threshold to 65
- If >20 High Priority: Thresholds too loose, consider raising high threshold to 75

---

### Statistical Analysis & Model Development

**Not Applicable**: This user story does not involve statistical modeling or predictive analytics. The framework uses descriptive statistics and multi-criteria decision analysis (weighted scoring), not inferential statistics or machine learning models.

**Analytical Methods Used**:
- **Descriptive Statistics**: Distribution of composite scores, tier counts, top rankings
- **Normalization**: Min-max scaling to 0-100 (deterministic transformation, not statistical estimation)
- **Sensitivity Analysis**: Recalculate rankings under alternative weights, assess robustness
- **Correlation Analysis**: Spearman rank correlation between scenarios (non-parametric association measure)

**No Hypothesis Testing**: Framework is a decision support tool, not a statistical inference exercise.

---

### Model Operations & Governance

**Not Applicable**: No machine learning models are trained, deployed, or monitored in this user story. The prioritization framework is a transparent, rule-based scoring system, not a predictive model.

---

### UI/Dashboard Visual Testing

**Not Applicable**: This user story does not involve interactive dashboards or UI components. Outputs are static visualizations (PNG figures) and tabular data (CSV files) for stakeholder review.

**Manual Visual Inspection**:
- Review all PNG figures for correct rendering, labels, colors
- Verify bar chart colors match tier definitions (Red/Orange/Green)
- Check heatmap annotations readable and correctly placed
- Ensure radar charts axes labeled and scaled correctly

---

### Success Metrics & Monitoring

#### Business Success Metrics

**Prioritization Framework Adoption**:
- **Target**: MOH policy makers use rankings in resource allocation decisions within 6 months
- **Measure**: Number of strategic planning documents citing prioritization framework

**Stakeholder Confidence**:
- **Target**: >80% of workshop participants agree framework is credible and useful
- **Measure**: Post-workshop survey on framework transparency and utility

**Decision Impact**:
- **Target**: High Priority diseases receive proportionally more budget allocation in next fiscal cycle
- **Measure**: Budget allocation correlation with tier assignment

#### Technical Success Metrics

**Reproducibility**:
- **Target**: Framework can be re-run annually with new data without modifications
- **Measure**: Successful execution of notebook with updated burden metrics file

**Robustness**:
- **Target**: Top 10 rankings stable across 3+ weighting scenarios (consensus priorities)
- **Measure**: Spearman correlation >0.80 between scenarios, 80% overlap in Top 10

**Transparency**:
- **Target**: All calculations auditable with clear methodology documentation
- **Measure**: Stakeholder feedback that framework logic is understandable

#### Monitoring & Alerting

**No Real-Time Monitoring**: Prioritization is an annual batch process, not a production system requiring alerting.

**Annual Review Checklist**:
- Verify burden metrics updated with latest year's data
- Re-run prioritization notebook
- Compare current rankings to prior year (rank changes >5 positions warrant investigation)
- Review weighting scheme relevance (update if strategic priorities shifted)
- Document year-over-year changes in top priorities

---

### References

**Domain Knowledge Documents**:
- [Disease Burden Assessment Methodology](../../../docs/domain_knowledge/disease-burden-assessment-methodology.md) - Multi-criteria prioritization framework (lines 189-211), burden metrics definitions (lines 39-58), common pitfalls and best practices (lines 268-292)

**Project Context**:
- [Data Sources](../../../docs/project_context/data-sources.md) - Kaggle health dataset structure and access methods
- [Tech Stack](../../../docs/project_context/tech-stack.md) - Python/Polars analytical environment

**Data Artifacts**:
- `data/4_processed/disease_burden_metrics.csv` - Input burden metrics from User Story 2
- `data/4_processed/README.md` - Processed data documentation

**Related User Stories**:
- [User Story 2: Calculate Comprehensive Burden Metrics](02-calculate-comprehensive-burden-metrics.md) - Provides input burden metrics for prioritization

**Data Plugin Skills** (for acceleration):
- `/create-viz` command - Generate publication-quality visualizations
- `/validate` command - Pre-delivery QA checklist
- `.github/prompts/data-plugin/skills/data-visualization/SKILL.md` - Chart selection best practices
- `.github/prompts/data-plugin/skills/data-validation/SKILL.md` - Common pitfalls and validation checklist
