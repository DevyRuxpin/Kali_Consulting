from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.core.celery_app import celery_app
import redis
import psutil
import os
from datetime import datetime
from app.utils.time_utils import get_current_time_iso

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring and deployment."""
    try:
        # Check database connection
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()
        
        # Check Redis connection
        redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        redis_client.ping()
        
        # Check Celery worker status
        celery_stats = celery_app.control.inspect().stats()
        
        # System metrics - use cached values to reduce CPU usage
        # Only measure CPU if not recently measured
        import time
        current_time = time.time()
        
        # Cache CPU measurement for 30 seconds
        if not hasattr(health_check, '_last_cpu_check') or current_time - getattr(health_check, '_last_cpu_check', 0) > 30:
            cpu_percent = psutil.cpu_percent(interval=0.1)  # Reduced interval
            health_check._last_cpu_check = current_time
            health_check._cached_cpu_percent = cpu_percent
        else:
            cpu_percent = getattr(health_check, '_cached_cpu_percent', 0)
        
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "status": "healthy",
            "timestamp": get_current_time_iso(),
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "services": {
                "database": "healthy",
                "redis": "healthy",
                "celery": "healthy" if celery_stats else "unhealthy"
            },
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "disk_percent": disk.percent
            }
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with component status."""
    health_status = {
        "status": "healthy",
        "timestamp": get_current_time_iso(),
        "components": {}
    }
    
    # Database health
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()
        health_status["components"]["database"] = {"status": "healthy", "message": "Connected"}
    except Exception as e:
        health_status["components"]["database"] = {"status": "unhealthy", "message": str(e)}
        health_status["status"] = "unhealthy"
    
    # Redis health
    try:
        redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        redis_client.ping()
        health_status["components"]["redis"] = {"status": "healthy", "message": "Connected"}
    except Exception as e:
        health_status["components"]["redis"] = {"status": "unhealthy", "message": str(e)}
        health_status["status"] = "unhealthy"
    
    # Celery health
    try:
        celery_stats = celery_app.control.inspect().stats()
        if celery_stats:
            health_status["components"]["celery"] = {"status": "healthy", "message": "Workers available"}
        else:
            health_status["components"]["celery"] = {"status": "unhealthy", "message": "No workers available"}
            health_status["status"] = "unhealthy"
    except Exception as e:
        health_status["components"]["celery"] = {"status": "unhealthy", "message": str(e)}
        health_status["status"] = "unhealthy"
    
    # System health
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_status["components"]["system"] = {
            "status": "healthy",
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "disk_percent": disk.percent
        }
        
        # Check if system resources are critical
        if cpu_percent > 90 or memory.percent > 90 or disk.percent > 90:
            health_status["components"]["system"]["status"] = "warning"
            health_status["components"]["system"]["message"] = "High resource usage"
    except Exception as e:
        health_status["components"]["system"] = {"status": "unhealthy", "message": str(e)}
        health_status["status"] = "unhealthy"
    
    return health_status 