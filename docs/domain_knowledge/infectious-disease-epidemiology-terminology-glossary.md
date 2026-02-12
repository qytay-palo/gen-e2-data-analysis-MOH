# Domain Knowledge: Infectious Disease Epidemiology Terminology

## Overview
This document provides essential epidemiological terminology, concepts, and definitions for infectious disease surveillance and analysis in Singapore's healthcare context. It supports MOH stakeholders in understanding surveillance data, interpreting analytical results, and making evidence-based public health decisions.

## Related Problem Statements
- [Problem Statement PS-001 - Seasonal Outbreak Forecasting](../objectives/problem_statements/ps-001-seasonal-outbreak-forecasting.md)
- [Problem Statement PS-002 - Disease Burden Assessment](../objectives/problem_statements/ps-002-disease-burden-prioritization.md)

## Related Stakeholders
- **MOH Policy Makers**: Use terminology to interpret disease trends and make resource allocation decisions
- **Public Health Surveillance Teams**: Apply concepts in routine monitoring and outbreak detection
- **Healthcare Facility Committees**: Understand disease patterns to inform capacity planning
- **Epidemiologists**: Validate analytical approaches and methodologies

## Key Concepts and Terminology

### Epidemiological Week (Epi-Week)
**Definition**: A standardized week numbering system used in disease surveillance, following the ISO 8601 week date system
**Relevance**: Enables consistent temporal comparison of disease patterns across years and jurisdictions
**Singapore Implementation**: Week starts Sunday, ends Saturday; Week 1 is the first week with at least 4 days in January
**Example**: 2020-W01 refers to the first epidemiological week of 2020

### Incidence
**Definition**: Number of new cases of a disease occurring in a defined population during a specified time period
**Relevance**: Primary metric for measuring disease occurrence and trends
**Calculation**: Case count in period / population at risk
**Example**: 1,200 dengue cases in Week 20 among Singapore's 5.7M residents = 21.1 cases per 100,000 population

### Prevalence
**Definition**: Proportion of a population that has a disease at a specific point in time
**Relevance**: Indicates disease burden at a given moment; less common for acute infectious diseases
**Use Case**: More applicable to chronic infections (e.g., hepatitis B) than acute diseases (e.g., dengue)

### Attack Rate
**Definition**: Proportion of a population that develops disease during an outbreak
**Relevance**: Measures outbreak severity and transmission intensity
**Calculation**: (New cases during outbreak / Population at risk) × 100
**Example**: If 500 of 10,000 school children develop HFMD during an outbreak, attack rate = 5%

### Case Definition
**Definition**: Standardized criteria for identifying whether a person has a particular disease
**Relevance**: Ensures consistency in disease reporting and surveillance
**Categories**:
  - **Confirmed**: Laboratory-confirmed diagnosis
  - **Probable**: Clinical criteria met but no lab confirmation
  - **Suspected**: Some clinical features present

### Notifiable Disease
**Definition**: Disease that healthcare providers are legally required to report to public health authorities
**Relevance**: Singapore's Infectious Diseases Act mandates reporting of 45 notifiable diseases
**Example**: Dengue, HFMD, measles, tuberculosis

### Outbreak / Epidemic
**Definition**: Occurrence of disease cases in excess of normal expectancy in a community or region
**Relevance**: Triggers enhanced surveillance and response measures
**Threshold**: Disease-specific; typically 2+ standard deviations above historical baseline
**Example**: Dengue cases exceeding 500/week may signal outbreak, depending on season

### Endemic
**Definition**: Constant presence of a disease in a population within a geographic area
**Relevance**: Distinguishes baseline disease presence from outbreak conditions
**Example**: Dengue is endemic in Singapore with predictable seasonal patterns

### Pandemic
**Definition**: Epidemic occurring over a very wide area (multiple countries/continents) affecting a large proportion of the population
**Relevance**: Requires national-level response coordination
**Example**: COVID-19, H1N1 influenza

### Seasonality
**Definition**: Predictable, recurring pattern of disease incidence associated with specific times of the year
**Relevance**: Critical for forecasting and resource planning
**Example**: Dengue peaks during warmer, wetter months (typically May-October in Singapore)

