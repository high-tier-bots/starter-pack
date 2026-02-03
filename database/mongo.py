"""
#(©)HighTierBots - MongoDB operations and database queries.
"""

from config.database import db
from typing import List, Optional
from datetime import datetime, timedelta, timezone


class MongoOperations:
    """Database operations handler."""
    
    @staticmethod
    def add_or_update_user(user_data: dict) -> bool:
      """
      Add a new user or update existing user information.
      
      Args:
          user_data: Dictionary containing user information
          
      Returns:
          True if successful, False otherwise
      """
      try:
        user_id = user_data.get("user_id")
        
        db.users.update_one(
          {"user_id": user_id},
          {
            "$set": {
              "username": user_data.get("username"),
              "first_name": user_data.get("first_name", ""),
              "last_name": user_data.get("last_name"),
              "language_code": user_data.get("language_code", "en"),
              "is_bot": user_data.get("is_bot", False),
              "last_active": datetime.now(timezone.utc),
            },
            "$setOnInsert": {
              "joined_at": datetime.now(timezone.utc),
              "is_blocked": False
            },
            "$inc": {"interaction_count": 1}
          },
          upsert=True
        )
        return True
      except Exception as e:
        print(f"Error adding/updating user: {e}")
        return False
  
    @staticmethod
    def get_user(user_id: int) -> Optional[dict]:
      """Get user by user ID."""
      try:
        return db.users.find_one({"user_id": user_id})
      except Exception as e:
        print(f"Error getting user: {e}")
        return None
  
    @staticmethod
    def is_user_new(user_id: int) -> bool:
      """Check if user is new (not in database)."""
      return db.users.find_one({"user_id": user_id}) is None
  
    @staticmethod
    def get_total_users() -> int:
      """Get total number of users."""
      try:
        return db.users.count_documents({})
      except Exception as e:
        print(f"Error getting total users: {e}")
        return 0

    @staticmethod
    def get_active_users(hours: int = 24) -> int:
      """Get number of active users in the last X hours."""
      try:
        time_threshold = datetime.now(timezone.utc) - timedelta(hours=hours)
        return db.users.count_documents({
          "last_active": {"$gte": time_threshold}
        })
      except Exception as e:
        print(f"Error getting active users: {e}")
        return 0
  
    @staticmethod
    def get_new_users_since(days: int) -> int:
        """Get number of new users since X days ago."""
        try:
            time_threshold = datetime.now(timezone.utc) - timedelta(days=days)
            return db.users.count_documents({
                "joined_at": {"$gte": time_threshold}
            })
        except Exception as e:
            print(f"Error getting new users: {e}")
            return 0
    
    @staticmethod
    def get_all_user_ids(exclude_blocked: bool = True) -> List[int]:
      """Get all user IDs for broadcasting."""
      try:
        query = {"is_blocked": False} if exclude_blocked else {}
        users = db.users.find(query, {"user_id": 1, "_id": 0})
        return [user["user_id"] for user in users]
      except Exception as e:
        print(f"Error getting user IDs: {e}")
        return []
  
    @staticmethod
    def mark_user_blocked(user_id: int):
      """Mark user as blocked (they blocked the bot)."""
      try:
        db.users.update_one(
          {"user_id": user_id},
          {"$set": {"is_blocked": True}}
        )
      except Exception as e:
        print(f"Error marking user as blocked: {e}")
    
    @staticmethod
    def save_broadcast(broadcast_data: dict) -> bool:
      """Save broadcast information to database."""
      try:
        db.broadcasts.insert_one(broadcast_data)
        return True
      except Exception as e:
        print(f"Error saving broadcast: {e}")
        return False
    
    @staticmethod
    def init_bot_stats(start_time: datetime):
      """Initialize bot statistics."""
      try:
        db.bot_stats.update_one(
          {},
          {
            "$setOnInsert": {
              "bot_started_at": start_time
            },
            "$set": {
              "last_updated": datetime.now(timezone.utc)
            }
          },
          upsert=True
        )
      except Exception as e:
        print(f"Error initializing bot stats: {e}")
  
    @staticmethod
    def get_bot_start_time() -> Optional[datetime]:
      """Get bot start time from database."""
      try:
        stats = db.bot_stats.find_one({})
        if stats:
          return stats.get("bot_started_at")
        return None
      except Exception as e:
        print(f"Error getting bot start time: {e}")
        return None
