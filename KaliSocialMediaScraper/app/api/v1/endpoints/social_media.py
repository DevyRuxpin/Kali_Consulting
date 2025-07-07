"""
Social media API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from app.core.database import get_db
from app.repositories.social_media_repository import SocialMediaRepository
from app.services.social_media_scraper import SocialMediaScraper
from app.models.schemas import PlatformType

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/scrape", response_model=Dict[str, Any])
async def scrape_social_media(
    request: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Scrape social media data for a target"""
    try:
        async with SocialMediaScraper() as scraper:
            # Get and validate request parameters
            platform_str = request.get("platform")
            target = request.get("target")
            
            if not platform_str or not target:
                raise HTTPException(status_code=400, detail="Platform and target are required")
            
            # Convert platform string to PlatformType enum
            try:
                platform = PlatformType(platform_str.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform_str}")
            
            # Scrape the specified platform
            data = await scraper.scrape_platform(
                platform,
                target,
                include_metadata=request.get("include_metadata", False)
            )
            # Store in database (simplified for now)
            repo = SocialMediaRepository(db)
            return {
                "platform": request.get("platform"),
                "target": request.get("target"),
                "data": data,
                "scraped_at": datetime.utcnow().isoformat()
            }
    except Exception as e:
        logger.error(f"Error scraping social media: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profiles", response_model=List[Dict[str, Any]])
