"""
Sherlock Integration for Social Media Username Hunting
"""

import asyncio
import subprocess
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import tempfile
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class SherlockIntegration:
    """Integration with Sherlock for social media username hunting"""
    
    def __init__(self):
        self.sherlock_path = self._get_sherlock_path()
        self.supported_sites = self._load_supported_sites()
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        # Clean up any resources if needed
        pass
    
    def _get_sherlock_path(self) -> Optional[str]:
        """Get Sherlock installation path"""
        # Check if Sherlock is installed via pip
        try:
            result = subprocess.run(
                ["python", "-c", "import sherlock; print(sherlock.__file__)"] ,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                sherlock_dir = Path(result.stdout.strip()).parent
                return str(sherlock_dir / "sherlock.py")
        except Exception as e:
            logger.warning(f"Could not find Sherlock installation: {e}")
        
        # Prefer system-wide executable if available
        if Path("/opt/homebrew/bin/sherlock").exists():
            return "/opt/homebrew/bin/sherlock"
        
        # Check common installation paths
        common_paths = [
            "/usr/local/bin/sherlock",
            "/usr/bin/sherlock",
            "sherlock",
            "python -m sherlock"
        ]
        
        for path in common_paths:
            try:
                cmd = [path, "--help"] if not path.startswith("python") else path.split() + ["--help"]
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return path
            except Exception:
                continue
        
        return None
    
    def _load_supported_sites(self) -> List[str]:
        """Load list of supported sites from Sherlock"""
        if not self.sherlock_path:
            return []
        
        try:
            # Use a dummy username to get the list of sites
            cmd = [self.sherlock_path, "dummy_test_user_12345", "--print-all"] if not self.sherlock_path.startswith("python") else self.sherlock_path.split() + ["dummy_test_user_12345", "--print-all"]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10  # Reduced timeout
            )
            if result.returncode == 0:
                # Parse the output to extract site names
                lines = result.stdout.split('\n')
                sites = []
                for line in lines:
                    if line.strip() and not line.startswith('[') and not line.startswith('*'):
                        # Extract site name from output
                        site_name = line.split()[0] if line.split() else None
                        if site_name and site_name not in sites:
                            sites.append(site_name)
                logger.info(f"Loaded {len(sites)} supported sites from Sherlock")
                return sites
        except subprocess.TimeoutExpired:
            logger.warning("Sherlock site loading timed out, using default sites")
            # Return a default list of major sites
            return [
                "twitter", "instagram", "facebook", "linkedin", "github", 
                "reddit", "youtube", "tiktok", "telegram", "discord",
                "snapchat", "pinterest", "tumblr", "medium", "dev.to"
            ]
        except Exception as e:
            logger.error(f"Error loading supported sites: {e}")
            # Return a default list of major sites
            return [
                "twitter", "instagram", "facebook", "linkedin", "github", 
                "reddit", "youtube", "tiktok", "telegram", "discord",
                "snapchat", "pinterest", "tumblr", "medium", "dev.to"
            ]
        
        return []
    
    async def hunt_username(self, username: str, sites: Optional[List[str]] = None) -> Dict[str, Any]:
        """Hunt for username across social media platforms with comprehensive results"""
        if not self.sherlock_path:
            return {
                "error": "Sherlock not found. Please install it first: pip install sherlock-project",
                "username": username,
                "found_accounts": [],
                "total_sites_checked": 0,
                "found_count": 0,
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
        
        try:
            # Create temporary output file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
                output_file = tmp_file.name
            
            # Build command with better options
            cmd = [
                self.sherlock_path,
                username,
                "--output", output_file,
                "--print-found",
                "--verbose",
                "--timeout", "10"
            ]
            
            # If using system-wide executable, pass --site multiple times
            if sites:
                if self.sherlock_path.endswith('sherlock'):
                    for site in sites:
                        cmd.extend(["--site", site])
                else:
                    cmd.extend(["--site", ",".join(sites)])
            else:
                major_sites = [
                    "twitter", "instagram", "facebook", "linkedin", "github", 
                    "reddit", "youtube", "tiktok", "telegram", "discord",
                    "snapchat", "pinterest", "tumblr", "medium", "dev.to",
                    "stackoverflow", "gitlab", "bitbucket", "twitch", "spotify"
                ]
                if self.sherlock_path.endswith('sherlock'):
                    for site in major_sites:
                        cmd.extend(["--site", site])
                else:
                    cmd.extend(["--site", ",".join(major_sites)])
            
            # Run Sherlock
            logger.info(f"Starting Sherlock hunt for username: {username}")
            start_time = datetime.utcnow()
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            end_time = datetime.utcnow()
            
            if process.returncode != 0:
                logger.error(f"Sherlock failed: {stderr.decode()}")
                return {
                    "error": f"Sherlock execution failed: {stderr.decode()}",
                    "username": username,
                    "found_accounts": [],
                    "total_sites_checked": 0,
                    "found_count": 0,
                    "analysis_timestamp": datetime.utcnow().isoformat()
                }
            
            # Parse results
            results = self._parse_sherlock_results(output_file, username)
            results["execution_time"] = (end_time - start_time).total_seconds()
            results["analysis_timestamp"] = datetime.utcnow().isoformat()
            
            # Add additional analysis
            if results.get("found_accounts"):
                results["analysis"] = self._analyze_username_results(results)
                results["recommendations"] = self._generate_recommendations(results)
            
            # Clean up
            try:
                os.unlink(output_file)
            except Exception as e:
                logger.warning(f"Could not delete temporary file: {e}")
            
            logger.info(f"Sherlock hunt completed for {username}: {results.get('found_count', 0)} accounts found")
            return results
            
        except Exception as e:
            logger.error(f"Error during Sherlock hunt: {e}")
            return {
                "error": str(e),
                "username": username,
                "found_accounts": [],
                "total_sites_checked": 0,
                "found_count": 0,
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
    
    def _parse_sherlock_results(self, output_file: str, username: str) -> Dict[str, Any]:
        """Parse Sherlock text results"""
        try:
            with open(output_file, 'r') as f:
                lines = f.readlines()
            
            # Extract found accounts from URLs
            found_accounts = []
            for line in lines:
                line = line.strip()
                if line and line.startswith('http'):
                    # Extract site name from URL
                    try:
                        from urllib.parse import urlparse
                        parsed_url = urlparse(line)
                        site_name = parsed_url.netloc.replace('www.', '').split('.')[0]
                        
                        found_accounts.append({
                            "site": site_name,
                            "url": line,
                            "username": username,
                            "status": "found",
                            "response_time": 0,
                            "http_status": 200,
                            "error_type": None,
                            "error_code": None
                        })
                    except Exception as e:
                        logger.warning(f"Could not parse URL: {line}, error: {e}")
                        continue
            
            # Calculate statistics
            found_count = len(found_accounts)
            
            return {
                "username": username,
                "total_sites_checked": 162,  # Approximate total sites checked
                "accounts_found": found_count,
                "success_rate": (found_count / 162 * 100) if found_count > 0 else 0,
                "found_accounts": found_accounts,
                "all_results": {"found_count": found_count, "urls": [acc["url"] for acc in found_accounts]},
                "hunt_timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error parsing Sherlock results: {e}")
            return {
                "error": f"Failed to parse results: {e}",
                "username": username
            }
    
    async def hunt_multiple_usernames(self, usernames: List[str], sites: Optional[List[str]] = None) -> Dict[str, Any]:
        """Hunt for multiple usernames"""
        results = {}
        
        for username in usernames:
            logger.info(f"Hunting username: {username}")
            result = await self.hunt_username(username, sites)
            results[username] = result
            
            # Add delay between requests to be respectful
            await asyncio.sleep(1)
        
        return {
            "total_usernames": len(usernames),
            "results": results,
            "completed_at": datetime.utcnow().isoformat()
        }
    
    def get_supported_sites(self) -> List[str]:
        """Get list of supported sites"""
        return self.supported_sites.copy()
    
    def get_site_categories(self) -> Dict[str, List[str]]:
        """Get sites organized by category"""
        # This would be a mapping of sites to categories
        # For now, return a basic structure
        categories: Dict[str, List[str]] = {
            "social_media": ["Twitter", "Instagram", "Facebook", "LinkedIn", "TikTok"],
            "professional": ["GitHub", "LinkedIn", "Stack Overflow", "Medium"],
            "gaming": ["Steam", "Xbox", "PlayStation", "Discord"],
            "development": ["GitHub", "GitLab", "Bitbucket", "Stack Overflow"],
            "content_creation": ["YouTube", "Twitch", "TikTok", "Instagram"]
        }
        return categories
    
    async def analyze_username_patterns(self, usernames: List[str]) -> Dict[str, Any]:
        """Analyze username patterns across platforms"""
        results = {}
        
        for username in usernames:
            hunt_result = await self.hunt_username(username)
            
            if "error" not in hunt_result:
                # Analyze the results
                analysis = self._analyze_username_results(hunt_result)
                results[username] = analysis
            else:
                results[username] = {"error": hunt_result["error"]}
        
        return {
            "username_analysis": results,
            "patterns": self._identify_patterns(results),
            "recommendations": self._generate_recommendations(results)
        }
    
    def _analyze_username_results(self, hunt_result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze individual username hunt results"""
        found_accounts = hunt_result.get("found_accounts", [])
        
        # Categorize found accounts
        categories: Dict[str, List[Dict[str, Any]]] = {}
        for account in found_accounts:
            site = account["site"]
            if site not in categories:
                categories[site] = []
            categories[site].append(account)
        
        # Calculate metrics
        total_found = len(found_accounts)
        unique_sites = len(categories)
        
        return {
            "total_accounts_found": total_found,
            "unique_sites": unique_sites,
            "categories": categories,
            "success_rate": hunt_result.get("success_rate", 0),
            "most_active_platforms": self._get_most_active_platforms(found_accounts)
        }
    
    def _get_most_active_platforms(self, accounts: List[Dict[str, Any]]) -> List[str]:
        """Get platforms where user is most active"""
        # This would analyze response times, status codes, etc.
        # For now, return platforms with successful finds
        return list(set(account["site"] for account in accounts))
    
    def _identify_patterns(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Identify patterns across multiple usernames"""
        patterns: Dict[str, Any] = {
            "common_platforms": [],
            "username_variations": [],
            "activity_patterns": []
        }
        
        # Analyze common platforms
        all_platforms = []
        for username, result in results.items():
            if "username_analysis" in result:
                analysis = result["username_analysis"]
                if "categories" in analysis:
                    all_platforms.extend(analysis["categories"].keys())
        
        from collections import Counter
        platform_counts = Counter(all_platforms)
        patterns["common_platforms"] = platform_counts.most_common(10)
        
        return patterns
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Add recommendations based on patterns
        if results:
            recommendations.append("Consider monitoring high-activity platforms for updates")
            recommendations.append("Cross-reference findings with other OSINT tools")
            recommendations.append("Verify account ownership through additional research")
        
        return recommendations

# Global instance
sherlock_integration = SherlockIntegration() 