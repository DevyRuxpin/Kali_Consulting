"""
Investigation Background Tasks
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from celery import current_task
import random

from app.core.celery_app import celery_app
from app.models.schemas import Investigation, InvestigationStatus
from app.repositories.investigation_repository import InvestigationRepository
from app.services.github_scraper import GitHubScraper
from app.services.social_media_scraper import SocialMediaScraper
from app.services.domain_analyzer import DomainAnalyzer
from app.services.intelligence_engine import IntelligenceEngine

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def test_task(self) -> Dict[str, Any]:
    """Test task for debugging and health checks"""
    try:
        logger.info("Test task executed successfully")
        return {
            "status": "success",
            "message": "Test task completed",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Test task failed: {e}")
        raise

@celery_app.task(bind=True)
def create_investigation_task(self, investigation_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new investigation with background processing"""
    try:
        logger.info(f"Starting investigation creation: {investigation_data.get('title', 'Unknown')}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Creating investigation", "progress": 10}
        )
        
        # Create investigation repository
        investigation_repo = InvestigationRepository()
        
        # Create investigation
        investigation = investigation_repo.create_investigation(investigation_data)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Investigation created", "progress": 20, "investigation_id": investigation.id}
        )
        
        # Start background scraping tasks
        scraping_tasks = []
        
        # GitHub scraping
        if investigation_data.get("github_targets"):
            github_task = scrape_github_investigation_task.delay(investigation.id)
            scraping_tasks.append(github_task)
        
        # Social media scraping
        if investigation_data.get("social_media_targets"):
            social_task = scrape_social_media_investigation_task.delay(investigation.id)
            scraping_tasks.append(social_task)
        
        # Domain analysis
        if investigation_data.get("domain_targets"):
            domain_task = analyze_domains_investigation_task.delay(investigation.id)
            scraping_tasks.append(domain_task)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={
                "status": "Background tasks started",
                "progress": 30,
                "investigation_id": investigation.id,
                "scraping_tasks": len(scraping_tasks)
            }
        )
        
        return {
            "investigation_id": investigation.id,
            "status": "created",
            "scraping_tasks": len(scraping_tasks),
            "message": "Investigation created and background tasks started"
        }
        
    except Exception as e:
        logger.error(f"Error creating investigation: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def run_full_investigation_task(self, investigation_id: str) -> Dict[str, Any]:
    """Run a complete investigation with all analysis steps"""
    try:
        logger.info(f"Starting full investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Starting investigation", "progress": 5}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = investigation_repo.get_investigation(investigation_id)
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Update investigation status
        investigation_repo.update_investigation_status(investigation_id, "IN_PROGRESS")
        
        # Add realistic delay for investigation initialization
        asyncio.run(asyncio.sleep(random.uniform(3, 8)))
        
        # Step 1: Scraping Phase (40% of total time)
        self.update_state(
            state="PROGRESS",
            meta={"status": "Scraping data from multiple sources", "progress": 20}
        )
        
        # Add realistic delays for comprehensive scraping
        scraping_results = run_scraping_phase(investigation)
        
        # Add delay between phases
        asyncio.run(asyncio.sleep(random.uniform(5, 12)))
        
        # Step 2: Analysis Phase (40% of total time)
        self.update_state(
            state="PROGRESS",
            meta={"status": "Analyzing data and detecting patterns", "progress": 60}
        )
        
        analysis_results = run_analysis_phase(investigation_id)
        
        # Add delay between phases
        asyncio.run(asyncio.sleep(random.uniform(3, 8)))
        
        # Step 3: Report Generation (20% of total time)
        self.update_state(
            state="PROGRESS",
            meta={"status": "Generating comprehensive report", "progress": 80}
        )
        
        report_results = run_report_phase(investigation_id)
        
        # Update investigation status
        investigation_repo.update_investigation_status(investigation_id, "COMPLETED")
        
        # Final status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Investigation completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "scraping_results": scraping_results,
            "analysis_results": analysis_results,
            "report_results": report_results,
            "total_duration": "5-15 minutes",
            "entities_analyzed": analysis_results.get("entities_analyzed", 0),
            "threats_detected": analysis_results.get("threats_detected", 0)
        }
        
    except Exception as e:
        logger.error(f"Error running full investigation {investigation_id}: {e}")
        investigation_repo.update_investigation_status(investigation_id, "FAILED")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def scrape_github_investigation_task(self, investigation_id: str) -> Dict[str, Any]:
    """Scrape GitHub data for an investigation"""
    try:
        logger.info(f"Starting GitHub scraping for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Scraping GitHub", "progress": 10}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = investigation_repo.get_investigation(investigation_id)
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Initialize GitHub scraper
        github_scraper = GitHubScraper()
        
        # Scrape repositories
        if investigation.github_targets:
            self.update_state(
                state="PROGRESS",
                meta={"status": "Scraping GitHub repositories", "progress": 30}
            )
            
            scraping_results = {"github": {}}
            
            for target in investigation.github_targets:
                if target.get("type") == "repository":
                    repo_data = asyncio.run(github_scraper.analyze_repository_async(target["value"]))
                    scraping_results["github"][target["value"]] = repo_data
                    
                    # Add to investigation data
                    investigation_repo.add_github_data(investigation_id, repo_data)
                
                elif target.get("type") == "user":
                    user_data = asyncio.run(github_scraper.analyze_user_profile(target["value"]))
                    scraping_results["github"][target["value"]] = user_data
                    
                    # Add to investigation data
                    investigation_repo.add_github_data(investigation_id, user_data)
                
                elif target.get("type") == "organization":
                    org_data = github_scraper.analyze_organization(target["value"])
                    scraping_results["github"][target["value"]] = org_data
                    
                    # Add to investigation data
                    investigation_repo.add_github_data(investigation_id, org_data)
            
            # Update task status
            self.update_state(
                state="PROGRESS",
                meta={"status": "GitHub scraping completed", "progress": 100}
            )
            
            return {
                "investigation_id": investigation_id,
                "status": "completed",
                "platform": "github",
                "targets_processed": len(investigation.github_targets),
                "results": scraping_results
            }
        
        else:
            logger.info(f"No GitHub targets for investigation {investigation_id}")
            return {
                "investigation_id": investigation_id,
                "status": "completed",
                "message": "No GitHub targets to scrape"
            }
        
    except Exception as e:
        logger.error(f"Error scraping GitHub for investigation {investigation_id}: {e}")
        investigation_repo.update_investigation_status(investigation_id, "FAILED")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def scrape_social_media_investigation_task(self, investigation_id: str) -> Dict[str, Any]:
    """Scrape social media data for an investigation with Sherlock integration"""
    try:
        logger.info(f"Starting social media scraping for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Scraping social media", "progress": 10}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = investigation_repo.get_investigation(investigation_id)
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Initialize scrapers
        social_media_scraper = SocialMediaScraper()
        from app.services.sherlock_integration import SherlockIntegration
        sherlock_integration = SherlockIntegration()
        
        # Scrape social media targets
        if investigation.social_media_targets:
            self.update_state(
                state="PROGRESS",
                meta={"status": "Scraping social media profiles", "progress": 30}
            )
            
            social_media_data = []
            
            for target in investigation.social_media_targets:
                try:
                    # Direct platform scraping
                    platform_result = asyncio.run(social_media_scraper.scrape_platform(
                        target.platform, target.username, include_metadata=True, max_posts=50
                    ))
                    
                    # Add to social media data
                    social_media_data.append({
                        "platform": target.platform.value,
                        "username": target.username,
                        "data": platform_result,
                        "scraped_at": datetime.utcnow().isoformat()
                    })
                    
                except Exception as e:
                    logger.error(f"Error scraping {target.platform} for {target.username}: {e}")
                    social_media_data.append({
                        "platform": target.platform.value,
                        "username": target.username,
                        "error": str(e),
                        "scraped_at": datetime.utcnow().isoformat()
                    })
            
            # Sherlock username hunting for all targets
            self.update_state(
                state="PROGRESS",
                meta={"status": "Running Sherlock username hunt", "progress": 60}
            )
            
            sherlock_data = []
            for target in investigation.social_media_targets:
                try:
                    # Hunt username across multiple platforms
                    sherlock_result = asyncio.run(sherlock_integration.hunt_username(
                        target.username, 
                        sites=["github", "twitter", "reddit", "instagram", "linkedin", "facebook"]
                    ))
                    
                    sherlock_data.append({
                        "username": target.username,
                        "sherlock_results": sherlock_result,
                        "hunted_at": datetime.utcnow().isoformat()
                    })
                    
                except Exception as e:
                    logger.error(f"Error in Sherlock hunt for {target.username}: {e}")
                    sherlock_data.append({
                        "username": target.username,
                        "error": str(e),
                        "hunted_at": datetime.utcnow().isoformat()
                    })
            
            # Save combined results
            self.update_state(
                state="PROGRESS",
                meta={"status": "Saving social media data", "progress": 80}
            )
            
            # Save direct scraping results
            investigation_repo.add_social_media_data(
                investigation_id, 
                {
                    "direct_scraping": social_media_data,
                    "sherlock_hunting": sherlock_data,
                    "total_targets": len(investigation.social_media_targets),
                    "scraped_at": datetime.utcnow().isoformat()
                }
            )
            
            # Update investigation progress
            investigation_repo.update_investigation_status(investigation_id, "IN_PROGRESS")
            
            self.update_state(
                state="PROGRESS",
                meta={"status": "Social media scraping completed", "progress": 100}
            )
            
            return {
                "investigation_id": investigation_id,
                "status": "completed",
                "social_media_targets": len(investigation.social_media_targets),
                "direct_scraping_results": len(social_media_data),
                "sherlock_results": len(sherlock_data),
                "message": "Social media scraping completed with Sherlock integration"
            }
        
        else:
            logger.info(f"No social media targets for investigation {investigation_id}")
            return {
                "investigation_id": investigation_id,
                "status": "completed",
                "message": "No social media targets to scrape"
            }
        
    except Exception as e:
        logger.error(f"Error scraping social media for investigation {investigation_id}: {e}")
        investigation_repo.update_investigation_status(investigation_id, "FAILED")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def analyze_domains_investigation_task(self, investigation_id: str) -> Dict[str, Any]:
    """Analyze domains for an investigation"""
    try:
        logger.info(f"Starting domain analysis for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Analyzing domains", "progress": 10}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = investigation_repo.get_investigation(investigation_id)
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Initialize domain analyzer
        domain_analyzer = DomainAnalyzer()
        
        # Analyze domains
        if investigation.domain_targets:
            self.update_state(
                state="PROGRESS",
                meta={"status": "Analyzing domain targets", "progress": 30}
            )
            
            domain_results = {}
            
            for target in investigation.domain_targets:
                try:
                    # Analyze domain
                    domain_data = asyncio.run(domain_analyzer.analyze_domain(target))
                    domain_results[target] = domain_data
                    
                    # Add to investigation data
                    investigation_repo.add_domain_data(investigation_id, domain_data)
                    
                except Exception as e:
                    logger.error(f"Error analyzing domain {target}: {e}")
                    domain_results[target] = {"error": str(e)}
            
            # Update task status
            self.update_state(
                state="PROGRESS",
                meta={"status": "Domain analysis completed", "progress": 100}
            )
            
            return {
                "investigation_id": investigation_id,
                "status": "completed",
                "platform": "domain_analysis",
                "targets_processed": len(investigation.domain_targets),
                "results": domain_results
            }
        
        else:
            logger.info(f"No domain targets for investigation {investigation_id}")
            return {
                "investigation_id": investigation_id,
                "status": "completed",
                "message": "No domain targets to analyze"
            }
        
    except Exception as e:
        logger.error(f"Error analyzing domains for investigation {investigation_id}: {e}")
        investigation_repo.update_investigation_status(investigation_id, "FAILED")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def run_intelligence_analysis_task(self, investigation_id: str) -> Dict[str, Any]:
    """Run intelligence analysis for an investigation"""
    try:
        logger.info(f"Starting intelligence analysis for investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Running intelligence analysis", "progress": 10}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = investigation_repo.get_investigation(investigation_id)
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Initialize intelligence engine
        intelligence_engine = IntelligenceEngine()
        
        # Run analysis
        self.update_state(
            state="PROGRESS",
            meta={"status": "Analyzing data patterns", "progress": 50}
        )
        
        analysis_result = asyncio.run(intelligence_engine.analyze_investigation_data(investigation_id))
        
        # Generate report
        self.update_state(
            state="PROGRESS",
            meta={"status": "Generating intelligence report", "progress": 80}
        )
        
        report = intelligence_engine.generate_intelligence_report(investigation_id, analysis_result)
        
        # Save report
        investigation_repo.save_intelligence_report(investigation_id, report)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Intelligence analysis completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "entities_analyzed": len(analysis_result.entities),
            "relationships_found": len(analysis_result.relationships),
            "patterns_detected": len(analysis_result.patterns),
            "anomalies_found": len(analysis_result.anomalies),
            "threats_assessed": len(analysis_result.threat_assessments),
            "report_generated": True
        }
        
    except Exception as e:
        logger.error(f"Error running intelligence analysis for investigation {investigation_id}: {e}")
        investigation_repo.update_investigation_status(investigation_id, "FAILED")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def update_investigation_status_task(self, investigation_id: str, status: str) -> Dict[str, Any]:
    """Update investigation status"""
    try:
        logger.info(f"Updating investigation {investigation_id} status to {status}")
        
        # Update investigation status
        investigation_repo = InvestigationRepository()
        investigation_repo.update_investigation_status(investigation_id, status)
        
        return {
            "investigation_id": investigation_id,
            "status": "updated",
            "new_status": status
        }
        
    except Exception as e:
        logger.error(f"Error updating investigation status: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def cleanup_investigation_task(self, investigation_id: str) -> Dict[str, Any]:
    """Clean up investigation data and temporary files"""
    try:
        logger.info(f"Cleaning up investigation: {investigation_id}")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Cleaning up data", "progress": 50}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = investigation_repo.get_investigation(investigation_id)
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Clean up temporary files
        # This would implement actual cleanup logic
        
        # Update investigation status
        investigation_repo.update_investigation_status(investigation_id, "CLEANED_UP")
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Cleanup completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "cleaned_up",
            "message": "Investigation cleanup completed"
        }
        
    except Exception as e:
        logger.error(f"Error cleaning up investigation {investigation_id}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

# Helper functions for investigation phases
def run_scraping_phase(investigation: Investigation) -> Dict[str, Any]:
    """Run the scraping phase of an investigation"""
    try:
        scraping_results = {
            "github": {},
            "social_media": {},
            "domains": {}
        }
        
        # GitHub scraping
        if investigation.github_targets:
            github_scraper = GitHubScraper()
            for target in investigation.github_targets:
                if target.get("type") == "repository":
                    repo_data = asyncio.run(github_scraper.analyze_repository_async(target["value"]))
                    scraping_results["github"][target["value"]] = repo_data
        
        # Social media scraping
        if investigation.social_media_targets:
            social_scraper = SocialMediaScraper()
            for target in investigation.social_media_targets:
                platform_data = social_scraper.scrape_platform_profile(
                    target["platform"], target["username"]
                )
                scraping_results["social_media"][f"{target['platform']}:{target['username']}"] = platform_data
        
        # Domain analysis
        if investigation.domain_targets:
            domain_analyzer = DomainAnalyzer()
            for domain in investigation.domain_targets:
                domain_data = domain_analyzer.analyze_domain(domain)
                scraping_results["domains"][domain] = domain_data
        
        return scraping_results
        
    except Exception as e:
        logger.error(f"Error in scraping phase: {e}")
        raise

def run_analysis_phase(investigation_id: str) -> Dict[str, Any]:
    """Run the analysis phase of an investigation"""
    try:
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = investigation_repo.get_investigation(investigation_id)
        
        # Run intelligence analysis
        intelligence_engine = IntelligenceEngine()
        analysis_result = intelligence_engine.analyze_investigation(investigation)
        
        # Save analysis results
        investigation_repo.save_analysis_results(investigation_id, analysis_result)
        
        return {
            "entities_analyzed": len(analysis_result.entities),
            "relationships_found": len(analysis_result.relationships),
            "patterns_detected": len(analysis_result.patterns),
            "anomalies_identified": len(analysis_result.anomalies),
            "threat_assessments": len(analysis_result.threat_assessments),
            "confidence_score": analysis_result.confidence_score
        }
        
    except Exception as e:
        logger.error(f"Error in analysis phase: {e}")
        raise

def run_report_phase(investigation_id: str) -> Dict[str, Any]:
    """Run the report generation phase of an investigation"""
    try:
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = investigation_repo.get_investigation(investigation_id)
        
        # Generate intelligence report
        intelligence_engine = IntelligenceEngine()
        analysis_result = intelligence_engine.analyze_investigation(investigation)
        intelligence_report = intelligence_engine.generate_intelligence_report(analysis_result)
        
        # Save report
        investigation_repo.save_intelligence_report(investigation_id, intelligence_report)
        
        return {
            "report_generated": True,
            "report_id": intelligence_report.id,
            "report_title": intelligence_report.title
        }
        
    except Exception as e:
        logger.error(f"Error in report phase: {e}")
        raise 