### Basic Reproduction Number (R₀)
**Definition**: Average number of secondary infections produced by one infected individual in a completely susceptible population
**Relevance**: Indicates transmissibility and outbreak potential
**Interpretation**:
  - R₀ < 1: Disease will die out
  - R₀ > 1: Disease can spread in population
**Example**: Measles R₀ = 12-18 (highly contagious); Dengue R₀ = 1-3 (moderate)

### Epidemic Curve (Epi-Curve)
**Definition**: Visual display of disease outbreak cases over time
**Relevance**: Identifies outbreak patterns, transmission mode, and intervention effectiveness
**Types**:
  - **Point source**: Single exposure event (sharp peak)
  - **Continuous common source**: Ongoing exposure (plateau)
  - **Propagated**: Person-to-person spread (successively larger peaks)

### Surveillance
**Definition**: Ongoing systematic collection, analysis, and interpretation of health data for public health action
**Types**:
  - **Passive**: Healthcare providers report cases to authorities
  - **Active**: Public health actively seeks cases
  - **Syndromic**: Monitors symptoms rather than confirmed diagnoses
**Singapore Approach**: Primarily passive surveillance for notifiable diseases; active for high-priority threats

### Contact Tracing
**Definition**: Identification and monitoring of persons exposed to an infected individual
**Relevance**: Essential for containing outbreaks of contagious diseases
**Application**: Used extensively for TB, COVID-19, measles

### Quarantine vs. Isolation
**Quarantine**: Separation of persons exposed but not yet ill
**Isolation**: Separation of persons who are ill and infectious
**Relevance**: Legal powers under Infectious Diseases Act

### Vector-borne Disease
**Definition**: Disease transmitted by living organisms (vectors) such as mosquitoes, ticks
**Relevance**: Major disease category in Singapore
**Examples**: Dengue (Aedes mosquito), Zika (Aedes mosquito), malaria (Anopheles mosquito)

### Foodborne Disease
**Definition**: Disease caused by consuming contaminated food or water
**Relevance**: Significant burden in Singapore's food service industry
**Examples**: Salmonellosis, campylobacteriosis, hepatitis A

### Vaccine-Preventable Disease
**Definition**: Disease for which effective vaccines exist
**Relevance**: Vaccination programs reduce disease burden
**Examples**: Measles, mumps, rubella, diphtheria, pertussis

### Herd Immunity
**Definition**: Protection of susceptible individuals when a sufficient proportion of the population is immune
**Relevance**: Target for vaccination programs
**Threshold**: Disease-specific; measles requires ~95% coverage

### Lag Time
**Definition**: Delay between disease occurrence and reporting/detection
**Relevance**: Affects timeliness of outbreak response; forecasting must account for reporting delays
**Singapore Context**: Weekly bulletin published ~1 week after epi-week ends

## Standard Metrics and KPIs

| Metric Name | Definition | Calculation Formula | Typical Range | Use Case | Data Requirements |
|-------------|-----------|---------------------|---------------|----------|-------------------|
| Weekly Incidence Rate | Cases per 100,000 population per week | (Weekly cases / Population) × 100,000 | 0-500+ (disease-specific) | Trend monitoring, benchmarking | Weekly cases, population |
| Case Fatality Rate (CFR) | Proportion of cases who die | (Deaths / Cases) × 100 | 0.1%-10% (disease-specific) | Severity assessment | Cases, deaths |
| Moving Average | Smoothed trend over n weeks | Sum(cases in n weeks) / n | Varies | Reduce noise in surveillance | Weekly cases |
| Percent Change | Growth/decline rate | ((Current - Previous) / Previous) × 100 | -50% to +200% | Trend analysis | Time series cases |
| Outbreak Threshold | Upper control limit for outbreak detection | Mean + (k × SD) | Disease-specific | Early warning | Historical baseline |
| Attack Rate | Proportion affected in outbreak | (Cases / Population at risk) × 100 | 5%-30% (outbreak-specific) | Outbreak severity | Outbreak cases, denominator |

## Feature Engineering Guidance

### Common Features for Infectious Disease Time Series

#### Temporal Features
- **Week of Year**: Captures seasonality (1-53)
  - **Description**: Week number within calendar year
  - **Calculation**: Extract from epi-week format
  - **Interpretation**: Seasonal patterns repeat across years
  - **Use Cases**: Seasonal forecasting, pattern detection
  - **Example**: Week 20 consistently shows dengue peaks

- **Month**: Broader seasonal grouping (1-12)
  - **Description**: Calendar month
  - **Calculation**: Map epi-week to corresponding month
  - **Interpretation**: Monthly aggregation smooths weekly noise
  - **Use Cases**: Policy reporting, annual comparisons

- **Quarter**: Quarterly patterns (Q1-Q4)
  - **Description**: 3-month groupings
  - **Calculation**: Group weeks into quarters
  - **Interpretation**: Identifies broader seasonal trends
  - **Use Cases**: Resource allocation by quarter

- **Year**: Long-term trends (2012-2020)
  - **Description**: Calendar year
  - **Calculation**: Extract year from epi-week
  - **Interpretation**: Inter-annual variation, multi-year trends
  - **Use Cases**: Long-term forecasting, policy impact assessment

#### Lag Features
- **Previous Week Cases**: Lagged case counts (lag-1, lag-2, etc.)
  - **Description**: Case count from n weeks prior
  - **Calculation**: Shift time series by n periods
  - **Interpretation**: Captures autocorrelation, disease persistence
  - **Use Cases**: Forecasting models (ARIMA, regression)
  - **Example**: Last week's dengue cases predict this week's

- **Rolling Averages**: Smoothed trends (2-week, 4-week, 8-week)
  - **Description**: Moving average over n weeks
  - **Calculation**: Mean of cases over rolling window
  - **Interpretation**: Reduces random fluctuation, reveals underlying trend
  - **Use Cases**: Trend visualization, threshold calculation

- **Exponential Moving Average (EMA)**: Weighted recent trends
  - **Description**: Weighted average favoring recent data
  - **Calculation**: EMA = α × current + (1 - α) × previous EMA
  - **Interpretation**: Responds faster to recent changes than simple moving average
  - **Use Cases**: Outbreak detection, rapid response systems

#### Statistical Features
- **Year-over-Year Change**: Percent change from same week previous year
  - **Description**: Compare cases to same seasonal period last year
  - **Calculation**: (Cases_this_year - Cases_last_year) / Cases_last_year × 100
  - **Interpretation**: Controls for seasonality, shows growth/decline
  - **Use Cases**: Annual reporting, growth trend analysis
  - **Example**: +50% dengue cases vs. Week 20 last year

- **Z-Score**: Standardized deviation from mean
  - **Description**: Standard deviations from historical average
  - **Calculation**: (Cases - Mean) / SD
  - **Interpretation**: Outlier detection; |Z| > 2 suggests anomaly
  - **Use Cases**: Outbreak detection, alert systems

- **Percentile Rank**: Relative position in historical distribution
  - **Description**: Percentage of historical weeks with lower case counts
  - **Calculation**: Rank current week among all historical same-week observations
  - **Interpretation**: 90th percentile = higher than 90% of historical weeks
  - **Use Cases**: Risk categorization, threshold alerts

#### Domain-Specific Calculated Features #++++++++++++++++++++++++THIS IS THE MAIN+++++++++++++++
- **Outbreak Flag**: Binary indicator of outbreak status
  - **Description**: 1 if outbreak threshold exceeded, 0 otherwise
  - **Calculation**: Cases > (Mean + 2×SD) for disease-week
  - **Interpretation**: Triggers enhanced surveillance/response
  - **Use Cases**: Resource allocation, alert systems

- **Peak Week Indicator**: Binary for seasonal peak period
  - **Description**: 1 during typical peak season, 0 otherwise
  - **Calculation**: Historical analysis identifies peak weeks
  - **Interpretation**: Dengue peaks weeks 15-35; HFMD weeks 20-40
  - **Use Cases**: Seasonal planning, staffing

- **Multi-Disease Index**: Composite burden across diseases
  - **Description**: Weighted sum of case counts across diseases
  - **Calculation**: Σ(Weight_i × Cases_i) for diseases i
  - **Interpretation**: Overall infectious disease burden
  - **Use Cases**: Healthcare system capacity planning

