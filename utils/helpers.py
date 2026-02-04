"""
#(©)HighTierBots 
Helper utility functions, add more as needed.
"""

from datetime import datetime, timedelta, timezone
import os


def format_uptime(start_time: datetime) -> str:
    """
    Format uptime duration.
    
    Args:
        start_time: Bot start datetime
        
    Returns:
        Formatted uptime string (e.g., "5d 12h 34m")
    """
    if not start_time:
        return "Unknown"
    
    if start_time.tzinfo is None:
        start_time = start_time.replace(tzinfo=timezone.utc)
    
    uptime = datetime.now(timezone.utc) - start_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    
    return " ".join(parts) if parts else "Less than 1m"


def get_database_size() -> str:
    """
    Get database size (approximation).
    
    Returns:
        Formatted database size string
    """
    return "N/A"


def format_number(number: int) -> str:
    """
    Format number with thousand separators.
    
    Args:
        number: Integer to format
        
    Returns:
        Formatted number string (e.g., "1,234")
    """
    return f"{number:,}"


def escape_markdown(text: str) -> str:
    """
    Escape special characters for Markdown.
    
    Args:
        text: Text to escape
        
    Returns:
        Escaped text
    """
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text


def check_banner_exists() -> tuple:
    """
    Check if banner image exists in assets folder.
    
    Returns:
        Tuple of (exists: bool, path: str)
    """
    assets_dir = "assets"
    possible_names = ["directory_banner.jpg", "directory_banner.png", "banner.jpg", "banner.png"]
    
    for name in possible_names:
        path = os.path.join(assets_dir, name)
        if os.path.exists(path):
            return True, path
    
    return False, None


def get_time_periods():
    """
    Get time periods for statistics.
    
    Returns:
        Dictionary with time thresholds
    """
    now = datetime.now(timezone.utc)
    return {
        "today_start": now.replace(hour=0, minute=0, second=0, microsecond=0),
        "week_start": now - timedelta(days=7),
        "month_start": now - timedelta(days=30)
    }
