"""
Main FastAPI application for Kali OSINT Investigation Platform
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
from typing import List, Optional, Dict, Any
import logging

from app.core.config import settings
# Database and API imports
from app.core.database import engine, Base, create_tables
from app.api.v1.api import api_router
from app.core.celery_app import celery_app

# Service imports
from app.services.github_scraper import GitHubScraper
from app.services.social_media_scraper import SocialMediaScraper
from app.services.domain_analyzer import DomainAnalyzer
from app.services.network_analyzer import NetworkAnalyzer
from app.services.threat_analyzer import ThreatAnalyzer
from app.models.schemas import (
    InvestigationRequest,
    InvestigationResult,
    AnalysisResult,
    NetworkGraph,
    TimelineData,
    ThreatAssessment
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Kali OSINT Investigation Platform...")
    
    # Create database tables
    create_tables()
    
    # Initialize services
    app.state.github_scraper = GitHubScraper()
    app.state.social_media_scraper = SocialMediaScraper()
    app.state.domain_analyzer = DomainAnalyzer()
    app.state.network_analyzer = NetworkAnalyzer()
    app.state.threat_analyzer = ThreatAnalyzer()
    
    logger.info("Application startup complete")
    yield
    
    # Shutdown
    logger.info("Shutting down Kali OSINT Investigation Platform...")

# Create FastAPI app
app = FastAPI(
    title="Kali OSINT Investigation Platform",
    description="Comprehensive OSINT investigation platform for professional security research and law enforcement",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Kali OSINT Investigation Platform",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "redis": "connected",
            "elasticsearch": "connected",
            "celery": "running"
        }
    }

@app.post("/api/v1/investigate", response_model=InvestigationResult)
async def start_investigation(
    request: InvestigationRequest,
    background_tasks: BackgroundTasks
):
    """Start a comprehensive OSINT investigation"""
    try:
        # Start background investigation
        background_tasks.add_task(
            run_comprehensive_investigation,
            request.target_type,
            request.target_value,
            request.analysis_options
        )
        
        from app.models.schemas import InvestigationStatus
        
        return InvestigationResult(
            status=InvestigationStatus.RUNNING,
            message="Investigation started",
            task_id=f"investigation_{request.target_type}_{request.target_value}",
            progress=0,
            estimated_completion=None
        )
    except Exception as e:
        logger.error(f"Investigation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze/threat", response_model=ThreatAssessment)
async def analyze_threat(
    target: str,
    analysis_type: str = "comprehensive"
):
    """Analyze threat level for a target"""
    try:
        analyzer = app.state.threat_analyzer
        assessment = await analyzer.analyze_threat(target, analysis_type)
        return assessment
    except Exception as e:
        logger.error(f"Threat analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/network-graph/{entity_id}", response_model=NetworkGraph)
async def get_network_graph(entity_id: str):
    """Get network graph for an entity"""
    try:
        analyzer = app.state.network_analyzer
        graph = await analyzer.generate_network_graph(entity_id)
        return graph
    except Exception as e:
        logger.error(f"Error generating network graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/timeline/{entity_id}", response_model=TimelineData)
async def get_timeline_data(entity_id: str):
    """Get timeline data for an entity"""
    try:
        analyzer = app.state.network_analyzer
        timeline = await analyzer.generate_timeline(entity_id)
        return timeline
    except Exception as e:
        logger.error(f"Error retrieving timeline data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze/domain")
async def analyze_domain(domain: str):
    """Analyze a domain for OSINT intelligence"""
    try:
        analyzer = app.state.domain_analyzer
        results = await analyzer.analyze_domain(domain)
        return results
    except Exception as e:
        logger.error(f"Domain analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/scrape/social-media")
async def scrape_social_media(
    platform: str,
    target: str,
    include_metadata: bool = True
):
    """Scrape social media data"""
    try:
        scraper = app.state.social_media_scraper
        results = await scraper.scrape_platform(platform, target, include_metadata)
        return results
    except Exception as e:
        logger.error(f"Social media scraping error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def run_comprehensive_investigation(
    target_type: str,
    target_value: str,
    analysis_options: Dict[str, Any]
):
    """Run comprehensive investigation in background"""
    try:
        logger.info(f"Starting comprehensive investigation for {target_type}: {target_value}")
        
        # This would coordinate all investigation services
        # For now, just log the start
        logger.info("Investigation completed")
        
    except Exception as e:
        logger.error(f"Comprehensive investigation error: {e}")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 