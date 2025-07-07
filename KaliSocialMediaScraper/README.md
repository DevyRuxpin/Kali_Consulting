# Kali OSINT Social Media Scraper Platform

A comprehensive, enterprise-grade Open Source Intelligence (OSINT) investigation platform designed for professional security research, law enforcement, and threat intelligence operations. This platform provides advanced social media scraping, real-time threat analysis, network intelligence, and automated report generation with a modern, responsive web interface.

## 🚀 Core Features

### 🔍 Advanced Investigation Capabilities
- **Multi-Platform Social Media Scraping**: Real-time scraping across Twitter, Instagram, Reddit, GitHub, LinkedIn, Facebook, YouTube, TikTok, Telegram, and Discord
- **Comprehensive Domain Intelligence**: Deep domain analysis including subdomain enumeration, DNS records, WHOIS data, SSL certificates, and technology detection
- **Network Analysis & Visualization**: Entity relationship mapping, community detection, and interactive network graphs
- **Threat Assessment Engine**: AI-powered threat scoring, anomaly detection, and risk analysis
- **Dark Web Intelligence**: Tor network scanning and dark web entity discovery (experimental)

### 🛡️ Security & Intelligence Features
- **Real-time Threat Detection**: Automated threat scoring with configurable thresholds
- **Anomaly Detection**: Machine learning-based pattern recognition and behavioral analysis
- **Entity Resolution**: Cross-platform entity correlation and relationship mapping
- **Intelligence Fusion**: Correlate data across multiple sources and platforms
- **Pattern Analysis**: Advanced pattern recognition for threat indicators

### 📊 Analytics & Reporting
- **Interactive Dashboard**: Real-time monitoring with live statistics and progress tracking
- **Advanced Analytics**: Network graphs, timeline analysis, and geographic mapping
- **Automated Report Generation**: PDF, CSV, JSON, and HTML report formats
- **Export Capabilities**: Comprehensive data export with customizable formats
- **Progress Tracking**: Real-time investigation progress with estimated completion times

### 🎨 Modern Web Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Dark Mode Support**: Toggle between light and dark themes
- **Real-time Updates**: WebSocket-based live updates and notifications
- **Interactive Visualizations**: Charts, graphs, and network diagrams
- **Professional UI/UX**: Clean, modern interface with cyberpunk aesthetics

## 🏗️ Technical Architecture

### Backend Stack
- **FastAPI**: High-performance async web framework
- **SQLAlchemy**: Advanced ORM with PostgreSQL/SQLite support
- **Celery**: Distributed task queue for background processing
- **Redis**: Caching and session management
- **Playwright**: Advanced browser automation for web scraping
- **Alembic**: Database migration management

### Frontend Stack
- **React 18**: Latest React with concurrent features
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **React Query**: Server state management
- **Chart.js**: Interactive data visualizations

### AI/ML Capabilities
- **Machine Learning Intelligence**: Advanced ML models for threat prediction
- **Natural Language Processing**: Sentiment analysis and text classification
- **Anomaly Detection**: Behavioral pattern recognition
- **Entity Resolution**: Cross-platform entity correlation
- **Threat Classification**: Automated threat level assessment

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.9+ (recommended 3.11+)
- **Node.js**: 16+ (for frontend development)
- **PostgreSQL**: 12+ (recommended) or SQLite
- **Redis**: 6+ (for background tasks)
- **Memory**: 4GB RAM minimum, 8GB+ recommended
- **Storage**: 10GB+ available space

### Recommended Setup
- **CPU**: 4+ cores
- **Memory**: 16GB+ RAM
- **Storage**: SSD with 50GB+ available space
- **Network**: Stable internet connection for scraping

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd KaliSocialMediaScraper
```

### 2. Install Python Dependencies
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Install Playwright Browsers
```bash
playwright install
```

### 4. Setup Database
```bash
# Run database migrations
alembic upgrade head

