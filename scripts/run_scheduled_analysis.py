#!/usr/bin/env python3
"""
Scheduled Analysis Runner
Runs automated analyses based on configuration
"""

import yaml
from pathlib import Path
import logging
from auto_analyze import AutomatedAnalyzer
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_path: str = "config/auto_analysis.yml") -> dict:
    """Load analysis configuration"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def run_scheduled_analyses():
    """Execute all enabled scheduled analyses"""
    project_root = Path(__file__).parent.parent
    config_path = project_root / "config" / "auto_analysis.yml"
    
    logger.info("Loading configuration...")
    config = load_config(config_path)
    
    analyzer = AutomatedAnalyzer(project_root=str(project_root))
    
    # Track overall results
    execution_summary = {
        "start_time": datetime.now().isoformat(),
        "schedules_run": [],
        "total_datasets": 0,
        "successful": 0,
        "failed": 0
    }
    
    # Run each scheduled analysis
    for schedule_name, schedule_config in config['analysis_schedules'].items():
        if not schedule_config.get('enabled', False):
            logger.info(f"Skipping disabled schedule: {schedule_name}")
            continue
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Running schedule: {schedule_name}")
        logger.info(f"{'='*60}")
        
        datasets = schedule_config.get('datasets', [])
        analysis_types = schedule_config.get('analysis_types', ['explore'])
        
        schedule_results = {
            "schedule": schedule_name,
            "datasets_processed": 0,
            "analyses_completed": 0,
            "errors": []
        }
        
        for dataset_path in datasets:
            full_path = project_root / dataset_path
            
            if not full_path.exists():
                error_msg = f"Dataset not found: {dataset_path}"
                logger.warning(error_msg)
                schedule_results["errors"].append(error_msg)
                execution_summary["failed"] += 1
                continue
            
            logger.info(f"Processing: {dataset_path}")
            execution_summary["total_datasets"] += 1
            schedule_results["datasets_processed"] += 1
            
            for analysis_type in analysis_types:
                try:
                    logger.info(f"  Running {analysis_type} analysis...")
                    result = analyzer.analyze_dataset(str(full_path), analysis_type)
                    
                    schedule_results["analyses_completed"] += 1
                    execution_summary["successful"] += 1
                    logger.info(f"  ✓ {analysis_type} completed")
                    
                except Exception as e:
                    error_msg = f"Error in {analysis_type} for {dataset_path}: {str(e)}"
                    logger.error(f"  ✗ {error_msg}")
                    schedule_results["errors"].append(error_msg)
                    execution_summary["failed"] += 1
        
        execution_summary["schedules_run"].append(schedule_results)
        logger.info(f"\nSchedule '{schedule_name}' complete:")
        logger.info(f"  Datasets processed: {schedule_results['datasets_processed']}")
        logger.info(f"  Analyses completed: {schedule_results['analyses_completed']}")
        if schedule_results["errors"]:
            logger.info(f"  Errors: {len(schedule_results['errors'])}")
    
    # Final summary
    execution_summary["end_time"] = datetime.now().isoformat()
    
    logger.info(f"\n{'='*60}")
    logger.info("EXECUTION SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"Total datasets: {execution_summary['total_datasets']}")
    logger.info(f"Successful analyses: {execution_summary['successful']}")
    logger.info(f"Failed analyses: {execution_summary['failed']}")
    logger.info(f"{'='*60}\n")
    
    # Save execution summary
    summary_path = project_root / "results" / "metrics" / f"execution_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
    with open(summary_path, 'w') as f:
        yaml.dump(execution_summary, f, default_flow_style=False)
    
    logger.info(f"Execution summary saved to: {summary_path}")
    
    return execution_summary


if __name__ == "__main__":
    import sys
    
    try:
        run_scheduled_analyses()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
