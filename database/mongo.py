#(©)HighTierBots - Database Configuration

import motor.motor_asyncio
from utils.logger import logger
from datetime import datetime

class Database:
  """MongoDB async database handler"""
  
  def __init__(self, uri, database_name):
    self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    self.db = self._client[database_name]
    self.users_col = self.db.users
    self.admins_col = self.db.admins
    self.channels_col = self.db.channels
    self.debug_logs_col = self.db.debug_logs
    self.groups_col = self.db.groups
    self.requests_col = self.db.requests
    logger.info("Database initialized")

  def new_user(self, id, name):
    """Create new user document"""
    return dict(
      id=id,
      name=name,
      session=None,
      joined_at=datetime.now(),
    )
  
  # ===== USER METHODS =====
  
  async def is_user_exist(self, user_id):
    """Check if user exists in database"""
    try:
      user = await self.users_col.find_one({"id": user_id})
      return user is not None
    except Exception as e:
      logger.error(f"Error checking user existence: {e}")
      return False
  
  async def add_user(self, user_id, name):
    """Add new user to database"""
    try:
      existing = await self.users_col.find_one({"id": user_id})
      if existing:
        logger.warning(f"User {user_id} already exists")
        return False
      
      user_doc = self.new_user(user_id, name)
      result = await self.users_col.insert_one(user_doc)
      logger.info(f"User {user_id} added to database")
      return result.inserted_id
    except Exception as e:
      logger.error(f"Error adding user {user_id}: {e}")
      return False
  
  async def get_session(self, user_id):
    """Get user session from database"""
    try:
      user = await self.users_col.find_one({"id": user_id})
      if user:
        return user.get("session")
      return None
    except Exception as e:
      logger.error(f"Error getting session for user {user_id}: {e}")
      return None
  
  async def delete_user(self, user_id):
    """Delete user from database"""
    try:
      result = await self.users_col.delete_one({"id": user_id})
      logger.info(f"User {user_id} deleted from database")
      return result.deleted_count > 0
    except Exception as e:
      logger.error(f"Error deleting user {user_id}: {e}")
      return False
  
  async def get_all_users(self):
    """Get all users as async cursor"""
    try:
      return self.users_col.find({})
    except Exception as e:
      logger.error(f"Error retrieving all users: {e}")
      return None
  
  async def total_users_count(self):
    """Get total count of users"""
    try:
      count = await self.users_col.count_documents({})
      return count
    except Exception as e:
      logger.error(f"Error counting users: {e}")
      return 0
  
  # ===== ADMIN METHODS =====
  
  async def is_admin(self, user_id):
    """Check if user is admin"""
    try:
      admin = await self.admins_col.find_one({"user_id": user_id})
      return admin is not None
    except Exception as e:
      logger.error(f"Error checking admin status for {user_id}: {e}")
      return False
  
  async def add_admin(self, user_id):
    """Add user as admin"""
    try:
      existing = await self.admins_col.find_one({"user_id": user_id})
      if existing:
        logger.warning(f"User {user_id} is already an admin")
        return False
      
      admin_doc = {
        "user_id": user_id,
        "added_at": datetime.now()
      }
      result = await self.admins_col.insert_one(admin_doc)
      logger.info(f"User {user_id} added as admin")
      return result.inserted_id
    except Exception as e:
      logger.error(f"Error adding admin {user_id}: {e}")
      return False
  
  async def remove_admin(self, user_id):
    """Remove user as admin"""
    try:
      result = await self.admins_col.delete_one({"user_id": user_id})
      logger.info(f"User {user_id} removed from admins")
      return result.deleted_count > 0
    except Exception as e:
      logger.error(f"Error removing admin {user_id}: {e}")
      return False
  
  async def total_admins_count(self):
    """Get total count of admins"""
    try:
      count = await self.admins_col.count_documents({})
      return count
    except Exception as e:
      logger.error(f"Error counting admins: {e}")
      return 0
  
  # ===== CHANNEL METHODS =====
  
  async def get_channel(self, channel_id):
    """Get channel from database"""
    try:
      channel = await self.channels_col.find_one({"channel_id": channel_id})
      return channel
    except Exception as e:
      logger.error(f"Error getting channel {channel_id}: {e}")
      return None
  
  async def add_channel(self, channel_id):
    """Add channel to database"""
    try:
      existing = await self.channels_col.find_one({"channel_id": channel_id})
      if existing:
        logger.warning(f"Channel {channel_id} already exists")
        return False
      
      channel_doc = {
        "channel_id": channel_id,
        "added_at": datetime.now()
      }
      result = await self.channels_col.insert_one(channel_doc)
      logger.info(f"Channel {channel_id} added to database")
      return result.inserted_id
    except Exception as e:
      logger.error(f"Error adding channel {channel_id}: {e}")
      return False
  
  async def remove_channel(self, channel_id):
    """Remove channel from database"""
    try:
      result = await self.channels_col.delete_one({"channel_id": channel_id})
      logger.info(f"Channel {channel_id} removed from database")
      return result.deleted_count > 0
    except Exception as e:
      logger.error(f"Error removing channel {channel_id}: {e}")
      return False
  
  async def total_channels_count(self):
    """Get total count of channels"""
    try:
      count = await self.channels_col.count_documents({})
      return count
    except Exception as e:
      logger.error(f"Error counting channels: {e}")
      return 0
  
  # ===== FORCE MODE METHODS =====
  
  async def set_force_mode(self, enabled):
    """Set force subscription mode"""
    try:
      result = await self.db.settings.update_one(
        {"_id": "force_mode"},
        {"$set": {"enabled": enabled, "updated_at": datetime.now()}},
        upsert=True
      )
      logger.info(f"Force mode set to {enabled}")
      return True
    except Exception as e:
      logger.error(f"Error setting force mode: {e}")
      return False
  
  async def get_force_mode(self):
    """Get current force subscription mode"""
    try:
      setting = await self.db.settings.find_one({"_id": "force_mode"})
      if setting:
        return setting.get("enabled", False)
      return False
    except Exception as e:
      logger.error(f"Error getting force mode: {e}")
      return False
  
  # ===== DEBUG LOGS METHODS =====
  
  async def log_error_to_debug_logs(self, command, user_id, error, suggested_fix):
    """Log error to debug_logs collection"""
    try:
      log_doc = {
        "command": command,
        "user_id": user_id,
        "error": error,
        "suggested_fix": suggested_fix,
        "timestamp": datetime.now()
      }
      result = await self.debug_logs_col.insert_one(log_doc)
      logger.info(f"Error logged for command {command}")
      return result.inserted_id
    except Exception as e:
      logger.error(f"Error logging to debug_logs: {e}")
      return False
  
  async def get_last_debug_log(self):
    """Get the most recent debug log"""
    try:
      log = await self.debug_logs_col.find_one(
        {},
        sort=[("timestamp", -1)]
      )
      return log
    except Exception as e:
      logger.error(f"Error retrieving last debug log: {e}")
      return None
  
  async def total_debug_logs_count(self):
    """Get total count of debug logs"""
    try:
      count = await self.debug_logs_col.count_documents({})
      return count
    except Exception as e:
      logger.error(f"Error counting debug logs: {e}")
      return 0
  
  # ===== STATISTICS METHODS =====
  
  async def total_groups_count(self):
    """Get total count of groups"""
    try:
      count = await self.groups_col.count_documents({})
      return count
    except Exception as e:
      logger.error(f"Error counting groups: {e}")
      return 0
  
  async def total_approved_count(self):
    """Get total count of approved requests"""
    try:
      count = await self.requests_col.count_documents({"status": "approved"})
      return count
    except Exception as e:
      logger.error(f"Error counting approved requests: {e}")
      return 0
  
  async def total_pending_count(self):
    """Get total count of pending requests"""
    try:
      count = await self.requests_col.count_documents({"status": "pending"})
      return count
    except Exception as e:
      logger.error(f"Error counting pending requests: {e}")
      return 0
    
db = None

def init_db(uri, db_name):
  """Initialize database connection"""
  global db
  db = Database(uri, db_name)
  return db
