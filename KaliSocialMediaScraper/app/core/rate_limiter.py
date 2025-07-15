"""
Rate limiting middleware for production use
"""

import time
import asyncio
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import logging
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import redis
import json

logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiter with Redis backend"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_client = redis.from_url(redis_url)
        self.default_limits = {
            "investigations": {"requests": 10, "window": 60},  # 10 requests per minute
            "analysis": {"requests": 20, "window": 60},        # 20 requests per minute
            "exports": {"requests": 5, "window": 60},          # 5 requests per minute
            "social_media": {"requests": 30, "window": 60},    # 30 requests per minute
            "auth": {"requests": 5, "window": 300},            # 5 requests per 5 minutes
            "default": {"requests": 100, "window": 60},        # 100 requests per minute
        }
    
    def get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host
    
    def get_rate_limit_key(self, client_ip: str, endpoint: str) -> str:
        """Generate Redis key for rate limiting"""
        return f"rate_limit:{client_ip}:{endpoint}"
    
    def get_rate_limit_config(self, endpoint: str) -> Dict[str, int]:
        """Get rate limit configuration for endpoint"""
        for key, config in self.default_limits.items():
            if key in endpoint:
                return config
        return self.default_limits["default"]
    
    async def check_rate_limit(self, request: Request, endpoint: str) -> Tuple[bool, Dict[str, any]]:
        """Check if request is within rate limits"""
        try:
            client_ip = self.get_client_ip(request)
            config = self.get_rate_limit_config(endpoint)
            
            key = self.get_rate_limit_key(client_ip, endpoint)
            current_time = int(time.time())
            window_start = current_time - config["window"]
            
            # Get current requests in window
            requests = self.redis_client.zrangebyscore(key, window_start, current_time)
            
            if len(requests) >= config["requests"]:
                # Rate limit exceeded
                oldest_request = self.redis_client.zrange(key, 0, 0, withscores=True)
                if oldest_request:
                    reset_time = oldest_request[0][1] + config["window"]
                    retry_after = reset_time - current_time
                else:
                    retry_after = config["window"]
                
                return False, {
                    "limit": config["requests"],
                    "window": config["window"],
                    "retry_after": retry_after,
                    "reset_time": current_time + retry_after
                }
            
            # Add current request
            self.redis_client.zadd(key, {str(current_time): current_time})
            self.redis_client.expire(key, config["window"])
            
            # Get remaining requests
            remaining = config["requests"] - len(requests) - 1
            
            return True, {
                "limit": config["requests"],
                "remaining": remaining,
                "reset_time": current_time + config["window"]
            }
            
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            # Allow request if rate limiting fails
            return True, {"limit": 100, "remaining": 99, "reset_time": int(time.time()) + 60}
    
    async def rate_limit_middleware(self, request: Request, call_next):
        """Rate limiting middleware"""
        endpoint = request.url.path
        
        # Skip rate limiting for health checks and static files
        if endpoint.startswith("/health") or endpoint.startswith("/static"):
            return await call_next(request)
        
        is_allowed, rate_info = await self.check_rate_limit(request, endpoint)
        
        if not is_allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate limit exceeded",
                    "retry_after": rate_info["retry_after"],
                    "limit": rate_info["limit"],
                    "window": rate_info["window"]
                },
                headers={
                    "Retry-After": str(rate_info["retry_after"]),
                    "X-RateLimit-Limit": str(rate_info["limit"]),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(rate_info["reset_time"])
                }
            )
        
        # Add rate limit headers
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(rate_info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(rate_info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(rate_info["reset_time"])
        
        return response

class TokenBucketRateLimiter:
    """Token bucket rate limiter for more sophisticated rate limiting"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_client = redis.from_url(redis_url)
        self.buckets = {
            "investigations": {"capacity": 10, "refill_rate": 1},  # 1 token per second
            "analysis": {"capacity": 20, "refill_rate": 2},        # 2 tokens per second
            "exports": {"capacity": 5, "refill_rate": 0.5},        # 0.5 tokens per second
            "social_media": {"capacity": 30, "refill_rate": 3},    # 3 tokens per second
            "auth": {"capacity": 5, "refill_rate": 0.1},           # 0.1 tokens per second
            "default": {"capacity": 100, "refill_rate": 10},       # 10 tokens per second
        }
    
    def get_bucket_key(self, client_ip: str, endpoint: str) -> str:
        """Generate Redis key for token bucket"""
        return f"token_bucket:{client_ip}:{endpoint}"
    
    def get_bucket_config(self, endpoint: str) -> Dict[str, float]:
        """Get bucket configuration for endpoint"""
        for key, config in self.buckets.items():
            if key in endpoint:
                return config
        return self.buckets["default"]
    
    async def check_token_bucket(self, request: Request, endpoint: str) -> Tuple[bool, Dict[str, any]]:
        """Check token bucket rate limiting"""
        try:
            client_ip = self.get_client_ip(request)
            config = self.get_bucket_config(endpoint)
            
            key = self.get_bucket_key(client_ip, endpoint)
            current_time = time.time()
            
            # Get current bucket state
            bucket_data = self.redis_client.get(key)
            if bucket_data:
                bucket = json.loads(bucket_data)
            else:
                bucket = {"tokens": config["capacity"], "last_refill": current_time}
            
            # Calculate tokens to add
            time_passed = current_time - bucket["last_refill"]
            tokens_to_add = time_passed * config["refill_rate"]
            
            # Refill bucket
            bucket["tokens"] = min(config["capacity"], bucket["tokens"] + tokens_to_add)
            bucket["last_refill"] = current_time
            
            # Check if we have enough tokens
            if bucket["tokens"] >= 1:
                bucket["tokens"] -= 1
                self.redis_client.setex(key, 3600, json.dumps(bucket))  # Expire in 1 hour
                
                return True, {
                    "tokens": bucket["tokens"],
                    "capacity": config["capacity"],
                    "refill_rate": config["refill_rate"]
                }
            else:
                # Calculate time until next token
                tokens_needed = 1 - bucket["tokens"]
                time_until_token = tokens_needed / config["refill_rate"]
                
                return False, {
                    "tokens": bucket["tokens"],
                    "capacity": config["capacity"],
                    "time_until_token": time_until_token
                }
                
        except Exception as e:
            logger.error(f"Token bucket rate limiting error: {e}")
            return True, {"tokens": 10, "capacity": 10, "refill_rate": 1}
    
    def get_client_ip(self, request: Request) -> str:
        """Get client IP address"""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host

# Global rate limiter instances
rate_limiter = RateLimiter()
token_bucket_limiter = TokenBucketRateLimiter() 