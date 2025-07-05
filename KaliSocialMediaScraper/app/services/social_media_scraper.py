"""
Advanced Social Media Scraping Service
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import json
import re
from urllib.parse import urlparse, parse_qs
import time
import random

from app.models.schemas import (
    SocialMediaProfile,
    SocialMediaPost,
    PlatformType,
    ThreatAssessment,
    ThreatLevel
)

logger = logging.getLogger(__name__)

class SocialMediaScraper:
    """Advanced social media scraping and analysis service"""
    
    def __init__(self):
        self.session = None
        self.rate_limits = {
            PlatformType.TWITTER: {"requests_per_minute": 300, "last_request": 0},
            PlatformType.INSTAGRAM: {"requests_per_minute": 200, "last_request": 0},
            PlatformType.REDDIT: {"requests_per_minute": 600, "last_request": 0},
            PlatformType.GITHUB: {"requests_per_minute": 5000, "last_request": 0},
            PlatformType.LINKEDIN: {"requests_per_minute": 100, "last_request": 0},
            PlatformType.FACEBOOK: {"requests_per_minute": 200, "last_request": 0},
            PlatformType.YOUTUBE: {"requests_per_minute": 10000, "last_request": 0},
            PlatformType.TIKTOK: {"requests_per_minute": 100, "last_request": 0},
            PlatformType.TELEGRAM: {"requests_per_minute": 30, "last_request": 0},
            PlatformType.DISCORD: {"requests_per_minute": 50, "last_request": 0}
        }
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers={
                "User-Agent": "Kali-OSINT-Platform/1.0",
                "Accept": "application/json, text/html, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def scrape_platform(
        self,
        platform: PlatformType,
        target: str,
        include_metadata: bool = True,
        include_media: bool = False,
        max_posts: int = 100
    ) -> Dict[str, Any]:
        """Scrape social media data from specified platform"""
        try:
            # Rate limiting
            await self._respect_rate_limit(platform)
            
            # Platform-specific scraping
            if platform == PlatformType.TWITTER:
                return await self._scrape_twitter(target, include_metadata, include_media, max_posts)
            elif platform == PlatformType.INSTAGRAM:
                return await self._scrape_instagram(target, include_metadata, include_media, max_posts)
            elif platform == PlatformType.REDDIT:
                return await self._scrape_reddit(target, include_metadata, max_posts)
            elif platform == PlatformType.GITHUB:
                return await self._scrape_github(target, include_metadata, max_posts)
            elif platform == PlatformType.LINKEDIN:
                return await self._scrape_linkedin(target, include_metadata, max_posts)
            elif platform == PlatformType.FACEBOOK:
                return await self._scrape_facebook(target, include_metadata, max_posts)
            elif platform == PlatformType.YOUTUBE:
                return await self._scrape_youtube(target, include_metadata, max_posts)
            elif platform == PlatformType.TIKTOK:
                return await self._scrape_tiktok(target, include_metadata, max_posts)
            elif platform == PlatformType.TELEGRAM:
                return await self._scrape_telegram(target, include_metadata, max_posts)
            elif platform == PlatformType.DISCORD:
                return await self._scrape_discord(target, include_metadata, max_posts)
            else:
                return {"error": f"Unsupported platform: {platform}"}
                
        except Exception as e:
            logger.error(f"Error scraping {platform} for {target}: {e}")
            return {"error": str(e)}
    
    async def analyze_profile(
        self,
        platform: PlatformType,
        username: str
    ) -> Dict[str, Any]:
        """Analyze social media profile comprehensively"""
        try:
            # Get profile data
            profile_data = await self._get_profile_data(platform, username)
            if not profile_data:
                return {"error": "Profile not found or inaccessible"}
            
            # Get recent posts
            posts = await self._get_recent_posts(platform, username)
            
            # Get followers/following data
            network_data = await self._get_network_data(platform, username)
            
            # Threat assessment
            threat_assessment = await self._assess_profile_threat(platform, profile_data, posts)
            
            # Sentiment analysis
            sentiment_data = await self._analyze_sentiment(posts)
            
            return {
                "platform": platform,
                "username": username,
                "profile": profile_data,
                "posts": posts,
                "network": network_data,
                "threat_assessment": threat_assessment,
                "sentiment_analysis": sentiment_data,
                "analyzed_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing profile {username} on {platform}: {e}")
            return {"error": str(e)}
    
    async def search_content(
        self,
        platform: PlatformType,
        query: str,
        max_results: int = 50
    ) -> Dict[str, Any]:
        """Search for content on social media platform"""
        try:
            # Rate limiting
            await self._respect_rate_limit(platform)
            
            # Platform-specific search
            if platform == PlatformType.TWITTER:
                return await self._search_twitter(query, max_results)
            elif platform == PlatformType.REDDIT:
                return await self._search_reddit(query, max_results)
            elif platform == PlatformType.GITHUB:
                return await self._search_github(query, max_results)
            elif platform == PlatformType.YOUTUBE:
                return await self._search_youtube(query, max_results)
            else:
                return {"error": f"Search not supported for platform: {platform}"}
                
        except Exception as e:
            logger.error(f"Error searching {platform} for {query}: {e}")
            return {"error": str(e)}
    
    async def _scrape_twitter(
        self, 
        username: str, 
        include_metadata: bool = True,
        include_media: bool = False,
        max_posts: int = 100
    ) -> Dict[str, Any]:
        """Scrape Twitter profile and posts"""
        try:
            # Note: This is a simplified implementation
            # In production, you would use Twitter API or web scraping
            
            # Simulate Twitter scraping
            profile_data = {
                "username": username,
                "display_name": f"User {username}",
                "bio": "Sample bio",
                "followers_count": random.randint(100, 10000),
                "following_count": random.randint(50, 5000),
                "posts_count": random.randint(10, 1000),
                "verified": random.choice([True, False]),
                "created_at": "2020-01-01T00:00:00Z",
                "profile_url": f"https://twitter.com/{username}",
                "is_private": False
            }
            
            # Generate sample posts
            posts = []
            for i in range(min(max_posts, 20)):
                post = {
                    "id": f"post_{i}",
                    "content": f"Sample tweet {i} from {username}",
                    "posted_at": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                    "likes_count": random.randint(0, 1000),
                    "retweets_count": random.randint(0, 500),
                    "replies_count": random.randint(0, 100),
                    "hashtags": ["#sample", "#test"],
                    "mentions": [],
                    "urls": [],
                    "media": []
                }
                posts.append(post)
            
            return {
                "platform": PlatformType.TWITTER,
                "profile": profile_data,
                "posts": posts,
                "scraped_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error scraping Twitter: {e}")
            return {"error": str(e)}
    
    async def _scrape_instagram(
        self, 
        username: str, 
        include_metadata: bool = True,
        include_media: bool = False,
        max_posts: int = 100
    ) -> Dict[str, Any]:
        """Scrape Instagram profile and posts"""
        try:
            # Simulate Instagram scraping
            profile_data = {
                "username": username,
                "display_name": f"User {username}",
                "bio": "Sample Instagram bio",
                "followers_count": random.randint(500, 50000),
                "following_count": random.randint(100, 2000),
                "posts_count": random.randint(5, 500),
                "verified": random.choice([True, False]),
                "is_private": random.choice([True, False]),
                "profile_url": f"https://instagram.com/{username}",
                "external_url": None
            }
            
            # Generate sample posts
            posts = []
            for i in range(min(max_posts, 15)):
                post = {
                    "id": f"ig_post_{i}",
                    "content": f"Sample Instagram post {i}",
                    "posted_at": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                    "likes_count": random.randint(0, 5000),
                    "comments_count": random.randint(0, 200),
                    "media_type": random.choice(["image", "video", "carousel"]),
                    "hashtags": ["#instagram", "#sample"],
                    "mentions": [],
                    "location": None
                }
                posts.append(post)
            
            return {
                "platform": PlatformType.INSTAGRAM,
                "profile": profile_data,
                "posts": posts,
                "scraped_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error scraping Instagram: {e}")
            return {"error": str(e)}
    
    async def _scrape_reddit(
        self, 
        username: str, 
        include_metadata: bool = True,
        max_posts: int = 100
    ) -> Dict[str, Any]:
        """Scrape Reddit user profile and posts"""
        try:
            # Simulate Reddit scraping
            profile_data = {
                "username": username,
                "display_name": f"Reddit User {username}",
                "karma": random.randint(100, 100000),
                "created_at": "2020-01-01T00:00:00Z",
                "is_gold": random.choice([True, False]),
                "is_moderator": random.choice([True, False]),
                "profile_url": f"https://reddit.com/user/{username}",
                "subreddits_moderated": random.randint(0, 5),
                "total_posts": random.randint(10, 1000)
            }
            
            # Generate sample posts
            posts = []
            for i in range(min(max_posts, 25)):
                post = {
                    "id": f"reddit_post_{i}",
                    "title": f"Sample Reddit post {i}",
                    "content": f"Sample content for post {i}",
                    "subreddit": random.choice(["programming", "technology", "science", "news"]),
                    "posted_at": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                    "upvotes": random.randint(-100, 1000),
                    "downvotes": random.randint(0, 100),
                    "comments_count": random.randint(0, 50),
                    "url": f"https://reddit.com/r/sample/comments/post_{i}"
                }
                posts.append(post)
            
            return {
                "platform": PlatformType.REDDIT,
                "profile": profile_data,
                "posts": posts,
                "scraped_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error scraping Reddit: {e}")
            return {"error": str(e)}
    
    async def _scrape_github(
        self, 
        username: str, 
        include_metadata: bool = True,
        max_posts: int = 100
    ) -> Dict[str, Any]:
        """Scrape GitHub user profile and activity"""
        try:
            # Simulate GitHub scraping
            profile_data = {
                "username": username,
                "display_name": f"GitHub User {username}",
                "bio": "Software developer and open source contributor",
                "followers": random.randint(10, 5000),
                "following": random.randint(5, 1000),
                "public_repos": random.randint(1, 100),
                "public_gists": random.randint(0, 50),
                "created_at": "2020-01-01T00:00:00Z",
                "updated_at": datetime.utcnow().isoformat(),
                "profile_url": f"https://github.com/{username}",
                "company": random.choice([None, "Tech Corp", "Open Source", "Freelance"]),
                "location": random.choice([None, "San Francisco", "New York", "London", "Remote"]),
                "blog": random.choice([None, f"https://{username}.com", "https://blog.example.com"]),
                "hireable": random.choice([True, False])
            }
            
            # Generate sample activity
            posts = []
            for i in range(min(max_posts, 30)):
                activity_types = ["commit", "issue", "pull_request", "repository", "gist"]
                activity_type = random.choice(activity_types)
                
                post = {
                    "id": f"github_activity_{i}",
                    "type": activity_type,
                    "title": f"Sample {activity_type} {i}",
                    "content": f"Sample GitHub activity {i}",
                    "repository": f"sample-repo-{i}",
                    "created_at": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                    "url": f"https://github.com/{username}/sample-repo-{i}"
                }
                posts.append(post)
            
            return {
                "platform": PlatformType.GITHUB,
                "profile": profile_data,
                "posts": posts,
                "scraped_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error scraping GitHub: {e}")
            return {"error": str(e)}
    
    async def _scrape_linkedin(
        self, 
        username: str, 
        include_metadata: bool = True,
        max_posts: int = 100
    ) -> Dict[str, Any]:
        """Scrape LinkedIn profile and posts"""
        try:
            # Simulate LinkedIn scraping
            profile_data = {
                "username": username,
                "display_name": f"LinkedIn User {username}",
                "headline": "Software Engineer | Technology Enthusiast",
                "company": random.choice(["Tech Corp", "Startup Inc", "Enterprise Ltd", "Freelance"]),
                "location": random.choice(["San Francisco, CA", "New York, NY", "London, UK", "Remote"]),
                "connections": random.randint(50, 5000),
                "followers": random.randint(10, 1000),
                "created_at": "2020-01-01T00:00:00Z",
                "profile_url": f"https://linkedin.com/in/{username}",
                "is_premium": random.choice([True, False])
            }
            
            # Generate sample posts
            posts = []
            for i in range(min(max_posts, 10)):
                post = {
                    "id": f"linkedin_post_{i}",
                    "content": f"Sample LinkedIn post {i} about professional development",
                    "posted_at": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                    "likes_count": random.randint(0, 500),
                    "comments_count": random.randint(0, 50),
                    "shares_count": random.randint(0, 20),
                    "hashtags": ["#technology", "#career", "#networking"],
                    "mentions": []
                }
                posts.append(post)
            
            return {
                "platform": PlatformType.LINKEDIN,
                "profile": profile_data,
                "posts": posts,
                "scraped_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error scraping LinkedIn: {e}")
            return {"error": str(e)}
    
    async def _scrape_facebook(
        self, 
        username: str, 
        include_metadata: bool = True,
        max_posts: int = 100
    ) -> Dict[str, Any]:
        """Scrape Facebook profile and posts"""
        try:
            # Simulate Facebook scraping
            profile_data = {
                "username": username,
                "display_name": f"Facebook User {username}",
                "bio": "Sample Facebook bio",
                "friends_count": random.randint(100, 2000),
                "followers_count": random.randint(10, 500),
                "posts_count": random.randint(5, 200),
                "created_at": "2020-01-01T00:00:00Z",
                "profile_url": f"https://facebook.com/{username}",
                "is_verified": random.choice([True, False]),
                "is_private": random.choice([True, False])
            }
            
            # Generate sample posts
            posts = []
            for i in range(min(max_posts, 15)):
                post = {
                    "id": f"fb_post_{i}",
                    "content": f"Sample Facebook post {i}",
                    "posted_at": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                    "likes_count": random.randint(0, 200),
                    "comments_count": random.randint(0, 30),
                    "shares_count": random.randint(0, 10),
                    "hashtags": ["#facebook", "#social"],
                    "mentions": []
                }
                posts.append(post)
            
            return {
                "platform": PlatformType.FACEBOOK,
                "profile": profile_data,
                "posts": posts,
                "scraped_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error scraping Facebook: {e}")
            return {"error": str(e)}
    
    async def _scrape_youtube(
        self, 
        username: str, 
        include_metadata: bool = True,
        max_posts: int = 100
    ) -> Dict[str, Any]:
        """Scrape YouTube channel and videos"""
        try:
            # Simulate YouTube scraping
            profile_data = {
                "username": username,
                "display_name": f"YouTube Channel {username}",
                "bio": "Sample YouTube channel description",
                "subscribers": random.randint(100, 1000000),
                "videos_count": random.randint(10, 500),
                "total_views": random.randint(10000, 10000000),
                "created_at": "2020-01-01T00:00:00Z",
                "profile_url": f"https://youtube.com/channel/{username}",
                "is_verified": random.choice([True, False])
            }
            
            # Generate sample videos
            posts = []
            for i in range(min(max_posts, 20)):
                post = {
                    "id": f"yt_video_{i}",
                    "title": f"Sample YouTube video {i}",
                    "description": f"Sample video description {i}",
                    "posted_at": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                    "views_count": random.randint(100, 1000000),
                    "likes_count": random.randint(0, 50000),
                    "comments_count": random.randint(0, 1000),
                    "duration": f"{random.randint(1, 60)}:{random.randint(0, 59):02d}",
                    "url": f"https://youtube.com/watch?v=video_{i}"
                }
                posts.append(post)
            
            return {
                "platform": PlatformType.YOUTUBE,
                "profile": profile_data,
                "posts": posts,
                "scraped_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error scraping YouTube: {e}")
            return {"error": str(e)}
    
    async def _scrape_tiktok(
        self, 
        username: str, 
        include_metadata: bool = True,
        max_posts: int = 100
    ) -> Dict[str, Any]:
        """Scrape TikTok profile and videos"""
        try:
            # Simulate TikTok scraping
            profile_data = {
                "username": username,
                "display_name": f"TikTok User {username}",
                "bio": "Sample TikTok bio",
                "followers": random.randint(100, 100000),
                "following": random.randint(10, 1000),
                "likes": random.randint(1000, 1000000),
                "videos_count": random.randint(5, 200),
                "created_at": "2020-01-01T00:00:00Z",
                "profile_url": f"https://tiktok.com/@{username}",
                "is_verified": random.choice([True, False])
            }
            
            # Generate sample videos
            posts = []
            for i in range(min(max_posts, 15)):
                post = {
                    "id": f"tt_video_{i}",
                    "title": f"Sample TikTok video {i}",
                    "description": f"Sample video description {i}",
                    "posted_at": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                    "views_count": random.randint(1000, 1000000),
                    "likes_count": random.randint(0, 100000),
                    "comments_count": random.randint(0, 5000),
                    "shares_count": random.randint(0, 1000),
                    "duration": f"{random.randint(15, 60)}s",
                    "hashtags": ["#tiktok", "#viral", "#trending"],
                    "url": f"https://tiktok.com/@username/video/{i}"
                }
                posts.append(post)
            
            return {
                "platform": PlatformType.TIKTOK,
                "profile": profile_data,
                "posts": posts,
                "scraped_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error scraping TikTok: {e}")
            return {"error": str(e)}
    
    async def _scrape_telegram(
        self, 
        username: str, 
        include_metadata: bool = True,
        max_posts: int = 100
    ) -> Dict[str, Any]:
        """Scrape Telegram channel/profile"""
        try:
            # Simulate Telegram scraping
            profile_data = {
                "username": username,
                "display_name": f"Telegram Channel {username}",
                "bio": "Sample Telegram channel description",
                "subscribers": random.randint(100, 100000),
                "posts_count": random.randint(10, 1000),
                "created_at": "2020-01-01T00:00:00Z",
                "profile_url": f"https://t.me/{username}",
                "is_verified": random.choice([True, False]),
                "is_private": random.choice([True, False])
            }
            
            # Generate sample posts
            posts = []
            for i in range(min(max_posts, 25)):
                post = {
                    "id": f"tg_post_{i}",
                    "content": f"Sample Telegram post {i}",
                    "posted_at": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                    "views_count": random.randint(100, 10000),
                    "forwards_count": random.randint(0, 100),
                    "replies_count": random.randint(0, 50),
                    "hashtags": ["#telegram", "#channel"],
                    "mentions": []
                }
                posts.append(post)
            
            return {
                "platform": PlatformType.TELEGRAM,
                "profile": profile_data,
                "posts": posts,
                "scraped_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error scraping Telegram: {e}")
            return {"error": str(e)}
    
    async def _scrape_discord(
        self, 
        username: str, 
        include_metadata: bool = True,
        max_posts: int = 100
    ) -> Dict[str, Any]:
        """Scrape Discord server/user"""
        try:
            # Simulate Discord scraping
            profile_data = {
                "username": username,
                "display_name": f"Discord User {username}",
                "bio": "Sample Discord bio",
                "servers_count": random.randint(1, 50),
                "created_at": "2020-01-01T00:00:00Z",
                "profile_url": f"https://discord.com/users/{username}",
                "is_verified": random.choice([True, False]),
                "is_bot": random.choice([True, False])
            }
            
            # Generate sample messages
            posts = []
            for i in range(min(max_posts, 30)):
                post = {
                    "id": f"discord_msg_{i}",
                    "content": f"Sample Discord message {i}",
                    "posted_at": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                    "server": f"Sample Server {random.randint(1, 10)}",
                    "channel": f"general",
                    "reactions": random.randint(0, 10),
                    "mentions": []
                }
                posts.append(post)
            
            return {
                "platform": PlatformType.DISCORD,
                "profile": profile_data,
                "posts": posts,
                "scraped_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error scraping Discord: {e}")
            return {"error": str(e)}
    
    async def _get_profile_data(self, platform: PlatformType, username: str) -> Optional[Dict[str, Any]]:
        """Get profile data for platform"""
        try:
            # This would implement platform-specific profile fetching
            # For now, return simulated data
            return {
                "username": username,
                "platform": platform,
                "display_name": f"User {username}",
                "bio": f"Sample bio for {username}",
                "created_at": "2020-01-01T00:00:00Z",
                "is_verified": random.choice([True, False])
            }
        except Exception as e:
            logger.error(f"Error getting profile data: {e}")
            return None
    
    async def _get_recent_posts(self, platform: PlatformType, username: str) -> List[Dict[str, Any]]:
        """Get recent posts for platform"""
        try:
            # This would implement platform-specific post fetching
            # For now, return simulated data
            posts = []
            for i in range(10):
                post = {
                    "id": f"post_{i}",
                    "content": f"Sample post {i} from {username}",
                    "posted_at": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                    "likes_count": random.randint(0, 1000),
                    "comments_count": random.randint(0, 100)
                }
                posts.append(post)
            return posts
        except Exception as e:
            logger.error(f"Error getting recent posts: {e}")
            return []
    
    async def _get_network_data(self, platform: PlatformType, username: str) -> Dict[str, Any]:
        """Get network data (followers, following)"""
        try:
            return {
                "followers_count": random.randint(100, 10000),
                "following_count": random.randint(50, 5000),
                "mutual_connections": random.randint(10, 500)
            }
        except Exception as e:
            logger.error(f"Error getting network data: {e}")
            return {}
    
    async def _assess_profile_threat(
        self, 
        platform: PlatformType, 
        profile_data: Dict[str, Any], 
        posts: List[Dict[str, Any]]
    ) -> ThreatAssessment:
        """Assess profile threat level"""
        try:
            threat_score = 0.0
            indicators = []
            risk_factors = []
            recommendations = []
            
            # Check for suspicious keywords in bio
            bio = profile_data.get("bio", "").lower()
            suspicious_keywords = [
                "hack", "crack", "exploit", "malware", "virus",
                "ddos", "botnet", "keylogger", "spyware", "ransomware"
            ]
            
            for keyword in suspicious_keywords:
                if keyword in bio:
                    threat_score += 0.3
                    indicators.append(f"Suspicious bio keyword: {keyword}")
            
            # Check for recently created account
            created_at = datetime.fromisoformat(profile_data["created_at"].replace("Z", "+00:00"))
            days_old = (datetime.utcnow() - created_at.replace(tzinfo=None)).days
            
            if days_old < 90:
                threat_score += 0.1
                indicators.append("Recently created account")
                risk_factors.append("New account with limited history")
            
            # Check for suspicious post content
            suspicious_post_count = 0
            for post in posts:
                content = post.get("content", "").lower()
                
                for keyword in suspicious_keywords:
                    if keyword in content:
                        suspicious_post_count += 1
                        break
            
            if suspicious_post_count > 0:
                threat_score += 0.2 * suspicious_post_count
                indicators.append(f"{suspicious_post_count} posts with suspicious content")
            
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
                recommendations.append("Review profile content")
                recommendations.append("Check post history")
            
            if threat_score > 0.6:
                recommendations.append("Consider security review")
                recommendations.append("Monitor for suspicious activity")
            
            return ThreatAssessment(
                target=f"{platform}:{profile_data['username']}",
                threat_level=threat_level,
                threat_score=min(threat_score, 1.0),
                indicators=indicators,
                risk_factors=risk_factors,
                recommendations=recommendations,
                confidence=0.8
            )
            
        except Exception as e:
            logger.error(f"Error assessing profile threat: {e}")
            return ThreatAssessment(
                target=f"{platform}:{profile_data.get('username', 'unknown')}",
                threat_level=ThreatLevel.LOW,
                threat_score=0.0,
                indicators=["Error in threat assessment"],
                risk_factors=[],
                recommendations=["Manual review recommended"],
                confidence=0.0
            )
    
    async def _analyze_sentiment(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze sentiment of posts"""
        try:
            # This would implement actual sentiment analysis
            # For now, return simulated data
            total_posts = len(posts)
            positive_count = random.randint(0, total_posts // 3)
            negative_count = random.randint(0, total_posts // 4)
            neutral_count = total_posts - positive_count - negative_count
            
            return {
                "total_posts": total_posts,
                "positive_posts": positive_count,
                "negative_posts": negative_count,
                "neutral_posts": neutral_count,
                "overall_sentiment": random.choice(["positive", "neutral", "negative"]),
                "sentiment_score": random.uniform(-1.0, 1.0)
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {"error": str(e)}
    
    async def _search_twitter(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search Twitter content"""
        try:
            # Simulate Twitter search
            results = []
            for i in range(min(max_results, 20)):
                result = {
                    "id": f"search_result_{i}",
                    "content": f"Sample tweet about {query}",
                    "author": f"user_{i}",
                    "posted_at": (datetime.utcnow() - timedelta(hours=i)).isoformat(),
                    "likes_count": random.randint(0, 1000),
                    "retweets_count": random.randint(0, 500)
                }
                results.append(result)
            
            return {
                "query": query,
                "results": results,
                "total_results": len(results)
            }
        except Exception as e:
            logger.error(f"Error searching Twitter: {e}")
            return {"error": str(e)}
    
    async def _search_reddit(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search Reddit content"""
        try:
            # Simulate Reddit search
            results = []
            for i in range(min(max_results, 25)):
                result = {
                    "id": f"reddit_search_{i}",
                    "title": f"Sample Reddit post about {query}",
                    "content": f"Sample content about {query}",
                    "subreddit": random.choice(["programming", "technology", "science"]),
                    "author": f"reddit_user_{i}",
                    "posted_at": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                    "upvotes": random.randint(-100, 1000)
                }
                results.append(result)
            
            return {
                "query": query,
                "results": results,
                "total_results": len(results)
            }
        except Exception as e:
            logger.error(f"Error searching Reddit: {e}")
            return {"error": str(e)}
    
    async def _search_github(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search GitHub repositories"""
        try:
            # Simulate GitHub search
            results = []
            for i in range(min(max_results, 30)):
                result = {
                    "id": f"github_search_{i}",
                    "name": f"sample-repo-{i}",
                    "full_name": f"user/sample-repo-{i}",
                    "description": f"Sample repository about {query}",
                    "language": random.choice(["Python", "JavaScript", "Java", "C++"]),
                    "stars": random.randint(0, 1000),
                    "forks": random.randint(0, 100),
                    "created_at": "2020-01-01T00:00:00Z"
                }
                results.append(result)
            
            return {
                "query": query,
                "results": results,
                "total_results": len(results)
            }
        except Exception as e:
            logger.error(f"Error searching GitHub: {e}")
            return {"error": str(e)}
    
    async def _search_youtube(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search YouTube videos"""
        try:
            # Simulate YouTube search
            results = []
            for i in range(min(max_results, 20)):
                result = {
                    "id": f"yt_search_{i}",
                    "title": f"Sample YouTube video about {query}",
                    "description": f"Sample video description about {query}",
                    "channel": f"channel_{i}",
                    "posted_at": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                    "views_count": random.randint(100, 1000000),
                    "likes_count": random.randint(0, 50000)
                }
                results.append(result)
            
            return {
                "query": query,
                "results": results,
                "total_results": len(results)
            }
        except Exception as e:
            logger.error(f"Error searching YouTube: {e}")
            return {"error": str(e)}
    
    async def _respect_rate_limit(self, platform: PlatformType):
        """Respect platform rate limits"""
        try:
            rate_limit = self.rate_limits.get(platform, {"requests_per_minute": 100, "last_request": 0})
            current_time = time.time()
            
            # Check if we need to wait
            time_since_last = current_time - rate_limit["last_request"]
            min_interval = 60.0 / rate_limit["requests_per_minute"]
            
            if time_since_last < min_interval:
                wait_time = min_interval - time_since_last
                await asyncio.sleep(wait_time)
            
            # Update last request time
            self.rate_limits[platform]["last_request"] = int(time.time())
            
        except Exception as e:
            logger.error(f"Error in rate limiting: {e}")
            # Default wait time
            await asyncio.sleep(1.0) 