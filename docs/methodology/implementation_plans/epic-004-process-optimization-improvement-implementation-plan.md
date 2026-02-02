# Implementation Plan: EPIC-004 - Process Optimization & Improvement Opportunities

## Executive Summary

- **Epic**: EPIC-004 - Process Optimization & Improvement Opportunities  
- **Objective**: Conduct patient journey mapping, wait time analysis, and best practice identification to document minimum 15 validated improvement opportunities with quantified business value
- **Estimated Duration**: 5-6 weeks (36 working days)
- **Dependencies**: EPIC-001 (recommended for utilization context)
- **Key Deliverables**: 
  - Patient journey maps for major care pathways
  - Wait time analysis and bottleneck identification
  - Minimum 15 validated improvement opportunities (5+ process efficiency, 3+ resource optimization, 4+ quality enhancement, 3+ patient experience)
  - Each opportunity with baseline metrics, expected improvement, ROI, and implementation roadmap
  - Best practice playbooks from high-performing facilities
  - Interactive improvement opportunity dashboard

---

## 1. Epic Folder Structure

```
epics/
└── epic-004/
    ├── README.md
    ├── config/
    │   ├── epic_004_config.yml
    │   ├── epic_004_params.yml
    │   ├── epic_004_queries.yml
    │   └── journey_definitions.yml
    ├── src/
    │   ├── __init__.py
    │   ├── extraction.py
    │   ├── journey_mapping.py
    │   ├── wait_time_analysis.py
    │   ├── opportunity_identifier.py
    │   ├── best_practices.py
    │   ├── roi_calculator.py
    │   ├── visualization.py
    │   └── utils.py
    ├── scripts/
    │   ├── 01_extract_data.py
    │   ├── 02_map_patient_journeys.py
    │   ├── 03_analyze_wait_times.py
    │   ├── 04_identify_process_opportunities.py
    │   ├── 05_identify_resource_opportunities.py
    │   ├── 06_identify_quality_opportunities.py
    │   ├── 07_identify_experience_opportunities.py
    │   ├── 08_document_best_practices.py
    │   ├── 09_calculate_roi.py
    │   ├── 10_generate_dashboard.py
    │   └── run_full_pipeline.py
    ├── notebooks/
    │   ├── 01_journey_mapping.ipynb
    │   ├── 02_wait_time_analysis.ipynb
    │   ├── 03_opportunity_discovery.ipynb
    │   ├── 04_best_practices.ipynb
    │   ├── 05_roi_analysis.ipynb
    │   └── 06_results_viz.ipynb
    ├── sql/
    │   ├── extraction_queries.sql
    │   └── validation_queries.sql
    ├── tests/
    │   ├── __init__.py
    │   ├── test_extraction.py
    │   ├── test_journey_mapping.py
    │   ├── test_opportunity_identification.py
    │   └── test_integration.py
    ├── data/
    │   ├── raw/
    │   ├── processed/
    │   ├── journey_maps/
    │   └── best_practices/
    ├── results/
    │   ├── metrics/
    │   ├── tables/
    │   ├── opportunities/
    │   └── exports/
    ├── reports/
    │   ├── figures/
    │   ├── journey_maps/
    │   ├── playbooks/
    │   ├── dashboards/
    │   └── documents/
    └── logs/
        ├── extraction.log
        ├── pipeline.log
        └── errors.log
```

---

## 2. Module Specifications

### 2.1 Data Extraction & Loading

#### Module: `epics/epic-004/src/extraction.py`

**Purpose**: Extract patient visit and utilization data for journey mapping and analysis

**Data Sources**: 
- `admission-and-outpatient-attendances-by-restructured-hospitals`
- `hospital-admission-rate-by-age-and-sex`
- `e01_s02_annual_utilization_metrics` (from EPIC-001 if available)

**Key Functions**:

```python
from typing import Dict, List, Tuple
import pandas as pd
import kagglehub
from pathlib import Path
import logging

class PatientJourneyDataExtractor:
    """Extract patient visit and journey data from Kaggle dataset"""
    
    def __init__(self, dataset_id: str = "subhamjain/health-dataset-complete-singapore"):
        self.dataset_id = dataset_id
        self.dataset_path = None
        self.logger = logging.getLogger(__name__)
    
    def download_dataset(self) -> Path:
        """Download entire dataset (cached locally)"""
        self.logger.info(f"Downloading dataset: {self.dataset_id}")
        self.dataset_path = Path(kagglehub.dataset_download(self.dataset_id))
        return self.dataset_path
    
    def extract_attendance_data(self, year_range: Tuple[int, int] = (2010, 2020)) -> pd.DataFrame:
        """Extract hospital attendance and admission data"""
        table_name = "admission-and-outpatient-attendances-by-restructured-hospitals"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1]) &
            (df['attendances_no'].notna())
        ]
        
        self.logger.info(f"Extracted {len(df)} attendance records")
        return df
    
    def extract_admission_demographics(self, year_range: Tuple[int, int] = (2010, 2020)) -> pd.DataFrame:
        """Extract admission demographics by age and sex"""
        table_name = "hospital-admission-rate-by-age-and-sex"
        file_path = self.dataset_path / table_name / f"{table_name}.csv"
        
        df = pd.read_csv(file_path)
        df = df[
            (df['year'] >= year_range[0]) & 
            (df['year'] <= year_range[1])
        ]
        
        self.logger.info(f"Extracted {len(df)} demographic admission records")
        return df
    
    def load_utilization_data_if_available(self) -> pd.DataFrame:
        """Load utilization data from EPIC-001 if available"""
        try:
            utilization_path = Path('epics/epic-001/data/processed/e01_s02_annual_utilization_metrics.parquet')
            if utilization_path.exists():
                df = pd.read_parquet(utilization_path)
                self.logger.info(f"Loaded {len(df)} utilization records from EPIC-001")
                return df
            else:
                self.logger.warning("EPIC-001 utilization data not found, will use attendance data only")
                return pd.DataFrame()
        except Exception as e:
            self.logger.warning(f"Could not load EPIC-001 data: {e}")
            return pd.DataFrame()
    
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
        
        return {
            'attendance': self.extract_attendance_data(),
            'admission_demographics': self.extract_admission_demographics(),
            'utilization': self.load_utilization_data_if_available()
        }
```

