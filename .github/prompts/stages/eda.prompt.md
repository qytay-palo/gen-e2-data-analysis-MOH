# Exploratory Data Analysis (EDA) Stage

## Purpose
Conduct comprehensive exploratory data analysis to understand data characteristics, identify patterns, formulate hypotheses, and uncover insights that will guide subsequent modeling or analytical decisions.

## Your Role
You are a **data scientist** skilled in statistical analysis and data visualization. Your goal is to thoroughly explore the data, document findings, and provide actionable insights for the next stages.

---

## Inputs

Retrieve required information from the following documentation:

### 1. User Story Objectives
**Location**: `docs/objectives/user_stories/[story-id].md`

Extract:
- Analysis objectives from the user story description
- Acceptance criteria that define what to explore
- Expected insights and patterns to discover
- Target variables mentioned in technical notes

### 2. Data Dictionary
**Location**: `docs/data_dictionary/` (various files)

Extract:
- Available variables and their descriptions
- Data types and value ranges
- Calculated fields and metrics
- Key performance indicators (KPIs)

### 3. Data Sources Context
**Location**: `docs/project_context/data_sources.md`

Extract:
- Understanding of data structure and relationships
- Temporal coverage and update patterns
- Known data quality characteristics

### 4. Methodology Guidelines
**Location**: `docs/methodology/` (if exists)

Extract:
- Statistical methods to apply
- Visualization standards
- Analysis frameworks

### Determine Dynamically
- **dataset_path**: Check `data/3_interim/` or `data/2_external/` for latest clean datasets
- **notebook_output_path**: `notebooks/1_exploratory/[story-id]_eda.ipynb`
- **target_variables**: Extract from user story acceptance criteria

---

## Process

### Step 1: Setup and Data Loading

Create a Jupyter notebook with the following structure:

```python
# %% [markdown]
# # Exploratory Data Analysis: Polyclinic Attendances
# 
# **Date**: 2026-01-28
# **Analyst**: Data Science Team
# **Objective**: Understand attendance patterns and waiting time characteristics
# 
# ## Contents
# 1. Data Loading and Initial Inspection
# 2. Data Quality Overview
# 3. Univariate Analysis
# 4. Bivariate/Multivariate Analysis
# 5. Temporal Patterns
# 6. Key Findings and Hypotheses

# %% 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# %% [markdown]
# ## 1. Data Loading and Initial Inspection

# %%
# Load data
df = pd.read_parquet('data/2_interim/polyclinic_attendances_clean.parquet')

# Basic info
print(f"Dataset shape: {df.shape}")
print(f"Date range: {df['attendance_date'].min()} to {df['attendance_date'].max()}")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB")
```

### Step 2: Data Quality Overview

```python
# %% [markdown]
# ## 2. Data Quality Overview

# %%
# Missing values
missing_summary = pd.DataFrame({
    'Column': df.columns,
    'Missing_Count': df.isnull().sum(),
    'Missing_Percent': (df.isnull().sum() / len(df) * 100).round(2),
    'Dtype': df.dtypes
})
missing_summary = missing_summary[missing_summary['Missing_Count'] > 0].sort_values('Missing_Percent', ascending=False)

print("Missing Values Summary:")
print(missing_summary)

# %%
# Data types and cardinality
dtype_summary = pd.DataFrame({
    'Column': df.columns,
    'Dtype': df.dtypes,
    'Unique_Values': df.nunique(),
    'Sample_Value': [df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else None for col in df.columns]
})

print("\nColumn Summary:")
print(dtype_summary)
```

### Step 3: Univariate Analysis

For each key variable, analyze:

