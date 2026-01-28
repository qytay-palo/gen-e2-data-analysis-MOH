# Data Sources: MOH Polyclinic Data Analysis

**Source**: Ministry of Health (MOH) Singapore Data  
**URL**: https://data.gov.sg/datasets?agencies=Ministry+of+Health+(MOH)&resultId=522  
**Last Updated**: 2026-01-26  
**Data Domain**: Healthcare - Primary Care (Polyclinics)

---

## Initialization

When analyzing this dataset, you are working with **Singapore's Ministry of Health polyclinic healthcare data**, which contains comprehensive patient visit records, diagnoses, treatments, and demographic information from public polyclinics. The data structure follows a **relational database model** with multiple interconnected tables capturing the patient journey from registration to treatment outcomes.

**Key Relationships**:
- Each **patient** can have multiple **attendances** (visits)
- Each **attendance** can have multiple **diagnoses**, **procedures**, **medications**, and **lab results**
- All tables link through common identifiers: `patient_id`, `attendance_id`, `polyclinic_id`

**Data Characteristics**:
- **Temporal range**: 2015-01-01 to present
- **Update frequency**: Daily incremental extraction
- **Geographic scope**: Singapore polyclinics
- **Privacy**: De-identified patient data with anonymized IDs

---

## Table Schema Overview

### **1. POLYCLINIC_ATTENDANCES** (Patient Visits)
**Purpose**: Records every patient visit/attendance at a polyclinic  
**Primary Key**: `attendance_id`  
**Incremental**: Yes (by `attendance_date`)

| Column Name | Data Type | Description | Example Values | Business Logic |
|-------------|-----------|-------------|----------------|----------------|
| `attendance_id` | INTEGER | Unique identifier for each visit | 1001234 | Primary key |
| `patient_id` | INTEGER | Links to patient demographics | 500123 | Foreign key to patient |
| `polyclinic_id` | INTEGER | Which polyclinic was visited | 101-115 | Foreign key to polyclinic |
| `attendance_date` | DATE | Date of visit | 2025-12-15 | Used for time-series analysis |
| `attendance_time` | TIME | Scheduled appointment time | 09:30:00 | Appointment slot |
| `visit_type` | VARCHAR | Type of medical visit | 'acute', 'chronic', 'preventive', 'follow-up' | Categorizes care type |
| `appointment_type` | VARCHAR | How visit was scheduled | 'walk-in', 'appointment', 'emergency' | Access pathway |
| `visit_status` | VARCHAR | Completion status | 'completed', 'cancelled', 'no-show' | Operational metric |
| `arrival_time` | TIME | Actual patient arrival | 09:25:00 | Calculate lateness |
| `consultation_start_time` | TIME | When doctor started | 09:45:00 | Service delivery start |
| `consultation_end_time` | TIME | When consultation ended | 10:15:00 | Service delivery end |
| `waiting_time_minutes` | INTEGER | Time from arrival to consultation | 20 | Key performance metric |
| `consultation_duration_minutes` | INTEGER | Length of doctor consultation | 30 | Service quality metric |
| `referring_source` | VARCHAR | Who referred the patient | 'self', 'GP', 'hospital', 'A&E' | Referral pathway |
| `created_at` | TIMESTAMP | Record creation timestamp | 2025-12-15 10:30:00 | Audit trail |
| `updated_at` | TIMESTAMP | Last modification timestamp | 2025-12-15 11:00:00 | Change tracking |

**LLM Analysis Prompts**:
- *"Calculate average waiting times by polyclinic and time of day"*
- *"Identify peak attendance hours and days of the week"*
- *"Compare walk-in vs appointment visit patterns"*
- *"Analyze no-show rates by appointment type"*

---

### **2. PATIENT_DEMOGRAPHICS** (Patient Information)
**Purpose**: Stores anonymized demographic information for each patient  
**Primary Key**: `patient_id`  
**Incremental**: Yes (by `updated_at`)

