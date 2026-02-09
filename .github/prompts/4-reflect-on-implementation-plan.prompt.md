# Implementation Plan Validation Prompt

## Context
As a senior data analyst, you are reviewing implementation plans for data analysis user stories. Your goal is to ensure each implementation plan is complete, realistic, and aligned with available data sources and technical capabilities.

## Prerequisites
Before validating implementation plans, review the project's data sources documentation to understand:
1. **Data access methods** (API, database, file download, web scraping, etc.)
2. **Available datasets** (names, schemas, record counts, time spans)
3. **Data characteristics** (granularity, update frequency, completeness, quality)
4. **Technical constraints** (authentication, rate limits, access restrictions)
5. **Known limitations** (missing fields, aggregation levels, data gaps)

## Your Task
Review the implementation plan in each user story and validate it against the following comprehensive checklist. Adapt each validation point based on the actual data sources documented in the project. Provide specific, actionable feedback for any gaps or misalignments.

---

## 1. Data Source Alignment Validation

### 1.1 Data Extraction Methods
**Review the project's data sources documentation, then check:**

- [ ] Does the implementation plan use the correct extraction method for this project?
  - API calls (verify endpoint, authentication method)
  - Database queries (verify connection method, credentials handling)
  - File downloads (verify source, download mechanism)
  - Web scraping (verify legality, rate limits, parsing approach)
  - Cloud storage (verify bucket/container access, credentials)

- [ ] Are authentication/access requirements addressed?
  - API keys, tokens, credentials properly referenced
  - Service account setup mentioned
  - Access permissions validated

- [ ] Are correct identifiers used?
  - Dataset/table names match documentation
  - File paths are accurate
  - Query parameters are correct

- [ ] Is the extraction method consistent with project infrastructure?
  - Uses existing connectors/modules if available
  - Follows project conventions
  - Includes error handling and retry logic

**Common Red Flags:**
- ❌ Extraction method doesn't match documented data source
- ❌ References non-existent datasets, tables, or files
- ❌ Missing extraction tasks entirely
- ❌ Assumes capabilities not supported (e.g., real-time when data is batch)
- ❌ Ignores authentication requirements
- ❌ No error handling for network/access issues

### 1.2 Data Availability Check
**Cross-reference against the project's data sources documentation:**

For each dataset/table/file referenced in the implementation plan, verify:

- [ ] **Existence**: Dataset/table/file actually exists and is accessible
- [ ] **Time span**: Temporal coverage matches user story requirements
  - Check start date, end date, update frequency
  - Identify any gaps in temporal coverage
- [ ] **Schema match**: Required columns/fields are present
  - Verify field names (case sensitivity, naming conventions)
  - Check data types match expected usage
- [ ] **Granularity**: Level of detail matches analysis needs
  - Temporal: hourly/daily/weekly/monthly/annual?
  - Geographic: national/regional/city/facility/individual?
  - Demographic: age groups, individual level?
- [ ] **Sufficient volume**: Record count adequate for statistical validity
  - Minimum samples per group for comparisons
  - Enough historical data for trends

**Common Misalignments to Check:**
- User story needs fine-grained data → Check if only aggregated data available
- Needs real-time/streaming → Check if data is batch/periodic only
- Requires specific breakdowns → Check if aggregation prevents desired slicing
- Wants historical trends → Check if sufficient temporal coverage exists
- Needs geographic analysis → Check if location data granular enough
- Requires demographic details → Check if PII restrictions limit access

### 1.3 Data Quality Assumptions
**Review data sources documentation for quality characteristics, then validate:**

- [ ] **Completeness**: Implementation plan addresses missing data appropriately
  - If data is complete: acknowledgment that no imputation needed
  - If data has gaps: imputation/handling strategy specified
- [ ] **Known anomalies**: Special periods or outliers are handled
  - Data disruptions (e.g., system changes, policy changes, crisis periods)
  - Seasonal effects or cyclical patterns
