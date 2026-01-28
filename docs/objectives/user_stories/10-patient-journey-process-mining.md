# Story 10: Patient Journey Process Mining Analysis

## Overview and Statement

Understanding the end-to-end patient journey reveals bottlenecks in the care delivery process. This story uses process mining techniques to map patient flows and identify stages where delays occur most frequently.

**As a** Healthcare Process Improvement Manager  
**I want** to visualize the complete patient journey from arrival to discharge with time spent at each stage  
**So that** I can identify process bottlenecks and prioritize improvement initiatives

### Acceptance Criteria
- [ ] Transform attendance data into event logs for process mining
- [ ] Events include: arrival, registration, waiting, consultation start, consultation end, treatment, discharge
- [ ] Generate process flow diagrams showing:
  - Most common patient pathways (variants)
  - Average time spent at each stage
  - Percentage of patients following each path
- [ ] Identify bottleneck stages where patients spend longest time
- [ ] Compare process flows across polyclinics (identify best practices)
- [ ] Calculate process efficiency metrics:
  - Value-added time vs non-value-added time
  - Cycle time from arrival to discharge
- [ ] Generate PDF report with process maps and recommendations

### Technical Notes
- Use pm4py (Python) or bupaR (R) for process mining
- Event log structure: case_id (attendance_id), activity, timestamp, resource
- Handle incomplete event logs (missing timestamps)
- Visualize using BPMN or Petri net diagrams
- Platform: CDSW with Python (pm4py) or R (bupaR)

### Estimated Effort
12-15 days

### Priority
Medium

## Dependencies
- POLYCLINIC_ATTENDANCES with all timestamp fields (arrival_time, consultation_start_time, consultation_end_time)
- PROCEDURE_RECORDS and DIAGNOSIS_RECORDS for detailed activity logs
