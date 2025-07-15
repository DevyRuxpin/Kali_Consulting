# Requirements & Dependencies

This document outlines all dependencies and requirements for the Kali OSINT Investigation Platform.

## Requirements Files

- `requirements/requirements.txt` - Main requirements file with all dependencies
- `requirements/requirements-core.txt` - Core dependencies only (minimal installation)
- `requirements/requirements-minimal.txt` - Minimal dependencies for basic functionality

## Installation

```bash
# Install all dependencies
pip install -r requirements/requirements.txt

# Install core dependencies only
pip install -r requirements/requirements-core.txt

# Install minimal dependencies
pip install -r requirements/requirements-minimal.txt
```

## Dependencies Categories

### Core Dependencies
- **FastAPI** - High-performance web framework for APIs
- **SQLAlchemy** - Database ORM with PostgreSQL support
- **Alembic** - Database migration management
- **Pydantic** - Data validation and serialization
- **Celery** - Distributed task queue for background processing
- **Redis** - In-memory data structure store (for Celery)

### Scraping Dependencies
- **aiohttp** - Async HTTP client
- **playwright** - Browser automation
- **beautifulsoup4** - HTML parsing
- **requests** - HTTP requests
- **snscrape** - Twitter scraping without API keys
- **instaloader** - Instagram scraping
- **facebook-scraper** - Facebook data extraction
- **youtube-dl/yt-dlp** - YouTube video and channel data
- **praw** - Reddit API wrapper
- **telethon** - Telegram client library
- **discord.py** - Discord bot framework

### OSINT Tools
- **Sherlock** - Username enumeration across social media platforms
- **Sublist3r** - Subdomain enumeration
- **Amass** - Network mapping and subdomain discovery
- **theHarvester** - Email, subdomain, and DNS enumeration

### Analysis Dependencies
- **numpy** - Numerical computing
- **pandas** - Data manipulation
- **scikit-learn** - Machine learning algorithms
- **networkx** - Network analysis and graph algorithms
- **spacy** - Natural language processing

### Domain Analysis
- **dnspython** - DNS toolkit
- **python-whois** - WHOIS data extraction
- **phonenumbers** - Phone number parsing and validation

### Development Dependencies
- **pytest** - Testing framework
- **black** - Code formatting
- **flake8** - Linting
- **mypy** - Type checking
- **pre-commit** - Git hooks for code quality

## System Dependencies

### macOS (via Homebrew)
```bash
# Install system dependencies
brew install python@3.11
brew install redis
brew install postgresql
brew install openblas  # For numpy/scipy performance
```

### Ubuntu/Debian
```bash
# Install system dependencies
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
sudo apt install redis-server postgresql postgresql-contrib
sudo apt install libopenblas-dev liblapack-dev
```

### Windows
```bash
# Install via Chocolatey
choco install python redis postgresql
choco install openblas
```

## Virtual Environment

The project uses Python 3.11 for optimal compatibility with all dependencies.

```bash
# Create virtual environment
python3.11 -m venv venv311
source venv311/bin/activate  # On Windows: venv311\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements/requirements.txt
```

## Version Compatibility

- **Python**: 3.11+ (recommended: 3.11.13)
- **Node.js**: 18+ (for frontend)
- **PostgreSQL**: 12+
- **Redis**: 6+
- **OpenBLAS**: Latest stable version

## Troubleshooting

### Common Issues

1. **OpenBLAS Installation Issues**
   ```bash
   # macOS
   brew install openblas
   export OPENBLAS="$(brew --prefix openblas)"
   export CFLAGS="-falign-functions=8 ${CFLAGS}"
   
   # Ubuntu
   sudo apt install libopenblas-dev
   ```

2. **Playwright Installation**
   ```bash
   # Install browser binaries
   playwright install
   ```

3. **Redis Connection Issues**
   ```bash
   # Start Redis service
   brew services start redis  # macOS
   sudo systemctl start redis  # Linux
   ```

4. **PostgreSQL Connection Issues**
   ```bash
   # Start PostgreSQL service
   brew services start postgresql  # macOS
   sudo systemctl start postgresql  # Linux
   ``` 