# 🚀 Production Deployment Guide

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Database Configuration](#database-configuration)
4. [Backend Deployment](#backend-deployment)
5. [Frontend Deployment](#frontend-deployment)
6. [Docker Deployment](#docker-deployment)
7. [Monitoring & Logging](#monitoring--logging)
8. [Security Configuration](#security-configuration)
9. [Performance Optimization](#performance-optimization)
10. [Troubleshooting](#troubleshooting)
11. [Maintenance](#maintenance)

## Prerequisites

### System Requirements

- **OS**: Ubuntu 20.04+ / CentOS 8+ / macOS 12+
- **CPU**: 4+ cores (8+ recommended for production)
- **RAM**: 8GB+ (16GB+ recommended for production)
- **Storage**: 50GB+ SSD storage
- **Network**: Stable internet connection

### Software Dependencies

```bash
# System packages
sudo apt update
sudo apt install -y python3.9 python3.9-dev python3.9-venv
sudo apt install -y nodejs npm
sudo apt install -y postgresql postgresql-contrib
sudo apt install -y redis-server
sudo apt install -y nginx
sudo apt install -y git curl wget

# Python dependencies
python3.9 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements/requirements.txt

# Node.js dependencies
cd frontend
npm install
npm run build
```

## Environment Setup

### 1. Create Environment File

```bash
# Copy example environment file
cp config/.env.example .env

# Edit environment variables
nano .env
```

### 2. Environment Configuration

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/kali_osint
DATABASE_TEST_URL=postgresql://username:password@localhost:5432/kali_osint_test

# Redis Configuration
REDIS_URL=redis://localhost:6379
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Security Configuration
SECRET_KEY=your-super-secret-key-change-in-production
API_KEY=your-api-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Kali OSINT Platform
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=3600

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/kali_osint/app.log

# File Storage
UPLOAD_DIR=/var/kali_osint/uploads
EXPORT_DIR=/var/kali_osint/exports
CACHE_DIR=/var/kali_osint/cache
```

### 3. Create Required Directories

```bash
# Create application directories
sudo mkdir -p /var/kali_osint/{uploads,exports,cache,logs}
sudo mkdir -p /var/log/kali_osint

# Set permissions
sudo chown -R $USER:$USER /var/kali_osint
sudo chown -R $USER:$USER /var/log/kali_osint
```

## Database Configuration

### 1. PostgreSQL Setup

```bash
# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql

CREATE DATABASE kali_osint;
CREATE DATABASE kali_osint_test;
CREATE USER kali_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE kali_osint TO kali_user;
GRANT ALL PRIVILEGES ON DATABASE kali_osint_test TO kali_user;
\q
```

### 2. Database Migration

```bash
# Activate virtual environment
source venv/bin/activate

# Run database migrations
alembic upgrade head

# Verify database connection
python -c "from app.core.database import engine; print('Database connected successfully')"
```

### 3. Redis Setup

```bash
# Install Redis
sudo apt install -y redis-server

# Configure Redis
sudo nano /etc/redis/redis.conf

# Add/modify these settings:
maxmemory 256mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000

# Restart Redis
sudo systemctl restart redis
sudo systemctl enable redis

# Test Redis connection
redis-cli ping
```

## Backend Deployment

### 1. Gunicorn Configuration

Create `gunicorn.conf.py`:

```python
# Gunicorn configuration
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
preload_app = True
```

### 2. Systemd Service

Create `/etc/systemd/system/kali-osint.service`:

```ini
[Unit]
Description=Kali OSINT Platform Backend
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/KaliSocialMediaScraper
Environment=PATH=/path/to/KaliSocialMediaScraper/venv/bin
ExecStart=/path/to/KaliSocialMediaScraper/venv/bin/gunicorn app.main:app -c gunicorn.conf.py
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Celery Worker Service

Create `/etc/systemd/system/kali-osint-celery.service`:

```ini
[Unit]
Description=Kali OSINT Platform Celery Worker
After=network.target redis.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/path/to/KaliSocialMediaScraper
Environment=PATH=/path/to/KaliSocialMediaScraper/venv/bin
ExecStart=/path/to/KaliSocialMediaScraper/venv/bin/celery -A app.core.celery_app worker --loglevel=info
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4. Start Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start services
sudo systemctl start kali-osint
sudo systemctl start kali-osint-celery

# Enable services
sudo systemctl enable kali-osint
sudo systemctl enable kali-osint-celery

# Check status
sudo systemctl status kali-osint
sudo systemctl status kali-osint-celery
```

## Frontend Deployment

### 1. Build Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# The build output will be in frontend/dist/
```

### 2. Nginx Configuration

Create `/etc/nginx/sites-available/kali-osint`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend static files
    location / {
        root /path/to/KaliSocialMediaScraper/frontend/dist;
        try_files $uri $uri/ /index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Backend API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout settings
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # WebSocket support
    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
```

### 3. Enable Nginx Site

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/kali-osint /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

## Docker Deployment

### 1. Docker Compose Configuration

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://kali_user:password@db:5432/kali_osint
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ./uploads:/app/uploads
      - ./exports:/app/exports
      - ./logs:/app/logs
    restart: unless-stopped

  celery:
    build: .
    command: celery -A app.core.celery_app worker --loglevel=info
    environment:
      - DATABASE_URL=postgresql://kali_user:password@db:5432/kali_osint
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./uploads:/app/uploads
      - ./exports:/app/exports
      - ./logs:/app/logs
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=kali_osint
      - POSTGRES_USER=kali_user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:6-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./frontend/dist:/usr/share/nginx/html
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### 2. Production Dockerfile

Create `Dockerfile.prod`:

```dockerfile
# Multi-stage build for production
FROM python:3.9-slim as backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY alembic.ini .
COPY alembic/ ./alembic/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "app.main:app", "-b", "0.0.0.0:8000", "-w", "4", "--worker-class", "uvicorn.workers.UvicornWorker"]
```

### 3. Deploy with Docker

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## Monitoring & Logging

### 1. Application Logging

Configure logging in `app/core/config.py`:

```python
# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "json": {
            "format": '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/kali_osint/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "json"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
}
```

### 2. Prometheus Monitoring

Create `monitoring/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'kali-osint'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### 3. Health Checks

Add health check endpoints:

```python
@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    try:
        # Check database
        db_status = "healthy" if await check_database() else "unhealthy"
        
        # Check Redis
        redis_status = "healthy" if await check_redis() else "unhealthy"
        
        # Check Celery
        celery_status = "healthy" if await check_celery() else "unhealthy"
        
        overall_status = "healthy" if all([
            db_status == "healthy",
            redis_status == "healthy",
            celery_status == "healthy"
        ]) else "unhealthy"
        
        return {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "database": db_status,
                "redis": redis_status,
                "celery": celery_status
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
```

## Security Configuration

### 1. SSL/TLS Configuration

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. Firewall Configuration

```bash
# Configure UFW firewall
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Check status
sudo ufw status
```

### 3. Security Headers

Add to Nginx configuration:

```nginx
# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

## Performance Optimization

### 1. Database Optimization

```sql
-- Create indexes for better performance
CREATE INDEX idx_investigations_status ON investigations(status);
CREATE INDEX idx_investigations_created_at ON investigations(created_at);
CREATE INDEX idx_investigations_target_type ON investigations(target_type);

-- Analyze tables
ANALYZE investigations;
ANALYZE entities;
ANALYZE relationships;
```

### 2. Redis Optimization

```bash
# Redis configuration optimization
sudo nano /etc/redis/redis.conf

# Add/modify:
maxmemory 512mb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

### 3. Application Optimization

```python
# Connection pooling
DATABASE_CONFIG = {
    "pool_size": 20,
    "max_overflow": 30,
    "pool_pre_ping": True,
    "pool_recycle": 3600
}

# Caching configuration
CACHE_CONFIG = {
    "default": "redis",
    "redis": {
        "host": "localhost",
        "port": 6379,
        "db": 0,
        "password": None
    }
}
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U kali_user -d kali_osint

# View PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

#### 2. Redis Connection Issues

```bash
# Check Redis status
sudo systemctl status redis

# Test Redis connection
redis-cli ping

# View Redis logs
sudo tail -f /var/log/redis/redis-server.log
```

#### 3. Application Issues

```bash
# Check application logs
sudo tail -f /var/log/kali_osint/app.log

# Check systemd service status
sudo systemctl status kali-osint

# Restart services
sudo systemctl restart kali-osint
sudo systemctl restart kali-osint-celery
```

#### 4. Nginx Issues

```bash
# Check Nginx configuration
sudo nginx -t

# Check Nginx status
sudo systemctl status nginx

# View Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Performance Monitoring

```bash
# Monitor system resources
htop
iotop
nethogs

# Monitor application performance
curl -s http://localhost:8000/health | jq

# Monitor database performance
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"
```

## Maintenance

### 1. Regular Backups

```bash
#!/bin/bash
# backup.sh

# Database backup
pg_dump -h localhost -U kali_user kali_osint > /backups/db_$(date +%Y%m%d_%H%M%S).sql

# Application files backup
tar -czf /backups/app_$(date +%Y%m%d_%H%M%S).tar.gz /var/kali_osint

# Clean old backups (keep last 7 days)
find /backups -name "*.sql" -mtime +7 -delete
find /backups -name "*.tar.gz" -mtime +7 -delete
```

### 2. Log Rotation

```bash
# Configure logrotate
sudo nano /etc/logrotate.d/kali-osint

/var/log/kali_osint/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload kali-osint
    endscript
}
```

### 3. Updates and Maintenance

```bash
# Update system packages
sudo apt update && sudo apt upgrade

# Update application
git pull origin main
source venv/bin/activate
pip install -r requirements/requirements.txt
alembic upgrade head

# Restart services
sudo systemctl restart kali-osint
sudo systemctl restart kali-osint-celery
```

### 4. Monitoring Scripts

```bash
#!/bin/bash
# health_check.sh

# Check application health
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ $response -ne 200 ]; then
    echo "Application health check failed: $response"
    # Send alert
    curl -X POST -H "Content-Type: application/json" \
         -d '{"text":"Kali OSINT Platform health check failed"}' \
         $SLACK_WEBHOOK_URL
fi
```

## Conclusion

This deployment guide provides comprehensive instructions for deploying the Kali OSINT Platform in production. Follow these steps carefully and ensure all security measures are in place before going live.

For additional support, refer to the troubleshooting section or create an issue in the project repository. 