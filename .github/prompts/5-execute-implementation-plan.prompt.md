---
description: Prompt for Execution of the Implementation Plan
stage: Development
---
# AI Agent Prompt: Execute Implementation Plan

## Role

Execute a detailed implementation plan accurately and verify its completion according to specifications for a end-to-end data analysis project.

## Input Requirements

The input will consist of:
- A detailed implementation plan (typically in Markdown format)
- User story and acceptance criteria
- Design specifications and requirements

## Output Requirements

The output MUST include:
- Implementation of all required files and changes
- Verification that specifications have been met
- Completed Design Implementation Verification Checklist

## Review Requirements

Before implementation, the implementation plan MUST be reviewed for:
- Clarity and completeness of all steps
- Availability of all necessary information
- Alignment with project guidelines and technical stack
- Completeness of design specifications (colors, spacing, typography)

If any part of the plan is unclear or missing information, clarification MUST be requested before proceeding.

## Implementation Requirements

The implementation MUST:
- Follow the staged implementation approach outlined below
- Adhere to file paths, code structures, and configurations specified in the plan
- Follow project coding standards and best practices
- Create exact visual implementations matching design specifications
- For any service or API integration step, you MUST implement the actual data fetching, error handling, and retries as described in the plan. Stubs or placeholders are NOT considered complete. If a function is only a stub, the implementation is NOT complete.
- **Leverage MCP (Model Context Protocol) tools for all file and data operations as specified below**
- **Implement ALL code blocks provided in the implementation plan verbatim (see Code Implementation Fidelity below)**

### Code Implementation Fidelity

**CRITICAL**: When an implementation plan includes code blocks with complete function implementations, these MUST be used exactly as specified:

✅ **REQUIRED - Implement Verbatim:**
- ALL code blocks provided in the implementation plan
- All type hints, docstrings, and parameter definitions
- All error handling, retry logic, and validation checks
- All logging statements and audit trail tracking
- All unit tests specified with full test coverage
- All helper functions, utility modules, and configuration files
- All security best practices (credential handling, input validation)

❌ **FORBIDDEN - Do NOT:**
- Simplify or omit "helper" functions or "boilerplate" code
- Skip validation, error handling, or logging statements
- Reduce comprehensive error handling to basic try/except blocks
- Replace detailed implementations with stubs or placeholders
- Assume "obvious" code can be skipped or simplified
- Modify function signatures, parameters, or return types without justification
- Create partial implementations with TODO comments

**Rationale**: Implementation plan code blocks are:
- Production-ready and tested against edge cases
- Include proper error handling for real-world scenarios
- Follow security best practices
- Implement comprehensive logging for debugging and audit trails
- Support reproducibility and long-term maintainability

**Verification After Implementation**:
1. Every function specified in the plan exists and is fully implemented
2. All type hints and docstrings match the specification exactly
3. All unit tests run successfully with expected coverage
4. No functions are stubs (contain only `pass` or `NotImplementedError`)
5. All error handling, retry logic, and validation checks are present
6. All logging and metadata tracking code is functional

## MCP Tools Integration

This implementation MUST leverage available MCP (Model Context Protocol) tools for efficient execution:

### Available MCP Servers

#### 1. Filesystem Server (REQUIRED for all implementations)
Use for all file operations throughout the project structure:

**Data Operations**:
- Reading source data from `data/1_raw/`, `data/2_external/`
- Writing processed data to `data/3_interim/`, `data/4_processed/`
- Managing schemas in `data/schemas/`

**Code & Notebooks**:
- Creating/editing notebooks in `notebooks/1_exploratory/`, `notebooks/2_analysis/`, `notebooks/3_feature_engineering/`
- Managing source code in `src/` subdirectories

**Outputs & Results**:
- Creating result directories in `results/tables/`, `results/metrics/`, `results/exports/`
- Saving reports to `reports/figures/`, `reports/dashboards/`, `reports/presentations/`
- Storing models in `models/`

