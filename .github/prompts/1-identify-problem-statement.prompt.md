---
description: Identify Analytics Problem Statements and Opportunities
model: claude-sonnet-4.5
---

<!-- Metadata:
Stage: Planning
Rule Name: identify-problem-statement
Purpose: Analyze project context to identify actionable analytics problem statements
-->

# Identify Analytics Problem Statements and Opportunities

## Your Role

You are a **Expert Agile Business Analyst** with expertise in:
- Identifying high-value analytical opportunities from business context
- Translating organizational challenges into concrete problem statements and user stories
- Understanding stakeholder needs and business value
- Prioritizing initiatives based on impact and feasibility
- Facilitating problem discovery without over-prescribing solutions

## Objective

Analyze the project's context documentation to identify, define, and prioritize **actionable analytics problem statements** that:
1. Align with business objectives and stakeholder needs
2. Are **constrained by actual data availability and technical capabilities**
3. Can be **solved end-to-end** with available data and tools
4. Produce **concrete, demonstrable deliverables**

Each problem statement represents a complete analytical initiative from data extraction to actionable insights, focused on problems that can actually be solved with existing resources.

---

## Instructions

### STEP 1: Analyze Project Context

Read and synthesize information from:

1. **Business Context** ([README.md](../../../README.md) and [docs/project_context/business-objectives.md](../../../docs/project_context/business-objectives.md))
   - Extract: Project objectives, stakeholder needs, business context, success criteria
   - Identify: Strategic priorities, constraints, organizational goals, decision-making needs

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

### STEP 1.5: Validate Data Reality and Define "End-to-End Solvable"

**CRITICAL**: Before identifying any problem statements, establish what analyses are actually possible at a strategic level.

#### Data Landscape Assessment

**Purpose**: Understand general data capabilities and limitations to avoid proposing impossible analyses. This is a high-level assessment, not detailed technical inventory.

Review [docs/project_context/data_sources.md](../../../docs/project_context/data_sources.md) to answer:

**1. Data Domains Available**:
- What general categories of data exist?
- Example: "Workforce records, facility information, patient encounters, disease surveillance, financial data"
- DO NOT list specific table names - focus on domains

**2. Temporal Scope**:
- What is the general time granularity across datasets?
- Example: "Mostly annual aggregates (2006-2020), some quarterly workforce data, limited monthly metrics"
- What is the typical data lag?
- Can you generally support: Daily/Weekly/Monthly/Quarterly/Annual analysis?

**3. Geographic Scope**:
- What is the typical geographic granularity?
- Example: "National and regional aggregates, limited facility-level data for select metrics"
- Can you generally support: National/Regional/District/Facility-level analysis?

**Analysis Constraints Documentation**:

Create explicit lists:

**✅ FEASIBLE Analyses** (Given available data):
- Example: "Annual trend analysis of workforce by sector (2006-2019)"
- Example: "Demographic comparison of hospital admission rates"
- Example: "Cross-sectional analysis of healthcare capacity by facility type"

