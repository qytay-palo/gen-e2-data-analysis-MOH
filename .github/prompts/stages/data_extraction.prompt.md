---
description: Data Extraction Stage with MCP Integration
stage: Data Acquisition
---

# Stage Prompt: Data Extraction

## Objective

Extract data from configured sources and organize it according to the project structure using MCP filesystem and database tools for automated, efficient data acquisition.

## Required MCP Tools

- **Filesystem Server** (REQUIRED): For creating directories, saving extracted data, and managing schemas
- **SQLite Server** (when applicable): For querying source databases directly

## Input Requirements

The following inputs MUST be available before proceeding:

1. **Data Source Configuration**: `config/data_sources.yml`
   - Connection details (if database)
   - File paths (if file-based)
   - API endpoints (if API-based)
   - Authentication credentials (from environment variables)

2. **Extraction Queries** (if applicable): `sql/extractions/`
   - SQL queries for database extraction
   - Query parameters and filters

3. **Target Epic/User Story**: 
   - Epic number (e.g., epic-001)
   - User story identifier
   - Data requirements from user story acceptance criteria

4. **Project Context** (REQUIRED - read before extraction):
   - **Available data sources**: `docs/project_context/data_sources.md`
   - **Technical stack capabilities**: `docs/project_context/tech_stack.md`
   - **Business objectives**: `docs/project_context/business-objectives.md`
   
   **Use MCP filesystem tools to read these files** and understand:
   - What data sources are available and how to access them
   - What technical platforms and tools are approved
   - What business objectives drive data needs

## Output Requirements

The extraction MUST produce:

1. **Raw Data Files**: `data/1_raw/{epic_id}/`
   - Original, immutable source data
   - Filename format: `{source_name}_{timestamp}.{format}`
   - Supported formats: CSV, JSON, Parquet, Excel

2. **Schema Documentation**: `data/schemas/{epic_id}/`
   - Data dictionary for each extracted dataset
   - Column names, data types, descriptions
   - Sample values and value ranges

3. **Extraction Metadata**: `data/1_raw/{epic_id}/metadata.json`
   - Extraction timestamp
   - Source system and version
   - Row counts and file sizes
   - Extraction parameters used

4. **Extraction Log**: `logs/etl/extraction_{epic_id}_{timestamp}.log`
   - Extraction start/end times
   - Success/failure status
   - Any warnings or errors encountered
   - Data quality summary

## Execution Steps

### Step 1: Pre-Extraction Setup (using MCP filesystem tools)

```
1. Use filesystem tools to read config/data_sources.yml
2. Identify the data sources needed for this epic
3. Use filesystem tools to create target directory: data/1_raw/{epic_id}/
4. Use filesystem tools to create schema directory: data/schemas/{epic_id}/
5. Use filesystem tools to list existing files to check for duplicates
```

**Example MCP Commands**:
- "Use filesystem tools to read config/data_sources.yml and show me the data sources for epic-001"
- "Use filesystem tools to create directory data/1_raw/epic-001/"
- "Use filesystem tools to list all files in data/1_raw/epic-001/ to check what already exists"

### Step 2: Data Extraction (using appropriate MCP tools)

#### For Database Sources (SQLite/SQL):
```
1. Use SQLite tools to connect to the source database
2. For each extraction query in sql/extractions/:
   a. Use filesystem tools to read the SQL query file
   b. Use SQLite tools to execute the query
   c. Use filesystem tools to save results to data/1_raw/{epic_id}/{table_name}.csv
   d. Record row count and extraction time
```

**Example MCP Commands**:
- "Use SQLite tools to query the patient_visits table with date range filter"
- "Use filesystem tools to save the query results to data/1_raw/epic-001/patient_visits_2026-02-06.csv"

#### For File-Based Sources:
```
1. Use filesystem tools to read source file locations from config
2. Use filesystem tools to copy or read source files
3. Use filesystem tools to write to data/1_raw/{epic_id}/
4. Verify file integrity (size, format)
```

**Example MCP Commands**:
- "Use filesystem tools to read /external/kaggle/healthcare_dataset.csv"
- "Use filesystem tools to copy the data to data/1_raw/epic-001/healthcare_dataset.csv"

#### For API Sources (manual processing required):
```
1. Use filesystem tools to read API configuration
2. Make API calls (programmatically)
3. Use filesystem tools to save API responses to data/1_raw/{epic_id}/
4. Handle pagination and rate limiting
```

### Step 3: Schema Documentation (using MCP filesystem tools)

