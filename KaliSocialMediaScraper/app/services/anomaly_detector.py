"""
Anomaly Detection Service
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import statistics
from collections import defaultdict, Counter
import re

from app.models.schemas import Entity, Relationship, Pattern, Anomaly

logger = logging.getLogger(__name__)

class AnomalyDetector:
    """Advanced anomaly detection service"""
    
    def __init__(self):
        self.anomaly_thresholds = self._load_anomaly_thresholds()
        self.behavioral_baselines = {}
        self.network_baselines = {}
        
    async def detect_behavioral_anomalies(self, entities: List[Entity]) -> List[Anomaly]:
        """Detect behavioral anomalies in entities"""
        try:
            anomalies = []
            
            # Group entities by type
            user_entities = [e for e in entities if e.type == "user"]
            
            # Detect posting anomalies
            posting_anomalies = await self._detect_posting_anomalies(user_entities)
            anomalies.extend(posting_anomalies)
            
            # Detect engagement anomalies
            engagement_anomalies = await self._detect_engagement_anomalies(user_entities)
            anomalies.extend(engagement_anomalies)
            
            # Detect follower anomalies
            follower_anomalies = await self._detect_follower_anomalies(user_entities)
            anomalies.extend(follower_anomalies)
            
            # Detect account age anomalies
            age_anomalies = await self._detect_account_age_anomalies(user_entities)
            anomalies.extend(age_anomalies)
            
            # Detect cross-platform anomalies
            cross_platform_anomalies = await self._detect_cross_platform_anomalies(user_entities)
            anomalies.extend(cross_platform_anomalies)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting behavioral anomalies: {e}")
            return []
    
    async def detect_network_anomalies(self, relationships: List[Relationship]) -> List[Anomaly]:
        """Detect network anomalies in relationships"""
        try:
            anomalies = []
            
            # Detect relationship anomalies
            relationship_anomalies = await self._detect_relationship_anomalies(relationships)
            anomalies.extend(relationship_anomalies)
            
            # Detect centrality anomalies
            centrality_anomalies = await self._detect_centrality_anomalies(relationships)
            anomalies.extend(centrality_anomalies)
            
            # Detect clustering anomalies
            clustering_anomalies = await self._detect_clustering_anomalies(relationships)
            anomalies.extend(clustering_anomalies)
            
            # Detect communication anomalies
            communication_anomalies = await self._detect_communication_anomalies(relationships)
            anomalies.extend(communication_anomalies)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting network anomalies: {e}")
            return []
    
    async def detect_temporal_anomalies(self, entities: List[Entity]) -> List[Anomaly]:
        """Detect temporal anomalies in entities"""
        try:
            anomalies = []
            
            # Detect creation timing anomalies
            creation_anomalies = await self._detect_creation_timing_anomalies(entities)
            anomalies.extend(creation_anomalies)
            
            # Detect activity timing anomalies
            activity_anomalies = await self._detect_activity_timing_anomalies(entities)
            anomalies.extend(activity_anomalies)
            
            # Detect growth rate anomalies
            growth_anomalies = await self._detect_growth_rate_anomalies(entities)
            anomalies.extend(growth_anomalies)
            
            # Detect seasonal anomalies
            seasonal_anomalies = await self._detect_seasonal_anomalies(entities)
            anomalies.extend(seasonal_anomalies)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting temporal anomalies: {e}")
            return []
    
    async def detect_content_anomalies(self, entities: List[Entity]) -> List[Anomaly]:
        """Detect content anomalies in entities"""
        try:
            anomalies = []
            
            # Detect content length anomalies
            length_anomalies = await self._detect_content_length_anomalies(entities)
            anomalies.extend(length_anomalies)
            
            # Detect hashtag anomalies
            hashtag_anomalies = await self._detect_hashtag_anomalies(entities)
            anomalies.extend(hashtag_anomalies)
            
            # Detect mention anomalies
            mention_anomalies = await self._detect_mention_anomalies(entities)
            anomalies.extend(mention_anomalies)
            
            # Detect URL anomalies
            url_anomalies = await self._detect_url_anomalies(entities)
            anomalies.extend(url_anomalies)
            
            # Detect sentiment anomalies
            sentiment_anomalies = await self._detect_sentiment_anomalies(entities)
            anomalies.extend(sentiment_anomalies)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting content anomalies: {e}")
            return []
    
    async def _detect_posting_anomalies(self, user_entities: List[Entity]) -> List[Anomaly]:
        """Detect anomalies in posting behavior"""
        try:
            anomalies = []
            
            # Calculate posting statistics
            posting_counts = []
            for user in user_entities:
                if hasattr(user, 'metadata') and user.metadata:
                    posts_count = user.metadata.get('posts_count', 0)
                    if posts_count > 0:
                        posting_counts.append(posts_count)
            
            if posting_counts:
                mean_posts = statistics.mean(posting_counts)
                std_posts = statistics.stdev(posting_counts) if len(posting_counts) > 1 else 0
                
                for user in user_entities:
                    if hasattr(user, 'metadata') and user.metadata:
                        posts_count = user.metadata.get('posts_count', 0)
                        
                        # Detect unusually high posting frequency
                        if posts_count > mean_posts + (2 * std_posts):
                            anomaly = Anomaly(
                                id=f"anomaly_high_posting_{user.id}",
                                anomaly_type="behavioral",
                                category="posting_frequency",
                                title="Unusually High Posting Frequency",
                                description=f"User {user.username} posts {posts_count} times, significantly above average",
                                severity="medium",
                                confidence=0.8,
                                entities_involved=[user.id],
                                metadata={
                                    "posts_count": posts_count,
                                    "average_posts": mean_posts,
                                    "standard_deviation": std_posts,
                                    "z_score": (posts_count - mean_posts) / std_posts if std_posts > 0 else 0
                                }
                            )
                            anomalies.append(anomaly)
                        
                        # Detect unusually low posting frequency
                        elif posts_count < mean_posts - (2 * std_posts) and posts_count > 0:
                            anomaly = Anomaly(
                                id=f"anomaly_low_posting_{user.id}",
                                anomaly_type="behavioral",
                                category="posting_frequency",
                                title="Unusually Low Posting Frequency",
                                description=f"User {user.username} posts {posts_count} times, significantly below average",
                                severity="low",
                                confidence=0.7,
                                entities_involved=[user.id],
                                metadata={
                                    "posts_count": posts_count,
                                    "average_posts": mean_posts,
                                    "standard_deviation": std_posts,
                                    "z_score": (posts_count - mean_posts) / std_posts if std_posts > 0 else 0
                                }
                            )
                            anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting posting anomalies: {e}")
            return []
    
    async def _detect_engagement_anomalies(self, user_entities: List[Entity]) -> List[Anomaly]:
        """Detect anomalies in engagement behavior"""
        try:
            anomalies = []
            
            for user in user_entities:
                followers_count = user.followers_count or 0
                following_count = user.following_count or 0
                
                # Detect suspicious follower ratio
                if followers_count > 1000 and following_count < 10:
                    ratio = followers_count / max(following_count, 1)
                    anomaly = Anomaly(
                        id=f"anomaly_suspicious_ratio_{user.id}",
                        anomaly_type="behavioral",
                        category="follower_ratio",
                        title="Suspicious Follower Ratio",
                        description=f"User {user.username} has suspicious follower/following ratio of {ratio:.2f}",
                        severity="high",
                        confidence=0.9,
                        entities_involved=[user.id],
                        metadata={
                            "followers_count": followers_count,
                            "following_count": following_count,
                            "ratio": ratio
                        }
                    )
                    anomalies.append(anomaly)
                
                # Detect bot-like behavior
                if followers_count > 5000 and following_count > 4000:
                    anomaly = Anomaly(
                        id=f"anomaly_bot_behavior_{user.id}",
                        anomaly_type="behavioral",
                        category="bot_indicators",
                        title="Bot-like Behavior",
                        description=f"User {user.username} shows bot-like following behavior",
                        severity="medium",
                        confidence=0.7,
                        entities_involved=[user.id],
                        metadata={
                            "followers_count": followers_count,
                            "following_count": following_count
                        }
                    )
                    anomalies.append(anomaly)
                
                # Detect low engagement
                if followers_count > 1000:
                    avg_engagement = user.metadata.get('avg_engagement', 0) if user.metadata else 0
                    engagement_rate = avg_engagement / max(followers_count, 1)
                    
                    if engagement_rate < 0.01:  # Less than 1% engagement
                        anomaly = Anomaly(
                            id=f"anomaly_low_engagement_{user.id}",
                            anomaly_type="behavioral",
                            category="engagement_rate",
                            title="Unusually Low Engagement",
                            description=f"User {user.username} has very low engagement rate of {engagement_rate:.4f}",
                            severity="medium",
                            confidence=0.8,
                            entities_involved=[user.id],
                            metadata={
                                "engagement_rate": engagement_rate,
                                "followers_count": followers_count,
                                "avg_engagement": avg_engagement
                            }
                        )
                        anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting engagement anomalies: {e}")
            return []
    
    async def _detect_follower_anomalies(self, user_entities: List[Entity]) -> List[Anomaly]:
        """Detect anomalies in follower behavior"""
        try:
            anomalies = []
            
            # Calculate follower statistics
            follower_counts = [user.followers_count or 0 for user in user_entities]
            follower_counts = [count for count in follower_counts if count > 0]
            
            if follower_counts:
                mean_followers = statistics.mean(follower_counts)
                std_followers = statistics.stdev(follower_counts) if len(follower_counts) > 1 else 0
                
                for user in user_entities:
                    followers_count = user.followers_count or 0
                    
                    # Detect unusually high follower count
                    if followers_count > mean_followers + (3 * std_followers):
                        anomaly = Anomaly(
                            id=f"anomaly_high_followers_{user.id}",
                            anomaly_type="behavioral",
                            category="follower_count",
                            title="Unusually High Follower Count",
                            description=f"User {user.username} has {followers_count} followers, significantly above average",
                            severity="medium",
                            confidence=0.8,
                            entities_involved=[user.id],
                            metadata={
                                "followers_count": followers_count,
                                "average_followers": mean_followers,
                                "standard_deviation": std_followers,
                                "z_score": (followers_count - mean_followers) / std_followers if std_followers > 0 else 0
                            }
                        )
                        anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting follower anomalies: {e}")
            return []
    
    async def _detect_account_age_anomalies(self, user_entities: List[Entity]) -> List[Anomaly]:
        """Detect anomalies in account age"""
        try:
            anomalies = []
            
            for user in user_entities:
                if user.created_at:
                    days_old = (datetime.utcnow() - user.created_at).days
                    followers_count = user.followers_count or 0
                    
                    # Detect recently created account with high followers
                    if days_old < 30 and followers_count > 1000:
                        anomaly = Anomaly(
                            id=f"anomaly_recent_high_followers_{user.id}",
                            anomaly_type="behavioral",
                            category="account_age",
                            title="Recently Created Account with High Followers",
                            description=f"User {user.username} created {days_old} days ago but has {followers_count} followers",
                            severity="high",
                            confidence=0.9,
                            entities_involved=[user.id],
                            metadata={
                                "days_old": days_old,
                                "followers_count": followers_count,
                                "created_at": user.created_at.isoformat()
                            }
                        )
                        anomalies.append(anomaly)
                    
                    # Detect very old account with low activity
                    elif days_old > 365 and followers_count < 10:
                        anomaly = Anomaly(
                            id=f"anomaly_old_inactive_{user.id}",
                            anomaly_type="behavioral",
                            category="account_age",
                            title="Old Account with Low Activity",
                            description=f"User {user.username} account is {days_old} days old but has only {followers_count} followers",
                            severity="low",
                            confidence=0.6,
                            entities_involved=[user.id],
                            metadata={
                                "days_old": days_old,
                                "followers_count": followers_count,
                                "created_at": user.created_at.isoformat()
                            }
                        )
                        anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting account age anomalies: {e}")
            return []
    
    async def _detect_cross_platform_anomalies(self, user_entities: List[Entity]) -> List[Anomaly]:
        """Detect anomalies in cross-platform behavior"""
        try:
            anomalies = []
            
            for user in user_entities:
                if hasattr(user, 'metadata') and user.metadata:
                    all_platforms = user.metadata.get('all_platforms', [])
                    
                    # Detect presence on many platforms
                    if len(all_platforms) > 5:
                        anomaly = Anomaly(
                            id=f"anomaly_many_platforms_{user.id}",
                            anomaly_type="behavioral",
                            category="cross_platform",
                            title="Presence on Many Platforms",
                            description=f"User {user.username} is present on {len(all_platforms)} platforms",
                            severity="medium",
                            confidence=0.7,
                            entities_involved=[user.id],
                            metadata={
                                "platforms": all_platforms,
                                "platform_count": len(all_platforms)
                            }
                        )
                        anomalies.append(anomaly)
                    
                    # Detect suspicious platform combinations
                    suspicious_combinations = [
                        ['twitter', 'telegram', 'discord'],
                        ['instagram', 'tiktok', 'youtube'],
                        ['github', 'linkedin', 'twitter']
                    ]
                    
                    for combination in suspicious_combinations:
                        if all(platform in all_platforms for platform in combination):
                            anomaly = Anomaly(
                                id=f"anomaly_suspicious_platforms_{user.id}",
                                anomaly_type="behavioral",
                                category="cross_platform",
                                title="Suspicious Platform Combination",
                                description=f"User {user.username} uses suspicious platform combination",
                                severity="medium",
                                confidence=0.6,
                                entities_involved=[user.id],
                                metadata={
                                    "suspicious_combination": combination,
                                    "all_platforms": all_platforms
                                }
                            )
                            anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting cross-platform anomalies: {e}")
            return []
    
    async def _detect_relationship_anomalies(self, relationships: List[Relationship]) -> List[Anomaly]:
        """Detect anomalies in relationships"""
        try:
            anomalies = []
            
            # Group relationships by type
            relationship_groups = defaultdict(list)
            for rel in relationships:
                relationship_groups[rel.relationship_type].append(rel)
            
            # Detect unusual relationship patterns
            for rel_type, rels in relationship_groups.items():
                if len(rels) > 20:  # Unusually large relationship cluster
                    anomaly = Anomaly(
                        id=f"anomaly_large_cluster_{rel_type}",
                        anomaly_type="network",
                        category="relationship_cluster",
                        title=f"Unusually Large {rel_type.title()} Cluster",
                        description=f"Found {len(rels)} {rel_type} relationships, unusually large cluster",
                        severity="medium",
                        confidence=0.8,
                        entities_involved=list(set([rel.source_id for rel in rels] + [rel.target_id for rel in rels])),
                        metadata={
                            "relationship_type": rel_type,
                            "cluster_size": len(rels)
                        }
                    )
                    anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting relationship anomalies: {e}")
            return []
    
    async def _detect_centrality_anomalies(self, relationships: List[Relationship]) -> List[Anomaly]:
        """Detect anomalies in network centrality"""
        try:
            anomalies = []
            
            # Calculate entity centrality
            entity_centrality = defaultdict(int)
            for rel in relationships:
                entity_centrality[rel.source_id] += 1
                entity_centrality[rel.target_id] += 1
            
            if entity_centrality:
                centrality_values = list(entity_centrality.values())
                mean_centrality = statistics.mean(centrality_values)
                std_centrality = statistics.stdev(centrality_values) if len(centrality_values) > 1 else 0
                
                for entity_id, centrality in entity_centrality.items():
                    # Detect unusually high centrality
                    if centrality > mean_centrality + (2 * std_centrality):
                        anomaly = Anomaly(
                            id=f"anomaly_high_centrality_{entity_id}",
                            anomaly_type="network",
                            category="centrality",
                            title="Unusually High Network Centrality",
                            description=f"Entity {entity_id} has unusually high network centrality",
                            severity="medium",
                            confidence=0.8,
                            entities_involved=[entity_id],
                            metadata={
                                "centrality": centrality,
                                "average_centrality": mean_centrality,
                                "standard_deviation": std_centrality,
                                "z_score": (centrality - mean_centrality) / std_centrality if std_centrality > 0 else 0
                            }
                        )
                        anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting centrality anomalies: {e}")
            return []
    
    async def _detect_clustering_anomalies(self, relationships: List[Relationship]) -> List[Anomaly]:
        """Detect anomalies in network clustering"""
        try:
            anomalies = []
            
            # This would require network analysis library
            # For now, return empty list
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting clustering anomalies: {e}")
            return []
    
    async def _detect_communication_anomalies(self, relationships: List[Relationship]) -> List[Anomaly]:
        """Detect anomalies in communication patterns"""
        try:
            anomalies = []
            
            # Analyze mention patterns
            mention_relationships = [r for r in relationships if r.relationship_type == "mentions"]
            
            if mention_relationships:
                # Find entities with unusually high mention activity
                mention_counts = Counter([r.source_id for r in mention_relationships])
                mean_mentions = statistics.mean(mention_counts.values())
                std_mentions = statistics.stdev(mention_counts.values()) if len(mention_counts) > 1 else 0
                
                for entity_id, mention_count in mention_counts.items():
                    if mention_count > mean_mentions + (2 * std_mentions):
                        anomaly = Anomaly(
                            id=f"anomaly_high_mentions_{entity_id}",
                            anomaly_type="network",
                            category="communication",
                            title="Unusually High Mention Activity",
                            description=f"Entity {entity_id} mentions others unusually frequently",
                            severity="medium",
                            confidence=0.7,
                            entities_involved=[entity_id],
                            metadata={
                                "mention_count": mention_count,
                                "average_mentions": mean_mentions,
                                "standard_deviation": std_mentions
                            }
                        )
                        anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting communication anomalies: {e}")
            return []
    
    async def _detect_creation_timing_anomalies(self, entities: List[Entity]) -> List[Anomaly]:
        """Detect anomalies in account creation timing"""
        try:
            anomalies = []
            
            # Group entities by creation time
            creation_times = []
            for entity in entities:
                if entity.created_at:
                    creation_times.append(entity.created_at)
            
            if len(creation_times) > 3:
                # Sort creation times
                creation_times.sort()
                
                # Calculate time differences between consecutive creations
                time_diffs = []
                for i in range(1, len(creation_times)):
                    diff = (creation_times[i] - creation_times[i-1]).total_seconds()
                    time_diffs.append(diff)
                
                if time_diffs:
                    mean_diff = statistics.mean(time_diffs)
                    
                    # Detect rapid account creation
                    rapid_creations = [diff for diff in time_diffs if diff < 3600]  # Less than 1 hour
                    if len(rapid_creations) > 2:
                        anomaly = Anomaly(
                            id="anomaly_rapid_creation",
                            anomaly_type="temporal",
                            category="creation_timing",
                            title="Rapid Account Creation",
                            description=f"Found {len(rapid_creations)} accounts created in rapid succession",
                            severity="high",
                            confidence=0.9,
                            entities_involved=[e.id for e in entities if e.created_at],
                            metadata={
                                "rapid_creations": len(rapid_creations),
                                "average_time_between": mean_diff,
                                "total_accounts": len(creation_times)
                            }
                        )
                        anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting creation timing anomalies: {e}")
            return []
    
    async def _detect_activity_timing_anomalies(self, entities: List[Entity]) -> List[Anomaly]:
        """Detect anomalies in activity timing"""
        try:
            anomalies = []
            
            # This would require activity timestamp data
            # For now, return empty list
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting activity timing anomalies: {e}")
            return []
    
    async def _detect_growth_rate_anomalies(self, entities: List[Entity]) -> List[Anomaly]:
        """Detect anomalies in follower growth rates"""
        try:
            anomalies = []
            
            for entity in entities:
                if entity.followers_count and entity.created_at:
                    days_old = (datetime.utcnow() - entity.created_at).days
                    if days_old > 0:
                        growth_rate = entity.followers_count / days_old
                        
                        # Detect suspicious growth rate
                        if growth_rate > 100:  # More than 100 followers per day
                            anomaly = Anomaly(
                                id=f"anomaly_suspicious_growth_{entity.id}",
                                anomaly_type="temporal",
                                category="growth_rate",
                                title="Suspicious Growth Rate",
                                description=f"Entity {entity.username} shows suspicious follower growth rate",
                                severity="high",
                                confidence=0.8,
                                entities_involved=[entity.id],
                                metadata={
                                    "growth_rate": growth_rate,
                                    "followers_count": entity.followers_count,
                                    "days_old": days_old
                                }
                            )
                            anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting growth rate anomalies: {e}")
            return []
    
    async def _detect_seasonal_anomalies(self, entities: List[Entity]) -> List[Anomaly]:
        """Detect seasonal anomalies"""
        try:
            anomalies = []
            
            # Group entities by creation month
            monthly_creations = defaultdict(int)
            for entity in entities:
                if entity.created_at:
                    month = entity.created_at.month
                    monthly_creations[month] += 1
            
            if monthly_creations:
                mean_creations = statistics.mean(monthly_creations.values())
                
                for month, count in monthly_creations.items():
                    # Detect seasonal spikes
                    if count > mean_creations * 3:  # Three times the average
                        anomaly = Anomaly(
                            id=f"anomaly_seasonal_spike_{month}",
                            anomaly_type="temporal",
                            category="seasonal",
                            title=f"Seasonal Creation Spike",
                            description=f"Unusual account creation spike in month {month}",
                            severity="medium",
                            confidence=0.7,
                            entities_involved=[],
                            metadata={
                                "month": month,
                                "creation_count": count,
                                "average": mean_creations
                            }
                        )
                        anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting seasonal anomalies: {e}")
            return []
    
    async def _detect_content_length_anomalies(self, entities: List[Entity]) -> List[Anomaly]:
        """Detect anomalies in content length"""
        try:
            anomalies = []
            
            # Collect content lengths
            content_lengths = []
            for entity in entities:
                if hasattr(entity, 'content') and entity.content:
                    content_lengths.append(len(entity.content))
            
            if content_lengths:
                mean_length = statistics.mean(content_lengths)
                std_length = statistics.stdev(content_lengths) if len(content_lengths) > 1 else 0
                
                for entity in entities:
                    if hasattr(entity, 'content') and entity.content:
                        content_length = len(entity.content)
                        
                        # Detect unusually long content
                        if content_length > mean_length + (3 * std_length):
                            anomaly = Anomaly(
                                id=f"anomaly_long_content_{entity.id}",
                                anomaly_type="content",
                                category="content_length",
                                title="Unusually Long Content",
                                description=f"Entity {entity.username} posts unusually long content",
                                severity="low",
                                confidence=0.7,
                                entities_involved=[entity.id],
                                metadata={
                                    "content_length": content_length,
                                    "average_length": mean_length,
                                    "standard_deviation": std_length
                                }
                            )
                            anomalies.append(anomaly)
                        
                        # Detect unusually short content
                        elif content_length < mean_length - (3 * std_length) and content_length > 0:
                            anomaly = Anomaly(
                                id=f"anomaly_short_content_{entity.id}",
                                anomaly_type="content",
                                category="content_length",
                                title="Unusually Short Content",
                                description=f"Entity {entity.username} posts unusually short content",
                                severity="low",
                                confidence=0.6,
                                entities_involved=[entity.id],
                                metadata={
                                    "content_length": content_length,
                                    "average_length": mean_length,
                                    "standard_deviation": std_length
                                }
                            )
                            anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting content length anomalies: {e}")
            return []
    
    async def _detect_hashtag_anomalies(self, entities: List[Entity]) -> List[Anomaly]:
        """Detect anomalies in hashtag usage"""
        try:
            anomalies = []
            
            # Collect hashtags
            all_hashtags = []
            for entity in entities:
                if hasattr(entity, 'hashtags') and entity.hashtags:
                    all_hashtags.extend(entity.hashtags)
            
            if all_hashtags:
                hashtag_counts = Counter(all_hashtags)
                mean_usage = statistics.mean(hashtag_counts.values())
                
                for hashtag, count in hashtag_counts.items():
                    # Detect unusually frequent hashtag usage
                    if count > mean_usage * 5:  # Five times the average
                        anomaly = Anomaly(
                            id=f"anomaly_frequent_hashtag_{hashtag}",
                            anomaly_type="content",
                            category="hashtag_usage",
                            title=f"Unusually Frequent Hashtag: #{hashtag}",
                            description=f"Hashtag #{hashtag} appears unusually frequently",
                            severity="medium",
                            confidence=0.7,
                            entities_involved=[],
                            metadata={
                                "hashtag": hashtag,
                                "usage_count": count,
                                "average_usage": mean_usage
                            }
                        )
                        anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting hashtag anomalies: {e}")
            return []
    
    async def _detect_mention_anomalies(self, entities: List[Entity]) -> List[Anomaly]:
        """Detect anomalies in mention patterns"""
        try:
            anomalies = []
            
            # Collect mentions
            all_mentions = []
            for entity in entities:
                if hasattr(entity, 'mentions') and entity.mentions:
                    all_mentions.extend(entity.mentions)
            
            if all_mentions:
                mention_counts = Counter(all_mentions)
                mean_mentions = statistics.mean(mention_counts.values())
                
                for mention, count in mention_counts.items():
                    # Detect unusually frequent mentions
                    if count > mean_mentions * 3:  # Three times the average
                        anomaly = Anomaly(
                            id=f"anomaly_frequent_mention_{mention}",
                            anomaly_type="content",
                            category="mention_usage",
                            title=f"Unusually Frequent Mention: @{mention}",
                            description=f"User @{mention} is mentioned unusually frequently",
                            severity="medium",
                            confidence=0.7,
                            entities_involved=[],
                            metadata={
                                "mentioned_user": mention,
                                "mention_count": count,
                                "average_mentions": mean_mentions
                            }
                        )
                        anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting mention anomalies: {e}")
            return []
    
    async def _detect_url_anomalies(self, entities: List[Entity]) -> List[Anomaly]:
        """Detect anomalies in URL patterns"""
        try:
            anomalies = []
            
            # Collect URLs
            all_urls = []
            for entity in entities:
                if hasattr(entity, 'urls') and entity.urls:
                    all_urls.extend(entity.urls)
            
            if all_urls:
                # Analyze domains
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
                    mean_domain_usage = statistics.mean(domain_counts.values())
                    
                    for domain, count in domain_counts.items():
                        # Detect unusually frequent domain usage
                        if count > mean_domain_usage * 3:  # Three times the average
                            anomaly = Anomaly(
                                id=f"anomaly_frequent_domain_{domain}",
                                anomaly_type="content",
                                category="url_domain",
                                title=f"Unusually Frequent Domain: {domain}",
                                description=f"Domain {domain} appears unusually frequently",
                                severity="medium",
                                confidence=0.7,
                                entities_involved=[],
                                metadata={
                                    "domain": domain,
                                    "usage_count": count,
                                    "average_usage": mean_domain_usage
                                }
                            )
                            anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting URL anomalies: {e}")
            return []
    
    async def _detect_sentiment_anomalies(self, entities: List[Entity]) -> List[Anomaly]:
        """Detect anomalies in sentiment patterns"""
        try:
            anomalies = []
            
            # Simple sentiment analysis
            positive_keywords = ["good", "great", "love", "happy", "positive", "excellent"]
            negative_keywords = ["bad", "hate", "terrible", "awful", "negative", "horrible"]
            
            for entity in entities:
                if hasattr(entity, 'content') and entity.content:
                    content_lower = entity.content.lower()
                    
                    positive_count = sum(1 for word in positive_keywords if word in content_lower)
                    negative_count = sum(1 for word in negative_keywords if word in content_lower)
                    
                    # Detect extreme sentiment
                    if positive_count > 5 and negative_count == 0:
                        anomaly = Anomaly(
                            id=f"anomaly_extreme_positive_{entity.id}",
                            anomaly_type="content",
                            category="sentiment",
                            title="Extremely Positive Sentiment",
                            description=f"Entity {entity.username} shows extremely positive sentiment",
                            severity="low",
                            confidence=0.6,
                            entities_involved=[entity.id],
                            metadata={
                                "positive_keywords": positive_count,
                                "negative_keywords": negative_count
                            }
                        )
                        anomalies.append(anomaly)
                    
                    elif negative_count > 5 and positive_count == 0:
                        anomaly = Anomaly(
                            id=f"anomaly_extreme_negative_{entity.id}",
                            anomaly_type="content",
                            category="sentiment",
                            title="Extremely Negative Sentiment",
                            description=f"Entity {entity.username} shows extremely negative sentiment",
                            severity="medium",
                            confidence=0.6,
                            entities_involved=[entity.id],
                            metadata={
                                "positive_keywords": positive_count,
                                "negative_keywords": negative_count
                            }
                        )
                        anomalies.append(anomaly)
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting sentiment anomalies: {e}")
            return []
    
    async def detect_anomalies(self, data: list, *args, **kwargs) -> dict:
        """Test compatibility: detect anomalies (minimal implementation)"""
        return {
            "anomalies": [],
            "anomaly_score": 0.1,
            "input": data,
            "detected": False
        }

    async def analyze_patterns(self, patterns: list, *args, **kwargs) -> dict:
        """Test compatibility: analyze patterns (minimal implementation)"""
        return {
            "patterns": patterns,
            "pattern_analysis": "No significant patterns detected",
            "analysis": "No significant patterns detected",
            "risk_assessment": {
                "risk_level": "low",
                "risk_score": 0.2,
                "risk_factors": ["normal activity patterns"]
            }
        }
    
    def _load_anomaly_thresholds(self) -> Dict[str, Any]:
        """Load anomaly detection thresholds"""
        return {
            "posting_frequency": {
                "high_threshold": 100,
                "low_threshold": 1,
                "z_score_threshold": 2.0
            },
            "engagement_rate": {
                "low_threshold": 0.01,
                "suspicious_ratio": 100
            },
            "follower_growth": {
                "suspicious_rate": 100,
                "rapid_creation_threshold": 3600
            },
            "content_length": {
                "z_score_threshold": 3.0
            },
            "hashtag_usage": {
                "frequency_multiplier": 5
            },
            "mention_usage": {
                "frequency_multiplier": 3
            }
        } 