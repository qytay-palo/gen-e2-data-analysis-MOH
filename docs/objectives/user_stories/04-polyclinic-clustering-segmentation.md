# Story 04: Polyclinic Clustering and Segmentation

## Overview and Statement

Different polyclinics serve different populations and exhibit distinct operational characteristics. This story uses unsupervised learning to segment polyclinics into typologies, enabling tailored operational strategies for each cluster.

**As a** Healthcare Policy Analyst  
**I want** to group polyclinics into clusters based on their attendance patterns, patient demographics, and waiting time profiles  
**So that** I can design targeted interventions specific to each polyclinic type

### Acceptance Criteria
- [ ] Feature engineering for polyclinic-level attributes:
  - Average daily volume, peak hour intensity
  - Average waiting time, waiting time variance
  - Patient demographic mix (age distribution, chronic condition prevalence)
  - Visit type distribution (% acute, % chronic, % preventive)
- [ ] Apply clustering algorithms (K-means, Hierarchical, DBSCAN)
- [ ] Determine optimal number of clusters using Silhouette Score and Elbow Method
- [ ] Generate cluster profiles describing each typology (e.g., "High-volume urban", "Senior-focused suburban")
- [ ] Visualize clusters using PCA or t-SNE for dimensionality reduction
- [ ] Map polyclinics to their assigned cluster with interpretation document

### Technical Notes
- Use PySpark MLlib or scikit-learn on Databricks/CDSW
- Standardize features before clustering (StandardScaler)
- Experiment with k=3 to k=8 clusters
- Save cluster assignments to `results/tables/polyclinic_clusters.csv`
- Validate clusters with domain experts

### Estimated Effort
10-13 days

### Priority
Medium

## Dependencies
- [Story 03: Temporal Visitation EDA](#03-temporal-visitation-eda.md) - Understanding patterns helps define clustering features
- POLYCLINIC_ATTENDANCES and PATIENT_DEMOGRAPHICS tables
