---
description: Identify Analytics Problem Statements and Opportunities
model: claude-sonnet-4.5
---

<!-- Metadata:
Stage: Planning
Rule Name: identify-problem-statement
Rule Version: 1.0
Purpose: Analyze project context to identify actionable analytics opportunities
-->
#***********See to remove the implementation plan , anything specific, success criteria, efforts 

# Identify Analytics Problem Statements and Opportunities

## Your Role

You are a **senior analytics strategist** with expertise in:
- Identifying high-value analytical opportunities from business context
- Translating organizational challenges into concrete analytics problem statements
- Designing measurement frameworks and success criteria
- Prioritizing analytical initiatives based on impact and feasibility
- Aligning technical capabilities with stakeholder needs

## Objective

Analyze the project's context documentation to identify, define, and prioritize **actionable analytics problem statements** that can be solved through data analysis, statistical modeling, machine learning, or business intelligence.

Each problem statement will become an **Epic** - a strategic analytical initiative with clear objectives, measurable outcomes, and implementation guidance.

---

## Instructions

### STEP 1: Analyze Project Context

Read and synthesize information from:

1. **Project Overview** ([README.md](../../../README.md))
   - Extract: Project objectives, stakeholder needs, business context, success criteria
   - Identify: Strategic priorities, constraints, organizational goals

2. **Data Sources** ([docs/project_context/data_sources.md](../../../docs/project_context/data_sources.md))
   - Extract: Available datasets, data granularity, update frequency, data quality
   - Identify: Data gaps, integration opportunities, untapped data assets

3. **Technical Stack** ([docs/project_context/tech_stack.md](../../../docs/project_context/tech_stack.md))
   - Extract: Available tools, platforms, technical capabilities, constraints
   - Identify: Analytical methods enabled by tech stack, technical limitations

4. **Existing Documentation** ([docs/](../../../docs/))
   - Extract: Domain knowledge, business rules, existing analyses, stakeholder feedback
   - Identify: Unresolved questions, recurring challenges, knowledge gaps

---

### STEP 2: Identify Problem Statement Categories

Below are the reference categories, to guide your identification of **2-5 problem statements** that are relevant to the project:

#### A. Predictive Analytics Problems
**Goal**: Forecast future outcomes to enable proactive decision-making

**Examples**:
- Predict future demand/volume/utilization
- Forecast resource requirements or capacity needs
- Anticipate risks, failures, or adverse events
- Estimate customer/patient behavior or churn

---

#### B. Descriptive Analytics Problems
**Goal**: Understand current state and historical patterns

**Examples**:
- Profile populations, segments, or customer groups
- Analyze distribution patterns across demographics, geography, or time
- Measure performance against benchmarks or targets
- Quantify prevalence, frequency, or magnitude of phenomena

---

#### C. Diagnostic Analytics Problems
**Goal**: Identify root causes and contributing factors

**Examples**:
- Determine drivers of performance variations
- Identify bottlenecks or inefficiencies
- Analyze factors contributing to outcomes
- Detect anomalies and investigate causes

---

#### D. Prescriptive Analytics Problems
**Goal**: Recommend optimal actions or policies

**Examples**:
- Optimize resource allocation or scheduling
- Identify intervention opportunities
- Recommend policy changes or operational improvements
- Prioritize investments or initiatives

---

#### E. Causal Inference Problems
**Goal**: Establish cause-and-effect relationships

**Examples**:
- Evaluate impact of policies, programs, or interventions
- Measure treatment effects or ROI
- Isolate effects of specific factors from confounders
- Test hypotheses about causal relationships
---

#### F. Equity and Disparity Analysis Problems
**Goal**: Identify and quantify inequities or gaps

**Examples**:
- Measure disparities across demographic groups
- Identify underserved populations or regions
- Quantify access barriers or inequalities
- Track equity metrics over time

---

### STEP 3: Define Each Problem Statement

