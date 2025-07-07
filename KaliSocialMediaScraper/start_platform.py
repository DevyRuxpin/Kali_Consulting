#!/usr/bin/env python3
"""
Startup script for Kali OSINT Social Media Scraper Platform
"""

import os
import sys
import subprocess
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required dependencies are installed"""
    logger.info("Checking dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "alembic",
        "playwright",
        "aiohttp",
        "pandas",
        "reportlab"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing packages: {missing_packages}")
        logger.info("Installing missing packages...")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages, check=True)
    
    logger.info("All dependencies are available")

def setup_database():
    """Initialize database and run migrations"""
    logger.info("Setting up database...")
    
    try:
        # Run Alembic migrations
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        logger.info("Database migrations completed")
    except subprocess.CalledProcessError as e:
        logger.error(f"Database migration failed: {e}")
        return False
    
    return True

def install_playwright_browsers():
    """Install Playwright browsers for web scraping"""
    logger.info("Installing Playwright browsers...")
    
    try:
        subprocess.run(["playwright", "install"], check=True)
        logger.info("Playwright browsers installed")
    except subprocess.CalledProcessError as e:
        logger.error(f"Playwright installation failed: {e}")
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    logger.info("Creating directories...")
    
    directories = [
        "static",
        "reports",
        "logs",
        "data",
        "tmp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"Created directory: {directory}")

def start_backend():
    """Start the FastAPI backend server"""
    logger.info("Starting backend server...")
    
    try:
        # Start the FastAPI server
        subprocess.Popen([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
        logger.info("Backend server started on http://localhost:8000")
        return True
    except Exception as e:
        logger.error(f"Failed to start backend: {e}")
        return False

def start_frontend():
    """Start the React frontend development server"""
    logger.info("Starting frontend server...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        logger.error("Frontend directory not found")
        return False
    
    try:
        # Change to frontend directory and start React dev server
        os.chdir(frontend_dir)
        subprocess.Popen([
            "npm", "start"
        ])
        logger.info("Frontend server started on http://localhost:3000")
        return True
    except Exception as e:
        logger.error(f"Failed to start frontend: {e}")
        return False

def main():
    """Main startup function"""
    logger.info("Starting Kali OSINT Social Media Scraper Platform...")
    
    # Check and install dependencies
    check_dependencies()
    
    # Create necessary directories
    create_directories()
    
    # Setup database
    if not setup_database():
        logger.error("Database setup failed")
        return False
    
    # Install Playwright browsers
    if not install_playwright_browsers():
        logger.error("Playwright setup failed")
        return False
    
    # Start backend
    if not start_backend():
        logger.error("Backend startup failed")
        return False
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend
    if not start_frontend():
        logger.error("Frontend startup failed")
        return False
    
    logger.info("Platform startup completed!")
    logger.info("Backend API: http://localhost:8000")
    logger.info("Frontend UI: http://localhost:3000")
    logger.info("API Documentation: http://localhost:8000/docs")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 