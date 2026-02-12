# Domain Knowledge: Disease Burden Assessment Methodology

## Overview
This document provides methodologies, frameworks, and analytical approaches for assessing infectious disease burden across multiple dimensions. It supports MOH policy makers and disease program managers in making evidence-based resource allocation and prioritization decisions based on comprehensive burden analysis.

## Related Problem Statements
- [Problem Statement PS-002 - Disease Burden Assessment & Resource Prioritization](../objectives/problem_statements/ps-002-disease-burden-prioritization.md)

## Related Stakeholders
- **MOH Policy Makers**: Use burden rankings for budget allocation and program prioritization
- **Disease Control Program Managers**: Justify program funding based on evidence-based burden metrics
- **Public Health Surveillance Leadership**: Prioritize monitoring and intervention strategies
- **Healthcare Finance Committees**: Evaluate cost-benefit of disease control programs

## Key Concepts and Terminology

### Disease Burden
**Definition**: The impact of a health problem on a population, measured by multiple indicators including case volume, severity, mortality, economic cost, and social disruption
**Relevance**: Comprehensive burden assessment guides resource allocation decisions
**Components**:
  - **Morbidity**: Number of cases, illness duration, disability
  - **Mortality**: Deaths attributable to disease
  - **Economic Impact**: Healthcare costs, productivity loss
  - **Social Impact**: Quality of life, social disruption
**Example**: Dengue may have high morbidity (126,000+ cases) but low mortality, while Ebola has low morbidity but extreme severity

### Multi-Criteria Decision Analysis (MCDA)
**Definition**: Structured approach to evaluate options based on multiple, often conflicting criteria
**Relevance**: Disease prioritization requires balancing case volume, growth trends, outbreak frequency, severity
**Approaches**:
  - **Weighted Scoring**: Assign weights to criteria, score each disease, calculate composite
  - **Analytic Hierarchy Process (AHP)**: Pairwise comparisons to derive weights
  - **TOPSIS**: Rank by distance to ideal solution
**Use Case**: MOH may weight case volume 40%, growth rate 30%, outbreak frequency 30% to rank diseases

### Burden Metrics

#### Absolute Burden
**Definition**: Total impact measured in absolute terms (total cases, total deaths)
**Relevance**: Identifies high-volume diseases requiring substantial resources
**Interpretation**: Larger numbers indicate greater population health impact
**Example**: Dengue = 126,642 total cases vs. Cholera = 45 cases → Dengue has higher absolute burden

#### Relative Burden  
**Definition**: Impact measured relative to other diseases or population
**Relevance**: Enables cross-disease comparison and benchmarking
**Metrics**: Incidence rate, percent of total infectious disease cases, ranking percentile
**Example**: Dengue = 28% of all infectious disease cases (highest proportion)

#### Trend-Based Burden
**Definition**: Burden trajectory over time (increasing, stable, decreasing)
**Relevance**: Emerging threats may have low current burden but high future risk
**Interpretation**: 
  - Increasing trend signals growing problem requiring intervention
  - Decreasing trend indicates successful control or natural decline
**Example**: Zika cases surged 2016 (emerging threat) then declined (outbreak ended)

#### Outbreak Burden
**Definition**: Frequency and magnitude of epidemic spikes above endemic baseline
**Relevance**: Outbreak-prone diseases strain healthcare capacity unpredictably
**Metrics**: Number of outbreak weeks, peak magnitude, outbreak duration
**Example**: Dengue has annual outbreaks; HFMD has biennial pattern

## Standard Metrics and KPIs

| Metric Name | Definition | Calculation Formula | Typical Range | Use Case | Data Requirements |
|-------------|-----------|---------------------|---------------|----------|-------------------|
| Total Case Count | Cumulative cases over analysis period | Sum of all weekly cases | 0 to 160,000+ (disease-specific) | Absolute burden ranking | Weekly case data |
| Annual Average Cases | Mean cases per year | Total cases / Number of years | 0 to 18,000+ | Normalize for time period differences | Multi-year data |
| Incidence Rate | Cases per 100,000 population | (Total cases / Population) × 100,000 | 0 to 2,500+ per 100K | Population-adjusted burden | Cases, population |
| Compound Annual Growth Rate (CAGR) | Average annual growth over period | ((Final/Initial)^(1/years) - 1) × 100 | -20% to +50% | Trend analysis | Multi-year time series |
| Outbreak Frequency | Number of outbreak episodes | Count of periods exceeding threshold | 0-50+ outbreaks | Predictability assessment | Weekly cases, threshold |
| Peak-to-Baseline Ratio | Outbreak magnitude | Maximum cases / Median baseline | 2-20x | Outbreak intensity measure | Peak cases, baseline |
| Coefficient of Variation (CV) | Volatility of cases | (Standard Deviation / Mean) × 100 | 10%-200%+ | Stability assessment | Weekly cases |
| Seasonal Strength | Amplitude of seasonal pattern | (Seasonal component range / Mean) | 0-2+ | Predictability measure | Seasonal decomposition |
| Burden Score | Composite weighted metric | Σ(weight_i × normalized_metric_i) | 0-100 scale | Holistic ranking | All burden metrics |

