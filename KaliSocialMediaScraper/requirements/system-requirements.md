# System Requirements

This document lists all system-level dependencies required for the Kali OSINT Investigation Platform.

## Operating System Support

- **macOS**: 10.15+ (Catalina and later)
- **Ubuntu**: 20.04+ (LTS versions recommended)
- **Debian**: 11+ (Bullseye and later)
- **Windows**: 10+ (with WSL2 recommended)

## System Dependencies

### Python Environment
- **Python**: 3.11+ (recommended: 3.11.13)
- **pip**: Latest version
- **virtualenv**: For isolated environments

### Database Systems
- **PostgreSQL**: 12+ (for production)
- **SQLite**: 3.35+ (for development)
- **Redis**: 6+ (for Celery task queue)

### System Libraries

#### macOS (via Homebrew)
```bash
# Core system dependencies
brew install python@3.11
brew install redis
brew install postgresql

# Performance optimization
brew install openblas
brew install lapack
brew install gcc

# Development tools
brew install git
brew install curl
brew install wget
```

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Core system dependencies
sudo apt install python3.11 python3.11-venv python3.11-dev
sudo apt install redis-server postgresql postgresql-contrib

# Performance optimization
sudo apt install libopenblas-dev liblapack-dev
sudo apt install gcc g++ make

# Development tools
sudo apt install git curl wget
sudo apt install build-essential
```

#### Windows (via Chocolatey)
```bash
# Core dependencies
choco install python redis postgresql

# Performance optimization
choco install openblas

# Development tools
choco install git curl wget
```

## Performance Optimization Libraries

### OpenBLAS (Open Basic Linear Algebra Subprograms)
OpenBLAS is required for optimal performance of numpy, scipy, and scikit-learn operations.

#### Installation Verification
```bash
# Check if OpenBLAS is properly linked
python -c "import numpy; print(numpy.__config__.show())"

# Verify BLAS implementation
python -c "import numpy as np; print(np.__config__.get_info('blas'))"
```

#### Environment Variables
```bash
# macOS
export OPENBLAS="$(brew --prefix openblas)"
export CFLAGS="-falign-functions=8 ${CFLAGS}"

# Linux
export OPENBLAS_NUM_THREADS=4
export GOTO_NUM_THREADS=4
export OMP_NUM_THREADS=4
```

### LAPACK (Linear Algebra Package)
LAPACK provides routines for solving systems of simultaneous linear equations, least-squares solutions of linear systems of equations, eigenvalue problems, and singular value problems.

## Network Dependencies

### Internet Connectivity
- **HTTP/HTTPS**: For web scraping and API access
- **DNS**: For domain resolution
- **SOCKS/HTTP Proxies**: For proxy rotation (optional)

### Port Requirements
- **8000**: FastAPI backend (configurable)
- **5173**: Vite development server (configurable)
- **6379**: Redis (default)
- **5432**: PostgreSQL (default)

## Hardware Requirements

### Minimum Requirements
- **CPU**: 2 cores, 2.0 GHz
- **RAM**: 4 GB
- **Storage**: 10 GB free space
- **Network**: Broadband internet connection

### Recommended Requirements
- **CPU**: 4+ cores, 3.0 GHz
- **RAM**: 8+ GB
- **Storage**: 50+ GB free space (SSD recommended)
- **Network**: High-speed internet connection

### Production Requirements
- **CPU**: 8+ cores, 3.5 GHz
- **RAM**: 16+ GB
- **Storage**: 100+ GB SSD
- **Network**: Gigabit connection with low latency

## Browser Dependencies

### Playwright Browsers
The platform uses Playwright for web scraping, which requires browser binaries.

```bash
# Install browser binaries
playwright install

# Install specific browsers
playwright install chromium
playwright install firefox
playwright install webkit
```

### Browser Requirements
- **Chromium**: Latest stable version
- **Firefox**: Latest stable version
- **WebKit**: Latest stable version (macOS/Linux only)

## Security Dependencies

### SSL/TLS Libraries
- **OpenSSL**: 1.1.1+ (for HTTPS connections)
- **Certificates**: CA certificates for secure connections

### System Security
- **Firewall**: Configure to allow required ports
- **SELinux/AppArmor**: Configure for application permissions (Linux)

## Monitoring Dependencies

### System Monitoring
- **htop/top**: Process monitoring
- **iotop**: I/O monitoring
- **nethogs**: Network monitoring

### Log Management
- **logrotate**: Log rotation (Linux)
- **rsyslog**: System logging (Linux)

## Development Dependencies

### Code Quality Tools
- **Git**: Version control
- **Docker**: Containerization (optional)
- **Make**: Build automation (optional)

### IDE/Editor Support
- **VS Code**: Recommended with Python extension
- **PyCharm**: Professional Python IDE
- **Vim/Emacs**: Text editors with Python support

## Troubleshooting

### Common Installation Issues

1. **OpenBLAS Not Found**
   ```bash
   # macOS
   brew install openblas
   export OPENBLAS="$(brew --prefix openblas)"
   
   # Ubuntu
   sudo apt install libopenblas-dev
   ```

2. **PostgreSQL Connection Issues**
   ```bash
   # Check service status
   sudo systemctl status postgresql
   
   # Start service
   sudo systemctl start postgresql
   ```

3. **Redis Connection Issues**
   ```bash
   # Check service status
   sudo systemctl status redis
   
   # Start service
   sudo systemctl start redis
   ```

4. **Playwright Browser Issues**
   ```bash
   # Reinstall browsers
   playwright install --force
   
   # Check browser status
   playwright --version
   ```

### Performance Optimization

1. **CPU Optimization**
   ```bash
   # Set thread limits
   export OPENBLAS_NUM_THREADS=$(nproc)
   export OMP_NUM_THREADS=$(nproc)
   ```

2. **Memory Optimization**
   ```bash
   # Monitor memory usage
   free -h
   
   # Check swap usage
   swapon --show
   ```

3. **Disk I/O Optimization**
   ```bash
   # Use SSD for database
   # Monitor I/O performance
   iostat -x 1
   ```

## Version Compatibility Matrix

| Component | Minimum Version | Recommended Version | Tested Version |
|-----------|----------------|-------------------|----------------|
| Python | 3.11.0 | 3.11.13 | 3.11.13 |
| PostgreSQL | 12.0 | 15.0 | 15.0 |
| Redis | 6.0 | 7.0 | 7.0 |
| OpenBLAS | 0.3.0 | 0.3.23 | 0.3.23 |
| Node.js | 18.0 | 20.0 | 20.0 |
| Git | 2.30 | 2.40 | 2.40 |

## Installation Scripts

### Automated Installation (Ubuntu/Debian)
```bash
#!/bin/bash
# install-system-deps.sh

set -e

echo "Installing system dependencies..."

# Update package list
sudo apt update

# Install core dependencies
sudo apt install -y python3.11 python3.11-venv python3.11-dev
sudo apt install -y redis-server postgresql postgresql-contrib
sudo apt install -y libopenblas-dev liblapack-dev
sudo apt install -y gcc g++ make git curl wget

# Start services
sudo systemctl start redis
sudo systemctl enable redis
sudo systemctl start postgresql
sudo systemctl enable postgresql

echo "System dependencies installed successfully!"
```

### Automated Installation (macOS)
```bash
#!/bin/bash
# install-system-deps.sh

set -e

echo "Installing system dependencies..."

# Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install core dependencies
brew install python@3.11
brew install redis
brew install postgresql
brew install openblas
brew install git

# Start services
brew services start redis
brew services start postgresql

echo "System dependencies installed successfully!"
``` 