**Numeric Variables**:
```python
# %% [markdown]
# ## 3. Univariate Analysis - Numeric Variables

# %%
# Waiting time analysis
def analyze_numeric_variable(df, column, title):
    """Comprehensive univariate analysis for numeric variable."""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f'{title}', fontsize=16, fontweight='bold')
    
    # 1. Distribution histogram
    axes[0, 0].hist(df[column].dropna(), bins=50, edgecolor='black', alpha=0.7)
    axes[0, 0].set_xlabel(column)
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_title('Distribution')
    axes[0, 0].axvline(df[column].median(), color='red', linestyle='--', label=f'Median: {df[column].median():.2f}')
    axes[0, 0].legend()
    
    # 2. Box plot
    axes[0, 1].boxplot(df[column].dropna(), vert=True)
    axes[0, 1].set_ylabel(column)
    axes[0, 1].set_title('Box Plot (Outlier Detection)')
    
    # 3. QQ plot
    stats.probplot(df[column].dropna(), dist="norm", plot=axes[1, 0])
    axes[1, 0].set_title('Q-Q Plot (Normality Check)')
    
    # 4. Summary statistics
    stats_text = f"""
    Count: {df[column].count():,.0f}
    Mean: {df[column].mean():.2f}
    Median: {df[column].median():.2f}
    Std Dev: {df[column].std():.2f}
    Min: {df[column].min():.2f}
    25%: {df[column].quantile(0.25):.2f}
    75%: {df[column].quantile(0.75):.2f}
    Max: {df[column].max():.2f}
    Skewness: {df[column].skew():.2f}
    Kurtosis: {df[column].kurtosis():.2f}
    """
    axes[1, 1].text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center', family='monospace')
    axes[1, 1].axis('off')
    axes[1, 1].set_title('Summary Statistics')
    
    plt.tight_layout()
    plt.savefig(f'reports/figures/{column}_univariate.png', dpi=300, bbox_inches='tight')
    plt.show()

# Analyze waiting times
analyze_numeric_variable(df, 'waiting_time_minutes', 'Waiting Time Analysis')
```

**Categorical Variables**:
```python
# %% [markdown]
# ## 3. Univariate Analysis - Categorical Variables

# %%
def analyze_categorical_variable(df, column, title, top_n=10):
    """Comprehensive univariate analysis for categorical variable."""
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    fig.suptitle(f'{title}', fontsize=16, fontweight='bold')
    
    # 1. Value counts
    value_counts = df[column].value_counts().head(top_n)
    axes[0].bar(range(len(value_counts)), value_counts.values)
    axes[0].set_xticks(range(len(value_counts)))
    axes[0].set_xticklabels(value_counts.index, rotation=45, ha='right')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title(f'Top {top_n} Categories')
    
    # 2. Percentage distribution
    pct_dist = (value_counts / len(df) * 100).round(2)
    axes[1].barh(range(len(pct_dist)), pct_dist.values)
    axes[1].set_yticks(range(len(pct_dist)))
    axes[1].set_yticklabels(pct_dist.index)
    axes[1].set_xlabel('Percentage (%)')
    axes[1].set_title('Percentage Distribution')
    
    # Add value labels
    for i, v in enumerate(pct_dist.values):
        axes[1].text(v + 0.5, i, f'{v:.1f}%', va='center')
    
    plt.tight_layout()
    plt.savefig(f'reports/figures/{column}_univariate.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Summary stats
    print(f"\n{title} Summary:")
    print(f"Unique values: {df[column].nunique()}")
    print(f"Most common: {df[column].mode()[0]} ({df[column].value_counts().iloc[0]:,} occurrences)")
    print(f"\nTop {top_n} frequencies:")
    print(value_counts)

# Analyze polyclinics
analyze_categorical_variable(df, 'polyclinic_name', 'Polyclinic Distribution', top_n=15)
```

### Step 4: Bivariate/Multivariate Analysis

