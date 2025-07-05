# Kali OSINT Social Media Scraper Platform

## 🚨 CURRENT STATUS: DEVELOPMENT IN PROGRESS

**Last Updated:** July 5, 2025  
**Status:** Backend functional, Frontend dependency issues  
**Current Issues:** Frontend `ajv` dependency conflicts preventing React app startup

## 📋 Project Overview

A comprehensive OSINT (Open Source Intelligence) investigation platform designed for advanced security research, law enforcement, and threat intelligence gathering. The platform integrates multiple scraping tools and libraries covering a wide range of areas for advanced investigations, including extremist organizations and extremist groups.

### 🎯 Key Features

- **Multi-Platform Social Media Scraping**: GitHub, Twitter, Instagram, Telegram, Discord, Reddit
- **Advanced OSINT Tools**: Domain analysis, network mapping, threat assessment
- **Intelligence Engine**: Pattern detection, anomaly analysis, threat correlation
- **Real-time Analysis**: Background task processing with Celery
- **Professional UI**: React-based frontend with modern design
- **Comprehensive Reporting**: Detailed investigation reports and visualizations

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with async/await support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Background Tasks**: Celery with Redis
- **Search**: Elasticsearch for advanced querying
- **API Documentation**: Auto-generated with OpenAPI/Swagger

### Frontend (React)
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS with Headless UI
- **State Management**: Zustand + React Query
- **Charts**: Recharts for data visualization
- **Routing**: React Router v6

## 📁 Project Structure

```
KaliSocialMediaScraper/
├── app/                          # Backend application
│   ├── api/v1/                   # API endpoints
│   ├── core/                     # Core configuration
│   ├── models/                   # Database models & schemas
│   ├── repositories/             # Data access layer
│   ├── services/                 # Business logic services
│   ├── tasks/                    # Background tasks
│   └── utils/                    # Utility functions
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── pages/                # Page components
│   │   ├── services/             # API services
│   │   └── utils/                # Frontend utilities
│   └── public/                   # Static assets
├── docs/                         # Documentation
├── static/                       # Static files
└── alembic/                      # Database migrations
```

## 🚀 Current Implementation Status

### ✅ Completed Components

#### Backend
- ✅ FastAPI application structure
- ✅ Database models and schemas
- ✅ API endpoints for investigations
- ✅ Background task system with Celery
- ✅ Advanced scraping services (GitHub, social media)
- ✅ Intelligence engine with pattern detection
- ✅ Anomaly detection and threat analysis
- ✅ Network analysis and visualization
- ✅ Comprehensive error handling
- ✅ Health check endpoints
- ✅ CORS middleware configuration

#### Frontend
- ✅ React application structure
- ✅ Modern UI components with Tailwind CSS
- ✅ Dashboard and investigation pages
- ✅ Data visualization components
- ✅ Form handling and validation
- ✅ API integration services
- ✅ Responsive design

#### Infrastructure
- ✅ Docker configuration
- ✅ Database setup with PostgreSQL
- ✅ Redis for caching and message queue
- ✅ Environment configuration
- ✅ Development setup scripts

### ⚠️ Current Issues

#### Frontend Dependencies
- **Issue**: `ajv` dependency conflicts preventing React app startup
- **Error**: `Cannot find module 'ajv/dist/compile/codegen'`
- **Status**: Partially resolved with `ajv@^8.0.0` installation
- **Impact**: Frontend cannot start, blocking full platform testing

#### Backend Dependencies
- **Issue**: Some packages commented out due to compilation issues
- **Packages**: `networkit`, `face-recognition` (resolved)
- **Status**: Core functionality working, advanced features limited

#### Development Environment
- **Issue**: macOS Apple Silicon compatibility challenges
- **Status**: Most issues resolved with Homebrew and manual installations

## 🔧 Installation & Setup

### Prerequisites

- Python 3.11+ (3.13 recommended)
- Node.js 18+ 
- PostgreSQL 13+
- Redis 6+
- Homebrew (macOS)

### Backend Setup

