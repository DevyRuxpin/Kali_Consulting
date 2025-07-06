"""
Advanced Network Analysis Service for Intelligence Correlation
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import json
import networkx as nx
from collections import defaultdict, Counter
import numpy as np

logger = logging.getLogger(__name__)

class NetworkAnalyzer:
    """Advanced network analysis and intelligence correlation service"""
    
    def __init__(self):
        self.graph = nx.Graph()
        self.node_attributes = {}
        self.edge_attributes = {}
        
    async def analyze_network(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
        analysis_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """Analyze network structure and identify patterns"""
        try:
            # Build network graph
            self._build_graph(nodes, edges)
            
            # Perform network analysis
            analysis_results = {
                "network_metrics": await self._calculate_network_metrics(),
                "centrality_analysis": await self._analyze_centrality(),
                "community_detection": await self._detect_communities(),
                "threat_hotspots": await self._identify_threat_hotspots(),
                "influence_analysis": await self._analyze_influence(),
                "temporal_analysis": await self._analyze_temporal_patterns(),
                "correlation_analysis": await self._correlate_intelligence(),
                "analyzed_at": datetime.utcnow().isoformat()
            }
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error in network analysis: {e}")
            return {"error": str(e)}
    
    def _build_graph(self, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]):
        """Build NetworkX graph from nodes and edges"""
        try:
            # Clear existing graph
            self.graph.clear()
            
            # Add nodes
            for node in nodes:
                node_id = node.get("id", str(hash(str(node))))
                self.graph.add_node(
                    node_id,
                    **{
                        "type": node.get("type", "unknown"),
                        "name": node.get("name", str(node_id)),
                        "threat_score": node.get("threat_score", 0),
                        "attributes": node.get("attributes", {})
                    }
                )
                self.node_attributes[node_id] = node.get("attributes", {})
            
            # Add edges
            for edge in edges:
                source_id = edge.get("source_id", "unknown")
                target_id = edge.get("target_id", "unknown")
                
                self.graph.add_edge(
                    source_id,
                    target_id,
                    **{
                        "type": edge.get("type", "unknown"),
                        "weight": edge.get("weight", 1.0),
                        "timestamp": edge.get("timestamp", datetime.utcnow().isoformat()),
                        "attributes": edge.get("attributes", {})
                    }
                )
                self.edge_attributes[(source_id, target_id)] = edge.get("attributes", {})
                
        except Exception as e:
            logger.error(f"Error building graph: {e}")
            raise
    
    async def _calculate_network_metrics(self) -> Dict[str, Any]:
        """Calculate basic network metrics"""
        try:
            metrics = {
                "total_nodes": self.graph.number_of_nodes(),
                "total_edges": self.graph.number_of_edges(),
                "density": nx.density(self.graph),
                "average_clustering": nx.average_clustering(self.graph),
                "average_shortest_path": nx.average_shortest_path_length(self.graph) if nx.is_connected(self.graph) else None,
                "diameter": nx.diameter(self.graph) if nx.is_connected(self.graph) else None,
                "connected_components": nx.number_connected_components(self.graph),
                "largest_component_size": len(max(nx.connected_components(self.graph), key=len)) if self.graph.nodes() else 0
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating network metrics: {e}")
            return {"error": str(e)}
    
    async def _analyze_centrality(self) -> Dict[str, Any]:
        """Analyze node centrality measures"""
        try:
            centrality_measures = {
                "degree_centrality": nx.degree_centrality(self.graph),
                "betweenness_centrality": nx.betweenness_centrality(self.graph),
                "closeness_centrality": nx.closeness_centrality(self.graph),
                "eigenvector_centrality": nx.eigenvector_centrality(self.graph, max_iter=1000) if self.graph.nodes() else {},
                "pagerank": nx.pagerank(self.graph) if self.graph.nodes() else {}
            }
            
            # Find top central nodes
            top_nodes = {}
            for measure_name, measure_values in centrality_measures.items():
                if measure_values:
                    sorted_nodes = sorted(measure_values.items(), key=lambda x: x[1], reverse=True)
                    top_nodes[measure_name] = sorted_nodes[:10]  # Top 10 nodes
            
            return {
                "measures": centrality_measures,
                "top_nodes": top_nodes
            }
            
        except Exception as e:
            logger.error(f"Error analyzing centrality: {e}")
            return {"error": str(e)}
    
    async def _detect_communities(self) -> Dict[str, Any]:
        """Detect communities in the network"""
        try:
            # Use Louvain method for community detection
            communities = nx.community.louvain_communities(self.graph)
            
            community_analysis = {
                "number_of_communities": len(communities),
                "community_sizes": [len(community) for community in communities],
                "largest_community_size": max(len(community) for community in communities) if communities else 0,
                "communities": [
                    {
                        "id": i,
                        "size": len(community),
                        "nodes": list(community),
                        "threat_score": self._calculate_community_threat_score(community)
                    }
                    for i, community in enumerate(communities)
                ]
            }
            
            return community_analysis
            
        except Exception as e:
            logger.error(f"Error detecting communities: {e}")
            return {"error": str(e)}
    
    async def _identify_threat_hotspots(self) -> List[Dict[str, Any]]:
        """Identify threat hotspots in the network"""
        try:
            hotspots = []
            
            # Find nodes with high threat scores
            high_threat_nodes = [
                node for node, attrs in self.graph.nodes(data=True)
                if attrs.get("threat_score", 0) > 70
            ]
            
            # Find clusters of suspicious activity
            for node in high_threat_nodes:
                neighbors = list(self.graph.neighbors(node))
                neighbor_threat_scores = [
                    self.graph.nodes[neighbor].get("threat_score", 0)
                    for neighbor in neighbors
                ]
                
                if neighbor_threat_scores:
                    avg_neighbor_threat = sum(neighbor_threat_scores) / len(neighbor_threat_scores)
                    
                    if avg_neighbor_threat > 50:  # Suspicious cluster
                        hotspots.append({
                            "center_node": node,
                            "neighbors": neighbors,
                            "center_threat_score": self.graph.nodes[node].get("threat_score", 0),
                            "avg_neighbor_threat": avg_neighbor_threat,
                            "cluster_size": len(neighbors) + 1,
                            "risk_level": "high" if avg_neighbor_threat > 70 else "medium"
                        })
            
            return hotspots
            
        except Exception as e:
            logger.error(f"Error identifying threat hotspots: {e}")
            return []
    
    async def _analyze_influence(self) -> Dict[str, Any]:
        """Analyze influence patterns in the network"""
        try:
            influence_analysis = {
                "influencers": [],
                "influence_flow": {},
                "cascade_analysis": {}
            }
            
            # Identify influencers (high centrality nodes)
            centrality = nx.degree_centrality(self.graph)
            top_influencers = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
            
            for node, centrality_score in top_influencers:
                node_attrs = self.graph.nodes[node]
                influence_analysis["influencers"].append({
                    "node": node,
                    "centrality": centrality_score,
                    "threat_score": node_attrs.get("threat_score", 0),
                    "type": node_attrs.get("type", "unknown"),
                    "followers": len(list(self.graph.neighbors(node)))
                })
            
            return influence_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing influence: {e}")
            return {"error": str(e)}
    
    async def _analyze_temporal_patterns(self) -> Dict[str, Any]:
        """Analyze temporal patterns in the network"""
        try:
            temporal_analysis = {
                "activity_timeline": {},
                "growth_patterns": {},
                "seasonal_patterns": {}
            }
            
            # Analyze edge timestamps if available
            edge_timestamps = []
            for edge in self.graph.edges(data=True):
                if "timestamp" in edge[2]:
                    edge_timestamps.append(edge[2]["timestamp"])
            
            if edge_timestamps:
                # Group by time periods
                from collections import defaultdict
                time_periods = defaultdict(int)
                
                for timestamp in edge_timestamps:
                    if isinstance(timestamp, str):
                        try:
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            period = dt.strftime("%Y-%m")
                            time_periods[period] += 1
                        except:
                            continue
                
                temporal_analysis["activity_timeline"] = dict(time_periods)
            
            return temporal_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing temporal patterns: {e}")
            return {"error": str(e)}
    
    async def _correlate_intelligence(self) -> Dict[str, Any]:
        """Correlate intelligence from multiple sources"""
        try:
            correlation_analysis = {
                "cross_references": [],
                "pattern_matches": [],
                "anomaly_detection": [],
                "threat_correlation": {}
            }
            
            # Cross-reference nodes across different types
            node_types = defaultdict(list)
            for node, attrs in self.graph.nodes(data=True):
                node_type = attrs.get("type", "unknown")
                node_types[node_type].append(node)
            
            # Find correlations between different node types
            for type1 in node_types:
                for type2 in node_types:
                    if type1 != type2:
                        common_neighbors = set(node_types[type1]) & set(node_types[type2])
                        if common_neighbors:
                            correlation_analysis["cross_references"].append({
                                "type1": type1,
                                "type2": type2,
                                "common_nodes": list(common_neighbors),
                                "correlation_strength": len(common_neighbors)
                            })
            
            # Detect anomalies
            threat_scores = [attrs.get("threat_score", 0) for attrs in self.graph.nodes(data=True)]
            if threat_scores:
                mean_threat = np.mean(threat_scores)
                std_threat = np.std(threat_scores)
                
                for node, attrs in self.graph.nodes(data=True):
                    threat_score = attrs.get("threat_score", 0)
                    if threat_score > mean_threat + 2 * std_threat:
                        correlation_analysis["anomaly_detection"].append({
                            "node": node,
                            "threat_score": threat_score,
                            "deviation": (threat_score - mean_threat) / std_threat,
                            "type": attrs.get("type", "unknown")
                        })
            
            return correlation_analysis
            
        except Exception as e:
            logger.error(f"Error correlating intelligence: {e}")
            return {"error": str(e)}
    
    def _calculate_community_threat_score(self, community: set) -> float:
        """Calculate threat score for a community"""
        try:
            if not community:
                return 0.0
            
            threat_scores = [
                self.graph.nodes[node].get("threat_score", 0)
                for node in community
            ]
            
            return sum(threat_scores) / len(threat_scores)
            
        except Exception as e:
            logger.error(f"Error calculating community threat score: {e}")
            return 0.0 