"""
Timezone-aware datetime utilities
"""

from datetime import datetime, timezone
from typing import Optional


def get_current_time() -> datetime:
    """
    Get current time in UTC with timezone information.
    
    Returns:
        datetime: Current time in UTC with timezone info
    """
    return datetime.now(timezone.utc)


def get_current_time_iso() -> str:
    """
    Get current time in UTC as ISO format string.
    
    Returns:
        str: Current time in ISO format
    """
    return get_current_time().isoformat()


def get_current_time_strftime(format_str: str = "%Y%m%d_%H%M%S") -> str:
    """
    Get current time in UTC as formatted string.
    
    Args:
        format_str: Format string for strftime
        
    Returns:
        str: Current time formatted as string
    """
    return get_current_time().strftime(format_str)


def days_since(date: datetime) -> int:
    """
    Calculate days since a given date.
    
    Args:
        date: The date to calculate from
        
    Returns:
        int: Number of days since the given date
    """
    current = get_current_time()
    if date.tzinfo is None:
        # If date is naive, assume it's UTC
        date = date.replace(tzinfo=timezone.utc)
    return (current - date).days


def ensure_timezone_aware(date: datetime) -> datetime:
    """
    Ensure a datetime object is timezone-aware.
    If it's naive, assume it's UTC.
    
    Args:
        date: The datetime object to make timezone-aware
        
    Returns:
        datetime: Timezone-aware datetime object
    """
    if date.tzinfo is None:
        return date.replace(tzinfo=timezone.utc)
    return date 