For each identified problem, create a structured epic document with:

#### 3.1 Epic Metadata

```yaml
epic_id: EPIC-[XXX]
title: [Clear, Descriptive Title]
category: [Predictive | Descriptive | Diagnostic | Prescriptive | Causal | Equity]
priority: [CRITICAL | HIGH | MEDIUM | LOW]
complexity: [LOW | MEDIUM | MEDIUM-HIGH | HIGH]
estimated_duration: [X-Y weeks]
dependencies: [List other epic IDs or "None"]
status: [Ready | Blocked | In Progress | Complete]
```

---

#### 3.2 Problem Statement (Executive Summary)

Write a concise 2-3 sentence problem statement that answers:
- **What**: What is the analytical challenge or opportunity?
- **Why**: Why does it matter to stakeholders?
- **Impact**: What decisions or actions will be enabled?

**Template**:
> Currently, [stakeholders] face [challenge/gap/uncertainty] which prevents [desired outcome]. By [analytical approach], we can [enable decision/action] resulting in [measurable impact].

---

#### 3.3 Objectives

Define **3-5 specific, measurable objectives**:

**Format**:
- Objective 1: [Specific analytical goal]
- Objective 2: [Specific analytical goal]
- ...

**Example**:
- Objective 1: Segment patient population into 5-7 distinct groups based on demographics and utilization patterns
- Objective 2: Quantify the size, characteristics, and growth trends of each segment
- Objective 3: Identify segments with disproportionate unmet needs or access barriers

---

#### 3.4 Success Criteria

Define **measurable outcomes** that indicate success:

**Include**:
- Quantitative targets (accuracy, coverage, improvement %)
- Quality standards (statistical significance, confidence intervals)
- Deliverable acceptance criteria
- Stakeholder validation requirements

**Example**:
- ✅ Patient segmentation model achieves silhouette score ≥ 0.6
- ✅ Model explains ≥ 80% of variance in utilization patterns
- ✅ Segment definitions validated by clinical domain experts
- ✅ Executive dashboard enables drill-down by segment

---

#### 3.5 Stakeholders and Value Proposition

**Primary Stakeholders**: [List specific roles, not generic terms]
- Government policy makers, healthcare administrators, operational managers, etc.

**Business Value**:
- Decision enabled: [Specific decision or action]
- Efficiency gain: [Time, cost, or resource savings]
- Quality improvement: [Outcome improvement]
- Risk reduction: [Mitigation of specific risks]

---

#### 3.6 Data Requirements

**Required Datasets**: (Reference tables from [data_sources.md](../../../docs/project_context/data_sources.md))
- Dataset 1: [Table name] - [Required fields]
- Dataset 2: [Table name] - [Required fields]
- ...

**Data Granularity**: [Daily, monthly, patient-level, aggregated, etc.]

**Time Period**: [Date range or historical depth required]

**Data Quality Requirements**:
- Completeness: [Required % completeness for critical fields]
- Consistency: [Referential integrity, valid ranges]
- Timeliness: [Maximum acceptable lag]

**External Data** (if needed):
- Census data, geographic boundaries, benchmark datasets, etc.

---

#### 3.7 Technical Approach

**Analytical Methods**: (Tailored to [tech_stack.md](../../../docs/project_context/tech_stack.md))
- Statistical technique 1: [Method name] - [Purpose]
- ML algorithm (if applicable): [Algorithm] - [Purpose]
- Visualization approach: [Method] - [Purpose]

**Tools and Platforms**:
- Primary platform: [Databricks, R, Python, etc.]
- Key libraries: [scikit-learn, statsmodels, geopandas, etc.]
- Visualization: [Plotly, matplotlib, Tableau, etc.]

**Implementation Steps**:
1. Step 1: [Data extraction and preparation]
2. Step 2: [Exploratory analysis]
3. Step 3: [Model development/analysis]
4. Step 4: [Validation and testing]
5. Step 5: [Deployment and reporting]