# Initialize database
python -m app.utils.db_init
```

### 5. Install Frontend Dependencies
```bash
cd frontend
npm install
```

### 6. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

## 🚀 Quick Start

### Automated Startup (Recommended)
```bash
# Run the automated startup script
python start_platform.py
```

This script will:
- Check and install missing dependencies
- Setup the database and run migrations
- Install Playwright browsers
- Start the backend server (FastAPI)
- Start the frontend development server (React)

### Manual Startup

#### Backend Server
```bash
# Start the FastAPI backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Server
```bash
# Start the React frontend
cd frontend
npm start
```

## 🌐 Access Points

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Interactive API Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/kali_osint
DATABASE_TEST_URL=sqlite:///./kali_osint_test.db

# Redis Configuration
REDIS_URL=redis://localhost:6379
REDIS_HOST=localhost
REDIS_PORT=6379

# Security Settings
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Settings
ALLOWED_HOSTS=["http://localhost:3000", "http://localhost:8000"]
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Scraping Configuration
SCRAPING_DELAY=1.0
MAX_CONCURRENT_REQUESTS=16
USER_AGENT_ROTATION=true
REQUEST_TIMEOUT=30
PROXY_ROTATION=false

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Analysis Settings
MAX_ANALYSIS_DEPTH=3
NETWORK_GRAPH_MAX_NODES=1000
THREAT_SCORE_THRESHOLD=0.7
THREAT_INTELLIGENCE_ENABLED=true
ANOMALY_DETECTION_ENABLED=true

# Optional API Keys (for enhanced functionality)
SHODAN_API_KEY=your-shodan-api-key
CENSYS_API_ID=your-censys-api-id
CENSYS_API_SECRET=your-censys-api-secret
VIRUSTOTAL_API_KEY=your-virustotal-api-key
```

### Settings Management
The platform includes a comprehensive settings management system accessible via:

- **API Endpoints**: `/api/v1/settings`
- **Frontend UI**: Settings page in the web interface

Settings categories:
- **Scraping**: User agent rotation, proxy settings, delays, rate limits
- **Security**: Threat detection thresholds, anomaly detection, auto-blocking
- **Analysis**: Analysis depth, network graph limits, timeline settings
- **Notifications**: Email and webhook notifications
- **Export**: Report formats and export options

## 📊 Usage Examples

### 1. Create a Comprehensive Investigation
```python
import requests

# Create investigation
investigation_data = {
    "target_type": "username",
    "target_value": "target_user",
    "analysis_depth": "comprehensive",
    "platforms": ["github", "twitter", "instagram", "linkedin"],
    "include_network_analysis": True,
    "include_timeline_analysis": True,
    "include_threat_assessment": True,
    "analysis_options": {
        "max_depth": 3,
        "include_relationships": True,
        "threat_threshold": 0.7
    }
}

response = requests.post("http://localhost:8000/api/v1/investigations", json=investigation_data)
investigation_id = response.json()["id"]
```

### 2. Domain Intelligence Analysis
```python
# Analyze domain with comprehensive options
domain_data = {
    "domain": "example.com",
    "include_subdomains": True,
    "include_dns": True,
    "include_whois": True,
    "include_ssl": True,
    "include_technologies": True,
    "include_threat_analysis": True
}

response = requests.post("http://localhost:8000/api/v1/analysis/domain", json=domain_data)
```

### 3. Generate Comprehensive Report
```python
# Generate PDF report with all findings
report_data = {
    "investigation_id": investigation_id,
    "report_type": "pdf",
    "include_network_graphs": True,
    "include_timeline": True,
    "include_threat_assessment": True,
    "include_raw_data": False
}

response = requests.post("http://localhost:8000/api/v1/exports/investigation/{investigation_id}/pdf", json=report_data)
```

### 4. Real-time Monitoring
```python
# Monitor investigation progress
import websockets
import asyncio

async def monitor_investigation(investigation_id):
    async with websockets.connect(f"ws://localhost:8000/ws") as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Progress: {data.get('progress', 0)}%")
