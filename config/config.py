"""
#(©)HighTierBots - Configuration loader for the Telegram bot.
Loads environment variables and provides them to the application.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  """Bot configuration class."""
    
  # ===== TELEGRAM BOT CREDENTIALS =====
  API_ID = int(os.environ.get("API_ID", 0))
  API_HASH = os.environ.get("API_HASH", "")
  BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

  # ===== LOGGING & ADMIN =====
  OWNER_ID = int(os.getenv("OWNER_ID", 0))
  OWNER_USERNAME = os.getenv("OWNER_USERNAME", "sahilkumardev")
  LOG_GROUP_ID = int(os.environ.get("LOG_GROUP_ID", 0))

  # ===== DATABASE =====
  DB_URI = os.environ.get("DB_URI", "")
  DB_NAME = os.environ.get("DB_NAME", "highTierBots")


  # ===== VALIDATION =====
  @staticmethod
  def validate_config():
    """Validate required configuration"""
    
    if not Config.API_ID or not Config.API_HASH or not Config.BOT_TOKEN:
      raise ValueError("Missing: API_ID, API_HASH, or BOT_TOKEN")
    
    if not Config.LOG_GROUP_ID or not Config.OWNER_ID or not Config.OWNER_USERNAME:
      raise ValueError("Missing: LOG_GROUP_ID, OWNER_ID, or OWNER_USERNAME")
    
    if not Config.DB_URI or not Config.DB_NAME:
      raise ValueError("Missing: DB_URI or DB_NAME")
    
    print("✅ Configuration validated successfully")
    return True

try:
  Config.validate_config()
except ValueError as e:
  print(f"❌ Configuration Error: {e}")
  print("Please check your .env file and ensure all required variables are set.")
  exit(1)