- [ ] **Update frequency**: Analysis design matches data refresh rate
  - Real-time/streaming data → appropriate real-time processing
  - Batch/periodic data → appropriate batch processing windows
  - Static/historical → acknowledgment of no updates
- [ ] **Documented limitations**: All known constraints are acknowledged
  - Granularity limitations
  - Coverage gaps (temporal, geographic, demographic)
  - Accuracy/precision limitations
  - Bias or sampling issues

---

## 2. Exploratory Data Analysis (EDA) Validation

### 2.1 Data Characterization
**Required EDA Steps:**
- [ ] Shape inspection (rows, columns) for each dataset
- [ ] Data type verification (numeric, categorical, datetime)
- [ ] Descriptive statistics (mean, median, std, min, max) for numeric variables
- [ ] Value range checks (verify against expected/documented ranges)
- [ ] Unique value counts for categorical variables
- [ ] Duplicate detection

### 2.2 Data Appropriateness for Analysis Type

**Time Series Data:**
If user story involves trends, seasonality, forecasting:
- [ ] Dataset has temporal dimension (year, month, date, timestamp)
- [ ] Sufficient time points for analysis (minimum 2-3 years for trends, more for seasonality)
- [ ] Consistent time intervals match analysis needs (hourly/daily/monthly/annual)
- [ ] Missing time periods identified and handled

**Demographic Analysis:**
If user story involves age, gender, race comparisons:
- [ ] Dataset contains demographic breakdowns
- [ ] Categories are clearly defined
- [ ] Sample sizes per group are adequate
- [ ] Statistical significance testing is planned

**Geographic Analysis:**
If user story involves location-based comparisons:
- [ ] Dataset has geographic identifiers (coordinates, regions, facilities, addresses)
- [ ] Geographic granularity matches analysis needs
- [ ] Coverage across locations is balanced (check for gaps)
- [ ] Spatial data quality assessed (accuracy, completeness)

**Cross-sectional Analysis:**
If comparing groups at single time point:
- [ ] Data from consistent time period
- [ ] Comparable metrics across groups

### 2.3 Visualization Appropriateness

**Match visualization to data type:**

| Data Type | Appropriate Visualizations | Inappropriate Visualizations |
|-----------|---------------------------|------------------------------|
| **Time series** (temporal data) | ✓ Line charts, area charts<br>✓ Seasonal decomposition plots<br>✓ Trend + seasonality components | ❌ Pie charts<br>❌ Static bar charts (for many time points) |
| **Categorical distributions** | ✓ Bar charts<br>✓ Grouped bar charts<br>✓ Stacked bar charts | ❌ Line charts<br>❌ Scatter plots |
| **Comparisons (groups)** | ✓ Grouped bar charts<br>✓ Box plots<br>✓ Violin plots | ❌ Single pie chart with many categories |
| **Correlations (numeric)** | ✓ Scatter plots<br>✓ Correlation matrices<br>✓ Heatmaps | ❌ Bar charts |
| **Proportions (parts of whole)** | ✓ Pie charts (≤5 categories)<br>✓ Stacked bar charts<br>✓ Treemaps | ❌ Line charts |
| **Geographic/Spatial** | ✓ Choropleth maps<br>✓ Location scatter maps<br>✓ Bubble maps | ❌ (Check if geographic data available) |
| **Distributions** | ✓ Histograms<br>✓ Density plots<br>✓ Box plots | ❌ Pie charts |

**Check Implementation Plan:**
- [ ] Visualizations match data type and structure
- [ ] Interactive dashboards use appropriate tools (Plotly, Dash, Streamlit, Tableau, Power BI)
- [ ] Time-changing data uses line/area charts, not static comparisons
- [ ] Heatmaps used for 2D patterns (time × category, factor1 × factor2)
- [ ] Geographic visualizations only if location data available with sufficient detail