| Column Name | Data Type | Description | Example Values | Business Logic |
|-------------|-----------|-------------|----------------|----------------|
| `patient_id` | INTEGER | Unique patient identifier (anonymized) | 500123 | Primary key |
| `birth_year` | INTEGER | Year of birth (not full DOB for privacy) | 1975 | Calculate age |
| `age_group` | VARCHAR | Binned age category | '0-10', '11-20', '21-30', '65+' | Population segmentation |
| `gender` | VARCHAR | Biological sex | 'M', 'F' | Demographic analysis |
| `race` | VARCHAR | Ethnic group | 'Chinese', 'Malay', 'Indian', 'Others' | Singapore demographics |
| `nationality` | VARCHAR | Citizenship status | 'Singaporean', 'PR', 'Foreigner' | Eligibility categories |
| `residential_status` | VARCHAR | Housing status | 'HDB', 'Private', 'Others' | Socioeconomic proxy |
| `postal_code` | VARCHAR | First 2 digits only (privacy) | '60', '73', '11' | Geographic distribution |
| `planning_area` | VARCHAR | Singapore planning area | 'Ang Mo Kio', 'Tampines', 'Jurong' | Geographic analysis |
| `region` | VARCHAR | Geographic region | 'North', 'South', 'East', 'West', 'Central' | Macro geography |
| `registration_date` | DATE | First registration at polyclinic | 2018-03-12 | Patient tenure |
| `healthier_sg_enrolled` | BOOLEAN | Enrolled in Healthier SG program | TRUE, FALSE | National health initiative |
| `healthier_sg_enrolment_date` | DATE | When enrolled in program | 2023-07-01 | Program tracking |
| `chronic_conditions_count` | INTEGER | Number of chronic conditions | 0, 1, 2, 3+ | Disease burden metric |
| `subsidy_category` | VARCHAR | Government subsidy tier | 'Pioneer', 'CHAS', 'Merdeka', 'None' | Financial assistance |
| `created_at` | TIMESTAMP | Record creation | 2018-03-12 09:00:00 | Audit trail |
| `updated_at` | TIMESTAMP | Last update | 2025-11-20 14:30:00 | Change tracking |

---

### **3. DIAGNOSIS_RECORDS** (Medical Diagnoses)
**Purpose**: Records medical diagnoses made during each visit  
**Primary Key**: `diagnosis_id`  
**Incremental**: Yes (by `diagnosis_date`)

| Column Name | Data Type | Description | Example Values | Business Logic |
|-------------|-----------|-------------|----------------|----------------|
| `diagnosis_id` | INTEGER | Unique diagnosis record ID | 2001234 | Primary key |
| `attendance_id` | INTEGER | Links to visit record | 1001234 | Foreign key to attendance |
| `patient_id` | INTEGER | Links to patient | 500123 | Foreign key to patient |
| `diagnosis_date` | DATE | When diagnosis was made | 2025-12-15 | Temporal tracking |
| `diagnosis_type` | VARCHAR | Category of diagnosis | 'primary', 'secondary', 'complication' | Diagnostic hierarchy |
| `icd_code` | VARCHAR | ICD-10 diagnosis code | 'J06.9', 'E11.9', 'I10' | International standard |
| `icd_version` | VARCHAR | ICD coding version | 'ICD-10-CM', 'ICD-11' | Version control |
| `diagnosis_description` | TEXT | Human-readable diagnosis | 'Acute upper respiratory infection' | Clinical interpretation |
| `condition_category` | VARCHAR | Disease grouping | 'Respiratory', 'Cardiovascular', 'Metabolic' | Disease classification |
| `is_chronic` | BOOLEAN | Is this a chronic condition | TRUE, FALSE | Care type indicator |
| `is_primary_diagnosis` | BOOLEAN | Main reason for visit | TRUE, FALSE | Chief complaint |
| `diagnosis_sequence` | INTEGER | Order of diagnosis | 1, 2, 3 | Priority ranking |
| `created_at` | TIMESTAMP | Record creation | 2025-12-15 10:45:00 | Audit trail |
| `updated_at` | TIMESTAMP | Last modification | 2025-12-15 11:00:00 | Change tracking |

