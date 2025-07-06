# Kali OSINT Social Media Scraper Platform

## 🚀 CURRENT STATUS: ENHANCED & PRODUCTION-READY

**Last Updated:** January 2025  
**Status:** ✅ **ENHANCED** - Advanced Anti-Detection & Real-Time Features  
**Platform:** Enterprise-grade OSINT investigation platform with robust scraping capabilities

## 📋 Project Overview

A comprehensive OSINT (Open Source Intelligence) investigation platform designed for advanced security research, law enforcement, and threat intelligence gathering. The platform integrates multiple scraping tools and libraries covering a wide range of areas for advanced investigations, including extremist organizations and extremist groups.

### 🎯 Key Features

- **Advanced Anti-Detection Scraping**: Playwright-based scraping with user-agent rotation, proxy support, and random delays
- **Multi-Platform Social Media Scraping**: GitHub, Twitter, Instagram, Telegram, Discord, Reddit, YouTube, LinkedIn, Facebook, TikTok
- **Real-Time Intelligence Dashboard**: Live monitoring with WebSocket support and auto-reconnection
- **Advanced OSINT Tools**: Domain analysis, network mapping, threat assessment
- **Intelligence Engine**: Pattern detection, anomaly analysis, threat correlation
- **Comprehensive Settings**: Configurable scraping behavior, proxy management, rate limiting
- **Professional UI**: React-based frontend with modern design and real-time updates
- **Comprehensive Reporting**: Detailed investigation reports and visualizations

## 🏗️ Architecture

### Backend (FastAPI) ✅ ENHANCED
- **Framework**: FastAPI with async/await support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Background Tasks**: Celery with Redis
- **Search**: Elasticsearch for advanced querying
- **API Documentation**: Auto-generated with OpenAPI/Swagger
- **Advanced Scraping**: Playwright with anti-detection measures
- **Real-Time Features**: WebSocket support for live updates

### Frontend (React) ✅ ENHANCED
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS with Headless UI
- **State Management**: Custom hooks with real-time data fetching
- **Charts**: Recharts for data visualization
- **Routing**: React Router v6
- **Real-Time Updates**: WebSocket integration with auto-reconnection
- **Error Handling**: Comprehensive error states and retry logic

## 📁 Project Structure