**General Validation Principles:**
```
✓ GOOD: Line chart for temporal trends (any time series data)
✓ GOOD: Heatmap for 2D patterns (time × category, geographic × metric)
✓ GOOD: Bar chart for categorical comparisons (few categories)
❌ BAD: Pie chart for temporal data (time series → line chart)
❌ BAD: Bar chart for 15+ time points (use line chart)
❌ BAD: Geographic map without location coordinates/boundaries
```

---

## 3. Data Processing & Transformation Validation

### 3.1 Data Cleaning Tasks
**Check that standard cleaning steps are included (adapt based on data characteristics):**
- [ ] Date/time parsing and standardization (handling format variations)
- [ ] Column name standardization (consistent naming across datasets)
- [ ] Data type conversions (string → numeric, datetime, categorical)
- [ ] Missing value handling (imputation, removal, flagging)
- [ ] Duplicate detection and removal
- [ ] Outlier detection strategy (if relevant to analysis)
- [ ] Text cleaning (if working with free-text fields)
- [ ] Unit standardization (currency, measurements, percentages)

### 3.2 Feature Engineering
**Check if appropriate features are created based on analysis needs:**
- [ ] Temporal features: year, month, quarter, day_of_week, hour (if temporal data)
- [ ] Derived metrics: rates, ratios, growth rates, per-capita/normalized values
- [ ] Aggregations: totals, averages, medians by relevant groupings
- [ ] Categorical encodings: one-hot, label encoding (for modeling)
- [ ] Interaction features: combinations of variables (if needed for analysis)
- [ ] Flags/indicators: special periods, outliers, thresholds, categories

### 3.3 Data Integration
**For multi-table/multi-source analyses:**
- [ ] Join keys identified and validated (common columns across datasets)
- [ ] Join type specified and appropriate (inner, left, right, outer, cross)
- [ ] Handling of mismatched granularity (e.g., daily vs monthly, facility vs regional)
- [ ] Schema alignment (consistent column names, data types, units)
- [ ] Handling of missing matches (strategy for unmatched records)
- [ ] Data lineage tracking (source of each field after integration)

---

## 4. Analysis Method Validation

### 4.1 Statistical Methods Appropriateness
**Match method to data and question:**

| Analysis Goal | Appropriate Methods | Check Implementation |
|--------------|---------------------|---------------------|
| **Trend detection** | Linear regression, moving averages, time series decomposition | [ ] Method specified<br>[ ] Libraries included |
| **Group comparisons** | t-tests, ANOVA, chi-square tests | [ ] Statistical tests named<br>[ ] Significance level defined (α=0.05) |
| **Anomaly detection** | Z-scores, IQR method, control charts, isolation forest | [ ] Threshold defined<br>[ ] Validation approach |
| **Clustering** | K-means, hierarchical, DBSCAN | [ ] Distance metric<br>[ ] Optimal clusters method |
| **Forecasting** | ARIMA, exponential smoothing, Prophet, LSTM | [ ] Train/test split<br>[ ] Evaluation metrics |
| **Classification** | Logistic regression, decision trees, random forest, SVM | [ ] Class balance checked<br>[ ] Metrics appropriate for problem |
| **Regression** | Linear, polynomial, ridge, lasso, random forest | [ ] Assumptions validated<br>[ ] Residual analysis |

### 4.2 Model Validation
**If predictive modeling involved:**
- [ ] Train/test split strategy (e.g., temporal split for time series)
- [ ] Cross-validation approach (if appropriate)
- [ ] Performance metrics defined (RMSE, MAE, accuracy, precision/recall)
- [ ] Baseline model for comparison
- [ ] Overfitting prevention (regularization, validation set)

### 4.3 Causal Inference Considerations
**If claiming causation:**
- [ ] Appropriate causal inference methods used (not just correlation)
- [ ] Confounding variables considered
- [ ] Limitations explicitly stated
- [ ] Language is careful ("associated with" vs "causes")