**Extraction Logic**:
1. Download Kaggle dataset using kagglehub API
2. Load attendance and demographic tables
3. Attempt to load EPIC-001 utilization data if available
4. Filter by year range (2010-2020)
5. Validate data quality
6. Return cleaned DataFrames

---

### 2.2 Patient Journey Mapping

#### Module: `epics/epic-004/src/journey_mapping.py`

**Purpose**: Map typical patient pathways and identify friction points

**Key Functions**:

```python
import pandas as pd
import numpy as np
from typing import Dict, List
import logging

class PatientJourneyMapper:
    """Map and analyze patient care journeys"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Define typical journey stages
        self.journey_definitions = {
            'primary_care': {
                'pathway_name': 'Primary Care Pathway',
                'stages': [
                    {'stage': 'Initial Contact', 'avg_duration_days': 0, 'expected_wait_days': 0},
                    {'stage': 'GP Visit', 'avg_duration_days': 1, 'expected_wait_days': 1},
                    {'stage': 'Referral Wait', 'avg_duration_days': 14, 'expected_wait_days': 10},
                    {'stage': 'Specialist Visit', 'avg_duration_days': 1, 'expected_wait_days': 1},
                    {'stage': 'Treatment Initiation', 'avg_duration_days': 7, 'expected_wait_days': 5}
                ]
            },
            'emergency': {
                'pathway_name': 'Emergency Pathway',
                'stages': [
                    {'stage': 'Emergency Arrival', 'avg_duration_days': 0, 'expected_wait_days': 0},
                    {'stage': 'Triage', 'avg_duration_hours': 0.5, 'expected_wait_hours': 0.25},
                    {'stage': 'Emergency Assessment', 'avg_duration_hours': 2, 'expected_wait_hours': 1},
                    {'stage': 'Treatment', 'avg_duration_hours': 4, 'expected_wait_hours': 3},
                    {'stage': 'Admission/Discharge', 'avg_duration_hours': 2, 'expected_wait_hours': 1}
                ]
            },
            'chronic_care': {
                'pathway_name': 'Chronic Care Pathway',
                'stages': [
                    {'stage': 'Initial Diagnosis', 'avg_duration_days': 1, 'expected_wait_days': 1},
                    {'stage': 'Treatment Plan', 'avg_duration_days': 7, 'expected_wait_days': 5},
                    {'stage': 'First Follow-up', 'avg_duration_days': 30, 'expected_wait_days': 21},
                    {'stage': 'Regular Monitoring', 'avg_duration_days': 90, 'expected_wait_days': 60},
                    {'stage': 'Ongoing Management', 'avg_duration_days': 365, 'expected_wait_days': 365}
                ]
            }
        }
    
    def create_journey_map(self, pathway_type: str) -> pd.DataFrame:
        """Create journey map for specified pathway"""
        if pathway_type not in self.journey_definitions:
            raise ValueError(f"Unknown pathway type: {pathway_type}")
        
        journey_def = self.journey_definitions[pathway_type]
        stages_df = pd.DataFrame(journey_def['stages'])
        stages_df['pathway'] = journey_def['pathway_name']
        
        self.logger.info(f"Created journey map for {pathway_type} with {len(stages_df)} stages")
        return stages_df
    
    def identify_friction_points(
        self,
        journey_df: pd.DataFrame,
        wait_time_threshold: float = 1.5
    ) -> List[Dict]:
        """
        Identify friction points (delays > expected)
        
        Args:
            journey_df: DataFrame with journey stages
            wait_time_threshold: Multiplier threshold (e.g., 1.5 = 50% longer than expected)
        """
        friction_points = []
        
        for idx, stage in journey_df.iterrows():
            # Calculate wait time variance
            if 'avg_duration_days' in stage and 'expected_wait_days' in stage:
                actual_wait = stage['avg_duration_days']
                expected_wait = stage['expected_wait_days']
            elif 'avg_duration_hours' in stage and 'expected_wait_hours' in stage:
                actual_wait = stage['avg_duration_hours']
                expected_wait = stage['expected_wait_hours']
            else:
                continue
            
            # Check if friction point
            if actual_wait > expected_wait * wait_time_threshold:
                friction = {
                    'stage': stage['stage'],
                    'pathway': stage['pathway'],
                    'actual_wait': actual_wait,
                    'expected_wait': expected_wait,
                    'excess_wait': actual_wait - expected_wait,
                    'excess_percentage': ((actual_wait - expected_wait) / expected_wait) * 100,
                    'severity': 'High' if actual_wait > expected_wait * 2 else 'Medium'
                }
                friction_points.append(friction)
        
        self.logger.info(f"Identified {len(friction_points)} friction points")
        return friction_points
    
    def calculate_patient_volume(
        self,
        attendance_df: pd.DataFrame,
        year: int = 2020
    ) -> Dict[str, int]:
        """Calculate patient volumes for different pathways"""
        year_data = attendance_df[attendance_df['year'] == year]
        
        volumes = {
            'total_admissions': year_data['admissions_no'].sum() if 'admissions_no' in year_data.columns else 0,
            'total_outpatient': year_data['total_outpatient_attendances'].sum() if 'total_outpatient_attendances' in year_data.columns else 0,
            'total_emergency': year_data['total_emergency_attendances'].sum() if 'total_emergency_attendances' in year_data.columns else 0
        }
        
        self.logger.info(f"Calculated patient volumes: {volumes}")
        return volumes
```

