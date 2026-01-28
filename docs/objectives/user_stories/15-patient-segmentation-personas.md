# Story 15: Patient Segmentation and Persona Development

## Overview and Statement

Different patient groups have distinct healthcare needs and visit patterns. This story creates patient personas based on demographics, health status, and utilization patterns to enable targeted service design and communication strategies.

**As a** Healthcare Service Designer  
**I want** to segment patients into personas based on their characteristics and visit patterns  
**So that** I can design tailored services and communication strategies for each patient group

### Acceptance Criteria
- [ ] Patient-level feature engineering:
  - Visit frequency (visits per year)
  - Visit consistency (regularity of visits)
  - Primary visit type (acute vs chronic vs preventive)
  - Chronic condition burden (chronic_conditions_count)
  - Demographics (age_group, subsidy_category)
  - Healthcare engagement (healthier_sg_enrolled)
- [ ] Apply clustering algorithms (K-means, Hierarchical) to identify patient segments
- [ ] Determine optimal number of segments (3-6 personas)
- [ ] Generate persona profiles with:
  - Demographic characteristics
  - Health status and needs
  - Visit behavior patterns
  - Engagement level with healthcare system
- [ ] Estimate segment sizes (% of patient population)
- [ ] Recommendations for each persona (e.g., proactive outreach, appointment preferences)

### Technical Notes
- Use scikit-learn for clustering (Python)
- Standardize features before clustering
- Validate segments with clinical stakeholders
- Create persona cards with representative statistics
- Platform: Databricks with Python

### Estimated Effort
12-15 days

### Priority
Low

## Dependencies
- PATIENT_DEMOGRAPHICS for patient characteristics
- POLYCLINIC_ATTENDANCES aggregated at patient level
- DIAGNOSIS_RECORDS for chronic condition identification