**Common ICD-10 Codes**:
- `J06.9` - Upper respiratory infection (acute)
- `E11.9` - Type 2 diabetes mellitus
- `I10` - Essential hypertension
- `E78.5` - Hyperlipidemia
- `M54.5` - Low back pain

---

### **4. PROCEDURE_RECORDS** (Medical Procedures)
**Purpose**: Documents procedures, treatments, and interventions performed  
**Primary Key**: `procedure_id`  
**Incremental**: Yes (by `procedure_date`)

| Column Name | Data Type | Description | Example Values | Business Logic |
|-------------|-----------|-------------|----------------|----------------|
| `procedure_id` | INTEGER | Unique procedure record | 3001234 | Primary key |
| `attendance_id` | INTEGER | Associated visit | 1001234 | Foreign key to attendance |
| `patient_id` | INTEGER | Patient identifier | 500123 | Foreign key to patient |
| `procedure_date` | DATE | When procedure performed | 2025-12-15 | Temporal tracking |
| `procedure_code` | VARCHAR | Standardized procedure code | 'CPT-99213', 'HCPCS-G0008' | Billing/clinical code |
| `procedure_description` | TEXT | What was done | 'Blood glucose test', 'ECG', 'Wound dressing' | Clinical detail |
| `procedure_type` | VARCHAR | Category of procedure | 'Diagnostic', 'Therapeutic', 'Preventive' | Service classification |
| `provider_id` | INTEGER | Healthcare provider ID | 7001 | Anonymized clinician |
| `procedure_cost` | DECIMAL | Total cost (SGD) | 45.00 | Financial metric |
| `patient_charge` | DECIMAL | Amount charged to patient | 15.00 | Out-of-pocket cost |
| `subsidy_amount` | DECIMAL | Government subsidy | 30.00 | Public funding |
| `created_at` | TIMESTAMP | Record creation | 2025-12-15 11:00:00 | Audit trail |
| `updated_at` | TIMESTAMP | Last modification | 2025-12-15 11:15:00 | Change tracking |

---

### **5. MEDICATION_PRESCRIPTIONS** (Medications)
**Purpose**: Records all medications prescribed during visits  
**Primary Key**: `prescription_id`  
**Incremental**: Yes (by `prescription_date`)

| Column Name | Data Type | Description | Example Values | Business Logic |
|-------------|-----------|-------------|----------------|----------------|
| `prescription_id` | INTEGER | Unique prescription record | 4001234 | Primary key |
| `attendance_id` | INTEGER | Associated visit | 1001234 | Foreign key to attendance |
| `patient_id` | INTEGER | Patient identifier | 500123 | Foreign key to patient |
| `prescription_date` | DATE | When prescribed | 2025-12-15 | Temporal tracking |
| `medication_code` | VARCHAR | Drug classification code | 'ATC-C09AA01' | WHO ATC system |
| `medication_name` | VARCHAR | Drug name | 'Metformin', 'Lisinopril', 'Paracetamol' | Generic/brand name |
| `medication_category` | VARCHAR | Drug class | 'Antidiabetic', 'Antihypertensive', 'Analgesic' | Therapeutic category |
| `dosage` | VARCHAR | Strength per unit | '500mg', '10mg', '325mg' | Clinical dose |
| `frequency` | VARCHAR | How often taken | 'BD' (twice daily), 'TDS' (3x), 'PRN' (as needed) | Dosing schedule |
| `duration_days` | INTEGER | Length of prescription | 30, 60, 90 | Supply duration |
| `quantity` | INTEGER | Total units prescribed | 60 (tablets) | Inventory count |
| `medication_cost` | DECIMAL | Total medication cost | 25.00 | Financial metric |
| `patient_charge` | DECIMAL | Patient pays | 8.00 | Out-of-pocket |
| `subsidy_amount` | DECIMAL | Government subsidy | 17.00 | Public funding |
| `is_chronic_medication` | BOOLEAN | For chronic disease | TRUE, FALSE | Long-term therapy |
| `created_at` | TIMESTAMP | Record creation | 2025-12-15 11:00:00 | Audit trail |
| `updated_at` | TIMESTAMP | Last modification | 2025-12-15 11:15:00 | Change tracking |