## Feature Engineering Guidance

### Common Features for Disease Burden Assessment

#### Volume Features
- **Total Cases**: Cumulative count over entire period
  - **Description**: Sum of all weekly cases from 2012-2020
  - **Calculation**: Sum(weekly_cases)
  - **Interpretation**: Absolute disease burden on healthcare system
  - **Use Cases**: Initial prioritization, resource needs estimation
  - **Example**: Dengue = 126,642 cases ranks #2 overall

- **Annual Average Cases**: Mean yearly case count
  - **Description**: Average cases per year
  - **Calculation**: Total cases / 9 years
  - **Interpretation**: Normalized for time period; enables fair comparison
  - **Use Cases**: Diseases with partial data coverage
  - **Example**: HFMD annual average = 8,214 cases/year

- **Peak Weekly Cases**: Maximum cases in single week
  - **Description**: Highest weekly case count observed
  - **Calculation**: Max(weekly_cases)
  - **Interpretation**: Surge capacity requirement; outbreak intensity
  - **Use Cases**: Capacity planning, outbreak preparedness
  - **Example**: Dengue peak = 1,791 cases in one week during 2013 outbreak

#### Trend Features
- **Linear Trend Coefficient**: Slope of cases over time
  - **Description**: Rate of change per week
  - **Calculation**: Linear regression slope (cases ~ time)
  - **Interpretation**: Positive = increasing; Negative = decreasing
  - **Use Cases**: Identify emerging vs. declining diseases
  - **Example**: Zika +50 cases/week in 2016, then -20 cases/week in 2017-2018

- **Compound Annual Growth Rate (CAGR)**: Average yearly growth
  - **Description**: Geometric mean of annual growth rates
  - **Calculation**: ((Final_year / First_year)^(1/n_years) - 1) × 100
  - **Interpretation**: Consistent growth/decline rate
  - **Use Cases**: Long-term projections, program evaluation
  - **Example**: Dengue CAGR = +8% suggests growing burden

- **Trend Direction**: Categorical trend classification
  - **Description**: Increasing, Stable, Decreasing based on slope significance
  - **Calculation**: Statistical test of trend slope (p < 0.05)
  - **Interpretation**: Clear directional signal for policy
  - **Use Cases**: Prioritize increasing diseases, reduce focus on decreasing
  - **Example**: "Measles: Stable" vs. "HFMD: Increasing"

#### Variability Features
- **Coefficient of Variation (CV)**: Relative volatility
  - **Description**: Standard deviation as percentage of mean
  - **Calculation**: (Std Dev / Mean) × 100
  - **Interpretation**: Higher = more volatile, unpredictable
  - **Use Cases**: Risk assessment, forecast difficulty
  - **Example**: Dengue CV = 120% (high volatility) vs. Tuberculosis CV = 15% (stable)

- **Interquartile Range (IQR)**: Spread of middle 50% of data
  - **Description**: Difference between 75th and 25th percentiles
  - **Calculation**: Q3 - Q1
  - **Interpretation**: Robust measure of spread (less affected by outliers)
  - **Use Cases**: Outlier detection, typical case range
  - **Example**: HFMD IQR = 150-350 cases/week (typical range)

- **Outbreak Intensity Score**: Magnitude of spikes above baseline
  - **Description**: Average peak-to-baseline ratio during outbreaks
  - **Calculation**: Mean(peak_cases / baseline) for outbreak periods
  - **Interpretation**: How severe outbreaks become relative to normal
  - **Use Cases**: Outbreak response resource requirements
  - **Example**: Dengue intensity = 5x baseline vs. Salmonellosis = 1.5x

#### Outbreak Features
- **Outbreak Frequency**: Number of outbreak episodes
  - **Description**: Count of distinct outbreak periods
  - **Calculation**: Count periods where cases exceed threshold (e.g., mean + 2 SD)
  - **Interpretation**: How often disease surges unpredictably
  - **Use Cases**: Outbreak preparedness planning, resource buffering
  - **Example**: Dengue = 8 outbreaks over 9 years (nearly annual)

