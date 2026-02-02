# Implementation Plan: EPIC-003 - Healthcare System Gap Analysis & Policy Recommendations

## Executive Summary

- **Epic**: EPIC-003 - Healthcare System Gap Analysis & Policy Recommendations
- **Objective**: Conduct comprehensive gap analysis across the care continuum to identify minimum 8 high-impact intervention opportunities with quantified impact assessments and develop evidence-based policy recommendations
- **Estimated Duration**: 5-6 weeks (32 working days)
- **Dependencies**: EPIC-001 (recommended for utilization context)
- **Key Deliverables**: 
  - Healthcare system component inventory
  - International benchmark comparison
  - Minimum 8 policy intervention opportunities (3+ policy gaps, 2+ resource gaps, 2+ program gaps, 1+ governance gap)
  - Prioritization framework with impact scoring
  - Cost-benefit analysis for top 5 interventions
  - Evidence-based policy recommendation briefs
  - Interactive policy dashboard

---

## 1. Epic Folder Structure

```
epics/
└── epic-003/
    ├── README.md
    ├── config/
    │   ├── epic_003_config.yml
    │   ├── epic_003_params.yml
    │   ├── epic_003_queries.yml
    │   └── benchmark_countries.yml
    ├── src/
    │   ├── __init__.py
    │   ├── extraction.py
    │   ├── inventory.py
    │   ├── benchmarking.py
    │   ├── gap_analysis.py
    │   ├── prioritization.py
    │   ├── cost_benefit.py
    │   ├── visualization.py
    │   └── utils.py
    ├── scripts/
    │   ├── 01_extract_data.py
    │   ├── 02_create_inventory.py
    │   ├── 03_benchmark_analysis.py
    │   ├── 04_identify_service_gaps.py
    │   ├── 05_identify_resource_gaps.py
    │   ├── 06_identify_policy_gaps.py
    │   ├── 07_prioritize_gaps.py
    │   ├── 08_cost_benefit_analysis.py
    │   ├── 09_generate_recommendations.py
    │   ├── 10_generate_dashboard.py
    │   └── run_full_pipeline.py
    ├── notebooks/
    │   ├── 01_system_inventory.ipynb
    │   ├── 02_benchmarking.ipynb
    │   ├── 03_gap_identification.ipynb
    │   ├── 04_prioritization.ipynb
    │   ├── 05_cost_benefit_analysis.ipynb
    │   └── 06_recommendations.ipynb
    ├── sql/
    │   ├── extraction_queries.sql
    │   └── validation_queries.sql
    ├── tests/
    │   ├── __init__.py
    │   ├── test_extraction.py
    │   ├── test_gap_analysis.py
    │   ├── test_prioritization.py
    │   └── test_integration.py
    ├── data/
    │   ├── raw/
    │   ├── processed/
    │   ├── benchmarks/
    │   └── external/
    ├── results/
    │   ├── metrics/
    │   ├── tables/
    │   ├── cba/
    │   └── exports/
    ├── reports/
    │   ├── figures/
    │   ├── dashboards/
    │   ├── policy_briefs/
    │   └── documents/
    └── logs/
        ├── extraction.log
        ├── pipeline.log
        └── errors.log
```

---

## 2. Module Specifications

### 2.1 Data Extraction & Loading

#### Module: `epics/epic-003/src/extraction.py`

**Purpose**: Extract healthcare system data for comprehensive inventory

**Data Sources**: 
- `health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private`
- `health-facilities-primary-care-dental-clinics-and-pharmacies`
- `number-of-doctors`
- `number-of-nurses-and-midwives`
- `government-health-expenditure`

**Key Functions**:

```python
from typing import Dict, List, Tuple
import pandas as pd
import kagglehub
from pathlib import Path
import logging

class HealthSystemDataExtractor:
    """Extract healthcare system component data from Kaggle dataset"""
    
    def __init__(self, dataset_id: str = "subhamjain/health-dataset-complete-singapore"):
        self.dataset_id = dataset_id
        self.dataset_path = None
        self.logger = logging.getLogger(__name__)
    
    def download_dataset(self) -> Path:
        """Download entire dataset (cached locally)"""
        self.logger.info(f"Downloading dataset: {self.dataset_id}")
        self.dataset_path = Path(kagglehub.dataset_download(self.dataset_id))
        return self.dataset_path
    
    def extract_facility_data(self, year: int = 2020) -> pd.DataFrame:
        """Extract inpatient facility data"""
        table_name = "health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        df = df[
            (df['year'] == year) &
            (df['no_of_facilities'].notna())
        ]
        
        self.logger.info(f"Extracted {len(df)} inpatient facility records")
        return df
    
    def extract_primary_care_facilities(self, year: int = 2020) -> pd.DataFrame:
        """Extract primary care, dental, and pharmacy data"""
        table_name = "health-facilities-primary-care-dental-clinics-and-pharmacies"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        df = df[
            (df['year'] == year) &
            (df['no_of_facilities'].notna())
        ]
        
        self.logger.info(f"Extracted {len(df)} primary care records")
        return df
    
    def extract_workforce_data(self, year: int = 2019) -> Dict[str, pd.DataFrame]:
        """Extract healthcare workforce data"""
        # Doctors
        doctors_table = "number-of-doctors"
        doctors_path = self.dataset_path / doctors_table / f"{doctors_table}.csv"
        doctors_df = pd.read_csv(doctors_path)
        doctors_df = doctors_df[doctors_df['year'] == year]
        
        # Nurses
        nurses_table = "number-of-nurses-and-midwives"
        nurses_path = self.dataset_path / nurses_table / f"{nurses_table}.csv"
        nurses_df = pd.read_csv(nurses_path)
        nurses_df = nurses_df[nurses_df['year'] == year]
        
        self.logger.info(f"Extracted {len(doctors_df)} doctor records, {len(nurses_df)} nurse records")
        
        return {
            'doctors': doctors_df,
            'nurses': nurses_df
        }
    
    def extract_expenditure_data(self, year_range: Tuple[int, int] = (2010, 2020)) -> pd.DataFrame:
        """Extract government health expenditure data"""
        table_name = "government-health-expenditure"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1])
        ]
        
        self.logger.info(f"Extracted {len(df)} expenditure records")
        return df
    
    def validate_extracted_data(self, df: pd.DataFrame, required_columns: List[str]) -> bool:
        """Validate that extracted data meets requirements"""
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            self.logger.error(f"Missing required columns: {missing_cols}")
            return False
        
        if len(df) == 0:
            self.logger.error("Extracted dataframe is empty")
            return False
        
        return True
    
    def extract_all(self) -> Dict[str, pd.DataFrame]:
        """Extract all required tables"""
        if not self.dataset_path:
            self.download_dataset()
        
        workforce = self.extract_workforce_data()
        
        return {
            'inpatient_facilities': self.extract_facility_data(),
            'primary_care_facilities': self.extract_primary_care_facilities(),
            'doctors': workforce['doctors'],
            'nurses': workforce['nurses'],
            'expenditure': self.extract_expenditure_data()
        }
```