**Logs & Documentation**:
- Writing logs to `logs/etl/`, `logs/errors/`, `logs/audit/`
- Creating/updating documentation in `docs/`

**MCP Commands Examples**:
```
"Use filesystem tools to read data/1_raw/hospital_visits.csv"
"Use filesystem tools to create directory results/epic-001/wave-1/"
"Use filesystem tools to write the processed data to data/4_processed/clean_visits.csv"
"Use filesystem tools to list all files in notebooks/1_exploratory/"
```

#### 2. SQLite Server (when applicable)
Use for database operations:
- Querying existing databases in `data/` directory
- Creating summary tables and views
- Data validation and quality checks via SQL
- Aggregating data for analysis

**MCP Commands Examples**:
```
"Query the patient_records database using SQLite tools to get admission trends"
"Use SQLite tools to create a summary table of visits by department"
"Execute data quality checks using SQLite tools on the staging database"
```

#### 3. GitHub Server (optional, when enabled)
Use for version control and collaboration:
- Searching codebase for existing implementations
- Creating issues for tracking
- Managing pull requests

### MCP Tool Usage Requirements

When implementing any feature or analysis:

1. **File Reading**: MUST use filesystem MCP tools instead of manual file operations
   - ✅ Correct: "Use filesystem tools to read data/1_raw/input.csv"
   - ❌ Incorrect: Asking user to paste file contents

2. **Directory Management**: MUST use filesystem MCP tools for organization
   - ✅ Correct: "Use filesystem tools to create directory structure for Epic 001"
   - ❌ Incorrect: Manual directory creation commands

3. **Data Writing**: MUST use filesystem MCP tools for all outputs
   - ✅ Correct: "Use filesystem tools to save analysis results to results/tables/"
   - ❌ Incorrect: Generating code without actually saving files

4. **Database Queries**: MUST use SQLite MCP tools when databases are involved
   - ✅ Correct: "Query using SQLite tools and save results with filesystem tools"
   - ❌ Incorrect: Writing SQL without executing it

5. **Verification**: MUST use MCP tools to verify implementation
   - ✅ Correct: "Use filesystem tools to list and verify all created files"
   - ❌ Incorrect: Assuming files were created without verification

### MCP-Enhanced Implementation Workflow

For each implementation stage, follow this MCP-integrated approach:

#### Pre-Implementation
1. Use **filesystem tools** to list and read existing relevant files
2. Use **filesystem tools** to verify project structure
3. Use **SQLite tools** to check existing data (if applicable)

#### During Implementation
1. Use **filesystem tools** to create necessary directories
2. Use **filesystem tools** to read input data/configurations
3. Process data (analysis, transformation, modeling)
4. Use **filesystem tools** to write outputs to appropriate locations
5. Use **filesystem tools** to write logs for audit trail

#### Post-Implementation Verification
1. Use **filesystem tools** to list all created files and verify existence
2. Use **filesystem tools** to read outputs and validate content
3. Use **SQLite tools** to verify database changes (if applicable)
4. Document which MCP tools were used in the verification checklist

### MCP Integration in Acceptance Criteria Verification

When verifying acceptance criteria, explicitly state MCP tool usage:

```
Acceptance Criterion 1: Data extracted and saved to data/1_raw/
✅ Verified using filesystem tools: 
   - Listed directory contents: data/1_raw/hospital_visits.csv exists
   - File size: 2.5 MB (verified non-empty)
   - Read first 5 rows to confirm data structure

Acceptance Criterion 2: Quality report generated
✅ Verified using filesystem tools:
   - Report exists at: reports/quality_report_2026-02-06.md
   - Report contains required sections (checked via file read)
```

### Implementation Stages

The implementation MUST proceed through stages aligned with the data analysis lifecycle. **Adapt these stages according to the specific implementation plan provided:**

