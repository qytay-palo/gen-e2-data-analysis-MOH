# Generate User Stories from Project Opportunities

## Context
You are a senior data science product owner with expertise in translating analytical objectives into actionable user stories. You excel at breaking down complex data initiatives into manageable, iterative development steps.

## Task
Analyze the project opportunities document and generate a comprehensive set of user stories that will guide the implementation of end-to-end identified analytics and machine learning solutions.

## Instructions

1. **Review the Opportunities Document**
   - Examine the opportunities file in `docs/objectives/opportunities.md`
   - Identify all major analytical opportunities and their priorities
   - Note the stakeholders, objectives, and expected outcomes
   - Review `docs/project_context/` folder for additional context on:
     - Available data sources and their characteristics
     - Technical stack and platform constraints
     - Other project background that may influence story design
   - Review `docs/data_dictionary/` for data field definitions and structures

2. **Generate User Stories**
   - Create user stories for each opportunity using the standard format:
     ```
     As a [role/stakeholder],
     I want to [action/capability],
     So that [business value/outcome].
     ```
   - Include appropriate acceptance criteria for each story
   - Consider technical and operational feasibility
   - Sequence stories to enable incremental value delivery

3. **Structure and Prioritization**
   - Group user stories by opportunity or theme (Epics)
   - Assign priority labels (High/Medium/Low) based on:
     - Expected business impact
     - Technical complexity
     - Dependencies on other work
     - Data readiness
   - Suggest implementation phases or sprints

4. **Technical Considerations**
   - Include stories for data validation and quality checks
   - Address infrastructure and pipeline setup needs
   - Consider monitoring, testing, and deployment requirements
   - Account for stakeholder communication and documentation

5. **Output Format**
   - Create separate markdown files for each Epic/theme
   - Use the following naming convention for files:
     ```
     [epic-number]-[short-epic-name].md
     
     Example:
     01-temporal-pattern-analysis.md
     02-queue-management.md
     03-patient-flow-optimization.md
     ```
   - Within each file, number individual user stories sequentially:
     ```
     User Story [story-number]: [Story Title]
     
     Example:
     User Story 1: Peak Hour Identification Analysis
     User Story 2: Seasonal Trend Forecasting
     User Story 3: No-Show Prediction Model
     ```
   - Include estimated effort/complexity where relevant
   - Provide a recommended implementation sequence

## File Organization

Save all user story files to: `docs/objectives/user_stories/`

Create an index file: `docs/objectives/user_stories/README.md` that:
- Lists all Epic files with descriptions
- Shows the recommended implementation order
- Summarizes total story count and estimated effort
- Provides navigation links to each Epic file

## User Story File Structure

Each Epic file should include the following:

```md
## Overview
[Brief description of the Epic and its business value]

## Priority
[High/Medium/Low]

## Dependencies
[List any prerequisite Epics or technical requirements]

```
## User Stories should include:

**As a** [role/stakeholder]
**I want** [action/capability]
**So that** [business value/outcome]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### Technical Notes
[Implementation considerations, data requirements, etc.]

### Estimated Effort
[Story points or time estimate]

### Priority
[High/Medium/Low]

---

[Repeat for each story in the Epic]
```

## Key Principles
1. **Value-focused:**: Each story must deliver tangible value to a specific end-user, stakeholder, or the system itself (e.g., improving performance, security). Clearly articulate the "so that" benefit.
2. **Small**: User stories must be able to be completed within a sprint. Avoid overly broad, vague or complex stories
3. **Testable**: Include clear acceptance criteria
4. **Independent**: Minimize dependencies between stories where possible
5. **Traceable**: Clear numbering system allows easy reference and tracking
6. **Negotiable**: A user story is not a contract; its a placeholder for conversation and refinement
7. **Iterative**: Enable incremental progress and early wins


## Deliverable
Generate:
1. Individual Epic files in `docs/objectives/user_stories/` following the naming convention
2. An index/README file that provides overview and navigation
3. Each file should be self-contained but cross-reference related stories where needed

The naming convention ensures:
- Easy sorting and navigation (numeric prefix)
- Clear Epic identification
- Readable file names without opening
- Logical grouping by theme
- Simple reference in discussions and tickets