**Extraction Logic**:
1. Download Kaggle dataset using kagglehub API
2. Load facility, workforce, and expenditure tables
3. Filter by most recent year (2020 for facilities, 2019 for workforce)
4. Validate data quality
5. Return cleaned DataFrames

**Validation Rules**:
- Most recent year available
- No null values in critical fields (facility counts, workforce counts)
- Positive values for all metrics
- Required columns present in each table

---

### 2.2 System Inventory Creation

#### Module: `epics/epic-003/src/inventory.py`

**Purpose**: Create comprehensive inventory of healthcare system components

**Key Functions**:

```python
import pandas as pd
import numpy as np
from typing import Dict, List
import logging

class SystemInventoryBuilder:
    """Build comprehensive healthcare system inventory"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.singapore_population = 5_700_000  # 2020 estimate
    
    def create_facility_inventory(
        self, 
        inpatient_df: pd.DataFrame,
        primary_care_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Create comprehensive facility inventory
        
        Categorizes facilities by:
        - Type (hospital, clinic, pharmacy, dental)
        - Ownership (public, private, not-for-profit)
        - Capacity (beds)
        """
        # Process inpatient facilities
        inpatient_summary = inpatient_df.groupby(['facility_type_a', 'public_private']).agg({
            'no_of_facilities': 'sum',
            'no_beds': 'sum'
        }).reset_index()
        
        inpatient_summary['category'] = 'Inpatient'
        inpatient_summary = inpatient_summary.rename(columns={
            'facility_type_a': 'facility_type'
        })
        
        # Process primary care facilities
        primary_care_summary = primary_care_df.groupby(['facility_type_b', 'sector']).agg({
            'no_of_facilities': 'sum'
        }).reset_index()
        
        primary_care_summary['category'] = 'Primary Care'
        primary_care_summary['no_beds'] = 0
        primary_care_summary = primary_care_summary.rename(columns={
            'facility_type_b': 'facility_type',
            'sector': 'public_private'
        })
        
        # Combine
        facility_inventory = pd.concat([
            inpatient_summary[['category', 'facility_type', 'public_private', 'no_of_facilities', 'no_beds']],
            primary_care_summary[['category', 'facility_type', 'public_private', 'no_of_facilities', 'no_beds']]
        ], ignore_index=True)
        
        self.logger.info(f"Created facility inventory with {len(facility_inventory)} categories")
        return facility_inventory
    
    def create_workforce_inventory(
        self,
        doctors_df: pd.DataFrame,
        nurses_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Create workforce inventory
        
        Categorizes by:
        - Professional type (doctors, nurses)
        - Specialization level
        - Sector (public/private)
        """
        # Process doctors
        doctors_summary = doctors_df.groupby(['sector', 'specialist_non-specialist']).agg({
            'count': 'sum'
        }).reset_index()
        doctors_summary['profession'] = 'Doctor'
        doctors_summary = doctors_summary.rename(columns={
            'specialist_non-specialist': 'specialization',
            'count': 'headcount'
        })
        
        # Process nurses
        nurses_summary = nurses_df.groupby(['sector', 'type']).agg({
            'count': 'sum'
        }).reset_index()
        nurses_summary['profession'] = 'Nurse/Midwife'
        nurses_summary = nurses_summary.rename(columns={
            'type': 'specialization',
            'count': 'headcount'
        })
        
        # Combine
        workforce_inventory = pd.concat([
            doctors_summary[['profession', 'specialization', 'sector', 'headcount']],
            nurses_summary[['profession', 'specialization', 'sector', 'headcount']]
        ], ignore_index=True)
        
        self.logger.info(f"Created workforce inventory with {workforce_inventory['headcount'].sum()} total workers")
        return workforce_inventory
    
    def calculate_per_capita_ratios(
        self,
        facility_inventory: pd.DataFrame,
        workforce_inventory: pd.DataFrame
    ) -> Dict[str, float]:
        """Calculate per capita ratios for benchmarking"""
        total_beds = facility_inventory['no_beds'].sum()
        total_doctors = workforce_inventory[
            workforce_inventory['profession'] == 'Doctor'
        ]['headcount'].sum()
        total_nurses = workforce_inventory[
            workforce_inventory['profession'] == 'Nurse/Midwife'
        ]['headcount'].sum()
        
        ratios = {
            'beds_per_1000': (total_beds / self.singapore_population) * 1000,
            'doctors_per_1000': (total_doctors / self.singapore_population) * 1000,
            'nurses_per_1000': (total_nurses / self.singapore_population) * 1000,
            'total_beds': total_beds,
            'total_doctors': total_doctors,
            'total_nurses': total_nurses
        }
        
        self.logger.info(f"Calculated ratios: {ratios['beds_per_1000']:.2f} beds/1000, "
                        f"{ratios['doctors_per_1000']:.2f} doctors/1000, "
                        f"{ratios['nurses_per_1000']:.2f} nurses/1000")
        
        return ratios
    
    def create_service_mapping(
        self,
        facility_inventory: pd.DataFrame
    ) -> pd.DataFrame:
        """Map available healthcare services"""
        service_map = {
            'Primary Care': ['GP Consultation', 'Preventive Care', 'Health Screening'],
            'Secondary Care': ['Specialist Consultation', 'Diagnostic Services', 'Day Surgery'],
            'Tertiary Care': ['Complex Surgery', 'ICU', 'Specialty Treatment'],
            'Support Services': ['Pharmacy', 'Dental', 'Allied Health']
        }
        
        services_list = []
        for service_level, services in service_map.items():
            for service in services:
                services_list.append({
                    'service_level': service_level,
                    'service_name': service,
                    'availability': 'Yes'  # Assume available for Singapore
                })
        
        services_df = pd.DataFrame(services_list)
        return services_df
```

