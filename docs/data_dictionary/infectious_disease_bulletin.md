# Data Dictionary: Weekly Infectious Disease Bulletin

**Dataset:** Weekly Infectious Disease Bulletin Cases  
**Source:** Ministry of Health Singapore (via Kaggle)  
**Table Name:** `weekly-infectious-disease-bulletin-cases.csv`  
**Last Updated:** 9 February 2026  
**Data Period:** 2012-W01 to 2020-W53

---

## Table Overview

This table contains weekly case counts for all notifiable infectious diseases tracked by Singapore's Ministry of Health surveillance system. The data is reported in epidemiological weeks (epi-weeks) and covers 45 different infectious diseases over a 9-year period.

**Key Statistics:**
- **Total Records:** 16,066
- **Unique Diseases:** 45
- **Weeks Covered:** 470 (2012-2020)
- **Data Quality:** 100% complete (no missing values)
- **Update Frequency:** Weekly (historical data)
- **Granularity:** National level (no regional breakdowns)

---

## Schema

| Column Name | Data Type | Description | Example Values | Constraints |
|-------------|-----------|-------------|----------------|-------------|
| `epi_week` | String | Epidemiological week in ISO format (YYYY-Wxx) | `2012-W01`, `2020-W53` | Not null, Format: `YYYY-Wxx` |
| `disease` | String | Name of the infectious disease | `Dengue Fever`, `HFMD`, `Cholera` | Not null, 45 unique values |
| `no._of_cases` | Integer | Number of confirmed cases reported in that week | `0`, `74`, `1791` | Not null, ≥ 0 |

---

## Field Definitions

### 1. `epi_week`

**Description:** Epidemiological week identifier using the ISO week date system

**Format:** `YYYY-Wxx`
- `YYYY`: 4-digit year
- `W`: Literal character "W"
- `xx`: 2-digit week number (01-53)

**Epidemiological Week System:**
- Week starts on Sunday, ends on Saturday
- Week 1 is the first week with at least 4 days in the new year
- Some years have 53 weeks (e.g., 2020)

**Examples:**
- `2012-W01`: First week of 2012
- `2020-W53`: 53rd week of 2020 (leap year with extra week)

**Parsing Note:** To extract year and week number:
```python
df['year'] = df['epi_week'].str.split('-').str[0].astype(int)
df['week'] = df['epi_week'].str.split('-').str[1].str.replace('W', '').astype(int)
```

---

### 2. `disease`

**Description:** Official name of the notifiable infectious disease as classified by MOH

**Data Type:** String (categorical)

**Unique Values:** 45 diseases

#### High-Burden Diseases (>1,000 total cases):
| Disease | Total Cases (2012-2020) | Category |
|---------|-------------------------|----------|
| Hand, Foot Mouth Disease | 161,482 | Viral Infection |
| Dengue Fever | 126,642 | Vector-borne |
| HFMD | 73,927 | Viral Infection |
| Salmonellosis(non-enteric fevers) | 16,497 | Foodborne |
| Mumps | 4,213 | Vaccine-preventable |
| Campylobacterenterosis | 2,138 | Foodborne |
| Campylobacter enteritis | 1,914 | Foodborne |
| Chikungunya Fever | 1,348 | Vector-borne |
| Pneumococcal Disease (invasive) | 1,203 | Bacterial |

#### Complete Disease List:
- Acute Viral Hepatitis A
- Acute Viral Hepatitis B
- Acute Viral Hepatitis C
- Acute Viral Hepatitis E
- Avian Influenza
- Botulism
- Campylobacter enteritis
- Campylobacterenterosis
- Chikungunya
- Chikungunya Fever
- Cholera
- Dengue Fever
- Dengue Haemorrhagic Fever
- Diphtheria
- Ebola Virus Disease
- Encephalitis
- Haemophilus influenzae type b
- Hand, Foot Mouth Disease
- HFMD
- Japanese Encephalitis
- Legionellosis
- Leptospirosis
- Malaria
- Measles
- Melioidosis
- Meningococcal Infection
- Mumps
- Murine Typhus
- Nipah
- Nipah virus infection
- Paratyphoid
- Pertussis
- Plague
- Pneumococcal Disease (invasive)
- Poliomyelitis
- Rubella
- Salmonellosis(non-enteric fevers)
- SARS
- Tetanus
- Typhoid
- Viral Hepatitis A
- Viral Hepatitis E
- Yellow Fever
- Zika
- Zika Virus Infection

**Data Quality Notes:**
- Some disease names changed over time (e.g., "Hand, Foot Mouth Disease" vs "HFMD")
- "HFMD" appears only in 2017-2020 data
- "Hand, Foot Mouth Disease" appears in 2012-2016 data
- These represent the same disease and should be merged for temporal analysis

---

### 3. `no._of_cases`

**Description:** Number of confirmed infectious disease cases reported to MOH for that specific disease during that epidemiological week

