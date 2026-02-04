"""
#(©)HighTierBots Data models for MongoDB documents.
"""

from datetime import datetime, timezone
from typing import Optional


class User:
    """User model for MongoDB."""
    
    def __init__(
        self,
        user_id: int,
        username: Optional[str] = None,
        first_name: str = "",
        last_name: Optional[str] = None,
        language_code: Optional[str] = "en",
        is_bot: bool = False
    ):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.language_code = language_code
        self.is_bot = is_bot
        self.joined_at = datetime.now(timezone.utc)
        self.last_active = datetime.now(timezone.utc)
        self.is_blocked = False
        self.interaction_count = 1
    
    def to_dict(self):
        """Convert user object to dictionary for MongoDB."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "language_code": self.language_code,
            "is_bot": self.is_bot,
            "joined_at": self.joined_at,
            "last_active": self.last_active,
            "is_blocked": self.is_blocked,
            "interaction_count": self.interaction_count
        }


class Broadcast:
    """Broadcast model for MongoDB."""
    
    def __init__(
        self,
        message: str,
        sent_by: int,
        total_recipients: int,
        successful: int,
        failed: int
    ):
        self.message = message
        self.sent_by = sent_by
        self.sent_at = datetime.now(timezone.utc)
        self.total_recipients = total_recipients
        self.successful = successful
        self.failed = failed
    
    def to_dict(self):
        """Convert broadcast object to dictionary for MongoDB."""
        return {
            "message": self.message,
            "sent_by": self.sent_by,
            "sent_at": self.sent_at,
            "total_recipients": self.total_recipients,
            "successful": self.successful,
            "failed": self.failed
        }


class BotStats:
    """Bot statistics model for MongoDB."""
    
    def __init__(self, total_users: int, bot_started_at: datetime):
        self.total_users = total_users
        self.bot_started_at = bot_started_at
        self.last_updated = datetime.now(timezone.utc)
    
    def to_dict(self):
        """Convert bot stats object to dictionary for MongoDB."""
        return {
            "total_users": self.total_users,
            "bot_started_at": self.bot_started_at,
            "last_updated": self.last_updated
        }