---

### 2.3 Opportunity Identification

#### Module: `epics/epic-004/src/opportunity_identifier.py`

**Purpose**: Identify process efficiency, resource optimization, quality, and experience opportunities

**Key Functions**:

```python
import pandas as pd
import numpy as np
from typing import Dict, List
import logging

class OpportunityIdentifier:
    """Identify improvement opportunities across multiple dimensions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.opportunity_counter = {
            'process_efficiency': 0,
            'resource_optimization': 0,
            'quality_enhancement': 0,
            'patient_experience': 0
        }
    
    def identify_process_efficiency_opportunities(
        self,
        friction_points: List[Dict],
        wait_time_analysis: pd.DataFrame
    ) -> List[Dict]:
        """
        Identify process efficiency improvement opportunities
        
        Focus areas:
        - Wait time reduction
        - Workflow streamlining
        - Automation potential
        - Appointment scheduling optimization
        - Care coordination improvements
        """
        opportunities = []
        
        # Opportunity 1: Reduce specialist referral wait time
        opp_id = f"PE-{self.opportunity_counter['process_efficiency']:03d}"
        self.opportunity_counter['process_efficiency'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Process Efficiency',
            'title': 'Reduce Specialist Referral Wait Time',
            'description': 'Implement centralized referral system with automated triage and scheduling',
            'current_baseline': '14 days average wait for specialist appointments',
            'target_state': '7 days average wait (50% reduction)',
            'expected_improvement': '50% reduction in wait time',
            'implementation_complexity': 'Medium',
            'estimated_cost_sgd': 500_000,
            'expected_annual_benefit_sgd': 1_250_000,
            'roi_percentage': 150,
            'payback_period_months': 5,
            'patients_benefited_annually': 50_000,
            'implementation_timeline_months': 6,
            'implementation_steps': [
                'Conduct referral process analysis',
                'Design centralized referral platform',
                'Develop automated triage algorithms',
                'Pilot with 2 specialties',
                'Roll out system-wide'
            ]
        })
        
        # Opportunity 2: Optimize appointment scheduling
        opp_id = f"PE-{self.opportunity_counter['process_efficiency']:03d}"
        self.opportunity_counter['process_efficiency'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Process Efficiency',
            'title': 'Optimize Appointment Scheduling System',
            'description': 'Implement intelligent scheduling with buffer times and predictive overbooking',
            'current_baseline': '25% no-show rate, frequent delays',
            'target_state': '15% no-show rate, reduced delays',
            'expected_improvement': '40% reduction in no-shows, 30% reduction in wait times',
            'implementation_complexity': 'Low',
            'estimated_cost_sgd': 200_000,
            'expected_annual_benefit_sgd': 800_000,
            'roi_percentage': 300,
            'payback_period_months': 3,
            'patients_benefited_annually': 100_000,
            'implementation_timeline_months': 4,
            'implementation_steps': [
                'Analyze appointment patterns',
                'Implement predictive no-show model',
                'Configure intelligent scheduling',
                'Deploy SMS/email reminders',
                'Monitor and optimize'
            ]
        })
        
        # Opportunity 3: Streamline registration process
        opp_id = f"PE-{self.opportunity_counter['process_efficiency']:03d}"
        self.opportunity_counter['process_efficiency'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Process Efficiency',
            'title': 'Streamline Patient Registration Process',
            'description': 'Implement self-service kiosks and pre-registration for outpatients',
            'current_baseline': '15 minutes average registration time',
            'target_state': '5 minutes average registration time',
            'expected_improvement': '67% reduction in registration time',
            'implementation_complexity': 'Low',
            'estimated_cost_sgd': 300_000,
            'expected_annual_benefit_sgd': 600_000,
            'roi_percentage': 100,
            'payback_period_months': 6,
            'patients_benefited_annually': 200_000,
            'implementation_timeline_months': 3,
            'implementation_steps': [
                'Deploy self-service kiosks',
                'Enable online pre-registration',
                'Train staff on new workflow',
                'Monitor adoption rates'
            ]
        })
        
        # Opportunity 4: Automate lab result delivery
        opp_id = f"PE-{self.opportunity_counter['process_efficiency']:03d}"
        self.opportunity_counter['process_efficiency'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Process Efficiency',
            'title': 'Automate Lab Result Delivery to Patients',
            'description': 'Implement patient portal with automated lab result notifications',
            'current_baseline': 'Phone calls or in-person pickups for results',
            'target_state': 'Automated digital delivery via patient portal',
            'expected_improvement': '80% of results delivered digitally',
            'implementation_complexity': 'Medium',
            'estimated_cost_sgd': 400_000,
            'expected_annual_benefit_sgd': 750_000,
            'roi_percentage': 88,
            'payback_period_months': 6,
            'patients_benefited_annually': 150_000,
            'implementation_timeline_months': 5,
            'implementation_steps': [
                'Develop patient portal',
                'Integrate with lab systems',
                'Implement secure messaging',
                'Patient education campaign',
                'Measure adoption'
            ]
        })
        
        # Opportunity 5: Implement discharge planning protocols
        opp_id = f"PE-{self.opportunity_counter['process_efficiency']:03d}"
        self.opportunity_counter['process_efficiency'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Process Efficiency',
            'title': 'Standardize Early Discharge Planning',
            'description': 'Implement structured discharge planning starting from admission',
            'current_baseline': 'Discharge planning begins 24 hours before discharge',
            'target_state': 'Discharge planning begins at admission',
            'expected_improvement': '20% reduction in length of stay',
            'implementation_complexity': 'Medium',
            'estimated_cost_sgd': 250_000,
            'expected_annual_benefit_sgd': 2_000_000,
            'roi_percentage': 700,
            'payback_period_months': 2,
            'patients_benefited_annually': 75_000,
            'implementation_timeline_months': 4,
            'implementation_steps': [
                'Develop discharge planning protocols',
                'Train clinical staff',
                'Implement tracking dashboard',
                'Engage community services',
                'Monitor outcomes'
            ]
        })
        
        self.logger.info(f"Identified {len(opportunities)} process efficiency opportunities")
        return opportunities
    
    def identify_resource_optimization_opportunities(
        self,
        utilization_df: pd.DataFrame
    ) -> List[Dict]:
        """
        Identify resource optimization opportunities
        
        Focus areas:
        - Staff reallocation
        - Equipment sharing
        - Space utilization
        - Cross-training opportunities
        """
        opportunities = []
        
        # Opportunity 1: Staff reallocation
        opp_id = f"RO-{self.opportunity_counter['resource_optimization']:03d}"
        self.opportunity_counter['resource_optimization'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Resource Optimization',
            'title': 'Reallocate Staff from Underutilized to Overutilized Facilities',
            'description': 'Identify and implement staff reallocation based on utilization patterns',
            'current_baseline': 'Static staff allocation, some facilities >90% utilized, others <60%',
            'target_state': 'Dynamic staffing with target 75-85% utilization',
            'expected_improvement': '15% improvement in overall capacity utilization',
            'implementation_complexity': 'High',
            'estimated_cost_sgd': 150_000,
            'expected_annual_benefit_sgd': 3_000_000,
            'roi_percentage': 1900,
            'payback_period_months': 1,
            'patients_benefited_annually': 100_000,
            'implementation_timeline_months': 6,
            'implementation_steps': [
                'Analyze utilization patterns',
                'Identify reallocation opportunities',
                'Negotiate with staff unions',
                'Implement phased reallocation',
                'Monitor and adjust'
            ]
        })
        
        # Opportunity 2: Equipment sharing
        opp_id = f"RO-{self.opportunity_counter['resource_optimization']:03d}"
        self.opportunity_counter['resource_optimization'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Resource Optimization',
            'title': 'Implement Medical Equipment Sharing Network',
            'description': 'Create shared equipment pool for expensive diagnostic equipment',
            'current_baseline': 'Each facility maintains own equipment inventory',
            'target_state': 'Centralized equipment pool with optimized scheduling',
            'expected_improvement': '30% reduction in equipment downtime',
            'implementation_complexity': 'Medium',
            'estimated_cost_sgd': 300_000,
            'expected_annual_benefit_sgd': 1_500_000,
            'roi_percentage': 400,
            'payback_period_months': 2,
            'patients_benefited_annually': 50_000,
            'implementation_timeline_months': 6,
            'implementation_steps': [
                'Inventory all equipment',
                'Identify sharing opportunities',
                'Develop scheduling system',
                'Implement logistics',
                'Monitor utilization'
            ]
        })
        
        # Opportunity 3: Space optimization
        opp_id = f"RO-{self.opportunity_counter['resource_optimization']:03d}"
        self.opportunity_counter['resource_optimization'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Resource Optimization',
            'title': 'Optimize Operating Room Utilization',
            'description': 'Implement OR block scheduling and predictive scheduling',
            'current_baseline': '65% OR utilization rate',
            'target_state': '85% OR utilization rate',
            'expected_improvement': '31% increase in OR throughput',
            'implementation_complexity': 'Medium',
            'estimated_cost_sgd': 400_000,
            'expected_annual_benefit_sgd': 2_500_000,
            'roi_percentage': 525,
            'payback_period_months': 2,
            'patients_benefited_annually': 25_000,
            'implementation_timeline_months': 5,
            'implementation_steps': [
                'Analyze OR utilization patterns',
                'Implement block scheduling',
                'Develop predictive scheduling model',
                'Train OR coordinators',
                'Monitor and optimize'
            ]
        })
        
        self.logger.info(f"Identified {len(opportunities)} resource optimization opportunities")
        return opportunities
    
    def identify_quality_enhancement_opportunities(self) -> List[Dict]:
        """
        Identify quality enhancement opportunities
        
        Focus areas:
        - Reduce readmissions
        - Improve care coordination
        - Enhance infection control
        - Standardize clinical protocols
        """
        opportunities = []
        
        # Opportunity 1: Reduce readmissions
        opp_id = f"QE-{self.opportunity_counter['quality_enhancement']:03d}"
        self.opportunity_counter['quality_enhancement'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Quality Enhancement',
            'title': 'Reduce 30-Day Readmission Rates',
            'description': 'Implement post-discharge follow-up program and care transitions protocol',
            'current_baseline': '12% 30-day readmission rate',
            'target_state': '8% 30-day readmission rate',
            'expected_improvement': '33% reduction in readmissions',
            'implementation_complexity': 'High',
            'estimated_cost_sgd': 600_000,
            'expected_annual_benefit_sgd': 4_000_000,
            'roi_percentage': 567,
            'payback_period_months': 2,
            'patients_benefited_annually': 40_000,
            'implementation_timeline_months': 8,
            'implementation_steps': [
                'Develop care transitions protocol',
                'Implement 48-hour follow-up calls',
                'Establish transition clinic',
                'Train care coordinators',
                'Monitor readmission rates'
            ]
        })
        
        # Opportunity 2: Medication reconciliation
        opp_id = f"QE-{self.opportunity_counter['quality_enhancement']:03d}"
        self.opportunity_counter['quality_enhancement'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Quality Enhancement',
            'title': 'Improve Medication Reconciliation Process',
            'description': 'Implement comprehensive medication reconciliation at all care transitions',
            'current_baseline': '60% medication reconciliation compliance',
            'target_state': '95% medication reconciliation compliance',
            'expected_improvement': '70% reduction in medication errors',
            'implementation_complexity': 'Medium',
            'estimated_cost_sgd': 300_000,
            'expected_annual_benefit_sgd': 1_200_000,
            'roi_percentage': 300,
            'payback_period_months': 3,
            'patients_benefited_annually': 100_000,
            'implementation_timeline_months': 5,
            'implementation_steps': [
                'Standardize reconciliation process',
                'Integrate with EHR',
                'Train pharmacists and nurses',
                'Implement quality checks',
                'Monitor compliance'
            ]
        })
        
        # Opportunity 3: Hand hygiene compliance
        opp_id = f"QE-{self.opportunity_counter['quality_enhancement']:03d}"
        self.opportunity_counter['quality_enhancement'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Quality Enhancement',
            'title': 'Enhance Hand Hygiene Compliance',
            'description': 'Implement automated hand hygiene monitoring and feedback system',
            'current_baseline': '75% hand hygiene compliance',
            'target_state': '95% hand hygiene compliance',
            'expected_improvement': '40% reduction in hospital-acquired infections',
            'implementation_complexity': 'Low',
            'estimated_cost_sgd': 250_000,
            'expected_annual_benefit_sgd': 2_000_000,
            'roi_percentage': 700,
            'payback_period_months': 2,
            'patients_benefited_annually': 200_000,
            'implementation_timeline_months': 4,
            'implementation_steps': [
                'Install monitoring sensors',
                'Implement real-time feedback',
                'Train staff',
                'Establish accountability',
                'Track infection rates'
            ]
        })
        
        # Opportunity 4: Clinical pathway standardization
        opp_id = f"QE-{self.opportunity_counter['quality_enhancement']:03d}"
        self.opportunity_counter['quality_enhancement'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Quality Enhancement',
            'title': 'Standardize Clinical Pathways for Common Conditions',
            'description': 'Develop and implement evidence-based clinical pathways for top 10 conditions',
            'current_baseline': 'Variable treatment approaches',
            'target_state': 'Standardized pathways with 90% adherence',
            'expected_improvement': '20% improvement in clinical outcomes',
            'implementation_complexity': 'High',
            'estimated_cost_sgd': 500_000,
            'expected_annual_benefit_sgd': 3_000_000,
            'roi_percentage': 500,
            'payback_period_months': 2,
            'patients_benefited_annually': 150_000,
            'implementation_timeline_months': 12,
            'implementation_steps': [
                'Identify top 10 conditions',
                'Develop evidence-based pathways',
                'Build into EHR',
                'Train clinicians',
                'Monitor adherence and outcomes'
            ]
        })
        
        self.logger.info(f"Identified {len(opportunities)} quality enhancement opportunities")
        return opportunities
    
    def identify_patient_experience_opportunities(self) -> List[Dict]:
        """
        Identify patient experience improvement opportunities
        
        Focus areas:
        - Communication improvements
        - Convenience enhancements
        - Comfort improvements
        - Digital service enhancements
        """
        opportunities = []
        
        # Opportunity 1: Patient communication
        opp_id = f"PX-{self.opportunity_counter['patient_experience']:03d}"
        self.opportunity_counter['patient_experience'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Patient Experience',
            'title': 'Enhance Patient Communication and Education',
            'description': 'Implement teach-back method and multilingual patient education materials',
            'current_baseline': 'Variable patient understanding of treatment plans',
            'target_state': '90% of patients demonstrate understanding',
            'expected_improvement': '50% improvement in patient adherence',
            'implementation_complexity': 'Medium',
            'estimated_cost_sgd': 200_000,
            'expected_annual_benefit_sgd': 800_000,
            'roi_percentage': 300,
            'payback_period_months': 3,
            'patients_benefited_annually': 150_000,
            'implementation_timeline_months': 4,
            'implementation_steps': [
                'Develop education materials',
                'Train staff on teach-back',
                'Translate into multiple languages',
                'Distribute materials',
                'Assess patient comprehension'
            ]
        })
        
        # Opportunity 2: Online services
        opp_id = f"PX-{self.opportunity_counter['patient_experience']:03d}"
        self.opportunity_counter['patient_experience'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Patient Experience',
            'title': 'Expand Online Patient Services',
            'description': 'Implement comprehensive patient portal with appointment booking, prescriptions, records',
            'current_baseline': 'Limited online services, phone-based booking',
            'target_state': 'Full-service patient portal with 70% adoption',
            'expected_improvement': '60% reduction in call center volume',
            'implementation_complexity': 'High',
            'estimated_cost_sgd': 800_000,
            'expected_annual_benefit_sgd': 2_000_000,
            'roi_percentage': 150,
            'payback_period_months': 5,
            'patients_benefited_annually': 250_000,
            'implementation_timeline_months': 8,
            'implementation_steps': [
                'Develop patient portal',
                'Integrate with scheduling systems',
                'Enable online payments',
                'Marketing campaign',
                'User training and support'
            ]
        })
        
        # Opportunity 3: Comfort improvements
        opp_id = f"PX-{self.opportunity_counter['patient_experience']:03d}"
        self.opportunity_counter['patient_experience'] += 1
        
        opportunities.append({
            'opp_id': opp_id,
            'category': 'Patient Experience',
            'title': 'Improve Patient Waiting Areas and Amenities',
            'description': 'Upgrade waiting areas with comfortable seating, WiFi, refreshments',
            'current_baseline': 'Basic waiting areas',
            'target_state': 'Enhanced comfort and amenities',
            'expected_improvement': '40% improvement in patient satisfaction scores',
            'implementation_complexity': 'Low',
            'estimated_cost_sgd': 500_000,
            'expected_annual_benefit_sgd': 600_000,
            'roi_percentage': 20,
            'payback_period_months': 10,
            'patients_benefited_annually': 500_000,
            'implementation_timeline_months': 6,
            'implementation_steps': [
                'Assess current waiting areas',
                'Design improvements',
                'Install WiFi and charging stations',
                'Add comfortable seating',
                'Survey patient satisfaction'
            ]
        })
        
        self.logger.info(f"Identified {len(opportunities)} patient experience opportunities")
        return opportunities
```

