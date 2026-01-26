"""
Performance Monitor for MOH Data Extraction System
Version: 1.0
Created: 2026-01-26

Monitors and tracks:
- Execution times
- Memory usage
- Row counts
- Success/failure rates
"""

import time
import psutil
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from functools import wraps
from pathlib import Path
import json


logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """
    Monitors performance metrics for data extraction operations.
    """
    
    def __init__(self):
        self.metrics = []
        self.start_time = None
        self.process = psutil.Process()
    
    def start_monitoring(self, operation: str, details: Optional[Dict] = None):
        """Start monitoring an operation."""
        self.start_time = time.time()
        
        metric = {
            'operation': operation,
            'start_time': datetime.now().isoformat(),
            'start_memory_mb': self.process.memory_info().rss / 1024 / 1024,
            'start_cpu_percent': self.process.cpu_percent(),
            'details': details or {}
        }
        
        logger.debug(f"Started monitoring: {operation}")
        return metric
    
    def stop_monitoring(self, metric: Dict, status: str = 'success', error: Optional[str] = None):
        """Stop monitoring and record results."""
        end_time = time.time()
        duration = end_time - self.start_time if self.start_time else 0
        
        metric.update({
            'end_time': datetime.now().isoformat(),
            'duration_seconds': round(duration, 2),
            'end_memory_mb': self.process.memory_info().rss / 1024 / 1024,
            'peak_memory_mb': self.process.memory_info().rss / 1024 / 1024,
            'cpu_percent': self.process.cpu_percent(),
            'status': status,
            'error': error
        })
        
        self.metrics.append(metric)
        
        logger.info(
            f"Completed {metric['operation']}: "
            f"{duration:.2f}s, {metric['end_memory_mb']:.1f}MB"
        )
        
        return metric
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        if not self.metrics:
            return {}
        
        total_duration = sum(m['duration_seconds'] for m in self.metrics)
        successful = sum(1 for m in self.metrics if m['status'] == 'success')
        
        return {
            'total_operations': len(self.metrics),
            'successful': successful,
            'failed': len(self.metrics) - successful,
            'total_duration_seconds': round(total_duration, 2),
            'average_duration_seconds': round(total_duration / len(self.metrics), 2),
            'peak_memory_mb': max(m['peak_memory_mb'] for m in self.metrics),
            'operations': self.metrics
        }
    
    def save_metrics(self, output_path: Optional[str] = None):
        """Save metrics to file."""
        if not output_path:
            output_dir = Path('results/metrics')
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        summary = self.get_summary()
        
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Performance metrics saved to: {output_path}")
        return output_path


def monitor_performance(operation_name: str = None):
    """
    Decorator to monitor function performance.
    
    Args:
        operation_name: Name of the operation (defaults to function name)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            op_name = operation_name or func.__name__
            monitor = PerformanceMonitor()
            
            metric = monitor.start_monitoring(op_name)
            
            try:
                result = func(*args, **kwargs)
                monitor.stop_monitoring(metric, status='success')
                return result
            except Exception as e:
                monitor.stop_monitoring(metric, status='failed', error=str(e))
                raise
        
        return wrapper
    return decorator


class AlertManager:
    """
    Manages alerts for data extraction issues.
    """
    
    def __init__(self, config_path: str = 'config/database.yml'):
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.alert_config = config.get('monitoring', {}).get('alerts', {})
        self.notifications = config.get('monitoring', {}).get('notifications', {})
    
    def check_alert_conditions(
        self,
        validation_results: Dict,
        extraction_metrics: Dict
    ) -> List[Dict[str, Any]]:
        """
        Check if any alert conditions are met.
        
        Args:
            validation_results: Validation results from validator
            extraction_metrics: Extraction metrics
            
        Returns:
            List of alerts to be sent
        """
        alerts = []
        
        # Check for extraction failures
        if self.alert_config.get('extraction_failure', True):
            if extraction_metrics.get('status') == 'failed':
                alerts.append({
                    'type': 'extraction_failure',
                    'severity': 'high',
                    'message': f"Data extraction failed: {extraction_metrics.get('error')}",
                    'details': extraction_metrics
                })
        
        # Check for quality check failures
        if self.alert_config.get('quality_check_failure', True):
            for source, results in validation_results.items():
                if results.get('failed', 0) > 0:
                    alerts.append({
                        'type': 'quality_check_failure',
                        'severity': 'medium',
                        'message': f"Quality checks failed for {source}",
                        'details': results
                    })
        
        # Check for row count deviation
        if 'row_count_deviation' in self.alert_config:
            # This would compare with historical averages
            pass
        
        return alerts
    
    def send_alert(self, alert: Dict[str, Any]):
        """
        Send an alert through configured channels.
        
        Args:
            alert: Alert dictionary with type, severity, message, details
        """
        logger.warning(f"ALERT [{alert['severity']}]: {alert['message']}")
        
        # Email notification
        if self.notifications.get('email'):
            self._send_email_alert(alert)
        
        # Slack notification
        if self.notifications.get('slack'):
            self._send_slack_alert(alert)
        
        # Teams notification
        if self.notifications.get('teams'):
            self._send_teams_alert(alert)
    
    def _send_email_alert(self, alert: Dict):
        """Send email alert (placeholder)."""
        logger.info(f"Would send email alert: {alert['message']}")
        # Implementation would use SMTP or email service API
    
    def _send_slack_alert(self, alert: Dict):
        """Send Slack alert (placeholder)."""
        logger.info(f"Would send Slack alert: {alert['message']}")
        # Implementation would use Slack webhook or API
    
    def _send_teams_alert(self, alert: Dict):
        """Send Microsoft Teams alert (placeholder)."""
        logger.info(f"Would send Teams alert: {alert['message']}")
        # Implementation would use Teams webhook
