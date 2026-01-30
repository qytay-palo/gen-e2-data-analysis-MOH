# Data Cleaning Process Generation Prompt

## Context
You are an expert data analyst tasked with generating comprehensive, production-ready data cleaning code for a data analysis project. Your code should be modular, well-documented, and follow industry best practices for data quality assurance.

## Objective
Generate a complete data cleaning workflow that systematically identifies, documents, and resolves data quality issues. The output should be organized in a Jupyter notebook format that serves as both executable code and documentation.

**Important**: The phases and actions outlined below serve as a **comprehensive framework, not a rigid checklist**. You are encouraged to:
- Explore additional data quality dimensions relevant to the specific dataset
- Apply domain-specific validation rules and checks
- Implement creative solutions to unique data challenges
- Add analysis steps that emerge from your findings
- Adapt, extend, or skip steps based on actual data characteristics

---

## Inputs

Before generating code, **review the project context documentation** (if available in `docs/project_context/`) to inform your approach:
- **`tech_stack.md`**: Select appropriate libraries, platforms, and frameworks; ensure compatibility with the computational environment
- **`data_sources.md`**: Apply schema-specific validation rules, business logic constraints, and domain-specific quality checks
- **`data_connections.md`**: Use correct connection methods, authentication patterns, and data access approaches

---

## Instructions

### Phase 1: Environment Setup

**Task**: Create the initial setup section with all required dependencies.

**Guidance** (adapt as needed):
1. **Library Installation**
   - **Reference `tech_stack.md`** to identify the appropriate libraries for the project's environment
   - For Python projects, typically include: pandas, numpy, matplotlib, seaborn, missingno, etc.
   - For R projects, typically include: tidyverse, dplyr, ggplot2, naniar, etc.
   - For Spark-based projects, include: pyspark/sparklyr and relevant data quality libraries
   - Provide installation commands appropriate to the environment (pip, conda, CRAN, etc.)
   - Include version specifications for reproducibility where critical

2. **Import Statements**
   - Import all necessary libraries with standard aliases
   - Group imports logically (standard library, data manipulation, visualization, utilities)
   - Include error handling for missing dependencies

3. **Configuration Setup**
   - Set display options for better data inspection (e.g., max rows, columns, precision)
   - Configure warning filters if appropriate
   - Set random seeds for reproducibility
   - Define project-specific paths and constants

**Output Format**:
```markdown
# Data Cleaning Pipeline

## 1. Environment Setup

### 1.1 Install Required Libraries
[Installation code with comments]

### 1.2 Import Libraries
[Import statements with error handling]

### 1.3 Configuration
[Display settings and constants]
```

---

### Phase 2: Data Loading and Initial Inspection

**Task**: Load the dataset(s) and perform initial exploratory checks.

**Suggested Actions** (add additional checks as discovered):
1. **Data Loading**
   - **Reference `data_connections.md`** for connection methods and authentication
   - Load data from the appropriate source (CSV, database, parquet, HDFS, cloud storage, etc.)
   - Handle file path configurations flexibly
   - Include error handling for file not found or connection issues
   - Display confirmation of successful load with basic info (rows, columns)

2. **Initial Data Profiling**
   - Display dataset shape (rows × columns)
   - Show column names and data types
   - Display first and last few rows for sanity check
   - Generate memory usage statistics
   - Check for duplicate rows at the record level

3. **Data Dictionary Review**
   - **Reference `data_sources.md`** for expected schema and column definitions
   - Cross-reference expected vs. actual columns
   - Flag any missing or unexpected columns
   - Document the purpose of each column for clarity based on business context

**Output Format**:
```markdown
## 2. Data Loading and Initial Inspection

### 2.1 Load Dataset
[Loading code with error handling]

### 2.2 Dataset Overview
[Shape, columns, data types]

### 2.3 Sample Records
[Head and tail display]

### 2.4 Duplicate Check
[Duplicate detection code]
```

---

### Phase 3: Comprehensive Data Quality Assessment

**Task**: Systematically assess data quality across multiple dimensions.

