"""
Investigation Background Tasks
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from celery import current_task

from app.core.celery_app import celery_app
from app.models.schemas import Investigation, InvestigationStatus
from app.repositories.investigation_repository import InvestigationRepository
from app.services.github_scraper import GitHubScraper
from app.services.social_media_scraper import SocialMediaScraper
from app.services.domain_analyzer import DomainAnalyzer
from app.services.intelligence_engine import IntelligenceEngine

logger = logging.getLogger(__name__)

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
        
        # Step 1: Scraping Phase
        self.update_state(
            state="PROGRESS",
            meta={"status": "Scraping data", "progress": 20}
        )
        
        scraping_results = run_scraping_phase(investigation)
        
        # Step 2: Analysis Phase
        self.update_state(
            state="PROGRESS",
            meta={"status": "Analyzing data", "progress": 60}
        )
        
        analysis_results = run_analysis_phase(investigation_id)
        
        # Step 3: Report Generation
        self.update_state(
            state="PROGRESS",
            meta={"status": "Generating report", "progress": 80}
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
            "report_results": report_results
        }
        
    except Exception as e:
        logger.error(f"Error running full investigation {investigation_id}: {e}")
        
        # Update investigation status to failed
        try:
            investigation_repo = InvestigationRepository()
            investigation_repo.update_investigation_status(investigation_id, "FAILED")
        except Exception as update_error:
            logger.error(f"Error updating investigation status: {update_error}")
        
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
                meta={"status": "Scraping repositories", "progress": 30}
            )
            
            for target in investigation.github_targets:
                if target.get("type") == "repository":
                    repo_data = github_scraper.scrape_repository(target["value"])
                    investigation_repo.add_github_data(investigation_id, repo_data)
                
                elif target.get("type") == "user":
                    user_data = github_scraper.scrape_user(target["value"])
                    investigation_repo.add_github_data(investigation_id, user_data)
                
                elif target.get("type") == "organization":
                    org_data = github_scraper.scrape_organization(target["value"])
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
            "targets_processed": len(investigation.github_targets) if investigation.github_targets else 0
        }
        
    except Exception as e:
        logger.error(f"Error scraping GitHub for investigation {investigation_id}: {e}")
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True)
def scrape_social_media_investigation_task(self, investigation_id: str) -> Dict[str, Any]:
    """Scrape social media data for an investigation"""
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
        
        # Initialize social media scraper
        social_scraper = SocialMediaScraper()
        
        # Scrape social media platforms
        if investigation.social_media_targets:
            total_targets = len(investigation.social_media_targets)
            
            for i, target in enumerate(investigation.social_media_targets):
                platform = target.get("platform")
                username = target.get("username")
                
                if platform and username:
                    # Update progress
                    progress = 10 + (i / total_targets) * 80
                    self.update_state(
                        state="PROGRESS",
                        meta={
                            "status": f"Scraping {platform}: {username}",
                            "progress": int(progress)
                        }
                    )
                    
                    # Scrape platform data
                    platform_data = social_scraper.scrape_platform_profile(platform, username)
                    investigation_repo.add_social_media_data(investigation_id, platform_data)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Social media scraping completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "platform": "social_media",
            "targets_processed": len(investigation.social_media_targets) if investigation.social_media_targets else 0
        }
        
    except Exception as e:
        logger.error(f"Error scraping social media for investigation {investigation_id}: {e}")
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
            total_targets = len(investigation.domain_targets)
            
            for i, domain in enumerate(investigation.domain_targets):
                # Update progress
                progress = 10 + (i / total_targets) * 80
                self.update_state(
                    state="PROGRESS",
                    meta={
                        "status": f"Analyzing domain: {domain}",
                        "progress": int(progress)
                    }
                )
                
                # Analyze domain
                domain_data = domain_analyzer.analyze_domain(domain)
                investigation_repo.add_domain_data(investigation_id, domain_data)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Domain analysis completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "platform": "domains",
            "targets_processed": len(investigation.domain_targets) if investigation.domain_targets else 0
        }
        
    except Exception as e:
        logger.error(f"Error analyzing domains for investigation {investigation_id}: {e}")
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
            meta={"status": "Starting analysis", "progress": 10}
        )
        
        # Get investigation
        investigation_repo = InvestigationRepository()
        investigation = investigation_repo.get_investigation(investigation_id)
        
        if not investigation:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        # Initialize intelligence engine
        intelligence_engine = IntelligenceEngine()
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Analyzing entities", "progress": 30}
        )
        
        # Run comprehensive analysis
        analysis_result = intelligence_engine.analyze_investigation(investigation)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Generating report", "progress": 80}
        )
        
        # Generate intelligence report
        intelligence_report = intelligence_engine.generate_intelligence_report(analysis_result)
        
        # Save analysis results
        investigation_repo.save_analysis_results(investigation_id, analysis_result)
        investigation_repo.save_intelligence_report(investigation_id, intelligence_report)
        
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={"status": "Analysis completed", "progress": 100}
        )
        
        return {
            "investigation_id": investigation_id,
            "status": "completed",
            "entities_analyzed": len(analysis_result.entities),
            "relationships_found": len(analysis_result.relationships),
            "patterns_detected": len(analysis_result.patterns),
            "anomalies_identified": len(analysis_result.anomalies),
            "threat_assessments": len(analysis_result.threat_assessments),
            "confidence_score": analysis_result.confidence_score
        }
        
    except Exception as e:
        logger.error(f"Error running intelligence analysis for investigation {investigation_id}: {e}")
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
                    repo_data = github_scraper.scrape_repository(target["value"])
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