- **If the plan specifies different stages**: Follow the plan's structure exactly
- **If the plan is task-oriented**: Map tasks to appropriate lifecycle stages below
- **If the plan omits stages**: Skip irrelevant stages (e.g., modeling for descriptive analysis)
- **If the plan combines stages**: Execute combined activities as specified
- **Always prioritize**: The implementation plan's instructions over these generic stages

The following stages represent a complete data analysis lifecycle and should be selectively applied based on the implementation plan:

#### Stage 0: Environment Setup & Dependencies
- Configure Python environment (virtual environment, conda, etc.)
- Use **configure_python_environment** tool to set up the workspace environment
- Install all required Python packages and libraries from `requirements.txt`
- Use **install_python_packages** tool for package installation in **kernel and environment**
- Verify Python version compatibility with project requirements
- Install additional system dependencies if needed
- Test import of critical libraries to ensure proper installation
- Document environment specifications (Python version, package versions)
- Use **get_python_environment_details** to verify installation success
- Set up any required API keys or environment variables
- Configure database connections if applicable
- Verify MCP tools availability (filesystem, SQLite, GitHub)

#### Stage 1: Problem Understanding & Setup
- Review user story and acceptance criteria thoroughly
- Understand business context and analytical objectives
- Set up project structure (directories, notebooks, configurations)
- Verify data sources and access requirements
- Document assumptions and constraints
- Use **filesystem tools** to create necessary directory structure

#### Stage 2: Data Collection & Extraction
- Extract data from source systems using appropriate methods
- Use **filesystem tools** to read data from `data/1_raw/` or `data/2_external/`
- Use **SQLite tools** for database extractions (if applicable)
- Implement data fetching logic with proper error handling and retries
- Save raw data with appropriate metadata and timestamps
- Document data lineage and extraction parameters
- Verify data completeness and successful extraction

#### Stage 3: Data Profiling & Quality Assessment
- Generate comprehensive data quality reports
- Analyze data distributions, missing values, and outliers
- Identify data types, formats, and schema inconsistencies
- Document data quality issues and anomalies
- Create data profiling notebooks in `notebooks/1_exploratory/`
- Use **filesystem tools** to save profiling results to `results/tables/`
- Establish data quality metrics and thresholds

#### Stage 4: Data Cleaning & Preprocessing
- Implement data cleaning logic based on profiling findings
- Handle missing values using appropriate strategies
- Correct data types and format inconsistencies
- Remove or flag outliers based on business rules
- Standardize and normalize data as needed
- Use **filesystem tools** to write cleaned data to `data/3_interim/`
- Document all transformations and cleaning decisions
- Log data cleaning operations to `logs/etl/`

#### Stage 5: Exploratory Data Analysis (EDA)
- Conduct statistical analysis and hypothesis testing
- Create visualizations to understand patterns and relationships
- Identify key insights and anomalies
- Explore temporal trends, correlations, and distributions
- Create analysis notebooks in `notebooks/2_analysis/`
- Use **filesystem tools** to save figures to `reports/figures/`
- Document findings and preliminary insights

#### Stage 6: Feature Engineering & Transformation
- Design and create relevant features based on domain knowledge
- Apply transformations (aggregations, encodings, scaling)
- Create derived metrics and calculated fields
- Validate feature quality and relevance
- Create feature engineering notebooks in `notebooks/3_feature_engineering/`
- Use **filesystem tools** to save processed data to `data/4_processed/`
- Document feature definitions and calculation logic

#### Stage 7: Analysis Implementation & Modeling
- Implement analytical methods or statistical models
- Perform calculations, aggregations, or predictive modeling
- Apply domain-specific analytical frameworks
- Validate analytical outputs against business logic
- Use **filesystem tools** to save model artifacts to `models/`
- Use **filesystem tools** to save analysis results to `results/`
- Document methodology and analytical approach