---

### **6. LABORATORY_RESULTS** (Lab Tests)
**Purpose**: Stores laboratory test orders and results  
**Primary Key**: `lab_result_id`  
**Incremental**: Yes (by `result_date`)

| Column Name | Data Type | Description | Example Values | Business Logic |
|-------------|-----------|-------------|----------------|----------------|
| `lab_result_id` | INTEGER | Unique lab result record | 5001234 | Primary key |
| `attendance_id` | INTEGER | Associated visit | 1001234 | Foreign key to attendance |
| `patient_id` | INTEGER | Patient identifier | 500123 | Foreign key to patient |
| `test_date` | DATE | When test was ordered | 2025-12-15 | Order date |
| `result_date` | DATE | When result was available | 2025-12-17 | Turnaround time |
| `test_code` | VARCHAR | LOINC or local code | 'LOINC-2345-7', 'GLU-001' | Test identifier |
| `test_name` | VARCHAR | Test description | 'Fasting glucose', 'HbA1c', 'Lipid panel' | Clinical name |
| `test_category` | VARCHAR | Test grouping | 'Biochemistry', 'Hematology', 'Microbiology' | Laboratory section |
| `result_value` | VARCHAR | Numeric or qualitative result | '6.5', '98', 'Positive' | Test outcome |
| `result_unit` | VARCHAR | Measurement unit | 'mmol/L', 'mg/dL', '%' | SI units |
| `reference_range` | VARCHAR | Normal value range | '3.9-6.1', '<140', '4-10' | Clinical reference |
| `is_abnormal` | BOOLEAN | Outside normal range | TRUE, FALSE | Clinical flag |
| `abnormal_flag` | VARCHAR | Type of abnormality | 'High', 'Low', 'Critical' | Severity indicator |
| `created_at` | TIMESTAMP | Record creation | 2025-12-17 14:00:00 | Audit trail |
| `updated_at` | TIMESTAMP | Last modification | 2025-12-17 14:30:00 | Change tracking |

---

### **7. POLYCLINIC_MASTER** (Reference Data)
**Purpose**: Master list of all polyclinics with facility information  
**Primary Key**: `polyclinic_id`  
**Incremental**: No (reference data, monthly refresh)

| Column Name | Data Type | Description | Example Values | Business Logic |
|-------------|-----------|-------------|----------------|----------------|
| `polyclinic_id` | INTEGER | Unique polyclinic identifier | 101, 102, 103 | Primary key |
| `polyclinic_name` | VARCHAR | Official name | 'Ang Mo Kio Polyclinic', 'Bedok Polyclinic' | Facility name |
| `cluster` | VARCHAR | Healthcare cluster | 'Central', 'Eastern', 'National' | MOH grouping |
| `region` | VARCHAR | Geographic region | 'North', 'East', 'West' | Location |
| `postal_code` | VARCHAR | Full postal code | '560123' | Address |
| `address` | TEXT | Street address | 'Blk 123 Ang Mo Kio Ave 3' | Full address |
| `operating_hours` | VARCHAR | Business hours | 'Mon-Fri 8am-9pm, Sat 8am-1pm' | Service hours |
| `total_doctors` | INTEGER | Staff count - doctors | 25 | Capacity indicator |
| `total_nurses` | INTEGER | Staff count - nurses | 45 | Capacity indicator |
| `annual_capacity` | INTEGER | Max patient visits/year | 150000 | Throughput metric |
| `establishment_date` | DATE | When polyclinic opened | 1995-06-01 | Facility age |
| `last_renovation_date` | DATE | Most recent renovation | 2020-03-15 | Facility condition |
| `facility_grade` | VARCHAR | Facility tier | 'A', 'B', 'C' | Service level |
| `services_offered` | TEXT | List of services | 'GP, Dental, Pharmacy, Lab' | Service scope |
| `is_active` | BOOLEAN | Currently operational | TRUE, FALSE | Status flag |

