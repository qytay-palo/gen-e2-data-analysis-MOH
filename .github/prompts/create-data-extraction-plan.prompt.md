# Healthcare Data Extraction Plan

## Role and Context
You are a senior data engineer designing a production-ready data extraction plan for healthcare analytics. Create a plan that extracts data from source databases, validates quality, and prepares data for analysis using our analytics platforms.

## Technical Environment

### Analytics Platforms
- **HEALIX** (GCC Cloud): Databricks (R/Python), STATA
- **MCDR** (On-Premise): CDSW (R/Python), HUE (SQL), STATA
- **Compute**: Apache Spark (primary analytics engine)
- **Storage**: Hadoop Distributed File System (HDFS)

### Platform Selection Guidance
- **Large-scale data processing**: Use Spark on Databricks (HEALIX) or CDSW (MCDR)
- **Interactive SQL queries**: Use HUE (MCDR)
- **Statistical/econometric analysis**: Use STATA (both platforms)
- **Cloud vs On-Prem**: HEALIX for new projects, MCDR for legacy integration

## Project Context

Before creating the plan, identify:
- **Organization & Geography**: [Name, location, applicable regulations]
- **Data Sources**: [EHR, billing, labs, pharmacy systems]
- **Objectives**: [Clinical quality, operations, population health, research, compliance]
- **Stakeholders**: [Clinicians, administrators, researchers, policymakers]
- **Compliance**: [HIPAA, GDPR, PDPA, or other regulations]

## Core Objectives

Design an extraction plan that:
1. **Retrieves accurate, complete data** aligned with project objectives
2. **Ensures data quality** through healthcare-appropriate validation
3. **Optimizes for Spark/HDFS** with efficient batch processing
4. **Maintains reliability** via checkpoints and retry logic
5. **Enables automation** for scheduled, unattended operations
6. **Ensures compliance** with applicable healthcare regulations
7. **Supports both platforms** (HEALIX and MCDR as appropriate)

## Required Deliverables

### 1. Data Source Identification
**Output**: `docs/data_dictionary/source_systems.md`

- **Systems & Tables**: List databases, schemas, and tables (EHR, LIS, RIS, billing, pharmacy)
- **Key Entities**: Patients, encounters, diagnoses (ICD), procedures (CPT), medications, labs, vitals
- **Relationships**: Document primary/foreign keys and dependencies
- **Standards**: Identify applicable codes (HL7, FHIR, ICD-10/11, LOINC, SNOMED, CPT)
- **Volumes**: Estimate row counts, growth rates, and historical data size
- **Access**: Document credentials, VPN/network requirements, API access

### 2. Extraction Strategy
**Output**: `config/queries.yml`, `docs/methodology/extraction_approach.md`

**Mode Selection** (per data source):
- **Incremental**: Extract deltas based on timestamps/change data capture (daily/weekly updates)
- **Full**: Initial load or complete refresh (reference data, historical backfills)
- **Checkpoint**: Use HDFS for tracking extraction state, enable resume from failure

**Query Design for Spark/HDFS**:
- Write SQL optimized for Spark execution (partition pruning, predicate pushdown)
- Use HUE for query development and validation
- Parameterize queries for dates, batch sizes, offsets
- Leverage indexed columns, avoid SELECT *
- Consider partitioning strategy for HDFS storage

**Batch Processing**:
- Define optimal batch sizes for Spark (e.g., 100K-1M rows per partition)
- Use Spark's distributed processing capabilities
- Implement pagination (LIMIT/OFFSET or cursor-based)
- Stream to HDFS to manage memory efficiently
- Log batch completion for restart capability

### 3. Data Quality & Validation
**Output**: `config/validation_rules.yml`, `src/data_processing/data_validator.py`

**Clinical Validation Rules**:
- **Temporal**: Encounter dates ≤ today, discharge ≥ admission, death ≥ birth
- **Ranges**: Age 0-120, vital signs within biologically plausible limits, lab values per test type
- **Codes**: ICD-10/11 format, valid CPT codes, LOINC for labs
- **Referential Integrity**: Valid patient/provider/facility IDs
- **Clinical Logic**: Age/gender-appropriate care, encounter type consistency

**Quality Checks**:
- Row count thresholds and historical comparison
- Required field completeness (null checks on critical columns)
- Data type validation (numeric, dates, categorical)
- Duplicate detection on primary/composite keys
- Statistical validation (outliers, distribution checks)

**Error Handling**:
- Define failure thresholds (e.g., >5% validation failures = stop pipeline)
- Quarantine invalid records for review
- Alert on critical failures
- Document remediation procedures

### 4. Transformation for Analytics
**Output**: `src/data_processing/transformers.py`, `notebooks/exploratory/01-data-profiling.ipynb`

**Standardization**:
- Convert column names to snake_case (if needed)
- Standardize date formats (ISO 8601)
- Cast to appropriate Spark data types
- Handle nulls consistently (None/NaN/NULL)
- Ensure UTF-8 encoding

