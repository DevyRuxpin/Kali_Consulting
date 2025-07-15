# 🕵️ Kali Social Media Scraper

> **Advanced Open-Source OSINT Investigation Platform for Comprehensive Digital Intelligence Gathering**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-19.1.0-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Material-UI](https://img.shields.io/badge/Material--UI-7.2.0-blue.svg)](https://mui.com/)
[![Open Source](https://img.shields.io/badge/Open%20Source-100%25-green.svg)](https://opensource.org/)

## 🎯 Overview

The Kali Social Media Scraper is a comprehensive **100% open-source** OSINT (Open Source Intelligence) investigation platform designed for advanced digital intelligence gathering. This powerful tool combines multiple open-source scraping technologies, threat analysis, and network intelligence to provide deep insights into digital footprints across various platforms - **all without requiring any API keys or paid services**.

### ✨ Key Features

- **🔍 Multi-Platform Intelligence Gathering**: GitHub, social media, domain analysis, and more
- **🎯 Advanced Investigation Management**: Create, monitor, and manage OSINT investigations
- **📊 Real-Time Analytics**: Live progress tracking and comprehensive reporting
- **🛡️ Threat Assessment**: Automated threat scoring and risk analysis
- **🌐 Network Intelligence**: Social network analysis and centrality calculations
- **📈 Modern Web Interface**: Responsive Material-UI dashboard with real-time updates
- **🔧 Scalable Architecture**: Microservices-based backend with Celery task processing
- **🆓 100% Open Source**: No API keys required - uses only free, open-source tools

## 🏗️ Architecture

### Backend Stack
- **FastAPI**: High-performance web framework for APIs
- **SQLAlchemy**: Database ORM with PostgreSQL support
- **Celery**: Distributed task queue for background processing
- **Alembic**: Database migration management
- **Pydantic**: Data validation and serialization

### Frontend Stack
- **React 19**: Modern UI framework with TypeScript
- **Material-UI 7**: Professional component library
- **Vite**: Fast build tool and development server
- **React Query**: Server state management
- **React Router**: Client-side routing

### Core Services (Open Source Only)
- **GitHub Intelligence**: User analysis, repository scraping, organization mapping (public API)
- **Social Media Analysis**: Multi-platform username hunting using Sherlock, snscrape, instaloader
- **Domain Intelligence**: DNS analysis, WHOIS data, subdomain enumeration with Sublist3r
- **Threat Assessment**: Risk scoring, indicator correlation, threat modeling
- **Network Analysis**: Social graph analysis, centrality calculations
- **ML Intelligence**: Anomaly detection, pattern recognition

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- PostgreSQL 12+
- Redis (for Celery)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kali-social-media-scraper.git
   cd kali-social-media-scraper
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies (all open-source)
   pip install -r requirements/requirements.txt
   
   # Set up environment variables (no API keys needed!)
   cp config/.env.example .env
   # Edit .env with your configuration
   
   # Initialize database
   alembic upgrade head
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Start the Application**
   ```bash
   # Terminal 1: Start backend
   source venv/bin/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 2: Start frontend
   cd frontend
   npm run dev
   
   # Terminal 3: Start Celery worker (optional)
   source venv/bin/activate
   celery -A app.core.celery_app worker --loglevel=info
   ```

5. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📋 Features

### 🔍 Investigation Management

- **Create Investigations**: Set up new OSINT investigations with custom targets
- **Real-Time Monitoring**: Track investigation progress with live updates
- **Status Management**: Start, pause, and resume investigations
- **Results Analysis**: Comprehensive findings with threat assessments
- **Export Capabilities**: Generate reports in multiple formats

### 🎯 Intelligence Gathering (Open Source Tools)

#### GitHub Intelligence
- User profile analysis and activity tracking (public API)
- Repository content and metadata extraction
- Organization structure mapping
- Threat assessment based on code patterns
- Repository search and filtering

#### Social Media Analysis
- Multi-platform username hunting (Sherlock integration)
- Profile content analysis and sentiment scoring
- Network mapping and relationship analysis
- Post history and engagement metrics
- Cross-platform correlation
- **Supported Platforms**: Twitter (snscrape), Instagram (instaloader), Facebook (facebook-scraper), YouTube (youtube-dl), Reddit (praw), Telegram, Discord

#### Domain Intelligence
- DNS record analysis and enumeration
- WHOIS data extraction and historical tracking
- SSL certificate analysis
- Subdomain discovery and mapping (Sublist3r)
- Technology stack identification
- DNS brute force enumeration

#### Threat Assessment
- Automated risk scoring algorithms
- Indicator of compromise (IoC) detection
- Threat correlation and pattern analysis
- Risk factor identification
- Mitigation recommendations
- DNSBL reputation checking

### 📊 Analytics & Reporting

- **Real-Time Dashboards**: Live investigation status and metrics
- **Progress Tracking**: Visual progress indicators and timelines
- **Statistics Overview**: Investigation counts, success rates, and trends
- **Export Functionality**: PDF, CSV, and JSON report generation
- **Data Visualization**: Charts and graphs for intelligence insights

## 🛠️ API Endpoints

### Core Endpoints
- `GET /api/v1/health/health` - Health check
- `GET /api/v1/investigations/` - List investigations
- `POST /api/v1/investigations/` - Create investigation
- `GET /api/v1/investigations/{id}/` - Get investigation details
- `PUT /api/v1/investigations/{id}/` - Update investigation
- `DELETE /api/v1/investigations/{id}/` - Delete investigation

### Intelligence Endpoints
- `POST /api/v1/github/scrape-user` - GitHub user analysis
- `POST /api/v1/social-media/analyze-profile` - Social media analysis
- `POST /api/v1/domain/analyze` - Domain intelligence
- `POST /api/v1/threat/analyze` - Threat assessment
- `POST /api/v1/analysis/network` - Network analysis

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/kali_scraper

# Redis (for Celery)
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Settings
API_V1_STR=/api/v1
PROJECT_NAME=Kali Social Media Scraper
BACKEND_CORS_ORIGINS=["http://localhost:5173"]

# Open Source Tools Configuration
# Note: All tools work without API keys using public data sources
GITHUB_API_URL=https://api.github.com
TWITTER_SCRAPER_ENABLED=true
INSTAGRAM_SCRAPER_ENABLED=true
FACEBOOK_SCRAPER_ENABLED=true
YOUTUBE_SCRAPER_ENABLED=true
REDDIT_SCRAPER_ENABLED=true
TELEGRAM_SCRAPER_ENABLED=true
DISCORD_SCRAPER_ENABLED=true

# Domain Analysis (Open Source)
WHOIS_SERVER=whois.iana.org
DNS_SERVERS=8.8.8.8,1.1.1.1
SSL_VERIFY=true
SUBDOMAIN_ENUMERATION_ENABLED=true
DNS_BRUTE_FORCE_ENABLED=true

# Threat Intelligence (Open Source)
THREAT_INTELLIGENCE_ENABLED=true
THREAT_SCORE_THRESHOLD=0.7
ANOMALY_DETECTION_ENABLED=true
DNSBL_CHECK_ENABLED=true
REPUTATION_CHECK_ENABLED=true

# Logging
LOG_LEVEL=INFO
```

## 🆓 Open Source Tools Used

### Social Media Scraping
- **snscrape**: Twitter scraping without API keys
- **instaloader**: Instagram scraping
- **facebook-scraper**: Facebook data extraction
- **youtube-dl/yt-dlp**: YouTube video and channel data
- **praw**: Reddit API wrapper
- **telethon**: Telegram client library
- **discord.py**: Discord bot framework

### OSINT Tools
- **Sherlock**: Username enumeration across social media platforms
- **Sublist3r**: Subdomain enumeration
- **Amass**: Network mapping and subdomain discovery
- **theHarvester**: Email, subdomain, and DNS enumeration

### Domain Analysis
- **dnspython**: DNS toolkit
- **python-whois**: WHOIS data extraction
- **phonenumbers**: Phone number parsing and validation

### Machine Learning & Analysis
- **scikit-learn**: Machine learning algorithms
- **numpy/pandas**: Data processing
- **networkx**: Network analysis and graph algorithms
- **spacy**: Natural language processing

## 🧪 Testing

### Run Comprehensive Tests
```bash
# Test all open-source features
python test_open_source_features.py

# Run unit tests
pytest tests/

# Run integration tests
pytest tests/integration/

# Run frontend tests
cd frontend && npm test
```

## 📈 Performance

- **Concurrent Scraping**: Up to 5 simultaneous scrapers
- **Rate Limiting**: Built-in rate limiting to respect platform limits
- **Caching**: Redis-based caching for improved performance
- **Background Processing**: Celery workers for non-blocking operations

## 🔒 Security

- **No API Keys Required**: All tools work with public data sources
- **Rate Limiting**: Automatic rate limiting to prevent abuse
- **Input Validation**: Comprehensive input validation and sanitization
- **Error Handling**: Robust error handling and logging
- **Secure Headers**: Security headers and CORS configuration

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Install development dependencies
pip install -r requirements/requirements.txt
pip install -r requirements/dev-requirements.txt

# Run linting
black app/
flake8 app/
mypy app/

# Run tests
pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Sherlock Project**: For username enumeration capabilities
- **Sublist3r**: For subdomain enumeration
- **snscrape**: For Twitter scraping without API keys
- **instaloader**: For Instagram scraping
- **All open-source contributors**: For making this platform possible

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/kali-social-media-scraper/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/kali-social-media-scraper/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/kali-social-media-scraper/wiki)

---

**⚠️ Disclaimer**: This tool is designed for legitimate OSINT investigations and research purposes only. Users are responsible for complying with all applicable laws and terms of service when using this platform. 