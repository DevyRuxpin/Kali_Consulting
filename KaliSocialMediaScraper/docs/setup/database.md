# Database Guide

This document covers database setup, management, and maintenance for the Kali OSINT Investigation Platform.

## Database Files

- `kali_osint.db` - Main application database (SQLite)
- `kali_osint.db-shm` - SQLite shared memory file
- `kali_osint.db-wal` - SQLite write-ahead log file

## Database Schema

### Core Tables

#### Investigations
```sql
CREATE TABLE investigations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    target_type VARCHAR(50) NOT NULL,
    target_value TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    github_data JSON,
    social_media_data JSON,
    domain_data JSON,
    threat_data JSON,
    network_data JSON
);
```

#### Social Media Data
```sql
CREATE TABLE social_media_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investigation_id INTEGER,
    platform VARCHAR(50) NOT NULL,
    username VARCHAR(255) NOT NULL,
    profile_data JSON,
    posts_data JSON,
    network_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (investigation_id) REFERENCES investigations(id)
);
```

#### Domain Data
```sql
CREATE TABLE domain_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investigation_id INTEGER,
    domain VARCHAR(255) NOT NULL,
    whois_data JSON,
    dns_data JSON,
    ssl_data JSON,
    subdomains JSON,
    technology_stack JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (investigation_id) REFERENCES investigations(id)
);
```

#### Network Data
```sql
CREATE TABLE network_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investigation_id INTEGER,
    network_type VARCHAR(50) NOT NULL,
    nodes JSON,
    edges JSON,
    centrality_data JSON,
    community_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (investigation_id) REFERENCES investigations(id)
);
```

#### Investigation Reports
```sql
CREATE TABLE investigation_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investigation_id INTEGER,
    report_type VARCHAR(50) NOT NULL,
    report_data JSON,
    file_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (investigation_id) REFERENCES investigations(id)
);
```

### Audit Tables

#### Audit Logs
```sql
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(100),
    record_id INTEGER,
    old_values JSON,
    new_values JSON,
    user_id VARCHAR(100),
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### API Requests
```sql
CREATE TABLE api_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER,
    response_time FLOAT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Database Setup

### SQLite (Development)
```bash
# SQLite is used by default for development
# Database file is created automatically at: ./kali_osint.db

# Initialize database with migrations
alembic upgrade head
```

### PostgreSQL (Production)
```bash
# Create database
createdb kali_scraper

# Create user
psql kali_scraper -c "CREATE USER kali_user WITH PASSWORD 'your_password';"
psql kali_scraper -c "GRANT ALL PRIVILEGES ON DATABASE kali_scraper TO kali_user;"

# Update DATABASE_URL in config/.env
DATABASE_URL=postgresql://kali_user:your_password@localhost/kali_scraper

# Run migrations
alembic upgrade head
```

## Database Management

### Backup
```bash
# Create backup with timestamp
cp kali_osint.db kali_osint_backup_$(date +%Y%m%d_%H%M%S).db

# PostgreSQL backup
pg_dump kali_scraper > kali_scraper_backup_$(date +%Y%m%d_%H%M%S).sql

# Automated backup script
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DB_FILE="kali_osint.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/kali_osint_backup_${TIMESTAMP}.db"

mkdir -p $BACKUP_DIR
cp $DB_FILE $BACKUP_FILE
echo "Backup created: $BACKUP_FILE"
```

### Maintenance
```bash
# SQLite optimization
sqlite3 kali_osint.db "VACUUM;"
sqlite3 kali_osint.db "ANALYZE;"
sqlite3 kali_osint.db "REINDEX;"

# Check database integrity
sqlite3 kali_osint.db "PRAGMA integrity_check;"

# PostgreSQL maintenance
psql kali_scraper -c "VACUUM ANALYZE;"
psql kali_scraper -c "REINDEX DATABASE kali_scraper;"
```

### Migration Management
```bash
# Check current migration
alembic current

# View migration history
alembic history

# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Performance Optimization

### SQLite Optimization
```sql
-- Enable WAL mode for better concurrency
PRAGMA journal_mode=WAL;

-- Set page size for better performance
PRAGMA page_size=4096;

-- Enable memory-mapped I/O
PRAGMA mmap_size=268435456;

-- Set cache size
PRAGMA cache_size=10000;
```

### PostgreSQL Optimization
```sql
-- Analyze tables for query optimization
ANALYZE investigations;
ANALYZE social_media_data;
ANALYZE domain_data;

-- Create indexes for better performance
CREATE INDEX idx_investigations_status ON investigations(status);
CREATE INDEX idx_investigations_created_at ON investigations(created_at);
CREATE INDEX idx_social_media_platform ON social_media_data(platform);
CREATE INDEX idx_domain_data_domain ON domain_data(domain);
```

## Security

### File Permissions
```bash
# Set secure permissions for database files
chmod 600 kali_osint.db
chmod 600 kali_osint.db-shm
chmod 600 kali_osint.db-wal

# For PostgreSQL
chmod 700 /var/lib/postgresql/data
```

### Encryption
```bash
# SQLite encryption (requires sqlcipher)
sqlite3 kali_osint.db "PRAGMA key='your-encryption-key';"

# PostgreSQL encryption
# Enable SSL in postgresql.conf
ssl = on
ssl_cert_file = '/path/to/server.crt'
ssl_key_file = '/path/to/server.key'
```

### Access Control
```sql
-- PostgreSQL user permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO kali_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO kali_user;

-- Revoke unnecessary permissions
REVOKE CREATE ON DATABASE kali_scraper FROM kali_user;
```

## Monitoring

### Database Size Monitoring
```bash
# SQLite size
ls -lh kali_osint.db

# PostgreSQL size
psql kali_scraper -c "SELECT pg_size_pretty(pg_database_size('kali_scraper'));"

# Table sizes
psql kali_scraper -c "
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```

### Performance Monitoring
```sql
-- Slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Table access statistics
SELECT 
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch
FROM pg_stat_user_tables;
```

## Troubleshooting

### Common Issues

1. **Database Locked**
   ```bash
   # Check for active connections
   sqlite3 kali_osint.db "PRAGMA busy_timeout=30000;"
   
   # Kill processes using the database
   lsof kali_osint.db
   ```

2. **Migration Errors**
   ```bash
   # Check migration status
   alembic current
   alembic history
   
   # Reset migrations (development only)
   rm -rf alembic/versions/*
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

3. **Performance Issues**
   ```bash
   # Analyze query performance
   EXPLAIN QUERY PLAN SELECT * FROM investigations WHERE status = 'completed';
   
   # Check for missing indexes
   sqlite3 kali_osint.db ".schema"
   ```

4. **Corruption Issues**
   ```bash
   # Check database integrity
   sqlite3 kali_osint.db "PRAGMA integrity_check;"
   
   # Recover from backup if needed
   cp kali_osint_backup_20231201_120000.db kali_osint.db
   ``` 