#### Stage 8: Results Validation & Quality Assurance
- Verify outputs meet acceptance criteria
- Validate analytical results against known benchmarks
- Perform sensitivity analysis and robustness checks
- Review results with domain experts (if applicable)
- Document validation procedures and outcomes
- Use **filesystem tools** to save validation results to `results/metrics/`
- Log validation checks to `logs/audit/`

#### Stage 9: Documentation & Reporting
- Create comprehensive analysis documentation
- Generate reports with findings, insights, and recommendations
- Create executive summaries and technical documentation
- Build interactive dashboards or visualizations (if required)
- Use **filesystem tools** to save reports to `reports/`
- Ensure all code is well-commented and reproducible
- Document limitations and future improvement opportunities

#### Stage 10: Delivery & Handoff
- Package final deliverables (data, code, reports, dashboards)
- Verify all acceptance criteria are met
- Complete verification checklists
- Prepare handoff documentation
- Use **filesystem tools** to organize final outputs
- Archive logs and intermediate outputs appropriately
- Provide recommendations for next steps or iterations

## Data Plugin Integration for Next Step Analysis

Before and during implementation, leverage the data plugin to analyze and optimize the next code generation steps:

### Pre-Implementation Analysis

Use data plugin commands to gather context and validate approach:

1. **Explore Existing Data** (`/explore-data`)
   - Profile datasets before writing transformation logic
   - Identify data quality issues that affect implementation approach
   - Discover actual data distributions to inform validation thresholds
   - Example: Before implementing data cleaning, run `/explore-data data/1_raw/patient_visits.csv` to understand null patterns

2. **Validate Queries** (`/write-query`)
   - Generate optimized SQL for data extraction steps
   - Ensure dialect-specific best practices are followed
   - Test query logic before embedding in pipeline code
   - Example: Use `/write-query` to generate PostgreSQL query for complex temporal aggregations

3. **Analyze Context** (`data-context-extractor` skill)
   - Extract domain knowledge about metrics, entities, and business rules
   - Build company-specific data analysis skills for consistent implementation
   - Document tribal knowledge for future implementations
   - Example: Create MOH-specific data analysis skill documenting disease classification hierarchies

### During Implementation

Use data plugin commands to accelerate code generation:

1. **Generate Visualizations** (`/create-viz`)
   - Create publication-quality charts instead of writing matplotlib code from scratch
   - Follow visualization best practices automatically
   - Ensure consistent styling across analysis outputs
   - Example: Generate time series plots for epidemiological trends

2. **Build Dashboards** (`/build-dashboard`)
   - Scaffold interactive HTML dashboards with proper structure
   - Apply dashboard design patterns automatically
   - Save development time on boilerplate code
   - Example: Create workforce capacity monitoring dashboard

3. **Statistical Analysis** (`/analyze`)
   - Perform statistical computations and exploratory analysis
   - Get quick answers to validate implementation logic
   - Generate analysis code snippets for integration
   - Example: Run hypothesis tests to validate correlation assumptions

4. **Continuous Validation** (`/validate`)
   - QA analysis outputs for methodology and accuracy
   - Detect common pitfalls before stakeholder delivery
   - Verify statistical assumptions and calculations
   - Example: Validate forecasting model outputs for bias and accuracy

### Determining Next Code Generation Step

When the implementation plan is ambiguous or requires decisions, use the data plugin to inform next steps:

**Decision Framework:**

1. **If data characteristics are unknown**: Run `/explore-data` first
   - Determines cleaning strategy (handling nulls, outliers)
   - Informs feature engineering approach
   - Validates data availability for planned analysis

2. **If query logic is complex**: Use `/write-query` to prototype
   - Tests extraction logic before pipeline implementation
   - Validates join relationships and aggregation correctness
   - Ensures performance optimization

3. **If visualization requirements are unclear**: Use `/create-viz` to prototype
   - Generates sample charts to validate with stakeholders
   - Determines appropriate chart types based on data
   - Identifies visualization library requirements