### Domain-Specific Patterns

#### Epidemic Curve Shapes
**Description**: Outbreak case progression patterns over time
**When to Apply**: Analyzing historical outbreaks, validating forecasts
**Implementation**: Classify epi-curve shape (point source, propagated, continuous)
**Example**: HFMD outbreaks show propagated pattern with 7-14 day peaks

#### Seasonal Decomposition
**Description**: Separate time series into trend, seasonal, and residual components
**When to Apply**: Understanding drivers of case fluctuations
**Implementation**: Use STL decomposition or moving averages
**Example**: Dengue = upward trend + strong seasonality + weather-driven noise

#### Lead-Lag Relationships
**Description**: Temporal relationship between diseases or environmental factors
**When to Apply**: Multi-disease forecasting, environmental correlates
**Implementation**: Cross-correlation analysis, Granger causality
**Example**: Temperature increase precedes dengue peak by 4-6 weeks

### Temporal Features
- **Week of Year (1-53)**: Captures intra-annual seasonality
- **Month (1-12)**: Monthly aggregation for policy reporting
- **Quarter (Q1-Q4)**: Quarterly patterns for resource planning
- **Holiday Indicators**: School holidays, public holidays (affect transmission)
- **Meteorological Season**: Hot/wet/cool periods (Singapore context)

### Aggregation Strategies
- **Rolling Windows**: 2-week, 4-week, 8-week averages to smooth volatility
- **Year-over-Year Comparison**: Same week/month in previous year for seasonality-adjusted growth
- **Cumulative Counts**: Year-to-date totals for annual burden assessment
- **Peak Detection**: Identify local maxima within seasons for outbreak characterization

## Data Quality Considerations #++++++++++++++check+++++++++++++++++++++ dw - A CERTAIN point conforming to specific type (got 2.d.p instead of 4)

### Reporting Completeness
- **Description**: All eligible cases captured in surveillance system
- **Impact**: Underreporting biases burden estimates and trends
- **Detection**: Compare multiple data sources (hospital admissions, lab reports, physician surveys)
- **Mitigation**: Sensitivity analysis with underreporting correction factors; focus on relative trends rather than absolute counts

### Reporting Timeliness
- **Description**: Lag between case occurrence and reporting in system
- **Impact**: Real-time forecasting uses delayed data; outbreak response delayed
- **Detection**: Analyze date of onset vs. date of reporting
- **Mitigation**: Nowcasting methods to adjust for reporting delays; state lag time in model documentation

### Case Definition Changes
- **Description**: Criteria for confirming cases may evolve (e.g., new lab tests)
- **Impact**: Apparent trend may reflect surveillance artifact, not true change
- **Detection**: Check for sudden changes coinciding with policy/protocol updates
- **Mitigation**: Segment analysis by case definition period; note limitations in trend interpretation

### Denominator Uncertainty
- **Description**: Population at risk may be uncertain (e.g., transient workers, tourists)
- **Impact**: Incidence rate calculations may be biased
- **Detection**: Compare to census data, work permit data
- **Mitigation**: Use case counts rather than rates; document population assumptions

### Disease Name Inconsistencies
- **Description**: Same disease reported under different names over time (e.g., HFMD vs Hand, Foot Mouth Disease)
- **Impact**: Artificial breaks in time series
- **Detection**: Manual review of disease names; check for duplicates
- **Mitigation**: Standardize disease names before analysis; merge equivalent categories

## Analytical Methodologies

### Time Series Forecasting
- **Application**: Predict future case counts 4-12 weeks ahead
- **Assumptions**: Historical patterns persist; seasonality stable; no major interventions
- **Implementation Notes**: Use ARIMA for univariate; Prophet for seasonal; machine learning for multivariate
- **Interpretation**: Forecast = point estimate; confidence interval = uncertainty range; wider intervals for longer horizons

### Outbreak Detection (Statistical Process Control)
- **Application**: Identify aberrations exceeding expected baseline
- **Assumptions**: Cases follow distribution (Poisson, negative binomial); baseline is stable
- **Implementation Notes**: Calculate control limits (mean ± 2 SD); adjust for seasonality
- **Interpretation**: Signal when cases exceed upper control limit; investigate potential outbreak

