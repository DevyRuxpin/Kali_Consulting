from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.celery_app import celery_app
import redis
import psutil
import os
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring and deployment."""
    try:
        # Check database connection
        db = next(get_db())
        db.execute("SELECT 1")
        db.close()
        
        # Check Redis connection
        redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        redis_client.ping()
        
        # Check Celery worker status
        celery_stats = celery_app.control.inspect().stats()
        
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
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
        "timestamp": datetime.utcnow().isoformat(),
        "components": {}
    }
    
    # Database health
    try:
        db = next(get_db())
        db.execute("SELECT 1")
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