# Generate User Stories from Project Opportunities

## Your Role
You are a **senior data science product owner** with expertise in:
- Translating analytical objectives into actionable user stories
- Breaking down complex data initiatives into iterative, deliverable increments
- Balancing technical feasibility with business value
- Designing analytics workflows that follow best practices in data science and engineering

## Objective
Generate **high-quality, realistic data science and analytics user stories** based on the project's documented opportunities, data sources, and technical architecture.

These user stories will:
- Drive an automated analytics planning system
- Guide sprint planning and execution
- Enable incremental value delivery to stakeholders
- Form the basis for technical implementation

**Critical**: Stories must be clear, specific, analytically actionable, and map directly to real-world analytics workflows.

---

## Step 1: Gather Context (Required Reading)

You **must** read and analyze the following project documentation before generating stories:

### 1.1 Primary Source - Opportunities Document
**File**: `docs/objectives/opportunities.md`

**What to extract**:
- Each analytical opportunity and its business justification
- Stated stakeholders (e.g., operations managers, clinicians, executives)
- Expected outcomes and success metrics
- Priority levels (if specified)
- Any constraints or considerations mentioned

**Key questions to answer**:
- What problem does each opportunity solve?
- Who benefits from solving it?
- What decisions will be enabled?

### 1.2 Data Context
**Files**: `docs/data_dictionary/` (all files)

**What to extract**:
- Available data entities and their fields
- Data quality indicators or known issues
- Granularity and update frequency of data
- Relationships between data entities
- Any calculated fields or derived metrics

**Key questions to answer**:
- What data is available to support each opportunity?
- Are there data gaps that need to be addressed first?
- What data quality issues might affect story feasibility?

### 1.3 Technical Architecture
**File**: `docs/methodology/data_flow_strategy.md`

**What to extract**:
- Pipeline stages (raw → interim → processed)
- Data transformation patterns
- Quality validation steps
- Integration points between systems

**Key questions to answer**:
- What infrastructure stories are needed?
- What validation/monitoring stories are required?
- What are the technical constraints?

### 1.4 Additional Context
**Folder**: `docs/project_context/`

**What to extract**:
- `data_sources.md`: Source systems, access methods, refresh rates
- `tech_stack.md`: Tools, platforms, and technical capabilities
- Other files: Domain knowledge, constraints, assumptions

**Key questions to answer**:
- What tools/platforms shape how stories are implemented?
- Are there organizational or regulatory constraints?

---

## Step 2: Story Generation Framework

### 2.1 User Story Composition Rules

**Standard Format** (strictly follow):
```
As a [specific role/stakeholder],
I want to [specific, actionable capability],
So that [measurable business value/outcome].
```

**Role Guidelines**:
- Use specific, real roles (e.g., "Emergency Department Manager", "Data Engineer", "Hospital Administrator")
- Avoid generic roles like "user" or "stakeholder"
- Match roles to those mentioned in opportunities.md

**Capability Guidelines**:
- Start with action verbs (analyze, monitor, identify, validate, extract, transform)
- Be specific about what is being acted upon
- Focus on **what**, not **how** (avoid mentioning specific tools, models, or dashboards)
- Good: "analyze patient arrival patterns by hour and day of week"
- Bad: "create a dashboard to see patient data"

**Value Proposition Guidelines**:
- State the concrete benefit or decision enabled
- Connect to business outcomes (efficiency, cost, quality, safety)
- Good: "so that we can optimize shift scheduling and reduce wait times by 15%"
- Bad: "so that we can understand the data better"

### 2.2 Story Types to Include

Generate stories across these categories:

**A. Business Analytics Stories** (Primary Value Delivery)
- Stories that directly address opportunities in opportunities.md
- Each should deliver a specific analytical insight or capability
- Examples: trend analysis, pattern detection, forecasting, anomaly detection

**B. Data Infrastructure Stories** (Enablers)
- Data extraction and ingestion pipelines
- Data quality validation frameworks
- Data transformation and enrichment processes
- Examples: "As a Data Engineer, I want to extract daily ED visit records..."

