"""
Settings API endpoints for platform configuration
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import logging
from datetime import datetime

from app.core.database import get_db
from app.models.schemas import User

logger = logging.getLogger(__name__)
router = APIRouter()

# Settings storage (in production, this would be in database)
PLATFORM_SETTINGS: Dict[str, Dict[str, Any]] = {
    "scraping": {
        "enableUserAgentRotation": True,
        "enableProxyRotation": False,
        "enableRandomDelays": True,
        "defaultDelayMin": 2,
        "defaultDelayMax": 5,
        "maxRetries": 3,
        "timeoutSeconds": 30
    },
    "proxy": {
        "enabled": False,
        "proxyList": [],
        "rotationInterval": 60,
        "authentication": {
            "username": "",
            "password": ""
        }
    },
    "rateLimits": {
        "requestsPerMinute": 60,
        "requestsPerHour": 1000,
        "requestsPerDay": 10000,
        "enableRateLimiting": True
    },
    "security": {
        "enableThreatDetection": True,
        "enableAnomalyDetection": True,
        "threatScoreThreshold": 0.7,
        "enableAutoBlocking": False
    },
    "notifications": {
        "emailNotifications": False,
        "webhookNotifications": False,
        "webhookUrl": "",
        "notificationLevel": "high"
    }
}

@router.get("/settings")
async def get_settings(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get platform settings"""
    try:
        if category:
            if category not in PLATFORM_SETTINGS:
                raise HTTPException(status_code=404, detail=f"Settings category '{category}' not found")
            return {
                "category": category,
                "settings": PLATFORM_SETTINGS[category],
                "last_updated": datetime.utcnow().isoformat()
            }
        else:
            return {
                "settings": PLATFORM_SETTINGS,
                "last_updated": datetime.utcnow().isoformat()
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/settings/{category}")
async def update_settings(
    category: str,
    settings: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update platform settings for a specific category"""
    try:
        if category not in PLATFORM_SETTINGS:
            raise HTTPException(status_code=404, detail=f"Settings category '{category}' not found")
        
        # Validate and update settings
        if category == "scraping":
            PLATFORM_SETTINGS[category].update({
                "enableUserAgentRotation": settings.get("enableUserAgentRotation", True),
                "enableProxyRotation": settings.get("enableProxyRotation", False),
                "enableRandomDelays": settings.get("enableRandomDelays", True),
                "defaultDelayMin": max(1, min(10, settings.get("defaultDelayMin", 2))),
                "defaultDelayMax": max(2, min(15, settings.get("defaultDelayMax", 5))),
                "maxRetries": max(1, min(10, settings.get("maxRetries", 3))),
                "timeoutSeconds": max(10, min(120, settings.get("timeoutSeconds", 30)))
            })
        elif category == "proxy":
            PLATFORM_SETTINGS[category].update({
                "enabled": settings.get("enabled", False),
                "proxyList": settings.get("proxyList", []),
                "rotationInterval": max(30, min(3600, settings.get("rotationInterval", 60))),
                "authentication": {
                    "username": settings.get("authentication", {}).get("username", ""),
                    "password": settings.get("authentication", {}).get("password", "")
                }
            })
        elif category == "rateLimits":
            PLATFORM_SETTINGS[category].update({
                "requestsPerMinute": max(10, min(1000, settings.get("requestsPerMinute", 60))),
                "requestsPerHour": max(100, min(10000, settings.get("requestsPerHour", 1000))),
                "requestsPerDay": max(1000, min(100000, settings.get("requestsPerDay", 10000))),
                "enableRateLimiting": settings.get("enableRateLimiting", True)
            })
        elif category == "security":
            PLATFORM_SETTINGS[category].update({
                "enableThreatDetection": settings.get("enableThreatDetection", True),
                "enableAnomalyDetection": settings.get("enableAnomalyDetection", True),
                "threatScoreThreshold": max(0.1, min(1.0, settings.get("threatScoreThreshold", 0.7))),
                "enableAutoBlocking": settings.get("enableAutoBlocking", False)
            })
        elif category == "notifications":
            PLATFORM_SETTINGS[category].update({
                "emailNotifications": settings.get("emailNotifications", False),
                "webhookNotifications": settings.get("webhookNotifications", False),
                "webhookUrl": settings.get("webhookUrl", ""),
                "notificationLevel": settings.get("notificationLevel", "high")
            })
        
        logger.info(f"Settings updated for category: {category}")
        
        return {
            "message": f"Settings updated successfully for category: {category}",
            "category": category,
            "settings": PLATFORM_SETTINGS[category],
            "updated_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating settings for category {category}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/settings/reset")
async def reset_settings(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Reset settings to default values"""
    try:
        default_settings = {
            "scraping": {
                "enableUserAgentRotation": True,
                "enableProxyRotation": False,
                "enableRandomDelays": True,
                "defaultDelayMin": 2,
                "defaultDelayMax": 5,
                "maxRetries": 3,
                "timeoutSeconds": 30
            },
            "proxy": {
                "enabled": False,
                "proxyList": [],
                "rotationInterval": 60,
                "authentication": {
                    "username": "",
                    "password": ""
                }
            },
            "rateLimits": {
                "requestsPerMinute": 60,
                "requestsPerHour": 1000,
                "requestsPerDay": 10000,
                "enableRateLimiting": True
            },
            "security": {
                "enableThreatDetection": True,
                "enableAnomalyDetection": True,
                "threatScoreThreshold": 0.7,
                "enableAutoBlocking": False
            },
            "notifications": {
                "emailNotifications": False,
                "webhookNotifications": False,
                "webhookUrl": "",
                "notificationLevel": "high"
            }
        }
        
        if category:
            if category not in default_settings:
                raise HTTPException(status_code=404, detail=f"Settings category '{category}' not found")
            PLATFORM_SETTINGS[category] = default_settings[category].copy()
            logger.info(f"Settings reset for category: {category}")
            return {
                "message": f"Settings reset for category: {category}",
                "category": category,
                "settings": PLATFORM_SETTINGS[category]
            }
        else:
            PLATFORM_SETTINGS.update(default_settings)
            logger.info("All settings reset to defaults")
            return {
                "message": "All settings reset to defaults",
                "settings": PLATFORM_SETTINGS
            }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resetting settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/settings/validate")
async def validate_settings(
    db: Session = Depends(get_db)
):
    """Validate current settings configuration"""
    try:
        validation_results = {
            "valid": True,
            "issues": [],
            "warnings": []
        }
        
        # Validate scraping settings
        scraping = PLATFORM_SETTINGS["scraping"]
        if scraping["defaultDelayMin"] >= scraping["defaultDelayMax"]:
            validation_results["valid"] = False
            validation_results["issues"].append("Minimum delay must be less than maximum delay")
        
        if scraping["timeoutSeconds"] < 10:
            validation_results["warnings"].append("Very low timeout may cause connection issues")
        
        # Validate proxy settings
        proxy = PLATFORM_SETTINGS["proxy"]
        if proxy["enabled"] and not proxy["proxyList"]:
            validation_results["warnings"].append("Proxy enabled but no proxy list provided")
        
        # Validate rate limits
        rate_limits = PLATFORM_SETTINGS["rateLimits"]
        if rate_limits["requestsPerMinute"] > rate_limits["requestsPerHour"] / 60:
            validation_results["warnings"].append("Minute rate limit exceeds hourly rate limit")
        
        # Validate security settings
        security = PLATFORM_SETTINGS["security"]
        if security["threatScoreThreshold"] < 0.1 or security["threatScoreThreshold"] > 1.0:
            validation_results["valid"] = False
            validation_results["issues"].append("Threat score threshold must be between 0.1 and 1.0")
        
        # Validate notifications
        notifications = PLATFORM_SETTINGS["notifications"]
        if notifications["webhookNotifications"] and not notifications["webhookUrl"]:
            validation_results["warnings"].append("Webhook notifications enabled but no URL provided")
        
        return validation_results
        
    except Exception as e:
        logger.error(f"Error validating settings: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 