"""
Celery Configuration and Background Task System
"""

import os
import logging
from celery import Celery
from celery.schedules import crontab
from typing import Dict, Any, Optional

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create Celery instance
celery_app = Celery(
    "kali_social_media_scraper",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.investigation_tasks",
        "app.tasks.scraping_tasks", 
        "app.tasks.analysis_tasks",
        "app.tasks.report_tasks",
        "app.tasks.maintenance_tasks"
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task routing
    task_routes={
        "app.tasks.investigation_tasks.*": {"queue": "investigations"},
        "app.tasks.scraping_tasks.*": {"queue": "scraping"},
        "app.tasks.analysis_tasks.*": {"queue": "analysis"},
        "app.tasks.report_tasks.*": {"queue": "reports"},
        "app.tasks.maintenance_tasks.*": {"queue": "maintenance"},
    },
    
    # Task serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Task execution
    task_always_eager=False,
    task_eager_propagates=True,
    task_ignore_result=False,
    task_store_errors_even_if_ignored=True,
    
    # Worker configuration
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    worker_disable_rate_limits=False,
    
    # Task timeouts
    task_soft_time_limit=3600,  # 1 hour
    task_time_limit=7200,       # 2 hours
    
    # Result backend
    result_expires=86400,  # 24 hours
    result_persistent=True,
    
    # Beat schedule for periodic tasks
    beat_schedule={
        "cleanup-old-results": {
            "task": "app.tasks.maintenance_tasks.cleanup_old_results",
            "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM
        },
        "update-platform-status": {
            "task": "app.tasks.maintenance_tasks.update_platform_status",
            "schedule": crontab(hour="*/2"),  # Every 2 hours instead of every 30 minutes
        },
        "health-check": {
            "task": "app.tasks.maintenance_tasks.health_check",
            "schedule": crontab(minute="*/30"),  # Every 30 minutes instead of every 15 minutes
        },
        "backup-database": {
            "task": "app.tasks.maintenance_tasks.backup_database",
            "schedule": crontab(hour=3, minute=0),  # Daily at 3 AM
        },
    },
    
    # Task compression
    task_compression="gzip",
    result_compression="gzip",
    
    # Security
    security_key=settings.SECRET_KEY,
    security_certificate=None,
    security_cert_store=None,
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
    
    # Error handling
    task_annotations={
        "*": {
            "rate_limit": "100/m",
            "max_retries": 3,
            "default_retry_delay": 60,
        }
    },
    
    # Queue configuration
    task_default_queue="default",
    task_default_exchange="default",
    task_default_routing_key="default",
    
    # Result backend configuration
    result_backend_transport_options={
        "master_name": "mymaster",
        "visibility_timeout": 3600,
    },
    
    # Broker configuration
    broker_transport_options={
        "visibility_timeout": 3600,
        "fanout_prefix": True,
        "fanout_patterns": True,
    },
)

