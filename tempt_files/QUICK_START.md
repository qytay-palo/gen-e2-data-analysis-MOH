# Quick Start Guide: Data Science Lifecycle Automation

## 🚀 Get Started in 3 Steps

### Step 1: Generate Execution Plan
**Prompt**: [`.github/prompts/4-generate-lifecycle-and-execution-plan.prompt.md`](../.github/prompts/4-generate-lifecycle-and-execution-plan.prompt.md)

**What to do**:
1. Open the prompt file in VS Code
2. Select all content (Cmd/Ctrl + A)
3. Use with GitHub Copilot Chat
4. Wait for analysis of your user stories

**You'll get**:
- ✅ Complete execution plan (`docs/project_context/execution_plan.yml`)
- ✅ Routing configuration (`config/prompt_routing.yml`)
- ✅ Lifecycle stages mapped to each user story
- ✅ Execution waves with dependencies

**Time**: ~5-10 minutes

---

### Step 2: Execute Your Project
**Prompt**: [`.github/prompts/5-orchestrate-execution.prompt.md`](../.github/prompts/5-orchestrate-execution.prompt.md)

**What to do**:
1. Review the generated execution plan
2. Open prompt 5 in VS Code
3. Use with GitHub Copilot Chat
4. The orchestrator will:
   - Load your execution plan
   - Execute each wave sequentially
   - Call stage-specific prompts
   - Track progress and create artifacts

**Time**: Depends on project complexity (hours to days)

---

### Step 3: Review Results
**Check these locations**:
- 📊 **Results**: `results/execution_logs/`
- 📓 **Notebooks**: `notebooks/`
- 📁 **Data**: `data/`
- 🤖 **Models**: `models/trained/`
- 📈 **Reports**: `reports/`

---

## 📋 Cheat Sheet

### For Each Lifecycle Stage

| Stage | Prompt File | Input | Output |
|-------|------------|-------|--------|
| Data Acquisition | `stages/data-acquisition.prompt.md` | DB connection, queries | Raw datasets |
| Data Quality | `stages/data-quality-check.prompt.md` | Dataset path, rules | Quality report |
| EDA | `stages/eda.prompt.md` | Clean dataset, objectives | EDA notebook |
| Feature Engineering | `stages/feature-engineering.prompt.md` | Prepared data | Feature dataset |
| Model Training | `stages/model-training.prompt.md` | Training data, config | Trained models |
| Model Evaluation | `stages/model-evaluation.prompt.md` | Models, test data | Performance report |
| Reporting | `stages/visualization-reporting.prompt.md` | Results data | Dashboards, reports |

### Common Commands

```bash
# View execution plan
cat docs/project_context/execution_plan.yml

# Check routing config
cat config/prompt_routing.yml

# Monitor execution logs
tail -f results/execution_logs/run_latest.log

# View checkpoint
cat results/execution_logs/checkpoint_latest.json

# List generated artifacts
find results/ -type f -mtime -1
```

## 🎯 Usage Patterns

### Pattern 1: Single User Story
```yaml
# Execute just one user story
Use: 5-orchestrate-execution.prompt.md
Specify: --story 01
Duration: Few hours
```

### Pattern 2: Specific Wave
```yaml
# Execute one wave (e.g., EDA wave)
Use: 5-orchestrate-execution.prompt.md
Specify: --wave 2
Duration: Few days
```

### Pattern 3: Full Project
```yaml
# Execute entire project
Use: 5-orchestrate-execution.prompt.md
Specify: (no flags, runs all)
Duration: Weeks
```

### Pattern 4: Resume from Failure
```yaml
# Resume from last checkpoint
Use: 5-orchestrate-execution.prompt.md
Specify: --resume
Duration: Continues from last successful stage
```

## 🔧 Troubleshooting

### Issue: "Prerequisite not met"
**Cause**: Previous stage didn't complete successfully  
**Fix**: 
1. Check execution logs
2. Rerun failed stage
3. Verify outputs were created

### Issue: "Missing input artifact"
**Cause**: Output from previous stage not found  
**Fix**:
1. Check artifact paths in routing config
2. Verify previous stage completed
3. Check artifact_registry in checkpoint

### Issue: "Stage execution failed"
**Cause**: Error during stage execution  
**Fix**:
1. Review error message in logs
2. Check stage-specific quality checks
3. Validate input data format
4. Rerun with corrected inputs

### Issue: "Execution takes too long"
**Cause**: Large dataset or complex computation  
**Fix**:
1. Use sampling for testing
2. Enable parallel execution where possible
3. Optimize stage parameters
4. Use more compute resources

## 💡 Pro Tips

### Tip 1: Start Small
Begin with 1-2 user stories to validate the workflow before scaling to full project.

