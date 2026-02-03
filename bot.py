"""
#(©)HighTierBots - Bot main file
Main bot file with instilization and command setup
"""

import sys
from datetime import datetime, timezone
from pyrogram import Client, filters, idle
from pyrogram.types import Message

# Import configuration
from config.config import Config
from config.database import db

# Import database operations
from database.mongo import MongoOperations

# Import handlers
from handlers.start import start_command
from handlers.broadcast import broadcast_command
from handlers.stats import stats_command

# Import utilities
from utils.logger import Logger


class HighTierBots:
  """Main HighTierBots Bot class."""
  
  def __init__(self):
    """Initialize the bot."""
    self.app = None
    self.logger = None
    self.start_time = datetime.now(timezone.utc)
    
    print("=" * 60)
    print("🤖 HighTierBots starter pack")
    print("=" * 60)
    print(f"Bot Owner: @{Config.OWNER_USERNAME}")
    print(f"Owner ID: {Config.OWNER_ID}")
    print(f"Database: {Config.DB_NAME}")
    print("=" * 60)
  
  def setup_application(self):
    """Set up the bot application."""
    try:
      self.app = Client(
        name="HighTierBots",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        bot_token=Config.BOT_TOKEN
      )
      
      print("✅ Bot application created successfully")
      return True
      
    except Exception as e:
      print(f"❌ Failed to create bot application: {e}")
      return False
  
  def register_handlers(self):
    """Register command handlers."""
    try:
      # Public commands
      @self.app.on_message(filters.command("start") & filters.private)
      async def handle_start(client: Client, message: Message):
        await start_command(client, message)
      
      # Owner-only commands
      @self.app.on_message(filters.command("broadcast") & filters.private)
      async def handle_broadcast(client: Client, message: Message):
        await broadcast_command(client, message)
      
      @self.app.on_message(filters.command("stats") & filters.private)
      async def handle_stats(client: Client, message: Message):
        await stats_command(client, message)
      
      print("✅ Command handlers registered successfully")
      print("   • /start (public)")
      print("   • /broadcast (owner only)")
      print("   • /stats (owner only)")
      return True
        
    except Exception as e:
      print(f"❌ Failed to register handlers: {e}")
      return False

  async def start_bot(self):
    """Start the bot."""
    try:
      await self.app.start()
       
      self.logger = Logger(self.app)
      self.app._logger = self.logger
       
      MongoOperations.init_bot_stats(self.start_time)
       
      total_users = MongoOperations.get_total_users()
      
      await self.logger.log_bot_started(total_users)
      
      print(f"✅ Bot started successfully at {self.start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
      print(f"📊 Total users in database: {total_users:,}")
      print("\n" + "=" * 60)
      print("✅ Bot is now running!")
      print("Press Ctrl+C to stop the bot")
      print("=" * 60 + "\n")
       
      await idle()
      
    except KeyboardInterrupt:
      print("\n⚠️ Bot stopped by user (Ctrl+C)")
    except Exception as e:
      print(f"\n❌ Error during bot operation: {e}")
      raise
    finally:
      await self.stop_bot()
  
  async def stop_bot(self):
    """Stop the bot."""
    try:
      print("\n🔄 Shutting down bot...")
      if self.app.is_connected:
        await self.app.stop()
      db.close()
      print("✅ Bot shutdown complete")
    except Exception as e:
      print(f"⚠️ Warning during shutdown: {e}")
  
  def run(self):
    """Run the bot."""
    if not self.setup_application():
      sys.exit(1)
     
    if not self.register_handlers():
      sys.exit(1)
     
    print("\n" + "=" * 60)
    print("🚀 Starting bot...")
    print("=" * 60)
    
    try:
      self.app.run(self.start_bot())
    except KeyboardInterrupt:
      print("\n⚠️ Bot stopped by user (Ctrl+C)")
    except Exception as e:
      print(f"\n❌ Unexpected error: {e}")
      sys.exit(1)

def main():
  """Main entry point."""
  try:
    bot = HighTierBots()
    bot.run()
  except KeyboardInterrupt:
    print("\n👋 Goodbye!")
    sys.exit(0)
  except Exception as e:
    print(f"\n❌ Fatal error: {e}")
    sys.exit(1)