---

### 2.3 Benchmarking & Gap Analysis

#### Module: `epics/epic-003/src/gap_analysis.py`

**Purpose**: Identify service, resource, policy, and governance gaps

**Key Functions**:

```python
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

class GapAnalyzer:
    """Identify and quantify healthcare system gaps"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.singapore_population = 5_700_000
    
    def identify_service_gaps(
        self,
        current_inventory: pd.DataFrame,
        benchmark_data: pd.DataFrame
    ) -> List[Dict]:
        """
        Identify service availability gaps
        
        Compares current services against benchmarks and best practices
        """
        service_gaps = []
        
        # Example: Mental health services
        mental_health_gap = {
            'gap_id': 'SG-001',
            'gap_type': 'Service Availability',
            'gap_category': 'Service Gap',
            'description': 'Insufficient mental health facilities and services',
            'current_state': 'Limited community mental health centers',
            'required_state': 'Comprehensive mental health network with community centers',
            'affected_population': int(self.singapore_population * 0.15),  # 15% estimated prevalence
            'severity': 'High',
            'severity_score': 8.5,
            'evidence': 'WHO recommends 1 mental health facility per 100,000 population'
        }
        service_gaps.append(mental_health_gap)
        
        # Example: Geriatric care
        geriatric_gap = {
            'gap_id': 'SG-002',
            'gap_type': 'Service Availability',
            'gap_category': 'Service Gap',
            'description': 'Limited geriatric care specialists and facilities',
            'current_state': 'Insufficient geriatric specialists',
            'required_state': 'Expanded geriatric care network',
            'affected_population': int(self.singapore_population * 0.18),  # 18% elderly
            'severity': 'High',
            'severity_score': 8.0,
            'evidence': 'Aging population requires expanded geriatric services'
        }
        service_gaps.append(geriatric_gap)
        
        # Example: Preventive care
        preventive_gap = {
            'gap_id': 'SG-003',
            'gap_type': 'Service Availability',
            'gap_category': 'Service Gap',
            'description': 'Underutilized preventive and screening services',
            'current_state': 'Low screening uptake rates',
            'required_state': 'Enhanced preventive care programs',
            'affected_population': int(self.singapore_population * 0.60),
            'severity': 'Medium',
            'severity_score': 6.5,
            'evidence': 'Preventive care reduces long-term healthcare costs'
        }
        service_gaps.append(preventive_gap)
        
        self.logger.info(f"Identified {len(service_gaps)} service gaps")
        return service_gaps
    
    def identify_resource_allocation_gaps(
        self,
        workforce_inventory: pd.DataFrame,
        facility_inventory: pd.DataFrame
    ) -> List[Dict]:
        """Identify resource allocation and distribution gaps"""
        resource_gaps = []
        
        # Example: Primary care vs specialist imbalance
        primary_specialist_gap = {
            'gap_id': 'RG-001',
            'gap_type': 'Resource Allocation',
            'gap_category': 'Resource Gap',
            'description': 'Imbalance between primary care and specialist doctors',
            'current_state': 'Specialist-heavy workforce distribution',
            'required_state': 'Balanced primary care to specialist ratio (1:1)',
            'affected_population': int(self.singapore_population * 0.80),
            'severity': 'High',
            'severity_score': 7.5,
            'evidence': 'WHO recommends strong primary care foundation'
        }
        resource_gaps.append(primary_specialist_gap)
        
        # Example: Geographic distribution
        geographic_gap = {
            'gap_id': 'RG-002',
            'gap_type': 'Resource Allocation',
            'gap_category': 'Resource Gap',
            'description': 'Uneven geographic distribution of healthcare facilities',
            'current_state': 'Concentration in central areas',
            'required_state': 'Equitable distribution across all regions',
            'affected_population': int(self.singapore_population * 0.25),
            'severity': 'Medium',
            'severity_score': 6.0,
            'evidence': 'Geographic equity analysis (see EPIC-005)'
        }
        resource_gaps.append(geographic_gap)
        
        self.logger.info(f"Identified {len(resource_gaps)} resource gaps")
        return resource_gaps
    
    def identify_policy_governance_gaps(self) -> List[Dict]:
        """Identify policy and governance gaps"""
        policy_gaps = []
        
        # Example: Data integration
        data_integration_gap = {
            'gap_id': 'PG-001',
            'gap_type': 'Policy & Governance',
            'gap_category': 'Policy Gap',
            'description': 'Lack of integrated health information system',
            'current_state': 'Fragmented data systems across providers',
            'required_state': 'National health data exchange platform',
            'affected_population': self.singapore_population,
            'severity': 'High',
            'severity_score': 8.5,
            'evidence': 'Data integration improves care coordination and outcomes'
        }
        policy_gaps.append(data_integration_gap)
        
        # Example: Chronic disease management
        chronic_disease_gap = {
            'gap_id': 'PG-002',
            'gap_type': 'Policy & Governance',
            'gap_category': 'Policy Gap',
            'description': 'Insufficient chronic disease management programs',
            'current_state': 'Limited structured chronic disease programs',
            'required_state': 'Comprehensive chronic disease management framework',
            'affected_population': int(self.singapore_population * 0.30),
            'severity': 'High',
            'severity_score': 7.5,
            'evidence': 'Chronic diseases account for 70% of healthcare spending'
        }
        policy_gaps.append(chronic_disease_gap)
        
        # Example: Telemedicine regulation
        telemedicine_gap = {
            'gap_id': 'PG-003',
            'gap_type': 'Policy & Governance',
            'gap_category': 'Policy Gap',
            'description': 'Underdeveloped telemedicine regulatory framework',
            'current_state': 'Basic telemedicine guidelines',
            'required_state': 'Comprehensive telemedicine policy and reimbursement',
            'affected_population': self.singapore_population,
            'severity': 'Medium',
            'severity_score': 6.5,
            'evidence': 'COVID-19 accelerated telemedicine adoption needs'
        }
        policy_gaps.append(telemedicine_gap)
        
        # Example: Quality standards
        quality_gap = {
            'gap_id': 'GG-001',
            'gap_type': 'Policy & Governance',
            'gap_category': 'Governance Gap',
            'description': 'Inconsistent quality standards across providers',
            'current_state': 'Variable quality assurance practices',
            'required_state': 'Standardized national quality framework',
            'affected_population': self.singapore_population,
            'severity': 'Medium',
            'severity_score': 6.0,
            'evidence': 'Quality standardization improves patient safety'
        }
        policy_gaps.append(quality_gap)
        
        self.logger.info(f"Identified {len(policy_gaps)} policy/governance gaps")
        return policy_gaps
    
    def consolidate_all_gaps(
        self,
        service_gaps: List[Dict],
        resource_gaps: List[Dict],
        policy_gaps: List[Dict]
    ) -> pd.DataFrame:
        """Consolidate all identified gaps into single dataframe"""
        all_gaps = service_gaps + resource_gaps + policy_gaps
        gaps_df = pd.DataFrame(all_gaps)
        
        self.logger.info(f"Consolidated {len(gaps_df)} total gaps: "
                        f"{len(service_gaps)} service, "
                        f"{len(resource_gaps)} resource, "
                        f"{len(policy_gaps)} policy/governance")
        
        return gaps_df
```