---

## 5. Implementation Completeness Check

### 5.1 End-to-End Pipeline Coverage
**Verify ALL stages are addressed:**

1. **Data Extraction** ✓
   - [ ] Connection to data source (using documented method)
   - [ ] Authentication/access handling
   - [ ] Download/caching strategy (if applicable)
   - [ ] Data loading into workspace

2. **Data Validation** ✓
   - [ ] Schema validation (structure, fields, types)
   - [ ] Quality checks (completeness, accuracy, consistency)
   - [ ] Error handling and logging

3. **Data Preprocessing** ✓
   - [ ] Cleaning steps (missing values, duplicates, outliers)
   - [ ] Transformation steps (types, formats, normalization)
   - [ ] Feature engineering (derived fields, aggregations)

4. **Exploratory Data Analysis** ✓
   - [ ] Summary statistics
   - [ ] Distribution analysis
   - [ ] Relationship/correlation analysis
   - [ ] Pattern identification

5. **Statistical Analysis** ✓
   - [ ] Hypothesis tests
   - [ ] Modeling (if applicable)
   - [ ] Validation

6. **Visualization** ✓
   - [ ] Exploratory plots
   - [ ] Final presentation visualizations
   - [ ] Interactive dashboards (if specified)

7. **Interpretation & Reporting** ✓
   - [ ] Results documentation
   - [ ] Limitations and assumptions documented
   - [ ] Recommendations provided
   - [ ] Business/research insights articulated

8. **Code Documentation** ✓
   - [ ] Docstrings for functions and classes
   - [ ] README/documentation files
   - [ ] Reproducibility instructions
   - [ ] Environment/dependency specifications

### 5.2 Dependency Management
**Check all dependencies are realistic:**

**External Packages:**
- [ ] All packages are accessible (open-source, licensed, or available in environment)
- [ ] Package versions specified (if critical for reproducibility)
- [ ] Installation instructions provided (pip, conda, npm, etc.)
- [ ] No unavailable proprietary tools or expired subscriptions
- [ ] Language-appropriate libraries (Python, R, SQL, etc.)

**Common packages by category (verify availability for project):**
```
Data Manipulation: pandas, numpy, dplyr, data.table
Statistical Analysis: scipy, statsmodels, scikit-learn, stats, forecast
Visualization: matplotlib, seaborn, plotly, ggplot2, altair
ML/AI: tensorflow, pytorch, keras, xgboost, lightgbm
Database: sqlalchemy, psycopg2, pymongo, pyodbc
API: requests, httpx, aiohttp
Cloud: boto3 (AWS), google-cloud, azure-sdk
```

**Internal Dependencies:**
- [ ] References to internal modules that actually exist in the project
- [ ] Uses project connectors/utilities if available
- [ ] Follows project conventions and patterns
- [ ] No references to non-existent internal modules

### 5.3 Configuration & Environment
**Infrastructure considerations (based on project setup):**
- [ ] Platform/environment specified correctly (cloud, on-prem, local, notebook environment)
- [ ] Compute requirements considered (memory, CPU, GPU if needed)
- [ ] Storage requirements addressed (disk space, database capacity)
- [ ] Output storage plan (where results saved, retention policy)
- [ ] Logging framework referenced or specified
- [ ] Configuration management (env vars, config files, secrets handling)
- [ ] Scalability considerations (if dealing with large data volumes)

---

## 6. Scenario Coverage Validation

### 6.1 Acceptance Criteria Mapping
**For each acceptance criterion:**
- [ ] At least one implementation task addresses it
- [ ] Task is specific and measurable
- [ ] Success can be objectively verified
- [ ] No acceptance criteria are orphaned (without tasks)