- **Outbreak Duration**: Average length of outbreak episodes
  - **Description**: Mean number of consecutive weeks above threshold
  - **Calculation**: Average duration of outbreak periods
  - **Interpretation**: Sustained vs. brief spikes
  - **Use Cases**: Staffing duration planning, alert fatigue management
  - **Example**: Dengue outbreaks average 12 weeks vs. HFMD 6 weeks

- **Weeks Above Threshold**: Proportion of time in outbreak state
  - **Description**: Percentage of weeks exceeding outbreak threshold
  - **Calculation**: (Weeks above threshold / Total weeks) × 100
  - **Interpretation**: Chronic outbreak vs. rare spikes
  - **Use Cases**: Distinguish endemic-elevated from outbreak-prone
  - **Example**: Dengue 25% of weeks in outbreak vs. Zika 2%

### Domain-Specific Patterns

#### Disease Clustering by Characteristics
**Description**: Group diseases with similar burden profiles for targeted strategies
**When to Apply**: Developing differentiated resource allocation approaches
**Implementation**: K-means clustering on normalized burden metrics; hierarchical clustering for interpretability
**Example Clusters**:
  - **High-Volume Endemic**: HFMD, Dengue (high cases, predictable seasonality)
  - **Low-Volume Outbreak-Prone**: Zika, Chikungunya (rare but epidemic potential)
  - **Stable Low-Burden**: Cholera, Plague (consistently low, maintenance mode)
**Policy Implication**: Each cluster requires different resource strategy (sustained capacity vs. surge capability vs. minimal monitoring)

#### Seasonality Pattern Recognition
**Description**: Identify and quantify seasonal disease patterns for forecasting
**When to Apply**: Diseases with recurring annual patterns
**Implementation**: Seasonal decomposition (STL), Fourier analysis, autocorrelation plots
**Example**: Dengue shows strong seasonality (Jun-Oct peak, Dec-Mar trough)

#### Trend Break Detection
**Description**: Identify time points where disease trajectory changes
**When to Apply**: Policy impact evaluation, outbreak onset detection
**Implementation**: PELT algorithm, Bayesian change point detection, CUSUM charts
**Example**: Zika 2016 surge represents structural break; analyze pre/post separately

## Multi-Criteria Prioritization Framework

### Step 1: Define Prioritization Criteria
**Common Criteria**:
1. **Case Volume** (40% weight): Total or annual average cases
2. **Trend** (25% weight): CAGR, trend direction
3. **Outbreak Risk** (20% weight): Outbreak frequency, intensity
4. **Volatility** (15% weight): Coefficient of variation

**Stakeholder Input**: Weights should be validated through stakeholder workshop

### Step 2: Normalize Metrics
**Purpose**: Convert different scales to comparable 0-100 scale
**Method**: Min-max normalization
```
Normalized = (Value - Min) / (Max - Min) × 100
```
**Example**: Dengue 126,642 cases on scale 0-161,482 = 78.4 normalized score

### Step 3: Calculate Composite Burden Score
```
Burden Score = (0.40 × Volume Score) + (0.25 × Trend Score) + 
               (0.20 × Outbreak Score) + (0.15 × Volatility Score)
```

### Step 4: Rank and Tier Diseases
**Tiers**:
- **Tier 1 (High Priority)**: Burden Score > 70
- **Tier 2 (Medium Priority)**: Burden Score 40-70
- **Tier 3 (Low Priority)**: Burden Score < 40

### Step 5: Sensitivity Analysis
**Purpose**: Test robustness of rankings to different weighting schemes
**Method**: Vary weights, recalculate scores, compare rankings
**Example**: If dengue ranks #1 under all reasonable weight variations, ranking is robust

## Analytical Methodologies

### Descriptive Burden Analysis
**Application**: Comprehensive characterization of disease burden landscape
**Methods**: Summary statistics, distribution analysis, temporal trends, cross-disease comparison
**Deliverable**: Disease burden profile cards, comparative tables, trend visualizations

### Time Series Decomposition
**Application**: Separate trend, seasonal, and irregular components
**Methods**: STL decomposition, moving averages, Hodrick-Prescott filter
**Deliverable**: Decomposed time series plots showing underlying patterns

### Trend Analysis
**Application**: Identify diseases with increasing/decreasing burden
**Methods**: Linear regression, Mann-Kendall test, Theil-Sen slope estimator
**Deliverable**: Trend classification (increasing/stable/decreasing) with significance levels

### Outbreak Detection
**Application**: Define and quantify outbreak episodes
**Methods**: Threshold-based (mean + 2 SD), EARS algorithms, Farrington algorithm
**Deliverable**: Outbreak timeline, frequency metrics, intensity measures

### Comparative Benchmarking
**Application**: Assess burden relative to peers or international standards
**Methods**: Percentile ranking, ratio to median, Z-scores
**Deliverable**: Disease rankings, priority tiers, international comparisons