**Core Assessments** (explore additional quality dimensions as relevant):
1. **Missing Value Analysis**
   - Count and percentage of missing values per column
   - Visualize missing data patterns (heatmap, bar chart, matrix)
   - Identify columns with high missingness (>30%, >50%, >70%)
   - Check for patterns in missing data (MCAR, MAR, MNAR)
   - Document findings with comments on potential causes

2. **Data Type Validation**
   - Verify each column has the correct data type
   - Identify columns that need type conversion (e.g., strings to dates, object to numeric)
   - Check for mixed types within columns
   - Validate date/time formats and ranges
   - Flag columns with inconsistent formatting

3. **Value Range and Distribution Analysis** (adapt statistical methods to data characteristics)
   - **Reference `data_sources.md`** for expected value ranges and business rules
   - For numeric columns:
     * Generate descriptive statistics (min, max, mean, median, std, quartiles)
     * Identify outliers using appropriate methods (IQR, Z-score, domain knowledge)
     * Check for impossible values (negative ages, future dates, values outside valid ranges)
     * Validate against expected ranges documented in data sources
     * Visualize distributions (histograms, box plots)
   
   - For categorical columns:
     * Display unique value counts and frequencies
     * Check for unexpected categories or inconsistent labeling
     * Identify low-frequency categories that may need grouping
     * Check for whitespace issues, case inconsistencies

4. **Data Consistency Checks**
   - **Reference `data_sources.md`** for business rules and relationships
   - Cross-field validation (e.g., end_date > start_date)
   - Referential integrity if multiple tables
   - Check for logical inconsistencies against documented business logic
   - Validate ID formats and uniqueness as per schema specifications

5. **Text Data Quality** (if applicable)
   - Check for special characters, encoding issues
   - Identify leading/trailing whitespace
   - Check string length consistency
   - Validate format patterns (emails, phone numbers, IDs)

6. **Additional Quality Dimensions** (explore based on data discovery)
   - Temporal patterns and anomalies
   - Geographical data validation
   - Business rule violations
   - Data freshness and staleness
   - Cardinality issues (too many/few unique values)
   - Any domain-specific quality metrics

**Output Format**:
```markdown
## 3. Data Quality Assessment

### 3.1 Missing Value Analysis
[Counts, percentages, and visualizations]

### 3.2 Data Type Validation
[Current types and required conversions]

### 3.3 Numeric Column Analysis
[Statistics, outliers, distributions]

### 3.4 Categorical Column Analysis
[Unique values, frequencies, inconsistencies]

### 3.5 Data Consistency Checks
[Cross-field validations]

### 3.6 Quality Issues Summary
[Consolidated list of all identified issues]
```

---

### Phase 4: Data Cleaning Implementation

**Task**: Implement systematic solutions to address identified data quality issues.

**Implementation Guidelines** (apply appropriate strategies; extend as needed):
1. **Create a Copy of Original Data**
   - Preserve the original dataset before any modifications
   - Work on a cleaned copy to enable comparison

2. **Handle Missing Values**
   For each column with missing data, implement appropriate strategy:
   - **Deletion**: Remove rows/columns if missingness is minimal (<5%) or data is not critical
   - **Imputation**: 
     * Numeric: mean, median, mode, forward/backward fill, interpolation, or predictive imputation
     * Categorical: mode, new category ('Unknown'), or predictive imputation
     * Time series: forward fill, backward fill, or interpolation
   - **Flag Creation**: Create indicator variables for missingness if it carries information
   - Document the rationale for each approach

3. **Data Type Conversions**
   - Convert columns to appropriate types with error handling
   - Parse dates with correct formats, handle timezone if needed
   - Convert string numbers to numeric types
   - Encode categorical variables appropriately (label encoding, one-hot encoding)
   - Validate conversions were successful

4. **Outlier Treatment**
   - For each identified outlier issue:
     * Decide: remove, cap (winsorize), transform, or keep
     * Document the business logic for the decision
     * Implement the solution with clear comments
   - Consider domain-specific knowledge (some outliers are valid)