**Data Type:** Integer

**Range:** 0 to 1,791 (max observed for Dengue Fever in peak outbreak)

**Statistics by Disease Category:**

| Disease | Mean Weekly Cases | Std Dev | Min | Max | Total Cases |
|---------|-------------------|---------|-----|-----|-------------|
| Dengue Fever | 269.4 | 297.2 | 8 | 1,791 | 126,642 |
| HFMD (2017-2020) | 353.7 | 280.3 | 26 | 1,249 | 73,927 |
| Hand, Foot Mouth Disease (2012-2016) | 618.7 | 333.5 | 46 | 1,682 | 161,482 |
| Salmonellosis | 35.1 | 11.4 | 9 | 80 | 16,497 |
| Mumps | 9.0 | 3.5 | 0 | 19 | 4,213 |

**Zero Cases:** Many diseases report 0 cases in most weeks (e.g., rare diseases like Yellow Fever, SARS, Ebola)

**Interpretation:**
- Weekly aggregate (not daily breakdown)
- Confirmed cases only (not suspected or probable)
- Resident population (citizens and permanent residents)
- Includes both public and private healthcare facilities

**Outbreak Definition:** Case count significantly above historical baseline for that disease and season

---

## Data Quality Assessment

### Completeness
✅ **100% complete** - No missing values in any column  
✅ All 470 weeks have data for all 45 diseases

### Consistency
✅ **Consistent format** - Epi-week format standardized throughout  
⚠️ **Disease naming** - Some diseases renamed over time (HFMD vs Hand, Foot Mouth Disease)  
✅ **Non-negative values** - All case counts are ≥ 0

### Accuracy
✅ **Official source** - Data from Ministry of Health Singapore  
✅ **Validated reporting** - Notifiable diseases have mandatory reporting requirements

### Timeliness
⚠️ **Historical data only** - Last update: 2020 (no 2021+ data available in this dataset)  
✅ **No backfilling gaps** - Weekly reporting maintained consistently

---

## Usage Guidelines

### Temporal Analysis
**Seasonality Detection:**
```python
# Filter single disease
dengue = df[df['disease'] == 'Dengue Fever'].copy()

# Convert to datetime
dengue['date'] = pd.to_datetime(dengue['epi_week'] + '-0', format='%Y-W%W-%w')

# Time series analysis
from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(dengue.set_index('date')['no._of_cases'], model='additive', period=52)
```

### Disease Merging
**Combine HFMD variants:**
```python
# Create unified HFMD category
df['disease_clean'] = df['disease'].replace({
    'Hand, Foot Mouth Disease': 'HFMD (Combined)',
    'HFMD': 'HFMD (Combined)'
})
```

### Outbreak Detection
**Identify weeks with unusually high cases:**
```python
# Calculate rolling mean and std
df_disease = df[df['disease'] == 'Dengue Fever'].copy()
df_disease['rolling_mean'] = df_disease['no._of_cases'].rolling(window=12).mean()
df_disease['rolling_std'] = df_disease['no._of_cases'].rolling(window=12).std()

# Flag outbreaks (>2 std dev above mean)
df_disease['outbreak'] = df_disease['no._of_cases'] > (df_disease['rolling_mean'] + 2 * df_disease['rolling_std'])
```

---

## Related Tables & Data Sources

### Complementary Data (Not in current dataset):
- Weather data (temperature, rainfall) - for correlation analysis
- Population demographics - for rate calculations
- Healthcare capacity metrics - for resource planning
- Intervention timelines - for impact evaluation

### Future Data Integration:
- Real-time surveillance feeds (if available)
- Regional/district breakdowns (if MOH releases)
- Hospitalization rates (severity indicators)
- Vaccination coverage data

---

## Business Context

### Primary Use Cases:
1. **Seasonal Pattern Identification** - Determine when diseases peak
2. **Outbreak Forecasting** - Predict future case volumes 8-12 weeks ahead
3. **Disease Burden Assessment** - Prioritize resources by disease impact
4. **Resource Optimization** - Allocate staff/supplies based on forecasts

### Key Stakeholders:
- MOH Policy Makers (budget allocation)
- Healthcare Facility Committees (operational planning)
- Public Health Surveillance Teams (outbreak response)

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-02-09 | Initial data dictionary created | Data Team |
| 2020-04-20 | Dataset last updated (source) | MOH Singapore |

---

## References

- **Data Source:** Kaggle Dataset - `subhamjain/health-dataset-complete-singapore`
- **Original Source:** Ministry of Health Singapore (data.gov.sg)
- **MOH Infectious Disease Surveillance:** https://www.moh.gov.sg/diseases-updates
- **ISO Week Date System:** https://en.wikipedia.org/wiki/ISO_week_date

---

**Document Owner:** Data Analytics Team  
**Contact:** [project-team@moh.gov.sg]  
**Last Reviewed:** 9 February 2026  
**Next Review:** Quarterly or upon data updates
