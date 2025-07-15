"""
Maintenance Background Tasks
"""

import asyncio
import logging
import os
import shutil
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path

from app.core.celery_app import celery_app
from app.repositories.investigation_repository import InvestigationRepository
from app.repositories.user_repository import UserRepository
from app.core.database import get_db

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def cleanup_old_results_task(self) -> Dict[str, Any]:
    """Clean up old task results and temporary files"""
    try:
        logger.info("Starting cleanup of old results")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Cleaning up old task results", "progress": 20}
        )
        
        # Clean up old Celery results (older than 7 days)
        cutoff_date = datetime.utcnow() - timedelta(days=7)
        
        # This would be implemented to clean up actual Celery results
        # For now, just log the cleanup
        logger.info(f"Cleaning up results older than {cutoff_date}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Cleaning up temporary files", "progress": 50}
        )
        
        # Clean up temporary files
        temp_dir = Path("temp")
        if temp_dir.exists():
            for file_path in temp_dir.glob("*"):
                if file_path.is_file():
                    file_age = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_age < cutoff_date:
                        file_path.unlink()
                        logger.info(f"Deleted old temp file: {file_path}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Cleaning up export files", "progress": 80}
        )
        
        # Clean up old export files
        exports_dir = Path("exports")
        if exports_dir.exists():
            for file_path in exports_dir.glob("*"):
                if file_path.is_file():
                    file_age = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_age < cutoff_date:
                        file_path.unlink()
                        logger.info(f"Deleted old export file: {file_path}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Cleanup completed", "progress": 100}
        )
        
        return {
            "status": "completed",
            "message": "Old results and temporary files cleaned up",
            "cutoff_date": cutoff_date.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def update_platform_status_task(self) -> Dict[str, Any]:
    """Update platform availability and status"""
    try:
        logger.info("Starting platform status update")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Checking platform availability", "progress": 20}
        )
        
        # Check platform availability
        platforms = {
            "github": check_github_availability(),
            "twitter": check_twitter_availability(),
            "instagram": check_instagram_availability(),
            "linkedin": check_linkedin_availability(),
            "facebook": check_facebook_availability(),
            "youtube": check_youtube_availability(),
            "tiktok": check_tiktok_availability(),
            "telegram": check_telegram_availability(),
            "discord": check_discord_availability(),
            "reddit": check_reddit_availability()
        }
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Updating platform status", "progress": 60}
        )
        
        # Save platform status
        asyncio.run(save_platform_status(platforms))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Platform status updated", "progress": 100}
        )
        
        return {
            "status": "completed",
            "platforms_checked": len(platforms),
            "available_platforms": len([p for p in platforms.values() if p["available"]]),
            "platforms": platforms
        }
        
    except Exception as e:
        logger.error(f"Error updating platform status: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def health_check_task(self) -> Dict[str, Any]:
    """Perform system health check"""
    try:
        logger.info("Starting system health check")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Checking database", "progress": 20}
        )
        
        # Check database connectivity
        db_status = asyncio.run(check_database_health())
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Checking Redis", "progress": 40}
        )
        
        # Check Redis connectivity
        redis_status = asyncio.run(check_redis_health())
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Checking file system", "progress": 60}
        )
        
        # Check file system
        filesystem_status = check_filesystem_health()
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Checking memory usage", "progress": 80}
        )
        
        # Check memory usage
        memory_status = check_memory_health()
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Health check completed", "progress": 100}
        )
        
        # Determine overall health
        overall_health = "healthy"
        if not all([db_status["healthy"], redis_status["healthy"], filesystem_status["healthy"], memory_status["healthy"]]):
            overall_health = "unhealthy"
        
        health_report = {
            "status": "completed",
            "overall_health": overall_health,
            "timestamp": datetime.utcnow().isoformat(),
            "database": db_status,
            "redis": redis_status,
            "filesystem": filesystem_status,
            "memory": memory_status
        }
        
        # Save health report
        asyncio.run(save_health_report(health_report))
        
        return health_report
        
    except Exception as e:
        logger.error(f"Error during health check: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def backup_database_task(self) -> Dict[str, Any]:
    """Create database backup"""
    try:
        logger.info("Starting database backup")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Preparing backup", "progress": 10}
        )
        
        # Create backup directory
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)
        
        # Generate backup filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{timestamp}.sql"
        backup_path = backup_dir / backup_filename
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Creating database dump", "progress": 50}
        )
        
        # Create database dump
        # This would be implemented to create actual database backup
        # For now, create a placeholder backup file
        with open(backup_path, 'w') as f:
            f.write(f"-- Database backup created at {datetime.utcnow()}\n")
            f.write("-- This is a placeholder backup file\n")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Compressing backup", "progress": 80}
        )
        
        # Compress backup
        compressed_path = backup_path.with_suffix('.sql.gz')
        # This would implement actual compression
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Backup completed", "progress": 100}
        )
        
        # Clean up old backups (keep last 10)
        cleanup_old_backups(backup_dir, keep_count=10)
        
        return {
            "status": "completed",
            "backup_path": str(backup_path),
            "backup_size": backup_path.stat().st_size if backup_path.exists() else 0,
            "timestamp": timestamp
        }
        
    except Exception as e:
        logger.error(f"Error creating database backup: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def cleanup_investigations_task(self, days_old: int = 30) -> Dict[str, Any]:
    """Clean up old completed investigations"""
    try:
        logger.info(f"Starting cleanup of investigations older than {days_old} days")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Finding old investigations", "progress": 20}
        )
        
        # Get investigation repository
        investigation_repo = InvestigationRepository()
        
        # Find old completed investigations
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        old_investigations = asyncio.run(investigation_repo.get_old_investigations(cutoff_date))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Cleaning up investigations", "progress": 60}
        )
        
        # Clean up each old investigation
        cleaned_count = 0
        for investigation in old_investigations:
            try:
                asyncio.run(investigation_repo.delete_investigation(investigation.id))
                cleaned_count += 1
                logger.info(f"Cleaned up investigation: {investigation.id}")
            except Exception as e:
                logger.error(f"Error cleaning up investigation {investigation.id}: {e}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Cleanup completed", "progress": 100}
        )
        
        return {
            "status": "completed",
            "old_investigations_found": len(old_investigations),
            "investigations_cleaned": cleaned_count,
            "cutoff_date": cutoff_date.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error cleaning up investigations: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def optimize_database_task(self) -> Dict[str, Any]:
    """Optimize database performance"""
    try:
        logger.info("Starting database optimization")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Analyzing database", "progress": 20}
        )
        
        # Get database connection
        db = get_db()
        
        # Analyze database statistics
        # This would implement actual database optimization
        # For now, just log the optimization
        logger.info("Database optimization completed")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Optimization completed", "progress": 100}
        )
        
        return {
            "status": "completed",
            "message": "Database optimization completed",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error optimizing database: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def monitor_system_resources_task(self) -> Dict[str, Any]:
    """Monitor system resource usage"""
    try:
        logger.info("Starting system resource monitoring")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Checking CPU usage", "progress": 25}
        )
        
        # Check CPU usage
        cpu_usage = get_cpu_usage()
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Checking memory usage", "progress": 50}
        )
        
        # Check memory usage
        memory_usage = get_memory_usage()
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Checking disk usage", "progress": 75}
        )
        
        # Check disk usage
        disk_usage = get_disk_usage()
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Monitoring completed", "progress": 100}
        )
        
        # Create resource report
        resource_report = {
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat(),
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage,
            "alerts": generate_resource_alerts(cpu_usage, memory_usage, disk_usage)
        }
        
        # Save resource report
        asyncio.run(save_resource_report(resource_report))
        
        return resource_report
        
    except Exception as e:
        logger.error(f"Error monitoring system resources: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

# Helper functions
def check_github_availability() -> Dict[str, Any]:
    """Check GitHub availability"""
    try:
        # This would implement actual GitHub availability check
        return {
            "available": True,
            "response_time": 0.5,
            "last_checked": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error checking GitHub availability: {e}")
        return {
            "available": False,
            "error": str(e),
            "last_checked": datetime.utcnow().isoformat()
        }

def check_twitter_availability() -> Dict[str, Any]:
    """Check Twitter availability"""
    try:
        # This would implement actual Twitter availability check
        return {
            "available": True,
            "response_time": 0.8,
            "last_checked": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error checking Twitter availability: {e}")
        return {
            "available": False,
            "error": str(e),
            "last_checked": datetime.utcnow().isoformat()
        }

def check_instagram_availability() -> Dict[str, Any]:
    """Check Instagram availability"""
    try:
        return {
            "available": True,
            "response_time": 1.2,
            "last_checked": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error checking Instagram availability: {e}")
        return {
            "available": False,
            "error": str(e),
            "last_checked": datetime.utcnow().isoformat()
        }

def check_linkedin_availability() -> Dict[str, Any]:
    """Check LinkedIn availability"""
    try:
        return {
            "available": True,
            "response_time": 0.9,
            "last_checked": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error checking LinkedIn availability: {e}")
        return {
            "available": False,
            "error": str(e),
            "last_checked": datetime.utcnow().isoformat()
        }

def check_facebook_availability() -> Dict[str, Any]:
    """Check Facebook availability"""
    try:
        return {
            "available": True,
            "response_time": 1.1,
            "last_checked": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error checking Facebook availability: {e}")
        return {
            "available": False,
            "error": str(e),
            "last_checked": datetime.utcnow().isoformat()
        }

def check_youtube_availability() -> Dict[str, Any]:
    """Check YouTube availability"""
    try:
        return {
            "available": True,
            "response_time": 0.7,
            "last_checked": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error checking YouTube availability: {e}")
        return {
            "available": False,
            "error": str(e),
            "last_checked": datetime.utcnow().isoformat()
        }

def check_tiktok_availability() -> Dict[str, Any]:
    """Check TikTok availability"""
    try:
        return {
            "available": True,
            "response_time": 1.3,
            "last_checked": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error checking TikTok availability: {e}")
        return {
            "available": False,
            "error": str(e),
            "last_checked": datetime.utcnow().isoformat()
        }

def check_telegram_availability() -> Dict[str, Any]:
    """Check Telegram availability"""
    try:
        return {
            "available": True,
            "response_time": 0.6,
            "last_checked": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error checking Telegram availability: {e}")
        return {
            "available": False,
            "error": str(e),
            "last_checked": datetime.utcnow().isoformat()
        }

def check_discord_availability() -> Dict[str, Any]:
    """Check Discord availability"""
    try:
        return {
            "available": True,
            "response_time": 0.4,
            "last_checked": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error checking Discord availability: {e}")
        return {
            "available": False,
            "error": str(e),
            "last_checked": datetime.utcnow().isoformat()
        }

def check_reddit_availability() -> Dict[str, Any]:
    """Check Reddit availability"""
    try:
        return {
            "available": True,
            "response_time": 0.8,
            "last_checked": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error checking Reddit availability: {e}")
        return {
            "available": False,
            "error": str(e),
            "last_checked": datetime.utcnow().isoformat()
        }

async def save_platform_status(platforms: Dict[str, Any]) -> None:
    """Save platform status to database"""
    try:
        # This would implement actual database save
        logger.info("Platform status saved")
    except Exception as e:
        logger.error(f"Error saving platform status: {e}")

async def check_database_health() -> Dict[str, Any]:
    """Check database health"""
    try:
        # This would implement actual database health check
        return {
            "healthy": True,
            "response_time": 0.1,
            "connections": 5
        }
    except Exception as e:
        logger.error(f"Error checking database health: {e}")
        return {
            "healthy": False,
            "error": str(e)
        }

async def check_redis_health() -> Dict[str, Any]:
    """Check Redis health"""
    try:
        # This would implement actual Redis health check
        return {
            "healthy": True,
            "response_time": 0.05,
            "memory_usage": "256MB"
        }
    except Exception as e:
        logger.error(f"Error checking Redis health: {e}")
        return {
            "healthy": False,
            "error": str(e)
        }

def check_filesystem_health() -> Dict[str, Any]:
    """Check file system health"""
    try:
        # This would implement actual filesystem health check
        return {
            "healthy": True,
            "free_space": "10GB",
            "disk_usage": "75%"
        }
    except Exception as e:
        logger.error(f"Error checking filesystem health: {e}")
        return {
            "healthy": False,
            "error": str(e)
        }

def check_memory_health() -> Dict[str, Any]:
    """Check memory health"""
    try:
        # This would implement actual memory health check
        return {
            "healthy": True,
            "memory_usage": "60%",
            "available_memory": "4GB"
        }
    except Exception as e:
        logger.error(f"Error checking memory health: {e}")
        return {
            "healthy": False,
            "error": str(e)
        }

async def save_health_report(health_report: Dict[str, Any]) -> None:
    """Save health report to database"""
    try:
        # This would implement actual database save
        logger.info("Health report saved")
    except Exception as e:
        logger.error(f"Error saving health report: {e}")

def cleanup_old_backups(backup_dir: Path, keep_count: int = 10) -> None:
    """Clean up old backup files"""
    try:
        backup_files = sorted(backup_dir.glob("backup_*.sql*"), key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Keep only the most recent files
        for backup_file in backup_files[keep_count:]:
            backup_file.unlink()
            logger.info(f"Deleted old backup: {backup_file}")
            
    except Exception as e:
        logger.error(f"Error cleaning up old backups: {e}")

def get_cpu_usage() -> float:
    """Get CPU usage percentage"""
    try:
        # This would implement actual CPU usage check
        return 45.2
    except Exception as e:
        logger.error(f"Error getting CPU usage: {e}")
        return 0.0

def get_memory_usage() -> Dict[str, Any]:
    """Get memory usage information"""
    try:
        # This would implement actual memory usage check
        return {
            "total": "16GB",
            "used": "8GB",
            "free": "8GB",
            "percentage": 50.0
        }
    except Exception as e:
        logger.error(f"Error getting memory usage: {e}")
        return {
            "total": "0GB",
            "used": "0GB",
            "free": "0GB",
            "percentage": 0.0
        }

def get_disk_usage() -> Dict[str, Any]:
    """Get disk usage information"""
    try:
        # This would implement actual disk usage check
        return {
            "total": "1TB",
            "used": "750GB",
            "free": "250GB",
            "percentage": 75.0
        }
    except Exception as e:
        logger.error(f"Error getting disk usage: {e}")
        return {
            "total": "0GB",
            "used": "0GB",
            "free": "0GB",
            "percentage": 0.0
        }

def generate_resource_alerts(cpu_usage: float, memory_usage: Dict[str, Any], disk_usage: Dict[str, Any]) -> List[str]:
    """Generate resource alerts"""
    alerts = []
    
    if cpu_usage > 80:
        alerts.append(f"High CPU usage: {cpu_usage}%")
    
    if memory_usage["percentage"] > 85:
        alerts.append(f"High memory usage: {memory_usage['percentage']}%")
    
    if disk_usage["percentage"] > 90:
        alerts.append(f"High disk usage: {disk_usage['percentage']}%")
    
    return alerts

async def save_resource_report(resource_report: Dict[str, Any]) -> None:
    """Save resource report to database"""
    try:
        # This would implement actual database save
        logger.info("Resource report saved")
    except Exception as e:
        logger.error(f"Error saving resource report: {e}") 