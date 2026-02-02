#(©)HighTierBots - Database Configuration

import motor.motor_asyncio
from logger import logger
from datetime import datetime

class Database:
  """MongoDB async database handler"""
  
  def __init__(self, uri, database_name):
    self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    self.db = self._client[database_name]
    self.users_col = self.db.users
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
    
db = None

def init_db(uri, db_name):
  """Initialize database connection"""
  global db
  db = Database(uri, db_name)
  return db