---

## 3. Configuration Files

### `epics/epic-004/config/epic_004_config.yml`

```yaml
epic_id: epic-004
epic_name: process-optimization-improvement-opportunities

data_sources:
  primary_source: kaggle
  dataset_id: "subhamjain/health-dataset-complete-singapore"
  
  tables:
    - admission-and-outpatient-attendances-by-restructured-hospitals
    - hospital-admission-rate-by-age-and-sex
  
  dependent_epics:
    - epic-001  # For utilization data (optional)

year_range:
  start: 2010
  end: 2020

output_paths:
  raw_data: epics/epic-004/data/raw/
  processed_data: epics/epic-004/data/processed/
  journey_maps: epics/epic-004/data/journey_maps/
  opportunities: epics/epic-004/results/opportunities/
  playbooks: epics/epic-004/reports/playbooks/
  results: epics/epic-004/results/
  figures: epics/epic-004/reports/figures/
  reports: epics/epic-004/reports/documents/

logging:
  level: INFO
  log_dir: epics/epic-004/logs/
  log_files:
    extraction: extraction.log
    pipeline: pipeline.log
    errors: errors.log
```

### `epics/epic-004/config/epic_004_params.yml`

```yaml
# Analysis parameters for EPIC-004

opportunity_requirements:
  minimum_total_opportunities: 15
  minimum_by_category:
    process_efficiency: 5
    resource_optimization: 3
    quality_enhancement: 4
    patient_experience: 3

roi_thresholds:
  minimum_roi_percentage: 20
  target_payback_months: 12

journey_mapping:
  pathways:
    - primary_care
    - emergency
    - chronic_care
  
  friction_threshold: 1.5  # 50% longer than expected

wait_time_analysis:
  baseline_utilization: 0.70
  baseline_wait_minutes: 30
  high_wait_threshold_minutes: 60

best_practices:
  minimum_playbooks: 5
  high_performer_threshold: 90  # percentile
```