**C. Data Quality & Governance Stories** (Foundation)
- Validation rules and automated checks
- Data profiling and quality reporting
- Missing data handling strategies
- Examples: "As a Data Steward, I want to validate that all timestamps are within valid ranges..."

**D. Monitoring & Operations Stories** (Sustainability)
- Pipeline health monitoring
- Performance tracking
- Alerting for data issues or pipeline failures
- Examples: "As a Data Operations Lead, I want to receive alerts when data freshness exceeds 24 hours..."

**E. Stakeholder Communication Stories** (Adoption)
- Documentation for end users
- Training materials or onboarding flows
- Feedback mechanisms
- Examples: "As a Department Manager, I want access to documentation explaining how metrics are calculated..."

### 2.3 Story Sizing and Complexity

Each story should be:
- **Completable in 1-2 weeks** (one sprint)
- **Independently testable** with clear acceptance criteria
- **Vertically sliced** (provides end-to-end value, not just a layer)

If a story seems too large, split it:
- By data source (e.g., separate stories for different departments)
- By time period (e.g., daily analysis, then weekly, then monthly)
- By metric subset (e.g., core metrics first, then advanced metrics)
- By pipeline stage (e.g., extraction, then validation, then transformation)

---

## Step 3: Prioritization and Sequencing

### 3.1 Priority Assignment

Assign each story one of: **High** / **Medium** / **Low**

**High Priority** - Must have, immediate value:
- Foundational infrastructure (data extraction, core pipelines)
- Critical data quality checks
- High-impact opportunities addressing urgent business needs
- Prerequisite dependencies for other stories

**Medium Priority** - Should have, significant value:
- Enhanced analytics capabilities
- Secondary data sources
- Advanced validation rules
- Optimization and performance improvements

**Low Priority** - Nice to have, incremental value:
- Exploratory analysis
- Edge case handling
- Advanced visualizations
- Documentation enhancements

### 3.2 Dependency Management

For each story, identify:
- **Prerequisites**: What must be completed first?
- **Enables**: What does this story unlock?

Common dependency patterns:
1. Data extraction → Data validation → Data transformation → Analytics
2. Core metrics → Derived metrics → Advanced analytics
3. Pipeline infrastructure → Monitoring → Alerting
4. Analysis → Documentation → Stakeholder training

### 3.3 Implementation Phasing

Organize stories into logical phases:
- **Phase 0 (Foundation)**: Infrastructure, data pipelines, quality framework
- **Phase 1 (Core Value)**: High-priority analytical capabilities
- **Phase 2 (Enhancement)**: Medium-priority features and optimizations
- **Phase 3 (Maturity)**: Low-priority refinements and advanced features

---

## Step 4: Output Format and File Structure

### 4.1 File Naming Convention

**Format**: `[sequential_number]-[short-descriptive-name].md`

**Rules**:
- Use two-digit sequential numbers: `01`, `02`, ..., `10`, `11`, etc.
- Use kebab-case for the descriptive name
- Keep names concise (3-5 words max)
- Make names searchable and descriptive

**Examples**:
- `01-extract-ed-visit-data.md`
- `02-validate-timestamp-integrity.md`
- `03-analyze-hourly-arrival-patterns.md`
- `10-monitor-pipeline-health.md`

### 4.2 Individual Story File Structure

Each user story file must include ALL of these sections:

```markdown
# [Story Number]: [Descriptive Title]

## Overview and Statement

[2-3 sentences describing the story's purpose and business context]

**As a** [specific role/stakeholder]  
**I want** [specific, actionable capability]  
**So that** [measurable business value/outcome]

---

## Acceptance Criteria

Define **3-7 specific, testable criteria**. Each should be:
- Concrete and measurable
- Independently verifiable
- Focused on outcomes, not implementation

- [ ] [Criterion 1: Specific condition or output]
- [ ] [Criterion 2: Quality or performance requirement]
- [ ] [Criterion 3: Data coverage or completeness requirement]
- [ ] [Criterion 4: Validation or error handling requirement]
- [ ] [Additional criteria as needed...]

---

## Technical Notes

**Data Requirements**:
- Data sources needed
- Key fields/tables referenced
- Expected data volume/granularity

**Assumptions**:
- Technical or business assumptions
- Data quality assumptions
- Access or permission assumptions

**Considerations**:
- Edge cases to handle
- Performance considerations
- Security or privacy requirements

---

## Estimated Effort

**Story Points**: [1, 2, 3, 5, 8, 13]  
**Estimated Duration**: [days or weeks]

Effort scale:
- 1-2 points: Simple, well-defined task (1-2 days)
- 3-5 points: Moderate complexity (3-5 days)
- 8-13 points: Complex, may need breakdown (1-2 weeks)

---

## Priority

**[High / Medium / Low]**

**Rationale**: [1-2 sentences explaining priority level]

---

## Dependencies

**Prerequisite Stories**:
- [Story #XX]: [Brief reason why this is needed first]

**Enables Stories**:
- [Story #YY]: [How this story unlocks future work]

**External Dependencies**:
- [Any non-story dependencies: data access, infrastructure, approvals]

---

## Related Opportunities

Maps to: `[Opportunity name from opportunities.md]`

**Contribution**: [How this story addresses the opportunity]
```

### 4.3 Index File Structure (README.md)

Create `docs/objectives/user_stories/README.md` with:

