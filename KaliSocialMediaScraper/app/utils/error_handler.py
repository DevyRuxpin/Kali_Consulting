"""
Enhanced Error Handling and Logging Utilities
"""

import logging
import traceback
import sys
from typing import Any, Dict, Optional, Callable
from app.utils.type_hints import JSON, LogContext, LogLevel
from datetime import datetime
import json
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)

class ErrorHandler:
    """Comprehensive error handling and logging"""
    
    def __init__(self):
        self.error_counts = {}
        self.error_thresholds = {
            'critical': 5,
            'error': 10,
            'warning': 20
        }
    
    def log_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        level: str = "error"
    ) -> None:
        """Log error with context"""
        error_info = {
            'timestamp': datetime.utcnow().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        
        # Log based on level
        if level == "critical":
            logger.critical(f"CRITICAL ERROR: {json.dumps(error_info, indent=2)}")
        elif level == "error":
            logger.error(f"ERROR: {json.dumps(error_info, indent=2)}")
        elif level == "warning":
            logger.warning(f"WARNING: {json.dumps(error_info, indent=2)}")
        else:
            logger.info(f"INFO: {json.dumps(error_info, indent=2)}")
        
        # Track error counts
        error_key = f"{type(error).__name__}_{level}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        
        # Check if threshold exceeded
        if self.error_counts[error_key] >= self.error_thresholds.get(level, 10):
            logger.critical(f"ERROR THRESHOLD EXCEEDED: {error_key} - {self.error_counts[error_key]} errors")
    
    def handle_exception(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        reraise: bool = True
    ) -> Dict[str, Any]:
        """Handle exception with recovery options"""
        try:
            # Log the error
            self.log_error(error, context)
            
            # Create error response
            error_response = {
                'error': True,
                'error_type': type(error).__name__,
                'error_message': str(error),
                'timestamp': datetime.utcnow().isoformat(),
                'context': context or {}
            }
            
            # Add recovery suggestions based on error type
            if isinstance(error, ConnectionError):
                error_response['suggestion'] = "Check network connectivity and try again"
            elif isinstance(error, TimeoutError):
                error_response['suggestion'] = "Request timed out, try again with longer timeout"
            elif isinstance(error, ValueError):
                error_response['suggestion'] = "Invalid input provided, check parameters"
            elif isinstance(error, PermissionError):
                error_response['suggestion'] = "Insufficient permissions, check access rights"
            else:
                error_response['suggestion'] = "An unexpected error occurred, contact support"
            
            # Reraise if requested
            if reraise:
                raise Exception(str(error))
            
            return error_response
            
        except Exception as e:
            logger.critical(f"Error in error handler: {e}")
            return {
                'error': True,
                'error_type': 'ErrorHandlerException',
                'error_message': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }

class AsyncErrorHandler:
    """Async error handling utilities"""
    
    @staticmethod
    async def handle_async_exception(
        coro: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Handle async function exceptions"""
        try:
            return await coro(*args, **kwargs)
        except Exception as e:
            error_handler = ErrorHandler()
            return error_handler.handle_exception(e, {
                'function': coro.__name__,
                'args': args,
                'kwargs': kwargs
            })

def error_handler_decorator(
    context: Optional[Dict[str, Any]] = None,
    reraise: bool = True
):
    """Decorator for error handling"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler = ErrorHandler()
                return handler.handle_exception(e, context, reraise)
        return wrapper
    return decorator

def async_error_handler_decorator(
    context: Optional[Dict[str, Any]] = None,
    reraise: bool = True
):
    """Decorator for async error handling"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                handler = ErrorHandler()
                return handler.handle_exception(e, context, reraise)
        return wrapper
    return decorator

class RecoveryManager:
    """Error recovery and retry logic"""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    async def retry_with_backoff(
        self,
        func: Callable,
        *args,
        **kwargs
    ) -> Any:
        """Retry function with exponential backoff"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
                    
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    delay = self.base_delay * (2 ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"All {self.max_retries + 1} attempts failed")
                    raise last_exception
        
        raise last_exception

class CircuitBreaker:
    """Circuit breaker pattern implementation"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
            else:
                raise RuntimeError("Circuit breaker is OPEN")
        
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            self._on_success()
            return result
            
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        self.state = "CLOSED"
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt reset"""
        if not self.last_failure_time:
            return True
        
        time_since_failure = (datetime.utcnow() - self.last_failure_time).total_seconds()
        return time_since_failure >= self.timeout

# Global error handler instance
error_handler = ErrorHandler()
recovery_manager = RecoveryManager() 