```
1. Analyze the structure of each extracted dataset
2. Generate data dictionary with:
   - Column names
   - Data types (inferred)
   - Non-null counts
   - Unique value counts
   - Sample values (first 5)
3. Use filesystem tools to write schema documentation to data/schemas/{epic_id}/{dataset_name}_schema.md
```

**Example MCP Commands**:
- "Analyze the structure of data/1_raw/epic-001/patient_visits.csv"
- "Use filesystem tools to write the schema documentation to data/schemas/epic-001/patient_visits_schema.md"

### Step 4: Metadata Generation (using MCP filesystem tools)

```
1. Collect extraction metadata:
   - Timestamp: Current datetime
   - Source: From config/data_sources.yml
   - Row count: From extracted data
   - File size: From file system
   - Extraction parameters: Query filters, date ranges, etc.
2. Format as JSON
3. Use filesystem tools to write to data/1_raw/{epic_id}/metadata.json
```

**Example MCP Commands**:
- "Use filesystem tools to write extraction metadata to data/1_raw/epic-001/metadata.json"

### Step 5: Logging (using MCP filesystem tools)

```
1. Create extraction log with:
   - Epic ID and user story reference
   - Start time and end time
   - List of extracted datasets with row counts
   - Success/failure status for each source
   - Any errors or warnings
2. Use filesystem tools to write log to logs/etl/extraction_{epic_id}_{timestamp}.log
```

**Example MCP Commands**:
- "Use filesystem tools to write the extraction log to logs/etl/extraction_epic-001_20260206.log"

### Step 6: Verification (using MCP filesystem tools)

```
1. Use filesystem tools to list all files in data/1_raw/{epic_id}/
2. Verify each expected file exists
3. Use filesystem tools to check file sizes (should be > 0)
4. Use filesystem tools to read first 5 rows of each dataset
5. Verify schema files exist in data/schemas/{epic_id}/
6. Verify metadata.json exists and is valid JSON
7. Verify extraction log exists in logs/etl/
```

**Example MCP Commands**:
- "Use filesystem tools to list all files in data/1_raw/epic-001/ and show their sizes"
- "Use filesystem tools to read the first 5 lines of data/1_raw/epic-001/patient_visits.csv"
- "Use filesystem tools to verify that data/schemas/epic-001/patient_visits_schema.md exists"

## Quality Checks

After extraction, perform these quality checks:

### 1. Completeness Check
```
- All expected datasets extracted? (compare with data source config)
- Row counts match expectations? (compare with source system if possible)
- All columns present? (compare with schema documentation)
```

### 2. Integrity Check
```
- Files are not corrupted (can be opened and read)
- Data types are as expected
- No completely empty files (size > 0)
```

### 3. Documentation Check
```
- Schema documentation exists for each dataset
- Metadata.json is present and valid
- Extraction log is complete and informative
```

## Error Handling

If extraction fails or encounters issues:

1. **Use filesystem tools to write detailed error log** to `logs/errors/extraction_{epic_id}_{timestamp}.log`
2. **Document the specific failure**:
   - Which data source failed
   - Error message and stack trace
   - Potential root causes
   - Suggested remediation steps
3. **Partial Success Handling**:
   - If some datasets extracted successfully, document which ones
   - Mark failed extractions clearly in the log
   - Continue with available data if acceptable

## Success Criteria

The data extraction is considered successful when:

- ✅ All required datasets are extracted and saved to `data/1_raw/{epic_id}/`
- ✅ All files are non-empty and readable (verified via MCP filesystem tools)
- ✅ Schema documentation exists for each dataset in `data/schemas/{epic_id}/`
- ✅ Metadata file `metadata.json` is present and valid
- ✅ Extraction log exists in `logs/etl/` and shows success status
- ✅ Quality checks pass (completeness, integrity, documentation)

## MCP Tools Usage Summary

At the end of extraction, document MCP tool usage:

```markdown
### MCP Tools Used

**Filesystem Server**:
- Created directories: data/1_raw/epic-001/, data/schemas/epic-001/
- Files written: 5 datasets, 5 schema docs, 1 metadata file, 1 log file
- Files read: config/data_sources.yml, sql/extractions/*.sql
- Verification: Listed directories, checked file sizes, read sample rows

**SQLite Server** (if used):
- Executed queries: 3 extraction queries from sql/extractions/
- Tables accessed: patient_visits, diagnoses, treatments
- Total rows extracted: 125,000 rows
```

## Next Stage

After successful data extraction, proceed to:
- **Data Quality Assessment** stage: Validate data completeness and integrity
- **Exploratory Data Analysis** stage: Initial analysis and profiling

## References

- Data Sources: `docs/project_context/data_sources.md`
- Tech Stack: `docs/project_context/tech_stack.md`
- Project Structure: `README.md`