### Trend Analysis (Mann-Kendall Test)
- **Application**: Detect statistically significant increasing/decreasing trends
- **Assumptions**: Independent observations (or adjust for autocorrelation)
- **Implementation Notes**: Non-parametric test robust to outliers; reports p-value and trend direction
- **Interpretation**: p < 0.05 indicates significant trend; examine magnitude and public health importance

### Cluster Detection (SaTScan)
- **Application**: Identify spatial or temporal clusters of cases
- **Assumptions**: Cases randomly distributed under null hypothesis
- **Implementation Notes**: Not applicable with national aggregates; requires geographic data
- **Interpretation**: Significant clusters suggest localized transmission; target interventions geographically

## Common Pitfalls and Best Practices #++++++++++look into it+++++++++++++ may not be relevant (e.g. metrics abt 80% completeness - proposal document (dh 80%, in strategy completeness -> TRACE WHERE THE VALUES COME FROM))

### Pitfalls to Avoid
- **Confusing Incidence with Prevalence**: Use incidence (new cases) for acute diseases; prevalence for chronic
- **Ignoring Reporting Delays**: Real-time data is incomplete; adjust for lag or use nowcasting
- **Overfitting Noise**: High-frequency fluctuations may be random; smooth with moving averages
- **Assuming Stationarity**: Disease patterns evolve; validate models regularly with recent data
- **Ignoring Outbreak Context**: Unusual events (e.g., Zika 2016) may distort long-term trends; consider excluding or modeling separately

### Best Practices
- **Visualize First**: Plot time series before modeling; identify seasonality, trends, outliers
- **Use Domain Knowledge**: Consult epidemiologists on disease characteristics, expected patterns
- **Communicate Uncertainty**: Always report forecast confidence intervals; acknowledge limitations
- **Validate with Holdout Data**: Test forecasting models on recent data not used in training
- **Update Models Regularly**: Retrain with new data to capture evolving patterns
- **Document Assumptions**: State data limitations, modeling choices, and caveats clearly

## References and Sources

### Authoritative Sources
- **Singapore Ministry of Health**: https://www.moh.gov.sg/ - Official disease surveillance reports and outbreak updates
- **Weekly Infectious Disease Bulletin**: https://www.moh.gov.sg/resources-statistics/infectious-disease-statistics - Primary data source for this analysis
- **CDC Principles of Epidemiology**: https://www.cdc.gov/csels/dsepd/ss1978/ - Foundational epidemiology training resource
- **WHO Disease Outbreak News**: https://www.who.int/emergencies/disease-outbreak-news - Global context for infectious disease threats

### Academic References
- Centers for Disease Control and Prevention. (2012). *Principles of Epidemiology in Public Health Practice* (3rd ed.). U.S. Department of Health and Human Services.
- Rothman, K. J., Greenland, S., & Lash, T. L. (2008). *Modern Epidemiology* (3rd ed.). Lippincott Williams & Wilkins.
- Giesecke, J. (2017). *Modern Infectious Disease Epidemiology* (3rd ed.). CRC Press.

### Industry Standards
- **ISO 8601 Week Date System**: https://www.iso.org/iso-8601-date-and-time-format.html - Standard for epidemiological week numbering

## Cross-References

### Related Domain Knowledge Files
- [Infectious Disease Forecasting Best Practices](time-series-forecasting-best-practices.md) - Methodology for predictive modeling
- [Stakeholder: Public Health Surveillance Team Expertise](stakeholder-public-health-surveillance-team-expertise.md) - Understanding surveillance operations

### Related Data Dictionary Entries
- [Weekly Infectious Disease Bulletin](../data_dictionary/infectious_disease_bulletin.md) - Field definitions and data structure

## Metadata

**Created**: 9 February 2026
**Last Updated**: 9 February 2026
**Updated By**: GitHub Copilot
**Update Reason**: Initial creation for PS-001 and PS-002 user story generation
**Version**: 1.0

## Notes

This glossary focuses on concepts relevant to Singapore's infectious disease surveillance system. Additional terms may be added as analysis requirements evolve. For disease-specific clinical details, consult MOH disease-specific guidelines.