```

## 🧪 Testing & Validation

### Run Comprehensive Tests
```bash
# Test all functionality including real scraping
python test_real_functionality.py
```

This comprehensive test suite validates:
- API health and connectivity
- Real social media scraping (GitHub, Twitter, etc.)
- Domain intelligence and analysis
- Threat assessment and scoring
- Report generation and export
- Settings management
- Database operations

### Test Individual Components
```bash
# Test domain analyzer specifically
python test_domain_analyzer.py

# Test general functionality
python test_functionality.py
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📁 Project Structure

```
KaliSocialMediaScraper/
├── app/                          # Backend application
│   ├── api/                      # API endpoints and routing
│   │   └── v1/
│   │       ├── endpoints/        # Individual endpoint modules
│   │       ├── api.py           # Main API router
│   │       └── docs.py          # API documentation
│   ├── core/                     # Core configuration and utilities
│   │   ├── config.py            # Application settings
│   │   ├── database.py          # Database configuration
│   │   ├── auth.py              # Authentication utilities
│   │   └── celery_app.py        # Background task configuration
│   ├── models/                   # Database models and schemas
│   │   ├── database.py          # SQLAlchemy models
│   │   └── schemas.py           # Pydantic schemas
│   ├── repositories/             # Data access layer
│   │   ├── base_repository.py   # Base repository pattern
│   │   ├── investigation_repository.py
│   │   ├── social_media_repository.py
│   │   └── user_repository.py
│   ├── services/                 # Business logic and external services
│   │   ├── social_media_scraper.py    # Multi-platform scraping
│   │   ├── github_scraper.py          # GitHub-specific scraping
│   │   ├── domain_analyzer.py         # Domain intelligence
│   │   ├── network_analyzer.py        # Network analysis
│   │   ├── threat_analyzer.py         # Threat assessment
│   │   ├── ml_intelligence.py         # Machine learning
│   │   ├── anomaly_detector.py        # Anomaly detection
│   │   ├── pattern_analyzer.py        # Pattern recognition
│   │   ├── dark_web_intelligence.py   # Dark web scanning
│   │   ├── intelligence_engine.py     # Intelligence fusion
│   │   ├── entity_resolver.py         # Entity resolution
│   │   ├── threat_correlator.py       # Threat correlation
│   │   └── proxy_rotator.py           # Proxy management
│   └── tasks/                    # Background task processing
│       ├── analysis_tasks.py     # Analysis background tasks
│       ├── investigation_tasks.py # Investigation processing
│       ├── scraping_tasks.py     # Scraping background tasks
│       ├── report_tasks.py       # Report generation tasks
│       └── maintenance_tasks.py  # System maintenance
├── frontend/                     # React frontend application
│   ├── src/
│   │   ├── components/           # Reusable React components
│   │   │   ├── Layout.tsx       # Main layout component
│   │   │   └── RealTimeDashboard.tsx
│   │   ├── pages/                # Page components
│   │   │   ├── Dashboard.tsx    # Main dashboard
│   │   │   ├── Investigations.tsx # Investigation management
│   │   │   ├── SocialMedia.tsx  # Social media analysis
│   │   │   ├── Analysis.tsx     # Advanced analytics
│   │   │   ├── Reports.tsx      # Report management
│   │   │   └── Settings.tsx     # Platform settings
│   │   ├── services/             # API service layer
│   │   │   ├── api.ts           # Base API client
│   │   │   └── investigations.ts # Investigation API
│   │   ├── hooks/                # Custom React hooks
│   │   │   ├── useDashboardData.ts
│   │   │   └── useRealTimeData.ts
│   │   └── styles/               # Styling and CSS
│   ├── public/                   # Static assets
│   └── package.json              # Frontend dependencies
├── alembic/                      # Database migrations
│   ├── versions/                 # Migration files
│   └── env.py                    # Migration environment
├── static/                       # Static files served by FastAPI
├── reports/                      # Generated reports storage
├── logs/                         # Application logs
├── data/                         # Data storage
├── docs/                         # Documentation
├── tests/                        # Test files
├── requirements.txt              # Python dependencies
├── start_platform.py            # Automated startup script
├── docker-compose.yml           # Docker configuration
└── README.md                    # This file
```

