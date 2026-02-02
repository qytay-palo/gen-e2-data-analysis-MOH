# E05-S02: Calculate Geographic Access Metrics

**Story ID**: E05-S02  
**Epic**: EPIC-005 - Geographic Access & Health Equity Analysis

## Parent Epic
Geographic Access & Health Equity Analysis - Conducting geographic access analysis and equity assessment to identify underserved areas requiring intervention and promote health equity across Singapore.

## Overview and Statement

Calculate travel distance and time from residential areas to nearest healthcare facilities, and develop accessibility scores for all geographic areas.

**As a** health equity analyst  
**I want to** quantify geographic access to healthcare facilities for all areas  
**So that** I can identify areas with poor access requiring intervention

### Acceptance Criteria
- [ ] Calculate distance from each residential area to nearest facility (primary care, hospital, specialist)
- [ ] Estimate travel time using road networks and transport modes where data permits
- [ ] Develop accessibility score (0-100) combining distance, facility density, and capacity
- [ ] Calculate access metrics by facility type (hospital, polyclinic, clinic)
- [ ] Identify areas >5km from nearest facility (healthcare deserts)
- [ ] Create accessibility maps showing spatial variation
- [ ] Generate summary statistics of access by planning area
- [ ] Document methodology and assumptions

### Technical Notes
- Use Euclidean distance as proxy if road network data unavailable
- Consider public transport accessibility in Singapore context
- Weight by facility capacity (larger facilities serve wider catchment)
- Normalize access scores for comparability
- Use spatial analysis tools: GeoPandas, shapely
- Create accessibility index combining multiple dimensions

### Estimated Effort
6 days

### Priority
Critical

## Dependencies
- E05-S01: Requires geographic and population data
