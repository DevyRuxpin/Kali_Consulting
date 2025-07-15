"""
Scraping Background Tasks
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from celery import current_task

from app.core.celery_app import celery_app
from app.services.github_scraper import GitHubScraper
from app.services.social_media_scraper import SocialMediaScraper
from app.services.domain_analyzer import DomainAnalyzer
from app.repositories.investigation_repository import InvestigationRepository
from app.models.schemas import PlatformType

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def scrape_github_repository_task(self, repository_url: str, investigation_id: Optional[str] = None) -> Dict[str, Any]:
    """Scrape GitHub repository data"""
    try:
        logger.info(f"Starting GitHub repository scraping: {repository_url}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Initializing scraper", "progress": 10}
        )
        
        # Initialize GitHub scraper
        github_scraper = GitHubScraper()
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Scraping repository", "progress": 30}
        )
        
        # Scrape repository (full analysis)
        repo_data = asyncio.run(github_scraper.analyze_repository_async(repository_url))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Analyzing repository", "progress": 70}
        )
        
        # Analyze repository for threats (already included in repo_data)
        threat_assessment = repo_data.get("threat_assessment")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Saving data", "progress": 90}
        )
        
        # Save data if investigation_id provided
        if investigation_id:
            investigation_repo = InvestigationRepository()
            asyncio.run(investigation_repo.add_github_data(investigation_id, repo_data))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Repository scraping completed", "progress": 100}
        )
        
        return {
            "status": "completed",
            "repository_url": repository_url,
            "repository_data": repo_data,
            "threat_assessment": threat_assessment,
            "investigation_id": investigation_id
        }
        
    except Exception as e:
        logger.error(f"Error scraping GitHub repository {repository_url}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def scrape_github_user_task(self, username: str, investigation_id: Optional[str] = None) -> Dict[str, Any]:
    """Scrape GitHub user data"""
    try:
        logger.info(f"Starting GitHub user scraping: {username}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Initializing scraper", "progress": 10}
        )
        
        # Initialize GitHub scraper
        github_scraper = GitHubScraper()
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Scraping user profile", "progress": 30}
        )
        
        # Scrape user profile (full analysis)
        user_data = asyncio.run(github_scraper.analyze_user_profile(username))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Scraping user repositories", "progress": 50}
        )
        
        # Scrape user repositories (already included in user_data)
        repositories = user_data.get("repositories")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Analyzing user activity", "progress": 70}
        )
        
        # Analyze user activity (already included in user_data)
        activity_analysis = user_data.get("activity")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Assessing threats", "progress": 90}
        )
        
        # Assess threats (already included in user_data)
        threat_assessment = user_data.get("threat_assessment")
        
        # Combine all data
        combined_data = {
            "user_profile": user_data.get("user"),
            "repositories": repositories,
            "activity_analysis": activity_analysis,
            "threat_assessment": threat_assessment
        }
        
        # Save data if investigation_id provided
        if investigation_id:
            investigation_repo = InvestigationRepository()
            asyncio.run(investigation_repo.add_github_data(investigation_id, combined_data))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "User scraping completed", "progress": 100}
        )
        
        return {
            "status": "completed",
            "username": username,
            "user_data": combined_data,
            "investigation_id": investigation_id
        }
        
    except Exception as e:
        logger.error(f"Error scraping GitHub user {username}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def scrape_github_organization_task(self, org_name: str, investigation_id: Optional[str] = None) -> Dict[str, Any]:
    """Scrape GitHub organization data"""
    try:
        logger.info(f"Starting GitHub organization scraping: {org_name}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Initializing scraper", "progress": 10}
        )
        
        # Initialize GitHub scraper
        github_scraper = GitHubScraper()
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Scraping organization profile", "progress": 30}
        )
        
        # Scrape organization profile (full analysis)
        org_data = asyncio.run(github_scraper.analyze_organization(org_name))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Scraping organization repositories", "progress": 50}
        )
        
        # Scrape organization repositories (already included in org_data)
        repositories = org_data.get("repositories")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Scraping organization members", "progress": 70}
        )
        
        # Scrape organization members (already included in org_data)
        members = org_data.get("members")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Assessing threats", "progress": 90}
        )
        
        # Assess threats (already included in org_data)
        threat_assessment = org_data.get("threat_assessment")
        
        # Combine all data
        combined_data = {
            "organization_profile": org_data.get("organization"),
            "repositories": repositories,
            "members": members,
            "threat_assessment": threat_assessment
        }
        
        # Save data if investigation_id provided
        if investigation_id:
            investigation_repo = InvestigationRepository()
            asyncio.run(investigation_repo.add_github_data(investigation_id, combined_data))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Organization scraping completed", "progress": 100}
        )
        
        return {
            "status": "completed",
            "organization_name": org_name,
            "organization_data": combined_data,
            "investigation_id": investigation_id
        }
        
    except Exception as e:
        logger.error(f"Error scraping GitHub organization {org_name}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def scrape_social_media_profile_task(self, platform: str, username: str, investigation_id: Optional[str] = None) -> Dict[str, Any]:
    """Scrape social media profile data"""
    try:
        logger.info(f"Starting social media scraping: {platform} - {username}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Initializing scraper", "progress": 10}
        )
        
        # Initialize social media scraper
        social_scraper = SocialMediaScraper()
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Scraping profile", "progress": 30}
        )
        
        # Scrape profile (full analysis)
        platform_enum = PlatformType(platform)
        profile_data = asyncio.run(social_scraper.analyze_profile(platform_enum, username))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Scraping posts", "progress": 50}
        )
        
        # Scrape recent posts (already included in profile_data)
        posts_data = profile_data.get("posts")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Analyzing content", "progress": 70}
        )
        
        # Analyze content sentiment (already included in profile_data)
        sentiment_analysis = profile_data.get("sentiment_analysis")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Assessing threats", "progress": 90}
        )
        
        # Assess threats (already included in profile_data)
        threat_assessment = profile_data.get("threat_assessment")
        
        # Combine all data
        combined_data = {
            "platform": platform,
            "username": username,
            "profile_data": profile_data.get("profile"),
            "posts_data": posts_data,
            "sentiment_analysis": sentiment_analysis,
            "threat_assessment": threat_assessment
        }
        
        # Save data if investigation_id provided
        if investigation_id:
            investigation_repo = InvestigationRepository()
            asyncio.run(investigation_repo.add_social_media_data(investigation_id, combined_data))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Social media scraping completed", "progress": 100}
        )
        
        return {
            "status": "completed",
            "platform": platform,
            "username": username,
            "profile_data": combined_data,
            "investigation_id": investigation_id
        }
        
    except Exception as e:
        logger.error(f"Error scraping social media profile {platform}/{username}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def analyze_domain_task(self, domain: str, investigation_id: Optional[str] = None) -> Dict[str, Any]:
    """Analyze domain data"""
    try:
        logger.info(f"Starting domain analysis: {domain}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Initializing analyzer", "progress": 10}
        )
        
        # Initialize domain analyzer
        domain_analyzer = DomainAnalyzer()
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Analyzing domain", "progress": 30}
        )
        
        # Analyze domain (full analysis)
        domain_data = asyncio.run(domain_analyzer.analyze_domain(domain))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Enumerating subdomains", "progress": 50}
        )
        
        # Enumerate subdomains (already included in domain_data)
        subdomains = domain_data.get("subdomains")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Detecting technologies", "progress": 70}
        )
        
        # Detect technologies (already included in domain_data)
        technologies = domain_data.get("technologies")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Assessing threats", "progress": 90}
        )
        
        # Assess threats (already included in domain_data)
        threat_assessment = domain_data.get("threat_assessment")
        
        # Combine all data
        combined_data = {
            "domain": domain,
            "domain_data": domain_data,
            "subdomains": subdomains,
            "technologies": technologies,
            "threat_assessment": threat_assessment
        }
        
        # Save data if investigation_id provided
        if investigation_id:
            investigation_repo = InvestigationRepository()
            asyncio.run(investigation_repo.add_domain_data(investigation_id, combined_data))
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Domain analysis completed", "progress": 100}
        )
        
        return {
            "status": "completed",
            "domain": domain,
            "domain_data": combined_data,
            "investigation_id": investigation_id
        }
        
    except Exception as e:
        logger.error(f"Error analyzing domain {domain}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def bulk_scrape_task(self, targets: List[Dict[str, Any]], investigation_id: Optional[str] = None) -> Dict[str, Any]:
    """Bulk scrape multiple targets"""
    try:
        logger.info(f"Starting bulk scraping for {len(targets)} targets")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Initializing bulk scraping", "progress": 5}
        )
        
        results = []
        total_targets = len(targets)
        
        for i, target in enumerate(targets):
            target_type = target.get("type")
            target_value = target.get("value")
            
            # Update progress
            progress = 5 + (i / total_targets) * 90
            self.update_state(
                state="PROGRESS",
                meta={
                    "status": f"Scraping {target_type}: {target_value}",
                    "progress": int(progress)
                }
            )
            
            try:
                if target_type == "github_repository":
                    result = scrape_github_repository_task.apply_async(
                        args=[target_value, investigation_id],
                        countdown=i * 2  # Stagger requests
                    )
                    results.append({
                        "target": target,
                        "task_id": result.id,
                        "status": "queued"
                    })
                
                elif target_type == "github_user":
                    result = scrape_github_user_task.apply_async(
                        args=[target_value, investigation_id],
                        countdown=i * 2
                    )
                    results.append({
                        "target": target,
                        "task_id": result.id,
                        "status": "queued"
                    })
                
                elif target_type == "github_organization":
                    result = scrape_github_organization_task.apply_async(
                        args=[target_value, investigation_id],
                        countdown=i * 2
                    )
                    results.append({
                        "target": target,
                        "task_id": result.id,
                        "status": "queued"
                    })
                
                elif target_type == "social_media":
                    platform = target.get("platform")
                    username = target.get("username")
                    result = scrape_social_media_profile_task.apply_async(
                        args=[platform, username, investigation_id],
                        countdown=i * 2
                    )
                    results.append({
                        "target": target,
                        "task_id": result.id,
                        "status": "queued"
                    })
                
                elif target_type == "domain":
                    result = analyze_domain_task.apply_async(
                        args=[target_value, investigation_id],
                        countdown=i * 2
                    )
                    results.append({
                        "target": target,
                        "task_id": result.id,
                        "status": "queued"
                    })
                
                else:
                    results.append({
                        "target": target,
                        "error": f"Unknown target type: {target_type}",
                        "status": "failed"
                    })
                    
            except Exception as e:
                logger.error(f"Error queuing task for target {target}: {e}")
                results.append({
                    "target": target,
                    "error": str(e),
                    "status": "failed"
                })
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Bulk scraping completed", "progress": 100}
        )
        
        return {
            "status": "completed",
            "total_targets": total_targets,
            "queued_tasks": len([r for r in results if r["status"] == "queued"]),
            "failed_tasks": len([r for r in results if r["status"] == "failed"]),
            "results": results,
            "investigation_id": investigation_id
        }
        
    except Exception as e:
        logger.error(f"Error in bulk scraping: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def monitor_scraping_progress_task(self, task_ids: List[str]) -> Dict[str, Any]:
    """Monitor progress of scraping tasks"""
    try:
        logger.info(f"Starting monitoring for {len(task_ids)} tasks")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Checking task status", "progress": 50}
        )
        
        # Check status of all tasks
        task_statuses = []
        for task_id in task_ids:
            try:
                from app.core.celery_app import get_task_status
                status = get_task_status(task_id)
                task_statuses.append({
                    "task_id": task_id,
                    "status": status
                })
            except Exception as e:
                logger.error(f"Error checking task {task_id}: {e}")
                task_statuses.append({
                    "task_id": task_id,
                    "status": {"status": "error", "error": str(e)}
                })
        
        # Calculate overall progress
        completed_tasks = len([s for s in task_statuses if s["status"].get("status") == "SUCCESS"])
        failed_tasks = len([s for s in task_statuses if s["status"].get("status") == "FAILURE"])
        total_tasks = len(task_ids)
        
        overall_progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Monitoring completed", "progress": 100}
        )
        
        return {
            "status": "completed",
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "in_progress_tasks": total_tasks - completed_tasks - failed_tasks,
            "overall_progress": overall_progress,
            "task_statuses": task_statuses
        }
        
    except Exception as e:
        logger.error(f"Error monitoring scraping progress: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise 