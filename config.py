#(©)HighTierBots - Configuration

import os
import logging
from dotenv import load_dotenv

load_dotenv()

# ===== TELEGRAM BOT CREDENTIALS =====
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# ===== LOGGING & ADMIN =====
LOG_GROUP_ID = int(os.environ.get("LOG_GROUP_ID", 0))
OWNERS = [int(x) for x in os.environ.get("OWNERS", "").split(",") if x.strip()] if os.environ.get("OWNERS") else []

# ===== DATABASE =====
DB_URI = os.environ.get("DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "highTierBots")

# ===== BOT MESSAGES =====
BOT_STATS_TEXT = "<b>📊 BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌ Don't send me messages directly. I'm only for create a new bot!"
FORCE_SUB_TEXT = "⚠️ You must join our channel first: {channel_link}\n\nUse /accept after joining."

# ===== VALIDATION =====
def validate_config():
  """Validate required configuration"""
  errors = []
  
  if not API_ID or not API_HASH or not BOT_TOKEN:
    errors.append("Missing: API_ID, API_HASH, or BOT_TOKEN")
  
  if not LOG_GROUP_ID or not OWNERS:
    errors.append("Missing: LOG_GROUP_ID and OWNERS")
  
  if not DB_URI or not DB_NAME:
    errors.append("Missing: DB_URI or DB_NAME")
  
  return errors