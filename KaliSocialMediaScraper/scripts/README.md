# Scripts Directory

This directory contains utility scripts for the Kali OSINT Investigation Platform.

## Scripts

- `fetch_and_load_proxies.py` - Proxy fetching and loading utility

## Usage

### Proxy Management
```bash
# Fetch and load proxies
python scripts/fetch_and_load_proxies.py

# Run with specific options
python scripts/fetch_and_load_proxies.py --source free-proxy-list --limit 100
```

## Script Descriptions

### fetch_and_load_proxies.py
- Fetches proxy lists from various sources
- Tests proxy connectivity and performance
- Saves working proxies to configuration
- Supports multiple proxy protocols (HTTP, HTTPS, SOCKS)
- Includes proxy rotation and failover logic

## Adding New Scripts

When adding new utility scripts:
1. Place them in this directory
2. Add a description to this README
3. Include proper error handling
4. Add command-line argument support
5. Include logging for debugging 