4. **If analysis methodology needs validation**: Run `/analyze` or `/validate`
   - Verifies statistical approach before full implementation
   - Identifies potential issues early
   - Generates reference outputs for comparison

**Adaptive Implementation Workflow:**

```
1. Review implementation plan stage
2. Identify knowledge gaps or uncertainties
3. Select appropriate data plugin command to gather context
4. Execute command and analyze results
5. Adjust implementation approach based on findings
6. Generate code with informed decisions
7. Validate outputs using `/validate`
8. Proceed to next stage
```

This approach ensures that code generation is **data-driven and context-aware**, reducing rework and improving implementation quality.

## Verification Requirements

After implementation, the following verifications MUST be completed:

1. **Acceptance Criteria Verification**
   - Each acceptance criterion MUST be verified as met
   - Any discrepancies MUST be documented

2. **Design Implementation Verification**
   - Complete the Design Implementation Verification Checklist
   - The checklist MUST include the sections below

- Explicitly check that all service and API integration logic is implemented, not just stubbed.
- During verification, confirm that all functions required to fetch, process, and return data are fully implemented and tested.
- If any function is a stub or placeholder, the implementation is NOT complete. Document this as a failure and halt further verification until resolved.

### Color Verification Table
The Color Verification table MUST:
- List every color specified in the design
- Compare design color values with implementation
- Verify exact matches using this format:

```
| Element | Design Color | Implementation | Status |
|---------|--------------|----------------|--------|
| Header Text | #718EBF | text-[#718EBF] | ✅ Match |
| Regular Text | #232323 | text-[#232323] | ✅ Match |
| Positive Values | #16DBAA | text-[#16DBAA] | ✅ Match |
| Negative Values | #FE5C73 | text-[#FE5C73] | ✅ Match |
| Card Background | #FFFFFF | bg-white | ✅ Match |
| Separator Line | #F4F5F7 | bg-[#F4F5F7] | ✅ Match |
```

### Spacing Verification Table
The Spacing Verification table MUST:
- List all spacing values specified in the design
- Compare design spacing values with implementation
- Verify exact matches using this format:

```
| Element | Design Value | Implementation | Status |
|---------|--------------|----------------|--------|
| Card Padding | 24px | p-6 (1.5rem = 24px) | ✅ Match |
| Row Gap | 16px | gap-4 (1rem = 16px) | ✅ Match |
| Vertical Padding | 12px | py-3 (0.75rem = 12px) | ✅ Match |
```

### Typography Verification Table
The Typography Verification table MUST:
- List all typography values specified in the design
- Compare design typography values with implementation
- Verify exact matches using this format:

```
| Element | Design Value | Implementation | Status |
|---------|--------------|----------------|--------|
| Font Size | 16px | text-base (1rem = 16px) | ✅ Match |
| Header Weight | 500 | font-medium | ✅ Match |
| Text Weight | 400 | font-normal | ✅ Match |
| Line Height | 1.21 | leading-normal | ✅ Match |
```

### Structure Verification Checklist
The Structure Verification checklist MUST:
- Verify all structural elements match the design
- Include specific components and their properties
- Use this format:

```
- ✅ Card container matches design (rounded-3xl)
- ✅ Header row positioning correct
- ✅ Separator line positioned correctly
- ✅ Data rows structured correctly
- ✅ Column alignment matches design
```

## Error Handling Requirements

If implementation or verification fails, the output MUST:
- Clearly identify which part of the plan failed
- Describe the specific issue encountered
- Explain how it deviates from the plan or acceptance criteria
- Suggest possible solutions or next steps

## Documentation Requirements

The final output MUST include:
- Confirmation of completion if successful
- Results of all verification steps
- Any command outputs or test results
- The completed Design Implementation Verification Checklist
- Any noted discrepancies or issues