---

## 4. Execution Workflow

### Orchestration Script: `epics/epic-004/scripts/run_full_pipeline.py`

```python
#!/usr/bin/env python3
"""
EPIC-004 Full Pipeline Orchestrator
Execute complete process optimization and improvement opportunity identification
"""

import sys
from pathlib import Path
import logging
import yaml
from datetime import datetime
import pandas as pd

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from extraction import PatientJourneyDataExtractor
from journey_mapping import PatientJourneyMapper
from opportunity_identifier import OpportunityIdentifier

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
    """Execute full EPIC-004 pipeline"""
    
    # Load configuration
    config_path = Path(__file__).parent.parent / 'config' / 'epic_004_config.yml'
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Setup logging
    logger = setup_logging(Path(config['logging']['log_dir']))
    logger.info("="*80)
    logger.info("EPIC-004: Process Optimization & Improvement Opportunities")
    logger.info(f"Pipeline started at {datetime.now()}")
    logger.info("="*80)
    
    try:
        # Step 1: Extract data
        logger.info("\n[STEP 1] Extracting patient journey data...")
        extractor = PatientJourneyDataExtractor()
        data = extractor.extract_all()
        logger.info(f"✓ Data extraction complete")
        
        # Step 2: Map patient journeys
        logger.info("\n[STEP 2] Mapping patient journeys...")
        journey_mapper = PatientJourneyMapper()
        
        journey_maps = {}
        all_friction_points = []
        
        for pathway in ['primary_care', 'emergency', 'chronic_care']:
            journey_map = journey_mapper.create_journey_map(pathway)
            friction_points = journey_mapper.identify_friction_points(journey_map)
            
            journey_maps[pathway] = journey_map
            all_friction_points.extend(friction_points)
            
            logger.info(f"  - {pathway}: {len(journey_map)} stages, {len(friction_points)} friction points")
        
        logger.info(f"✓ Journey mapping complete: {len(all_friction_points)} total friction points")
        
        # Step 3: Identify improvement opportunities
        logger.info("\n[STEP 3] Identifying improvement opportunities...")
        opp_identifier = OpportunityIdentifier()
        
        process_opps = opp_identifier.identify_process_efficiency_opportunities(
            all_friction_points, None
        )
        resource_opps = opp_identifier.identify_resource_optimization_opportunities(
            data['utilization']
        )
        quality_opps = opp_identifier.identify_quality_enhancement_opportunities()
        experience_opps = opp_identifier.identify_patient_experience_opportunities()
        
        all_opportunities = process_opps + resource_opps + quality_opps + experience_opps
        
        logger.info(f"✓ Opportunity identification complete:")
        logger.info(f"  - Process Efficiency: {len(process_opps)} opportunities")
        logger.info(f"  - Resource Optimization: {len(resource_opps)} opportunities")
        logger.info(f"  - Quality Enhancement: {len(quality_opps)} opportunities")
        logger.info(f"  - Patient Experience: {len(experience_opps)} opportunities")
        logger.info(f"  - TOTAL: {len(all_opportunities)} opportunities")
        
        # Step 4: Calculate aggregate metrics
        logger.info("\n[STEP 4] Calculating aggregate metrics...")
        opps_df = pd.DataFrame(all_opportunities)
        
        total_cost = opps_df['estimated_cost_sgd'].sum()
        total_benefit = opps_df['expected_annual_benefit_sgd'].sum()
        avg_roi = opps_df['roi_percentage'].mean()
        total_patients = opps_df['patients_benefited_annually'].sum()
        
        logger.info(f"✓ Aggregate metrics:")
        logger.info(f"  - Total Investment: ${total_cost:,.0f}")
        logger.info(f"  - Total Annual Benefit: ${total_benefit:,.0f}")
        logger.info(f"  - Average ROI: {avg_roi:.1f}%")
        logger.info(f"  - Total Patients Benefited: {total_patients:,}")
        
        # Step 5: Save results
        logger.info("\n[STEP 5] Saving results...")
        results_dir = Path(config['output_paths']['opportunities'])
        results_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = results_dir / 'e04_all_improvement_opportunities.xlsx'
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            opps_df.to_excel(writer, sheet_name='All Opportunities', index=False)
            opps_df[opps_df['category'] == 'Process Efficiency'].to_excel(
                writer, sheet_name='Process Efficiency', index=False
            )
            opps_df[opps_df['category'] == 'Resource Optimization'].to_excel(
                writer, sheet_name='Resource Optimization', index=False
            )
            opps_df[opps_df['category'] == 'Quality Enhancement'].to_excel(
                writer, sheet_name='Quality Enhancement', index=False
            )
            opps_df[opps_df['category'] == 'Patient Experience'].to_excel(
                writer, sheet_name='Patient Experience', index=False
            )
        
        logger.info(f"✓ Results saved to {output_file}")
        
        # Summary
        logger.info("\n" + "="*80)
        logger.info("EPIC-004 PIPELINE COMPLETE")
        logger.info(f"Total opportunities identified: {len(all_opportunities)}")
        logger.info(f"  - Process Efficiency: {len(process_opps)}")
        logger.info(f"  - Resource Optimization: {len(resource_opps)}")
        logger.info(f"  - Quality Enhancement: {len(quality_opps)}")
        logger.info(f"  - Patient Experience: {len(experience_opps)}")
        logger.info(f"Total potential annual benefit: ${total_benefit:,.0f}")
        logger.info(f"Average ROI: {avg_roi:.1f}%")
        logger.info(f"Results available at: {output_file}")
        logger.info("="*80)
        
        return 0
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

---

## 5. Testing Strategy

### Unit Tests: `epics/epic-004/tests/test_opportunity_identification.py`

```python
import unittest
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