## Common Pitfalls and Best Practices

### Pitfalls to Avoid
- **Case counts don't equal severity**: High-volume disease may be mild (HFMD) while rare disease deadly (Ebola). Document limitation; incorporate severity data if available
- **Surveillance artifacts**: Changes in reporting, testing, or case definitions create artificial trends. Check for surveillance system changes
- **Underreporting varies by disease**: Some diseases (STIs) underreported more than others. Acknowledge limitation
- **Weighting bias**: Subjective weights favor certain diseases. Use sensitivity analysis, stakeholder consensus
- **Short-term trends**: Recent spike doesn't guarantee ongoing increase. Use multi-year data, statistical tests
- **Ignoring external factors**: Policy interventions, vaccination campaigns affect burden. Document contextual factors

### Best Practices
- **Use multiple metrics**: Single metric misleading; composite view more robust
- **Normalize for comparison**: Different scales (0-100 vs. 0-100,000) require standardization
- **Validate with stakeholders**: Epidemiologists can identify data artifacts, context
- **Document methodology transparently**: Reproducibility and trust require clear explanation
- **Update annually**: Burden changes; rankings should refresh as new data arrives
- **Communicate uncertainty**: Confidence intervals, data quality flags maintain credibility
- **Scenario analysis**: Show rankings under different assumptions (weights, metrics)

## Visualization Best Practices

### Disease Burden Heatmap
**Purpose**: Show multiple burden dimensions simultaneously
**Format**: Rows = diseases, Columns = metrics, Color intensity = normalized score
**Example**: High burden diseases appear as dark rows across multiple columns

### Trend Line Charts
**Purpose**: Visualize temporal patterns for top diseases
**Format**: Line plot with case counts over time, separate line per disease
**Best Practice**: Include smoothed trend line, highlight outbreak periods

### Bubble Charts
**Purpose**: Display 3+ dimensions (e.g., case volume, growth rate, outbreak frequency)
**Format**: X-axis = volume, Y-axis = trend, Bubble size = outbreak frequency
**Advantage**: Identify outliers, natural groupings

### Ranking Tables
**Purpose**: Clear prioritization for decision-makers
**Format**: Sorted list with rank, disease name, key metrics, tier classification
**Best Practice**: Include uncertainty indicators (confidence intervals, sensitivity notes)

## References and Sources

### Authoritative Sources
- **World Health Organization (WHO)**: https://www.who.int/health-topics/disease-burden - Global disease burden frameworks
- **Institute for Health Metrics and Evaluation (IHME)**: https://www.healthdata.org/ - Global Burden of Disease study methodologies
- **US CDC**: https://www.cdc.gov/surveillance/ - Surveillance and burden assessment guidance
- **European CDC**: https://www.ecdc.europa.eu/ - Multi-criteria decision analysis for disease prioritization

### Academic References
- Murray CJ, Lopez AD. "Measuring the Global Burden of Disease." New England Journal of Medicine (2013)
- Cox LA. "What's Wrong with Risk Matrices?" Risk Analysis (2008)
- Baltussen R, Niessen L. "Priority Setting of Health Interventions: The Need for Multi-Criteria Decision Analysis." Cost Effectiveness and Resource Allocation (2006)

### Industry Standards
- **WHO Global Health Estimates**: Standardized burden metrics across countries
- **DALY (Disability-Adjusted Life Year)**: Combined measure of morbidity and mortality
- **QALY (Quality-Adjusted Life Year)**: Health outcome measure for economic evaluation

## Cross-References

### Related Domain Knowledge Files
- [Infectious Disease Epidemiology Terminology](infectious-disease-epidemiology-terminology-glossary.md) - Core surveillance concepts
- [Time Series Forecasting Best Practices](time-series-forecasting-best-practices.md) - Trend analysis methods

### Related Data Dictionary Entries
- [Infectious Disease Bulletin](../data_dictionary/infectious_disease_bulletin.md) - Weekly case data structure

## Metadata

**Created**: 9 February 2026
**Last Updated**: 9 February 2026
**Updated By**: GitHub Copilot (Claude Sonnet 4.5)
**Update Reason**: Initial creation to support PS-002 disease burden assessment
**Version**: 1.0

## Notes

This framework is designed for infectious disease burden assessment using case count data. For comprehensive burden assessment, consider incorporating:
- **Mortality data**: Case fatality rates, deaths attributable
- **Economic burden**: Healthcare costs, productivity loss
- **Disability**: Duration and severity of illness (DALYs)
- **Geographic distribution**: Identify high-burden regions
- **Demographic impact**: Age groups most affected

These additional dimensions require data beyond the weekly infectious disease bulletin dataset.
