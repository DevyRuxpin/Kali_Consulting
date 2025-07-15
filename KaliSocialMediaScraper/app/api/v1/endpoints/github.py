"""
GitHub API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import logging

from app.services.github_scraper import GitHubScraper
from app.models.schemas import GitHubUserRequest, GitHubRepoRequest, GitHubSearchRequest

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analyze")
async def analyze_github_target(request: Dict[str, Any]):
    """Analyze GitHub target (user, organization, or repository)"""
    try:
        target = request.get("target")
        target_type = request.get("target_type", "user")
        
        if not target:
            raise HTTPException(status_code=400, detail="Target is required")
        
        async with GitHubScraper() as scraper:
            if target_type == "user":
                result = await scraper.analyze_user_profile(target)
            elif target_type == "organization":
                result = await scraper.analyze_organization(target)
            elif target_type == "repository":
                result = await scraper.analyze_repository_async(target)
            else:
                raise HTTPException(status_code=400, detail="Invalid target_type")
            
            return result
    except Exception as e:
        logger.error(f"Error analyzing GitHub target: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/scrape-user", response_model=Dict[str, Any])
async def scrape_github_user(request: GitHubUserRequest):
    """Scrape GitHub user profile"""
    try:
        async with GitHubScraper() as scraper:
            result = await scraper.analyze_user_profile(request.username)
            return result
    except Exception as e:
        logger.error(f"Error scraping GitHub user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/scrape-repo", response_model=Dict[str, Any])
async def scrape_github_repo(request: GitHubRepoRequest):
    """Scrape GitHub repository"""
    try:
        async with GitHubScraper() as scraper:
            result = await scraper.analyze_repository_async(request.repo_url)
            return result
    except Exception as e:
        logger.error(f"Error scraping GitHub repo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search", response_model=Dict[str, Any])
async def search_github_repos(request: GitHubSearchRequest):
    """Search GitHub repositories"""
    try:
        async with GitHubScraper() as scraper:
            result = await scraper.search_repositories(request.query, max_results=request.max_results)
            return result
    except Exception as e:
        logger.error(f"Error searching GitHub repos: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 