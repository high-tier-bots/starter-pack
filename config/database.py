"""
MongoDB database connection and initialization.
"""

import sys
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config.config import Config

class Database:
  """MongoDB database connection handler."""
  
  _instance = None
  _client = None
  _db = None
  
  def __new__(cls):
    """Singleton pattern to ensure only one database connection."""
    if cls._instance is None:
      cls._instance = super(Database, cls).__new__(cls)
    return cls._instance
  
  def __init__(self):
    """Initialize database connection."""
    if self._client is None:
      self.connect()
  
  def connect(self):
    """Establish connection to MongoDB."""
    try:
      print(f"🔄 Connecting to MongoDB...")
      self._client = MongoClient(
        Config.DB_URI,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000
      )
      
      self._client.admin.command('ping')
      
      self._db = self._client[Config.DB_NAME]
      print(f"✅ Connected to MongoDB: {Config.DB_NAME}")
      
      self.create_indexes()
        
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
      print(f"❌ Failed to connect to MongoDB: {e}")
      print("Please ensure MongoDB is running and the connection string is correct.")
      sys.exit(1)
    except Exception as e:
      print(f"❌ Unexpected database error: {e}")
      sys.exit(1)
  
  def create_indexes(self):
    """Create database indexes for better query performance."""
    try:
      users = self._db.users
        
      users.create_index([("user_id", ASCENDING)], unique=True)
      users.create_index([("joined_at", ASCENDING)])
      users.create_index([("last_active", ASCENDING)])
      users.create_index([("is_blocked", ASCENDING)])
      
      print("✅ Database indexes created successfully")
    except Exception as e:
      print(f"⚠️ Warning: Could not create indexes: {e}")
  
  @property
  def db(self):
    """Get database instance."""
    if self._db is None:
      self.connect()
    return self._db

  @property
  def users(self):
    """Get users collection."""
    return self.db.users

  @property
  def bot_stats(self):
    """Get bot_stats collection."""
    return self.db.bot_stats

  @property
  def broadcasts(self):
    """Get broadcasts collection."""
    return self.db.broadcasts
  
  def close(self):
    """Close database connection."""
    if self._client:
      self._client.close()
      print("🔌 MongoDB connection closed")

db = Database()