```
KaliSocialMediaScraper/
├── app/                          # Backend application ✅ ENHANCED
│   ├── api/v1/                   # API endpoints ✅
│   │   ├── endpoints/            # Individual endpoint modules
│   │   │   ├── investigations.py # Investigation management
│   │   │   ├── social_media.py  # Social media scraping
│   │   │   ├── analysis.py      # Intelligence analysis
│   │   │   ├── exports.py       # Report generation
│   │   │   ├── auth.py          # Authentication
│   │   │   └── health.py        # Health monitoring
│   ├── core/                     # Core configuration ✅
│   │   ├── config.py            # Application settings
│   │   ├── database.py          # Database connection
│   │   ├── celery_app.py        # Background tasks
│   │   └── middleware.py        # Request middleware
│   ├── models/                   # Database models & schemas ✅
│   │   ├── database.py          # SQLAlchemy models
│   │   └── schemas.py           # Pydantic schemas
│   ├── repositories/             # Data access layer ✅
│   │   ├── base_repository.py   # Base repository pattern
│   │   ├── investigation_repository.py
│   │   ├── social_media_repository.py
│   │   └── user_repository.py
│   ├── services/                 # Business logic services ✅ ENHANCED
│   │   ├── playwright_utils.py  # NEW: Anti-detection utilities
│   │   ├── github_scraper.py    # GitHub data collection
│   │   ├── social_media_scraper.py # ENHANCED: Playwright-based scraping
│   │   ├── intelligence_engine.py # Advanced analysis
│   │   ├── anomaly_detector.py  # Pattern detection
│   │   ├── network_analyzer.py  # Network visualization
│   │   ├── threat_analyzer.py   # Threat assessment
│   │   ├── pattern_analyzer.py  # Pattern analysis
│   │   ├── entity_resolver.py   # Entity correlation
│   │   ├── threat_correlator.py # Threat correlation
│   │   └── domain_analyzer.py   # Domain intelligence
│   ├── tasks/                    # Background tasks ✅
│   │   ├── investigation_tasks.py
│   │   ├── scraping_tasks.py
│   │   ├── analysis_tasks.py
│   │   ├── report_tasks.py
│   │   └── maintenance_tasks.py
│   └── utils/                    # Utility functions ✅
├── frontend/                     # React frontend ✅ ENHANCED
│   ├── src/
│   │   ├── components/           # React components ✅ ENHANCED
│   │   │   ├── Layout.tsx       # Main layout component
│   │   │   └── RealTimeDashboard.tsx # ENHANCED: Real-time monitoring
│   │   ├── pages/                # Page components ✅ ENHANCED
│   │   │   ├── Dashboard.tsx    # ENHANCED: Real data integration
│   │   │   ├── Investigations.tsx # Investigation management
│   │   │   ├── SocialMedia.tsx  # Social media analysis
│   │   │   ├── Analysis.tsx     # Intelligence analysis
│   │   │   ├── Reports.tsx      # Report generation
│   │   │   └── Settings.tsx     # NEW: Comprehensive configuration
│   │   ├── services/             # API services ✅ ENHANCED
│   │   │   └── api.ts           # ENHANCED: Comprehensive API client
│   │   ├── hooks/                # NEW: Custom React hooks ✅
│   │   │   ├── useRealTimeData.ts # Real-time data fetching
│   │   │   └── useDashboardData.ts # Dashboard data management
│   │   └── utils/                # Frontend utilities ✅
│   └── public/                   # Static assets ✅
├── docs/                         # Documentation ✅
├── static/                       # Static files ✅
└── alembic/                      # Database migrations ✅
```

## 🚀 Current Implementation Status

### ✅ Enhanced Operational Components

#### Backend Infrastructure ✅ ENHANCED
- ✅ FastAPI application structure with comprehensive API
- ✅ Database models and schemas (PostgreSQL + SQLAlchemy)
- ✅ API endpoints for all core functionality
- ✅ Background task system with Celery and Redis
- ✅ **NEW: Playwright-based scraping with anti-detection measures**
- ✅ **ENHANCED: User-agent rotation and proxy support**
- ✅ **ENHANCED: Random delays and retry logic**
- ✅ Advanced scraping services (GitHub, social media)
- ✅ Intelligence engine with pattern detection
- ✅ Anomaly detection and threat analysis
- ✅ Network analysis and visualization
- ✅ Comprehensive error handling and logging
- ✅ Health check endpoints and monitoring
- ✅ CORS middleware configuration
- ✅ Authentication and authorization system

#### Frontend Infrastructure ✅ ENHANCED
- ✅ React application structure with TypeScript
- ✅ Modern UI components with Tailwind CSS
- ✅ **ENHANCED: Real-time data integration**
- ✅ **NEW: Custom hooks for data management**
- ✅ **ENHANCED: WebSocket support with auto-reconnection**
- ✅ **NEW: Comprehensive settings interface**
- ✅ Dashboard and investigation pages
- ✅ Data visualization components
- ✅ Form handling and validation
- ✅ API integration services
- ✅ Responsive design and routing
- ✅ State management with custom hooks
- ✅ Real-time updates and notifications

#### Infrastructure ✅
- ✅ Docker configuration for all services
- ✅ Database setup with PostgreSQL
- ✅ Redis for caching and message queue
- ✅ Environment configuration management
- ✅ Development and production setups
- ✅ Health monitoring and logging

