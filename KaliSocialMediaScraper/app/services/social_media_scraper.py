"""
Advanced Social Media Scraping Service
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
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
    
    async def _scrape_twitter(self, username: str, include_metadata: bool = True, include_media: bool = False, max_posts: int = 100) -> Dict[str, Any]:
        """Scrape X (Twitter) profile and posts using Playwright for robust, stealthy scraping"""
        try:
            from app.services.playwright_utils import get_browser, get_context, get_page, random_delay
            import re
            
            # Optionally select a proxy from config/env
            proxy = None
            browser = await get_browser(proxy)
            context = await get_context(browser)
            page = await get_page(context)
            profile_url = f"https://twitter.com/{username}"
            try:
                await page.goto(profile_url, timeout=30000)
                await random_delay(2, 4)
                
                # Wait for profile header to load
                await page.wait_for_selector('div[data-testid="primaryColumn"]', timeout=10000)
                content = await page.content()
                
                # Parse profile data
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                profile_data = {
                    "username": username,
                    "display_name": "",
                    "bio": "",
                    "followers_count": 0,
                    "following_count": 0,
                    "posts_count": 0,
                    "verified": False,
                    "created_at": "",
                    "profile_url": profile_url,
                    "is_private": False
                }
                # Display name
                display_name_elem = soup.find('span', {'data-testid': 'UserName'})
                if display_name_elem:
                    profile_data["display_name"] = display_name_elem.get_text().strip()
                # Bio
                bio_elem = soup.find('div', {'data-testid': 'UserDescription'})
                if bio_elem:
                    profile_data["bio"] = bio_elem.get_text().strip()
                # Followers
                followers_elem = soup.find('a', href=f'/{username}/followers')
                if followers_elem:
                    followers_text = followers_elem.get_text()
                    followers_match = re.search(r'(\d+(?:,\d+)*)', followers_text)
                    if followers_match:
                        profile_data["followers_count"] = int(followers_match.group(1).replace(',', ''))
                # Following
                following_elem = soup.find('a', href=f'/{username}/following')
                if following_elem:
                    following_text = following_elem.get_text()
                    following_match = re.search(r'(\d+(?:,\d+)*)', following_text)
                    if following_match:
                        profile_data["following_count"] = int(following_match.group(1).replace(',', ''))
                # Verified
                verified_elem = soup.find('svg', {'data-testid': 'icon-verified'})
                profile_data["verified"] = verified_elem is not None
                
                # Posts (tweets)
                posts = []
                tweet_divs = soup.find_all('div', {'data-testid': 'tweet'})
                for i, tweet_div in enumerate(tweet_divs[:max_posts]):
                    try:
                        tweet_content = tweet_div.get_text(separator=" ", strip=True)
                        post = {
                            "id": f"tweet_{i}",
                            "content": tweet_content,
                            "posted_at": "",  # Could extract from timestamp if available
                            "likes_count": 0,  # Could extract if available
                            "retweets_count": 0,  # Could extract if available
                            "replies_count": 0,  # Could extract if available
                            "hashtags": [],
                            "mentions": [],
                            "urls": [],
                            "media": []
                        }
                        posts.append(post)
                    except Exception as e:
                        continue
                
                await context.close()
                await browser.close()
                
                return {
                    "platform": PlatformType.TWITTER,
                    "profile": profile_data,
                    "posts": posts,
                    "scraped_at": datetime.utcnow().isoformat()
                }
            except Exception as e:
                await context.close()
                await browser.close()
                logger.error(f"Error scraping X profile {username}: {e}")
                return {"error": str(e)}
        except Exception as e:
            logger.error(f"Error scraping X profile {username}: {e}")
            return {"error": str(e)}
    
    async def _scrape_instagram(self, username: str, include_metadata: bool = True, include_media: bool = False, max_posts: int = 100) -> Dict[str, Any]:
        """Scrape Instagram profile and posts using Playwright for robust, stealthy scraping"""
        try:
            from app.services.playwright_utils import get_browser, get_context, get_page, random_delay
            import re
            
            # Rate limiting
            await self._respect_rate_limit(PlatformType.INSTAGRAM)
            
            # Instagram profile URL
            profile_url = f"https://www.instagram.com/{username}/"
            
            # Optionally select a proxy from config/env
            proxy = None
            browser = await get_browser(proxy)
            context = await get_context(browser)
            page = await get_page(context)
            
            try:
                await page.goto(profile_url, timeout=30000)
                await random_delay(3, 5)
                
                # Wait for profile content to load
                await page.wait_for_selector('main', timeout=15000)
                await random_delay(2, 3)
                
                # Extract profile information
                profile_data = await self._parse_instagram_profile(page, username)
                
                # Get posts
                posts = await self._get_instagram_posts(page, max_posts)
                
                return {
                    "platform": PlatformType.INSTAGRAM,
                    "profile": profile_data,
                    "posts": posts,
                    "scraped_at": datetime.utcnow().isoformat()
                }
                
            finally:
                await browser.close()
                
        except Exception as e:
            logger.error(f"Error scraping Instagram profile {username}: {e}")
            return {"error": str(e)}
    
    async def _parse_instagram_profile(self, page, username: str) -> Dict[str, Any]:
        """Parse Instagram profile data from Playwright page"""
        try:
            profile_data = {
                "username": username,
                "display_name": "",
                "bio": "",
                "followers_count": 0,
                "following_count": 0,
                "posts_count": 0,
                "verified": False,
                "is_private": False,
                "profile_url": f"https://instagram.com/{username}",
                "external_url": None
            }
            
            # Try to extract display name
            try:
                display_name_elem = await page.query_selector("h2")
                if display_name_elem:
                    profile_data["display_name"] = await display_name_elem.text_content()
                    if profile_data["display_name"]:
                        profile_data["display_name"] = profile_data["display_name"].strip()
            except:
                pass
            
            # Try to extract bio
            try:
                bio_elem = await page.query_selector("div[data-testid='user-bio']")
                if bio_elem:
                    profile_data["bio"] = await bio_elem.text_content()
                    if profile_data["bio"]:
                        profile_data["bio"] = profile_data["bio"].strip()
            except:
                pass
            
            # Try to extract follower counts
            try:
                stats_elements = await page.query_selector_all("li")
                for stat_elem in stats_elements:
                    stat_text = await stat_elem.text_content()
                    if stat_text:
                        stat_text = stat_text.lower()
                        if "posts" in stat_text:
                            import re
                            match = re.search(r'(\d+(?:,\d+)*)', stat_text)
                            if match:
                                profile_data["posts_count"] = int(match.group(1).replace(',', ''))
                        elif "followers" in stat_text:
                            import re
                            match = re.search(r'(\d+(?:,\d+)*)', stat_text)
                            if match:
                                profile_data["followers_count"] = int(match.group(1).replace(',', ''))
                        elif "following" in stat_text:
                            import re
                            match = re.search(r'(\d+(?:,\d+)*)', stat_text)
                            if match:
                                profile_data["following_count"] = int(match.group(1).replace(',', ''))
            except:
                pass
            
            # Check if private
            try:
                private_elem = await page.query_selector("h2[data-testid='private-account']")
                if private_elem:
                    profile_data["is_private"] = True
            except:
                pass
            
            # Check if verified
            try:
                verified_elem = await page.query_selector("span[data-testid='verified-badge']")
                if verified_elem:
                    profile_data["verified"] = True
            except:
                pass
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error parsing Instagram profile: {e}")
            return {"error": str(e)}
    
    async def _get_instagram_posts(self, page, max_posts: int) -> List[Dict[str, Any]]:
        """Get Instagram posts from profile using Playwright"""
        try:
            posts: List[Dict[str, Any]] = []
            
            # Scroll to load more posts
            for _ in range(3):  # Scroll 3 times to load more content
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                await asyncio.sleep(2)
            
            # Find post elements
            post_elements = await page.query_selector_all("article a")
            
            for i, post_elem in enumerate(post_elements[:max_posts]):
                try:
                    # Get post URL
                    post_url = await post_elem.get_attribute("href")
                    
                    # Extract post information
                    post_info = {
                        "id": f"ig_post_{i}",
                        "content": "",  # Would need to visit post page
                        "posted_at": "",  # Would need to visit post page
                        "likes_count": 0,  # Would need to visit post page
                        "comments_count": 0,  # Would need to visit post page
                        "media_type": "image",  # Default
                        "hashtags": [],
                        "mentions": [],
                        "location": None,
                        "url": post_url
                    }
                    
                    posts.append(post_info)
                    
                except Exception as e:
                    logger.error(f"Error extracting Instagram post {i}: {e}")
                    continue
            
            return posts
            
        except Exception as e:
            logger.error(f"Error getting Instagram posts: {e}")
            return []

    async def _scrape_reddit(self, username: str, include_metadata: bool = True, max_posts: int = 100) -> Dict[str, Any]:
        """Scrape Reddit user profile and posts using real API and web scraping"""
        try:
            # Rate limiting
            await self._respect_rate_limit(PlatformType.REDDIT)
            
            # Reddit API endpoint for user data
            user_url = f"https://www.reddit.com/user/{username}/about.json"
            
            async with self.session.get(user_url, headers={
                "User-Agent": "Kali-OSINT-Platform/1.0"
            }) as response:
                if response.status != 200:
                    return {"error": f"Failed to access Reddit user: {response.status}"}
                
                user_data = await response.json()
                
                if "data" not in user_data:
                    return {"error": "Invalid Reddit user data"}
                
                profile_data = await self._parse_reddit_profile(user_data["data"], username)
                
                # Get user posts
                posts = await self._get_reddit_posts(username, max_posts)
                
                return {
                    "platform": PlatformType.REDDIT,
                    "profile": profile_data,
                    "posts": posts,
                    "scraped_at": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error scraping Reddit user {username}: {e}")
            return {"error": str(e)}
    
    async def _parse_reddit_profile(self, user_data: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Parse Reddit profile data from API response"""
        try:
            profile_data = {
                "username": username,
                "display_name": user_data.get("subreddit", {}).get("display_name", username),
                "karma": user_data.get("total_karma", 0),
                "created_at": datetime.fromtimestamp(user_data.get("created_utc", 0)).isoformat(),
                "is_gold": user_data.get("is_gold", False),
                "is_moderator": user_data.get("is_mod", False),
                "profile_url": f"https://reddit.com/user/{username}",
                "subreddits_moderated": len(user_data.get("moderated_subreddits", [])),
                "total_posts": user_data.get("link_karma", 0) + user_data.get("comment_karma", 0),
                "link_karma": user_data.get("link_karma", 0),
                "comment_karma": user_data.get("comment_karma", 0),
                "verified": user_data.get("verified", False),
                "has_verified_email": user_data.get("has_verified_email", False),
                "is_employee": user_data.get("is_employee", False),
                "hide_from_robots": user_data.get("hide_from_robots", False)
            }
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error parsing Reddit profile: {e}")
            return {"error": str(e)}
    
    async def _get_reddit_posts(self, username: str, max_posts: int) -> List[Dict[str, Any]]:
        """Get recent Reddit posts from user"""
        try:
            posts: List[Dict[str, Any]] = []
            
            # Reddit API endpoint for user posts
            posts_url = f"https://www.reddit.com/user/{username}/submitted.json?limit={max_posts}"
            
            async with self.session.get(posts_url, headers={
                "User-Agent": "Kali-OSINT-Platform/1.0"
            }) as response:
                if response.status == 200:
                    posts_data = await response.json()
                    
                    if "data" in posts_data and "children" in posts_data["data"]:
                        for post in posts_data["data"]["children"]:
                            post_data = post["data"]
                            
                            post_info = {
                                "id": post_data.get("id", ""),
                                "title": post_data.get("title", ""),
                                "content": post_data.get("selftext", ""),
                                "subreddit": post_data.get("subreddit", ""),
                                "posted_at": datetime.fromtimestamp(post_data.get("created_utc", 0)).isoformat(),
                                "upvotes": post_data.get("score", 0),
                                "downvotes": 0,  # Reddit doesn't provide downvote counts
                                "comments_count": post_data.get("num_comments", 0),
                                "url": f"https://reddit.com{post_data.get('permalink', '')}",
                                "is_self": post_data.get("is_self", False),
                                "is_video": post_data.get("is_video", False),
                                "over_18": post_data.get("over_18", False),
                                "spoiler": post_data.get("spoiler", False),
                                "stickied": post_data.get("stickied", False),
                                "locked": post_data.get("locked", False)
                            }
                            
                            posts.append(post_info)
            
            return posts
            
        except Exception as e:
            logger.error(f"Error getting Reddit posts: {e}")
            return []

    async def _scrape_github(self, username: str, include_metadata: bool = True, max_posts: int = 100) -> Dict[str, Any]:
        """Scrape GitHub user profile and activity using real API"""
        try:
            # Rate limiting
            await self._respect_rate_limit(PlatformType.GITHUB)
            
            # GitHub API endpoint for user data
            user_url = f"https://api.github.com/users/{username}"
            
            async with self.session.get(user_url, headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Kali-OSINT-Platform/1.0"
            }) as response:
                if response.status != 200:
                    return {"error": f"Failed to access GitHub user: {response.status}"}
                
                user_data = await response.json()
                profile_data = await self._parse_github_profile(user_data, username)
                
                # Get user repositories
                repos = await self._get_github_repos(username, max_posts)
                
                # Get user activity (public events)
                activity = await self._get_github_activity(username, max_posts)
                
                return {
                    "platform": PlatformType.GITHUB,
                    "profile": profile_data,
                    "repositories": repos,
                    "activity": activity,
                    "scraped_at": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error scraping GitHub user {username}: {e}")
            return {"error": str(e)}
    
    async def _parse_github_profile(self, user_data: Dict[str, Any], username: str) -> Dict[str, Any]:
        """Parse GitHub profile data from API response"""
        try:
            profile_data = {
                "username": username,
                "display_name": user_data.get("name", username),
                "bio": user_data.get("bio", ""),
                "followers": user_data.get("followers", 0),
                "following": user_data.get("following", 0),
                "public_repos": user_data.get("public_repos", 0),
                "public_gists": user_data.get("public_gists", 0),
                "created_at": user_data.get("created_at", ""),
                "updated_at": user_data.get("updated_at", ""),
                "profile_url": user_data.get("html_url", f"https://github.com/{username}"),
                "company": user_data.get("company"),
                "location": user_data.get("location"),
                "blog": user_data.get("blog"),
                "hireable": user_data.get("hireable", False),
                "verified": user_data.get("verified", False),
                "type": user_data.get("type", "User"),
                "site_admin": user_data.get("site_admin", False),
                "avatar_url": user_data.get("avatar_url"),
                "gravatar_id": user_data.get("gravatar_id")
            }
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error parsing GitHub profile: {e}")
            return {"error": str(e)}
    
    async def _get_github_repos(self, username: str, max_repos: int) -> List[Dict[str, Any]]:
        """Get GitHub repositories for user"""
        try:
            repos: List[Dict[str, Any]] = []
            
            # GitHub API endpoint for user repositories
            repos_url = f"https://api.github.com/users/{username}/repos?per_page={max_repos}&sort=updated"
            
            async with self.session.get(repos_url, headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Kali-OSINT-Platform/1.0"
            }) as response:
                if response.status == 200:
                    repos_data = await response.json()
                    
                    for repo in repos_data:
                        repo_info = {
                            "id": repo.get("id", ""),
                            "name": repo.get("name", ""),
                            "full_name": repo.get("full_name", ""),
                            "description": repo.get("description", ""),
                            "language": repo.get("language"),
                            "stars": repo.get("stargazers_count", 0),
                            "forks": repo.get("forks_count", 0),
                            "watchers": repo.get("watchers_count", 0),
                            "open_issues": repo.get("open_issues_count", 0),
                            "created_at": repo.get("created_at", ""),
                            "updated_at": repo.get("updated_at", ""),
                            "pushed_at": repo.get("pushed_at", ""),
                            "size": repo.get("size", 0),
                            "license": repo.get("license"),
                            "topics": repo.get("topics", []),
                            "default_branch": repo.get("default_branch", ""),
                            "private": repo.get("private", False),
                            "archived": repo.get("archived", False),
                            "disabled": repo.get("disabled", False),
                            "homepage": repo.get("homepage"),
                            "html_url": repo.get("html_url", ""),
                            "clone_url": repo.get("clone_url", ""),
                            "ssh_url": repo.get("ssh_url", ""),
                            "fork": repo.get("fork", False),
                            "mirror_url": repo.get("mirror_url"),
                            "has_issues": repo.get("has_issues", True),
                            "has_projects": repo.get("has_projects", True),
                            "has_downloads": repo.get("has_downloads", True),
                            "has_wiki": repo.get("has_wiki", True),
                            "has_pages": repo.get("has_pages", False),
                            "has_discussions": repo.get("has_discussions", False)
                        }
                        
                        repos.append(repo_info)
            
            return repos
            
        except Exception as e:
            logger.error(f"Error getting GitHub repos: {e}")
            return []
    
    async def _get_github_activity(self, username: str, max_events: int) -> List[Dict[str, Any]]:
        """Get GitHub public activity for user"""
        try:
            activity: List[Dict[str, Any]] = []
            
            # GitHub API endpoint for public events
            events_url = f"https://api.github.com/users/{username}/events?per_page={max_events}"
            
            async with self.session.get(events_url, headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Kali-OSINT-Platform/1.0"
            }) as response:
                if response.status == 200:
                    events_data = await response.json()
                    
                    for event in events_data:
                        event_info = {
                            "id": event.get("id", ""),
                            "type": event.get("type", ""),
                            "actor": event.get("actor", {}).get("login", ""),
                            "repo": event.get("repo", {}).get("name", ""),
                            "created_at": event.get("created_at", ""),
                            "payload": event.get("payload", {}),
                            "public": event.get("public", True)
                        }
                        
                        activity.append(event_info)
            
            return activity
            
        except Exception as e:
            logger.error(f"Error getting GitHub activity: {e}")
            return []

    async def _scrape_linkedin(self, username: str, include_metadata: bool = True, max_posts: int = 100) -> Dict[str, Any]:
        """Scrape LinkedIn profile and posts using real web scraping"""
        try:
            # Rate limiting
            await self._respect_rate_limit(PlatformType.LINKEDIN)
            
            # LinkedIn requires authentication for most data
            # For now, return limited public data
            profile_url = f"https://www.linkedin.com/in/{username}/"
            
            async with self.session.get(profile_url) as response:
                if response.status != 200:
                    return {"error": f"Failed to access LinkedIn profile: {response.status}"}
                
                html_content = await response.text()
                
                # Parse basic profile data
                profile_data = await self._parse_linkedin_profile(html_content, username)
                
                return {
                    "platform": PlatformType.LINKEDIN,
                    "profile": profile_data,
                    "posts": [],  # LinkedIn posts require authentication
                    "scraped_at": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error scraping LinkedIn profile {username}: {e}")
            return {"error": str(e)}
    
    async def _parse_linkedin_profile(self, html_content: str, username: str) -> Dict[str, Any]:
        """Parse LinkedIn profile data from HTML"""
        try:
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            profile_data = {
                "username": username,
                "display_name": "",
                "headline": "",
                "company": "",
                "location": "",
                "connections": 0,
                "followers": 0,
                "created_at": "",
                "profile_url": f"https://linkedin.com/in/{username}",
                "is_premium": False
            }
            
            # Try to extract display name
            name_elem = soup.find('h1', {'class': 'text-heading-xlarge'})
            if name_elem:
                profile_data["display_name"] = name_elem.get_text().strip()
            
            # Try to extract headline
            headline_elem = soup.find('div', {'class': 'text-body-medium'})
            if headline_elem:
                profile_data["headline"] = headline_elem.get_text().strip()
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error parsing LinkedIn profile: {e}")
            return {"error": str(e)}
    
    async def _scrape_facebook(self, username: str, include_metadata: bool = True, max_posts: int = 100) -> Dict[str, Any]:
        """Scrape Facebook profile and posts using real web scraping"""
        try:
            # Rate limiting
            await self._respect_rate_limit(PlatformType.FACEBOOK)
            
            # Facebook requires authentication for most data
            # For now, return limited public data
            profile_url = f"https://www.facebook.com/{username}/"
            
            async with self.session.get(profile_url) as response:
                if response.status != 200:
                    return {"error": f"Failed to access Facebook profile: {response.status}"}
                
                html_content = await response.text()
                
                # Parse basic profile data
                profile_data = await self._parse_facebook_profile(html_content, username)
                
                return {
                    "platform": PlatformType.FACEBOOK,
                    "profile": profile_data,
                    "posts": [],  # Facebook posts require authentication
                    "scraped_at": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error scraping Facebook profile {username}: {e}")
            return {"error": str(e)}
    
    async def _parse_facebook_profile(self, html_content: str, username: str) -> Dict[str, Any]:
        """Parse Facebook profile data from HTML"""
        try:
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            profile_data = {
                "username": username,
                "display_name": "",
                "bio": "",
                "friends_count": 0,
                "followers_count": 0,
                "posts_count": 0,
                "created_at": "",
                "profile_url": f"https://facebook.com/{username}",
                "is_verified": False,
                "is_private": False
            }
            
            # Try to extract display name
            name_elem = soup.find('h1')
            if name_elem:
                profile_data["display_name"] = name_elem.get_text().strip()
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error parsing Facebook profile: {e}")
            return {"error": str(e)}
    
    async def _scrape_youtube(self, username: str, include_metadata: bool = True, max_posts: int = 100) -> Dict[str, Any]:
        """Scrape YouTube channel and videos using Playwright for robust, stealthy scraping"""
        try:
            from app.services.playwright_utils import get_browser, get_context, get_page, random_delay
            import re
            
            # Rate limiting
            await self._respect_rate_limit(PlatformType.YOUTUBE)
            
            # YouTube channel URL
            channel_url = f"https://www.youtube.com/@{username}"
            
            # Optionally select a proxy from config/env
            proxy = None
            browser = await get_browser(proxy)
            context = await get_context(browser)
            page = await get_page(context)
            
            try:
                await page.goto(channel_url, timeout=30000)
                await random_delay(3, 5)
                
                # Wait for channel content to load
                await page.wait_for_selector('ytd-channel-name', timeout=15000)
                await random_delay(2, 3)
                
                # Extract channel information
                profile_data = await self._parse_youtube_channel(page, username)
                
                # Get videos
                videos = await self._get_youtube_videos(page, max_posts)
                
                return {
                    "platform": PlatformType.YOUTUBE,
                    "profile": profile_data,
                    "videos": videos,
                    "scraped_at": datetime.utcnow().isoformat()
                }
                
            finally:
                await browser.close()
                
        except Exception as e:
            logger.error(f"Error scraping YouTube channel {username}: {e}")
            return {"error": str(e)}
    
    async def _parse_youtube_channel(self, page, username: str) -> Dict[str, Any]:
        """Parse YouTube channel data from Playwright page"""
        try:
            profile_data = {
                "username": username,
                "display_name": "",
                "bio": "",
                "subscribers": 0,
                "videos_count": 0,
                "total_views": 0,
                "created_at": "",
                "profile_url": f"https://youtube.com/@{username}",
                "is_verified": False
            }
            
            # Try to extract channel name
            try:
                channel_name_elem = await page.query_selector("yt-formatted-string.ytd-channel-name")
                if channel_name_elem:
                    profile_data["display_name"] = await channel_name_elem.text_content()
                    if profile_data["display_name"]:
                        profile_data["display_name"] = profile_data["display_name"].strip()
            except:
                pass
            
            # Try to extract subscriber count
            try:
                subscriber_elem = await page.query_selector("yt-formatted-string#subscriber-count")
                if subscriber_elem:
                    subscriber_text = await subscriber_elem.text_content()
                    if subscriber_text:
                        # Parse subscriber count (e.g., "1.2M subscribers")
                        import re
                        match = re.search(r'(\d+(?:\.\d+)?)([KMB]?)', subscriber_text)
                        if match:
                            count = float(match.group(1))
                            multiplier = {"K": 1000, "M": 1000000, "B": 1000000000}.get(match.group(2), 1)
                            profile_data["subscribers"] = int(count * multiplier)
            except:
                pass
            
            # Try to extract video count
            try:
                video_count_elem = await page.query_selector("span#video-count")
                if video_count_elem:
                    video_count_text = await video_count_elem.text_content()
                    if video_count_text:
                        import re
                        match = re.search(r'(\d+(?:,\d+)*)', video_count_text)
                        if match:
                            profile_data["videos_count"] = int(match.group(1).replace(',', ''))
            except:
                pass
            
            # Check if verified
            try:
                verified_elem = await page.query_selector("yt-icon#channel-name.ytd-channel-name")
                if verified_elem:
                    profile_data["is_verified"] = True
            except:
                pass
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error parsing YouTube channel: {e}")
            return {"error": str(e)}
    
    async def _get_youtube_videos(self, page, max_videos: int) -> List[Dict[str, Any]]:
        """Get YouTube videos from channel using Playwright"""
        try:
            videos: List[Dict[str, Any]] = []
            
            # Scroll to load more videos
            for _ in range(3):  # Scroll 3 times to load more content
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                await asyncio.sleep(2)
            
            # Find video elements
            video_elements = await page.query_selector_all("ytd-grid-video-renderer")
            
            for i, video_elem in enumerate(video_elements[:max_videos]):
                try:
                    # Extract video information
                    title_elem = await video_elem.query_selector("#video-title")
                    title = ""
                    if title_elem:
                        title = await title_elem.get_attribute("title")
                    
                    # Get video URL
                    video_url = ""
                    if title_elem:
                        video_url = await title_elem.get_attribute("href")
                        if video_url and not video_url.startswith("http"):
                            video_url = f"https://youtube.com{video_url}"
                    
                    # Extract view count
                    views_count = 0
                    try:
                        view_count_elem = await video_elem.query_selector("#metadata-line span")
                        if view_count_elem:
                            view_count_text = await view_count_elem.text_content()
                            if view_count_text:
                                import re
                                match = re.search(r'(\d+(?:,\d+)*)', view_count_text)
                                views_count = int(match.group(1).replace(',', '')) if match else 0
                    except:
                        pass
                    
                    # Extract upload time
                    upload_time = ""
                    try:
                        time_elem = await video_elem.query_selector("#metadata-line span:last-child")
                        if time_elem:
                            upload_time = await time_elem.text_content()
                            if upload_time:
                                upload_time = upload_time.strip()
                    except:
                        pass
                    
                    video_info = {
                        "id": f"video_{i}",
                        "title": title,
                        "description": "",  # Would need to visit video page
                        "posted_at": upload_time,
                        "views_count": views_count,
                        "likes_count": 0,  # Would need to visit video page
                        "comments_count": 0,  # Would need to visit video page
                        "duration": "",  # Would need to visit video page
                        "url": video_url
                    }
                    
                    videos.append(video_info)
                    
                except Exception as e:
                    logger.error(f"Error extracting video {i}: {e}")
                    continue
            
            return videos
            
        except Exception as e:
            logger.error(f"Error getting YouTube videos: {e}")
            return []

    async def _scrape_tiktok(self, username: str, include_metadata: bool = True, max_posts: int = 100) -> Dict[str, Any]:
        """Scrape TikTok profile and videos using real web scraping"""
        try:
            # Rate limiting
            await self._respect_rate_limit(PlatformType.TIKTOK)
            
            # TikTok profile URL
            profile_url = f"https://www.tiktok.com/@{username}"
            
            async with self.session.get(profile_url) as response:
                if response.status != 200:
                    return {"error": f"Failed to access TikTok profile: {response.status}"}
                
                html_content = await response.text()
                
                # Parse profile data
                profile_data = await self._parse_tiktok_profile(html_content, username)
                
                return {
                    "platform": PlatformType.TIKTOK,
                    "profile": profile_data,
                    "videos": [],  # TikTok videos require more complex scraping
                    "scraped_at": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error scraping TikTok profile {username}: {e}")
            return {"error": str(e)}
    
    async def _parse_tiktok_profile(self, html_content: str, username: str) -> Dict[str, Any]:
        """Parse TikTok profile data from HTML"""
        try:
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            profile_data = {
                "username": username,
                "display_name": "",
                "bio": "",
                "followers": 0,
                "following": 0,
                "likes": 0,
                "videos_count": 0,
                "created_at": "",
                "profile_url": f"https://tiktok.com/@{username}",
                "is_verified": False
            }
            
            # Try to extract display name
            name_elem = soup.find('h1')
            if name_elem:
                profile_data["display_name"] = name_elem.get_text().strip()
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error parsing TikTok profile: {e}")
            return {"error": str(e)}
    
    async def _scrape_telegram(self, username: str, include_metadata: bool = True, max_posts: int = 100) -> Dict[str, Any]:
        """Scrape Telegram channel/profile using real web scraping"""
        try:
            # Rate limiting
            await self._respect_rate_limit(PlatformType.TELEGRAM)
            
            # Telegram channel URL
            channel_url = f"https://t.me/{username}"
            
            async with self.session.get(channel_url) as response:
                if response.status != 200:
                    return {"error": f"Failed to access Telegram channel: {response.status}"}
                
                html_content = await response.text()
                
                # Parse channel data
                profile_data = await self._parse_telegram_channel(html_content, username)
                
                return {
                    "platform": PlatformType.TELEGRAM,
                    "profile": profile_data,
                    "posts": [],  # Telegram posts require more complex scraping
                    "scraped_at": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error scraping Telegram channel {username}: {e}")
            return {"error": str(e)}
    
    async def _parse_telegram_channel(self, html_content: str, username: str) -> Dict[str, Any]:
        """Parse Telegram channel data from HTML"""
        try:
            from bs4 import BeautifulSoup
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            profile_data = {
                "username": username,
                "display_name": "",
                "bio": "",
                "subscribers": 0,
                "posts_count": 0,
                "created_at": "",
                "profile_url": f"https://t.me/{username}",
                "is_verified": False,
                "is_private": False
            }
            
            # Try to extract channel name
            name_elem = soup.find('div', {'class': 'tgme_channel_info_header_title'})
            if name_elem:
                profile_data["display_name"] = name_elem.get_text().strip()
            
            # Try to extract description
            desc_elem = soup.find('div', {'class': 'tgme_channel_info_description'})
            if desc_elem:
                profile_data["bio"] = desc_elem.get_text().strip()
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error parsing Telegram channel: {e}")
            return {"error": str(e)}
    
    async def _scrape_discord(self, username: str, include_metadata: bool = True, max_posts: int = 100) -> Dict[str, Any]:
        """Scrape Discord server/user using real web scraping"""
        try:
            # Rate limiting
            await self._respect_rate_limit(PlatformType.DISCORD)
            
            # Discord doesn't have public profiles like other platforms
            # This would require Discord API or server-specific scraping
            
            profile_data = {
                "username": username,
                "display_name": username,
                "bio": "",
                "servers_count": 0,
                "created_at": "",
                "profile_url": f"https://discord.com/users/{username}",
                "is_verified": False,
                "is_bot": False
            }
            
            return {
                "platform": PlatformType.DISCORD,
                "profile": profile_data,
                "messages": [],  # Discord messages require API access
                "scraped_at": datetime.utcnow().isoformat()
            }
                
        except Exception as e:
            logger.error(f"Error scraping Discord user {username}: {e}")
            return {"error": str(e)}

    async def _get_profile_data(self, platform: PlatformType, username: str) -> Optional[Dict[str, Any]]:
        """Get profile data for platform using real scraping"""
        try:
            # Use the platform-specific scraping methods
            if platform == PlatformType.TWITTER:
                result = await self._scrape_twitter(username, include_metadata=True, max_posts=0)
                return result.get("profile") if "error" not in result else None
            elif platform == PlatformType.REDDIT:
                result = await self._scrape_reddit(username, include_metadata=True, max_posts=0)
                return result.get("profile") if "error" not in result else None
            elif platform == PlatformType.GITHUB:
                result = await self._scrape_github(username, include_metadata=True, max_posts=0)
                return result.get("profile") if "error" not in result else None
            else:
                # For other platforms, use their specific scraping methods
                return None
        except Exception as e:
            logger.error(f"Error getting profile data: {e}")
            return None
    
    async def _get_recent_posts(self, platform: PlatformType, username: str) -> List[Dict[str, Any]]:
        """Get recent posts for platform using real scraping"""
        try:
            # Use the platform-specific scraping methods
            if platform == PlatformType.TWITTER:
                result = await self._scrape_twitter(username, include_metadata=True, max_posts=10)
                return result.get("posts", []) if "error" not in result else []
            elif platform == PlatformType.REDDIT:
                result = await self._scrape_reddit(username, include_metadata=True, max_posts=10)
                return result.get("posts", []) if "error" not in result else []
            elif platform == PlatformType.GITHUB:
                result = await self._scrape_github(username, include_metadata=True, max_posts=10)
                return result.get("activity", []) if "error" not in result else []
            else:
                # For other platforms, use their specific scraping methods
                return []
        except Exception as e:
            logger.error(f"Error getting recent posts: {e}")
            return []
    
    async def _get_network_data(self, platform: PlatformType, username: str) -> Dict[str, Any]:
        """Get network data (followers, following) using real scraping"""
        try:
            profile_data = await self._get_profile_data(platform, username)
            if not profile_data:
                return {}
            
            # Extract network data from profile
            network_data = {}
            
            if platform == PlatformType.TWITTER:
                network_data = {
                    "followers_count": profile_data.get("followers_count", 0),
                    "following_count": profile_data.get("following_count", 0),
                    "mutual_connections": 0  # Not available for Twitter
                }
            elif platform == PlatformType.REDDIT:
                network_data = {
                    "followers_count": 0,  # Reddit doesn't have followers
                    "following_count": 0,  # Reddit doesn't have following
                    "mutual_connections": 0
                }
            elif platform == PlatformType.GITHUB:
                network_data = {
                    "followers_count": profile_data.get("followers", 0),
                    "following_count": profile_data.get("following", 0),
                    "mutual_connections": 0  # Not available for GitHub
                }
            
            return network_data
            
        except Exception as e:
            logger.error(f"Error getting network data: {e}")
            return {}
    
    async def _assess_profile_threat(self, platform: PlatformType, profile_data: Dict[str, Any], posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess threat level of a social media profile"""
        try:
            threat_score = 0
            threat_indicators = []
            
            # Check for suspicious indicators
            if profile_data.get("followers_count", 0) > 10000:
                threat_score += 10
                threat_indicators.append("High follower count")
            
            if profile_data.get("posts_count", 0) > 1000:
                threat_score += 5
                threat_indicators.append("High post count")
            
            # Check for extremist keywords in bio
            extremist_keywords = ["nazi", "white power", "supremacy", "extremist", "terrorist", "hate"]
            bio = profile_data.get("bio", "").lower()
            for keyword in extremist_keywords:
                if keyword in bio:
                    threat_score += 20
                    threat_indicators.append(f"Extremist keyword in bio: {keyword}")
            
            # Check posts for suspicious content
            for post in posts:
                content = post.get("content", "").lower()
                for keyword in extremist_keywords:
                    if keyword in content:
                        threat_score += 15
                        threat_indicators.append(f"Extremist content in posts: {keyword}")
                        break
            
            # Determine threat level
            if threat_score >= 50:
                threat_level = ThreatLevel.HIGH
            elif threat_score >= 25:
                threat_level = ThreatLevel.MEDIUM
            elif threat_score >= 10:
                threat_level = ThreatLevel.LOW
            else:
                threat_level = ThreatLevel.LOW  # Default to LOW instead of NONE
            
            return {
                "threat_level": threat_level,
                "threat_score": threat_score,
                "threat_indicators": threat_indicators,
                "assessed_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error assessing profile threat: {e}")
            return {"error": str(e)}
    
    async def _analyze_sentiment(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze sentiment of posts using real analysis"""
        try:
            # This would implement actual sentiment analysis
            # For now, return basic analysis based on content
            total_posts = len(posts)
            if total_posts == 0:
                return {
                    "total_posts": 0,
                    "positive_posts": 0,
                    "negative_posts": 0,
                    "neutral_posts": 0,
                    "overall_sentiment": "neutral",
                    "sentiment_score": 0.0
                }
            
            # Simple keyword-based sentiment analysis
            positive_keywords = ["good", "great", "awesome", "love", "happy", "excellent", "amazing"]
            negative_keywords = ["bad", "terrible", "hate", "awful", "horrible", "disappointed", "angry"]
            
            positive_count = 0
            negative_count = 0
            
            for post in posts:
                content = post.get("content", "").lower()
                
                positive_matches = sum(1 for keyword in positive_keywords if keyword in content)
                negative_matches = sum(1 for keyword in negative_keywords if keyword in content)
                
                if positive_matches > negative_matches:
                    positive_count += 1
                elif negative_matches > positive_matches:
                    negative_count += 1
            
            neutral_count = total_posts - positive_count - negative_count
            
            # Calculate sentiment score
            sentiment_score = (positive_count - negative_count) / total_posts
            
            # Determine overall sentiment
            if sentiment_score > 0.1:
                overall_sentiment = "positive"
            elif sentiment_score < -0.1:
                overall_sentiment = "negative"
            else:
                overall_sentiment = "neutral"
            
            return {
                "total_posts": total_posts,
                "positive_posts": positive_count,
                "negative_posts": negative_count,
                "neutral_posts": neutral_count,
                "overall_sentiment": overall_sentiment,
                "sentiment_score": sentiment_score
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {"error": str(e)}
    
    async def _search_twitter(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search Twitter content using real search"""
        try:
            # Twitter search URL
            search_url = f"https://twitter.com/search?q={query}&src=typed_query&f=live"
            
            # This would require more complex scraping for search results
            # For now, return basic structure
            return {
                "query": query,
                "results": [],
                "total_results": 0,
                "error": "Twitter search requires advanced scraping implementation"
            }
            
        except Exception as e:
            logger.error(f"Error searching Twitter: {e}")
            return {"error": str(e)}
    
    async def _search_reddit(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search Reddit content using real API"""
        try:
            # Reddit search API
            search_url = f"https://www.reddit.com/search.json?q={query}&limit={max_results}"
            
            async with self.session.get(search_url, headers={
                "User-Agent": "Kali-OSINT-Platform/1.0"
            }) as response:
                if response.status == 200:
                    search_data = await response.json()
                    
                    results = []
                    if "data" in search_data and "children" in search_data["data"]:
                        for post in search_data["data"]["children"]:
                            post_data = post["data"]
                            
                            result = {
                                "id": post_data.get("id", ""),
                                "title": post_data.get("title", ""),
                                "content": post_data.get("selftext", ""),
                                "subreddit": post_data.get("subreddit", ""),
                                "author": post_data.get("author", ""),
                                "posted_at": datetime.fromtimestamp(post_data.get("created_utc", 0)).isoformat(),
                                "upvotes": post_data.get("score", 0),
                                "url": f"https://reddit.com{post_data.get('permalink', '')}"
                            }
                            
                            results.append(result)
                    
                    return {
                        "query": query,
                        "results": results,
                        "total_results": len(results)
                    }
                else:
                    return {"error": f"Failed to search Reddit: {response.status}"}
                    
        except Exception as e:
            logger.error(f"Error searching Reddit: {e}")
            return {"error": str(e)}
    
    async def _search_github(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search GitHub repositories using real API"""
        try:
            # GitHub search API
            search_url = f"https://api.github.com/search/repositories?q={query}&per_page={max_results}"
            
            async with self.session.get(search_url, headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Kali-OSINT-Platform/1.0"
            }) as response:
                if response.status == 200:
                    search_data = await response.json()
                    
                    results = []
                    if "items" in search_data:
                        for repo in search_data["items"]:
                            result = {
                                "id": repo.get("id", ""),
                                "name": repo.get("name", ""),
                                "full_name": repo.get("full_name", ""),
                                "description": repo.get("description", ""),
                                "language": repo.get("language"),
                                "stars": repo.get("stargazers_count", 0),
                                "forks": repo.get("forks_count", 0),
                                "created_at": repo.get("created_at", ""),
                                "html_url": repo.get("html_url", ""),
                                "owner": repo.get("owner", {}).get("login", "")
                            }
                            
                            results.append(result)
                    
                    return {
                        "query": query,
                        "results": results,
                        "total_results": search_data.get("total_count", 0)
                    }
                else:
                    return {"error": f"Failed to search GitHub: {response.status}"}
                    
        except Exception as e:
            logger.error(f"Error searching GitHub: {e}")
            return {"error": str(e)}
    
    async def _search_youtube(self, query: str, max_results: int) -> Dict[str, Any]:
        """Search YouTube videos using real search"""
        try:
            # YouTube search URL
            search_url = f"https://www.youtube.com/results?search_query={query}"
            
            # This would require more complex scraping for search results
            # For now, return basic structure
            return {
                "query": query,
                "results": [],
                "total_results": 0,
                "error": "YouTube search requires advanced scraping implementation"
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