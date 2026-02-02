#(©)HighTierBots - Main Bot & Flask Server

import asyncio
from datetime import datetime
from flask import Flask
from pyrogram import Client
from pyrogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeChat
from config import API_ID, API_HASH, BOT_TOKEN, DB_URI, DB_NAME, OWNERS_ID, validate_config
from database.mongo import init_db
from logger import logger

app = Flask(__name__)

@app.route('/')
def check():
  """Health check endpoint"""
  return 'HighTierBots Join Bot is Running! ✅'


class HighTierBots(Client):
  """Custom Bot class extending Pyrogram Client"""
  
  def __init__(self):
    super().__init__(
      name="HighTierBots",
      api_id=API_ID,
      api_hash=API_HASH,
      bot_token=BOT_TOKEN,
      plugins=dict(root="handlers"),
      workers=50,
      sleep_threshold=10
    )
    self.uptime = None

  async def register_bot_commands(self):
    """Register bot commands for users and owner"""
    
    try:
      
      # Write Their Menu Commands for user
      user_commands = [
        BotCommand(command="start", description="Welcome message"),
        BotCommand(command="debug", description="Check That Bot is running or not"),
      ]
      
      # Write Their Menu Commands for owner
      owner_commands = [
        BotCommand(command="start", description="Welcome message"),
        BotCommand(command="stats", description="Show bot statistics"),
        BotCommand(command="addadmin", description="Add admin"),
        BotCommand(command="removeadmin", description="Remove admin"),
        BotCommand(command="setforce", description="ON/OFF set force"),
        BotCommand(command="addchannel", description="Add channel/group"),
        BotCommand(command="removechannel", description="Remove channel/group")
      ]
        
      await self.set_bot_commands(
        commands=user_commands,
        scope=BotCommandScopeAllPrivateChats()
      )
      logger.info("User commands registered successfully")
      
      for owners_id in OWNERS_ID:
        try:
          await self.set_bot_commands(
            commands=owner_commands,
            scope=BotCommandScopeChat(chat_id=owners_id)
          )
          logger.info(f"Oowner commands registered for user {owners_id}")
        except Exception as e:
          logger.error(f"Failed to register commands for owners {owners_id}: {e}")
      
      print("✅ Bot commands registered")
        
    except Exception as e:
      logger.error(f"Error registering bot commands: {e}")

  async def start(self):
    """Start bot - initialize database and handlers"""
    
    try:
      errors = validate_config()
      if errors:
        for error in errors:
          logger.error(f"Config Error: {error}")
        raise ValueError("Configuration validation failed")
      
      init_db(DB_URI, DB_NAME)
      logger.info("Database initialized")
      
      await super().start()
      
      self.uptime = datetime.now()
      
      me = await self.get_me()
      self.username = '@' + me.username
      
      # Register bot commands
      await self.register_bot_commands()
      
      logger.info(f"Bot started successfully: {self.username}")
      print(f"✅ Bot Started: {self.username}")
        
    except Exception as e:
      logger.error(f"Error starting bot: {e}")
      raise

  async def stop(self, *args):
    """Stop bot gracefully"""
    
    try:
      await super().stop()
      logger.info("Bot stopped successfully")
      print("👋 Bot Stopped")
    except Exception as e:
      logger.error(f"Error stopping bot: {e}")


async def run_flask_async():
  """Run Flask server in background"""
  
  try:
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
  except Exception as e:
    logger.error(f"Flask server error: {e}")


def run():
  """Run bot with Flask server"""
  
  try:
    bot = HighTierBots()
    loop = asyncio.get_event_loop()
    
    bot.run()

  except KeyboardInterrupt:
    logger.info("Bot interrupted by user")
  except Exception as e:
    logger.error(f"Fatal error: {e}")
    raise


if __name__ == "__main__":
  print("Starting Join Request Bot...")
  run()
  