5. **Standardization and Normalization**
   - Standardize text fields (trim whitespace, case normalization)
   - Standardize categorical values (consistent naming, fix typos)
   - Normalize formats (dates, phone numbers, addresses)
   - Create consistent ID formats

6. **Feature Engineering for Data Quality**
   - Create derived columns that improve data quality
   - Calculate durations from date pairs
   - Extract components from complex fields
   - Create flags for data quality issues

7. **Remove or Handle Duplicates**
   - Identify true duplicates vs. near-duplicates
   - Decide on deduplication strategy (keep first, last, aggregate)
   - Implement and document the approach

8. **Additional Transformations** (apply as discovered)
   - Custom business logic implementations
   - Domain-specific calculations
   - Data enrichment from external sources
   - Advanced imputation techniques (ML-based, KNN, etc.)
   - Custom validation rules
   - Any other transformations needed for data quality

**Output Format**:
```markdown
## 4. Data Cleaning Implementation

### 4.1 Create Working Copy
[Backup original data]

### 4.2 Missing Value Treatment
[For each column: strategy and implementation]

### 4.3 Data Type Corrections
[Type conversions with validation]

### 4.4 Outlier Handling
[Treatment approach for each case]

### 4.5 Standardization
[Text and format standardization]

### 4.6 Feature Engineering
[Derived columns for data quality]

### 4.7 Deduplication
[Duplicate handling implementation]
```

---

### Phase 5: Post-Cleaning Validation

**Task**: Verify that cleaning operations were successful and data quality has improved.

**Validation Steps** (comprehensive checks; add custom validations):
1. **Re-run Data Quality Checks**
   - Regenerate missing value report
   - Verify data types are correct
   - Check value ranges are now valid
   - Confirm duplicates are resolved

2. **Before/After Comparison**
   - Create side-by-side comparison of key metrics
   - Show reduction in missing values
   - Document changes in data distribution
   - Quantify improvements (e.g., "reduced missing values from 15% to 2%")

3. **Data Integrity Checks**
   - Verify row count changes are expected
   - Confirm no unintended data loss
   - Validate key business logic still holds
   - Check for any new issues introduced

4. **Generate Cleaning Report**
   - Summary statistics table (before/after)
   - List all transformations applied
   - Flag any remaining issues that need domain expert review
   - Document assumptions made during cleaning

**Output Format**:
```markdown
## 5. Post-Cleaning Validation

### 5.1 Data Quality Re-Assessment
[Re-run checks from Phase 3]

### 5.2 Before/After Comparison
[Comparative metrics and visualizations]

### 5.3 Data Integrity Verification
[Validation checks]

### 5.4 Cleaning Report Summary
[Comprehensive summary table]
```

---

### Phase 6: Export Cleaned Data

**Task**: Save the cleaned dataset for downstream analysis.

**Export Actions** (adjust to project needs):
1. **Export to Appropriate Format**
   - Save to the format specified by the project (CSV, parquet, database, etc.)
   - Include timestamp in filename for version control
   - Preserve data types in the export format

2. **Generate Metadata**
   - Save a data cleaning log with all transformations
   - Export a data dictionary with updated information
   - Save the cleaning report as a separate document

3. **Create Data Lineage Documentation**
   - Document the path from raw to cleaned data
   - List all scripts and notebooks used
   - Include information for reproducibility

**Output Format**:
```markdown
## 6. Export Cleaned Data

### 6.1 Save Cleaned Dataset
[Export code with versioning]

### 6.2 Generate Metadata
[Cleaning log and data dictionary]

### 6.3 Documentation
[Lineage and reproducibility information]
```

---

## Code Quality Standards

**Note**: These are recommended practices. Apply judgment based on the specific context and feel free to incorporate additional quality standards relevant to your environment.

### Error Handling
- Wrap critical operations in try-except blocks
- Provide informative error messages
- Log errors appropriately
- Fail gracefully with clear user guidance

