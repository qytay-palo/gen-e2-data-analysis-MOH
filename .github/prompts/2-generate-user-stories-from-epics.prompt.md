---
description: Generate User Stories from Problem Statements for Data Science and Analytics
stage: Project Management
subcategory: subcategory-agile-tools
rule_name: user-stories
rule_version: latest
---

# Generate User Stories from Problem Statements

## Role
You are a **senior data analyst** with expertise in:
- Translating analytical objectives into actionable user stories
- Breaking down complex data initiatives into iterative, deliverable increments
- Balancing technical feasibility with business value
- Designing analytics workflows that follow best practices in data science and engineering

## Objective
Decompose **ALL problem statements into high-quality, manageable user stories** for data science and analytics work. You must process every problem statement found in `docs/objectives/problem_statements/` directory. Analyze the problem statements and generate a list of user stories for each problem statement. The stories should represent distinct pieces of functionality or value from an end-user perspective.

These user stories will:
- Drive an automated analytics planning system
- Guide sprint planning and execution
- Enable incremental value delivery to stakeholders
- Form the basis for technical implementation

**CRITICAL**: This task must be completed for ALL problem statements in the project, not just a subset. Generate comprehensive user stories for every problem statement file you find.

---

## Instructions

### Step 1: Analyze Project Context

#### Inputs
You have access to the following project documentation files:
   - **Read ALL files** from `docs/objectives/problem_statements/` directory to understand:
      - Each problem statement's scope, objectives, and expected outcomes
      - Stakeholders and their needs
      - Business priorities and success criteria
   - Review `docs/project_context/` folder for additional context on:
     - Available data sources and their characteristics
     - Technical stack and platform constraints
     - Other project background that may influence story design
   - Review `docs/data_dictionary/` for data field definitions and structures

**CRITICAL CONSTRAINT**: All problem statements must be **grounded in available data sources** documented in [docs/project_context/data_sources.md](../../../docs/project_context/data_sources.md) and **feasible with the current tech stack** documented in [docs/project_context/tech_stack.md](../../../docs/project_context/tech_stack.md). Do not propose problems that require unavailable data or exceed technical capabilities.

#### Expected Problem Statement Format

Each problem statement file in `docs/objectives/problem_statements/` should contain:
- **Problem Statement Title and ID**: Clear, descriptive name with unique identifier
- **Business Objective**: What business problem this problem statement solves
- **Success Criteria**: Measurable outcomes that define completion
- **Stakeholders**: Who benefits and who needs to be involved
- **Scope**: What is included and explicitly excluded
- **Assumptions and Constraints**: Technical, data, or resource limitations

**If problem statements are incomplete or poorly defined**: Make reasonable assumptions based on project context and document them in the generated user stories.

---

### Step 2: Extract Stakeholders and Gather Domain Knowledge

This step ensures that domain expertise is captured and made available to guide feature engineering and analysis decisions throughout the project.

#### a. Identify Stakeholders

For each problem statement:
- Extract all stakeholder types mentioned (e.g., healthcare operations manager, policy analyst, clinician)
- Document their roles, expertise areas, and analytical perspectives
- Group stakeholders by domain (e.g., healthcare operations, policy, clinical practice, public health)
- Note specific expertise or concerns each stakeholder brings

#### b. Assess Domain Knowledge Requirements

For each stakeholder group and problem statement, identify relevant domain knowledge areas needed for:
- Understanding context, terminology, and domain-specific concepts
- Feature engineering and variable selection
- Interpreting analytical results and validating assumptions
- Identifying relevant metrics, KPIs, and benchmarks
- Recognizing data quality issues specific to the domain

#### c. Check Existing Domain Knowledge Files