**Cleaning**:
- Remove duplicates based on business keys
- Trim whitespace from text fields
- Standardize case (upper/lower)
- Map legacy codes to current standards

**Derived Fields**:
- Extract temporal features (year, month, quarter from dates)
- Calculate age from birth date, duration from timestamps
- Create flags/indicators for conditions and thresholds
- Pre-aggregate metrics for common analyses

### 5. Storage & Output

**File Format**:
- **Parquet** (primary): Columnar format optimized for Spark analytics, compression
- **CSV** (secondary): For compatibility with STATA and external tools
- Store in HDFS with appropriate replication factor

**Directory Structure (HDFS)**:
```
/data/
├── raw/                    # Unprocessed extraction
│   ├── clinical/
│   ├── administrative/
│   └── reference/
├── processed/              # Analysis-ready
│   └── [same structure]
└── external/               # Reference data, benchmarks
    └── code_mappings/      # ICD/CPT crosswalks
```

**Partitioning Strategy**:
- Partition by year/month/date for query performance
- Use Spark-optimized partition sizes (128MB-1GB per file)
- Enable partition pruning in queries

**Metadata**:
- Extraction timestamp, source system, row count, data size
- Validation results and data lineage
- Store metadata in Hive metastore or separate table

### 6. Execution Plan
**Output**: `config/database.yml`, `scripts/run_extraction.py`, `scripts/run_scheduler.py`

**Platform Selection**:
- **HEALIX/Databricks**: New projects, cloud-native workflows, large-scale Spark jobs
- **MCDR/CDSW**: Legacy system integration, on-prem requirements, HUE access needed
- **Tool Choice**: 
  - Python/R on Databricks or CDSW for ETL pipelines
  - HUE for ad-hoc SQL queries and validation
  - STATA for econometric analysis post-extraction

**Scheduling**:
- **Real-time/Hourly**: Critical alerts (if applicable)
- **Daily**: Clinical data, labs, pharmacy (run 2-4 AM)
- **Weekly**: Demographics, provider data (weekends)
- **Monthly**: Reference data, compliance reports (1st of month)
- Schedule during off-peak clinical hours

**Sequencing**:
- Extract reference tables before fact tables
- Identify parallel extraction opportunities (independent sources)
- Use Spark's parallelism for concurrent processing

**Retry Logic**:
- 3 automatic retries with exponential backoff (5s, 15s, 45s)
- Resume from last checkpoint on failure
- Alert on persistent failures

### 7. Monitoring & Logging
**Output**: `src/utils/logging_config.py`, `src/utils/monitoring.py`, `logs/`

**Key Metrics**:
- Performance: Extraction duration, Spark job metrics, HDFS I/O
- Data Quality: Validation pass rate, error counts by type
- System: Spark cluster utilization, HDFS storage usage
- Business: Data freshness, completeness

**Logging**:
- Structured logs for extraction events (start/end, row counts, errors)
- Store logs in HDFS or centralized logging system
- Use Spark's built-in logging with appropriate levels

**Alerting**:
- Critical: Extraction failures, data quality below threshold
- Warning: Performance degradation, approaching storage limits
- Info: Successful completion

### 8. Security & Compliance
**Output**: `.env`, `config/security_policies.md`, `docs/methodology/compliance_framework.md`

**Data Protection**:
- Store credentials in secure vaults (never hardcode)
- Use TLS 1.2+ for all connections
- Encrypt sensitive data at rest in HDFS
- Implement RBAC for platform access

**PHI/PII Handling**:
- Classify data elements per applicable regulations
- Apply de-identification (Safe Harbor, pseudonymization, tokenization)
- Mask PHI in logs and non-production environments
- Extract only minimum necessary data

**Compliance** (identify applicable):
- US: HIPAA, HITECH
- EU: GDPR
- Singapore: PDPA
- Other: [Specify based on geography]

**Audit**:
- Log all data access and queries
- Enable audit trail in Spark/Databricks
- Regular compliance reviews

### 9. Testing & Documentation
**Output**: `tests/`, `docs/`, `README.md`

**Testing**:
- Unit tests for validation rules and transformations
- Integration tests with test data
- Performance benchmarks with production volumes
- PHI protection verification

**Documentation**:
- Data dictionary (source → target mapping)
- Transformation logic
- Validation rules and thresholds
- Runbook for scheduled jobs
- Troubleshooting guide

## Output Format

