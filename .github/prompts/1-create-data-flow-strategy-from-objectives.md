---
description: Generate Data Flow Strategy for Analytics Project
model: claude-sonnet-4.5
---

<!-- Metadata:
Stage: Planning
Rule Name: create-data-flow-strategy
Rule Version: latest
-->

Your prompt instructions start here:

## Context

You are a senior data architect tasked with designing an end-to-end data flow strategy for this analytics project. Review the following project documentation:

- `docs/objectives/opportunities.md` - Business problems and analytical opportunities
- `docs/data_dictionary/` - Available data schemas, fields, and definitions
- `docs/project_context/` - Data sources, technical stack, and project constraints

## Your Task

Analyze the opportunities document and create a comprehensive data flow plan that maps the journey from **data extraction** to **final business-ready outputs**. Consider:

1. **Data Sources & Extraction**: Identify what data needs to be extracted and from where
2. **Data Transformation Pipeline**: Define processing stages (cleaning, validation, feature engineering)
3. **Analysis & Modeling**: Determine analytical approaches and potential ML models
4. **Output Artifacts**: Specify deliverables (dashboards, reports, APIs, datasets)
5. **Integration Points**: Identify where different opportunities can share pipelines or outputs

## Instructions

1. Review project documentation:
   - Read `docs/objectives/opportunities.md` to understand the business problems
   - Examine `docs/data_dictionary/` to understand available data structures and fields
   - Check `docs/project_context/` for data source locations, technical constraints, and platform capabilities
2. For each opportunity identified:
   - Map the required input data sources
   - Design the transformation workflow
   - Specify the analytical methods/models to apply
   - Define the final output format and consumers
3. Identify opportunities to consolidate workflows (e.g., multiple opportunities using same data sources)
4. Create implementation recommendations prioritizing by business impact and technical dependencies

## Output Requirements

Generate a structured data flow strategy document that includes:

- **Data Flow Diagram** (conceptual): Source → Processing → Analysis → Output (using Mermaid or ASCII)
- **Pipeline Architecture**: Key stages and their responsibilities (using Mermaid or ASCII)
- **Data Dependencies**: What data feeds into each analysis 
- **Reusable Components**: Shared transformations or feature engineering logic (use structured lists or YAML-style formatting)
- **Delivery Mechanisms**: How outputs reach end users (dashboards, reports, APIs)

Document your strategy in `docs/methodology/data_flow_strategy.md`

### Formatting Guidelines

- Use Mermaid diagrams for all workflows and architecture visualizations
- Use markdown tables for structured data (dependencies, stages, mappings)
- Use code blocks with language tags for any configuration examples
- Use clear headings and bullet points for easy parsing
- Avoid complex visual formatting; prioritize machine-readable structure

Be analytical in your approach—examine the opportunities deeply, make informed architectural decisions, and justify your design choices based on scalability, maintainability, and business value.
