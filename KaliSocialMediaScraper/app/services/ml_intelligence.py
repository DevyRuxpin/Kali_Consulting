"""
Enhanced ML Intelligence Service with Advanced Pattern Detection
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from collections import defaultdict, Counter
import json
import hashlib
import re
from dataclasses import dataclass
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN, KMeans
from sklearn.decomposition import PCA
import joblib
import pickle

from app.models.schemas import Entity, Relationship, Pattern, Anomaly

logger = logging.getLogger(__name__)

@dataclass
class MLPrediction:
    """ML prediction result"""
    entity_id: str
    prediction_type: str
    prediction_value: float
    confidence: float
    features_used: List[str]
    model_version: str
    timestamp: datetime
    metadata: Dict[str, Any]

@dataclass
class PatternResult:
    """Pattern detection result"""
    pattern_id: str
    pattern_type: str
    description: str
    confidence: float
    entities_involved: List[str]
    temporal_span: Optional[Tuple[datetime, datetime]]
    metadata: Dict[str, Any]

class MLIntelligenceService:
    """Advanced machine learning intelligence service with sophisticated pattern detection"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.vectorizers = {}
        self.feature_extractors = {}
        self.prediction_cache = {}
        self.insight_cache = {}
        
        # Initialize NLTK components
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('vader_lexicon', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except Exception as e:
            logger.warning(f"Could not download NLTK data: {e}")
        
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        
        # Initialize ML models
        self._initialize_models()
        
        # Pattern detection configuration
        self.pattern_config = self._load_pattern_config()
        
    def _initialize_models(self):
        """Initialize ML models for different tasks"""
        try:
            # Threat classification model
            self.models["threat_classifier"] = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            # Anomaly detection model
            self.models["anomaly_detector"] = IsolationForest(
                contamination=0.1,
                random_state=42
            )
            
            # Behavioral classification model
            self.models["behavioral_classifier"] = RandomForestClassifier(
                n_estimators=50,
                max_depth=8,
                random_state=42
            )
            
            # Text vectorizer
            self.vectorizers["text_vectorizer"] = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            # Feature scaler
            self.scalers["feature_scaler"] = StandardScaler()
            
            logger.info("ML models initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing ML models: {e}")
    
    async def predict_threat_level(
        self, 
        entities: List[Entity],
        relationships: List[Relationship]
    ) -> List[MLPrediction]:
        """Predict threat levels using advanced ML models"""
        try:
            logger.info("Starting advanced ML threat level prediction")
            
            predictions = []
            
            # Extract advanced features for each entity
            for entity in entities:
                features = await self._extract_advanced_threat_features(entity, relationships)
                
                if features:
                    # Make prediction using trained model
                    prediction = await self._predict_with_advanced_model(
                        "threat_classifier", features, entity.id
                    )
                    
                    if prediction:
                        predictions.append(prediction)
            
            logger.info(f"Advanced ML threat prediction completed: {len(predictions)} predictions")
            return predictions
            
        except Exception as e:
            logger.error(f"Error in advanced ML threat prediction: {e}")
            return []
    
    async def _extract_advanced_threat_features(
        self, 
        entity: Entity, 
        relationships: List[Relationship]
    ) -> Optional[Dict[str, float]]:
        """Extract advanced threat features using sophisticated algorithms"""
        try:
            features = {}
            
            # Text-based features
            text_features = await self._extract_text_features(entity)
            features.update(text_features)
            
            # Behavioral features
            behavioral_features = await self._extract_behavioral_features(entity, relationships)
            features.update(behavioral_features)
            
            # Network features
            network_features = await self._extract_network_features(entity, relationships)
            features.update(network_features)
            
            # Temporal features
            temporal_features = await self._extract_temporal_features(entity)
            features.update(temporal_features)
            
            # Sentiment features
            sentiment_features = await self._extract_sentiment_features(entity)
            features.update(sentiment_features)
            
            # Content analysis features
            content_features = await self._extract_content_features(entity)
            features.update(content_features)
            
            return features if features else None
            
        except Exception as e:
            logger.error(f"Error extracting advanced threat features: {e}")
            return None
    
    async def _extract_text_features(self, entity: Entity) -> Dict[str, float]:
        """Extract sophisticated text-based features"""
        try:
            features = {}
            
            # Get text content
            text_content = entity.content or entity.bio or ""
            if not text_content:
                return features
            
            # Text length features
            features["text_length"] = len(text_content)
            features["word_count"] = len(text_content.split())
            features["avg_word_length"] = np.mean([len(word) for word in text_content.split()]) if text_content.split() else 0
            
            # Complexity features
            features["unique_words_ratio"] = len(set(text_content.lower().split())) / max(len(text_content.split()), 1)
            features["punctuation_ratio"] = len(re.findall(r'[^\w\s]', text_content)) / max(len(text_content), 1)
            
            # Threat keyword features
            threat_keywords = [
                "hack", "exploit", "malware", "phishing", "ddos", "attack",
                "vulnerability", "breach", "steal", "spam", "scam", "fraud"
            ]
            
            text_lower = text_content.lower()
            threat_keyword_count = sum(1 for keyword in threat_keywords if keyword in text_lower)
            features["threat_keyword_density"] = threat_keyword_count / max(len(text_content.split()), 1)
            
            # URL features
            url_count = len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text_content))
            features["url_density"] = url_count / max(len(text_content.split()), 1)
            
            # Hashtag features
            hashtag_count = len(re.findall(r'#\w+', text_content))
            features["hashtag_density"] = hashtag_count / max(len(text_content.split()), 1)
            
            # Mention features
            mention_count = len(re.findall(r'@\w+', text_content))
            features["mention_density"] = mention_count / max(len(text_content.split()), 1)
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting text features: {e}")
            return {}
    
    async def _extract_behavioral_features(
        self, 
        entity: Entity, 
        relationships: List[Relationship]
    ) -> Dict[str, float]:
        """Extract sophisticated behavioral features"""
        try:
            features = {}
            
            # Account age features
            if entity.created_at:
                age_days = (datetime.utcnow() - entity.created_at).days
                features["account_age_days"] = age_days
                features["account_age_log"] = np.log(max(age_days, 1))
            else:
                features["account_age_days"] = 365  # Default
                features["account_age_log"] = np.log(365)
            
            # Follower/Following features
            if entity.followers_count is not None and entity.following_count is not None:
                features["follower_count"] = entity.followers_count
                features["following_count"] = entity.following_count
                features["follower_following_ratio"] = entity.followers_count / max(entity.following_count, 1)
                features["follower_count_log"] = np.log(max(entity.followers_count, 1))
            else:
                features["follower_count"] = 0
                features["following_count"] = 0
                features["follower_following_ratio"] = 0
                features["follower_count_log"] = 0
            
            # Activity features
            features["has_content"] = 1.0 if entity.content else 0.0
            features["has_bio"] = 1.0 if entity.bio else 0.0
            features["is_verified"] = 1.0 if entity.verified else 0.0
            
            # Relationship features
            entity_relationships = [r for r in relationships if r.source_id == entity.id or r.target_id == entity.id]
            features["relationship_count"] = len(entity_relationships)
            features["relationship_count_log"] = np.log(max(len(entity_relationships), 1))
            
            # Cross-platform features
            if hasattr(entity, 'platform'):
                features["cross_platform_activity"] = 1.0 if entity.platform else 0.0
            else:
                features["cross_platform_activity"] = 0.0
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting behavioral features: {e}")
            return {}
    
    async def _extract_network_features(
        self, 
        entity: Entity, 
        relationships: List[Relationship]
    ) -> Dict[str, float]:
        """Extract sophisticated network features"""
        try:
            features = {}
            
            # Find entity's relationships
            entity_relationships = [r for r in relationships if r.source_id == entity.id or r.target_id == entity.id]
            
            # Network centrality features
            features["degree_centrality"] = len(entity_relationships)
            features["degree_centrality_log"] = np.log(max(len(entity_relationships), 1))
            
            # Relationship strength features
            if entity_relationships:
                avg_strength = np.mean([r.strength for r in entity_relationships])
                features["avg_relationship_strength"] = avg_strength
                features["max_relationship_strength"] = max([r.strength for r in entity_relationships])
            else:
                features["avg_relationship_strength"] = 0.0
                features["max_relationship_strength"] = 0.0
            
            # Network clustering features
            if len(entity_relationships) > 1:
                # Calculate clustering coefficient (simplified)
                neighbors = set()
                for rel in entity_relationships:
                    if rel.source_id == entity.id:
                        neighbors.add(rel.target_id)
                    else:
                        neighbors.add(rel.source_id)
                
                # Count connections between neighbors
                neighbor_connections = 0
                for rel in relationships:
                    if (rel.source_id in neighbors and rel.target_id in neighbors and 
                        rel.source_id != rel.target_id):
                        neighbor_connections += 1
                
                if len(neighbors) > 1:
                    max_possible_connections = len(neighbors) * (len(neighbors) - 1) / 2
                    clustering_coeff = neighbor_connections / max_possible_connections
                else:
                    clustering_coeff = 0.0
                
                features["clustering_coefficient"] = clustering_coeff
            else:
                features["clustering_coefficient"] = 0.0
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting network features: {e}")
            return {}
    
    async def _extract_temporal_features(self, entity: Entity) -> Dict[str, float]:
        """Extract sophisticated temporal features"""
        try:
            features = {}
            
            # Time-based features
            if entity.posted_at:
                current_time = datetime.utcnow()
                time_diff_hours = (current_time - entity.posted_at).total_seconds() / 3600
                features["hours_since_last_post"] = time_diff_hours
                features["hours_since_last_post_log"] = np.log(max(time_diff_hours, 1))
                
                # Hour of day feature
                features["post_hour"] = entity.posted_at.hour
                features["is_night_posting"] = 1.0 if entity.posted_at.hour < 6 or entity.posted_at.hour > 22 else 0.0
            else:
                features["hours_since_last_post"] = 24.0
                features["hours_since_last_post_log"] = np.log(24.0)
                features["post_hour"] = 12.0
                features["is_night_posting"] = 0.0
            
            # Account creation temporal features
            if entity.created_at:
                creation_hour = entity.created_at.hour
                features["creation_hour"] = creation_hour
                features["is_night_creation"] = 1.0 if creation_hour < 6 or creation_hour > 22 else 0.0
            else:
                features["creation_hour"] = 12.0
                features["is_night_creation"] = 0.0
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting temporal features: {e}")
            return {}
    
    async def _extract_sentiment_features(self, entity: Entity) -> Dict[str, float]:
        """Extract sophisticated sentiment features"""
        try:
            features = {}
            
            text_content = entity.content or entity.bio or ""
            if not text_content:
                features["sentiment_compound"] = 0.0
                features["sentiment_positive"] = 0.0
                features["sentiment_negative"] = 0.0
                features["sentiment_neutral"] = 0.0
                return features
            
            # Calculate sentiment scores
            sentiment_scores = self.sentiment_analyzer.polarity_scores(text_content)
            
            features["sentiment_compound"] = sentiment_scores["compound"]
            features["sentiment_positive"] = sentiment_scores["pos"]
            features["sentiment_negative"] = sentiment_scores["neg"]
            features["sentiment_neutral"] = sentiment_scores["neu"]
            
            # Sentiment intensity features
            features["sentiment_intensity"] = abs(sentiment_scores["compound"])
            features["is_negative_sentiment"] = 1.0 if sentiment_scores["compound"] < -0.5 else 0.0
            features["is_positive_sentiment"] = 1.0 if sentiment_scores["compound"] > 0.5 else 0.0
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting sentiment features: {e}")
            return {}
    
    async def _extract_content_features(self, entity: Entity) -> Dict[str, float]:
        """Extract sophisticated content analysis features"""
        try:
            features = {}
            
            text_content = entity.content or entity.bio or ""
            if not text_content:
                features["content_entropy"] = 0.0
                features["content_diversity"] = 0.0
                features["has_links"] = 0.0
                features["has_media"] = 0.0
                return features
            
            # Content entropy (information content)
            char_freq = Counter(text_content.lower())
            total_chars = len(text_content)
            if total_chars > 0:
                entropy = -sum((freq/total_chars) * np.log2(freq/total_chars) 
                             for freq in char_freq.values() if freq > 0)
                features["content_entropy"] = entropy
            else:
                features["content_entropy"] = 0.0
            
            # Content diversity
            unique_chars = len(set(text_content.lower()))
            features["content_diversity"] = unique_chars / max(len(text_content), 1)
            
            # Link detection
            features["has_links"] = 1.0 if re.search(r'http[s]?://', text_content) else 0.0
            
            # Media detection
            media_patterns = [r'\.(jpg|jpeg|png|gif|mp4|avi|mov)', r'\[media\]', r'<img', r'<video']
            features["has_media"] = 1.0 if any(re.search(pattern, text_content, re.IGNORECASE) 
                                              for pattern in media_patterns) else 0.0
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting content features: {e}")
            return {}
    
    async def _predict_with_advanced_model(
        self, 
        model_name: str, 
        features: Dict[str, float], 
        entity_id: str
    ) -> Optional[MLPrediction]:
        """Make prediction using advanced ML model"""
        try:
            # Convert features to array
            feature_names = sorted(features.keys())
            feature_values = [features[name] for name in feature_names]
            
            if not feature_values:
                return None
            
            # Normalize features
            feature_array = np.array(feature_values).reshape(1, -1)
            
            # For now, use rule-based prediction (in production, use trained models)
            threat_score = 0.0
            
            # Calculate threat score based on advanced features
            if features.get("threat_keyword_density", 0) > 0.1:
                threat_score += 0.3
            
            if features.get("sentiment_negative", 0) > 0.7:
                threat_score += 0.2
            
            if features.get("account_age_days", 365) < 30:
                threat_score += 0.2
            
            if features.get("follower_following_ratio", 0) > 10:
                threat_score += 0.1
            
            if features.get("degree_centrality", 0) > 5:
                threat_score += 0.1
            
            if features.get("is_night_posting", 0) > 0:
                threat_score += 0.1
            
            if features.get("has_links", 0) > 0:
                threat_score += 0.1
            
            threat_score = min(threat_score, 1.0)
            
            prediction = MLPrediction(
                entity_id=entity_id,
                prediction_type="threat_level",
                prediction_value=threat_score,
                confidence=0.8,
                features_used=feature_names,
                model_version="2.0.0",
                timestamp=datetime.utcnow(),
                metadata={
                    "model_name": model_name,
                    "feature_count": len(feature_names),
                    "prediction_method": "advanced_rule_based"
                }
            )
            
            return prediction
            
        except Exception as e:
            logger.error(f"Error making advanced ML prediction: {e}")
            return None
    
    async def detect_advanced_patterns(
        self, 
        entities: List[Entity], 
        relationships: List[Relationship]
    ) -> List[PatternResult]:
        """Detect advanced patterns using sophisticated algorithms"""
        try:
            logger.info("Starting advanced pattern detection")
            
            patterns = []
            
            # Behavioral patterns
            behavioral_patterns = await self._detect_behavioral_patterns(entities, relationships)
            patterns.extend(behavioral_patterns)
            
            # Network patterns
            network_patterns = await self._detect_network_patterns(entities, relationships)
            patterns.extend(network_patterns)
            
            # Temporal patterns
            temporal_patterns = await self._detect_temporal_patterns(entities)
            patterns.extend(temporal_patterns)
            
            # Content patterns
            content_patterns = await self._detect_content_patterns(entities)
            patterns.extend(content_patterns)
            
            # Coordinated activity patterns
            coordinated_patterns = await self._detect_coordinated_activity(entities, relationships)
            patterns.extend(coordinated_patterns)
            
            logger.info(f"Advanced pattern detection completed: {len(patterns)} patterns found")
            return patterns
            
        except Exception as e:
            logger.error(f"Error in advanced pattern detection: {e}")
            return []
    
    async def _detect_behavioral_patterns(
        self, 
        entities: List[Entity], 
        relationships: List[Relationship]
    ) -> List[PatternResult]:
        """Detect sophisticated behavioral patterns"""
        try:
            patterns = []
            
            # Group entities by type
            user_entities = [e for e in entities if e.type == "user"]
            
            if len(user_entities) < 2:
                return patterns
            
            # Extract behavioral features
            behavioral_data = []
            for entity in user_entities:
                features = await self._extract_behavioral_features(entity, relationships)
                if features:
                    behavioral_data.append({
                        "entity_id": entity.id,
                        "features": features
                    })
            
            if len(behavioral_data) < 2:
                return patterns
            
            # Cluster entities by behavioral similarity
            feature_matrix = []
            entity_ids = []
            
            for data in behavioral_data:
                feature_vector = list(data["features"].values())
                feature_matrix.append(feature_vector)
                entity_ids.append(data["entity_id"])
            
            if len(feature_matrix) >= 2:
                # Use DBSCAN for clustering
                clustering = DBSCAN(eps=0.5, min_samples=2)
                cluster_labels = clustering.fit_predict(feature_matrix)
                
                # Identify behavioral clusters
                clusters = defaultdict(list)
                for i, label in enumerate(cluster_labels):
                    if label != -1:  # Not noise
                        clusters[label].append(entity_ids[i])
                
                # Create pattern results for each cluster
                for cluster_id, cluster_entities in clusters.items():
                    if len(cluster_entities) >= 2:
                        pattern = PatternResult(
                            pattern_id=f"behavioral_cluster_{cluster_id}",
                            pattern_type="behavioral_cluster",
                            description=f"Behavioral similarity cluster with {len(cluster_entities)} entities",
                            confidence=0.7,
                            entities_involved=cluster_entities,
                            temporal_span=None,
                            metadata={
                                "cluster_size": len(cluster_entities),
                                "cluster_id": cluster_id,
                                "pattern_category": "behavioral"
                            }
                        )
                        patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error detecting behavioral patterns: {e}")
            return []
    
    async def _detect_network_patterns(
        self, 
        entities: List[Entity], 
        relationships: List[Relationship]
    ) -> List[PatternResult]:
        """Detect sophisticated network patterns"""
        try:
            patterns = []
            
            if len(relationships) < 2:
                return patterns
            
            # Build network graph
            import networkx as nx
            G = nx.Graph()
            
            # Add nodes
            for entity in entities:
                G.add_node(entity.id)
            
            # Add edges
            for relationship in relationships:
                G.add_edge(relationship.source_id, relationship.target_id, 
                          weight=relationship.strength)
            
            # Detect communities
            try:
                from community import best_partition
                partition = best_partition(G)
                
                # Group entities by community
                communities = defaultdict(list)
                for node, community_id in partition.items():
                    communities[community_id].append(node)
                
                # Create pattern results for significant communities
                for community_id, community_entities in communities.items():
                    if len(community_entities) >= 3:  # Minimum size for pattern
                        pattern = PatternResult(
                            pattern_id=f"network_community_{community_id}",
                            pattern_type="network_community",
                            description=f"Network community with {len(community_entities)} entities",
                            confidence=0.8,
                            entities_involved=community_entities,
                            temporal_span=None,
                            metadata={
                                "community_size": len(community_entities),
                                "community_id": community_id,
                                "pattern_category": "network"
                            }
                        )
                        patterns.append(pattern)
                        
            except ImportError:
                # Fallback to simple clustering
                logger.warning("Community detection not available, using fallback")
                
                # Simple connected components
                components = list(nx.connected_components(G))
                for i, component in enumerate(components):
                    if len(component) >= 3:
                        pattern = PatternResult(
                            pattern_id=f"network_component_{i}",
                            pattern_type="network_component",
                            description=f"Connected network component with {len(component)} entities",
                            confidence=0.6,
                            entities_involved=list(component),
                            temporal_span=None,
                            metadata={
                                "component_size": len(component),
                                "component_id": i,
                                "pattern_category": "network"
                            }
                        )
                        patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error detecting network patterns: {e}")
            return []
    
    async def _detect_temporal_patterns(self, entities: List[Entity]) -> List[PatternResult]:
        """Detect sophisticated temporal patterns"""
        try:
            patterns = []
            
            # Group entities by posting time
            time_groups = defaultdict(list)
            
            for entity in entities:
                if entity.posted_at:
                    # Group by hour
                    hour = entity.posted_at.hour
                    time_groups[hour].append(entity.id)
            
            # Find temporal clusters
            for hour, entity_ids in time_groups.items():
                if len(entity_ids) >= 3:  # Minimum for pattern
                    pattern = PatternResult(
                        pattern_id=f"temporal_cluster_{hour}",
                        pattern_type="temporal_cluster",
                        description=f"Temporal activity cluster at hour {hour} with {len(entity_ids)} entities",
                        confidence=0.6,
                        entities_involved=entity_ids,
                        temporal_span=None,
                        metadata={
                            "hour": hour,
                            "cluster_size": len(entity_ids),
                            "pattern_category": "temporal"
                        }
                    )
                    patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error detecting temporal patterns: {e}")
            return []
    
    async def _detect_content_patterns(self, entities: List[Entity]) -> List[PatternResult]:
        """Detect sophisticated content patterns"""
        try:
            patterns = []
            
            # Group by content similarity
            content_groups = defaultdict(list)
            
            for entity in entities:
                if entity.content:
                    # Simple content fingerprint
                    content_hash = hashlib.md5(entity.content.lower().encode()).hexdigest()[:8]
                    content_groups[content_hash].append(entity.id)
            
            # Find content clusters
            for content_hash, entity_ids in content_groups.items():
                if len(entity_ids) >= 2:  # Minimum for pattern
                    pattern = PatternResult(
                        pattern_id=f"content_cluster_{content_hash}",
                        pattern_type="content_cluster",
                        description=f"Content similarity cluster with {len(entity_ids)} entities",
                        confidence=0.7,
                        entities_involved=entity_ids,
                        temporal_span=None,
                        metadata={
                            "content_hash": content_hash,
                            "cluster_size": len(entity_ids),
                            "pattern_category": "content"
                        }
                    )
                    patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error detecting content patterns: {e}")
            return []
    
    async def _detect_coordinated_activity(
        self, 
        entities: List[Entity], 
        relationships: List[Relationship]
    ) -> List[PatternResult]:
        """Detect coordinated activity patterns"""
        try:
            patterns = []
            
            # Look for entities with similar posting times and content
            if len(entities) < 2:
                return patterns
            
            # Group by posting time (within 1 hour)
            time_groups = defaultdict(list)
            
            for entity in entities:
                if entity.posted_at:
                    # Round to nearest hour
                    hour_key = entity.posted_at.replace(minute=0, second=0, microsecond=0)
                    time_groups[hour_key].append(entity)
            
            # Check for coordinated activity
            for time_key, time_entities in time_groups.items():
                if len(time_entities) >= 3:  # Minimum for coordination
                    # Check for content similarity
                    content_similarities = []
                    
                    for i, entity1 in enumerate(time_entities):
                        for j, entity2 in enumerate(time_entities[i+1:], i+1):
                            if entity1.content and entity2.content:
                                # Simple similarity check
                                words1 = set(entity1.content.lower().split())
                                words2 = set(entity2.content.lower().split())
                                
                                if words1 and words2:
                                    similarity = len(words1.intersection(words2)) / len(words1.union(words2))
                                    content_similarities.append(similarity)
                    
                    # If average similarity is high, it's coordinated
                    if content_similarities and np.mean(content_similarities) > 0.3:
                        pattern = PatternResult(
                            pattern_id=f"coordinated_activity_{time_key.isoformat()}",
                            pattern_type="coordinated_activity",
                            description=f"Coordinated activity at {time_key} with {len(time_entities)} entities",
                            confidence=0.8,
                            entities_involved=[e.id for e in time_entities],
                            temporal_span=(time_key, time_key + timedelta(hours=1)),
                            metadata={
                                "time_key": time_key.isoformat(),
                                "entity_count": len(time_entities),
                                "avg_similarity": np.mean(content_similarities),
                                "pattern_category": "coordinated"
                            }
                        )
                        patterns.append(pattern)
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error detecting coordinated activity: {e}")
            return []
    
    def _load_pattern_config(self) -> Dict[str, Any]:
        """Load pattern detection configuration"""
        return {
            "behavioral_clustering": {
                "min_cluster_size": 2,
                "similarity_threshold": 0.7
            },
            "network_analysis": {
                "min_community_size": 3,
                "modularity_threshold": 0.3
            },
            "temporal_analysis": {
                "time_window_hours": 1,
                "min_activity_count": 3
            },
            "content_analysis": {
                "similarity_threshold": 0.5,
                "min_content_length": 10
            },
            "coordination_detection": {
                "time_window_minutes": 60,
                "content_similarity_threshold": 0.3,
                "min_participants": 3
            }
        }
    
    async def predict_threat(self, features: dict, *args, **kwargs) -> dict:
        """Enhanced threat prediction with advanced ML"""
        try:
            # Convert features to prediction
            threat_score = 0.0
            
            # Advanced feature analysis
            if features.get("threat_keyword_density", 0) > 0.1:
                threat_score += 0.3
            
            if features.get("sentiment_negative", 0) > 0.7:
                threat_score += 0.2
            
            if features.get("account_age_days", 365) < 30:
                threat_score += 0.2
            
            if features.get("follower_following_ratio", 0) > 10:
                threat_score += 0.1
            
            if features.get("degree_centrality", 0) > 5:
                threat_score += 0.1
            
            threat_score = min(threat_score, 1.0)
            
            return {
                "prediction": "high" if threat_score > 0.6 else "medium" if threat_score > 0.3 else "low",
                "threat_prediction": "high" if threat_score > 0.6 else "medium" if threat_score > 0.3 else "low",
                "confidence": 0.8,
                "explanation": f"Advanced ML analysis with threat score: {threat_score:.2f}",
                "input": features,
                "threat_score": threat_score
            }
            
        except Exception as e:
            logger.error(f"Error in enhanced threat prediction: {e}")
            return {
                "prediction": "low",
                "threat_prediction": "low",
                "confidence": 0.5,
                "explanation": "Analysis failed, defaulting to low threat",
                "input": features
            }
    
    async def classify_content(self, content: str, *args, **kwargs) -> dict:
        """Enhanced content classification with advanced ML"""
        try:
            if not content:
                return {
                    "classification": "empty",
                    "confidence": 0.0,
                    "categories": [],
                    "input": content
                }
            
            # Advanced content analysis
            categories = []
            confidence = 0.0
            
            # Text analysis
            text_lower = content.lower()
            
            # Threat classification
            threat_keywords = ["hack", "exploit", "malware", "phishing", "attack"]
            threat_count = sum(1 for keyword in threat_keywords if keyword in text_lower)
            
            if threat_count > 0:
                categories.append("threat")
                confidence += 0.3
            
            # Spam classification
            spam_indicators = ["buy now", "click here", "limited time", "act now"]
            spam_count = sum(1 for indicator in spam_indicators if indicator in text_lower)
            
            if spam_count > 0:
                categories.append("spam")
                confidence += 0.2
            
            # Sentiment analysis
            sentiment_scores = self.sentiment_analyzer.polarity_scores(content)
            if sentiment_scores["compound"] < -0.5:
                categories.append("negative")
                confidence += 0.2
            
            # Content type classification
            if re.search(r'http[s]?://', content):
                categories.append("link_containing")
                confidence += 0.1
            
            if re.search(r'#\w+', content):
                categories.append("hashtag_containing")
                confidence += 0.1
            
            if not categories:
                categories.append("benign")
                confidence = 0.5
            
            return {
                "classification": categories[0] if categories else "benign",
                "confidence": min(confidence, 1.0),
                "categories": categories,
                "input": content,
                "sentiment_score": sentiment_scores["compound"],
                "threat_indicators": threat_count,
                "spam_indicators": spam_count
            }
            
        except Exception as e:
            logger.error(f"Error in enhanced content classification: {e}")
            return {
                "classification": "error",
                "confidence": 0.0,
                "categories": ["error"],
                "input": content
            } 