### Tip 2: Review Plans Before Execution
Always review the generated execution plan. Adjust waves or stage parameters as needed.

### Tip 3: Use Checkpoints
The system creates checkpoints automatically. Use `--resume` to recover from failures.

### Tip 4: Parallel Execution
Mark independent stories as `can_run_parallel: true` in execution plan for faster completion.

### Tip 5: Customize Stage Prompts
Modify stage prompts to fit your specific needs or domain requirements.

### Tip 6: Track Experiments
Use MLflow or similar tools (already integrated in model-training prompt) for experiment tracking.

### Tip 7: Version Your Plans
Commit execution plans and routing configs to git for reproducibility.

## 📚 Examples

### Example 1: Data Quality Check Only

```yaml
# execution_plan.yml (simplified)
waves:
  - wave_1:
      user_stories:
        - story_id: "01"
          lifecycle_stages:
            - stage: "Data Acquisition"
            - stage: "Data Quality Assessment"
```

**Command**: Use prompt 5 with this plan  
**Duration**: 1-2 hours  
**Output**: Quality report in `reports/`

### Example 2: Full Forecasting Project

```yaml
# execution_plan.yml (simplified)
waves:
  - wave_1:  # Foundation
      stages: [Data Acquisition, Quality Check]
  - wave_2:  # Analysis
      stages: [EDA, Feature Engineering]
  - wave_3:  # Modeling
      stages: [Model Training, Model Evaluation]
  - wave_4:  # Deployment
      stages: [Visualization, Reporting]
```

**Command**: Use prompt 5 (full execution)  
**Duration**: 2-3 weeks  
**Output**: Full project deliverables

## 🎓 Learning Resources

- **Full Documentation**: [`.github/prompts/README.md`](../.github/prompts/README.md)
- **System Overview**: [`docs/project_context/LIFECYCLE_AUTOMATION_SUMMARY.md`](LIFECYCLE_AUTOMATION_SUMMARY.md)
- **Stage Prompts**: [`.github/prompts/stages/`](../.github/prompts/stages/)
- **Example Outputs**: `results/execution_logs/` (after first run)

## 🔄 Workflow Diagram

```
User Stories
     ↓
[Prompt 4: Generate Plan]
     ↓
execution_plan.yml + routing_config.yml
     ↓
[Prompt 5: Orchestrate]
     ↓
┌─────────────────────────────────┐
│  Wave 1: Foundation             │
│  ├─ Story 01                    │
│  │  ├─ Stage: Data Acquisition  │ → [Call data-acquisition.prompt.md]
│  │  └─ Stage: Quality Check     │ → [Call data-quality-check.prompt.md]
│  └─ Story 02                    │
└─────────────────────────────────┘
     ↓
┌─────────────────────────────────┐
│  Wave 2: Analysis               │
│  ├─ Story 03                    │
│  │  ├─ Stage: EDA               │ → [Call eda.prompt.md]
│  │  └─ Stage: Feature Eng       │ → [Call feature-engineering.prompt.md]
└─────────────────────────────────┘
     ↓
[Continue through waves...]
     ↓
Final Artifacts + Reports
```

## ✅ Success Checklist

Before starting:
- [ ] User stories defined in `docs/objectives/user_stories/`
- [ ] Project context documented in `docs/project_context/`
- [ ] Data sources accessible
- [ ] Required tools installed (Python, Jupyter, etc.)

After execution plan generation:
- [ ] Execution plan reviewed and validated
- [ ] Routing configuration correct
- [ ] Dependencies identified
- [ ] Resource requirements understood

During execution:
- [ ] Progress monitored via logs
- [ ] Outputs validated at each stage
- [ ] Checkpoints created regularly
- [ ] Issues documented and resolved

After completion:
- [ ] All artifacts generated
- [ ] Quality checks passed
- [ ] Summary report created
- [ ] Stakeholders notified

## 🆘 Getting Help

1. **Check Documentation**: Start with README.md
2. **Review Logs**: Look at execution logs for errors
3. **Validate Inputs**: Ensure stage inputs are correct
4. **Check Examples**: Refer to stage prompt examples
5. **Test Incrementally**: Run one stage at a time

## 🎉 Quick Wins

### Win 1: Automated EDA (30 min)
Just need exploratory analysis? Use `stages/eda.prompt.md` directly with your dataset.

### Win 2: Data Quality Report (15 min)
Quick quality check? Use `stages/data-acquisition.prompt.md` + validate.

### Win 3: Model Training Pipeline (2 hours)
Have clean data? Jump straight to `stages/model-training.prompt.md`.

---

**Ready to start?** Open [`.github/prompts/4-generate-lifecycle-and-execution-plan.prompt.md`](../.github/prompts/4-generate-lifecycle-and-execution-plan.prompt.md) and begin!