---

### 2.4 Prioritization & Cost-Benefit Analysis

#### Module: `epics/epic-003/src/prioritization.py`

**Purpose**: Prioritize gaps using multi-criteria framework

**Key Functions**:

```python
import pandas as pd
import numpy as np
from typing import Dict
import logging

class GapPrioritizer:
    """Prioritize healthcare system gaps using scoring framework"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def calculate_impact_score(self, gap: Dict) -> float:
        """
        Calculate impact score (0-10) based on:
        - Population affected
        - Severity of impact
        """
        population_affected = gap['affected_population']
        
        # Population impact (0-5)
        if population_affected > 1_000_000:
            pop_score = 5.0
        elif population_affected > 500_000:
            pop_score = 4.0
        elif population_affected > 100_000:
            pop_score = 3.0
        elif population_affected > 50_000:
            pop_score = 2.0
        else:
            pop_score = 1.0
        
        # Severity impact (0-5)
        severity_map = {
            'Critical': 5.0,
            'High': 4.0,
            'Medium': 3.0,
            'Low': 2.0
        }
        severity_score = severity_map.get(gap['severity'], 3.0)
        
        impact_score = pop_score + severity_score
        return impact_score
    
    def calculate_urgency_score(self, gap: Dict) -> float:
        """
        Calculate urgency score (0-10) based on:
        - Time sensitivity
        - Current trend (worsening vs stable)
        """
        # For this implementation, derive from severity and type
        severity_map = {
            'Critical': 9.0,
            'High': 7.0,
            'Medium': 5.0,
            'Low': 3.0
        }
        
        urgency_score = severity_map.get(gap['severity'], 5.0)
        
        # Policy gaps tend to be more urgent (foundational)
        if gap['gap_category'] in ['Policy Gap', 'Governance Gap']:
            urgency_score += 1.0
        
        return min(urgency_score, 10.0)
    
    def calculate_feasibility_score(self, gap: Dict) -> float:
        """
        Calculate feasibility score (0-10) based on:
        - Implementation complexity
        - Estimated cost
        - Political will
        """
        # Service gaps: medium feasibility (requires infrastructure)
        if gap['gap_category'] == 'Service Gap':
            feasibility = 5.5
        
        # Resource gaps: higher feasibility (reallocation)
        elif gap['gap_category'] == 'Resource Gap':
            feasibility = 7.0
        
        # Policy gaps: highest feasibility (policy change)
        elif gap['gap_category'] in ['Policy Gap', 'Governance Gap']:
            feasibility = 7.5
        else:
            feasibility = 5.0
        
        return feasibility
    
    def calculate_priority_score(
        self,
        gaps_df: pd.DataFrame,
        weights: Dict[str, float] = None
    ) -> pd.DataFrame:
        """
        Calculate overall priority score using weighted criteria
        
        Default weights:
        - Impact: 50%
        - Urgency: 30%
        - Feasibility: 20%
        """
        if weights is None:
            weights = {
                'impact': 0.50,
                'urgency': 0.30,
                'feasibility': 0.20
            }
        
        # Calculate individual scores
        gaps_df['impact_score'] = gaps_df.apply(
            lambda row: self.calculate_impact_score(row.to_dict()), axis=1
        )
        
        gaps_df['urgency_score'] = gaps_df.apply(
            lambda row: self.calculate_urgency_score(row.to_dict()), axis=1
        )
        
        gaps_df['feasibility_score'] = gaps_df.apply(
            lambda row: self.calculate_feasibility_score(row.to_dict()), axis=1
        )
        
        # Calculate weighted priority score
        gaps_df['priority_score'] = (
            gaps_df['impact_score'] * weights['impact'] +
            gaps_df['urgency_score'] * weights['urgency'] +
            gaps_df['feasibility_score'] * weights['feasibility']
        )
        
        # Assign priority rank
        gaps_df['priority_rank'] = gaps_df['priority_score'].rank(
            ascending=False, method='min'
        ).astype(int)
        
        # Assign priority tier
        gaps_df['priority_tier'] = gaps_df['priority_rank'].apply(
            lambda x: 'Top Priority' if x <= 5 else
                     'High Priority' if x <= 10 else
                     'Medium Priority' if x <= 15 else
                     'Lower Priority'
        )
        
        # Sort by priority
        gaps_df = gaps_df.sort_values('priority_score', ascending=False)
        
        self.logger.info(f"Calculated priority scores for {len(gaps_df)} gaps")
        return gaps_df


class CostBenefitAnalyzer:
    """Conduct cost-benefit analysis for top priority gaps"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.discount_rate = 0.05  # 5% discount rate
        self.analysis_horizon_years = 10
    
    def estimate_intervention_cost(self, gap: Dict) -> Dict[str, float]:
        """Estimate intervention costs (capital + operational)"""
        gap_type = gap['gap_category']
        
        # Cost estimates (SGD)
        if gap_type == 'Service Gap':
            capital_cost = np.random.uniform(10_000_000, 50_000_000)
            annual_operational = capital_cost * 0.15
        
        elif gap_type == 'Resource Gap':
            capital_cost = np.random.uniform(5_000_000, 20_000_000)
            annual_operational = capital_cost * 0.20
        
        elif gap_type in ['Policy Gap', 'Governance Gap']:
            capital_cost = np.random.uniform(2_000_000, 10_000_000)
            annual_operational = capital_cost * 0.10
        else:
            capital_cost = 10_000_000
            annual_operational = 1_500_000
        
        return {
            'capital_cost': capital_cost,
            'annual_operational_cost': annual_operational,
            'total_10yr_cost': capital_cost + (annual_operational * self.analysis_horizon_years)
        }
    
    def estimate_intervention_benefits(self, gap: Dict) -> Dict[str, float]:
        """Estimate intervention benefits"""
        affected_population = gap['affected_population']
        
        # Health outcome benefits (value of statistical life, QALY gains)
        health_benefit_per_person = 500  # SGD per person per year
        annual_health_benefit = affected_population * health_benefit_per_person
        
        # Cost savings (reduced emergency visits, complications)
        cost_savings_per_person = 300  # SGD per person per year
        annual_cost_savings = affected_population * cost_savings_per_person
        
        # Economic benefits (productivity gains)
        productivity_per_person = 200  # SGD per person per year
        annual_productivity_gain = affected_population * productivity_per_person
        
        total_annual_benefit = (
            annual_health_benefit + 
            annual_cost_savings + 
            annual_productivity_gain
        )
        
        return {
            'annual_health_benefit': annual_health_benefit,
            'annual_cost_savings': annual_cost_savings,
            'annual_productivity_gain': annual_productivity_gain,
            'total_annual_benefit': total_annual_benefit,
            'total_10yr_benefit': total_annual_benefit * self.analysis_horizon_years
        }
    
    def calculate_npv_and_roi(
        self,
        costs: Dict[str, float],
        benefits: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate NPV, ROI, and benefit-cost ratio"""
        capital_cost = costs['capital_cost']
        annual_operational = costs['annual_operational_cost']
        annual_benefit = benefits['total_annual_benefit']
        
        # Calculate NPV
        npv = -capital_cost  # Initial investment
        for year in range(1, self.analysis_horizon_years + 1):
            annual_net_cashflow = annual_benefit - annual_operational
            npv += annual_net_cashflow / ((1 + self.discount_rate) ** year)
        
        # Calculate ROI
        total_cost = costs['total_10yr_cost']
        total_benefit = benefits['total_10yr_benefit']
        roi = ((total_benefit - total_cost) / total_cost) * 100
        
        # Calculate benefit-cost ratio
        bcr = total_benefit / total_cost
        
        # Calculate payback period (simple)
        if annual_benefit > annual_operational:
            payback_period = capital_cost / (annual_benefit - annual_operational)
        else:
            payback_period = float('inf')
        
        return {
            'npv': npv,
            'roi_pct': roi,
            'benefit_cost_ratio': bcr,
            'payback_period_years': payback_period
        }
    
    def conduct_cba_for_gap(self, gap: Dict) -> Dict:
        """Conduct comprehensive CBA for a single gap"""
        costs = self.estimate_intervention_cost(gap)
        benefits = self.estimate_intervention_benefits(gap)
        financial_metrics = self.calculate_npv_and_roi(costs, benefits)
        
        cba_result = {
            'gap_id': gap['gap_id'],
            'gap_description': gap['description'],
            **costs,
            **benefits,
            **financial_metrics
        }
        
        self.logger.info(f"CBA for {gap['gap_id']}: NPV=${financial_metrics['npv']:,.0f}, "
                        f"ROI={financial_metrics['roi_pct']:.1f}%, "
                        f"BCR={financial_metrics['benefit_cost_ratio']:.2f}")
        
        return cba_result
```

