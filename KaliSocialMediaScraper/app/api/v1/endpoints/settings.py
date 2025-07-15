"""
Settings API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.utils.time_utils import get_current_time_iso
from app.core.database import get_db

router = APIRouter()

# Default platform settings - these could be moved to a database table in the future
DEFAULT_SETTINGS = {
    "max_concurrent_scrapers": 5,
    "rate_limiting_enabled": True,
    "proxy_rotation_enabled": True,
    "data_retention_days": 90,
    "threat_detection_sensitivity": "medium",
    "auto_export_enabled": False,
    "notification_enabled": True,
    "dark_web_monitoring": False,
    "ml_analysis_enabled": True,
    "max_investigations_per_user": 100,
    "scraping_timeout_seconds": 300,
    "max_profiles_per_investigation": 1000,
    "threat_score_threshold": 0.7,
    "auto_cleanup_enabled": True,
    "backup_enabled": True
}

@router.get("/", response_model=Dict[str, Any])
async def get_settings():
    """Get platform settings"""
    try:
        # In a production environment, these settings would be stored in a database
        # For now, we return the default settings
        return {
            "status": "success",
            "settings": DEFAULT_SETTINGS,
            "timestamp": get_current_time_iso()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting settings: {str(e)}")

@router.put("/", response_model=Dict[str, Any])
async def update_settings(settings: Dict[str, Any]):
    """Update platform settings"""
    try:
        # Validate and sanitize settings
        valid_settings = {}
        
        # Validate each setting type
        if "max_concurrent_scrapers" in settings:
            value = settings["max_concurrent_scrapers"]
            if isinstance(value, int) and 1 <= value <= 20:
                valid_settings["max_concurrent_scrapers"] = value
        
        if "rate_limiting_enabled" in settings:
            valid_settings["rate_limiting_enabled"] = bool(settings["rate_limiting_enabled"])
        
        if "proxy_rotation_enabled" in settings:
            valid_settings["proxy_rotation_enabled"] = bool(settings["proxy_rotation_enabled"])
        
        if "data_retention_days" in settings:
            value = settings["data_retention_days"]
            if isinstance(value, int) and 1 <= value <= 365:
                valid_settings["data_retention_days"] = value
        
        if "threat_detection_sensitivity" in settings:
            value = settings["threat_detection_sensitivity"]
            if value in ["low", "medium", "high", "critical"]:
                valid_settings["threat_detection_sensitivity"] = value
        
        if "auto_export_enabled" in settings:
            valid_settings["auto_export_enabled"] = bool(settings["auto_export_enabled"])
        
        if "notification_enabled" in settings:
            valid_settings["notification_enabled"] = bool(settings["notification_enabled"])
        
        if "dark_web_monitoring" in settings:
            valid_settings["dark_web_monitoring"] = bool(settings["dark_web_monitoring"])
        
        if "ml_analysis_enabled" in settings:
            valid_settings["ml_analysis_enabled"] = bool(settings["ml_analysis_enabled"])
        
        if "max_investigations_per_user" in settings:
            value = settings["max_investigations_per_user"]
            if isinstance(value, int) and 1 <= value <= 1000:
                valid_settings["max_investigations_per_user"] = value
        
        if "scraping_timeout_seconds" in settings:
            value = settings["scraping_timeout_seconds"]
            if isinstance(value, int) and 60 <= value <= 3600:
                valid_settings["scraping_timeout_seconds"] = value
        
        if "max_profiles_per_investigation" in settings:
            value = settings["max_profiles_per_investigation"]
            if isinstance(value, int) and 1 <= value <= 10000:
                valid_settings["max_profiles_per_investigation"] = value
        
        if "threat_score_threshold" in settings:
            value = settings["threat_score_threshold"]
            if isinstance(value, (int, float)) and 0.0 <= value <= 1.0:
                valid_settings["threat_score_threshold"] = float(value)
        
        if "auto_cleanup_enabled" in settings:
            valid_settings["auto_cleanup_enabled"] = bool(settings["auto_cleanup_enabled"])
        
        if "backup_enabled" in settings:
            valid_settings["backup_enabled"] = bool(settings["backup_enabled"])
        
        # In a production environment, these settings would be saved to a database
        # For now, we just return the validated settings
        
        return {
            "status": "success",
            "settings": valid_settings,
            "message": f"Updated {len(valid_settings)} settings successfully",
            "timestamp": get_current_time_iso()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating settings: {str(e)}")

@router.get("/system-info", response_model=Dict[str, Any])
async def get_system_info():
    """Get system information and capabilities"""
    try:
        import psutil
        import os
        
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "status": "success",
            "system_info": {
                "platform": os.name,
                "python_version": os.sys.version,
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "disk_usage": disk.percent,
                "available_memory_gb": memory.available / (1024**3),
                "available_disk_gb": disk.free / (1024**3)
            },
            "capabilities": {
                "social_media_scraping": True,
                "domain_analysis": True,
                "threat_detection": True,
                "ml_analysis": True,
                "export_functionality": True,
                "real_time_monitoring": True
            },
            "timestamp": get_current_time_iso()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting system info: {str(e)}") 