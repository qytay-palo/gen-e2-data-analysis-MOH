# Story 16: Chronic Disease Management Impact Analysis

## Overview and Statement

Patients with chronic conditions are high utilizers of polyclinic services. This story analyzes visit patterns and outcomes for chronic patients to assess the effectiveness of chronic disease management programs and identify opportunities for better care coordination.

**As a** Chronic Disease Management Program Director  
**I want** to analyze visit patterns and outcomes for patients with chronic conditions  
**So that** I can evaluate program effectiveness and identify patients who may benefit from enhanced care coordination

### Acceptance Criteria
- [ ] Identify chronic disease patients (using chronic_conditions_count, ICD codes)
- [ ] Analyze chronic patient utilization patterns:
  - Visit frequency compared to recommended follow-up schedules
  - Polyclinic loyalty (% visits to primary polyclinic)
  - Acute exacerbations (unscheduled acute visits)
  - Medication adherence indicators
- [ ] Compare outcomes by chronic disease type (diabetes, hypertension, hyperlipidemia)
- [ ] Assess impact of Healthier SG enrollment on visit patterns
- [ ] Identify "high-risk" chronic patients with:
  - Irregular follow-up attendance
  - Multiple chronic conditions
  - Frequent acute visits
- [ ] Generate patient lists for care management team outreach

### Technical Notes
- Filter on is_chronic=TRUE in DIAGNOSIS_RECORDS
- Join with MEDICATION_PRESCRIPTIONS to assess adherence patterns
- Survival analysis for time-to-next-visit (R or Python)
- Platform: CDSW with R or Databricks with Python
- Export high-risk patient lists to `results/exports/high_risk_chronic_patients.csv`

### Estimated Effort
15-18 days

### Priority
Medium

## Dependencies
- DIAGNOSIS_RECORDS with ICD codes for chronic conditions
- PATIENT_DEMOGRAPHICS with chronic_conditions_count and healthier_sg_enrolled
- MEDICATION_PRESCRIPTIONS for adherence analysis
- Clinical guidelines for recommended follow-up schedules