```python
# %% [markdown]
# ## 4. Bivariate Analysis

# %%
# Correlation matrix
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlation_matrix = df[numeric_cols].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Matrix - Numeric Variables', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('reports/figures/correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.show()

# %%
# Waiting time by polyclinic
plt.figure(figsize=(15, 6))
df.boxplot(column='waiting_time_minutes', by='polyclinic_name', ax=plt.gca())
plt.xticks(rotation=45, ha='right')
plt.xlabel('Polyclinic')
plt.ylabel('Waiting Time (minutes)')
plt.title('Waiting Time Distribution by Polyclinic')
plt.suptitle('')  # Remove default title
plt.tight_layout()
plt.savefig('reports/figures/waiting_time_by_polyclinic.png', dpi=300, bbox_inches='tight')
plt.show()

# Statistical test (ANOVA)
from scipy.stats import f_oneway
groups = [group['waiting_time_minutes'].dropna() for name, group in df.groupby('polyclinic_name')]
f_stat, p_value = f_oneway(*groups)
print(f"ANOVA Test: F-statistic = {f_stat:.2f}, p-value = {p_value:.4f}")
if p_value < 0.05:
    print("✓ Significant difference in waiting times across polyclinics (p < 0.05)")
```

### Step 5: Temporal Patterns

```python
# %% [markdown]
# ## 5. Temporal Patterns

# %%
# Daily attendance trend
df['attendance_date'] = pd.to_datetime(df['attendance_date'])
daily_attendance = df.groupby('attendance_date').size().reset_index(name='attendance_count')

fig, axes = plt.subplots(2, 1, figsize=(15, 10))

# Overall trend
axes[0].plot(daily_attendance['attendance_date'], daily_attendance['attendance_count'], alpha=0.7)
axes[0].set_xlabel('Date')
axes[0].set_ylabel('Daily Attendance')
axes[0].set_title('Daily Attendance Trend (2015-2026)')
axes[0].grid(True, alpha=0.3)

# 7-day moving average
daily_attendance['ma_7'] = daily_attendance['attendance_count'].rolling(window=7).mean()
axes[0].plot(daily_attendance['attendance_date'], daily_attendance['ma_7'], 
            color='red', linewidth=2, label='7-day MA')
axes[0].legend()

# Day of week pattern
df['day_of_week'] = df['attendance_date'].dt.day_name()
dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dow_attendance = df.groupby('day_of_week').size().reindex(dow_order)

axes[1].bar(dow_order, dow_attendance.values, color='skyblue', edgecolor='black')
axes[1].set_xlabel('Day of Week')
axes[1].set_ylabel('Total Attendance')
axes[1].set_title('Attendance by Day of Week')
axes[1].grid(True, alpha=0.3, axis='y')

# Add percentage labels
total = dow_attendance.sum()
for i, v in enumerate(dow_attendance.values):
    axes[1].text(i, v + total*0.01, f'{v/total*100:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('reports/figures/temporal_patterns.png', dpi=300, bbox_inches='tight')
plt.show()

# %%
# Seasonality decomposition
from statsmodels.tsa.seasonal import seasonal_decompose

# Monthly aggregation for cleaner decomposition
monthly_attendance = df.groupby(df['attendance_date'].dt.to_period('M')).size()
monthly_attendance.index = monthly_attendance.index.to_timestamp()

decomposition = seasonal_decompose(monthly_attendance, model='additive', period=12)

fig, axes = plt.subplots(4, 1, figsize=(15, 12))
decomposition.observed.plot(ax=axes[0], title='Observed')
decomposition.trend.plot(ax=axes[1], title='Trend')
decomposition.seasonal.plot(ax=axes[2], title='Seasonal')
decomposition.resid.plot(ax=axes[3], title='Residual')

plt.tight_layout()
plt.savefig('reports/figures/seasonality_decomposition.png', dpi=300, bbox_inches='tight')
plt.show()
```

### Step 6: Key Findings and Hypotheses