## 🔍 API Endpoints

### Investigations
- `POST /api/v1/investigations` - Create new investigation
- `GET /api/v1/investigations` - List all investigations
- `GET /api/v1/investigations/{id}` - Get investigation details
- `PUT /api/v1/investigations/{id}` - Update investigation
- `DELETE /api/v1/investigations/{id}` - Delete investigation
- `GET /api/v1/investigations/{id}/status` - Get investigation status
- `GET /api/v1/investigations/{id}/findings` - Get investigation findings

### Social Media Analysis
- `POST /api/v1/social-media/scrape` - Scrape social media profiles
- `GET /api/v1/social-media/search` - Search social media content
- `GET /api/v1/social-media/platforms` - Get available platforms
- `POST /api/v1/social-media/analyze` - Analyze social media data

### Domain Intelligence
- `POST /api/v1/analysis/domain` - Analyze domain comprehensively
- `GET /api/v1/analysis/domain/{domain}/subdomains` - Get subdomains
- `GET /api/v1/analysis/domain/{domain}/dns` - Get DNS records
- `GET /api/v1/analysis/domain/{domain}/whois` - Get WHOIS data
- `GET /api/v1/analysis/domain/{domain}/ssl` - Get SSL certificate

### Network Analysis
- `GET /api/v1/analysis/network/{entity_id}` - Get network graph
- `POST /api/v1/analysis/network/generate` - Generate network analysis
- `GET /api/v1/analysis/timeline/{entity_id}` - Get timeline data
- `POST /api/v1/analysis/timeline/generate` - Generate timeline

### Threat Intelligence
- `POST /api/v1/analysis/threat` - Analyze threat level
- `GET /api/v1/analysis/threat/indicators` - Get threat indicators
- `POST /api/v1/analysis/anomaly` - Detect anomalies
- `GET /api/v1/analysis/anomaly/patterns` - Get anomaly patterns

### Reports & Exports
- `POST /api/v1/exports/investigation/{id}/pdf` - Generate PDF report
- `POST /api/v1/exports/investigation/{id}/csv` - Generate CSV export
- `POST /api/v1/exports/investigation/{id}/json` - Generate JSON export
- `GET /api/v1/exports/reports` - List generated reports
- `GET /api/v1/exports/reports/{id}/download` - Download report

### Dashboard & Analytics
- `GET /api/v1/dashboard/stats` - Get dashboard statistics
- `GET /api/v1/dashboard/recent` - Get recent activity
- `GET /api/v1/dashboard/threats` - Get threat summary
- `GET /api/v1/dashboard/performance` - Get system performance

### Settings Management
- `GET /api/v1/settings` - Get all platform settings
- `PUT /api/v1/settings/{category}` - Update settings category
- `POST /api/v1/settings/reset` - Reset settings to defaults
- `GET /api/v1/settings/categories` - Get settings categories

### System Health
- `GET /api/v1/health` - System health check
- `GET /api/v1/health/services` - Service status
- `GET /api/v1/health/metrics` - System metrics

### Real-time Updates
- `WS /ws` - WebSocket endpoint for real-time updates

## 🛡️ Security Features

### Platform Security
- **Rate Limiting**: Configurable request limits per endpoint
- **Input Validation**: Comprehensive input sanitization and validation
- **Error Handling**: Secure error handling without information leakage
- **Authentication**: JWT-based authentication system
- **Authorization**: Role-based access control

### Scraping Security
- **Proxy Support**: Rotating proxy support for anonymity
- **User Agent Rotation**: Automatic user agent rotation
- **Request Throttling**: Configurable delays between requests
- **SSL Verification**: Configurable SSL certificate verification
- **Timeout Management**: Request timeout configuration

