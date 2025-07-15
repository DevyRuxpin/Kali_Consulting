"""
Middleware for request processing, rate limiting, and logging
"""

import time
import logging
from typing import Callable, Dict, Any
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import json
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio
from app.core.config import settings

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.requests: Dict[str, list] = defaultdict(list)
        self.rate_limit_requests = settings.RATE_LIMIT_REQUESTS
        self.rate_limit_window = settings.RATE_LIMIT_WINDOW
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Clean old requests
        now = time.time()
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < self.rate_limit_window
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.rate_limit_requests:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Limit: {self.rate_limit_requests} per {self.rate_limit_window} seconds"
                }
            )
        
        # Add current request
        self.requests[client_ip].append(now)
        
        return await call_next(request)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Request/response logging middleware"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Log request
        client_host = getattr(request.client, 'host', 'unknown') if request.client else 'unknown'
        logger.info(f"Request: {request.method} {request.url} from {client_host}")
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log response
            logger.info(f"Response: {request.method} {request.url} - {response.status_code} - {process_time:.3f}s")
            
            # Add timing header
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"Error processing request: {request.method} {request.url} - {str(e)} - {process_time:.3f}s")
            raise

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Global error handling middleware"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except HTTPException:
            # Re-raise HTTP exceptions as they are handled by FastAPI
            raise
        except Exception as e:
            # Log the error
            logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            
            # Return a generic error response
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "message": "An unexpected error occurred",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

class SecurityMiddleware(BaseHTTPMiddleware):
    """Security headers middleware"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response

class InputValidationMiddleware(BaseHTTPMiddleware):
    """Input validation and sanitization middleware"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.suspicious_patterns = [
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>.*?</iframe>",
            r"<object[^>]*>.*?</object>",
            r"<embed[^>]*>",
            r"<form[^>]*>.*?</form>",
            r"<input[^>]*>",
            r"<textarea[^>]*>.*?</textarea>",
            r"<select[^>]*>.*?</select>",
        ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Validate request body for POST/PUT requests
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    body_str = body.decode('utf-8')
                    if self._contains_suspicious_content(body_str):
                        logger.warning(f"Suspicious content detected in request from {request.client.host}")
                        return JSONResponse(
                            status_code=400,
                            content={
                                "error": "Invalid input",
                                "message": "Request contains potentially malicious content"
                            }
                        )
            except Exception as e:
                logger.error(f"Error validating request body: {e}")
        
        return await call_next(request)
    
    def _contains_suspicious_content(self, content: str) -> bool:
        """Check for suspicious content patterns"""
        import re
        content_lower = content.lower()
        
        for pattern in self.suspicious_patterns:
            if re.search(pattern, content_lower, re.IGNORECASE):
                return True
        
        return False

class CachingMiddleware(BaseHTTPMiddleware):
    """Response caching middleware"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.cache: Dict[str, tuple] = {}
        self.cache_ttl = 300  # 5 minutes
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Only cache GET requests
        if request.method != "GET":
            return await call_next(request)
        
        # Create cache key
        cache_key = f"{request.url}"
        
        # Check cache
        if cache_key in self.cache:
            cached_response, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                logger.debug(f"Cache hit for: {request.url}")
                return cached_response
        
        # Get response
        response = await call_next(request)
        
        # Cache successful responses
        if response.status_code == 200:
            self.cache[cache_key] = (response, time.time())
            logger.debug(f"Cached response for: {request.url}")
        
        return response

# Middleware stack
def setup_middleware(app):
    """Setup all middleware"""
    from fastapi import FastAPI
    if isinstance(app, FastAPI):
        app.add_middleware(ErrorHandlingMiddleware)
        app.add_middleware(SecurityMiddleware)
        app.add_middleware(InputValidationMiddleware)
        app.add_middleware(RateLimitMiddleware)
        app.add_middleware(LoggingMiddleware)
        app.add_middleware(CachingMiddleware)
    
    return app 