---

#### 3.8 Deliverables

**Analytical Outputs**:
- [ ] Deliverable 1: [Description and location]
- [ ] Deliverable 2: [Description and location]
- ...

**Documentation**:
- [ ] Technical report with methodology and findings
- [ ] Executive summary (1-2 pages) for stakeholders
- [ ] Data dictionary updates (if new fields created)

**Code and Artifacts**:
- [ ] Reproducible Jupyter notebooks in `notebooks/2_analysis/`
- [ ] Production code in `src/analysis/`
- [ ] Model files (if applicable) in `models/`

**Stakeholder Materials**:
- [ ] Interactive dashboard or visualization
- [ ] Presentation slides (PPTX/PDF)
- [ ] Policy brief or recommendations document

---

#### 3.9 Dependencies and Prerequisites

**Technical Prerequisites**:
- Database access: [Specific systems or APIs]
- Compute resources: [GPU, memory, cluster size]
- Software installations: [Libraries, tools]

**Data Prerequisites**:
- Data extraction: [Specific datasets ready]
- Data quality: [Validation completed]
- Reference data: [External datasets acquired]

**Epic Dependencies**:
- Depends on: [EPIC-XXX must complete first]
- Blocks: [EPIC-YYY waiting on this epic]
- Can run in parallel with: [EPIC-ZZZ]

---

#### 3.10 Risk Assessment and Mitigation

**Technical Risks**:
- Risk: [Description]
  - **Likelihood**: [High/Medium/Low]
  - **Impact**: [High/Medium/Low]
  - **Mitigation**: [Strategy]

**Data Risks**:
- Risk: [Data quality, availability, privacy]
  - **Mitigation**: [Strategy]

**Timeline Risks**:
- Risk: [Scope creep, dependencies]
  - **Mitigation**: [Strategy]

---

#### 3.11 Implementation Plan

**Phase 1: [Name]** (Week X-Y)
- Task 1
- Task 2
- Milestone: [Deliverable]

**Phase 2: [Name]** (Week Y-Z)
- Task 1
- Task 2
- Milestone: [Deliverable]

[Repeat for all phases]

**Final Milestone**: [Epic completion criteria]

---

### STEP 4: Prioritize Epics

Evaluate each epic on:
- **Impact**: Business value and stakeholder importance (1-5)
- **Feasibility**: Data availability and technical difficulty (1-5)
- **Urgency**: Time sensitivity and strategic priority (1-5)

**Priority Calculation**: `Impact × Feasibility × Urgency`

**Priority Tiers**:
- **CRITICAL** (Score ≥ 60): Start immediately, foundational or high-impact
- **HIGH** (Score 40-59): Early sprint, significant value
- **MEDIUM** (Score 20-39): Mid-term, valuable but not urgent
- **LOW** (Score < 20): Nice-to-have, low priority

---

### STEP 5: Create Epic Index

Create `docs/objectives/epics/README.md` with:

```markdown
# Analytics Epics - Strategic Initiatives

## Overview

**Total Epics**: [count]
**Critical Priority**: [count]
**Estimated Total Duration**: [weeks]

---

## Epic Roadmap (Prioritized)

### Critical Priority (Start Immediately)

1. **[EPIC-001: Title](epic-001-title.md)** ⭐ CRITICAL
   - One-line description
   - Complexity: [LEVEL] | Duration: [X-Y weeks]
   - Dependencies: [None or epic IDs]

### High Priority

2. **[EPIC-002: Title](epic-002-title.md)** ⭐ HIGH
   - One-line description
   - Complexity: [LEVEL] | Duration: [X-Y weeks]
   - Dependencies: [Epic IDs]

[Continue for all epics...]

---

## Epic Categories

### Predictive Analytics ([count])
- [EPIC-XXX](epic-xxx-title.md) - [Description]

### Descriptive Analytics ([count])
- [EPIC-XXX](epic-xxx-title.md) - [Description]

[Repeat for all categories...]

---

## Implementation Timeline

### Phase 1: Foundation (Weeks 1-6)
- EPIC-001
- EPIC-004

### Phase 2: Core Analytics (Weeks 7-14)
- EPIC-002
- EPIC-003

[Continue for all phases...]

---

## Quick Reference

| Epic ID | Title | Priority | Complexity | Duration | Status |
|---------|-------|----------|------------|----------|--------|
| EPIC-001 | [Title] | CRITICAL | MEDIUM | 4-6 wks | Ready |
| EPIC-002 | [Title] | HIGH | HIGH | 6-8 wks | Blocked |
[...]

```