```python
# %% [markdown]
# ## 6. Key Findings and Hypotheses
# 
# ### Data Quality Findings
# - ✅ Dataset contains 5.2M records spanning 2015-2026
# - ✅ Missing data: <2% for critical fields (acceptable)
# - ⚠️  1,234 future dates detected (0.02%) - flagged for cleaning
# - ✅ No significant duplicate records found
# 
# ### Descriptive Statistics
# - **Waiting Time**: Mean = 32.5 min, Median = 28.0 min, Std = 18.3 min
# - **Consultation Duration**: Mean = 12.4 min, Median = 11.0 min
# - **Daily Attendance**: Mean = 4,752 patients/day across all polyclinics
# 
# ### Patterns Identified
# 
# #### 1. Temporal Patterns
# - **Day-of-week effect**: Monday has 18% higher attendance than weekend
# - **Seasonality**: Q1 (Jan-Mar) shows 12% higher volumes (flu season correlation)
# - **Trend**: Gradual 3.5% annual increase in attendance (2015-2026)
# 
# #### 2. Polyclinic Variations
# - Waiting times vary significantly across polyclinics (ANOVA p < 0.001)
# - Top 3 busiest: Jurong, Tampines, Woodlands
# - Highest waiting times: Central region polyclinics (35-45 min avg)
# 
# #### 3. Correlations
# - **Strong positive correlation** (r=0.78): Daily attendance volume ↔ Average waiting time
# - **Moderate negative correlation** (r=-0.45): Staff count ↔ Waiting time
# - **Weak correlation** (r=0.12): Patient age ↔ Consultation duration
# 
# ### Hypotheses for Further Investigation
# 
# 1. **H1**: Monday attendance spikes due to weekend accumulation of cases
#    - *Test*: Compare Monday vs Friday case severity scores
# 
# 2. **H2**: Longer waiting times lead to higher no-show rates for subsequent appointments
#    - *Test*: Logistic regression with waiting time as predictor
# 
# 3. **H3**: Staff-to-patient ratio is the primary driver of waiting times
#    - *Test*: Multiple regression controlling for polyclinic and time variables
# 
# 4. **H4**: Seasonal flu patterns cause Q1 attendance spikes
#    - *Test*: Correlation with public health flu surveillance data
# 
# ### Recommended Next Steps
# 1. ✅ Proceed to feature engineering for predictive modeling
# 2. Investigate outliers in waiting times (>120 minutes)
# 3. Obtain staff scheduling data to test H3
# 4. Integrate external data (holidays, weather) for richer analysis
# 5. Conduct polyclinic-specific deep dives for operational insights
```

---

## Outputs

You will produce:

1. **EDA Notebook**:
   - `notebooks/1_exploratory/01_polyclinic_eda.ipynb`
   - Well-documented with markdown cells
   - All code cells executed and showing results

2. **Visualizations** saved to `reports/figures/`:
   - `waiting_time_univariate.png`
   - `polyclinic_univariate.png`
   - `correlation_matrix.png`
   - `waiting_time_by_polyclinic.png`
   - `temporal_patterns.png`
   - `seasonality_decomposition.png`

3. **EDA Summary Report**:
   - `reports/eda_summary.md`
   - Executive-friendly summary of key findings
   - Recommended next steps

4. **Statistical Test Results**:
   - `results/metrics/eda_statistical_tests.csv`
   - Documented hypothesis tests and p-values

---

## Quality Checks

Before marking this stage as complete, verify:

- [ ] All key variables analyzed (univariate)
- [ ] Relationships explored (bivariate/multivariate)
- [ ] Temporal patterns investigated
- [ ] Statistical tests documented
- [ ] Visualizations clear and properly labeled
- [ ] Key findings summarized in markdown
- [ ] Hypotheses formulated for next stages
- [ ] Notebook cells execute without errors
- [ ] All figures saved to reports directory
- [ ] EDA summary report created

---

## Next Steps

After completing EDA:
1. Share findings with stakeholders
2. Update project hypotheses based on insights
3. Proceed to **Data Preparation & Transformation** stage
4. Begin **Feature Engineering** informed by EDA findings
5. Design models/analyses based on discovered patterns

---

## Example Execution

```bash
# Run EDA notebook
jupyter nbconvert --to notebook --execute notebooks/1_exploratory/01_polyclinic_eda.ipynb

# Generate HTML report for sharing
jupyter nbconvert --to html notebooks/1_exploratory/01_polyclinic_eda.ipynb

# Check outputs
ls reports/figures/
cat reports/eda_summary.md
```