### Code Structure
- Use functions for repeatable operations
- Keep code DRY (Don't Repeat Yourself)
- Use meaningful variable names
- Add docstrings to functions
- Include inline comments for complex logic

### Documentation
- Add markdown cells explaining the purpose of each section
- Comment on key decisions and assumptions
- Document any manual interventions required
- Include references to data quality standards used

### Performance Considerations
- Use vectorized operations where possible
- Be mindful of memory usage with large datasets
- Include progress indicators for long-running operations
- Consider chunking for very large datasets

### Best Practices
- Never modify original data in place (use copies)
- Log all transformations for reproducibility
- Use assertions to validate assumptions
- Create checkpoints for long workflows
- Version control the cleaning code

---

## Output Format Requirements

**Notebook Structure**:
1. One markdown cell at the top with title and overview
2. Each phase in a separate section with markdown header
3. Alternate between markdown (explanation) and code cells
4. Include visualization outputs inline
5. End with a summary markdown cell

**Code Cell Standards**:
- Maximum 30-40 lines per cell for readability
- Each cell should have a single clear purpose
- Include a comment header describing what the cell does
- Display relevant outputs for validation

**Markdown Cell Standards**:
- Use headers (##, ###) for section organization
- Explain the "why" not just the "what"
- Include bullet points for key findings
- Use tables for structured information
- Add warnings or notes where appropriate

---

## Adaptability Guidelines

The generated code should be adaptable to different:
- **Data sources**: CSV, databases, APIs, cloud storage
- **Data scales**: Small (MB), medium (GB), large (TB+)
- **Tech stacks**: Pure Python/R, Spark, Dask, SQL-based
- **Domains**: Healthcare, finance, retail, etc.

**Adapt by**:
1. Detecting the project's tech stack from context
2. Using appropriate libraries for the scale of data
3. Adjusting validation rules based on domain knowledge
4. Scaling solutions (pandas vs. Spark vs. SQL) based on data size

---

## Example Template Structure

Generate output following this template:

```
# Data Cleaning Pipeline for [Dataset Name]

**Purpose**: [Brief description]
**Date**: [Current date]
**Author**: [Generated by AI]

---

## 1. Environment Setup
[Code and markdown cells]

## 2. Data Loading and Initial Inspection
[Code and markdown cells]

## 3. Data Quality Assessment
[Code and markdown cells]

## 4. Data Cleaning Implementation
[Code and markdown cells]

## 5. Post-Cleaning Validation
[Code and markdown cells]

## 6. Export Cleaned Data
[Code and markdown cells]

---

## Summary

**Data Quality Improvements**:
- [Metric 1]: [Before] → [After]
- [Metric 2]: [Before] → [After]
- [Metric 3]: [Before] → [After]

**Remaining Considerations**:
- [Item 1]
- [Item 2]

**Next Steps**:
- [Recommendation 1]
- [Recommendation 2]
```

---

## Critical Reminders

1. ✅ **Always preserve original data** - never modify source files
2. ✅ **Document all assumptions** - make decisions transparent
3. ✅ **Validate after each major transformation** - catch issues early
4. ✅ **Provide clear rationale** - explain why you chose each cleaning approach
5. ✅ **Make code reusable** - use functions and parameterization
6. ✅ **Test edge cases** - handle nulls, empty datasets, single rows
7. ✅ **Generate visualizations** - show, don't just tell
8. ✅ **Create audit trail** - log what changed and why
9. ✅ **Think beyond the template** - explore data characteristics and apply appropriate techniques
10. ✅ **Adapt to discoveries** - be flexible and responsive to what the data reveals

---

## Success Criteria

The generated data cleaning code is successful when:
- ✅ All data quality issues are identified and documented
- ✅ Cleaning transformations are implemented with clear rationale
- ✅ Code runs without errors and includes proper error handling
- ✅ Output is reproducible and well-documented
- ✅ Before/after comparisons demonstrate improvement
- ✅ Cleaned data is ready for analysis with minimal further preprocessing
- ✅ Code follows best practices and is maintainable
- ✅ Non-technical stakeholders can understand the cleaning report

---

## End of Prompt

Use this prompt to generate a complete, production-ready data cleaning workflow in notebook format.