#### Core Services ✅ ENHANCED
- ✅ **GitHub Scraper**: Repository analysis, user profiling, organization data
- ✅ **ENHANCED Social Media Scraper**: Playwright-based multi-platform scraping
- ✅ **NEW: Anti-Detection Features**: User-agent rotation, proxy support, random delays
- ✅ **Intelligence Engine**: Advanced pattern detection and analysis
- ✅ **Anomaly Detector**: Behavioral analysis and threat detection
- ✅ **Network Analyzer**: Graph generation and visualization
- ✅ **Threat Analyzer**: Risk assessment and scoring
- ✅ **Pattern Analyzer**: Advanced pattern recognition
- ✅ **Entity Resolver**: Entity correlation and linking
- ✅ **Domain Analyzer**: Domain intelligence and analysis

## 🔧 Installation & Setup

### Prerequisites

- Python 3.11+ (3.13 recommended)
- Node.js 18+ 
- PostgreSQL 13+
- Redis 6+
- Homebrew (macOS)

### Quick Start

```bash
# Clone repository
git clone <repository-url>
cd KaliSocialMediaScraper

# Backend Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database Setup
createdb kali_osint_db
createdb kali_osint_test

# Run migrations
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend Setup (in new terminal)
cd frontend
npm install --legacy-peer-deps
npm start
```

### Docker Setup

```bash
# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🧪 Testing

### Health Checks
```bash
# Backend Health
curl http://localhost:8000/health

# Frontend Health
curl http://localhost:3000

# Database Health
psql -h localhost -U kali_user -d kali_osint_db -c "SELECT 1;"
```

### API Testing
```bash
# Access API documentation
open http://localhost:8000/docs

# Test investigation creation
curl -X POST "http://localhost:8000/api/v1/investigations" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Investigation",
    "target_type": "DOMAIN",
    "target_value": "example.com",
    "analysis_options": {
      "include_network_analysis": true,
      "include_threat_assessment": true
    }
  }'
```

## 📊 API Endpoints

### Core Endpoints
- `GET /` - Root endpoint with platform info
- `GET /health` - Comprehensive health check
- `GET /docs` - Interactive API documentation

### Investigation Endpoints
- `POST /api/v1/investigations` - Create new investigation
- `GET /api/v1/investigations` - List all investigations
- `GET /api/v1/investigations/{id}` - Get investigation details
- `PUT /api/v1/investigations/{id}` - Update investigation
- `DELETE /api/v1/investigations/{id}` - Delete investigation

### Analysis Endpoints
- `POST /api/v1/analysis/threat` - Threat analysis
- `GET /api/v1/analysis/network-graph/{entity_id}` - Network visualization
- `GET /api/v1/analysis/timeline/{entity_id}` - Timeline data
- `POST /api/v1/analysis/domain` - Domain analysis

### Social Media Endpoints
- `POST /api/v1/social-media/scrape` - Scrape social media data
- `GET /api/v1/social-media/platforms` - List available platforms
- `GET /api/v1/social-media/data/{investigation_id}` - Get collected data

### Export Endpoints
- `POST /api/v1/exports/report` - Generate investigation report
- `GET /api/v1/exports/{export_id}` - Download report
- `GET /api/v1/exports/formats` - List available formats

## 🎯 Current Capabilities

### Investigation Management
- ✅ Create and manage investigations
- ✅ Track investigation progress
- ✅ Configure analysis options
- ✅ Monitor real-time status
- ✅ Generate comprehensive reports

### Data Collection ✅ ENHANCED
- ✅ GitHub repository analysis
- ✅ **ENHANCED: Multi-platform social media scraping with anti-detection**
- ✅ **NEW: Playwright-based scraping for Twitter, Instagram, YouTube**
- ✅ Domain intelligence gathering
- ✅ Network relationship mapping
- ✅ Timeline data collection

### Intelligence Analysis
- ✅ Threat assessment and scoring
- ✅ Pattern detection and analysis
- ✅ Anomaly detection
- ✅ Entity correlation
- ✅ Network visualization

### Reporting & Export
- ✅ PDF report generation
- ✅ JSON data export
- ✅ CSV data export
- ✅ HTML report generation
- ✅ Custom report templates

## 🔍 Advanced Features

### GitHub Intelligence
- Repository analysis and profiling
- User activity monitoring
- Organization structure analysis
- Code pattern detection
- Threat indicator identification

### Social Media Analysis ✅ ENHANCED
- **ENHANCED: Multi-platform data collection with anti-detection**
- **NEW: Playwright-based scraping for robust data collection**
- **NEW: User-agent rotation and proxy support**
- **NEW: Random delays and retry logic**
- Profile analysis and scoring
- Content sentiment analysis
- Network relationship mapping
- Behavioral pattern detection

### Domain Intelligence
- DNS record analysis
- WHOIS data collection
- SSL certificate analysis
- Subdomain enumeration
- Technology stack identification

### Network Analysis
- Graph-based relationship mapping
- Community detection
- Centrality analysis
- Threat hotspot identification
- Timeline visualization

## 🚀 Production Deployment

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/kali_osint
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-production-secret-key
ENVIRONMENT=production

# API Keys (Optional)
GITHUB_TOKEN=your-github-token
TWITTER_API_KEY=your-twitter-api-key

# NEW: Anti-Detection Settings
ENABLE_PROXY_ROTATION=false
ENABLE_USER_AGENT_ROTATION=true
DEFAULT_DELAY_MIN=2
DEFAULT_DELAY_MAX=5
MAX_RETRIES=3
```