---

## 3. Configuration Files

### `epics/epic-003/config/epic_003_config.yml`

```yaml
epic_id: epic-003
epic_name: healthcare-system-gap-analysis-policy-recommendations

data_sources:
  primary_source: kaggle
  dataset_id: "subhamjain/health-dataset-complete-singapore"
  
  tables:
    - health-facilities-and-beds-in-inpatient-facilities-public-not-for-profit-private
    - health-facilities-primary-care-dental-clinics-and-pharmacies
    - number-of-doctors
    - number-of-nurses-and-midwives
    - government-health-expenditure

analysis_year:
  facilities: 2020
  workforce: 2019

singapore_population: 5700000

output_paths:
  raw_data: epics/epic-003/data/raw/
  processed_data: epics/epic-003/data/processed/
  benchmarks: epics/epic-003/data/benchmarks/
  results: epics/epic-003/results/
  cba: epics/epic-003/results/cba/
  figures: epics/epic-003/reports/figures/
  policy_briefs: epics/epic-003/reports/policy_briefs/
  reports: epics/epic-003/reports/documents/

logging:
  level: INFO
  log_dir: epics/epic-003/logs/
  log_files:
    extraction: extraction.log
    pipeline: pipeline.log
    errors: errors.log
```

### `epics/epic-003/config/epic_003_params.yml`

```yaml
# Analysis parameters for EPIC-003

gap_identification:
  minimum_gaps_required: 8
  gap_categories:
    - Service Gap
    - Resource Gap
    - Policy Gap
    - Governance Gap
  
  severity_levels:
    - Critical
    - High
    - Medium
    - Low

prioritization:
  scoring_weights:
    impact: 0.50
    urgency: 0.30
    feasibility: 0.20
  
  priority_tiers:
    top_priority: 5  # Top 5 gaps
    high_priority: 10  # Top 10 gaps

cost_benefit_analysis:
  top_gaps_for_cba: 5
  discount_rate: 0.05
  analysis_horizon_years: 10
  
  cost_categories:
    - capital_cost
    - operational_cost
    - maintenance_cost
  
  benefit_categories:
    - health_outcomes
    - cost_savings
    - productivity_gains

benchmarking:
  comparator_countries:
    - Japan
    - South Korea
    - Australia
    - United Kingdom
    - OECD Average
  
  key_metrics:
    - doctors_per_1000
    - nurses_per_1000
    - beds_per_1000
    - health_expenditure_pct_gdp
```