---

### **8. CONDITION_MASTER** (Reference Data)
**Purpose**: Master list of medical conditions and disease classifications  
**Primary Key**: `condition_code`  
**Incremental**: No (reference data)

| Column Name | Data Type | Description | Example Values | Business Logic |
|-------------|-----------|-------------|----------------|----------------|
| `condition_code` | VARCHAR | Unique condition identifier | 'COND-001', 'COND-002' | Primary key |
| `condition_name` | VARCHAR | Medical condition name | 'Type 2 Diabetes', 'Hypertension' | Human-readable |
| `condition_category` | VARCHAR | Disease system | 'Metabolic', 'Cardiovascular', 'Respiratory' | Classification |
| `is_chronic` | BOOLEAN | Chronic vs acute | TRUE, FALSE | Care model |
| `is_preventable` | BOOLEAN | Preventable condition | TRUE, FALSE | Public health flag |
| `severity_level` | VARCHAR | Clinical severity | 'Mild', 'Moderate', 'Severe' | Risk stratification |
| `icd_10_codes` | TEXT | Related ICD codes | 'E11, E11.0, E11.9' | Code mapping |
| `healthier_sg_priority` | BOOLEAN | Priority condition | TRUE, FALSE | National program |
| `description` | TEXT | Detailed information | 'Chronic metabolic disorder...' | Clinical definition |

---

## Table Relationships (Entity-Relationship)

```
PATIENT_DEMOGRAPHICS (1) ─────< (M) POLYCLINIC_ATTENDANCES
                                         │
                                         ├─< DIAGNOSIS_RECORDS (M)
                                         │
                                         ├─< PROCEDURE_RECORDS (M)
                                         │
                                         ├─< MEDICATION_PRESCRIPTIONS (M)
                                         │
                                         └─< LABORATORY_RESULTS (M)

POLYCLINIC_MASTER (1) ─────< (M) POLYCLINIC_ATTENDANCES

CONDITION_MASTER (1) ─────< (M) DIAGNOSIS_RECORDS
```

**Relationship Key**:
- `(1) ──< (M)` = One-to-Many relationship
- **Primary joins**: `patient_id`, `attendance_id`, `polyclinic_id`

---

## Data Quality Standards

**Completeness**:
- Critical fields (`patient_id`, `attendance_id`) must have 100% fill rate
- Max 5% null values in non-critical fields

**Validity**:
- Dates must be between 2015-01-01 and today
- Future dates trigger validation errors
- Referential integrity enforced on all foreign keys

**Consistency**:
- Attendance times: `arrival_time` < `consultation_start_time` < `consultation_end_time`
- Costs: `patient_charge` + `subsidy_amount` = `total_cost`

---

## 📖 Glossary of Healthcare Terms

- **Polyclinic**: Singapore's public primary care clinics (outpatient)
- **Healthier SG**: National preventive health program (launched 2023)
- **CHAS**: Community Health Assist Scheme (subsidy program)
- **ICD-10**: International Classification of Diseases, 10th revision
- **Chronic condition**: Long-term disease requiring ongoing management
- **Acute visit**: One-time treatment for short-term illness
- **Walk-in**: No prior appointment, immediate care
- **BD/TDS**: Medical dosing frequency (twice/three times daily)

---
Update date: 2026-01-26*