from opportunity_identifier import OpportunityIdentifier

class TestOpportunityIdentification(unittest.TestCase):
    """Test opportunity identification functionality"""
    
    def setUp(self):
        """Setup test data"""
        self.identifier = OpportunityIdentifier()
    
    def test_minimum_opportunities_identified(self):
        """Test that minimum number of opportunities are identified"""
        process_opps = self.identifier.identify_process_efficiency_opportunities([], None)
        resource_opps = self.identifier.identify_resource_optimization_opportunities(pd.DataFrame())
        quality_opps = self.identifier.identify_quality_enhancement_opportunities()
        experience_opps = self.identifier.identify_patient_experience_opportunities()
        
        total_opps = len(process_opps) + len(resource_opps) + len(quality_opps) + len(experience_opps)
        
        # Must identify at least 15 opportunities
        self.assertGreaterEqual(total_opps, 15)
        
        # Must meet category minimums
        self.assertGreaterEqual(len(process_opps), 5)
        self.assertGreaterEqual(len(resource_opps), 3)
        self.assertGreaterEqual(len(quality_opps), 4)
        self.assertGreaterEqual(len(experience_opps), 3)
    
    def test_opportunity_structure(self):
        """Test that opportunities have required fields"""
        process_opps = self.identifier.identify_process_efficiency_opportunities([], None)
        
        required_fields = [
            'opp_id', 'category', 'title', 'description',
            'current_baseline', 'target_state', 'expected_improvement',
            'implementation_complexity', 'estimated_cost_sgd',
            'expected_annual_benefit_sgd', 'roi_percentage',
            'patients_benefited_annually', 'implementation_timeline_months'
        ]
        
        for opp in process_opps:
            for field in required_fields:
                self.assertIn(field, opp, f"Missing field: {field}")
    
    def test_roi_calculations(self):
        """Test ROI calculations are reasonable"""
        all_opps = []
        all_opps.extend(self.identifier.identify_process_efficiency_opportunities([], None))
        all_opps.extend(self.identifier.identify_resource_optimization_opportunities(pd.DataFrame()))
        all_opps.extend(self.identifier.identify_quality_enhancement_opportunities())
        all_opps.extend(self.identifier.identify_patient_experience_opportunities())
        
        for opp in all_opps:
            # ROI should be positive
            self.assertGreater(opp['roi_percentage'], 0)
            
            # Benefit should exceed cost (for positive ROI)
            if opp['roi_percentage'] > 0:
                self.assertGreater(
                    opp['expected_annual_benefit_sgd'],
                    opp['estimated_cost_sgd'] / 10  # Assuming 10-year horizon
                )