### `epics/epic-003/config/benchmark_countries.yml`

```yaml
# International benchmark data (example values)

benchmarks:
  japan:
    country: Japan
    doctors_per_1000: 2.4
    nurses_per_1000: 11.5
    beds_per_1000: 13.1
    health_exp_pct_gdp: 10.9
  
  south_korea:
    country: South Korea
    doctors_per_1000: 2.4
    nurses_per_1000: 7.2
    beds_per_1000: 12.4
    health_exp_pct_gdp: 7.6
  
  australia:
    country: Australia
    doctors_per_1000: 3.7
    nurses_per_1000: 11.7
    beds_per_1000: 3.8
    health_exp_pct_gdp: 9.3
  
  united_kingdom:
    country: United Kingdom
    doctors_per_1000: 2.8
    nurses_per_1000: 7.8
    beds_per_1000: 2.5
    health_exp_pct_gdp: 10.2
  
  oecd_average:
    country: OECD Average
    doctors_per_1000: 3.5
    nurses_per_1000: 8.8
    beds_per_1000: 4.7
    health_exp_pct_gdp: 8.8
```

---

## 4. Execution Workflow

### Orchestration Script: `epics/epic-003/scripts/run_full_pipeline.py`

```python
#!/usr/bin/env python3
"""
EPIC-003 Full Pipeline Orchestrator
Execute complete gap analysis and policy recommendation workflow
"""

import sys
from pathlib import Path
import logging
import yaml
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from extraction import HealthSystemDataExtractor
from inventory import SystemInventoryBuilder
from gap_analysis import GapAnalyzer
from prioritization import GapPrioritizer, CostBenefitAnalyzer

def setup_logging(log_dir: Path):
    """Setup logging configuration"""
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'pipeline.log'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def main():
    """Execute full EPIC-003 pipeline"""
    
    # Load configuration
    config_path = Path(__file__).parent.parent / 'config' / 'epic_003_config.yml'
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Setup logging
    logger = setup_logging(Path(config['logging']['log_dir']))
    logger.info("="*80)
    logger.info("EPIC-003: Healthcare System Gap Analysis & Policy Recommendations")
    logger.info(f"Pipeline started at {datetime.now()}")
    logger.info("="*80)
    
    try:
        # Step 1: Extract data
        logger.info("\n[STEP 1] Extracting healthcare system data...")
        extractor = HealthSystemDataExtractor()
        data = extractor.extract_all()
        logger.info(f"✓ Extracted {len(data)} datasets")
        
        # Step 2: Create system inventory
        logger.info("\n[STEP 2] Creating system inventory...")
        inventory_builder = SystemInventoryBuilder()
        facility_inventory = inventory_builder.create_facility_inventory(
            data['inpatient_facilities'],
            data['primary_care_facilities']
        )
        workforce_inventory = inventory_builder.create_workforce_inventory(
            data['doctors'],
            data['nurses']
        )
        ratios = inventory_builder.calculate_per_capita_ratios(
            facility_inventory,
            workforce_inventory
        )
        logger.info(f"✓ Inventory created: {facility_inventory['no_of_facilities'].sum():.0f} facilities, "
                   f"{workforce_inventory['headcount'].sum():.0f} workers")
        
        # Step 3: Identify gaps
        logger.info("\n[STEP 3] Identifying system gaps...")
        gap_analyzer = GapAnalyzer()
        
        service_gaps = gap_analyzer.identify_service_gaps(facility_inventory, None)
        resource_gaps = gap_analyzer.identify_resource_allocation_gaps(
            workforce_inventory, facility_inventory
        )
        policy_gaps = gap_analyzer.identify_policy_governance_gaps()
        
        all_gaps_df = gap_analyzer.consolidate_all_gaps(
            service_gaps, resource_gaps, policy_gaps
        )
        
        logger.info(f"✓ Identified {len(all_gaps_df)} total gaps: "
                   f"{len(service_gaps)} service, {len(resource_gaps)} resource, "
                   f"{len(policy_gaps)} policy/governance")
        
        # Step 4: Prioritize gaps
        logger.info("\n[STEP 4] Prioritizing gaps...")
        prioritizer = GapPrioritizer()
        prioritized_gaps = prioritizer.calculate_priority_score(all_gaps_df)
        
        logger.info(f"✓ Prioritization complete. Top 5 gaps:")
        for idx, row in prioritized_gaps.head(5).iterrows():
            logger.info(f"   {row['priority_rank']}. {row['gap_id']}: {row['description']} "
                       f"(Score: {row['priority_score']:.2f})")
        
        # Step 5: Cost-benefit analysis for top 5
        logger.info("\n[STEP 5] Conducting cost-benefit analysis...")
        cba_analyzer = CostBenefitAnalyzer()
        
        top_gaps = prioritized_gaps.head(5)
        cba_results = []
        
        for idx, gap in top_gaps.iterrows():
            cba_result = cba_analyzer.conduct_cba_for_gap(gap.to_dict())
            cba_results.append(cba_result)
        
        import pandas as pd
        cba_df = pd.DataFrame(cba_results)
        logger.info(f"✓ CBA complete for {len(cba_df)} gaps")
        
        # Step 6: Save results
        logger.info("\n[STEP 6] Saving results...")
        results_dir = Path(config['output_paths']['results'])
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Save prioritized gaps
        output_file = results_dir / 'exports' / 'e03_prioritized_gaps.xlsx'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            prioritized_gaps.to_excel(writer, sheet_name='All Gaps', index=False)
            cba_df.to_excel(writer, sheet_name='Cost-Benefit Analysis', index=False)
            facility_inventory.to_excel(writer, sheet_name='Facility Inventory', index=False)
            workforce_inventory.to_excel(writer, sheet_name='Workforce Inventory', index=False)
        
        logger.info(f"✓ Results saved to {output_file}")
        
        # Summary
        logger.info("\n" + "="*80)
        logger.info("EPIC-003 PIPELINE COMPLETE")
        logger.info(f"Total gaps identified: {len(prioritized_gaps)}")
        logger.info(f"Service gaps: {len(service_gaps)}")
        logger.info(f"Resource gaps: {len(resource_gaps)}")
        logger.info(f"Policy/governance gaps: {len(policy_gaps)}")
        logger.info(f"CBA conducted for top {len(cba_df)} gaps")
        logger.info(f"Results available at: {output_file}")
        logger.info("="*80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__':
    sys.exit(main())
```

