# Kali OSINT Investigation Platform - Documentation

Welcome to the comprehensive documentation for the Kali Social Media Scraper, an advanced open-source OSINT investigation platform.

## 📚 Documentation Index

### 🚀 Getting Started
- **[Main README](../README.md)** - Project overview and quick start guide
- **[Requirements & Dependencies](setup/requirements.md)** - Complete dependency list and installation guide
- **[Configuration Guide](setup/configuration.md)** - Environment setup and configuration options
- **[Database Guide](setup/database.md)** - Database setup, management, and maintenance

### 🔧 Development
- **[API Documentation](api/)** - Complete API reference and endpoints
- **[Development Guide](development/)** - Development setup and guidelines
- **[Testing Guide](development/testing.md)** - Testing strategies and procedures

### 🚀 Deployment
- **[Deployment Guide](deployment/)** - Production deployment instructions
- **[Docker Guide](deployment/docker.md)** - Containerized deployment
- **[Performance Tuning](deployment/performance.md)** - Optimization and scaling

## 🎯 Quick Navigation

### For New Users
1. Start with the [Main README](../README.md) for project overview
2. Follow the [Requirements & Dependencies](setup/requirements.md) for installation
3. Configure your environment using [Configuration Guide](setup/configuration.md)
4. Set up your database with [Database Guide](setup/database.md)

### For Developers
1. Review the [API Documentation](api/) for endpoint details
2. Check the [Development Guide](development/) for coding standards
3. Follow the [Testing Guide](development/testing.md) for quality assurance

### For System Administrators
1. Use the [Deployment Guide](deployment/) for production setup
2. Follow the [Docker Guide](deployment/docker.md) for containerization
3. Optimize with [Performance Tuning](deployment/performance.md)

## 🔍 Key Features

### Open Source Intelligence
- **Multi-Platform Scraping**: GitHub, social media, domains, and more
- **Advanced Analysis**: Threat assessment, network analysis, pattern recognition
- **Real-Time Monitoring**: Live investigation tracking and progress updates
- **Comprehensive Reporting**: Detailed reports with actionable insights

### Technical Stack
- **Backend**: FastAPI, SQLAlchemy, Celery, Redis
- **Frontend**: React 19, Material-UI, TypeScript
- **Database**: PostgreSQL/SQLite with Alembic migrations
- **Analysis**: scikit-learn, networkx, pandas, numpy

### Security & Compliance
- **100% Open Source**: No API keys required
- **Privacy Focused**: Local data processing
- **Rate Limiting**: Respectful scraping practices
- **Audit Logging**: Complete activity tracking

## 🛠️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Celery        │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   Workers       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (PostgreSQL)  │
                       └─────────────────┘
```

## 📋 Documentation Standards

### Code Examples
All code examples in this documentation are tested and verified to work with the current version of the platform.

### Version Compatibility
- **Python**: 3.11+ (recommended: 3.11.13)
- **Node.js**: 18+
- **PostgreSQL**: 12+
- **Redis**: 6+

### Contributing to Documentation
1. Follow the existing structure and formatting
2. Include practical examples and use cases
3. Update version numbers and compatibility notes
4. Test all code examples before committing

## 🆘 Support & Troubleshooting

### Common Issues
- **Installation Problems**: Check [Requirements & Dependencies](setup/requirements.md)
- **Configuration Issues**: Review [Configuration Guide](setup/configuration.md)
- **Database Problems**: See [Database Guide](setup/database.md)
- **API Issues**: Consult [API Documentation](api/)

### Getting Help
- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and share solutions
- **Wiki**: Community-maintained knowledge base

## 📄 License

This project and its documentation are licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

---

**⚠️ Disclaimer**: This tool is designed for legitimate OSINT investigations and research purposes only. Users are responsible for complying with all applicable laws and terms of service when using this platform. 