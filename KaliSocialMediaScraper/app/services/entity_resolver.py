"""
Entity Resolution Service
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import re
import hashlib
from difflib import SequenceMatcher

from app.models.schemas import Entity

logger = logging.getLogger(__name__)

class EntityResolver:
    """Entity resolution and linking service"""
    
    def __init__(self):
        self.entity_cache = {}
        self.resolution_rules = self._load_resolution_rules()
        
    async def resolve_entities(self, entities: List[Entity]) -> List[Entity]:
        """Resolve and link entities across platforms"""
        try:
            # Group entities by potential matches
            entity_groups = await self._group_entities(entities)
            
            # Resolve entities within groups
            resolved_entities = []
            for group in entity_groups:
                resolved_group = await self._resolve_entity_group(group)
                resolved_entities.extend(resolved_group)
            
            # Update entity metadata with resolution info
            for entity in resolved_entities:
                entity.metadata = entity.metadata or {}
                entity.metadata["resolved"] = True
                entity.metadata["resolution_confidence"] = self._calculate_resolution_confidence(entity)
            
            return resolved_entities
            
        except Exception as e:
            logger.error(f"Error resolving entities: {e}")
            return entities
    
    async def _group_entities(self, entities: List[Entity]) -> List[List[Entity]]:
        """Group entities by potential matches"""
        try:
            groups = []
            processed = set()
            
            for i, entity1 in enumerate(entities):
                if entity1.id in processed:
                    continue
                
                group = [entity1]
                processed.add(entity1.id)
                
                for entity2 in entities[i+1:]:
                    if entity2.id in processed:
                        continue
                    
                    if await self._entities_match(entity1, entity2):
                        group.append(entity2)
                        processed.add(entity2.id)
                
                groups.append(group)
            
            return groups
            
        except Exception as e:
            logger.error(f"Error grouping entities: {e}")
            return [[entity] for entity in entities]
    
    async def _entities_match(self, entity1: Entity, entity2: Entity) -> bool:
        """Check if two entities are the same"""
        try:
            # Username matching
            if entity1.username and entity2.username:
                if self._usernames_match(entity1.username, entity2.username):
                    return True
            
            # Email matching
            email1 = self._extract_email(entity1)
            email2 = self._extract_email(entity2)
            if email1 and email2 and email1.lower() == email2.lower():
                return True
            
            # Display name matching
            if entity1.display_name and entity2.display_name:
                if self._names_match(entity1.display_name, entity2.display_name):
                    return True
            
            # Bio/content matching
            if entity1.bio and entity2.bio:
                if self._content_matches(entity1.bio, entity2.bio):
                    return True
            
            # Domain matching (for domain entities)
            if entity1.type == "domain" and entity2.type == "domain":
                if entity1.domain and entity2.domain:
                    if self._domains_match(entity1.domain, entity2.domain):
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking entity match: {e}")
            return False
    
    def _usernames_match(self, username1: str, username2: str) -> bool:
        """Check if usernames match"""
        try:
            # Normalize usernames
            norm1 = self._normalize_username(username1)
            norm2 = self._normalize_username(username2)
            
            # Exact match
            if norm1 == norm2:
                return True
            
            # Similarity match
            similarity = SequenceMatcher(None, norm1, norm2).ratio()
            if similarity > 0.8:
                return True
            
            # Handle common variations
            variations1 = self._generate_username_variations(username1)
            variations2 = self._generate_username_variations(username2)
            
            for var1 in variations1:
                for var2 in variations2:
                    if var1 == var2:
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking username match: {e}")
            return False
    
    def _normalize_username(self, username: str) -> str:
        """Normalize username for comparison"""
        try:
            # Remove common prefixes/suffixes
            username = username.lower()
            username = re.sub(r'^[0-9]+', '', username)  # Remove leading numbers
            username = re.sub(r'[0-9]+$', '', username)  # Remove trailing numbers
            username = re.sub(r'[^a-z0-9_]', '', username)  # Keep only alphanumeric and underscore
            return username
            
        except Exception as e:
            logger.error(f"Error normalizing username: {e}")
            return username.lower()
    
    def _generate_username_variations(self, username: str) -> List[str]:
        """Generate common username variations"""
        try:
            variations = [username.lower()]
            
            # Remove numbers
            no_numbers = re.sub(r'[0-9]', '', username.lower())
            if no_numbers:
                variations.append(no_numbers)
            
            # Remove underscores
            no_underscores = username.lower().replace('_', '')
            if no_underscores:
                variations.append(no_underscores)
            
            # Remove hyphens
            no_hyphens = username.lower().replace('-', '')
            if no_hyphens:
                variations.append(no_hyphens)
            
            # Common suffixes
            suffixes = ['_', '1', '2', '3', 'real', 'official', 'verified']
            for suffix in suffixes:
                if not username.lower().endswith(suffix):
                    variations.append(username.lower() + suffix)
            
            return list(set(variations))
            
        except Exception as e:
            logger.error(f"Error generating username variations: {e}")
            return [username.lower()]
    
    def _extract_email(self, entity: Entity) -> Optional[str]:
        """Extract email from entity"""
        try:
            # Check metadata for email
            if entity.metadata and 'email' in entity.metadata:
                return entity.metadata['email']
            
            # Check bio for email patterns
            if entity.bio:
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, entity.bio)
                if emails:
                    return emails[0]
            
            # Check content for email patterns
            if hasattr(entity, 'content') and entity.content:
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, entity.content)
                if emails:
                    return emails[0]
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting email: {e}")
            return None
    
    def _names_match(self, name1: str, name2: str) -> bool:
        """Check if names match"""
        try:
            # Normalize names
            norm1 = self._normalize_name(name1)
            norm2 = self._normalize_name(name2)
            
            # Exact match
            if norm1 == norm2:
                return True
            
            # Similarity match
            similarity = SequenceMatcher(None, norm1, norm2).ratio()
            if similarity > 0.7:
                return True
            
            # Check for partial matches
            words1 = set(norm1.split())
            words2 = set(norm2.split())
            
            if len(words1.intersection(words2)) >= min(len(words1), len(words2)) * 0.5:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking name match: {e}")
            return False
    
    def _normalize_name(self, name: str) -> str:
        """Normalize name for comparison"""
        try:
            # Remove extra whitespace
            name = ' '.join(name.split())
            
            # Convert to lowercase
            name = name.lower()
            
            # Remove common prefixes/suffixes
            prefixes = ['mr', 'mrs', 'ms', 'dr', 'prof']
            suffixes = ['jr', 'sr', 'ii', 'iii', 'iv']
            
            words = name.split()
            if words and words[0] in prefixes:
                words = words[1:]
            if words and words[-1] in suffixes:
                words = words[:-1]
            
            return ' '.join(words)
            
        except Exception as e:
            logger.error(f"Error normalizing name: {e}")
            return name.lower()
    
    def _content_matches(self, content1: str, content2: str) -> bool:
        """Check if content matches"""
        try:
            # Normalize content
            norm1 = self._normalize_content(content1)
            norm2 = self._normalize_content(content2)
            
            # Exact match
            if norm1 == norm2:
                return True
            
            # Similarity match
            similarity = SequenceMatcher(None, norm1, norm2).ratio()
            if similarity > 0.6:
                return True
            
            # Check for common phrases
            words1 = set(norm1.split())
            words2 = set(norm2.split())
            
            if len(words1.intersection(words2)) >= min(len(words1), len(words2)) * 0.3:
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking content match: {e}")
            return False
    
    def _normalize_content(self, content: str) -> str:
        """Normalize content for comparison"""
        try:
            # Remove URLs
            content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', content)
            
            # Remove mentions and hashtags
            content = re.sub(r'@\w+', '', content)
            content = re.sub(r'#\w+', '', content)
            
            # Remove extra whitespace
            content = ' '.join(content.split())
            
            # Convert to lowercase
            content = content.lower()
            
            return content
            
        except Exception as e:
            logger.error(f"Error normalizing content: {e}")
            return content.lower()
    
    def _domains_match(self, domain1: str, domain2: str) -> bool:
        """Check if domains match"""
        try:
            # Normalize domains
            norm1 = domain1.lower().strip()
            norm2 = domain2.lower().strip()
            
            # Exact match
            if norm1 == norm2:
                return True
            
            # Remove www prefix
            if norm1.startswith('www.'):
                norm1 = norm1[4:]
            if norm2.startswith('www.'):
                norm2 = norm2[4:]
            
            if norm1 == norm2:
                return True
            
            # Check for subdomain relationships
            if norm1.endswith('.' + norm2) or norm2.endswith('.' + norm1):
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking domain match: {e}")
            return False
    
    async def _resolve_entity_group(self, entities: List[Entity]) -> List[Entity]:
        """Resolve entities within a group"""
        try:
            if len(entities) == 1:
                return entities
            
            # Find the primary entity (most complete information)
            primary_entity = self._find_primary_entity(entities)
            
            # Merge information from other entities
            resolved_entities = []
            for entity in entities:
                if entity.id == primary_entity.id:
                    # Enhance primary entity with information from others
                    enhanced_entity = self._enhance_entity(primary_entity, entities)
                    resolved_entities.append(enhanced_entity)
                else:
                    # Mark as resolved and link to primary
                    entity.metadata = entity.metadata or {}
                    entity.metadata["resolved_to"] = primary_entity.id
                    entity.metadata["resolution_type"] = "linked"
                    resolved_entities.append(entity)
            
            return resolved_entities
            
        except Exception as e:
            logger.error(f"Error resolving entity group: {e}")
            return entities
    
    def _find_primary_entity(self, entities: List[Entity]) -> Entity:
        """Find the primary entity in a group"""
        try:
            # Score entities based on completeness
            entity_scores = []
            for entity in entities:
                score = 0
                
                # Basic information
                if entity.username:
                    score += 10
                if entity.display_name:
                    score += 5
                if entity.bio:
                    score += 3
                if entity.followers_count:
                    score += 2
                if entity.created_at:
                    score += 2
                if entity.verified:
                    score += 5
                if entity.location:
                    score += 2
                
                # Platform-specific scoring
                if entity.platform in ['github', 'linkedin']:
                    score += 3  # Professional platforms
                elif entity.platform in ['twitter', 'instagram']:
                    score += 2  # Popular social platforms
                
                # Metadata completeness
                if entity.metadata:
                    score += len(entity.metadata) * 0.5
                
                entity_scores.append((entity, score))
            
            # Return entity with highest score
            return max(entity_scores, key=lambda x: x[1])[0]
            
        except Exception as e:
            logger.error(f"Error finding primary entity: {e}")
            return entities[0]
    
    def _enhance_entity(self, primary_entity: Entity, all_entities: List[Entity]) -> Entity:
        """Enhance primary entity with information from other entities"""
        try:
            enhanced_entity = primary_entity
            
            # Collect all unique information
            all_usernames = set()
            all_display_names = set()
            all_bios = set()
            all_locations = set()
            all_platforms = set()
            all_metadata = {}
            
            for entity in all_entities:
                if entity.username:
                    all_usernames.add(entity.username)
                if entity.display_name:
                    all_display_names.add(entity.display_name)
                if entity.bio:
                    all_bios.add(entity.bio)
                if entity.location:
                    all_locations.add(entity.location)
                if entity.platform:
                    all_platforms.add(entity.platform)
                if entity.metadata:
                    all_metadata.update(entity.metadata)
            
            # Update enhanced entity
            if all_usernames:
                enhanced_entity.metadata = enhanced_entity.metadata or {}
                enhanced_entity.metadata["all_usernames"] = list(all_usernames)
            
            if all_display_names:
                enhanced_entity.metadata["all_display_names"] = list(all_display_names)
            
            if all_bios:
                enhanced_entity.metadata["all_bios"] = list(all_bios)
            
            if all_locations:
                enhanced_entity.metadata["all_locations"] = list(all_locations)
            
            if all_platforms:
                enhanced_entity.metadata["all_platforms"] = list(all_platforms)
            
            # Merge metadata
            if all_metadata:
                enhanced_entity.metadata.update(all_metadata)
            
            # Add resolution metadata
            enhanced_entity.metadata["resolution_count"] = len(all_entities)
            enhanced_entity.metadata["resolution_timestamp"] = datetime.utcnow().isoformat()
            
            return enhanced_entity
            
        except Exception as e:
            logger.error(f"Error enhancing entity: {e}")
            return primary_entity
    
    def _calculate_resolution_confidence(self, entity: Entity) -> float:
        """Calculate confidence score for entity resolution"""
        try:
            confidence = 0.0
            
            # Base confidence
            if entity.metadata and entity.metadata.get("resolved"):
                confidence += 0.3
            
            # Resolution count
            resolution_count = entity.metadata.get("resolution_count", 1)
            if resolution_count > 1:
                confidence += min(resolution_count * 0.1, 0.3)
            
            # Information completeness
            if entity.username:
                confidence += 0.1
            if entity.display_name:
                confidence += 0.1
            if entity.bio:
                confidence += 0.1
            if entity.followers_count:
                confidence += 0.05
            if entity.verified:
                confidence += 0.1
            
            # Cross-platform presence
            all_platforms = entity.metadata.get("all_platforms", [])
            if len(all_platforms) > 1:
                confidence += min(len(all_platforms) * 0.05, 0.2)
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating resolution confidence: {e}")
            return 0.5
    
    def _load_resolution_rules(self) -> Dict[str, Any]:
        """Load entity resolution rules"""
        return {
            "username_similarity_threshold": 0.8,
            "name_similarity_threshold": 0.7,
            "content_similarity_threshold": 0.6,
            "email_exact_match": True,
            "domain_exact_match": True,
            "cross_platform_weight": 0.2,
            "metadata_weight": 0.1
        } 