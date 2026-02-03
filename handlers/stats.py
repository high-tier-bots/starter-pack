#(©)HighTierBots - Stats Handler

from pyrogram import Client, filters
from pyrogram.types import Message
from utils.logger import logger
from utils.config import OWNERS
from services.stats import build_stats_text

# Stats Command only for Owners
@Client.on_message(filters.command('ownerstats') & filters.user(OWNERS))
async def stats_command(bot: Client, message: Message):
  """Enhanced stats command showing bot metrics"""
  
  try:
    stats_text = await build_stats_text(bot)
    await message.reply(stats_text)
    
    logger.info(f"Stats command executed for owner {message.from_user.id}")
    
  except Exception as e:
    logger.error(f"Error in stats command: {e}")
    try:
      await message.reply(f"❌ **Error retrieving stats:** `{str(e)}`")
    except:
      pass

# Stats Command only for Admins