async def list_social_media_profiles(
    platform: Optional[str] = None,
    investigation_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List social media profiles with optional filtering"""
    try:
        repo = SocialMediaRepository(db)
        if platform:
            profiles = repo.get_by_platform(platform)
        elif investigation_id:
            profiles = repo.get_by_investigation(investigation_id)
        else:
            profiles = repo.get_all(skip=skip, limit=limit)
        return [
            {
                "id": profile.id,
                "username": profile.username,
                "display_name": profile.display_name,
                "platform": profile.platform.name,
                "followers_count": profile.followers_count,
                "following_count": profile.following_count,
                "posts_count": profile.posts_count,
                "is_verified": profile.is_verified,
                "threat_score": profile.threat_score,
                "collected_at": profile.collected_at
            }
            for profile in profiles
        ]
    except Exception as e:
        logger.error(f"Error listing social media profiles: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profiles/{profile_id}", response_model=Dict[str, Any])
async def get_social_media_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):
    """Get social media profile by ID"""
    try:
        repo = SocialMediaRepository(db)
        profile = repo.get(profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return {
            "id": profile.id,
            "username": profile.username,
            "display_name": profile.display_name,
            "bio": profile.bio,
            "platform": profile.platform.name,
            "followers_count": profile.followers_count,
            "following_count": profile.following_count,
            "posts_count": profile.posts_count,
            "profile_url": profile.profile_url,
            "is_verified": profile.is_verified,
            "is_private": profile.is_private,
            "threat_score": profile.threat_score,
            "threat_indicators": profile.threat_indicators,
            "sentiment_score": profile.sentiment_score,
            "collected_at": profile.collected_at
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting social media profile {profile_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profiles/{profile_id}/posts", response_model=List[Dict[str, Any]])
async def get_profile_posts(
    profile_id: int,
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get posts for a social media profile"""
    try:
        repo = SocialMediaRepository(db)
        posts = repo.get_posts_by_profile(profile_id)
        return [
            {
                "id": post.id,
                "post_id": post.post_id,
                "content": post.content,
                "post_url": post.post_url,
                "posted_at": post.posted_at,
                "likes_count": post.likes_count,
                "shares_count": post.shares_count,
                "comments_count": post.comments_count,
                "threat_score": post.threat_score,
                "sentiment_score": post.sentiment_score,
                "collected_at": post.collected_at
            }
            for post in posts[:limit]
        ]
    except Exception as e:
        logger.error(f"Error getting profile posts {profile_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/high-threat", response_model=List[Dict[str, Any]])
async def get_high_threat_profiles(
    threshold: float = Query(0.7, ge=0.0, le=1.0),
    db: Session = Depends(get_db)
):
    """Get profiles with high threat scores"""
    try:
        repo = SocialMediaRepository(db)
        profiles = repo.get_high_threat_profiles(threshold)
        return [
            {
                "id": profile.id,
                "username": profile.username,
                "display_name": profile.display_name,
                "platform": profile.platform.name,
                "threat_score": profile.threat_score,
                "threat_indicators": profile.threat_indicators,
                "collected_at": profile.collected_at
            }
            for profile in profiles
        ]
    except Exception as e:
        logger.error(f"Error getting high threat profiles: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/verified", response_model=List[Dict[str, Any]])
async def get_verified_profiles(
    db: Session = Depends(get_db)
):
    """Get verified social media profiles"""
    try:
        repo = SocialMediaRepository(db)
        profiles = repo.get_verified_profiles()
        return [
            {
                "id": profile.id,
                "username": profile.username,
                "display_name": profile.display_name,
                "platform": profile.platform.name,
                "followers_count": profile.followers_count,
                "is_verified": profile.is_verified,
                "collected_at": profile.collected_at
            }
            for profile in profiles
        ]
    except Exception as e:
        logger.error(f"Error getting verified profiles: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/posts/recent", response_model=List[Dict[str, Any]])
async def get_recent_posts(
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get recent social media posts"""
    try:
        repo = SocialMediaRepository(db)
        posts = repo.get_recent_posts(limit)
        return [
            {
                "id": post.id,
                "post_id": post.post_id,
                "content": post.content,
                "platform": post.platform.name,
                "posted_at": post.posted_at,
                "likes_count": post.likes_count,
                "shares_count": post.shares_count,
                "comments_count": post.comments_count,
                "threat_score": post.threat_score,
                "collected_at": post.collected_at
            }
            for post in posts
        ]
    except Exception as e:
        logger.error(f"Error getting recent posts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/posts/high-engagement", response_model=List[Dict[str, Any]])
async def get_high_engagement_posts(
    min_likes: int = Query(100, ge=0),
    db: Session = Depends(get_db)
):
    """Get posts with high engagement"""
    try:
        repo = SocialMediaRepository(db)
        posts = repo.get_high_engagement_posts(min_likes)
        return [
            {
                "id": post.id,
                "post_id": post.post_id,
                "content": post.content,
                "platform": post.platform.name,
                "posted_at": post.posted_at,
                "likes_count": post.likes_count,
                "shares_count": post.shares_count,
                "comments_count": post.comments_count,
                "engagement_rate": post.engagement_rate,
                "collected_at": post.collected_at
            }
            for post in posts
        ]
    except Exception as e:
        logger.error(f"Error getting high engagement posts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/platforms")
async def get_social_media_platforms():
    """Get list of supported social media platforms"""
    try:
        platforms = [
            {"id": "github", "name": "GitHub", "description": "Code repository and developer profiles"},
            {"id": "twitter", "name": "Twitter", "description": "Social media platform"},
            {"id": "instagram", "name": "Instagram", "description": "Photo and video sharing platform"},
            {"id": "linkedin", "name": "LinkedIn", "description": "Professional networking platform"},
            {"id": "reddit", "name": "Reddit", "description": "Community discussion platform"},
            {"id": "youtube", "name": "YouTube", "description": "Video sharing platform"},
            {"id": "facebook", "name": "Facebook", "description": "Social networking platform"},
            {"id": "tiktok", "name": "TikTok", "description": "Short-form video platform"},
            {"id": "telegram", "name": "Telegram", "description": "Messaging platform"},
            {"id": "discord", "name": "Discord", "description": "Gaming and community platform"}
        ]
        return {"platforms": platforms}
    except Exception as e:
        logger.error(f"Error getting social media platforms: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/statistics")
async def get_social_media_statistics(
    db: Session = Depends(get_db)
):
    """Get social media statistics"""
    try:
        repo = SocialMediaRepository(db)
        stats = repo.get_social_media_statistics()
        return {
            "total_profiles": stats.get("total_profiles", 0),
            "total_posts": stats.get("total_posts", 0),
            "verified_profiles": stats.get("verified_profiles", 0),
            "high_threat_profiles": stats.get("high_threat_profiles", 0),
            "platforms": stats.get("platforms", {})
        }
    except Exception as e:
        logger.error(f"Error getting social media statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data")
async def get_social_media_data(
    db: Session = Depends(get_db)
):
    """Get all social media data"""
    try:
        repo = SocialMediaRepository(db)
        profiles = repo.get_all()
        return [
            {
                "id": profile.id,
                "username": profile.username,
                "display_name": profile.display_name,
                "platform": profile.platform.name,
                "followers_count": profile.followers_count,
                "following_count": profile.following_count,
                "posts_count": profile.posts_count,
                "is_verified": profile.is_verified,
                "threat_score": profile.threat_score,
                "collected_at": profile.collected_at
            }
            for profile in profiles
        ]
    except Exception as e:
        logger.error(f"Error getting social media data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_profile(
    request: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Analyze a social media profile"""
    try:
        platform = request.get("platform")
        username = request.get("username")
        
        if not platform or not username:
            raise HTTPException(status_code=400, detail="Platform and username are required")
        
        # Mock analysis for now
        return {
            "platform": platform,
            "username": username,
            "analysis": {
                "threat_score": 0.3,
                "sentiment_score": 0.5,
                "engagement_rate": 0.02,
                "influence_score": 0.4
            },
            "analyzed_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
async def search_content(
    request: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Search social media content using real APIs"""
    try:
        platform = request.get("platform")
        query = request.get("query")
        max_results = request.get("max_results", 50)
        
        if not platform or not query:
            raise HTTPException(status_code=400, detail="Platform and query are required")
        
        # Initialize social media scraper for real search
        scraper = SocialMediaScraper()
        
        results = []
        
        if platform.lower() == "twitter":
            # Real Twitter search using Twitter API
            try:
                search_results = await scraper._search_twitter(query, max_results)
                if "error" not in search_results:
                    results = search_results.get("results", [])
            except Exception as e:
                logger.warning(f"Twitter search failed: {e}")
        
        elif platform.lower() == "reddit":
            # Real Reddit search using Reddit API
            try:
                search_results = await scraper._search_reddit(query, max_results)
                if "error" not in search_results:
                    results = search_results.get("results", [])
            except Exception as e:
                logger.warning(f"Reddit search failed: {e}")
        
        elif platform.lower() == "github":
            # Real GitHub search using GitHub API
            try:
                search_results = await scraper._search_github(query, max_results)
                if "error" not in search_results:
                    results = search_results.get("results", [])
            except Exception as e:
                logger.warning(f"GitHub search failed: {e}")
        
        else:
            # Generic search across multiple platforms
            platforms_to_search = ["twitter", "reddit", "github"]
            for platform_name in platforms_to_search:
                try:
                    if platform_name == "twitter":
                        search_results = await scraper._search_twitter(query, max_results // 3)
                    elif platform_name == "reddit":
                        search_results = await scraper._search_reddit(query, max_results // 3)
                    elif platform_name == "github":
                        search_results = await scraper._search_github(query, max_results // 3)
                    
                    if "error" not in search_results:
                        platform_results = search_results.get("results", [])
                        # Add platform info to results
                        for result in platform_results:
                            result["platform"] = platform_name
                        results.extend(platform_results)
                        
                except Exception as e:
                    logger.warning(f"Search failed for {platform_name}: {e}")
                    continue
        
        return {
            "platform": platform,
            "query": query,
            "results": results,
            "total_found": len(results),
            "searched_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error searching content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/proxy/status")
async def get_proxy_status():
    """Get proxy rotation status and statistics"""
    try:
        from app.services.proxy_rotator import proxy_rotator
        stats = proxy_rotator.get_proxy_stats()
        return {
            "status": "operational",
            "proxy_rotation": True,
            "statistics": stats,
            "last_updated": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting proxy status: {e}")
        return {
            "status": "error",
            "proxy_rotation": False,
            "error": str(e),
            "last_updated": datetime.utcnow().isoformat()
        } 