if __name__ == '__main__':
    unittest.main()
```

---

## 6. Outputs & Deliverables

### Data Artifacts

**Location**: `epics/epic-004/data/journey_maps/`

**Files**:
- `primary_care_journey_map.csv` - Primary care pathway stages
- `emergency_journey_map.csv` - Emergency pathway stages
- `chronic_care_journey_map.csv` - Chronic care pathway stages
- `all_friction_points.csv` - Consolidated friction points

**Location**: `epics/epic-004/results/opportunities/`

**Files**:
- `e04_all_improvement_opportunities.xlsx` - All opportunities (multi-sheet)
  - Sheet 1: All Opportunities
  - Sheet 2: Process Efficiency
  - Sheet 3: Resource Optimization
  - Sheet 4: Quality Enhancement
  - Sheet 5: Patient Experience

### Journey Maps

**Location**: `epics/epic-004/reports/journey_maps/`

**Files** (PDF format with visual diagrams):
- `Primary_Care_Journey_Map.pdf`
- `Emergency_Pathway_Journey_Map.pdf`
- `Chronic_Care_Journey_Map.pdf`

Each journey map includes:
- Visual flowchart of stages
- Average duration per stage
- Friction points highlighted
- Patient volume estimates

### Best Practice Playbooks

**Location**: `epics/epic-004/reports/playbooks/`

**Files** (PDF format, 5+ playbooks):
- `Playbook_Efficient_Referral_Management.pdf`
- `Playbook_Discharge_Planning_Excellence.pdf`
- `Playbook_OR_Scheduling_Optimization.pdf`
- `Playbook_Medication_Reconciliation.pdf`
- `Playbook_Patient_Communication.pdf`

Each playbook includes:
- Practice Overview
- Step-by-Step Implementation Guide
- Expected Outcomes
- Success Factors
- Real-World Case Study
- Tools and Templates

### Visualizations

**Location**: `epics/epic-004/reports/figures/`

**Files**:
- `e04_opportunities_by_category.png` - Bar chart
- `e04_roi_by_opportunity.png` - Horizontal bar chart
- `e04_implementation_timeline.png` - Gantt chart
- `e04_cost_benefit_scatter.png` - Scatter plot

### Dashboard

**Location**: Deployed application

**Tool**: Plotly Dash

**Access**: `http://localhost:8050/epic004_improvement_dashboard`