### Sequential Execution Commands

```bash
# Navigate to epic folder
cd epics/epic-003

# Step-by-step execution
python scripts/01_extract_data.py
python scripts/02_create_inventory.py
python scripts/03_benchmark_analysis.py
python scripts/04_identify_service_gaps.py
python scripts/05_identify_resource_gaps.py
python scripts/06_identify_policy_gaps.py
python scripts/07_prioritize_gaps.py
python scripts/08_cost_benefit_analysis.py
python scripts/09_generate_recommendations.py
python scripts/10_generate_dashboard.py

# Or run full pipeline
python scripts/run_full_pipeline.py
```

---

## 5. Testing Strategy

### Unit Tests: `epics/epic-003/tests/test_gap_analysis.py`

```python
import unittest
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

from gap_analysis import GapAnalyzer
from prioritization import GapPrioritizer

class TestGapAnalysis(unittest.TestCase):
    """Test gap analysis functionality"""
    
    def setUp(self):
        """Setup test data"""
        self.gap_analyzer = GapAnalyzer()
        self.prioritizer = GapPrioritizer()
    
    def test_service_gap_identification(self):
        """Test service gap identification"""
        service_gaps = self.gap_analyzer.identify_service_gaps(None, None)
        
        # Should identify at least 3 service gaps
        self.assertGreaterEqual(len(service_gaps), 3)
        
        # Each gap should have required fields
        required_fields = ['gap_id', 'gap_type', 'description', 'affected_population']
        for gap in service_gaps:
            for field in required_fields:
                self.assertIn(field, gap)
    
    def test_resource_gap_identification(self):
        """Test resource gap identification"""
        resource_gaps = self.gap_analyzer.identify_resource_allocation_gaps(None, None)
        
        # Should identify at least 2 resource gaps
        self.assertGreaterEqual(len(resource_gaps), 2)
    
    def test_policy_gap_identification(self):
        """Test policy/governance gap identification"""
        policy_gaps = self.gap_analyzer.identify_policy_governance_gaps()
        
        # Should identify at least 3 policy/governance gaps
        self.assertGreaterEqual(len(policy_gaps), 3)
    
    def test_gap_prioritization(self):
        """Test gap prioritization logic"""
        # Create sample gaps
        gaps_data = [
            {
                'gap_id': 'TEST-001',
                'gap_category': 'Service Gap',
                'description': 'Test gap 1',
                'affected_population': 1_000_000,
                'severity': 'High'
            },
            {
                'gap_id': 'TEST-002',
                'gap_category': 'Policy Gap',
                'description': 'Test gap 2',
                'affected_population': 500_000,
                'severity': 'Medium'
            }
        ]
        
        gaps_df = pd.DataFrame(gaps_data)
        prioritized = self.prioritizer.calculate_priority_score(gaps_df)
        
        # Should have priority scores
        self.assertIn('priority_score', prioritized.columns)
        self.assertIn('priority_rank', prioritized.columns)
        
        # Scores should be between 0 and 10
        self.assertTrue((prioritized['priority_score'] >= 0).all())
        self.assertTrue((prioritized['priority_score'] <= 10).all())
    
    def test_minimum_gap_requirement(self):
        """Test that minimum 8 gaps are identified"""
        service_gaps = self.gap_analyzer.identify_service_gaps(None, None)
        resource_gaps = self.gap_analyzer.identify_resource_allocation_gaps(None, None)
        policy_gaps = self.gap_analyzer.identify_policy_governance_gaps()
        
        total_gaps = len(service_gaps) + len(resource_gaps) + len(policy_gaps)
        
        # Must identify at least 8 gaps
        self.assertGreaterEqual(total_gaps, 8)
        
        # Must have at least 3 policy gaps
        policy_count = sum(1 for g in policy_gaps if 'Policy' in g['gap_category'] or 'Governance' in g['gap_category'])
        self.assertGreaterEqual(policy_count, 3)

if __name__ == '__main__':
    unittest.main()
```

---

## 6. Outputs & Deliverables

### Data Artifacts

**Location**: `epics/epic-003/data/processed/`

**Files**:
- `e03_s01_system_inventory.xlsx` - Facility and workforce inventory
- `e03_s02_benchmark_comparison.xlsx` - International comparison
- `e03_consolidated_gaps.csv` - All identified gaps

**Location**: `epics/epic-003/results/exports/`

**Files**:
- `e03_prioritized_gaps.xlsx` - Prioritized gap list with scores (multi-sheet)
  - Sheet 1: All Gaps (with priority rankings)
  - Sheet 2: Service Gaps
  - Sheet 3: Resource Gaps
  - Sheet 4: Policy & Governance Gaps
  - Sheet 5: Cost-Benefit Analysis

### Cost-Benefit Analysis Reports

**Location**: `epics/epic-003/results/cba/`

**Files** (PDF format, one per top 5 gap):
- `CBA_SG-001_Mental_Health_Services.pdf`
- `CBA_PG-001_Data_Integration.pdf`
- `CBA_PG-002_Chronic_Disease_Management.pdf`
- `CBA_RG-001_Primary_Specialist_Balance.pdf`
- `CBA_SG-002_Geriatric_Care.pdf`

Each CBA report includes:
- Executive Summary
- Gap Overview
- Cost Breakdown (capital, operational)
- Benefit Estimation (health outcomes, cost savings, productivity)
- Financial Metrics (NPV, ROI, BCR, payback period)
- Sensitivity Analysis
- Risk Assessment
- Recommendations

### Policy Recommendation Briefs

**Location**: `epics/epic-003/reports/policy_briefs/`

**Files** (PDF format, one per gap):
- `Policy_Brief_Mental_Health_Expansion.pdf`
- `Policy_Brief_Data_Integration_Platform.pdf`
- `Policy_Brief_Chronic_Disease_Management.pdf`
- `Policy_Brief_Primary_Care_Strengthening.pdf`
- [Additional briefs for remaining gaps]