### 6.2 Edge Cases & Data Limitations
**Check if implementation handles project-specific limitations:**
- [ ] Known data anomalies or disruption periods
- [ ] Missing variables or incomplete coverage
- [ ] Limited granularity (temporal, geographic, categorical)
- [ ] Sparse data (limited historical records, small sample sizes)
- [ ] Data aggregation constraints
- [ ] Privacy/anonymization impacts on analysis
- [ ] Data quality issues documented in data sources

### 6.3 Known Data Constraints
**Validate awareness of documented constraints (examples - adapt to your project):**

| Constraint Type | Potential Implications | Check Implementation |
|----------------|----------------------|---------------------|
| Temporal granularity | Limited to available intervals (hourly/daily/monthly/annual) | [ ] Acknowledged in limitations |
| Geographic aggregation | Analysis constrained to available geographic levels | [ ] Uses appropriate data |
| Data freshness | Latest data date limits recency of insights | [ ] Noted in assumptions |
| Update frequency | Real-time vs batch determines monitoring capabilities | [ ] Design matches data refresh |
| Completeness | Missing data affects analysis methods | [ ] Handling strategy specified |
| Sample size | Small samples limit statistical power | [ ] Power analysis or caveats included |
| Bias/Representativeness | Sampling or collection bias affects generalizability | [ ] Limitations documented |

---

## 7. Output Quality Validation

### 7.1 Deliverables Checklist
**Ensure implementation produces:**
- [ ] **Analysis artifacts**: Cleaned datasets, intermediate results
- [ ] **Visualizations**: Publication-quality charts, interactive dashboards
- [ ] **Statistical outputs**: Test results, model performance metrics
- [ ] **Documentation**: Analysis report, methodology description
- [ ] **Code**: Reproducible scripts/notebooks with documentation
- [ ] **Recommendations**: Actionable insights for stakeholders

### 7.2 Stakeholder Alignment
**Check outputs match user needs:**
- [ ] Technical detail appropriate for audience (epidemiologist vs executive)
- [ ] Visualizations are interpretable by non-technical users
- [ ] Recommendations are actionable (not just observations)
- [ ] Limitations and caveats are clearly stated

---

## 8. Risk & Feasibility Assessment

### 8.1 Technical Feasibility
**Red flags for infeasibility (check against project constraints):**
- ❌ Requires data not available in documented sources
- ❌ Needs infrastructure not available (real-time when data is batch, etc.)
- ❌ Advanced ML without sufficient data volume or quality
- ❌ Causal inference without appropriate experimental/quasi-experimental design
- ❌ Analysis requiring granularity not available in data
- ❌ Privacy-violating analysis with anonymized/aggregated data
- ❌ Geographic/spatial analysis without location data

### 8.2 Complexity vs Timeline
**Assess if tasks are realistic (adjust based on complexity and team size):**
- [ ] Data extraction: 0.5-2 days (depending on complexity)
- [ ] EDA: 1-3 days (depending on dataset size/complexity)
- [ ] Analysis: 2-7 days (simple stats vs complex modeling)
- [ ] Visualization: 1-3 days (static charts vs interactive dashboards)
- [ ] Documentation: 1-2 days
- **Typical total**: 1-3 weeks per user story (varies significantly)

### 8.3 Dependency Risks
**Potential blockers:**
- [ ] External data sources availability confirmed (APIs, third-party data)
- [ ] Cross-user-story dependencies identified and sequenced
- [ ] Shared code/data dependencies managed
- [ ] Compute/infrastructure resources available when needed
- [ ] Team member availability and expertise aligned with tasks

---

## Output Format

For each user story implementation plan, provide:

### ✅ Strengths
List what is well-aligned and complete.

### ⚠️ Gaps & Misalignments
List specific issues with:
1. **Issue description**
2. **Impact** (low/medium/high)
3. **Recommendation**

### 🔧 Required Fixes
Specific, actionable changes needed:
```markdown
- [ ] Add data extraction task using documented method
- [ ] Change pie chart to line chart for time series
- [ ] Specify statistical test for group comparison
- [ ] Add handling for known data anomalies
- [ ] Include validation step for data quality
```

