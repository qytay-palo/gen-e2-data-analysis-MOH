---
description: Prompt for Execution of the Implementation Plan
stage: Development
---
# AI Agent Prompt: Execute Implementation Plan

## Objective

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

The implementation MUST proceed through these sequential stages:

#### Stage 1: Basic Structure Implementation
- Create component hierarchy and file structure
- Implement basic layout without detailed styling
- Verify structure matches design specifications

#### Stage 2: Color Implementation
- Apply ALL colors as exact hex values (#RRGGBB) first
- Double-check every color against design specification
- Convert to Tailwind color tokens only if they are an EXACT match

#### Stage 3: Layout & Spacing Implementation
- Apply exact padding, margin and gap values in pixels
- Validate that spacing perfectly matches design specification
- Convert to Tailwind spacing classes only if they are an EXACT match

#### Stage 4: Typography & Detail Implementation
- Apply font families, sizes, weights, and line heights exactly as specified
- Implement any remaining details (borders, shadows, etc.)
- Verify against design specification

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