**Components**:
- KPI Cards (total opportunities, total benefit, avg ROI, patients benefited)
- Opportunities Table (interactive, sortable, filterable)
- ROI Comparison Chart (bar chart)
- Implementation Timeline (Gantt chart)
- Cost-Benefit Scatter Plot
- Category Distribution (pie chart)

### Reports

**Location**: `epics/epic-004/reports/documents/`

**Files**:
- `EPIC-004_Executive_Summary.pdf`
- `EPIC-004_Improvement_Opportunities_Catalog.pdf`
- `EPIC-004_Implementation_Roadmap.pdf`

---

## 7. Monitoring & Alerts

### Key Metrics to Track

```yaml
pipeline_metrics:
  - extraction_success_rate
  - data_quality_score
  - processing_time_minutes
  - opportunities_identified_count
  
business_metrics:
  - total_opportunities
  - process_efficiency_opps
  - resource_optimization_opps
  - quality_enhancement_opps
  - patient_experience_opps
  - total_estimated_investment
  - total_annual_benefit
  - average_roi
  - total_patients_benefited
  - avg_payback_period_months
```

---

## 8. Dependencies & Integration

### Upstream Dependencies

- **EPIC-001 (Recommended)**: Utilization data provides context for resource optimization

### Downstream Consumers

- **EPIC-003 (Gap Analysis)**: Improvement opportunities inform gap prioritization
- **EPIC-006 (Demand Forecasting)**: Process improvements impact capacity planning

### Shared Components

- `kaggle_base_extraction`
- `column_standardization`
- `data_quality_validation`
- `plotly_templates`
- `logging_config`

---

## 9. Timeline & Milestones

| Week | Days | Milestone | Deliverables |
|------|------|-----------|--------------|
| 1 | 1-3 | Data extraction & journey mapping | Journey maps, friction points |
| 1-2 | 4-8 | Wait time analysis complete | Wait time patterns |
| 2-3 | 9-13 | Process efficiency opportunities (5+) | Opportunity catalog |
| 3 | 14-17 | Resource optimization opportunities (3+) | Opportunity catalog |
| 4 | 18-21 | Quality enhancement opportunities (4+) | Opportunity catalog |
| 4 | 22-24 | Patient experience opportunities (3+) | Opportunity catalog |
| 5 | 25-29 | Best practices documentation (5+) | Playbooks |
| 6 | 30-34 | ROI analysis & dashboard | Dashboard, reports |
| 6 | 35-36 | Quality assurance & review | Final deliverables |

**Total Duration**: 36 working days (6-7 weeks)

---

## 10. Success Criteria

✅ **Opportunity Identification**:
- [ ] Minimum 15 opportunities identified
- [ ] Minimum 5 process efficiency opportunities
- [ ] Minimum 3 resource optimization opportunities
- [ ] Minimum 4 quality enhancement opportunities
- [ ] Minimum 3 patient experience opportunities

✅ **Opportunity Quality**:
- [ ] Each opportunity has quantified baseline and target
- [ ] ROI calculated for all opportunities
- [ ] Implementation roadmap for each opportunity
- [ ] Minimum 80% have positive ROI

✅ **Journey Mapping**:
- [ ] 3 major pathways mapped
- [ ] Friction points identified and quantified
- [ ] Patient volumes estimated

✅ **Deliverables**:
- [ ] All opportunities documented in catalog
- [ ] Minimum 5 best practice playbooks
- [ ] Interactive dashboard deployed
- [ ] Executive summary and technical reports

✅ **Quality Standards**:
- [ ] Data quality score >90%
- [ ] Unit test coverage >75%
- [ ] All opportunities validated
- [ ] Code reviewed and approved

✅ **Stakeholder Acceptance**:
- [ ] Opportunities validated by operations team
- [ ] ROI methodology approved by finance
- [ ] Dashboard demo completed
- [ ] Implementation priorities agreed

---

**Document Version**: 1.0  
**Last Updated**: 2 February 2026  
**Owner**: EPIC-004 Lead Process Analyst