```markdown
# Data Extraction Plan - [Project Name]

## Executive Summary
- Organization, geography, compliance requirements
- Data sources and objectives
- Platform selection (HEALIX vs MCDR) with rationale
- Key technical decisions

## 1. Data Sources
- Healthcare systems and tables
- Key entities and volumes
- Data standards (ICD, LOINC, etc.)

## 2. Extraction Approach
- Mode (incremental/full) per source
- Spark/HDFS optimization strategy
- Batch sizes and parallelization
- Query templates for HUE/Spark

## 3. Data Quality
- Clinical validation rules
- Quality thresholds
- Error handling procedures

## 4. Transformations
- Standardization steps
- Cleaning logic
- Derived fields

## 5. Storage
- HDFS directory structure
- Parquet/CSV format strategy
- Partitioning scheme

## 6. Execution
- Platform: HEALIX/Databricks or MCDR/CDSW
- Schedule (daily/weekly/monthly)
- Sequencing and dependencies
- Retry logic

## 7. Monitoring
- Spark metrics to track
- Logging approach
- Alert conditions

## 8. Security
- PHI/PII handling
- Compliance measures (HIPAA/GDPR/PDPA)
- Access controls

## 9. Implementation
- Phased rollout plan
- Testing approach
- Success criteria

## Appendices
- Sample Spark/SQL queries
- Validation rule examples
- HDFS path conventions

## File Structure Reference
```
config/
├── database.yml           # Database connections, extraction settings
├── queries.yml            # SQL query templates
└── validation_rules.yml   # Data quality rules

data/
├── raw/                   # Unprocessed extracted data
├── interim/               # Partially processed data
├── processed/             # Analysis-ready data
└── external/              # Reference data, code mappings

docs/
├── project-context/
│   ├── data-extraction-strategy.md
│   └── data-cleaning-plan.md
├── data_dictionary/
│   └── source_systems.md  # Data source documentation
├── methodology/
│   ├── extraction_approach.md
│   └── compliance_framework.md
└── DATA_EXTRACTION_GUIDE.md

notebooks/
├── exploratory/
│   ├── 01-query-testing.ipynb
│   └── 02-data-profiling.ipynb
└── analysis/

scripts/
├── run_extraction.py      # Manual extraction CLI
└── run_scheduler.py       # Automated scheduler

src/
├── data_processing/
│   ├── db_connector.py    # Database connections
│   ├── data_extractor.py  # Extraction logic
│   ├── data_validator.py  # Validation rules
│   ├── transformers.py    # Data transformations
│   └── etl_pipeline.py    # Pipeline orchestration
└── utils/
    ├── logging_config.py  # Logging setup
    └── monitoring.py      # Performance monitoring

tests/
├── test_extraction.py
├── test_validation.py
└── test_transformers.py

logs/
├── extraction.log         # Extraction events
├── errors.log             # Error tracking
└── audit.log              # Audit trail

.env                       # Credentials (DO NOT COMMIT)
README.md                  # Project overview
requirements.txt           # Python dependencies
```

## Success Criteria

- ✅ **Reliability**: <1% failure rate
- ✅ **Quality**: >95% validation pass rate
- ✅ **Performance**: Spark jobs complete within SLA
- ✅ **Compliance**: Passes regulatory audits
- ✅ **Usability**: Data accessible in STATA/Databricks/CDSW
- ✅ **Freshness**: Data available per business requirements

## Implementation Steps

After creating the plan:
1. **Review** with technical lead, clinical SMEs, compliance team
   - Files: `docs/project-context/data-extraction-strategy.md`, `docs/project-context/data-cleaning-plan.md`
2. **Prototype** queries in HUE, test Spark jobs on sample data
   - Files: `config/queries.yml`, `notebooks/exploratory/01-query-testing.ipynb`
3. **Configure** extraction settings and validation rules
   - Files: `config/database.yml`, `config/validation_rules.yml`, `.env`
4. **Develop** ETL pipeline modules
   - Files: `src/data_processing/`, `src/utils/`, `scripts/`
5. **Test** with pilot data sources
   - Files: `tests/`, `data/interim/`, validation logs in `logs/`
6. **Deploy** to production environment
   - Monitor: `logs/extraction.log`, `logs/audit.log`
7. **Document** final implementation
   - Files: `docs/DATA_EXTRACTION_GUIDE.md`, `docs/ARCHITECTURE.md`, `README.md`

## Output Format

Provide your response as **one separate, well-structured markdown documents**:

1. **`docs/project-context/data-extraction-strategy.md`** - Primary strategic document (3,000-4,000 words)
2. **`docs/project-context/data-cleaning-plan.md`** - Phasing and value delivery (1,500-2,500 words)

### Document Requirements

Each document should be:
- **Comprehensive yet concise** - Cover all required elements without unnecessary detail
- **Scannable** - Use clear headings, bullets, and tables for easy navigation
- **Professional** - Written for technical and business stakeholders alike
- **Referenceable** - Each section should stand alone and be easily cited in downstream documents
- **Cross-linked** - Reference other documents where appropriate (e.g., "See Value Delivery Roadmap for phasing details")

### Presentation Format

Present your response as follows:

```markdown
# Document 1: Data Extraction Strategy

[Full content of data-extraction-strategy.md]

---

# Document 2: Data Cleaning Plan

[Full content of data-cleaning-plan.md]

```

Each document should be complete and ready to save directly to its respective file path.

---