"""
Advanced GitHub Scraping Service
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any, Union
from app.utils.type_hints import JSON, ValidationResult, PlatformType
from datetime import datetime, timedelta
import json
import re
from urllib.parse import urlparse, parse_qs

from app.models.schemas import (
    RepositoryData,
    UserProfile,
    OrganizationData,
    TechnologyStack,
    ThreatAssessment,
    ThreatLevel
)

logger = logging.getLogger(__name__)

class GitHubScraper:
    """Advanced GitHub scraping and analysis service"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.session = None
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": "Kali-OSINT-Platform/1.0",
                "Accept": "application/vnd.github.v3+json"
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def analyze_repository_async(
        self, 
        repo_url: str, 
        analysis_depth: str = "comprehensive"
    ) -> Dict[str, Any]:
        """Analyze GitHub repository comprehensively"""
        try:
            # Parse repository URL
            repo_info = self._parse_repo_url(repo_url)
            if not repo_info:
                raise ValueError(f"Invalid GitHub repository URL: {repo_url}")
            
            owner, repo_name = repo_info["owner"], repo_info["repo"]
            
            # Basic repository information
            repo_data = await self._get_repository_data(owner, repo_name)
            if not repo_data:
                return {"error": "Repository not found or inaccessible"}
            
            # Enhanced analysis based on depth
            analysis = {
                "repository": repo_data,
                "analysis_depth": analysis_depth,
                "analyzed_at": datetime.utcnow().isoformat()
            }
            
            if analysis_depth in ["deep", "comprehensive"]:
                # Get contributors
                contributors = await self._get_repository_contributors(owner, repo_name)
                analysis["contributors"] = contributors
                
                # Get recent commits
                commits = await self._get_recent_commits(owner, repo_name)
                analysis["recent_commits"] = commits
                
                # Get issues and pull requests
                issues = await self._get_repository_issues(owner, repo_name)
                analysis["issues"] = issues
                
                # Get releases
                releases = await self._get_repository_releases(owner, repo_name)
                analysis["releases"] = releases
            
            if analysis_depth == "comprehensive":
                # Get organization data
                if repo_data.get("organization"):
                    org_data = await self._get_organization_data(repo_data["organization"]["login"])
                    analysis["organization"] = org_data
                
                # Get repository languages
                languages = await self._get_repository_languages(owner, repo_name)
                analysis["languages"] = languages
                
                # Get repository topics
                topics = await self._get_repository_topics(owner, repo_name)
                analysis["topics"] = topics
                
                # Get repository traffic (if available)
                traffic = await self._get_repository_traffic(owner, repo_name)
                analysis["traffic"] = traffic
            
            # Threat assessment
            threat_assessment = await self._assess_repository_threat(repo_data, analysis)
            analysis["threat_assessment"] = threat_assessment
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing repository {repo_url}: {e}")
            return {"error": str(e)}
    
    async def analyze_user_profile(self, username: str) -> Dict[str, Any]:
        """Analyze GitHub user profile"""
        try:
            # Get user data
            user_data = await self._get_user_data(username)
            if not user_data:
                return {"error": "User not found"}
            
            # Get user repositories
            repos = await self._get_user_repositories(username)
            
            # Get user organizations
            orgs = await self._get_user_organizations(username)
            
            # Get user activity
            activity = await self._get_user_activity(username)
            
            # Threat assessment
            threat_assessment = await self._assess_user_threat(user_data, repos)
            
            return {
                "user": user_data,
                "repositories": repos,
                "organizations": orgs,
                "activity": activity,
                "threat_assessment": threat_assessment.dict() if hasattr(threat_assessment, 'dict') else threat_assessment,
                "analyzed_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing user {username}: {e}")
            return {"error": str(e)}
    
    async def analyze_organization(self, org_name: str) -> Dict[str, Any]:
        """Analyze GitHub organization"""
        try:
            # Get organization data
            org_data = await self._get_organization_data(org_name)
            if not org_data:
                return {"error": "Organization not found"}
            
            # Get organization repositories
            repos = await self._get_organization_repositories(org_name)
            
            # Get organization members
            members = await self._get_organization_members(org_name)
            
            # Get organization activity
            activity = await self._get_organization_activity(org_name)
            
            # Threat assessment
            threat_assessment = await self._assess_organization_threat(org_data, repos)
            
            return {
                "organization": org_data,
                "repositories": repos,
                "members": members,
                "activity": activity,
                "threat_assessment": threat_assessment,
                "analyzed_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing organization {org_name}: {e}")
            return {"error": str(e)}
    
    async def search_repositories(
        self, 
        query: str, 
        language: Optional[str] = None,
        sort: str = "stars",
        order: str = "desc",
        per_page: int = 30,
        *args,
        **kwargs
    ) -> Dict[str, Any]:
        """Search GitHub repositories"""
        try:
            search_params = {
                "q": query,
                "sort": sort,
                "order": order,
                "per_page": min(per_page, 100)
            }
            
            if language:
                search_params["q"] += f" language:{language}"
            
            url = f"{self.base_url}/search/repositories"
            async with self.session.get(url, params=search_params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "total_count": data.get("total_count", 0),
                        "repositories": data.get("items", []),
                        "search_query": query,
                        "search_params": search_params
                    }
                else:
                    return {"error": f"Search failed: {response.status}"}
                    
        except Exception as e:
            logger.error(f"Error searching repositories: {e}")
            return {"error": str(e)}
    
    async def _get_repository_data(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Get basic repository data"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "id": data["id"],
                        "name": data["name"],
                        "full_name": data["full_name"],
                        "description": data["description"],
                        "language": data["language"],
                        "stars": data["stargazers_count"],
                        "forks": data["forks_count"],
                        "watchers": data["watchers_count"],
                        "open_issues": data["open_issues_count"],
                        "created_at": data["created_at"],
                        "updated_at": data["updated_at"],
                        "pushed_at": data["pushed_at"],
                        "size": data["size"],
                        "license": data.get("license"),
                        "topics": data.get("topics", []),
                        "default_branch": data["default_branch"],
                        "private": data["private"],
                        "archived": data["archived"],
                        "disabled": data["disabled"],
                        "organization": data.get("organization"),
                        "owner": data["owner"],
                        "homepage": data.get("homepage"),
                        "html_url": data["html_url"],
                        "clone_url": data["clone_url"],
                        "ssh_url": data["ssh_url"]
                    }
                return None
                
        except Exception as e:
            logger.error(f"Error getting repository data: {e}")
            return None
    
    async def _get_repository_contributors(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """Get repository contributors"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/contributors"
            async with self.session.get(url) as response:
                if response.status == 200:
                    contributors = await response.json()
                    return [
                        {
                            "login": c["login"],
                            "id": c["id"],
                            "contributions": c["contributions"],
                            "avatar_url": c["avatar_url"],
                            "html_url": c["html_url"]
                        }
                        for c in contributors[:50]  # Limit to top 50 contributors
                    ]
                return []
                
        except Exception as e:
            logger.error(f"Error getting contributors: {e}")
            return []
    
    async def _get_recent_commits(self, owner: str, repo: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent commits"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/commits"
            params = {"per_page": limit}
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    commits = await response.json()
                    return [
                        {
                            "sha": c["sha"],
                            "message": c["commit"]["message"],
                            "author": c["commit"]["author"],
                            "committer": c["commit"]["committer"],
                            "html_url": c["html_url"]
                        }
                        for c in commits
                    ]
                return []
                
        except Exception as e:
            logger.error(f"Error getting commits: {e}")
            return []
    
    async def _get_repository_issues(self, owner: str, repo: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get repository issues"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/issues"
            params = {"per_page": limit, "state": "all"}
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    issues = await response.json()
                    return [
                        {
                            "id": i["id"],
                            "number": i["number"],
                            "title": i["title"],
                            "state": i["state"],
                            "user": i["user"],
                            "created_at": i["created_at"],
                            "updated_at": i["updated_at"],
                            "labels": i["labels"]
                        }
                        for i in issues
                    ]
                return []
                
        except Exception as e:
            logger.error(f"Error getting issues: {e}")
            return []
    
    async def _get_repository_releases(self, owner: str, repo: str) -> List[Dict[str, Any]]:
        """Get repository releases"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/releases"
            async with self.session.get(url) as response:
                if response.status == 200:
                    releases = await response.json()
                    return [
                        {
                            "id": r["id"],
                            "tag_name": r["tag_name"],
                            "name": r["name"],
                            "body": r["body"],
                            "created_at": r["created_at"],
                            "published_at": r["published_at"],
                            "author": r["author"]
                        }
                        for r in releases[:10]  # Limit to 10 recent releases
                    ]
                return []
                
        except Exception as e:
            logger.error(f"Error getting releases: {e}")
            return []
    
    async def _get_organization_data(self, org_name: str) -> Optional[Dict[str, Any]]:
        """Get organization data"""
        try:
            url = f"{self.base_url}/orgs/{org_name}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "id": data["id"],
                        "login": data["login"],
                        "name": data["name"],
                        "description": data["description"],
                        "avatar_url": data["avatar_url"],
                        "html_url": data["html_url"],
                        "blog": data.get("blog"),
                        "location": data.get("location"),
                        "email": data.get("email"),
                        "public_repos": data["public_repos"],
                        "public_gists": data["public_gists"],
                        "followers": data["followers"],
                        "following": data["following"],
                        "created_at": data["created_at"],
                        "updated_at": data["updated_at"]
                    }
                return None
                
        except Exception as e:
            logger.error(f"Error getting organization data: {e}")
            return None
    
    async def _get_repository_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """Get repository languages"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/languages"
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                return {}
                
        except Exception as e:
            logger.error(f"Error getting languages: {e}")
            return {}
    
    async def _get_repository_topics(self, owner: str, repo: str) -> List[str]:
        """Get repository topics"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/topics"
            headers = {"Accept": "application/vnd.github.mercy-preview+json"}
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("names", [])
                return []
                
        except Exception as e:
            logger.error(f"Error getting topics: {e}")
            return []
    
    async def _get_repository_traffic(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository traffic data (if available)"""
        try:
            # Note: This requires special permissions and may not be available
            url = f"{self.base_url}/repos/{owner}/{repo}/traffic/views"
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                return {"error": "Traffic data not available"}
                
        except Exception as e:
            logger.error(f"Error getting traffic data: {e}")
            return {"error": "Traffic data not available"}
    
    async def _get_user_data(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user data"""
        try:
            url = f"{self.base_url}/users/{username}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and isinstance(data, dict):
                        return {
                            "id": data.get("id"),
                            "login": data.get("login"),
                            "name": data.get("name"),
                            "email": data.get("email"),
                            "bio": data.get("bio"),
                            "company": data.get("company"),
                            "blog": data.get("blog"),
                            "location": data.get("location"),
                            "hireable": data.get("hireable"),
                            "public_repos": data.get("public_repos", 0),
                            "public_gists": data.get("public_gists", 0),
                            "followers": data.get("followers", 0),
                            "following": data.get("following", 0),
                            "created_at": data.get("created_at"),
                            "updated_at": data.get("updated_at"),
                            "avatar_url": data.get("avatar_url"),
                            "html_url": data.get("html_url")
                        }
                return None
                
        except Exception as e:
            logger.error(f"Error getting user data: {e}")
            return None
    
    async def _get_user_repositories(self, username: str) -> List[Dict[str, Any]]:
        """Get user repositories"""
        try:
            url = f"{self.base_url}/users/{username}/repos"
            params = {"per_page": 100, "sort": "updated"}
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    repos = await response.json()
                    return [
                        {
                            "id": r["id"],
                            "name": r["name"],
                            "full_name": r["full_name"],
                            "description": r["description"],
                            "language": r["language"],
                            "stars": r["stargazers_count"],
                            "forks": r["forks_count"],
                            "private": r["private"],
                            "created_at": r["created_at"],
                            "updated_at": r["updated_at"]
                        }
                        for r in repos
                    ]
                return []
                
        except Exception as e:
            logger.error(f"Error getting user repositories: {e}")
            return []
    
    async def _get_user_organizations(self, username: str) -> List[Dict[str, Any]]:
        """Get user organizations"""
        try:
            url = f"{self.base_url}/users/{username}/orgs"
            async with self.session.get(url) as response:
                if response.status == 200:
                    orgs = await response.json()
                    return [
                        {
                            "id": o["id"],
                            "login": o["login"],
                            "name": o["name"],
                            "avatar_url": o["avatar_url"],
                            "html_url": o["html_url"]
                        }
                        for o in orgs
                    ]
                return []
                
        except Exception as e:
            logger.error(f"Error getting user organizations: {e}")
            return []
    
    async def _get_user_activity(self, username: str) -> Dict[str, Any]:
        """Get user activity data"""
        try:
            # Get recent events
            url = f"{self.base_url}/users/{username}/events"
            params = {"per_page": 30}
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    events = await response.json()
                    return {
                        "recent_events": events[:10],
                        "event_count": len(events)
                    }
                return {"recent_events": [], "event_count": 0}
                
        except Exception as e:
            logger.error(f"Error getting user activity: {e}")
            return {"recent_events": [], "event_count": 0}
    
    async def _get_organization_repositories(self, org_name: str) -> List[Dict[str, Any]]:
        """Get organization repositories"""
        try:
            url = f"{self.base_url}/orgs/{org_name}/repos"
            params = {"per_page": 100, "sort": "updated"}
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    repos = await response.json()
                    return [
                        {
                            "id": r["id"],
                            "name": r["name"],
                            "full_name": r["full_name"],
                            "description": r["description"],
                            "language": r["language"],
                            "stars": r["stargazers_count"],
                            "forks": r["forks_count"],
                            "private": r["private"],
                            "created_at": r["created_at"],
                            "updated_at": r["updated_at"]
                        }
                        for r in repos
                    ]
                return []
                
        except Exception as e:
            logger.error(f"Error getting organization repositories: {e}")
            return []
    
    async def _get_organization_members(self, org_name: str) -> List[Dict[str, Any]]:
        """Get organization members"""
        try:
            url = f"{self.base_url}/orgs/{org_name}/members"
            async with self.session.get(url) as response:
                if response.status == 200:
                    members = await response.json()
                    return [
                        {
                            "id": m["id"],
                            "login": m["login"],
                            "avatar_url": m["avatar_url"],
                            "html_url": m["html_url"]
                        }
                        for m in members
                    ]
                return []
                
        except Exception as e:
            logger.error(f"Error getting organization members: {e}")
            return []
    
    async def _get_organization_activity(self, org_name: str) -> Dict[str, Any]:
        """Get organization activity data"""
        try:
            # Get recent events
            url = f"{self.base_url}/orgs/{org_name}/events"
            params = {"per_page": 30}
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    events = await response.json()
                    return {
                        "recent_events": events[:10],
                        "event_count": len(events)
                    }
                return {"recent_events": [], "event_count": 0}
                
        except Exception as e:
            logger.error(f"Error getting organization activity: {e}")
            return {"recent_events": [], "event_count": 0}
    
    async def _assess_repository_threat(
        self, 
        repo_data: Dict[str, Any], 
        analysis: Dict[str, Any]
    ) -> ThreatAssessment:
        """Assess repository threat level"""
        try:
            threat_score = 0.0
            indicators = []
            risk_factors = []
            recommendations = []
            
            # Check for suspicious keywords in description
            description = repo_data.get("description", "").lower()
            suspicious_keywords = [
                "malware", "virus", "trojan", "backdoor", "exploit",
                "hack", "crack", "bypass", "inject", "overflow",
                "ddos", "botnet", "keylogger", "spyware", "ransomware"
            ]
            
            for keyword in suspicious_keywords:
                if keyword in description:
                    threat_score += 0.2
                    indicators.append(f"Suspicious keyword detected: {keyword}")
            
            # Check for recently created repositories
            created_at = datetime.fromisoformat(repo_data["created_at"].replace("Z", "+00:00"))
            days_old = (datetime.utcnow() - created_at.replace(tzinfo=None)).days
            
            if days_old < 30:
                threat_score += 0.1
                indicators.append("Recently created repository")
                risk_factors.append("New repository with limited history")
            
            # Check for high star count with low activity
            stars = repo_data.get("stars", 0)
            forks = repo_data.get("forks", 0)
            open_issues = repo_data.get("open_issues", 0)
            
            if stars > 100 and forks < 10:
                threat_score += 0.15
                indicators.append("High star count with low fork activity")
                risk_factors.append("Potential artificial popularity")
            
            # Check for suspicious topics
            topics = repo_data.get("topics", [])
            suspicious_topics = ["hack", "crack", "exploit", "malware", "virus"]
            
            for topic in topics:
                if any(susp in topic.lower() for susp in suspicious_topics):
                    threat_score += 0.25
                    indicators.append(f"Suspicious topic: {topic}")
            
            # Check for private repositories with high activity
            if repo_data.get("private", False) and stars > 50:
                threat_score += 0.1
                indicators.append("Private repository with high star count")
            
            # Determine threat level
            if threat_score >= 0.7:
                threat_level = ThreatLevel.HIGH
            elif threat_score >= 0.4:
                threat_level = ThreatLevel.MEDIUM
            else:
                threat_level = ThreatLevel.LOW
            
            # Generate recommendations
            if threat_score > 0.3:
                recommendations.append("Enhanced monitoring recommended")
                recommendations.append("Review repository content")
                recommendations.append("Check contributor backgrounds")
            
            if threat_score > 0.6:
                recommendations.append("Consider security review")
                recommendations.append("Monitor for suspicious activity")
            
            return ThreatAssessment(
                target=repo_data["full_name"],
                threat_level=threat_level,
                threat_score=min(threat_score, 1.0),
                indicators=indicators,
                risk_factors=risk_factors,
                recommendations=recommendations,
                confidence=0.8
            )
            
        except Exception as e:
            logger.error(f"Error assessing repository threat: {e}")
            return ThreatAssessment(
                target=repo_data.get("full_name", "unknown"),
                threat_level=ThreatLevel.LOW,
                threat_score=0.0,
                indicators=["Error in threat assessment"],
                risk_factors=[],
                recommendations=["Manual review recommended"],
                confidence=0.0
            )
    
    async def _assess_user_threat(
        self, 
        user_data: Dict[str, Any], 
        repos: List[Dict[str, Any]]
    ) -> ThreatAssessment:
        """Assess user threat level"""
        try:
            threat_score = 0.0
            indicators = []
            risk_factors = []
            recommendations = []
            
            # Check for suspicious bio content (handle None values)
            bio = user_data.get("bio", "")
            if bio is not None:
                bio = bio.lower()
                suspicious_bio_keywords = [
                    "hacker", "cracker", "malware", "virus", "exploit",
                    "ddos", "botnet", "keylogger", "spyware"
                ]
                
                for keyword in suspicious_bio_keywords:
                    if keyword in bio:
                        threat_score += 0.3
                        indicators.append(f"Suspicious bio keyword: {keyword}")
            
            # Check for recently created account (handle None values)
            created_at_str = user_data.get("created_at")
            if created_at_str:
                try:
                    created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                    days_old = (datetime.utcnow() - created_at.replace(tzinfo=None)).days
                    
                    if days_old < 90:
                        threat_score += 0.1
                        indicators.append("Recently created account")
                        risk_factors.append("New account with limited history")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Could not parse created_at date: {e}")
            
            # Check for suspicious repositories (handle None values)
            suspicious_repo_count = 0
            for repo in repos:
                repo_name = repo.get("name", "")
                repo_desc = repo.get("description", "")
                
                # Convert to lowercase only if not None
                if repo_name is not None:
                    repo_name = repo_name.lower()
                else:
                    repo_name = ""
                    
                if repo_desc is not None:
                    repo_desc = repo_desc.lower()
                else:
                    repo_desc = ""
                
                suspicious_repo_keywords = [
                    "malware", "virus", "trojan", "backdoor", "exploit",
                    "hack", "crack", "bypass", "inject", "overflow"
                ]
                
                for keyword in suspicious_repo_keywords:
                    if keyword in repo_name or keyword in repo_desc:
                        suspicious_repo_count += 1
                        break
            
            if suspicious_repo_count > 0:
                threat_score += 0.2 * suspicious_repo_count
                indicators.append(f"{suspicious_repo_count} suspicious repositories detected")
            
            # Check for high follower count with low activity
            followers = user_data.get("followers", 0)
            following = user_data.get("following", 0)
            public_repos = user_data.get("public_repos", 0)
            
            if followers > 100 and public_repos < 5:
                threat_score += 0.15
                indicators.append("High follower count with low repository activity")
                risk_factors.append("Potential artificial popularity")
            
            # Determine threat level
            if threat_score >= 0.7:
                threat_level = ThreatLevel.HIGH
            elif threat_score >= 0.4:
                threat_level = ThreatLevel.MEDIUM
            else:
                threat_level = ThreatLevel.LOW
            
            # Generate recommendations
            if threat_score > 0.3:
                recommendations.append("Enhanced monitoring recommended")
                recommendations.append("Review user repositories")
                recommendations.append("Check user activity patterns")
            
            if threat_score > 0.6:
                recommendations.append("Consider security review")
                recommendations.append("Monitor for suspicious activity")
            
            return ThreatAssessment(
                target=user_data.get("login", "unknown"),
                threat_level=threat_level,
                threat_score=min(threat_score, 1.0),
                indicators=indicators,
                risk_factors=risk_factors,
                recommendations=recommendations,
                confidence=0.8
            )
            
        except Exception as e:
            logger.error(f"Error assessing user threat: {e}")
            return ThreatAssessment(
                target=user_data.get("login", "unknown"),
                threat_level=ThreatLevel.LOW,
                threat_score=0.0,
                indicators=["Error in threat assessment"],
                risk_factors=[],
                recommendations=["Manual review recommended"],
                confidence=0.0
            )
    
    async def _assess_organization_threat(
        self, 
        org_data: Dict[str, Any], 
        repos: List[Dict[str, Any]]
    ) -> ThreatAssessment:
        """Assess organization threat level"""
        try:
            threat_score = 0.0
            indicators = []
            risk_factors = []
            recommendations = []
            
            # Check for suspicious organization description (handle None values)
            description = org_data.get("description", "")
            if description is not None:
                description = description.lower()
                suspicious_desc_keywords = [
                    "hack", "crack", "exploit", "malware", "virus",
                    "ddos", "botnet", "keylogger", "spyware"
                ]
                
                for keyword in suspicious_desc_keywords:
                    if keyword in description:
                        threat_score += 0.3
                        indicators.append(f"Suspicious organization description: {keyword}")
            
            # Check for recently created organization (handle None values)
            created_at_str = org_data.get("created_at")
            if created_at_str:
                try:
                    created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                    days_old = (datetime.utcnow() - created_at.replace(tzinfo=None)).days
                    
                    if days_old < 180:
                        threat_score += 0.1
                        indicators.append("Recently created organization")
                        risk_factors.append("New organization with limited history")
                except (ValueError, TypeError) as e:
                    logger.warning(f"Could not parse created_at date: {e}")
            
            # Check for suspicious repositories (handle None values)
            suspicious_repo_count = 0
            for repo in repos:
                repo_name = repo.get("name", "")
                repo_desc = repo.get("description", "")
                
                # Convert to lowercase only if not None
                if repo_name is not None:
                    repo_name = repo_name.lower()
                else:
                    repo_name = ""
                    
                if repo_desc is not None:
                    repo_desc = repo_desc.lower()
                else:
                    repo_desc = ""
                
                suspicious_repo_keywords = [
                    "malware", "virus", "trojan", "backdoor", "exploit",
                    "hack", "crack", "bypass", "inject", "overflow"
                ]
                
                for keyword in suspicious_repo_keywords:
                    if keyword in repo_name or keyword in repo_desc:
                        suspicious_repo_count += 1
                        break
            
            if suspicious_repo_count > 0:
                threat_score += 0.15 * suspicious_repo_count
                indicators.append(f"{suspicious_repo_count} suspicious repositories in organization")
            
            # Check for high member count with low activity
            public_repos = org_data.get("public_repos", 0)
            if public_repos < 10:
                threat_score += 0.1
                indicators.append("Low repository activity for organization")
                risk_factors.append("Limited public activity")
            
            # Determine threat level
            if threat_score >= 0.7:
                threat_level = ThreatLevel.HIGH
            elif threat_score >= 0.4:
                threat_level = ThreatLevel.MEDIUM
            else:
                threat_level = ThreatLevel.LOW
            
            # Generate recommendations
            if threat_score > 0.3:
                recommendations.append("Enhanced monitoring recommended")
                recommendations.append("Review organization repositories")
                recommendations.append("Check member backgrounds")
            
            if threat_score > 0.6:
                recommendations.append("Consider security review")
                recommendations.append("Monitor for suspicious activity")
            
            return ThreatAssessment(
                target=org_data.get("login", "unknown"),
                threat_level=threat_level,
                threat_score=min(threat_score, 1.0),
                indicators=indicators,
                risk_factors=risk_factors,
                recommendations=recommendations,
                confidence=0.8
            )
            
        except Exception as e:
            logger.error(f"Error assessing organization threat: {e}")
            return ThreatAssessment(
                target=org_data.get("login", "unknown"),
                threat_level=ThreatLevel.LOW,
                threat_score=0.0,
                indicators=["Error in threat assessment"],
                risk_factors=[],
                recommendations=["Manual review recommended"],
                confidence=0.0
            )
    
    def _parse_repo_url(self, repo_url: str) -> Optional[Dict[str, str]]:
        """Parse GitHub repository URL"""
        try:
            # Handle various GitHub URL formats
            if "github.com" in repo_url:
                # Extract owner and repo from URL
                path = urlparse(repo_url).path.strip("/")
                parts = path.split("/")
                
                if len(parts) >= 2:
                    return {
                        "owner": parts[0],
                        "repo": parts[1].split(".")[0]  # Remove .git if present
                    }
            
            # Handle direct owner/repo format
            if "/" in repo_url and "github.com" not in repo_url:
                parts = repo_url.split("/")
                if len(parts) >= 2:
                    return {
                        "owner": parts[0],
                        "repo": parts[1]
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing repository URL: {e}")
            return None 

    async def scrape_user(self, username: str, *args, **kwargs) -> dict:
        """Scrape GitHub user profile"""
        return await self.analyze_user_profile(username)
    
    async def scrape_repository(self, repo_url: str, *args, **kwargs) -> dict:
        """Scrape GitHub repository"""
        # Ensure session is initialized
        if not self.session:
            async with self:
                return await self.analyze_repository_async(repo_url)
        return await self.analyze_repository_async(repo_url)
    
    async def scrape_user_profile(self, username: str, *args, **kwargs) -> dict:
        """Scrape GitHub user profile (alias for scrape_user)"""
        # Ensure session is initialized
        if not self.session:
            async with self:
                return await self.analyze_user_profile(username)
        return await self.analyze_user_profile(username) 