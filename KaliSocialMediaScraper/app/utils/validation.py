"""
Input Validation and Sanitization Utilities
"""

import re
import html
import urllib.parse
from typing import Any, Dict, List, Optional, Union
from app.utils.type_hints import JSON, ValidationResult, is_valid_string, is_valid_dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class InputValidator:
    """Comprehensive input validation and sanitization"""
    
    # Regex patterns for validation
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    URL_PATTERN = re.compile(r'^https?://[^\s/$.?#].[^\s]*$')
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9._-]{3,30}$')
    DOMAIN_PATTERN = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$')
    IP_PATTERN = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    
    # Dangerous patterns to filter
    DANGEROUS_PATTERNS = [
        re.compile(r'<script', re.IGNORECASE),
        re.compile(r'javascript:', re.IGNORECASE),
        re.compile(r'on\w+\s*=', re.IGNORECASE),
        re.compile(r'data:text/html', re.IGNORECASE),
        re.compile(r'vbscript:', re.IGNORECASE),
        re.compile(r'expression\s*\(', re.IGNORECASE),
        re.compile(r'<iframe', re.IGNORECASE),
        re.compile(r'<object', re.IGNORECASE),
        re.compile(r'<embed', re.IGNORECASE),
    ]
    
    @classmethod
    def sanitize_string(cls, value: str, max_length: int = 1000) -> str:
        """Sanitize a string input"""
        if not isinstance(value, str):
            raise ValueError("Input must be a string")
        
        # Truncate if too long
        if len(value) > max_length:
            value = value[:max_length]
        
        # HTML escape
        value = html.escape(value)
        
        # Remove dangerous patterns
        for pattern in cls.DANGEROUS_PATTERNS:
            value = pattern.sub('', value)
        
        # Remove null bytes and control characters
        value = ''.join(char for char in value if ord(char) >= 32 or char in '\n\r\t')
        
        return value.strip()
    
    @classmethod
    def validate_email(cls, email: str) -> bool:
        """Validate email format"""
        if not isinstance(email, str):
            return False
        return bool(cls.EMAIL_PATTERN.match(email.strip()))
    
    @classmethod
    def validate_url(cls, url: str) -> bool:
        """Validate URL format"""
        if not isinstance(url, str):
            return False
        return bool(cls.URL_PATTERN.match(url.strip()))
    
    @classmethod
    def validate_username(cls, username: str) -> bool:
        """Validate username format"""
        if not isinstance(username, str):
            return False
        return bool(cls.USERNAME_PATTERN.match(username.strip()))
    
    @classmethod
    def validate_domain(cls, domain: str) -> bool:
        """Validate domain format"""
        if not isinstance(domain, str):
            return False
        return bool(cls.DOMAIN_PATTERN.match(domain.strip()))
    
    @classmethod
    def validate_ip(cls, ip: str) -> bool:
        """Validate IP address format"""
        if not isinstance(ip, str):
            return False
        return bool(cls.IP_PATTERN.match(ip.strip()))
    
    @classmethod
    def validate_investigation_target(cls, target: str, target_type: str) -> bool:
        """Validate investigation target based on type"""
        if not isinstance(target, str) or not target.strip():
            return False
        
        target = target.strip()
        
        if target_type == "email":
            return cls.validate_email(target)
        elif target_type == "domain":
            return cls.validate_domain(target)
        elif target_type == "username":
            return cls.validate_username(target)
        elif target_type == "url":
            return cls.validate_url(target)
        elif target_type == "ip":
            return cls.validate_ip(target)
        else:
            # For unknown types, just check basic string validation
            return len(target) >= 3 and len(target) <= 255
    
    @classmethod
    def sanitize_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize dictionary values"""
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized[key] = cls.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[key] = cls.sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = cls.sanitize_list(value)
            else:
                sanitized[key] = value
        return sanitized
    
    @classmethod
    def sanitize_list(cls, data: List[Any]) -> List[Any]:
        """Sanitize list values"""
        sanitized = []
        for item in data:
            if isinstance(item, str):
                sanitized.append(cls.sanitize_string(item))
            elif isinstance(item, dict):
                sanitized.append(cls.sanitize_dict(item))
            elif isinstance(item, list):
                sanitized.append(cls.sanitize_list(item))
            else:
                sanitized.append(item)
        return sanitized
    
    @classmethod
    def validate_date_range(cls, start_date: str, end_date: str) -> bool:
        """Validate date range"""
        try:
            start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            return start <= end
        except (ValueError, TypeError):
            return False
    
    @classmethod
    def validate_pagination_params(cls, page: int, size: int, max_size: int = 100) -> bool:
        """Validate pagination parameters"""
        return (
            isinstance(page, int) and page >= 1 and
            isinstance(size, int) and 1 <= size <= max_size
        )

class SQLInjectionValidator:
    """SQL injection prevention utilities"""
    
    # SQL keywords to check for
    SQL_KEYWORDS = [
        'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER',
        'UNION', 'EXEC', 'EXECUTE', 'DECLARE', 'CAST', 'CONVERT'
    ]
    
    @classmethod
    def contains_sql_injection(cls, value: str) -> bool:
        """Check if string contains potential SQL injection"""
        if not isinstance(value, str):
            return False
        
        # Convert to uppercase for checking
        upper_value = value.upper()
        
        # Check for SQL keywords
        for keyword in cls.SQL_KEYWORDS:
            if keyword in upper_value:
                return True
        
        # Check for common SQL injection patterns
        patterns = [
            r'--',  # SQL comments
            r'/\*.*\*/',  # SQL block comments
            r'xp_',  # Extended stored procedures
            r'sp_',  # Stored procedures
            r'@@',  # SQL Server variables
            r'WAITFOR',  # SQL Server delay
            r'BENCHMARK',  # MySQL delay
            r'SLEEP',  # MySQL delay
        ]
        
        for pattern in patterns:
            if re.search(pattern, upper_value, re.IGNORECASE):
                return True
        
        return False

class XSSValidator:
    """XSS prevention utilities"""
    
    @classmethod
    def contains_xss(cls, value: str) -> bool:
        """Check if string contains potential XSS"""
        if not isinstance(value, str):
            return False
        
        # Check for common XSS patterns
        patterns = [
            r'<script',  # Script tags
            r'javascript:',  # JavaScript protocol
            r'on\w+\s*=',  # Event handlers
            r'data:text/html',  # Data URLs
            r'vbscript:',  # VBScript
            r'expression\s*\(',  # CSS expressions
            r'<iframe',  # Iframe tags
            r'<object',  # Object tags
            r'<embed',  # Embed tags
            r'<form',  # Form tags
            r'<input',  # Input tags
            r'<textarea',  # Textarea tags
            r'<select',  # Select tags
            r'<button',  # Button tags
        ]
        
        for pattern in patterns:
            if re.search(pattern, value, re.IGNORECASE):
                return True
        
        return False

def validate_and_sanitize_input(
    data: Union[str, Dict[str, Any], List[Any]],
    input_type: str = "general"
) -> Union[str, Dict[str, Any], List[Any]]:
    """Main validation and sanitization function"""
    try:
        if isinstance(data, str):
            # Check for SQL injection
            if SQLInjectionValidator.contains_sql_injection(data):
                raise ValueError("Input contains potential SQL injection")
            
            # Check for XSS
            if XSSValidator.contains_xss(data):
                raise ValueError("Input contains potential XSS")
            
            return InputValidator.sanitize_string(data)
        
        elif isinstance(data, dict):
            return InputValidator.sanitize_dict(data)
        
        elif isinstance(data, list):
            return InputValidator.sanitize_list(data)
        
        else:
            return data
            
    except Exception as e:
        logger.error(f"Input validation failed: {e}")
        raise ValueError(f"Invalid input: {e}")

def validate_investigation_request(
    target: str,
    target_type: str,
    date_range: Optional[Dict[str, str]] = None
) -> bool:
    """Validate investigation request parameters"""
    try:
        # Validate target
        if not InputValidator.validate_investigation_target(target, target_type):
            return False
        
        # Validate date range if provided
        if date_range:
            start_date = date_range.get('start_date')
            end_date = date_range.get('end_date')
            if start_date and end_date:
                if not InputValidator.validate_date_range(start_date, end_date):
                    return False
        
        return True
        
    except Exception as e:
        logger.error(f"Investigation request validation failed: {e}")
        return False 