### Threat Intelligence
- **Threat Detection**: AI-powered threat assessment
- **Anomaly Detection**: Automated anomaly identification
- **Pattern Recognition**: Advanced pattern analysis
- **Risk Scoring**: Configurable risk assessment thresholds
- **Intelligence Fusion**: Cross-source threat correlation

## 📈 Performance & Scalability

### Performance Optimizations
- **Asynchronous Processing**: Non-blocking operations throughout
- **Background Tasks**: Celery-based task queue for heavy operations
- **Caching**: Redis-based caching for frequently accessed data
- **Connection Pooling**: Efficient database connection management
- **Memory Management**: Optimized memory usage and garbage collection

### Scalability Features
- **Horizontal Scaling**: Support for multiple backend instances
- **Load Balancing**: Ready for load balancer integration
- **Database Optimization**: Efficient queries and indexing
- **Task Distribution**: Distributed task processing
- **Resource Management**: Configurable resource limits

### Monitoring & Metrics
- **Health Checks**: Comprehensive system health monitoring
- **Performance Metrics**: Real-time performance tracking
- **Error Tracking**: Detailed error logging and monitoring
- **Resource Usage**: Memory, CPU, and network monitoring
- **Custom Metrics**: Application-specific metrics collection

## 🤝 Contributing

We welcome contributions from the security research community!

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes with proper testing
4. Add tests for new functionality
5. Ensure all tests pass: `python test_real_functionality.py`
6. Submit a pull request

### Code Standards
- **Python**: Follow PEP 8 style guidelines
- **TypeScript**: Use strict TypeScript configuration
- **Testing**: Maintain high test coverage
- **Documentation**: Update documentation for new features
- **Security**: Follow security best practices

### Testing Guidelines
- **Unit Tests**: Test individual components
- **Integration Tests**: Test API endpoints
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Test under load
- **Security Tests**: Test security features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Legal Disclaimer

This platform is designed for **legitimate OSINT research, security research, and law enforcement purposes only**. Users are responsible for:

- Complying with all applicable laws and regulations
- Respecting terms of service of target platforms
- Obtaining proper authorization for investigations
- Using the platform ethically and responsibly
- Not using the platform for malicious purposes

The developers are not responsible for misuse of this platform.

## 🆘 Support & Documentation

### Getting Help
- **API Documentation**: Interactive docs at `/docs`
- **Code Examples**: Review test files for usage examples
- **Issue Tracking**: Report bugs and feature requests on GitHub
- **Community**: Join our security research community

### Documentation
- **API Reference**: Complete API documentation
- **User Guide**: Step-by-step usage instructions
- **Developer Guide**: Development and contribution guidelines
- **Security Guide**: Security best practices and recommendations

### Troubleshooting
- **Health Checks**: Use `/health` endpoint for system status
- **Logs**: Check application logs for detailed error information
- **Testing**: Run test suite to validate functionality
- **Configuration**: Verify environment variables and settings

## 🔄 Recent Updates

### Latest Features (v1.0.0)
- **Advanced ML Intelligence**: Enhanced machine learning capabilities
- **Dark Web Intelligence**: Tor network scanning capabilities
- **Real-time Dashboard**: Live monitoring and progress tracking
- **Enhanced UI/UX**: Modern, responsive interface with dark mode
- **Comprehensive Testing**: Full test suite with real functionality validation
- **Performance Optimizations**: Improved scalability and performance
- **Security Enhancements**: Advanced threat detection and anomaly analysis
- **Export Capabilities**: Multiple report formats and export options

### Planned Features
- **Additional Platforms**: Support for more social media platforms
- **Advanced Analytics**: Enhanced visualization and analysis tools
- **Mobile App**: Native mobile application
- **API Enhancements**: Additional endpoints and capabilities
- **Performance Improvements**: Further optimization and scaling

---

**Built with ❤️ for the security research community** 