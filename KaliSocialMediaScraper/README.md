# Kali OSINT Social Media Scraper Platform

A comprehensive OSINT investigation platform for professional security research and law enforcement. This platform provides real-time social media scraping, threat analysis, network intelligence, and automated report generation.

## 🚀 Features

### Core Functionality
- **Real-time Social Media Scraping**: Multi-platform scraping (Twitter, Instagram, Reddit, GitHub, LinkedIn, Facebook, YouTube, TikTok, Telegram, Discord)
- **Advanced Threat Analysis**: AI-powered threat assessment and risk scoring
- **Network Intelligence**: Entity relationship mapping and community detection
- **Domain Intelligence**: Comprehensive domain analysis and subdomain enumeration
- **Automated Report Generation**: PDF, CSV, and JSON report formats
- **Real-time Dashboard**: Live monitoring and progress tracking
- **Settings Management**: Configurable scraping parameters and security settings

### Technical Capabilities
- **Playwright-based Scraping**: Robust, stealthy web scraping with browser automation
- **Rate Limiting & Proxy Support**: Configurable rate limits and proxy rotation
- **Background Task Processing**: Asynchronous task processing with Celery
- **WebSocket Real-time Updates**: Live progress updates and notifications
- **Comprehensive Logging**: Detailed activity logging and error tracking
- **API Documentation**: Auto-generated OpenAPI documentation

## 📋 Requirements

- Python 3.8+
- Node.js 16+ (for frontend)
- PostgreSQL (recommended) or SQLite
- Redis (for background tasks)
- Playwright browsers

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd KaliSocialMediaScraper
```

### 2. Install Python Dependencies
```bash
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

## 🚀 Quick Start

### Option 1: Automated Startup
```bash
# Run the automated startup script
python start_platform.py
```

This script will:
- Check and install missing dependencies
- Setup the database
- Install Playwright browsers
- Start the backend server
- Start the frontend development server

### Option 2: Manual Startup

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

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/kali_osint

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Settings
ALLOWED_HOSTS=["http://localhost:3000", "http://localhost:8000"]

# Scraping Settings
DEFAULT_DELAY_MIN=2
DEFAULT_DELAY_MAX=5
MAX_RETRIES=3
TIMEOUT_SECONDS=30
```

### Settings Management
The platform includes a comprehensive settings management system accessible via:

- **API Endpoints**: `/api/v1/settings`
- **Frontend UI**: Settings page in the web interface

Settings categories:
- **Scraping**: User agent rotation, proxy settings, delays
- **Rate Limits**: Request limits per minute/hour/day
- **Security**: Threat detection thresholds, anomaly detection
- **Notifications**: Email and webhook notifications

## 📊 Usage Examples

### 1. Social Media Investigation
```python
import requests

# Create investigation
investigation_data = {
    "target_type": "username",
    "target_value": "target_user",
    "analysis_depth": "comprehensive",
    "platforms": ["github", "twitter", "instagram"],
    "include_network_analysis": True,
    "include_threat_assessment": True
}

response = requests.post("http://localhost:8000/api/v1/investigations", json=investigation_data)
investigation_id = response.json()["id"]
```

### 2. Domain Intelligence
```python
# Analyze domain
domain_data = {
    "domain": "example.com",
    "include_subdomains": True,
    "include_dns": True,
    "include_whois": True
}

response = requests.post("http://localhost:8000/api/v1/analysis/domain", json=domain_data)
```

### 3. Report Generation
```python
# Generate PDF report
report_data = {
    "investigation_id": investigation_id,
    "report_type": "pdf"
}

response = requests.post("http://localhost:8000/api/v1/exports/report", json=report_data)
```

## 🧪 Testing

### Run Comprehensive Tests
```bash
# Test all functionality
python test_real_functionality.py
```

This will test:
- API health and connectivity
- Real social media scraping
- GitHub repository analysis
- Domain intelligence
- Threat analysis
- Report generation
- Settings management

### Test Individual Components
```bash
# Test domain analyzer
python test_domain_analyzer.py

# Test specific functionality
python test_functionality.py
```

## 📁 Project Structure

```
KaliSocialMediaScraper/
├── app/                          # Backend application
│   ├── api/                      # API endpoints
│   ├── core/                     # Core configuration
│   ├── models/                   # Database models
│   ├── repositories/             # Data access layer
│   ├── services/                 # Business logic
│   └── tasks/                    # Background tasks
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── pages/                # Page components
│   │   ├── services/             # API services
│   │   └── hooks/                # Custom hooks
├── alembic/                      # Database migrations
├── static/                       # Static files
├── reports/                      # Generated reports
└── docs/                         # Documentation
```

## 🔍 API Endpoints

### Investigations
- `POST /api/v1/investigations` - Create investigation
- `GET /api/v1/investigations` - List investigations
- `GET /api/v1/investigations/{id}` - Get investigation details

### Social Media
- `POST /api/v1/social-media/scrape` - Scrape social media profiles
- `GET /api/v1/social-media/search` - Search social media content

### Analysis
- `POST /api/v1/analysis/domain` - Analyze domain
- `POST /api/v1/analysis/threat` - Threat analysis
- `GET /api/v1/analysis/network/{entity_id}` - Network analysis

### Reports
- `POST /api/v1/exports/investigation/{id}/pdf` - Generate PDF report
- `POST /api/v1/exports/investigation/{id}/csv` - Generate CSV report
- `POST /api/v1/exports/investigation/{id}/json` - Generate JSON report

### Settings
- `GET /api/v1/settings` - Get platform settings
- `PUT /api/v1/settings/{category}` - Update settings
- `POST /api/v1/settings/reset` - Reset settings to defaults

## 🛡️ Security Features

- **Rate Limiting**: Configurable request limits
- **Proxy Support**: Rotating proxy support for anonymity
- **User Agent Rotation**: Automatic user agent rotation
- **Threat Detection**: AI-powered threat assessment
- **Anomaly Detection**: Automated anomaly identification
- **Input Validation**: Comprehensive input sanitization
- **Error Handling**: Secure error handling and logging

## 📈 Performance

- **Asynchronous Processing**: Non-blocking operations
- **Background Tasks**: Celery-based task queue
- **Caching**: Redis-based caching for performance
- **Connection Pooling**: Efficient database connections
- **Memory Management**: Optimized memory usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This platform is designed for legitimate OSINT research and law enforcement purposes only. Users are responsible for complying with all applicable laws and terms of service when using this tool.

## 🆘 Support

For issues and questions:
- Check the API documentation at `/docs`
- Review the test files for usage examples
- Open an issue on GitHub

## 🔄 Updates

The platform is actively maintained with regular updates for:
- New social media platforms
- Enhanced scraping capabilities
- Improved threat analysis
- Bug fixes and performance improvements 