```bash
# Clone repository
git clone <repository-url>
cd KaliSocialMediaScraper

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up database
createdb kali_osint_db
createdb kali_osint_test

# Run migrations
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies (with legacy peer deps for compatibility)
npm install --legacy-peer-deps

# Start development server
npm start
```

### Database Setup

```bash
# Create PostgreSQL user and databases
sudo -u postgres psql
CREATE USER kali_user WITH PASSWORD 'kali_password';
CREATE DATABASE kali_osint_db OWNER kali_user;
CREATE DATABASE kali_osint_test OWNER kali_user;
GRANT ALL PRIVILEGES ON DATABASE kali_osint_db TO kali_user;
GRANT ALL PRIVILEGES ON DATABASE kali_osint_test TO kali_user;
\q
```

## 🧪 Testing

### Backend Health Check
```bash
curl http://localhost:8000/health
```

### Frontend Health Check
```bash
curl http://localhost:3000
```

## 📊 API Endpoints

### Core Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /docs` - API documentation

### Investigation Endpoints
- `POST /api/v1/investigate` - Start investigation
- `GET /api/v1/investigations/{id}` - Get investigation status
- `GET /api/v1/investigations/{id}/results` - Get investigation results

### Analysis Endpoints
- `POST /api/v1/analyze/threat` - Threat analysis
- `GET /api/v1/network-graph/{entity_id}` - Network visualization
- `GET /api/v1/timeline/{entity_id}` - Timeline data

### Social Media Endpoints
- `POST /api/v1/scrape/social-media` - Social media scraping
- `POST /api/v1/analyze/domain` - Domain analysis

## 🔒 Security Features

- No API keys included in codebase
- Environment-based configuration
- Input validation and sanitization
- Rate limiting and request throttling
- Comprehensive error handling
- Audit logging for investigations

## 🚨 Known Issues & Limitations

### Frontend Issues
1. **ajv Dependency Conflict**: React app cannot start due to `ajv` module resolution issues
2. **Package Version Conflicts**: Some packages have peer dependency conflicts
3. **Development Server**: Frontend development server fails to start

### Backend Issues
1. **Missing Dependencies**: Some advanced packages commented out due to compilation issues
2. **Database Connectivity**: Requires manual PostgreSQL setup
3. **Background Tasks**: Celery worker not fully configured

### Environment Issues
1. **macOS Compatibility**: Some packages require manual compilation on Apple Silicon
2. **System Dependencies**: Requires Homebrew and system-level tools
3. **Memory Usage**: Some ML packages require significant memory

## 📈 Next Steps

### Immediate Priorities (Tomorrow)
1. **Fix Frontend Dependencies**: Resolve `ajv` and other package conflicts
2. **Complete Frontend Setup**: Ensure React app starts successfully
3. **Test Full Stack**: Verify backend-frontend communication
4. **Database Integration**: Complete PostgreSQL setup and testing
5. **Background Tasks**: Configure and test Celery workers

### Medium Term
1. **Advanced Features**: Enable commented-out packages
2. **Performance Optimization**: Optimize memory usage and response times
3. **Security Hardening**: Implement additional security measures
4. **Testing Suite**: Comprehensive unit and integration tests
5. **Documentation**: Complete API and user documentation

### Long Term
1. **Production Deployment**: Docker containerization and deployment
2. **Scalability**: Load balancing and horizontal scaling
3. **Advanced Analytics**: Machine learning integration
4. **Real-time Features**: WebSocket support for live updates
5. **Mobile Support**: Progressive web app features

## 🤝 Contributing

This project is under active development. Please refer to the documentation in the `docs/` folder for detailed implementation plans and status updates.

## 📄 License

This project is for educational and research purposes. Please ensure compliance with all applicable laws and platform terms of service when using this tool.

## ⚠️ Disclaimer

This tool is designed for legitimate security research and law enforcement purposes only. Users are responsible for ensuring compliance with all applicable laws, regulations, and platform terms of service. The developers are not responsible for any misuse of this software. 