```markdown
# User Stories Index

## Overview

**Total Stories**: [count]  
**Estimated Total Effort**: [sum of story points] points / [weeks] weeks  
**Implementation Phases**: [number] phases

---

## Implementation Roadmap

### Phase 0: Foundation (Stories 01-XX)
**Focus**: Infrastructure and data pipelines  
**Duration**: [weeks]

- [Story #01](./01-story-name.md) - [One-line description] `[Priority]` `[Points]`
- [Story #02](./02-story-name.md) - [One-line description] `[Priority]` `[Points]`

### Phase 1: Core Value (Stories XX-XX)
**Focus**: High-priority analytics  
**Duration**: [weeks]

- [Story #XX](./XX-story-name.md) - [One-line description] `[Priority]` `[Points]`

[Repeat for all phases...]

---

## Stories by Priority

### High Priority ([count] stories, [points] points)
- [Story #XX](./XX-story-name.md) - [Description]

### Medium Priority ([count] stories, [points] points)
- [Story #XX](./XX-story-name.md) - [Description]

### Low Priority ([count] stories, [points] points)
- [Story #XX](./XX-story-name.md) - [Description]

---

## Stories by Type

### Business Analytics ([count])
- [Story #XX](./XX-story-name.md) - [Description]

### Data Infrastructure ([count])
- [Story #XX](./XX-story-name.md) - [Description]

### Data Quality ([count])
- [Story #XX](./XX-story-name.md) - [Description]

### Monitoring & Operations ([count])
- [Story #XX](./XX-story-name.md) - [Description]

---

## Dependency Map

```
[Story #01] → [Story #02] → [Story #05]
           → [Story #03] → [Story #06]
[Story #04] → [Story #07]
```

[Visual representation of key dependencies]

---

## Quick Reference

| # | Story Title | Priority | Effort | Phase | Dependencies |
|---|-------------|----------|--------|-------|--------------|
| 01 | [Title] | High | 5 | 0 | None |
| 02 | [Title] | High | 8 | 0 | #01 |
[...] 

```

### 4.4 File Location

**Directory**: `docs/objectives/user_stories/`

**Structure**:
```
docs/objectives/user_stories/
├── README.md                          (Index file)
├── 01-story-name.md
├── 02-story-name.md
├── 03-story-name.md
└── ...
```

---

## Step 5: Quality Standards and Validation

### 5.1 INVEST Principles (Critical)

Every user story must satisfy the **INVEST** criteria:

1. **Independent**: Can be developed and delivered independently of other stories (minimize dependencies)
2. **Negotiable**: Details can be discussed and refined; not a rigid contract
3. **Valuable**: Delivers clear value to a stakeholder or the system
4. **Estimable**: Team can reasonably estimate the effort required
5. **Small**: Completable within one sprint (1-2 weeks)
6. **Testable**: Has clear acceptance criteria that can be verified

### 5.2 Quality Checklist

Before finalizing each story, verify:

**Story Statement**:
- [ ] Uses a specific, real role (not "user" or "stakeholder")
- [ ] Describes a concrete, actionable capability
- [ ] States measurable business value or outcome
- [ ] Avoids implementation details (tools, technologies)

**Acceptance Criteria**:
- [ ] Has 3-7 specific, testable criteria
- [ ] Criteria are measurable and verifiable
- [ ] Covers success conditions, data quality, and edge cases
- [ ] Does not prescribe implementation approach

**Technical Feasibility**:
- [ ] Required data is available or obtainable
- [ ] Effort is reasonable for one sprint
- [ ] Dependencies are identified and manageable
- [ ] No obvious technical blockers

**Business Alignment**:
- [ ] Maps to at least one opportunity in opportunities.md
- [ ] Addresses a real stakeholder need
- [ ] Delivers tangible, demonstrable value

### 5.3 Common Anti-Patterns to Avoid

**❌ Too Vague**:
- "As a manager, I want to understand patient flow patterns"
- **Why bad**: No specific action, no measurable outcome
- **✅ Better**: "As an ED Manager, I want to analyze hourly patient arrival volumes by day of week, so that I can identify optimal shift scheduling patterns"

**❌ Implementation-focused**:
- "As a data engineer, I want to build a Tableau dashboard showing wait times"
- **Why bad**: Prescribes tool and solution
- **✅ Better**: "As an ED Manager, I want to monitor real-time and historical wait times by triage category, so that I can proactively manage queue backlogs"

**❌ Too Large**:
- "As a hospital administrator, I want a complete operational analytics platform"
- **Why bad**: Not completable in one sprint, no specific value
- **✅ Better**: Split into 5-10 smaller stories, each with specific analytical capability

**❌ No Clear Value**:
- "As a data analyst, I want to explore the data"
- **Why bad**: No stakeholder benefit, no outcome
- **✅ Better**: "As a Data Analyst, I want to profile data completeness across all ED visit fields, so that I can identify which fields require validation rules"

**❌ Technology-dependent**:
- "As a developer, I want to set up an Airflow DAG for ETL"
- **Why bad**: Too focused on specific tool
- **✅ Better**: "As a Data Engineer, I want to automate daily extraction of ED visit records, so that analysis is based on current data"

### 5.4 Examples of Well-Crafted Stories

**Example 1: Business Analytics Story**
```markdown
# 05: Analyze Patient Arrival Patterns by Time of Day

## Overview and Statement
Enable operations team to identify peak arrival times to optimize staffing levels.

**As an** Emergency Department Operations Manager  
**I want to** analyze patient arrival patterns by hour of day and day of week over the past 12 months  
**So that** I can identify optimal shift schedules and reduce average wait times during peak periods

## Acceptance Criteria
- [ ] Analysis covers all ED visits from the past 12 months
- [ ] Results show arrival volume aggregated by hour (0-23) and day of week
- [ ] Statistical significance of patterns is calculated (p < 0.05)
- [ ] Peak hours (>1.5x average volume) are clearly identified
- [ ] Results are validated against known seasonal patterns (e.g., flu season)
```

**Example 2: Data Infrastructure Story**
```markdown
# 02: Extract Daily ED Visit Records

## Overview and Statement
Establish automated pipeline to extract ED visit data for downstream analytics.

**As a** Data Engineer  
**I want to** extract daily ED visit records from the source EMR system  
**So that** analysts have access to current data for operational reporting

## Acceptance Criteria
- [ ] Pipeline runs daily at 2:00 AM and completes within 30 minutes
- [ ] All required fields (visit_id, arrival_time, departure_time, triage_category) are extracted
- [ ] Data is stored in raw data layer following naming convention: `ed_visits_YYYYMMDD.csv`
- [ ] Pipeline logs execution status and record counts
- [ ] Failed extractions trigger alerts to data operations team
```

---

## Step 6: Execution Workflow

### 6.1 Recommended Process

1. **Read All Documentation** (Step 1)
   - Start with opportunities.md to understand business objectives
   - Review data dictionary to understand available data
   - Check data flow strategy for technical architecture
   - Review project context for constraints

2. **Identify Story Themes** (Step 2)
   - Group opportunities into story categories
   - Identify infrastructure prerequisites
   - Plan quality and monitoring stories
   - Consider stakeholder communication needs

3. **Draft Stories** (Step 2)
   - Write 10-20 user stories covering all categories
   - Ensure mix of business value and technical enablers
   - Follow the standardized file structure precisely
   - Apply INVEST principles to each story

4. **Prioritize and Sequence** (Step 3)
   - Assign High/Medium/Low priorities
   - Map dependencies between stories
   - Organize into implementation phases
   - Calculate estimated effort (story points)

5. **Validate Quality** (Step 5)
   - Run through quality checklist for each story
   - Check for anti-patterns
   - Ensure all stories map to opportunities
   - Verify effort estimates are reasonable

6. **Create Index** (Step 4)
   - Build comprehensive README.md
   - Include roadmap, priority views, and dependency map
   - Provide quick reference table
   - Ensure all navigation links work

### 6.2 Expected Output Counts

Generate approximately:
- **Total Stories**: 12-20 stories (adjust based on opportunities.md scope)
- **Foundation Stories (Phase 0)**: 3-5 stories (infrastructure, pipelines, validation framework)
- **Core Value Stories (Phase 1)**: 4-8 stories (primary analytical capabilities)
- **Enhancement Stories (Phase 2)**: 3-5 stories (optimizations, secondary analyses)
- **Maturity Stories (Phase 3)**: 2-4 stories (advanced features, refinements)

**Story Point Distribution**:
- Total effort: 60-120 story points
- Average per story: 5-8 points
- Phase 0: ~25% of total points
- Phase 1: ~40% of total points
- Phase 2: ~25% of total points
- Phase 3: ~10% of total points

---

## Final Deliverables

Generate the following files:

1. **README.md** (`docs/objectives/user_stories/README.md`)
   - Complete index with all views (roadmap, priority, type, dependencies)
   - Quick reference table
   - Summary statistics

2. **Individual Story Files** (`docs/objectives/user_stories/01-story-name.md`, etc.)
   - Each following the standardized structure exactly
   - All required sections completed
   - Cross-references to related stories
   - Mapped to opportunities

**Success Criteria**:
- Every story follows INVEST principles
- All stories map to documented opportunities
- Dependencies form a coherent workflow
- Effort estimates are realistic
- Files are properly formatted and linked
- Index provides clear navigation and overview

---

## Additional Guidance

### When to Make Assumptions

If information is missing:
- **Data availability**: Assume standard healthcare data structures (HL7, FHIR)
- **Stakeholders**: Infer from opportunity descriptions and healthcare context
- **Technical capabilities**: Assume modern analytics stack (SQL, Python, orchestration)
- **Constraints**: Assume standard healthcare privacy/security requirements

**Do NOT ask for clarification** - make reasonable assumptions and proceed.

### Handling Edge Cases

Include stories for:
- Data quality validation and profiling
- Error handling and pipeline resilience
- Documentation and knowledge transfer
- Monitoring and alerting
- Stakeholder training and adoption

### Tone and Style

- Professional and precise
- Action-oriented language
- Specific and measurable outcomes
- Free of jargon unless domain-specific
- Clear to both technical and business stakeholders

---

**Remember**: These stories will drive real implementation work. Quality and clarity are paramount. Write stories that a senior data scientist would respect and that development teams can confidently execute.
