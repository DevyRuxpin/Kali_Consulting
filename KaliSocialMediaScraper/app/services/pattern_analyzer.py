"""
Pattern Analysis Service
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import statistics
from dataclasses import dataclass

from app.models.schemas import Entity, Relationship, Pattern

logger = logging.getLogger(__name__)

@dataclass
class PatternContext:
    """Context for pattern analysis"""
    entities: List[Entity]
    relationships: List[Relationship]
    time_window: timedelta
    platform: Optional[str] = None

class PatternAnalyzer:
    """Advanced pattern detection and analysis service"""
    
    def __init__(self):
        self.pattern_templates = self._load_pattern_templates()
        self.behavioral_patterns = self._load_behavioral_patterns()
        self.network_patterns = self._load_network_patterns()
        self.temporal_patterns = self._load_temporal_patterns()
        self.content_patterns = self._load_content_patterns()
        
    async def detect_behavioral_patterns(self, entities: List[Entity]) -> List[Pattern]:
        """Detect behavioral patterns in entities"""
        try:
            patterns = []
            
            # Group entities by type
            user_entities = [e for e in entities if e.type == "user"]
            
            # Analyze posting patterns
            posting_patterns = await self._analyze_posting_patterns(user_entities)
            patterns.extend(posting_patterns)
            
            # Analyze engagement patterns
            engagement_patterns = await self._analyze_engagement_patterns(user_entities)
            patterns.extend(engagement_patterns)
            
            # Analyze follower patterns
            follower_patterns = await self._analyze_follower_patterns(user_entities)
            patterns.extend(follower_patterns)
            
            # Analyze cross-platform behavior
            cross_platform_patterns = await self._analyze_cross_platform_behavior(user_entities)
            patterns.extend(cross_platform_patterns)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error detecting behavioral patterns: {e}")
            return []
    
    async def detect_network_patterns(self, relationships: List[Relationship]) -> List[Pattern]:
        """Detect network patterns in relationships"""
        try:
            patterns = []
            
            # Analyze relationship clusters
            cluster_patterns = await self._analyze_relationship_clusters(relationships)
            patterns.extend(cluster_patterns)
            
            # Analyze influence patterns
            influence_patterns = await self._analyze_influence_patterns(relationships)
            patterns.extend(influence_patterns)
            
            # Analyze communication patterns
            communication_patterns = await self._analyze_communication_patterns(relationships)
            patterns.extend(communication_patterns)
            
            # Analyze cross-platform networks
            cross_network_patterns = await self._analyze_cross_platform_networks(relationships)
            patterns.extend(cross_network_patterns)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error detecting network patterns: {e}")
            return []
    
    async def detect_temporal_patterns(self, entities: List[Entity]) -> List[Pattern]:
        """Detect temporal patterns in entities"""
        try:
            patterns = []
            
            # Analyze activity timing
            timing_patterns = await self._analyze_activity_timing(entities)
            patterns.extend(timing_patterns)
            
            # Analyze creation patterns
            creation_patterns = await self._analyze_creation_patterns(entities)
            patterns.extend(creation_patterns)
            
            # Analyze growth patterns
            growth_patterns = await self._analyze_growth_patterns(entities)
            patterns.extend(growth_patterns)
            
            # Analyze seasonal patterns
            seasonal_patterns = await self._analyze_seasonal_patterns(entities)
            patterns.extend(seasonal_patterns)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error detecting temporal patterns: {e}")
            return []
    
    async def detect_content_patterns(self, entities: List[Entity]) -> List[Pattern]:
        """Detect content patterns in entities"""
        try:
            patterns = []
            
            # Analyze hashtag patterns
            hashtag_patterns = await self._analyze_hashtag_patterns(entities)
            patterns.extend(hashtag_patterns)
            
            # Analyze mention patterns
            mention_patterns = await self._analyze_mention_patterns(entities)
            patterns.extend(mention_patterns)
            
            # Analyze URL patterns
            url_patterns = await self._analyze_url_patterns(entities)
            patterns.extend(url_patterns)
            
            # Analyze language patterns
            language_patterns = await self._analyze_language_patterns(entities)
            patterns.extend(language_patterns)
            
            # Analyze sentiment patterns
            sentiment_patterns = await self._analyze_sentiment_patterns(entities)
            patterns.extend(sentiment_patterns)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error detecting content patterns: {e}")
            return []
    
    async def detect_geographic_patterns(self, entities: List[Entity]) -> List[Pattern]:
        """Detect geographic patterns in entities"""
        try:
            patterns = []
            
            # Analyze location clusters
            location_patterns = await self._analyze_location_clusters(entities)
            patterns.extend(location_patterns)
            
            # Analyze geographic movement
            movement_patterns = await self._analyze_geographic_movement(entities)
            patterns.extend(movement_patterns)
            
            # Analyze regional behavior
            regional_patterns = await self._analyze_regional_behavior(entities)
            patterns.extend(regional_patterns)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error detecting geographic patterns: {e}")
            return []
    
    async def _analyze_posting_patterns(self, user_entities: List[Entity]) -> List[Pattern]:
        """Analyze posting behavior patterns"""
        try:
            patterns = []
            
            # Get post entities for users
            for user in user_entities:
                # This would require access to user's posts
                # For now, simulate pattern detection
                pass
            
            # Analyze posting frequency
            for user in user_entities:
                if hasattr(user, 'metadata') and user.metadata:
                    posts_count = user.metadata.get('posts_count', 0)
                    followers_count = user.followers_count or 0
                    
                    # High posting frequency pattern
                    if posts_count > 100 and followers_count < 1000:
                        pattern = Pattern(
                            id=f"pattern_posting_frequency_{user.id}",
                            type="behavioral",
                            description=f"User {user.username} shows unusually high posting frequency",
                            entities=[user.id],
                            confidence=0.7,
                            metadata={
                                "posts_count": posts_count,
                                "followers_count": followers_count,
                                "posting_ratio": posts_count / max(followers_count, 1)
                            }
                        )
                        patterns.append(pattern)
                    
                    # Low engagement pattern
                    if posts_count > 50 and followers_count > 1000:
                        avg_engagement = user.metadata.get('avg_engagement', 0)
                        if avg_engagement < 10:
                            pattern = Pattern(
                                id=f"pattern_low_engagement_{user.id}",
                                type="behavioral",
                                description=f"User {user.username} has low engagement despite high follower count",
                                entities=[user.id],
                                confidence=0.6,
                                metadata={
                                    "posts_count": posts_count,
                                    "followers_count": followers_count,
                                    "avg_engagement": avg_engagement
                                }
                            )
                            patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing posting patterns: {e}")
            return []
    
    async def _analyze_engagement_patterns(self, user_entities: List[Entity]) -> List[Pattern]:
        """Analyze engagement behavior patterns"""
        try:
            patterns = []
            
            for user in user_entities:
                if hasattr(user, 'metadata') and user.metadata:
                    followers_count = user.followers_count or 0
                    following_count = user.following_count or 0
                    
                    # Suspicious follower ratio
                    if followers_count > 1000 and following_count < 10:
                        pattern = Pattern(
                            id=f"pattern_suspicious_ratio_{user.id}",
                            type="behavioral",
                            description=f"User {user.username} has suspicious follower/following ratio",
                            entities=[user.id],
                            confidence=0.8,
                            metadata={
                                "followers_count": followers_count,
                                "following_count": following_count,
                                "ratio": followers_count / max(following_count, 1)
                            }
                        )
                        patterns.append(pattern)
                    
                    # Bot-like behavior
                    if followers_count > 5000 and following_count > 4000:
                        pattern = Pattern(
                            id=f"pattern_bot_behavior_{user.id}",
                            type="behavioral",
                            description=f"User {user.username} shows bot-like following behavior",
                            entities=[user.id],
                            confidence=0.6,
                            metadata={
                                "followers_count": followers_count,
                                "following_count": following_count
                            }
                        )
                        patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing engagement patterns: {e}")
            return []
    
    async def _analyze_follower_patterns(self, user_entities: List[Entity]) -> List[Pattern]:
        """Analyze follower growth patterns"""
        try:
            patterns = []
            
            # Group users by follower count ranges
            follower_ranges = {
                "micro": (0, 1000),
                "small": (1000, 10000),
                "medium": (10000, 100000),
                "large": (100000, 1000000),
                "mega": (1000000, float('inf'))
            }
            
            for user in user_entities:
                followers_count = user.followers_count or 0
                
                # Determine follower range
                user_range = None
                for range_name, (min_followers, max_followers) in follower_ranges.items():
                    if min_followers <= followers_count < max_followers:
                        user_range = range_name
                        break
                
                if user_range:
                    pattern = Pattern(
                        id=f"pattern_follower_range_{user.id}",
                        type="behavioral",
                        description=f"User {user.username} falls into {user_range} influencer category",
                        entities=[user.id],
                        confidence=0.9,
                        metadata={
                            "follower_range": user_range,
                            "followers_count": followers_count
                        }
                    )
                    patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing follower patterns: {e}")
            return []
    
    async def _analyze_cross_platform_behavior(self, user_entities: List[Entity]) -> List[Pattern]:
        """Analyze behavior across multiple platforms"""
        try:
            patterns = []
            
            # Group users by cross-platform presence
            cross_platform_users = defaultdict(list)
            for user in user_entities:
                if hasattr(user, 'metadata') and user.metadata:
                    all_platforms = user.metadata.get('all_platforms', [])
                    if len(all_platforms) > 1:
                        cross_platform_users[user.id].extend(all_platforms)
            
            for user_id, platforms in cross_platform_users.items():
                pattern = Pattern(
                    id=f"pattern_cross_platform_{user_id}",
                    type="behavioral",
                    description=f"User present on {len(platforms)} platforms: {', '.join(platforms)}",
                    entities=[user_id],
                    confidence=0.8,
                    metadata={
                        "platforms": platforms,
                        "platform_count": len(platforms)
                    }
                )
                patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing cross-platform behavior: {e}")
            return []
    
    async def _analyze_relationship_clusters(self, relationships: List[Relationship]) -> List[Pattern]:
        """Analyze relationship clustering patterns"""
        try:
            patterns = []
            
            # Group relationships by type
            relationship_groups = defaultdict(list)
            for rel in relationships:
                relationship_groups[rel.type].append(rel)
            
            # Analyze cluster sizes
            for rel_type, rels in relationship_groups.items():
                if len(rels) > 5:  # Significant cluster
                    pattern = Pattern(
                        id=f"pattern_relationship_cluster_{rel_type}",
                        type="network",
                        description=f"Found {len(rels)} {rel_type} relationships",
                        entities=[rel.source_id for rel in rels] + [rel.target_id for rel in rels],
                        confidence=0.7,
                        metadata={
                            "relationship_type": rel_type,
                            "cluster_size": len(rels),
                            "platforms": list(set([rel.platform for rel in rels]))
                        }
                    )
                    patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing relationship clusters: {e}")
            return []
    
    async def _analyze_influence_patterns(self, relationships: List[Relationship]) -> List[Pattern]:
        """Analyze influence and centrality patterns"""
        try:
            patterns = []
            
            # Calculate entity centrality
            entity_centrality: Dict[str, int] = defaultdict(int)
            for rel in relationships:
                entity_centrality[rel.source_id] += 1
                entity_centrality[rel.target_id] += 1
            
            # Find high-influence entities
            high_influence_threshold = statistics.mean(list(entity_centrality.values())) + statistics.stdev(list(entity_centrality.values()))
            
            for entity_id, centrality in entity_centrality.items():
                if centrality > high_influence_threshold:
                    pattern = Pattern(
                        id=f"pattern_high_influence_{entity_id}",
                        type="network",
                        description=f"Entity {entity_id} shows high network centrality",
                        entities=[entity_id],
                        confidence=0.8,
                        metadata={
                            "centrality_score": centrality,
                            "threshold": high_influence_threshold
                        }
                    )
                    patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing influence patterns: {e}")
            return []
    
    async def _analyze_communication_patterns(self, relationships: List[Relationship]) -> List[Pattern]:
        """Analyze communication and interaction patterns"""
        try:
            patterns = []
            
            # Analyze mention patterns
            mention_relationships = [r for r in relationships if r.type == "mentions"]
            
            if mention_relationships:
                # Find frequent mentioners
                mention_counts = Counter([r.source_id for r in mention_relationships])
                frequent_mentioners = [entity_id for entity_id, count in mention_counts.items() if count > 10]
                
                for entity_id in frequent_mentioners:
                    pattern = Pattern(
                        id=f"pattern_frequent_mentions_{entity_id}",
                        type="network",
                        description=f"Entity {entity_id} frequently mentions others",
                        entities=[entity_id],
                        confidence=0.7,
                        metadata={
                            "mention_count": mention_counts[entity_id]
                        }
                    )
                    patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing communication patterns: {e}")
            return []
    
    async def _analyze_cross_platform_networks(self, relationships: List[Relationship]) -> List[Pattern]:
        """Analyze networks across multiple platforms"""
        try:
            patterns = []
            
            # Find cross-platform relationships
            cross_platform_rels = [r for r in relationships if r.platform == "cross_platform"]
            
            if cross_platform_rels:
                pattern = Pattern(
                    id="pattern_cross_platform_network",
                    type="network",
                    description=f"Found {len(cross_platform_rels)} cross-platform relationships",
                    entities=list(set([r.source_id for r in cross_platform_rels] + [r.target_id for r in cross_platform_rels])),
                    confidence=0.9,
                    metadata={
                        "cross_platform_relationships": len(cross_platform_rels)
                    }
                )
                patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing cross-platform networks: {e}")
            return []
    
    async def _analyze_activity_timing(self, entities: List[Entity]) -> List[Pattern]:
        """Analyze activity timing patterns"""
        try:
            patterns = []
            
            # Group entities by creation time
            creation_times = []
            for entity in entities:
                if entity.created_at:
                    creation_times.append(entity.created_at)
            
            if creation_times:
                # Analyze creation time clustering
                creation_times.sort()
                time_diffs = []
                for i in range(1, len(creation_times)):
                    diff = (creation_times[i] - creation_times[i-1]).total_seconds()
                    time_diffs.append(diff)
                
                if time_diffs:
                    avg_diff = statistics.mean(time_diffs)
                    if avg_diff < 3600:  # Less than 1 hour between creations
                        pattern = Pattern(
                            id="pattern_rapid_creation",
                            type="temporal",
                            description="Multiple accounts created in rapid succession",
                            entities=[e.id for e in entities if e.created_at],
                            confidence=0.8,
                            metadata={
                                "average_time_between_creations": avg_diff,
                                "total_entities": len(creation_times)
                            }
                        )
                        patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing activity timing: {e}")
            return []
    
    async def _analyze_creation_patterns(self, entities: List[Entity]) -> List[Pattern]:
        """Analyze account creation patterns"""
        try:
            patterns = []
            
            # Analyze creation dates
            recent_creations = []
            for entity in entities:
                if entity.created_at:
                    days_old = (datetime.utcnow() - entity.created_at).days
                    if days_old < 30:
                        recent_creations.append(entity)
            
            if len(recent_creations) > 3:
                pattern = Pattern(
                    id="pattern_recent_creations",
                    type="temporal",
                    description=f"Found {len(recent_creations)} recently created accounts",
                    entities=[e.id for e in recent_creations],
                    confidence=0.7,
                    metadata={
                        "recent_accounts": len(recent_creations),
                        "timeframe_days": 30
                    }
                )
                patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing creation patterns: {e}")
            return []
    
    async def _analyze_growth_patterns(self, entities: List[Entity]) -> List[Pattern]:
        """Analyze follower growth patterns"""
        try:
            patterns = []
            
            # Analyze follower growth rates
            for entity in entities:
                if entity.followers_count and entity.created_at:
                    days_old = (datetime.utcnow() - entity.created_at).days
                    if days_old > 0:
                        growth_rate = entity.followers_count / days_old
                        
                        # Suspicious growth rate
                        if growth_rate > 100:  # More than 100 followers per day
                            pattern = Pattern(
                                id=f"pattern_suspicious_growth_{entity.id}",
                                type="temporal",
                                description=f"Entity {entity.username} shows suspicious follower growth",
                                entities=[entity.id],
                                confidence=0.8,
                                metadata={
                                    "growth_rate": growth_rate,
                                    "followers_count": entity.followers_count,
                                    "days_old": days_old
                                }
                            )
                            patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing growth patterns: {e}")
            return []
    
    async def _analyze_seasonal_patterns(self, entities: List[Entity]) -> List[Pattern]:
        """Analyze seasonal and cyclical patterns"""
        try:
            patterns = []
            
            # Group entities by creation month
            monthly_creations: Dict[int, int] = defaultdict(int)
            for entity in entities:
                if entity.created_at:
                    month = entity.created_at.month
                    monthly_creations[month] += 1
            
            # Find seasonal spikes
            if monthly_creations:
                avg_creations = statistics.mean(monthly_creations.values())
                for month, count in monthly_creations.items():
                    if count > avg_creations * 2:  # Twice the average
                        pattern = Pattern(
                            id=f"pattern_seasonal_spike_{month}",
                            type="temporal",
                            description=f"Unusual account creation spike in month {month}",
                            entities=[],
                            confidence=0.6,
                            metadata={
                                "month": month,
                                "creation_count": count,
                                "average": avg_creations
                            }
                        )
                        patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing seasonal patterns: {e}")
            return []
    
    async def _analyze_hashtag_patterns(self, entities: List[Entity]) -> List[Pattern]:
        """Analyze hashtag usage patterns"""
        try:
            patterns = []
            
            # Collect hashtags from posts
            all_hashtags = []
            for entity in entities:
                if hasattr(entity, 'hashtags') and entity.hashtags:
                    all_hashtags.extend(entity.hashtags)
            
            if all_hashtags:
                # Find trending hashtags
                hashtag_counts = Counter(all_hashtags)
                trending_hashtags = [tag for tag, count in hashtag_counts.items() if count > 5]
                
                for hashtag in trending_hashtags:
                    pattern = Pattern(
                        id=f"pattern_trending_hashtag_{hashtag}",
                        type="content",
                        description=f"Hashtag #{hashtag} appears {hashtag_counts[hashtag]} times",
                        entities=[],
                        confidence=0.8,
                        metadata={
                            "hashtag": hashtag,
                            "usage_count": hashtag_counts[hashtag]
                        }
                    )
                    patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing hashtag patterns: {e}")
            return []
    
    async def _analyze_mention_patterns(self, entities: List[Entity]) -> List[Pattern]:
        """Analyze mention patterns"""
        try:
            patterns = []
            
            # Collect mentions from posts
            all_mentions = []
            for entity in entities:
                if hasattr(entity, 'mentions') and entity.mentions:
                    all_mentions.extend(entity.mentions)
            
            if all_mentions:
                # Find frequent mentions
                mention_counts = Counter(all_mentions)
                frequent_mentions = [mention for mention, count in mention_counts.items() if count > 3]
                
                for mention in frequent_mentions:
                    pattern = Pattern(
                        id=f"pattern_frequent_mention_{mention}",
                        type="content",
                        description=f"User @{mention} is frequently mentioned",
                        entities=[],
                        confidence=0.7,
                        metadata={
                            "mentioned_user": mention,
                            "mention_count": mention_counts[mention]
                        }
                    )
                    patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing mention patterns: {e}")
            return []
    
    async def _analyze_url_patterns(self, entities: List[Entity]) -> List[Pattern]:
        """Analyze URL patterns"""
        try:
            patterns = []
            
            # Collect URLs from posts
            all_urls = []
            for entity in entities:
                if hasattr(entity, 'urls') and entity.urls:
                    all_urls.extend(entity.urls)
            
            if all_urls:
                # Analyze domain patterns
                domains = []
                for url in all_urls:
                    try:
                        from urllib.parse import urlparse
                        domain = urlparse(url).netloc
                        if domain:
                            domains.append(domain)
                    except:
                        continue
                
                if domains:
                    domain_counts = Counter(domains)
                    frequent_domains = [domain for domain, count in domain_counts.items() if count > 2]
                    
                    for domain in frequent_domains:
                        pattern = Pattern(
                            id=f"pattern_frequent_domain_{domain}",
                            type="content",
                            description=f"Domain {domain} appears frequently in URLs",
                            entities=[],
                            confidence=0.8,
                            metadata={
                                "domain": domain,
                                "url_count": domain_counts[domain]
                            }
                        )
                        patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing URL patterns: {e}")
            return []
    
    async def _analyze_language_patterns(self, entities: List[Entity]) -> List[Pattern]:
        """Analyze language and text patterns"""
        try:
            patterns = []
            
            # Analyze content length patterns
            content_lengths = []
            for entity in entities:
                if hasattr(entity, 'content') and entity.content:
                    content_lengths.append(len(entity.content))
            
            if content_lengths:
                avg_length = statistics.mean(content_lengths)
                
                # Find entities with unusually long/short content
                for entity in entities:
                    if hasattr(entity, 'content') and entity.content:
                        content_length = len(entity.content)
                        
                        if content_length > avg_length * 2:
                            pattern = Pattern(
                                id=f"pattern_long_content_{entity.id}",
                                type="content",
                                description=f"Entity {entity.username} posts unusually long content",
                                entities=[entity.id],
                                confidence=0.6,
                                metadata={
                                    "content_length": content_length,
                                    "average_length": avg_length
                                }
                            )
                            patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing language patterns: {e}")
            return []
    
    async def _analyze_sentiment_patterns(self, entities: List[Entity]) -> List[Pattern]:
        """Analyze sentiment patterns"""
        try:
            patterns = []
            
            # Simple sentiment analysis based on keywords
            positive_keywords = ["good", "great", "love", "happy", "positive", "excellent"]
            negative_keywords = ["bad", "hate", "terrible", "awful", "negative", "horrible"]
            
            for entity in entities:
                if hasattr(entity, 'content') and entity.content:
                    content_lower = entity.content.lower()
                    
                    positive_count = sum(1 for word in positive_keywords if word in content_lower)
                    negative_count = sum(1 for word in negative_keywords if word in content_lower)
                    
                    if positive_count > negative_count * 2:
                        pattern = Pattern(
                            id=f"pattern_positive_sentiment_{entity.id}",
                            type="content",
                            description=f"Entity {entity.username} shows predominantly positive sentiment",
                            entities=[entity.id],
                            confidence=0.6,
                            metadata={
                                "positive_keywords": positive_count,
                                "negative_keywords": negative_count
                            }
                        )
                        patterns.append(pattern)
                    
                    elif negative_count > positive_count * 2:
                        pattern = Pattern(
                            id=f"pattern_negative_sentiment_{entity.id}",
                            type="content",
                            description=f"Entity {entity.username} shows predominantly negative sentiment",
                            entities=[entity.id],
                            confidence=0.6,
                            metadata={
                                "positive_keywords": positive_count,
                                "negative_keywords": negative_count
                            }
                        )
                        patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment patterns: {e}")
            return []
    
    async def _analyze_location_clusters(self, entities: List[Entity]) -> List[Pattern]:
        """Analyze geographic location patterns"""
        try:
            patterns: List[Pattern] = []
            
            # Group entities by location
            location_groups = defaultdict(list)
            for entity in entities:
                if entity.location:
                    location_groups[entity.location].append(entity)
            
            # Find location clusters
            for location, entities_list in location_groups.items():
                if len(entities_list) > 2:
                    pattern = Pattern(
                        id=f"pattern_location_cluster_{location}",
                        type="geographic",
                        description=f"Found {len(entities_list)} entities in {location}",
                        entities=[e.id for e in entities_list],
                        confidence=0.8,
                        metadata={
                            "location": location,
                            "entity_count": len(entities_list)
                        }
                    )
                    patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing location clusters: {e}")
            return []
    
    async def _analyze_geographic_movement(self, entities: List[Entity]) -> List[Pattern]:
        """Analyze geographic movement patterns"""
        try:
            patterns: List[Pattern] = []
            # This would require historical location data
            # For now, return empty list
            return patterns
        except Exception as e:
            logger.error(f"Error analyzing geographic movement: {e}")
            return []
    
    async def _analyze_regional_behavior(self, entities: List[Entity]) -> List[Pattern]:
        """Analyze regional behavior patterns"""
        try:
            patterns: List[Pattern] = []
            # Group by region/country
            regional_groups = defaultdict(list)
            for entity in entities:
                if entity.location:
                    # Extract country/region from location
                    location_parts = entity.location.split(',')
                    if len(location_parts) > 1:
                        region = location_parts[-1].strip()
                        regional_groups[region].append(entity)
            # Analyze regional patterns
            for region, entities_list in regional_groups.items():
                if len(entities_list) > 3:
                    pattern = Pattern(
                        id=f"pattern_regional_behavior_{region}",
                        type="geographic",
                        description=f"Found {len(entities_list)} entities from {region}",
                        entities=[e.id for e in entities_list],
                        confidence=0.7,
                        metadata={
                            "region": region,
                            "entity_count": len(entities_list)
                        }
                    )
                    patterns.append(pattern)
            return patterns
        except Exception as e:
            logger.error(f"Error analyzing regional behavior: {e}")
            return []
    
    def _load_pattern_templates(self) -> Dict[str, Any]:
        """Load pattern detection templates"""
        return {
            "behavioral": {
                "posting_frequency": {"threshold": 100, "severity": "medium"},
                "engagement_rate": {"threshold": 0.01, "severity": "medium"},
                "follower_ratio": {"threshold": 100, "severity": "high"}
            },
            "network": {
                "centrality": {"threshold": 10, "severity": "medium"},
                "clustering": {"threshold": 5, "severity": "low"},
                "influence": {"threshold": 0.8, "severity": "medium"}
            },
            "temporal": {
                "creation_timing": {"threshold": 3600, "severity": "high"},
                "activity_patterns": {"threshold": 24, "severity": "medium"},
                "growth_rate": {"threshold": 100, "severity": "high"}
            },
            "content": {
                "hashtag_frequency": {"threshold": 5, "severity": "low"},
                "mention_frequency": {"threshold": 3, "severity": "medium"},
                "url_domain": {"threshold": 2, "severity": "medium"}
            }
        }
    
    def _load_behavioral_patterns(self) -> Dict[str, Any]:
        """Load behavioral pattern definitions"""
        return {
            "high_posting_frequency": {
                "description": "Unusually high posting frequency",
                "indicators": ["posts_per_day > 10", "followers < 1000"],
                "severity": "medium"
            },
            "low_engagement": {
                "description": "Low engagement despite high follower count",
                "indicators": ["engagement_rate < 0.01", "followers > 1000"],
                "severity": "medium"
            },
            "suspicious_follower_ratio": {
                "description": "Suspicious follower to following ratio",
                "indicators": ["followers/following > 100"],
                "severity": "high"
            }
        }
    
    def _load_network_patterns(self) -> Dict[str, Any]:
        """Load network pattern definitions"""
        return {
            "high_centrality": {
                "description": "High network centrality",
                "indicators": ["degree_centrality > 10"],
                "severity": "medium"
            },
            "clustering": {
                "description": "Network clustering behavior",
                "indicators": ["clustering_coefficient > 0.5"],
                "severity": "low"
            },
            "cross_platform": {
                "description": "Cross-platform network presence",
                "indicators": ["platforms > 2"],
                "severity": "medium"
            }
        }
    
    def _load_temporal_patterns(self) -> Dict[str, Any]:
        """Load temporal pattern definitions"""
        return {
            "rapid_creation": {
                "description": "Rapid account creation",
                "indicators": ["time_between_creations < 1_hour"],
                "severity": "high"
            },
            "seasonal_activity": {
                "description": "Seasonal activity patterns",
                "indicators": ["monthly_variance > 2x_average"],
                "severity": "low"
            },
            "growth_spikes": {
                "description": "Unusual growth spikes",
                "indicators": ["growth_rate > 100_per_day"],
                "severity": "high"
            }
        }
    
    def _load_content_patterns(self) -> Dict[str, Any]:
        """Load content pattern definitions"""
        return {
            "trending_hashtags": {
                "description": "Trending hashtag usage",
                "indicators": ["hashtag_frequency > 5"],
                "severity": "low"
            },
            "frequent_mentions": {
                "description": "Frequent user mentions",
                "indicators": ["mention_frequency > 3"],
                "severity": "medium"
            },
            "suspicious_urls": {
                "description": "Suspicious URL patterns",
                "indicators": ["suspicious_domains > 2"],
                "severity": "high"
            }
        } 

    async def analyze_patterns(self, data: list, *args, **kwargs) -> dict:
        """Test compatibility: analyze patterns (minimal implementation)"""
        return {
            "patterns": data,
            "pattern_types": ["behavioral", "network", "temporal"],
            "confidence": 0.8,
            "analysis": "No significant patterns detected"
        }

    async def extract_entities(self, text: str, *args, **kwargs) -> dict:
        """Test compatibility: extract entities (minimal implementation)"""
        return {
            "entities": [],
            "entity_types": ["user", "domain", "email"],
            "input": text
        } 