### 💡 Enhancements (Optional)
Suggestions to improve beyond minimum requirements.

### ✔️ Final Verdict
- **Ready to implement** (minor or no issues)
- **Needs revision** (moderate issues to address)
- **Major rework required** (significant alignment problems)

---

## Validation Checklist Summary

Run through this quick checklist for each implementation plan:

```
DATA SOURCE ALIGNMENT
[ ] Extraction method matches documented data source
[ ] All referenced datasets/tables/files exist
[ ] Time span requirements match available data
[ ] Data granularity acknowledged and appropriate

EDA APPROPRIATENESS
[ ] Visualizations match data type (time → line charts)
[ ] Statistical methods suit data structure
[ ] EDA steps are comprehensive (shape, stats, distributions)

IMPLEMENTATION COMPLETENESS
[ ] All 8 pipeline stages have tasks (extraction → reporting)
[ ] Every acceptance criterion has implementing tasks
[ ] Dependencies (packages, internal modules) are realistic
[ ] Edge cases and limitations handled

TECHNICAL FEASIBILITY
[ ] No unavailable data sources required
[ ] Infrastructure assumptions match reality
[ ] Methods match available data size and quality
[ ] Outputs are well-defined and measurable

DOCUMENTATION & QUALITY
[ ] Limitations explicitly documented
[ ] Code reproducibility considered
[ ] Stakeholder outputs specified
```

---

## Examples of Good vs Bad Implementation Elements

### ❌ BAD: Data Extraction
```
- □ Extract data from undocumented database
- □ Connect to API without authentication plan
- □ Download files from unspecified source
```
**Issues:** Doesn't match documented data source; no authentication; vague source.

### ✓ GOOD: Data Extraction
```
- □ Extract data using [documented method, e.g., API endpoint, Kaggle, S3 bucket]
- □ Configure authentication per documentation (API key, OAuth, credentials)
- □ Load data into [workspace format] (DataFrame, database table, parquet files)
- □ Validate schema matches expected structure (fields, types, constraints)
```

---

### ❌ BAD: Visualization
```
- □ Create pie chart showing temporal trends over multiple years
- □ Make bar chart with 15+ time points
- □ Use geographic map without location data
```
**Issues:** Pie charts wrong for time series; bar charts poor for many time points; maps without coordinates.

### ✓ GOOD: Visualization
```
- □ Create line chart showing trends over time (for time series data)
- □ Generate heatmap for 2D patterns (time × category, location × metric)
- □ Build interactive dashboard for exploring patterns (Plotly, Dash, etc.)
- □ Use appropriate chart types matched to data structure
```

---

### ❌ BAD: Analysis Method
```
- □ Apply real-time algorithms to batch data
- □ Analyze hourly patterns with annual data
- □ Build deep learning model with 50 data points
```
**Issues:** Method doesn't match data characteristics; insufficient data for approach.

### ✓ GOOD: Analysis Method
```
- □ Apply appropriate statistical method for data structure
- □ Match temporal analysis to data granularity (annual → long-term trends)
- □ Use methods suitable for sample size (simple stats for small n)
- □ Include validation against known patterns or holdout data
```

---

### ❌ BAD: Dependency
```
- Internal: `src.nonexistent.module`
- External: `proprietary_lib`, `unavailable_api`
```
**Issues:** These modules don't exist in project or aren't accessible.

### ✓ GOOD: Dependency
```
- External: Standard open-source libraries (pandas, scikit-learn, plotly, etc.)
- Internal: Documented project modules that exist (src.data_processing.connector, src.utils.logger)
```

---

## Final Instruction

Review each user story implementation plan systematically using this prompt. Be thorough but constructive—focus on ensuring the analysis is feasible, rigorous, and aligned with available resources. Prioritize **data availability**, **method appropriateness**, and **end-to-end completeness**.
