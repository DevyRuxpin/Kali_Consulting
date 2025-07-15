"""
WebSocket API endpoints for real-time communication
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict, Any, List
import json
import logging
from datetime import datetime
from app.utils.time_utils import get_current_time_iso

logger = logging.getLogger(__name__)
router = APIRouter()

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_data: Dict[WebSocket, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_data[websocket] = {
            "connected_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
            "message_count": 0
        }
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.connection_data:
            del self.connection_data[websocket]
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send message to specific WebSocket connection"""
        try:
            await websocket.send_text(json.dumps(message))
            if websocket in self.connection_data:
                self.connection_data[websocket]["last_activity"] = datetime.utcnow().isoformat()
                self.connection_data[websocket]["message_count"] += 1
        except Exception as e:
            logger.error(f"Error sending message to WebSocket: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Send message to all connected WebSocket clients"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
                if connection in self.connection_data:
                    self.connection_data[connection]["last_activity"] = datetime.utcnow().isoformat()
                    self.connection_data[connection]["message_count"] += 1
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {e}")
                disconnected.append(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection)
    
    async def send_investigation_update(self, investigation_id: int, data: Dict[str, Any]):
        """Send investigation update to all connected clients"""
        message = {
            "type": "investigation_update",
            "investigation_id": investigation_id,
            "data": data,
            "timestamp": get_current_time_iso()
        }
        await self.broadcast(message)
    
    async def send_threat_alert(self, threat_data: Dict[str, Any]):
        """Send threat alert to all connected clients"""
        message = {
            "type": "threat_alert",
            "data": threat_data,
            "timestamp": get_current_time_iso()
        }
        await self.broadcast(message)
    
    async def send_system_status(self, status_data: Dict[str, Any]):
        """Send system status update to all connected clients"""
        message = {
            "type": "system_status",
            "data": status_data,
            "timestamp": get_current_time_iso()
        }
        await self.broadcast(message)
    
    async def send_metric_update(self, metrics: Dict[str, Any]):
        """Send metric update to all connected clients"""
        message = {
            "type": "metric_update",
            "data": metrics,
            "timestamp": get_current_time_iso()
        }
        await self.broadcast(message)

# Global connection manager
manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Update last activity
            if websocket in manager.connection_data:
                manager.connection_data[websocket]["last_activity"] = datetime.utcnow().isoformat()
            
            # Handle different message types
            await handle_websocket_message(websocket, message)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

async def handle_websocket_message(websocket: WebSocket, message: Dict[str, Any]):
    """Handle incoming WebSocket messages"""
    try:
        message_type = message.get("type")
        
        if message_type == "ping":
            # Respond to ping with pong
            await manager.send_personal_message({
                "type": "pong",
                "timestamp": get_current_time_iso()
            }, websocket)
        
        elif message_type == "subscribe":
            # Handle subscription to specific events
            events = message.get("events", [])
            if websocket in manager.connection_data:
                manager.connection_data[websocket]["subscribed_events"] = events
            
            await manager.send_personal_message({
                "type": "subscribed",
                "events": events,
                "timestamp": get_current_time_iso()
            }, websocket)
        
        elif message_type == "unsubscribe":
            # Handle unsubscription from events
            events = message.get("events", [])
            if websocket in manager.connection_data:
                current_events = manager.connection_data[websocket].get("subscribed_events", [])
                manager.connection_data[websocket]["subscribed_events"] = [
                    e for e in current_events if e not in events
                ]
            
            await manager.send_personal_message({
                "type": "unsubscribed",
                "events": events,
                "timestamp": get_current_time_iso()
            }, websocket)
        
        elif message_type == "get_status":
            # Send current system status
            status_data = {
                "active_connections": len(manager.active_connections),
                "system_health": "operational",
                "last_updated": get_current_time_iso()
            }
            
            await manager.send_personal_message({
                "type": "status_response",
                "data": status_data,
                "timestamp": get_current_time_iso()
            }, websocket)
        
        else:
            # Unknown message type
            await manager.send_personal_message({
                "type": "error",
                "message": f"Unknown message type: {message_type}",
                "timestamp": get_current_time_iso()
            }, websocket)
    
    except Exception as e:
        logger.error(f"Error handling WebSocket message: {e}")
        await manager.send_personal_message({
            "type": "error",
            "message": "Internal server error",
            "timestamp": get_current_time_iso()
        }, websocket)

@router.get("/ws/status")
async def get_websocket_status():
    """Get WebSocket connection status"""
    return {
        "active_connections": len(manager.active_connections),
        "connection_data": {
            str(i): {
                "connected_at": data["connected_at"],
                "last_activity": data["last_activity"],
                "message_count": data["message_count"],
                "subscribed_events": data.get("subscribed_events", [])
            }
            for i, (_, data) in enumerate(manager.connection_data.items())
        },
        "timestamp": get_current_time_iso()
    }

# Export manager for use in other modules
def get_connection_manager() -> ConnectionManager:
    return manager 