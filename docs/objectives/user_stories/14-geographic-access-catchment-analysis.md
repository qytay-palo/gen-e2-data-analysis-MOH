# Story 14: Geographic Access and Catchment Area Analysis

## Overview and Statement

Understanding where patients come from helps optimize polyclinic locations and capacity planning. This story analyzes patient residential patterns to identify underserved areas and assess catchment area overlap between polyclinics.

**As a** Healthcare Infrastructure Planner  
**I want** to map patient residential locations and analyze geographic accessibility to polyclinics  
**So that** I can identify underserved areas and inform future polyclinic site selection

### Acceptance Criteria
- [ ] Geographic analysis of patient distribution using postal_code and planning_area
- [ ] Calculate catchment area for each polyclinic (where majority of patients reside)
- [ ] Identify overlap zones where multiple polyclinics serve same population
- [ ] Heat map visualization showing:
  - Patient density by planning area
  - Distance-to-nearest-polyclinic distribution
  - Polyclinic utilization by catchment area
- [ ] Identify underserved areas with high population but low polyclinic access
- [ ] Correlation analysis: distance to polyclinic vs visit frequency/no-show rate
- [ ] Report recommending capacity adjustments or new site considerations

### Technical Notes
- Use GeoPandas for spatial analysis (Python)
- Singapore geographic data (planning areas, postal codes)
- Calculate travel distances using road network or Euclidean distance
- Visualize with Folium or Plotly for interactive maps
- Platform: Databricks with Python (geopandas, folium)

### Estimated Effort
13-16 days

### Priority
Medium

## Dependencies
- PATIENT_DEMOGRAPHICS with postal_code and planning_area
- Singapore geographic boundary files (GeoJSON or Shapefile)
- Polyclinic location data (latitude, longitude)
