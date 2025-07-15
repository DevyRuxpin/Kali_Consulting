"""
Datetime utilities for timezone-aware operations
"""

from datetime import datetime, timezone
from typing import Optional

def utc_now() -> datetime:
    """Get current UTC time with timezone info"""
    return datetime.now(timezone.utc)

def utc_now_isoformat() -> str:
    """Get current UTC time as ISO format string"""
    return datetime.now(timezone.utc).isoformat()

def utc_now_timestamp() -> float:
    """Get current UTC time as timestamp"""
    return datetime.now(timezone.utc).timestamp()

def days_since(date: datetime) -> int:
    """Calculate days since a given date"""
    if date.tzinfo is None:
        # If date has no timezone, assume UTC
        date = date.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - date).days

def hours_since(date: datetime) -> float:
    """Calculate hours since a given date"""
    if date.tzinfo is None:
        # If date has no timezone, assume UTC
        date = date.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - date).total_seconds() / 3600

def minutes_since(date: datetime) -> float:
    """Calculate minutes since a given date"""
    if date.tzinfo is None:
        # If date has no timezone, assume UTC
        date = date.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - date).total_seconds() / 60 