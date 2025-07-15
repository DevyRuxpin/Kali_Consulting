"""
Social Media API endpoints with Sherlock integration
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.auth import get_current_active_user, get_current_user
from app.services.sherlock_integration import sherlock_integration
from app.services.social_media_scraper import SocialMediaScraper
from app.models.schemas import (
    SocialMediaScrapingRequest,
    PlatformType,
    AnalyzeProfileRequest,
    SearchContentRequest,
    SocialMediaProfile,
    ThreatLevel
)
from app.utils.validation import validate_and_sanitize_input
from app.utils.error_handler import error_handler
from app.repositories.social_media_repository import SocialMediaRepository
from app.services.sherlock_integration import SherlockIntegration
from app.models.database import User

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/sherlock/hunt")
async def hunt_username_sherlock(
    username: str,
    sites: Optional[List[str]] = None,
    # current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Hunt for username across social media platforms using Sherlock"""
    try:
        async with SherlockIntegration() as sherlock:
            results = await sherlock.hunt_username(username, sites)
            
            return {
                "success": True,
                "username": username,
                "results": results,
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Error in Sherlock hunt: {e}")
        raise HTTPException(status_code=500, detail=f"Sherlock hunt failed: {str(e)}")

@router.post("/sherlock/hunt-multiple")
async def hunt_multiple_usernames_sherlock(
    usernames: List[str],
    sites: Optional[List[str]] = None,
    db: Session = Depends(get_db)
):
    """Hunt for multiple usernames using Sherlock"""
    try:
        sanitized_usernames = validate_and_sanitize_input(usernames)
        if isinstance(sanitized_usernames, list):
            sanitized_usernames = [str(u) for u in sanitized_usernames]
        else:
            sanitized_usernames = [str(sanitized_usernames)]
        sanitized_sites = validate_and_sanitize_input(sites) if sites else None
        if sanitized_sites is not None:
            if isinstance(sanitized_sites, list):
                sanitized_sites = [str(s) for s in sanitized_sites]
            else:
                sanitized_sites = [str(sanitized_sites)]
        logger.info(f"Starting Sherlock hunt for {len(sanitized_usernames)} usernames")
        
        result = await sherlock_integration.hunt_multiple_usernames(sanitized_usernames, sanitized_sites)
        
        return {
            "status": "success",
            "total_usernames": len(sanitized_usernames),
            "results": result
        }
        
    except ValueError as ve:
        error_handler.handle_exception(ve, {"endpoint": "hunt_multiple_usernames_sherlock"})
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        error_handler.handle_exception(e, {"endpoint": "hunt_multiple_usernames_sherlock"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/sherlock/sites")
async def get_sherlock_sites(
    # current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get list of supported sites for Sherlock"""
    try:
        sherlock = SherlockIntegration()
        sites = sherlock.get_supported_sites()
        categories = sherlock.get_site_categories()
        
        return {
            "success": True,
            "total_sites": len(sites),
            "sites": sites,
            "categories": categories,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting Sherlock sites: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get sites: {str(e)}")

@router.post("/sherlock/analyze-patterns")
async def analyze_username_patterns(
    usernames: List[str],
    db: Session = Depends(get_db)
):
    """Analyze username patterns across platforms"""
    try:
        sanitized_usernames = validate_and_sanitize_input(usernames)
        if isinstance(sanitized_usernames, list):
            sanitized_usernames = [str(u) for u in sanitized_usernames]
        else:
            sanitized_usernames = [str(sanitized_usernames)]
        logger.info(f"Analyzing patterns for {len(sanitized_usernames)} usernames")
        
        result = await sherlock_integration.analyze_username_patterns(sanitized_usernames)
        
        return {
            "status": "success",
            "analysis": result
        }
        
    except ValueError as ve:
        error_handler.handle_exception(ve, {"endpoint": "analyze_username_patterns"})
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        error_handler.handle_exception(e, {"endpoint": "analyze_username_patterns"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/scrape")
async def scrape_social_media(
    request: SocialMediaScrapingRequest,
    db: Session = Depends(get_db)
):
    """Scrape social media data from specified platform"""
    try:
        scraper = SocialMediaScraper()
        
        async with scraper:
            result = await scraper.scrape_platform(
                platform=request.platform,
                target=request.target,
                include_metadata=request.include_metadata,
                include_media=request.include_media,
                max_posts=request.max_posts
            )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "status": "success",
            "platform": request.platform,
            "target": request.target,
            "data": result
        }
        
    except ValueError as ve:
        error_handler.handle_exception(ve, {"endpoint": "scrape_social_media"})
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        error_handler.handle_exception(e, {"endpoint": "scrape_social_media"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/analyze-profile")
async def analyze_social_media_profile(
    platform: PlatformType,
    username: str,
    date_range: Optional[Dict[str, str]] = None,
    db: Session = Depends(get_db)
):
    """Analyze social media profile comprehensively"""
    try:
        scraper = SocialMediaScraper()
        
        async with scraper:
            result = await scraper.analyze_profile(
                platform=platform,
                username=username,
                date_range=date_range
            )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "status": "success",
            "platform": platform,
            "username": username,
            "analysis": result
        }
        
    except ValueError as ve:
        error_handler.handle_exception(ve, {"endpoint": "analyze_social_media_profile"})
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        error_handler.handle_exception(e, {"endpoint": "analyze_social_media_profile"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/search-content")
async def search_social_media_content(
    platform: PlatformType,
    query: str,
    max_results: int = 50,
    db: Session = Depends(get_db)
):
    """Search for content on social media platform"""
    try:
        scraper = SocialMediaScraper()
        
        async with scraper:
            result = await scraper.search_content(
                platform=platform,
                query=query,
                max_results=max_results
            )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "status": "success",
            "platform": platform,
            "query": query,
            "results": result
        }
        
    except ValueError as ve:
        error_handler.handle_exception(ve, {"endpoint": "search_social_media_content"})
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        error_handler.handle_exception(e, {"endpoint": "search_social_media_content"})
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/analyze")
async def analyze_profile_alias(
    request: AnalyzeProfileRequest,
    db: Session = Depends(get_db)
):
    return await analyze_social_media_profile(request.platform, request.username, request.date_range, db)

@router.post("/search")
async def search_content_alias(
    request: SearchContentRequest,
    db: Session = Depends(get_db)
):
    return await search_social_media_content(request.platform, request.query, request.max_results, db)

@router.post("/comprehensive-hunt")
async def comprehensive_social_media_hunt(
    username: str,
    include_direct_scraping: bool = True,
    include_sherlock: bool = True,
    platforms: Optional[List[str]] = None,
    # current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Comprehensive social media hunt using both direct scrapers and Sherlock"""
    try:
        results = {
            "username": username,
            "timestamp": datetime.utcnow().isoformat(),
            "direct_scraping": {},
            "sherlock_results": {},
            "summary": {},
            "recommendations": []
        }
        
        # Direct platform scraping
        if include_direct_scraping:
            logger.info(f"Starting direct scraping for {username}")
            async with SocialMediaScraper() as scraper:
                platforms_to_scrape = platforms or ["github", "twitter", "reddit", "instagram"]
                
                for platform in platforms_to_scrape:
                    try:
                        platform_enum = getattr(PlatformType, platform.upper(), None)
                        if platform_enum:
                            platform_result = await scraper.scrape_platform(
                                platform_enum, username, include_metadata=True, max_posts=50
                            )
                            results["direct_scraping"][platform] = platform_result
                        else:
                            logger.warning(f"Unsupported platform for direct scraping: {platform}")
                    except Exception as e:
                        logger.error(f"Error scraping {platform}: {e}")
                        results["direct_scraping"][platform] = {"error": str(e)}
        
        # Sherlock username hunting
        if include_sherlock:
            logger.info(f"Starting Sherlock hunt for {username}")
            async with SherlockIntegration() as sherlock:
                sherlock_results = await sherlock.hunt_username(username, sites=platforms)
                results["sherlock_results"] = sherlock_results
        
        # Generate summary and recommendations
        results["summary"] = _generate_comprehensive_summary(results)
        results["recommendations"] = _generate_comprehensive_recommendations(results)
        
        return {
            "success": True,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error in comprehensive hunt: {e}")
        raise HTTPException(status_code=500, detail=f"Comprehensive hunt failed: {str(e)}")

def _generate_comprehensive_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive summary of all findings"""
    summary = {
        "total_platforms_checked": 0,
        "accounts_found": 0,
        "platforms_with_activity": [],
        "threat_indicators": [],
        "activity_level": "low"
    }
    
    # Count direct scraping results
    direct_results = results.get("direct_scraping", {})
    for platform, data in direct_results.items():
        if "error" not in data:
            summary["total_platforms_checked"] += 1
            if data.get("profile") or data.get("posts"):
                summary["platforms_with_activity"].append(platform)
                summary["accounts_found"] += 1
    
    # Count Sherlock results
    sherlock_results = results.get("sherlock_results", {})
    if sherlock_results.get("found_accounts"):
        summary["accounts_found"] += len(sherlock_results["found_accounts"])
        summary["total_platforms_checked"] += sherlock_results.get("total_sites_checked", 0)
    
    # Determine activity level
    if summary["accounts_found"] > 10:
        summary["activity_level"] = "high"
    elif summary["accounts_found"] > 5:
        summary["activity_level"] = "medium"
    
    return summary

def _generate_comprehensive_recommendations(results: Dict[str, Any]) -> List[str]:
    """Generate actionable recommendations based on findings"""
    recommendations = []
    
    summary = results.get("summary", {})
    sherlock_results = results.get("sherlock_results", {})
    
    if summary.get("accounts_found", 0) > 0:
        recommendations.append("Multiple social media accounts found - consider cross-platform analysis")
        recommendations.append("Monitor high-activity platforms for updates and new content")
    
    if sherlock_results.get("found_accounts"):
        recommendations.append("Use Sherlock results to expand investigation to additional platforms")
    
    if summary.get("activity_level") == "high":
        recommendations.append("High social media activity detected - prioritize monitoring")
    
    recommendations.append("Cross-reference findings with domain analysis and threat intelligence")
    recommendations.append("Verify account ownership through additional OSINT research")
    
    return recommendations

@router.get("/platforms")
async def get_supported_platforms():
    """Get list of supported social media platforms"""
    platforms = [
        {"name": "twitter", "display_name": "Twitter/X", "enabled": True},
        {"name": "instagram", "display_name": "Instagram", "enabled": True},
        {"name": "reddit", "display_name": "Reddit", "enabled": True},
        {"name": "github", "display_name": "GitHub", "enabled": True},
        {"name": "linkedin", "display_name": "LinkedIn", "enabled": False},
        {"name": "facebook", "display_name": "Facebook", "enabled": False},
        {"name": "youtube", "display_name": "YouTube", "enabled": True},
        {"name": "tiktok", "display_name": "TikTok", "enabled": False},
        {"name": "telegram", "display_name": "Telegram", "enabled": False},
        {"name": "discord", "display_name": "Discord", "enabled": False}
    ]
    
    return {
        "platforms": platforms,
        "total": len(platforms),
        "enabled": len([p for p in platforms if p["enabled"]])
    }

@router.get("/status")
async def get_social_media_status():
    """Get social media scraping status and statistics"""
    try:
        # Get Sherlock status
        sherlock_sites = sherlock_integration.get_supported_sites()
        
        return {
            "sherlock": {
                "available": bool(sherlock_integration.sherlock_path),
                "supported_sites": len(sherlock_sites),
                "path": sherlock_integration.sherlock_path
            },
            "scraping": {
                "enabled": True,
                "rate_limiting": True,
                "proxy_rotation": True
            },
            "statistics": {
                "total_platforms": 10,
                "active_platforms": 5
            }
        }
        
    except ValueError as ve:
        error_handler.handle_exception(ve, {"endpoint": "get_social_media_status"})
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        error_handler.handle_exception(e, {"endpoint": "get_social_media_status"})
        raise HTTPException(status_code=500, detail="Internal server error") 

@router.get("/profiles")
async def get_social_media_profiles(db: Session = Depends(get_db)):
    """Get all scraped social media profiles from the database"""
    repo = SocialMediaRepository(db)
    profiles = repo.get_recent_profiles(limit=100)
    # Transform DB objects to API schema
    return [
        {
            "id": profile.id,
            "platform": profile.platform.name if hasattr(profile.platform, 'name') else profile.platform,
            "username": profile.username,
            "display_name": profile.display_name,
            "bio": profile.bio,
            "followers": profile.followers_count,
            "following": profile.following_count,
            "posts": profile.posts_count,
            "verified": profile.is_verified,
            "lastActive": profile.collected_at.isoformat() if profile.collected_at is not None else None,
            "profileUrl": profile.profile_url,
            "avatarUrl": getattr(profile, 'avatar_url', None),
            "threatLevel": profile.threat_score,
            "sentiment": profile.sentiment_score,
            "tags": profile.threat_indicators or [],
        }
        for profile in profiles
    ]

@router.get("/posts")
async def get_social_media_posts(db: Session = Depends(get_db)):
    """Get all scraped social media posts from the database"""
    repo = SocialMediaRepository(db)
    posts = repo.get_recent_posts(limit=100)
    return [
        {
            "id": post.id,
            "platform": post.platform.name if hasattr(post.platform, 'name') else post.platform,
            "author": post.author,
            "content": post.content,
            "timestamp": post.collected_at.isoformat() if post.collected_at is not None else None,
            "likes": post.likes_count,
            "comments": post.comments_count,
            "shares": post.shares_count,
            "url": post.url,
            "sentiment": post.sentiment_score,
            "threatLevel": post.threat_score,
            "tags": post.threat_indicators or [],
        }
        for post in posts
    ] 