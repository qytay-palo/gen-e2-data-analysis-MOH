"""
Scheduler for Automated Data Extraction
Version: 1.0
Created: 2026-01-26

Schedules and runs data extraction jobs:
- Daily incremental extraction
- Weekly full extraction
- Monthly reference data refresh
- Custom schedules
"""

import schedule
import time
import logging
from datetime import datetime, timedelta
from typing import Optional, Callable, List
import yaml
from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.data_processing.etl_pipeline import ETLPipeline
from src.utils.logging_config import setup_logging
from src.utils.monitoring import PerformanceMonitor, AlertManager


logger = logging.getLogger(__name__)


class ExtractionScheduler:
    """
    Manages scheduled data extraction jobs.
    """
    
    def __init__(self, config_path: str = 'config/database.yml'):
        """
        Initialize scheduler.
        
        Args:
            config_path: Path to configuration file
        """
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.schedule_config = config.get('schedule', {})
        self.pipeline = ETLPipeline(config_path)
        self.monitor = PerformanceMonitor()
        self.alert_manager = AlertManager(config_path)
        
        logger.info("Extraction scheduler initialized")
    
    def schedule_daily_extraction(self):
        """Schedule daily incremental extraction."""
        daily_config = self.schedule_config.get('daily', {})
        
        if not daily_config.get('enabled', False):
            logger.info("Daily extraction not enabled")
            return
        
        schedule_time = daily_config.get('time', '02:00')
        sources = daily_config.get('extractions', [])
        
        schedule.every().day.at(schedule_time).do(
            self._run_daily_extraction,
            sources=sources
        )
        
        logger.info(f"Scheduled daily extraction at {schedule_time} for sources: {sources}")
    
    def schedule_weekly_extraction(self):
        """Schedule weekly full extraction."""
        weekly_config = self.schedule_config.get('weekly', {})
        
        if not weekly_config.get('enabled', False):
            logger.info("Weekly extraction not enabled")
            return
        
        schedule_day = weekly_config.get('day', 'sunday')
        schedule_time = weekly_config.get('time', '00:00')
        sources = weekly_config.get('extractions', [])
        
        # Map day name to schedule function
        day_map = {
            'monday': schedule.every().monday,
            'tuesday': schedule.every().tuesday,
            'wednesday': schedule.every().wednesday,
            'thursday': schedule.every().thursday,
            'friday': schedule.every().friday,
            'saturday': schedule.every().saturday,
            'sunday': schedule.every().sunday
        }
        
        if schedule_day.lower() in day_map:
            day_map[schedule_day.lower()].at(schedule_time).do(
                self._run_weekly_extraction,
                sources=sources
            )
            
            logger.info(
                f"Scheduled weekly extraction on {schedule_day} at {schedule_time} "
                f"for sources: {sources}"
            )
    
    def schedule_monthly_extraction(self):
        """Schedule monthly reference data refresh."""
        monthly_config = self.schedule_config.get('monthly', {})
        
        if not monthly_config.get('enabled', False):
            logger.info("Monthly extraction not enabled")
            return
        
        # For monthly scheduling, we'll check daily if it's the right day
        schedule_day = monthly_config.get('day', 1)
        schedule_time = monthly_config.get('time', '00:00')
        sources = monthly_config.get('extractions', [])
        
        schedule.every().day.at(schedule_time).do(
            self._run_monthly_extraction_check,
            target_day=schedule_day,
            sources=sources
        )
        
        logger.info(
            f"Scheduled monthly extraction on day {schedule_day} at {schedule_time} "
            f"for sources: {sources}"
        )
    
    def _run_daily_extraction(self, sources: List[str]):
        """Execute daily incremental extraction."""
        logger.info("=== Starting Daily Extraction Job ===")
        
        try:
            # Calculate date range (yesterday's data)
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Handle 'all' sources
            if 'all' in sources:
                sources = None
            
            # Run pipeline
            result = self.pipeline.run_full_pipeline(
                sources=sources,
                start_date=start_date,
                end_date=end_date,
                incremental=True,
                stop_on_validation_failure=False
            )
            
            logger.info(f"Daily extraction completed: {result['status']}")
            
            # Check for alerts
            alerts = self.alert_manager.check_alert_conditions(
                result.get('validation_summary', {}),
                result
            )
            
            for alert in alerts:
                self.alert_manager.send_alert(alert)
            
        except Exception as e:
            logger.error(f"Daily extraction failed: {str(e)}", exc_info=True)
            
            # Send failure alert
            self.alert_manager.send_alert({
                'type': 'extraction_failure',
                'severity': 'high',
                'message': f"Daily extraction failed: {str(e)}",
                'details': {'error': str(e)}
            })
    
    def _run_weekly_extraction(self, sources: List[str]):
        """Execute weekly full extraction."""
        logger.info("=== Starting Weekly Full Extraction Job ===")
        
        try:
            # Calculate date range (last 7 days)
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            # Handle 'all' sources
            if 'all' in sources:
                sources = None
            
            # Run pipeline with full extraction
            result = self.pipeline.run_full_pipeline(
                sources=sources,
                start_date=start_date,
                end_date=end_date,
                incremental=False,  # Full extraction
                stop_on_validation_failure=False
            )
            
            logger.info(f"Weekly extraction completed: {result['status']}")
            
            # Check for alerts
            alerts = self.alert_manager.check_alert_conditions(
                result.get('validation_summary', {}),
                result
            )
            
            for alert in alerts:
                self.alert_manager.send_alert(alert)
            
        except Exception as e:
            logger.error(f"Weekly extraction failed: {str(e)}", exc_info=True)
            
            self.alert_manager.send_alert({
                'type': 'extraction_failure',
                'severity': 'high',
                'message': f"Weekly extraction failed: {str(e)}",
                'details': {'error': str(e)}
            })
    
    def _run_monthly_extraction_check(self, target_day: int, sources: List[str]):
        """Check if today is the scheduled monthly extraction day."""
        today = datetime.now().day
        
        if today == target_day:
            logger.info("=== Starting Monthly Reference Data Refresh ===")
            
            try:
                # Run extraction for reference data only
                result = self.pipeline.run_full_pipeline(
                    sources=sources if 'all' not in sources else None,
                    incremental=False,
                    stop_on_validation_failure=False
                )
                
                logger.info(f"Monthly extraction completed: {result['status']}")
                
            except Exception as e:
                logger.error(f"Monthly extraction failed: {str(e)}", exc_info=True)
                
                self.alert_manager.send_alert({
                    'type': 'extraction_failure',
                    'severity': 'medium',
                    'message': f"Monthly extraction failed: {str(e)}",
                    'details': {'error': str(e)}
                })
    
    def run_custom_job(
        self,
        job_func: Callable,
        schedule_time: str,
        job_name: str = "custom_job"
    ):
        """
        Schedule a custom job.
        
        Args:
            job_func: Function to execute
            schedule_time: Time to run (HH:MM format)
            job_name: Name of the job for logging
        """
        schedule.every().day.at(schedule_time).do(job_func)
        logger.info(f"Scheduled custom job '{job_name}' at {schedule_time}")
    
    def start(self, run_immediately: bool = False):
        """
        Start the scheduler.
        
        Args:
            run_immediately: Run all jobs immediately on start
        """
        logger.info("Starting extraction scheduler...")
        
        # Set up all scheduled jobs
        self.schedule_daily_extraction()
        self.schedule_weekly_extraction()
        self.schedule_monthly_extraction()
        
        # Run immediately if requested
        if run_immediately:
            logger.info("Running all jobs immediately...")
            schedule.run_all()
        
        # Show next run times
        logger.info("Scheduled jobs:")
        for job in schedule.get_jobs():
            logger.info(f"  - Next run: {job.next_run}")
        
        # Main scheduler loop
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
        except Exception as e:
            logger.error(f"Scheduler error: {str(e)}", exc_info=True)
            raise
    
    def stop(self):
        """Stop the scheduler and clear all jobs."""
        schedule.clear()
        logger.info("Scheduler stopped and all jobs cleared")


def main():
    """Main entry point for scheduler."""
    # Setup logging
    setup_logging(
        log_level='INFO',
        log_dir='logs',
        enable_console=True,
        enable_file=True
    )
    
    logger.info("="*70)
    logger.info("MOH Data Extraction Scheduler")
    logger.info("="*70)
    
    # Initialize and start scheduler
    scheduler = ExtractionScheduler()
    scheduler.start(run_immediately=False)


if __name__ == '__main__':
    main()