Search the `/docs` directory structure for existing domain knowledge documentation:
- Look in `docs/domain_knowledge/` (create if doesn't exist)
- Search for files matching patterns:
  - `stakeholder-{role}-expertise.md`
  - `{domain}-terminology-glossary.md`
  - `{domain}-metrics-kpis.md`
  - `{domain}-feature-engineering-guide.md`
  - `{analytical-area}-best-practices.md`
- Review existing files for:
  - Completeness relative to problem statement needs
  - Currency of information (check last updated date)
  - Coverage of relevant metrics and features

#### d. Update or Create Domain Knowledge Files

**If relevant files exist:**
- Review content against current problem statement requirements
- Update with more new concepts, metrics, or terminology referenced in problem statements
- Add cross-references to new problem statements
- Enhance feature engineering guidance if gaps are identified
- Update the "Last Updated" section with date and reason

**If files don't exist:**
- Use web search to gather authoritative domain knowledge from:
  - Government health agencies (e.g., MOH, CDC, WHO)
  - Academic publications and healthcare journals
  - Industry standard frameworks and guidelines
  - Healthcare analytics best practice documentation
- Focus search on:
  - Industry-standard metrics, KPIs, and benchmarks
  - Common feature engineering patterns for the domain
  - Domain-specific terminology, concepts, and calculations
  - Data quality considerations and validation approaches
  - Analytical methodologies commonly used in the domain
- Create new documentation files following the naming convention and structure below

#### e. File Naming Convention for Domain Knowledge

Use clear, descriptive names that enable easy identification of content:

**Stakeholder Expertise:**
- `stakeholder-{role}-expertise.md`
- Examples: 
  - `stakeholder-healthcare-operations-manager-expertise.md`
  - `stakeholder-clinical-director-expertise.md`
  - `stakeholder-health-policy-analyst-expertise.md`

**Domain Terminology:**
- `{domain}-terminology-glossary.md`
- Examples:
  - `healthcare-terminology-glossary.md`
  - `public-health-terminology-glossary.md`

**Metrics and KPIs:**
- `{domain}-metrics-kpis.md`
- Examples:
  - `polyclinic-utilization-metrics-kpis.md`
  - `patient-flow-metrics-kpis.md`
  - `disease-surveillance-metrics-kpis.md`

**Feature Engineering Guides:**
- `{domain}-feature-engineering-guide.md`
- Examples:
  - `patient-flow-feature-engineering-guide.md`
  - `healthcare-capacity-feature-engineering-guide.md`
  - `disease-outbreak-feature-engineering-guide.md`

**Best Practices:**
- `{analytical-area}-best-practices.md`
- Examples:
  - `time-series-forecasting-best-practices.md`
  - `geospatial-health-analysis-best-practices.md`
  - `healthcare-equity-analysis-best-practices.md`

#### f. File Content Structure for Domain Knowledge

Store all domain knowledge files in `docs/domain_knowledge/` directory. Each file should follow this structure:

```markdown
# Domain Knowledge: {Descriptive Title}

## Overview
Brief description of the domain area covered, its relevance to the project, and key stakeholders who need this knowledge.

## Related Problem Statements
- [Problem Statement {ID} - {Name}](../objectives/problem_statements/{file}.md)
- [Problem Statement {ID} - {Name}](../objectives/problem_statements/{file}.md)

## Related Stakeholders
- **{Stakeholder Role}**: {How they use this knowledge in their analysis or decision-making}
- **{Stakeholder Role}**: {Context and application}

## Key Concepts and Terminology

### {Concept 1}
**Definition**: Clear explanation of the concept
**Relevance**: How this applies to data analysis and feature engineering
**Example**: Concrete example in healthcare context

### {Concept 2}
**Definition**: Clear explanation
**Relevance**: Application to analytics
**Example**: Practical example

## Standard Metrics and KPIs

| Metric Name | Definition | Calculation Formula | Typical Range | Use Case | Data Requirements |
|-------------|-----------|---------------------|---------------|----------|-------------------|
| {Metric} | {Description} | {Formula or method} | {Normal range} | {When to use} | {Required fields} |
| {Metric} | {Description} | {Formula} | {Range} | {Application} | {Fields needed} |

## Feature Engineering Guidance

### Common Features for {Domain}

#### {Feature Category 1}
- **{Feature Name}**: 
  - **Description**: What this feature represents
  - **Calculation**: How to derive it from raw data
  - **Interpretation**: What values indicate
  - **Use Cases**: When this feature is valuable
  - **Example**: Concrete calculation example

#### {Feature Category 2}
- **{Feature Name}**: {Complete description as above}

### Domain-Specific Patterns

#### {Pattern 1}
**Description**: {What the pattern is}
**When to Apply**: {Situations where this is relevant}
**Implementation**: {How to create features based on this pattern}
**Example**: {Concrete example with data}

#### {Pattern 2}
{Complete pattern description}

### Temporal Features
{Specific guidance for time-based features in this domain}

### Aggregation Strategies
{How to aggregate data meaningfully in this domain}

## Data Quality Considerations

### {Domain-Specific Issue 1}
- **Description**: {What to watch for}
- **Impact**: {How it affects analysis}
- **Detection**: {How to identify the issue}
- **Mitigation**: {How to handle it}

### {Domain-Specific Issue 2}
{Complete data quality guidance}

## Analytical Methodologies

### {Method 1}
- **Application**: {When to use this method}
- **Assumptions**: {Key assumptions that must hold}
- **Implementation Notes**: {Practical guidance}
- **Interpretation**: {How to read results}

## Common Pitfalls and Best Practices

### Pitfalls to Avoid
- {Pitfall 1}: {Why it's problematic and how to avoid}
- {Pitfall 2}: {Description and prevention}

### Best Practices
- {Practice 1}: {Why it's important and how to implement}
- {Practice 2}: {Guidance}

## References and Sources

### Authoritative Sources
- **{Source Name}**: {URL} - {Brief description of content}
- **{Source Name}**: {URL} - {What's covered}

### Academic References
- {Citation 1}
- {Citation 2}

### Industry Standards
- {Standard 1}: {Description and link}

## Cross-References

### Related Domain Knowledge Files
- [{File Name}]({relative-path}) - {How it relates}

### Related Data Dictionary Entries
- [{Data Source}](../data_dictionary/{file}.md) - {Relevant fields}

## Metadata

**Created**: {Date}
**Last Updated**: {Date}
**Updated By**: {Who made changes}
**Update Reason**: {Why the update was made}
**Version**: {Version number}

## Notes

{Any additional context, open questions, or areas needing further research}
```

#### g. Integration with User Story Generation

The domain knowledge gathered in this step should inform:
- **Feature engineering tasks** in user stories (reference specific features from domain knowledge)
- **Acceptance criteria** (use standard metrics and KPIs documented)
- **Technical constraints** (apply domain-specific data quality considerations)
- **Implementation tasks** (leverage documented analytical methodologies)
- **Validation approaches** (use domain-appropriate benchmarks and ranges)

When generating user stories in subsequent steps, explicitly reference relevant domain knowledge files to guide implementation.

---

### Step 3: Identify User Stories from Each Problem Statement

Breakdown each problem statement into distinct user stories according to the following guidelines:

#### a. Apply INVEST Principles

Ensure each story adheres to the INVEST principles:

1.  **Independent:** Stories should be self-contained and ideally implementable without depending on others in the same batch (though natural dependencies between features are okay). Avoid tightly coupling unrelated concepts in one story.
2.  **Negotiable:** Stories are not contracts. They represent the essence of the requirement, leaving room for discussion and refinement of details during backlog grooming or sprint planning.
3.  **Valuable:** Each story must deliver tangible value to a specific end-user, stakeholder, or the system itself (e.g., improving performance, security). Clearly articulate the "so that" benefit.
4.  **Estimable:** The story should be clear and defined enough that the development team can reasonably estimate the effort required to implement it. Avoid vague or overly broad stories.
5.  **Small:** Stories should be small enough to be completed within a single iteration (e.g., a typical sprint). Break down large problem statements or features into smaller, manageable stories.
6.  **Testable:** Each story must have implicit or explicit acceptance criteria. It should be possible to verify that the story has been implemented correctly.

#### b. Use Vertical Slicing (CRITICAL)

*   **DO:** Create stories that represent a complete, thin slice of end-to-end functionality, delivering user value. Example: "As a user, I want to log in with my email and password so that I can access my account." (Touches UI, logic, potentially backend).
*   **DO NOT:** Split stories horizontally by technical layer or component. Avoid stories like: "Create the login database table," "Build the login API endpoint," or "Design the login UI." These are tasks, not user stories.

#### c. Story Format Requirements

*   Assign a sequential number to each story title (e.g., `# User Story: 1 - Search Products`).
*   Focus on extracting user-centric requirements and value propositions discussed.
*   Ignore conversational filler, off-topic discussions, or administrative details unless they directly inform a requirement.
*   If the problem statement mentions specific user roles, use them. Otherwise, infer logical user types (e.g., "user," "administrator," "analyst").
*   If acceptance criteria are explicitly discussed, include them as bullet points under the relevant story.

---

### Step 4: Generate User Story Files

#### a. File Organization

1. Story files should be placed in:
   `docs/objectives/user_stories/problem-statement-{num}-{name}/<numerical_prefix>-<story_name>.md`

2. Each problem statement should have an index.md, should be updated when any story is updated, created or deleted:
   `docs/objectives/user_stories/problem-statement-{num}-{name}/index.md`

   - Lists all stories in the feature
   - Brief description of each story
   - Links to story files
   - List of reusable components in the feature

3. Main problem statements index should be updated:
   `docs/objectives/problem_statements/index.md`

   - Add new problem statement if needed
   - Link to problem statement index
   - Brief problem statement description
   - Key stories or functionality
   - List of reusable components
   - Overall problem statement progress tracking

#### b. File Naming Convention

Use a two-digit sequential number prefix followed by kebab-case based on the story's core goal:
- `01-analyze-visit-patterns-by-age.md`
- `02-identify-seasonal-utilization-trends.md`

#### c. File Content Structure

Each markdown file should contain *one* user story following this format:

```markdown
# User Story: [Story Number] - [Brief Title Describing the Goal]

**As a** [type of user/role],
**I want** [to perform an action or achieve a goal],
**so that** [I gain a specific benefit or value].

## 1. 🎯 Acceptance Criteria

*   [Criterion 1]
*   [Criterion 2]
*   ... (Include if discussed or clearly implied)

## 2. 🔒 Technical Constraints

*   [Architecture requirements]
*   [State management approach]
*   [Data analysis guidelines]

## 3. 📚 Domain Knowledge References

*   [Link to relevant domain knowledge files in docs/domain_knowledge/]
*   [Specific metrics, KPIs, or features to leverage]
*   [Domain-specific considerations for this story]

## 4. 📦 Dependencies

*   [External packages with purpose]
*   [Internal dependencies and models]

## 5. ✅ Implementation Tasks

Each task has a status indicator:
- ⬜ Not Started
- 🟨 In Progress
- ✅ Completed

Common task groups:
- **Data Extraction**: Source identification, data loading, API integration
- **Data Preprocessing**: Cleaning, transformation, feature engineering
- **Data Quality**: Validation, completeness checks, outlier detection
- **Data Analysis**: Statistical analysis, exploratory data analysis, hypothesis testing
- **Machine Learning**: Model selection, training, hyperparameter tuning
- **Model Evaluation**: Validation, testing, performance metrics
- **Visualization**: Charts, dashboards, interactive reports
- **Documentation**: Analysis documentation, methodology notes, findings summary

## 6. Notes (Optional)

*   [Any relevant notes, context, or open questions]
```

---

## Reference: User Story Documentation Standards

This section outlines detailed formatting guidelines for writing user stories in the project.

### Story Component Details

#### 1. 📝 Description
   - Clear and concise explanation of the feature
   - Purpose and value proposition
   - Main functionality overview
   - Formatted like "as a user..."

#### 2. 🎯 Acceptance Criteria
   - Numbered list of requirements (1, 2, 3...)
   - Each major component gets its own section
   - Include data analysis requirements
   - Use bullet points for detailed requirements

#### 3. 🔒 Technical Constraints
   - Architecture requirements
   - State management approach
   - Data analysis guidelines

#### 4. 📚 Domain Knowledge References
   - Links to relevant domain knowledge files
   - Specific metrics, KPIs, or features to leverage
   - Domain-specific considerations

#### 5. 📦 Dependencies
   - External packages with their purpose
   - Internal dependencies and models

#### 6. ✅ Tasks
   - Grouped by implementation layer
   - Each task has a status indicator (⬜ Not Started / 🟨 In Progress / ✅ Completed)
   - Tasks should be specific enough for immediate development
   - Include data source file paths, API endpoints, or dataset references
   - Note any code reuse opportunities from existing components
   - Specify configuration or environment setup requirements

---

## Writing Style Guidelines

1. **Emojis**
   - Use consistent emojis for each section
   - 📝 for Description
   - 📊 for Story Metadata
   - 🎯 for Acceptance Criteria
   - 🔒 for Technical Constraints
   - � for Domain Knowledge References
   - �📦 for Dependencies
   - ✅ for Implementation Tasks
   - 🔍 for search results and findings

2. **Formatting**
   - Use headers for main sections
   - Use bullet points for lists
   - Use numbered lists for ordered requirements
   - Add spacing between sections
   - Use code blocks for package names and file paths

3. **Content**
   - Be specific and measurable
   - Focus on what, not how
   - Include both functional and non-functional requirements
   - Define clear success criteria with measurable metrics
   - Document data dependencies and availability explicitly
   - Specify performance and quality thresholds
   - Document component search results

### Maintenance

1. **Status Updates**
   - Keep task status up to date
   - Mark tasks as completed when merged
   - Use in-progress status for active work
   - Document component reuse decisions

2. **Documentation Updates**
   - Update documentation when requirements change
   - Update documentation when implementation change
   - Keep dependencies list current
   - Add new tasks as needed
   - Remove completed stories from active tracking
   - Update component lists when new ones are added

3. **Component Discovery**
   - Regularly update feature indices with reusable components
   - Document search strategies used
   - Note modifications made to existing components
   - Track component dependencies between features

---

## Example: From Problem Statement to User Stories

### Input Problem Statement Snippet

"...The analytics team needs to understand polyclinic utilization patterns. Sarah from MOH mentioned that tracking visit trends by age group and time period is critical for capacity planning. John added that analyzing seasonal patterns would help with resource allocation, especially during peak periods. We need to ensure the analysis is reliable and the insights are clearly communicated to stakeholders with supporting visualizations..."

### Generated User Stories

1.  **As a** healthcare policy analyst,
    **I want** to analyze polyclinic visit patterns by age group and year,
    **so that** I can identify demographic trends and inform capacity planning decisions.
    *   Acceptance Criteria:
        *   Data extraction includes visit counts by age group (per [`docs/data_dictionary/`](docs/data_dictionary/))
        *   Analysis covers full historical period available in the dataset
        *   Output includes summary statistics and trend metrics by age segment

2.  **As a** healthcare operations manager,
    **I want** to identify seasonal utilization patterns in polyclinic visits,
    **so that** I can optimize staff scheduling and resource allocation during peak periods.
    *   Acceptance Criteria:
        *   Analysis identifies quarterly and monthly visit patterns
        *   Seasonal peaks and troughs are clearly quantified
        *   Results are presented in an interactive dashboard with drill-down capabilities
        *   Statistical significance of seasonal variations is documented

---

## ✅ Completion Checklist

Before finishing, verify that you have:

- [ ] Read **ALL** problem statement files in `docs/objectives/problem_statements/`
- [ ] Extracted stakeholders from each problem statement
- [ ] Checked for existing domain knowledge files in `docs/domain_knowledge/`
- [ ] Updated existing domain knowledge files or created new ones with web research
- [ ] Named domain knowledge files following the prescribed naming convention
- [ ] Cross-referenced domain knowledge in user stories for feature engineering guidance
- [ ] Generated user stories for **EVERY** problem statement (not just a subset)
- [ ] Applied INVEST principles to each story
- [ ] Used vertical slicing (end-to-end value, not technical layers)
- [ ] Created separate markdown files with correct naming convention
- [ ] Included all required sections: Description, Acceptance Criteria, Technical Constraints, Dependencies, Tasks
- [ ] Updated each problem statement's `index.md` with links to new stories
- [ ] Updated the main `docs/objectives/problem_statements/index.md`
- [ ] Ensured stories are small enough for one sprint
- [ ] Made stories testable with clear acceptance criteria
- [ ] Documented any assumptions made for incomplete problem statements

---