"""
Monitoring and logging system for production use
"""

import logging
import time
import json
import traceback
from typing import Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from contextlib import contextmanager
import psutil
import os
from dataclasses import dataclass, asdict
from enum import Enum

class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class PerformanceMetrics:
    """Performance metrics data class"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    active_connections: int
    request_count: int
    error_count: int
    response_time_avg: float
    memory_usage_mb: float
    disk_usage_gb: float

@dataclass
class RequestMetrics:
    """Request metrics data class"""
    endpoint: str
    method: str
    status_code: int
    response_time: float
    client_ip: str
    user_agent: str
    timestamp: str
    error_message: Optional[str] = None

class MonitoringSystem:
    """Comprehensive monitoring system"""
    
    def __init__(self, log_file: str = "logs/app.log", metrics_file: str = "logs/metrics.json"):
        self.log_file = log_file
        self.metrics_file = metrics_file
        self.request_count = 0
        self.error_count = 0
        self.response_times = []
        self.active_connections = 0
        
        # Setup logging
        self.setup_logging()
        
        # Performance tracking
        self.performance_history = []
        self.max_history_size = 1000
        
        # Start background monitoring
        self.start_background_monitoring()
    
    def setup_logging(self):
        """Setup comprehensive logging"""
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def log_request(self, request_metrics: RequestMetrics):
        """Log request metrics"""
        self.request_count += 1
        self.response_times.append(request_metrics.response_time)
        
        # Keep only last 1000 response times
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
        
        if request_metrics.status_code >= 400:
            self.error_count += 1
            self.logger.error(f"Request error: {request_metrics}")
        else:
            self.logger.info(f"Request: {request_metrics}")
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log error with context"""
        self.error_count += 1
        error_data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.logger.error(f"Error: {json.dumps(error_data, indent=2)}")
    
    def log_performance(self, metrics: PerformanceMetrics):
        """Log performance metrics"""
        self.performance_history.append(metrics)
        
        # Keep only recent history
        if len(self.performance_history) > self.max_history_size:
            self.performance_history = self.performance_history[-self.max_history_size:]
        
        # Save to file
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump([asdict(m) for m in self.performance_history[-100:]], f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save metrics: {e}")
    
    def get_system_metrics(self) -> PerformanceMetrics:
        """Get current system metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)  # Reduced interval from 1 second to 0.1 seconds
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
            
            return PerformanceMetrics(
                timestamp=datetime.utcnow().isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                disk_percent=disk.percent,
                active_connections=self.active_connections,
                request_count=self.request_count,
                error_count=self.error_count,
                response_time_avg=avg_response_time,
                memory_usage_mb=memory.used / (1024 * 1024),
                disk_usage_gb=disk.used / (1024 * 1024 * 1024)
            )
        except Exception as e:
            self.logger.error(f"Failed to get system metrics: {e}")
            return PerformanceMetrics(
                timestamp=datetime.utcnow().isoformat(),
                cpu_percent=0,
                memory_percent=0,
                disk_percent=0,
                active_connections=0,
                request_count=0,
                error_count=0,
                response_time_avg=0,
                memory_usage_mb=0,
                disk_usage_gb=0
            )
    
    def start_background_monitoring(self):
        """Start background monitoring tasks"""
        import asyncio
        
        async def monitor_performance():
            while True:
                try:
                    metrics = self.get_system_metrics()
                    self.log_performance(metrics)
                    
                    # Log if system is under stress
                    if metrics.cpu_percent > 80 or metrics.memory_percent > 80:
                        self.logger.warning(f"High system load: CPU {metrics.cpu_percent}%, Memory {metrics.memory_percent}%")
                    
                    await asyncio.sleep(300)  # Monitor every 5 minutes instead of every minute
                except Exception as e:
                    self.logger.error(f"Background monitoring error: {e}")
                    await asyncio.sleep(300)  # 5 minutes
        
        # Start background task
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(monitor_performance())
        except RuntimeError:
            # No event loop, skip background monitoring
            pass
    
    @contextmanager
    def track_request(self, endpoint: str, method: str, client_ip: str, user_agent: str):
        """Context manager to track request performance"""
        start_time = time.time()
        status_code = 200
        error_message = None
        
        try:
            yield
        except Exception as e:
            status_code = 500
            error_message = str(e)
            raise
        finally:
            response_time = time.time() - start_time
            
            metrics = RequestMetrics(
                endpoint=endpoint,
                method=method,
                status_code=status_code,
                response_time=response_time,
                client_ip=client_ip,
                user_agent=user_agent,
                timestamp=datetime.utcnow().isoformat(),
                error_message=error_message
            )
            
            self.log_request(metrics)
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get system health status"""
        metrics = self.get_system_metrics()
        
        # Determine health status
        if metrics.cpu_percent > 90 or metrics.memory_percent > 90:
            status = "critical"
        elif metrics.cpu_percent > 70 or metrics.memory_percent > 70:
            status = "warning"
        else:
            status = "healthy"
        
        return {
            "status": status,
            "timestamp": metrics.timestamp,
            "metrics": asdict(metrics),
            "alerts": self.get_alerts(metrics)
        }
    
    def get_alerts(self, metrics: PerformanceMetrics) -> list:
        """Get system alerts based on metrics"""
        alerts = []
        
        if metrics.cpu_percent > 80:
            alerts.append({
                "type": "high_cpu",
                "message": f"High CPU usage: {metrics.cpu_percent}%",
                "severity": "warning" if metrics.cpu_percent < 90 else "critical"
            })
        
        if metrics.memory_percent > 80:
            alerts.append({
                "type": "high_memory",
                "message": f"High memory usage: {metrics.memory_percent}%",
                "severity": "warning" if metrics.memory_percent < 90 else "critical"
            })
        
        if metrics.disk_percent > 90:
            alerts.append({
                "type": "high_disk",
                "message": f"High disk usage: {metrics.disk_percent}%",
                "severity": "critical"
            })
        
        if metrics.error_count > 10:
            alerts.append({
                "type": "high_errors",
                "message": f"High error count: {metrics.error_count}",
                "severity": "warning"
            })
        
        return alerts

# Global monitoring instance
monitoring = MonitoringSystem() 