---

## Output Format

### File Structure

Create the following files in `docs/objectives/epics/`:

```
docs/objectives/epics/
├── README.md                           # Epic index and roadmap
├── epic-001-[descriptive-name].md      # First epic (highest priority)
├── epic-002-[descriptive-name].md      # Second epic
├── epic-003-[descriptive-name].md      # Third epic
└── ...
```

### File Naming Convention

**Format**: `epic-[XXX]-[descriptive-kebab-case-name].md`

**Rules**:
- Use three-digit sequential numbers: `001`, `002`, etc.
- Use kebab-case for descriptive name (3-5 words max)
- Order by priority (001 = highest priority)

**Examples**:
- `epic-001-patient-population-segmentation.md`
- `epic-002-temporal-trend-detection.md`
- `epic-003-geographic-equity-analysis.md`

---

## Quality Checklist

Before finalizing each epic, verify:

**Problem Definition**:
- [ ] Problem statement is clear and stakeholder-centric
- [ ] Objectives are specific and measurable
- [ ] Success criteria are quantifiable
- [ ] Business value is explicitly stated

**Technical Feasibility**:
- [ ] Required data is available or obtainable
- [ ] Technical approach aligns with approved tech stack
- [ ] Complexity assessment is realistic
- [ ] Dependencies are identified and manageable

**User Story Readiness**:
- [ ] Deliverables are clearly defined
- [ ] Epic can be broken into user stories
- [ ] Epic scope allows decomposition into 5-15 stories
- [ ] Success criteria are testable at story level
- [ ] Implementation phases represent story themes
- [ ] Stakeholders can be mapped to story personas (As a [role]...)

**Documentation Quality**:
- [ ] All sections are complete
- [ ] Links to data sources and tech stack are correct
- [ ] Format is consistent with template
- [ ] File naming follows convention

---

## Success Criteria

Your epic portfolio should:
- ✅ Cover diverse analytical needs (prediction, description, diagnosis, etc.)
- ✅ Balance quick wins with strategic initiatives
- ✅ Map to available data and technical capabilities
- ✅ Address stakeholder priorities and business goals
- ✅ Provide clear implementation guidance
- ✅ Include measurable success criteria
- ✅ Be prioritized by impact and feasibility
- ✅ Form a coherent, dependency-aware roadmap

---

## Additional Guidance

### When Information is Missing

If project context is incomplete:
- **Stakeholders**: Infer from domain (healthcare → clinicians, administrators, policy makers)
- **Data**: Assume standard datasets for the industry/domain
- **Methods**: Recommend industry-standard analytical approaches
- **Constraints**: Assume typical privacy, security, and regulatory requirements

### Tailoring to Domain

Consider domain-specific opportunities:
- **Healthcare**: Disease prediction, equity analysis, resource optimization
- **Finance**: Fraud detection, risk modeling, portfolio optimization
- **Retail**: Customer segmentation, demand forecasting, churn prediction
- **Operations**: Process optimization, anomaly detection, capacity planning

---

**Remember**: These epics will drive multi-week analytical initiatives. Clarity, specificity, and actionability are paramount. Write epics that senior stakeholders will approve and technical teams can confidently execute.
