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

---
## Inputs
You have access to the following project documentation files:
   - Examine the opportunities file in `docs/objectives/opportunities.md`
      - Identify all major analytical opportunities and their priorities
      - Note the stakeholders, objectives, and expected outcomes
   - Review `docs/project_context/` folder for additional context on:
     - Available data sources and their characteristics
     - Technical stack and platform constraints
     - Other project background that may influence story design
   - Review `docs/data_dictionary/` for data field definitions and structures
   - Review `docs/methodology/data_flow_strategy.md` for the designed data flow and pipeline architecture

---
## Instructions

1. **Generate User Stories**
   - Create user stories for each opportunity using the standard format:
     ```
     As a [role/stakeholder],
     I want to [action/capability],
     So that [business value/outcome].
     ```
   - Include appropriate acceptance criteria for each story
   - Consider technical and operational feasibility
   - Sequence stories to enable incremental value delivery

2. **Structure and Prioritization**
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
   - Avoid implementation details (e.g., tools, models, dashboards).
   Focus on *intent*, not *how*.

---
## Output Format
   - Create separate markdown files for each User Story
   - Use a two-digit sequential number prefix followed by kebab-case based on the story's core goal for e.g. [sequential_number]-[short-user-story-name].md
   - Include estimated effort/complexity where relevant
   - Provide a recommended implementation sequence

## File Organization

Save all user story files to: `docs/objectives/user_stories/`

Create an index file: `docs/objectives/user_stories/README.md` that:
- Lists all User Story files with descriptions
- Shows the recommended implementation order
- Summarizes total story count and estimated effort
- Provides navigation links to each User Story file

## User Story File Structure

Each user story file must include ALL of these sections:

```markdown
# [Story Number]: [Descriptive Title]

## Overview and Statement

[2-3 sentences describing the story's purpose and business context]

**As a** [role/stakeholder]
**I want** [action/capability]
**So that** [business value/outcome]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] [Additional criteria as needed...]

### Technical Notes
[Implementation considerations, data requirements, etc.]

### Estimated Effort
[Story points or time estimate]

### Priority
[High/Medium/Low]

## Dependencies
[List any prerequisite User Stories or technical requirements]

```

## Key Principles
1. **Value-focused:**: Each story must deliver tangible value to a specific end-user, stakeholder, or the system itself (e.g., improving performance, security). Clearly articulate the "so that" benefit.
2. **Small**: User stories must be able to be completed within a sprint. Avoid overly broad, vague or complex stories
3. **Testable**: Include clear acceptance criteria
4. **Independent**: Minimize dependencies between stories where possible
5. **Traceable**: Clear numbering system allows easy reference and tracking
6. **Negotiable**: A user story is not a contract; its a placeholder for conversation and refinement
7. **Iterative**: Enable incremental progress and early wins

## QUALITY BAR (IMPORTANT):

- Write stories that a senior data scientist would respect.
- Each story should naturally map to a different analytics workflow.
- Avoid generic filler (e.g., “get insights”, “understand data”).
- If assumptions are needed, make reasonable ones silently.

---
[Repeat for each story in the Epic]

## Deliverable
Generate:
1. Individual User Story files in `docs/objectives/user_stories/` following the naming convention
2. An index/README file that provides overview and navigation
3. Each file should be self-contained but cross-reference related stories where needed

```