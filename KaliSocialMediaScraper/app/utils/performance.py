"""
Performance Optimization Utilities
"""

import asyncio
import time
import functools
from typing import Any, Callable, Dict, List, Optional, Union
from datetime import datetime, timedelta
import logging
from collections import OrderedDict
import json
import hashlib

from app.utils.type_hints import JSON, CacheKey, CacheValue

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor and track performance metrics"""
    
    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
        self.start_times: Dict[str, float] = {}
    
    def start_timer(self, operation: str) -> None:
        """Start timing an operation"""
        self.start_times[operation] = time.time()
    
    def end_timer(self, operation: str) -> float:
        """End timing an operation and return duration"""
        if operation not in self.start_times:
            return 0.0
        
        duration = time.time() - self.start_times[operation]
        if operation not in self.metrics:
            self.metrics[operation] = []
        self.metrics[operation].append(duration)
        
        # Keep only last 100 measurements
        if len(self.metrics[operation]) > 100:
            self.metrics[operation] = self.metrics[operation][-100:]
        
        del self.start_times[operation]
        return duration
    
    def get_average_time(self, operation: str) -> float:
        """Get average time for an operation"""
        if operation not in self.metrics or not self.metrics[operation]:
            return 0.0
        return sum(self.metrics[operation]) / len(self.metrics[operation])
    
    def get_performance_report(self) -> JSON:
        """Get comprehensive performance report"""
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "operations": {}
        }
        
        for operation, times in self.metrics.items():
            if times:
                report["operations"][operation] = {
                    "count": len(times),
                    "average_time": sum(times) / len(times),
                    "min_time": min(times),
                    "max_time": max(times),
                    "total_time": sum(times)
                }
        
        return report

class AsyncCache:
    """Async cache with TTL and size limits"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: OrderedDict[str, tuple[CacheValue, float]] = OrderedDict()
    
    def _generate_key(self, *args, **kwargs) -> CacheKey:
        """Generate cache key from arguments"""
        key_data = {
            "args": args,
            "kwargs": sorted(kwargs.items())
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    async def get(self, key: CacheKey) -> Optional[CacheValue]:
        """Get value from cache"""
        if key in self.cache:
            value, expiry = self.cache[key]
            if time.time() < expiry:
                # Move to end (LRU)
                self.cache.move_to_end(key)
                return value
            else:
                # Expired
                del self.cache[key]
        return None
    
    async def set(self, key: CacheKey, value: CacheValue, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        expiry = time.time() + (ttl or self.default_ttl)
        
        # Remove if already exists
        if key in self.cache:
            del self.cache[key]
        
        # Evict oldest if at capacity
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)
        
        self.cache[key] = (value, expiry)
    
    async def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
    
    async def cleanup_expired(self) -> int:
        """Remove expired entries and return count"""
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry) in self.cache.items()
            if current_time >= expiry
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        return len(expired_keys)

def async_cache(ttl: Optional[int] = None, max_size: int = 1000):
    """Decorator for async function caching"""
    cache = AsyncCache(max_size=max_size)
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = cache._generate_key(*args, **kwargs)
            
            # Try to get from cache
            cached_result = await cache.get(key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache result
            await cache.set(key, result, ttl)
            logger.debug(f"Cached result for {func.__name__}")
            
            return result
        return wrapper
    return decorator

def performance_monitor(operation_name: Optional[str] = None):
    """Decorator for performance monitoring"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            monitor = PerformanceMonitor()
            op_name = operation_name or func.__name__
            
            monitor.start_timer(op_name)
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = monitor.end_timer(op_name)
                logger.info(f"{op_name} completed in {duration:.3f}s")
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            monitor = PerformanceMonitor()
            op_name = operation_name or func.__name__
            
            monitor.start_timer(op_name)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = monitor.end_timer(op_name)
                logger.info(f"{op_name} completed in {duration:.3f}s")
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    return decorator

class QueryOptimizer:
    """Database query optimization utilities"""
    
    @staticmethod
    def optimize_select_query(columns: List[str], table: str, conditions: Optional[Dict[str, Any]] = None) -> str:
        """Optimize SELECT query"""
        # Only select needed columns
        select_clause = ", ".join(columns) if columns else "*"
        query = f"SELECT {select_clause} FROM {table}"
        
        if conditions:
            where_clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])
            query += f" WHERE {where_clause}"
        
        return query
    
    @staticmethod
    def add_pagination(query: str, limit: int, offset: int) -> str:
        """Add pagination to query"""
        return f"{query} LIMIT {limit} OFFSET {offset}"
    
    @staticmethod
    def add_ordering(query: str, order_by: str, direction: str = "ASC") -> str:
        """Add ordering to query"""
        return f"{query} ORDER BY {order_by} {direction.upper()}"

class AsyncBatchProcessor:
    """Process items in batches asynchronously"""
    
    def __init__(self, batch_size: int = 100, max_concurrency: int = 10):
        self.batch_size = batch_size
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
    
    async def process_batch(
        self,
        items: List[Any],
        processor: Callable,
        *args,
        **kwargs
    ) -> List[Any]:
        """Process items in batches"""
        results = []
        
        # Process in batches
        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            
            async with self.semaphore:
                batch_results = await asyncio.gather(
                    *[processor(item, *args, **kwargs) for item in batch],
                    return_exceptions=True
                )
                
                # Filter out exceptions
                valid_results = [
                    result for result in batch_results
                    if not isinstance(result, Exception)
                ]
                results.extend(valid_results)
        
        return results

class MemoryOptimizer:
    """Memory usage optimization utilities"""
    
    @staticmethod
    def optimize_dict_size(data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize dictionary memory usage"""
        optimized = {}
        
        for key, value in data.items():
            if isinstance(value, str) and len(value) > 1000:
                # Truncate long strings
                optimized[key] = value[:1000] + "..."
            elif isinstance(value, dict):
                optimized[key] = MemoryOptimizer.optimize_dict_size(value)
            elif isinstance(value, list) and len(value) > 100:
                # Limit list size
                optimized[key] = value[:100]
            else:
                optimized[key] = value
        
        return optimized
    
    @staticmethod
    def get_memory_usage() -> Dict[str, Any]:
        """Get current memory usage"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            "rss": memory_info.rss,  # Resident Set Size
            "vms": memory_info.vms,  # Virtual Memory Size
            "percent": process.memory_percent(),
            "available": psutil.virtual_memory().available
        }

# Global instances
performance_monitor_instance = PerformanceMonitor()
async_cache_instance = AsyncCache()

# Utility functions
def get_performance_report() -> JSON:
    """Get current performance report"""
    return performance_monitor_instance.get_performance_report()

async def get_cache_stats() -> JSON:
    """Get cache statistics"""
    expired_count = await async_cache_instance.cleanup_expired()
    
    return {
        "cache_size": len(async_cache_instance.cache),
        "max_size": async_cache_instance.max_size,
        "expired_removed": expired_count,
        "hit_rate": "N/A"  # Would need to track hits/misses
    }

def optimize_response_size(response_data: Any, max_size: int = 1024 * 1024) -> Any:
    """Optimize response size for transmission"""
    if isinstance(response_data, dict):
        return MemoryOptimizer.optimize_dict_size(response_data)
    elif isinstance(response_data, list) and len(response_data) > 1000:
        return response_data[:1000]  # Limit large lists
    else:
        return response_data 