### Docker Production
```bash
# Build and run production containers
docker-compose -f docker-compose.prod.yml up -d

# Monitor logs
docker-compose logs -f

# Scale services
docker-compose up -d --scale celery=3
```

## 📈 Performance & Monitoring

### Health Monitoring
- ✅ Real-time health checks
- ✅ Service status monitoring
- ✅ Performance metrics
- ✅ Error tracking and logging
- ✅ Resource utilization monitoring

### Background Processing
- ✅ Celery worker management
- ✅ Task queue monitoring
- ✅ Progress tracking
- ✅ Error recovery
- ✅ Resource optimization

## 🔒 Security Features

### Authentication & Authorization
- ✅ User authentication system
- ✅ Role-based access control
- ✅ API key management
- ✅ Session management
- ✅ Audit logging

### Data Protection
- ✅ Encrypted data storage
- ✅ Secure API communication
- ✅ Input validation and sanitization
- ✅ Rate limiting
- ✅ CORS protection

### NEW: Anti-Detection Security
- ✅ User-agent rotation
- ✅ Proxy support and rotation
- ✅ Random delays between requests
- ✅ Retry logic with exponential backoff
- ✅ Comprehensive error handling

## 🎉 Success Metrics

### Technical Achievements
- ✅ Complete full-stack application
- ✅ Advanced OSINT capabilities
- ✅ **NEW: Enterprise-grade anti-detection scraping**
- ✅ **NEW: Real-time data integration**
- ✅ **NEW: Comprehensive settings management**
- ✅ Real-time processing
- ✅ Scalable architecture
- ✅ Production-ready deployment

### Feature Completeness
- ✅ 100% Core functionality implemented
- ✅ **ENHANCED: Advanced intelligence features with anti-detection**
- ✅ **NEW: Real-time dashboard with WebSocket support**
- ✅ **NEW: Comprehensive settings interface**
- ✅ Comprehensive reporting system
- ✅ Professional user interface
- ✅ Robust error handling

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Code formatting
black app/
isort app/

# Type checking
mypy app/
```

### Code Standards
- Follow PEP 8 for Python code
- Use TypeScript for frontend code
- Write comprehensive tests
- Document all API endpoints
- Maintain security best practices

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Documentation
- API Documentation: http://localhost:8000/docs
- Code Documentation: Available in `/docs` directory
- Architecture Overview: See project structure above

### Troubleshooting
- Check health endpoints for service status
- Review logs for error details
- Verify database connections
- Test API endpoints individually

---

**Status**: ✅ **ENHANCED & PRODUCTION READY** - Advanced anti-detection features with real-time capabilities 