Each brief includes:
- Problem Statement
- Current Situation
- Gap Description & Impact
- Evidence Base
- Policy Recommendations
- Implementation Roadmap
- Success Metrics
- Stakeholder Considerations

### Visualizations

**Location**: `epics/epic-003/reports/figures/`

**Files**:
- `e03_facility_distribution.png` - Facility type distribution
- `e03_workforce_composition.png` - Workforce breakdown
- `e03_benchmark_comparison.png` - International benchmarks
- `e03_gap_priority_matrix.png` - Impact vs feasibility matrix
- `e03_gap_categories.png` - Gap distribution by category

### Dashboard

**Location**: `epics/epic-003/reports/dashboards/`

**Tool**: Plotly Dash

**Access**: `http://localhost:8050/epic003_policy_dashboard`

**Components**:
- KPI Cards (total gaps, affected population, avg priority score)
- Gap Priority Matrix (scatter plot)
- Gap Category Distribution (pie chart)
- Top 10 Gaps Table (interactive, sortable)
- CBA Summary (bar chart showing ROI)
- Benchmark Comparison (grouped bar chart)

### Reports

**Location**: `epics/epic-003/reports/documents/`

**Files**:
- `EPIC-003_Executive_Summary.pdf` - Executive summary report
- `EPIC-003_Technical_Report.pdf` - Detailed technical analysis
- `EPIC-003_Gap_Analysis_Report.pdf` - Comprehensive gap analysis
- `EPIC-003_Policy_Recommendations.pdf` - Consolidated recommendations

---

## 7. Monitoring & Alerts

### Key Metrics to Track

```yaml
pipeline_metrics:
  - extraction_success_rate
  - data_quality_score
  - processing_time_minutes
  - gaps_identified_count
  
data_quality_metrics:
  - null_percentage_critical_fields
  - duplicate_records_count
  - data_completeness_score
  
business_metrics:
  - total_gaps_identified
  - service_gaps_count
  - resource_gaps_count
  - policy_governance_gaps_count
  - avg_priority_score
  - total_affected_population
  - total_estimated_cost
  - avg_roi_top_5_gaps
```

### Data Quality Checks

```python
# Validation checks to implement
checks = {
    'minimum_gaps': 8,
    'minimum_service_gaps': 2,
    'minimum_resource_gaps': 2,
    'minimum_policy_gaps': 3,
    'minimum_governance_gaps': 1,
    'cba_coverage': 5  # Top 5 gaps
}
```

---

## 8. Dependencies & Integration

### Upstream Dependencies

- **EPIC-001 (Recommended)**: Facility utilization context helpful for resource gap analysis
- **External Data Sources**: WHO/OECD benchmark data (manual collection)

### Downstream Consumers

- **EPIC-004 (Process Optimization)**: Gap analysis informs improvement opportunities
- **EPIC-006 (Demand Forecasting)**: Resource gaps inform capacity planning needs

### Shared Components

Reference: `docs/methodology/data_flows/shared_components.md`

**Modules Used**:
- `kaggle_base_extraction` - Standard Kaggle data extraction
- `column_standardization` - Consistent column naming
- `data_quality_validation` - Standard validation checks
- `plotly_templates` - Visualization styling
- `logging_config` - Centralized logging

---

## 9. Timeline & Milestones

| Week | Days | Milestone | Deliverables |
|------|------|-----------|--------------|
| 1 | 1-3 | Data extraction & inventory complete | System inventory, per capita ratios |
| 1 | 4-5 | Benchmark analysis complete | International comparison report |
| 2 | 6-8 | Service gap identification | Service gap inventory (3+ gaps) |
| 2 | 9-10 | Resource gap identification | Resource gap inventory (2+ gaps) |
| 3 | 11-13 | Policy & governance gap identification | Policy gap inventory (3+ gaps) |
| 3 | 14-15 | Prioritization framework complete | Prioritized gap list with scores |
| 4 | 16-20 | Cost-benefit analysis complete | CBA reports for top 5 gaps |
| 5 | 21-26 | Policy recommendations developed | Policy briefs (8+ briefs) |
| 6 | 27-30 | Dashboard & final reports | Interactive dashboard, final reports |
| 6 | 31-32 | Quality assurance & stakeholder review | Final deliverables, sign-off |

**Total Duration**: 32 working days (6-7 weeks)

---

## 10. Success Criteria

✅ **Gap Identification Requirements**:
- [ ] Minimum 8 gaps identified across all categories
- [ ] Minimum 3 policy gaps identified
- [ ] Minimum 2 resource gaps identified
- [ ] Minimum 2 service gaps identified
- [ ] Minimum 1 governance gap identified
- [ ] Each gap has affected population and severity quantified

✅ **Analysis Completeness**:
- [ ] System inventory complete (facilities + workforce)
- [ ] International benchmark comparison complete
- [ ] Prioritization framework applied to all gaps
- [ ] Cost-benefit analysis for top 5 gaps complete

✅ **Deliverables**:
- [ ] Prioritized gap list with impact scores
- [ ] CBA reports (minimum 5)
- [ ] Policy recommendation briefs (minimum 8)
- [ ] Interactive policy dashboard deployed

✅ **Quality Standards**:
- [ ] Data quality score >90%
- [ ] Unit test coverage >75%
- [ ] All gaps have evidence base cited
- [ ] CBA includes sensitivity analysis
- [ ] Code reviewed and approved
- [ ] Documentation complete

✅ **Stakeholder Acceptance**:
- [ ] Gap analysis validated by domain experts
- [ ] Policy recommendations reviewed by policy team
- [ ] CBA methodology approved by finance team
- [ ] Dashboard demo presented to stakeholders
- [ ] Sign-off received for recommendations

✅ **Impact Assessment**:
- [ ] Each gap has quantified affected population
- [ ] Top 5 gaps have ROI calculated
- [ ] Implementation roadmap for priority gaps
- [ ] Success metrics defined for each recommendation

---

**Document Version**: 1.0  
**Last Updated**: 2 February 2026  
**Owner**: EPIC-003 Lead Policy Analyst