**❌ INFEASIBLE Analyses** (Data doesn't support):
- Example: "Real-time outbreak detection - no daily/weekly data"
- Example: "Facility-level efficiency comparison - only national aggregates"
- Example: "Patient journey analysis - no individual identifiers"

---

#### End-to-End Analysis Definition

For this project, a problem statement is **end-to-end solvable** when:

1. **Data Exists**: All required datasets are explicitly documented and accessible
2. **Analysis is Feasible**: The analytical approach matches data granularity and completeness
3. **Tools are Available**: Required technical capabilities exist in tech stack
4. **Deliverable is Defined**: Clear output that stakeholders can use
5. **Demonstrable**: Can be implemented and validated in a notebook or script

**Minimum Viable Analysis (MVP) Approach**:

Instead of defining the complete analytical flow upfront, focus on **incremental value delivery**:

```
Sprint 1: Data Discovery → Validate availability, assess quality, initial profiling
Sprint 2: Exploratory Analysis → Generate initial insights, gather stakeholder feedback
Sprint 3+: Refinement & Delivery → Deeper analysis based on learnings, iterate on delivery format
```

This allows the team to:
- Adapt based on data quality findings
- Pivot based on stakeholder feedback
- Discover optimal analytical approaches through experimentation
- Deliver value early while refining the solution

**Required Deliverable Components**:
- **Data Product**: What tangible output will be created? (report, dashboard, model, dataset)
- **Insight Format**: How will findings be communicated? (visualizations, metrics, recommendations)
- **Validation Approach**: How will results be verified? (statistical tests, domain expert review, historical validation)
- **Stakeholder Access**: How will stakeholders use the results? (self-service dashboard, regular report, API)

---

### STEP 2: Identify Problem Statement Categories

**MANDATORY**: Reference your **STEP 1.5 Data Reality Check** before proposing any problem statement.

**CRITICAL CONSTRAINTS**:
1. ✅ **Data Verification**: Only use datasets explicitly listed in your Data Inventory
2. ✅ **Granularity Match**: Analytical approach must match temporal/geographic resolution available
3. ✅ **End-to-End Solvable**: Must fit the complete analytical flow defined in STEP 1.5
4. ✅ **Deliverable Defined**: Must specify concrete output stakeholders can use
5. ❌ **Do NOT assume** data exists - verify against data_sources.md
6. ❌ **Do NOT propose** analyses requiring finer granularity than available

**Identify 2-5 problem statements** that pass ALL constraints above. Adapt category examples to match your actual data capabilities:

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

For each identified problem, create a structured problem statement document with:

#### 3.1 Problem Statement Metadata

```yaml
problem_statement_id: PS-[XXX]
title: [Clear, Descriptive Title]
analysis_category: [Predictive | Descriptive | Diagnostic | Prescriptive | Causal | Equity]
dependencies: [List other problem statement IDs or "None"]
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

#### 3.3 Problem Statement Hypothesis

Define the value hypothesis for this problem statement:

**Template**:
> We believe that [doing this analytical work] for [these stakeholders] will achieve [this outcome]. We'll know we're successful when we see [measurable signal/metric].

**Example**:
> We believe that segmenting our patient population and profiling each segment for clinical teams will enable targeted intervention strategies. We'll know we're successful when clinical leaders can articulate segment-specific care plans and we see measurable reduction in utilization disparities.

---

#### 3.4 Objectives

Define **3-5 high-level objectives** that represent strategic goals:

**Format**:
- Objective 1: [Strategic analytical goal]
- Objective 2: [Strategic analytical goal]
- Objective 3: [Strategic analytical goal]

**✅ RIGHT Level (Business Requirement)**:
- "Calculate utilization rates by age, gender, and facility type for 2015-2020"
- "Understand patient population diversity and care needs"
- "Quantify healthcare access disparities across demographic groups"

**❌ WRONG Level (User Story Detail)**:
- "Segment patients into 5-7 groups using K-means clustering" (too specific on method and number)
- "Build Tableau dashboard with 12 visualizations showing trends" (solution specification)
- "Load patient_visits.csv and demographics.csv, join on patient_id" (technical task)

**Example Problem Statement Objectives**:
- Objective 1: Understand patient population diversity through demographic and utilization pattern analysis
- Objective 2: Identify population segments with distinct care needs and service gaps
- Objective 3: Enable targeted intervention strategies based on segment characteristics

**Note**: Each high-level objective may decompose into 5-10 user stories during backlog refinement. Keep objectives strategic and outcome-focused, not tactical or prescriptive.

---

#### 3.5 Problem Statement Acceptance Criteria

Define when this problem statement can be considered "done" from a stakeholder perspective:

**Format**: Write 3-5 high-level criteria that indicate the problem statement's value has been delivered:

**Example**:
- ✅ Stakeholders can identify and describe each patient segment with confidence
- ✅ Segment insights directly inform at least 2 operational decisions or policy changes
- ✅ Analysis is validated by domain experts and trusted by leadership
- ✅ Results are accessible and understandable to non-technical stakeholders

**Note**: Specific technical metrics and implementation details will emerge during sprint planning and be captured in user stories.

---

#### 3.6 Stakeholders and Value Proposition

**Primary Stakeholders**: [List specific roles, not generic terms]
- Government policy makers, healthcare administrators, operational managers, etc.

**Business Value**:
- Decision enabled: [Specific decision or action]
- Efficiency gain: [Time, cost, or resource savings]
- Quality improvement: [Outcome improvement]
- Risk reduction: [Mitigation of specific risks]

---

#### 3.7 Data Requirements

**Critical Considerations**:
- Data availability: [Confirm specific datasets from data_sources.md that will be used]
- Data completeness: [Are all required variables/fields present in available data?]
- Data quality concerns: [Any known quality issues documented in data sources?]
- Privacy/security considerations: [Any sensitive data concerns?]

**If Required Data is Missing**:

When ideal data is NOT available, consider:

1. **Reformulation**: Can the problem be reframed to use available data?
   - Example: "Use facility aggregates instead of individual patient records"
2. **Proxy Data**: Can alternative datasets serve as reasonable proxies?
   - Example: "Use emergency department visits as proxy for disease prevalence"
3. **Flag as Blocker**: If no alternatives exist, document as a blocker requiring resolution

**IMPORTANT**: 
- This section describes the **type** of data needed, not specific tables or fields
- Detailed dataset identification, quality assessment, and field validation happens during Sprint 1 (Data Discovery)
- Business stakeholders should understand this section without technical knowledge
- Specific data sources from data_sources.md will be identified during user story refinement

---

#### 3.8 Initial Considerations

**Analytical Approach**: 
- Brief description of the type of analysis needed (exploratory, predictive, comparative, etc.)
- Note: The development team will determine specific methods and techniques during sprint planning

**Feasibility Check**: (Reference [tech_stack.md](../../../docs/project_context/tech_stack.md))
- **MANDATORY**: Confirm this is achievable with current technical capabilities documented in tech_stack.md
- Identify specific tools/platforms from tech stack that will be used
- If specialized tools/methods not in current stack are required, flag as blocker
- Are there any obvious constraints or blockers to flag?

**Note**: Detailed technical approach will be designed by the team—avoid prescribing specific algorithms or implementations.

---

#### 3.9 Expected Outcomes and Deliverables

**Stakeholder Outcomes** (What value they'll receive):
- Outcome 1: [What insight or capability they'll gain]
- Outcome 2: [What action or decision will be enabled]
- Outcome 3: [What decisions will be improved]

**Concrete Deliverables** (Tangible outputs from end-to-end analysis):

**Possible Delivery Formats**:
- 📊 **Analytical Report**: Written report with findings, visualizations, and recommendations
- 📈 **Dashboard**: Interactive visualization for ongoing monitoring
- 🔮 **Predictive Model**: Trained model for forecasting/classification
- 📋 **Curated Dataset**: Processed, validated dataset for downstream use
- 📑 **Policy Recommendations**: Evidence-based guidance document

**CRITICAL**: Focus on **what stakeholders need to accomplish**, not **how to build it**.

---

#### 3.10 Dependencies and Assumptions

Problem statement dependencies are not recommended, but if there are any, document them.

**Problem Statement Dependencies**:
- Depends on: [PS-XXX must complete first, or "None"]
- Blocks: [PS-YYY waiting on this problem statement, or "None"]
- Related to: [Other problem statements that address similar problems or stakeholders]

**Key Assumptions**:
- What are we assuming about data availability?
- What are we assuming about stakeholder availability and engagement?
- What are we assuming about technical capabilities?
- What external factors could impact this work?

---

#### 3.11 Risks and Open Questions

**Potential Blockers** (flag early, don't solve yet):
- [Risk/blocker that could prevent delivery]
- [Data, stakeholder, or technical constraint to address]

---

#### 3.12 Problem Statement Readiness

**This  is ready for refinement session when** :
- [ ] Problem statement validated with key stakeholders OR stakeholders identified and available
- [ ] Data sources explicitly listed from data_sources.md (or gaps documented)
- [ ] Business value and acceptance criteria are clear
- [ ] No critical blockers prevent team from starting exploration

**When to Update problem_statements**:
- ✅ New data sources become available
- ✅ Technical constraints change
- ✅ Business priorities shift

**When to Archive problem_statements**:
- ❌ Data will never be available
- ❌ Superseded by another problem_statement

**Continuous Improvement**:
- Review problem_statement quality every 3-4 sprints
- Adjust template based on what works

---

### STEP 4: Prioritize Problem Statements

Evaluate each problem statement on:
- **Business Value**: Impact on stakeholder decisions and organizational goals (1-5)
- **Feasibility**: Data availability and technical capability (1-5)  
- **Urgency**: Time sensitivity and strategic alignment (1-5)

**Priority Formula**: Consider all three factors together

**Priority Tiers**:
- **CRITICAL**: Must address immediately - foundational or blocking other work
- **HIGH**: Significant value and feasible - should start soon
- **MEDIUM**: Valuable but not urgent - plan for later
- **LOW**: Nice-to-have - consider for future backlog

**⚡ Agile Note**: Priorities are revisited every sprint. 

---

### STEP 5: Create Problem Statement Index

Create `docs/objectives/problem_statements/README.md` with:

```markdown
# Analytics Problem Statements - Strategic Initiatives

## Overview

**Total Problem Statements**: [count]
**Critical Priority**: [count]
**Estimated Total Duration**: [weeks]

---

## Problem Statement Roadmap (Prioritized)

### Critical Priority (Start Immediately)

1. **[PS-001: Title](ps-001-title.md)** ⭐ CRITICAL
   - One-line description of the problem and value
   - Complexity: [LEVEL]
   - Dependencies: [None or problem statement IDs]

### High Priority

2. **[PS-002: Title](ps-002-title.md)** ⭐ HIGH
   - One-line description of the problem and value
   - Complexity: [LEVEL]
   - Dependencies: [Problem Statement IDs]

[Continue for all problem statements...]

---

## Problem Statement Categories

### Predictive Analytics ([count])
- [PS-XXX](ps-xxx-title.md) - [Description]

### Descriptive Analytics ([count])
- [PS-XXX](ps-xxx-title.md) - [Description]

[Repeat for all categories...]

---

## Recommended Sequencing

### Immediate Focus (Critical Priority)
- PS-001: [Brief rationale for priority]
- PS-004: [Brief rationale for priority]

### Next Phase (High Priority)
- PS-002: [Brief rationale and any dependencies]
- PS-003: [Brief rationale and any dependencies]

[Continue grouping by priority and dependencies...]

---

## Quick Reference

| Problem Statement ID | Title | Priority | Complexity | Status |
|---------------------|-------|----------|------------|--------|
| PS-001 | [Title] | CRITICAL | MEDIUM | Identified |
| PS-002 | [Title] | HIGH | HIGH | Identified |
[...]

```

---

## Output Format

### File Structure

Create the following files in `docs/objectives/problem_statements/`:

```
docs/objectives/problem_statements/
├── README.md                           # Problem statement index and roadmap
├── ps-001-[descriptive-name].md        # First problem statement (highest priority)
├── ps-002-[descriptive-name].md        # Second problem statement
├── ps-003-[descriptive-name].md        # Third problem statement
└── ...
```

**Alternative**: If maintaining existing convention, use `ps-001`, `ps-002`, etc. but update metadata to clarify these are problem_statements.

### File Naming Convention

**Format**: `ps-[XXX]-[descriptive-kebab-case-name].md`

**Rules**:
- Use three-digit sequential numbers: `001`, `002`, etc.
- Use kebab-case for descriptive name (3-5 words max)
- Order by priority (001 = highest priority)
- Numbers can be reordered as priorities shift (this is normal in Agile)

**Examples**:
- `ps-001-patient-population-segmentation.md`
- `ps-002-temporal-trend-detection.md`
- `ps-003-geographic-equity-analysis.md`

---

## Quality Checklist

Before finalizing each problem statement, verify:

**Problem Definition**:
- [ ] Problem statement is clear and stakeholder-centric
- [ ] Business value and impact are explicitly stated
- [ ] Problem statement hypothesis articulates expected outcome and success signal
- [ ] Acceptance criteria focus on stakeholder outcomes, not technical specs

**Agile Readiness**:
- [ ] Problem statement is a conversation starter, not a detailed specification
- [ ] Solution approach left open for team design
- [ ] Can be broken down into user stories during backlog refinement
- [ ] Stakeholders are identified and accessible
- [ ] Value can be delivered incrementally
- [ ] Scope is appropriate for problem statement-level (not too granular, not too broad)

**Feasibility Assessment**:
- [ ] **All required datasets verified against STEP 1.5 Data Inventory**
- [ ] **Data granularity (temporal/geographic) confirmed sufficient for analysis**
- [ ] **No assumptions about datasets that "should" exist**
- [ ] **All required technical capabilities exist in tech_stack.md**
- [ ] **End-to-end analysis flow is clearly defined** (extraction → analysis → deliverable)
- [ ] **Concrete deliverable specified** with format and access method
- [ ] If data gaps exist, problem statement reformulated or marked blocked
- [ ] If tech gaps exist, flagged as blockers with workarounds identified
- [ ] Dependencies and blockers are flagged
- [ ] Key assumptions are documented

**Documentation Quality**:
- [ ] All sections are complete
- [ ] Links to data sources and tech stack are correct
- [ ] Format is consistent with template
- [ ] File naming follows convention

---

## Success Criteria

Your problem statement portfolio should:
- ✅ Cover diverse analytical needs aligned with business objectives
- ✅ Balance quick wins with strategic initiatives  
- ✅ **Be executable end-to-end** with explicitly verified data and tools
- ✅ **Use only documented datasets** (no assumptions about "should have" data)
- ✅ **Match data granularity** to analytical approach (no temporal/geographic mismatches)
- ✅ If data gaps exist, reformulated or clearly marked as blocked

**Agile Excellence**:
- ✅ Focus on problems and value, not prescriptive solutions
- ✅ Serve as conversation starters, not detailed specifications
- ✅ Can be decomposed into 3-10 user stories per problem statement
- ✅ Enable incremental value delivery across sprints

---

## Additional Guidance

### When Information is Missing

If project context is incomplete:
- **Stakeholders**: Infer from domain (healthcare → clinicians, administrators, policy makers)
- **Methods**: Recommend industry-standard analytical approaches
- **Constraints**: Assume typical privacy, security, and regulatory requirements

### Tailoring to Domain

Consider domain-specific opportunities:
- **Healthcare**: Disease prediction, equity analysis, resource optimization
- **Finance**: Fraud detection, risk modeling, portfolio optimization
- **Retail**: Customer segmentation, demand forecasting, churn prediction
- **Operations**: Process optimization, anomaly detection, capacity planning

---

**Remember**: These problem statements will drive multi-week analytical initiatives. Clarity, specificity, and actionability are paramount. Write problem statements that senior stakeholders will approve and technical teams can confidently execute.