# Task error handling
@celery_app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery configuration"""
    logger.info(f"Request: {self.request!r}")
    return "Debug task completed"

# Task monitoring
@celery_app.task(bind=True)
def monitor_task(self, task_name: str, **kwargs):
    """Monitor task execution and performance"""
    try:
        logger.info(f"Starting monitored task: {task_name}")
        start_time = self.request.timestamp
        
        # Execute the actual task
        result = self.execute_task(task_name, **kwargs)
        
        end_time = self.request.timestamp
        execution_time = end_time - start_time
        
        logger.info(f"Task {task_name} completed in {execution_time:.2f} seconds")
        
        return {
            "task_name": task_name,
            "status": "completed",
            "execution_time": execution_time,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Task {task_name} failed: {e}")
        raise

def execute_task(self, task_name: str, **kwargs):
    """Execute a specific task by name"""
    # This would be implemented to execute different tasks
    # based on the task_name parameter
    pass

# Health check task
@celery_app.task(bind=True)
def health_check(self):
    """Health check task for monitoring system status"""
    try:
        # Check Redis connection
        redis_info = celery_app.control.inspect().stats()
        
        # Check worker status
        active_workers = celery_app.control.inspect().active()
        registered_workers = celery_app.control.inspect().registered()
        
        health_status = {
            "status": "healthy",
            "timestamp": self.request.timestamp,
            "redis_connected": bool(redis_info),
            "active_workers": len(active_workers) if active_workers else 0,
            "registered_workers": len(registered_workers) if registered_workers else 0,
            "queues": {
                "investigations": self.get_queue_length("investigations"),
                "scraping": self.get_queue_length("scraping"),
                "analysis": self.get_queue_length("analysis"),
                "reports": self.get_queue_length("reports"),
                "maintenance": self.get_queue_length("maintenance"),
            }
        }
        
        logger.info(f"Health check completed: {health_status}")
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": self.request.timestamp
        }

def get_queue_length(self, queue_name: str) -> int:
    """Get the length of a specific queue"""
    try:
        # This would be implemented to get actual queue lengths
        # For now, return a placeholder
        return 0
    except Exception as e:
        logger.error(f"Error getting queue length for {queue_name}: {e}")
        return -1

# Task utilities
def get_task_status(task_id: str) -> Dict[str, Any]:
    """Get the status of a specific task"""
    try:
        result = celery_app.AsyncResult(task_id)
        return {
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.ready() else None,
            "info": result.info if hasattr(result, 'info') else None,
        }
    except Exception as e:
        logger.error(f"Error getting task status for {task_id}: {e}")
        return {
            "task_id": task_id,
            "status": "error",
            "error": str(e)
        }

def cancel_task(task_id: str) -> bool:
    """Cancel a running task"""
    try:
        celery_app.control.revoke(task_id, terminate=True)
        logger.info(f"Task {task_id} cancelled successfully")
        return True
    except Exception as e:
        logger.error(f"Error cancelling task {task_id}: {e}")
        return False

def get_active_tasks() -> Dict[str, Any]:
    """Get all active tasks"""
    try:
        inspect = celery_app.control.inspect()
        active_tasks = inspect.active()
        return active_tasks or {}
    except Exception as e:
        logger.error(f"Error getting active tasks: {e}")
        return {}

def get_scheduled_tasks() -> Dict[str, Any]:
    """Get all scheduled tasks"""
    try:
        inspect = celery_app.control.inspect()
        scheduled_tasks = inspect.scheduled()
        return scheduled_tasks or {}
    except Exception as e:
        logger.error(f"Error getting scheduled tasks: {e}")
        return {}

def get_reserved_tasks() -> Dict[str, Any]:
    """Get all reserved tasks"""
    try:
        inspect = celery_app.control.inspect()
        reserved_tasks = inspect.reserved()
        return reserved_tasks or {}
    except Exception as e:
        logger.error(f"Error getting reserved tasks: {e}")
        return {}

def purge_queues() -> bool:
    """Purge all queues"""
    try:
        celery_app.control.purge()
        logger.info("All queues purged successfully")
        return True
    except Exception as e:
        logger.error(f"Error purging queues: {e}")
        return False

def get_worker_stats() -> Dict[str, Any]:
    """Get worker statistics"""
    try:
        inspect = celery_app.control.inspect()
        stats = inspect.stats()
        return stats or {}
    except Exception as e:
        logger.error(f"Error getting worker stats: {e}")
        return {}

# Task decorators for common functionality
def with_retry(max_retries: int = 3, retry_delay: int = 60):
    """Decorator for tasks with automatic retry"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Task {func.__name__} failed: {e}")
                # This would be implemented to retry the task
                raise
        return wrapper
    return decorator

def with_monitoring(func):
    """Decorator for task monitoring"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"Task {func.__name__} completed in {execution_time:.2f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Task {func.__name__} failed after {execution_time:.2f} seconds: {e}")
            raise
    return wrapper

# Import time for task modules
import time 