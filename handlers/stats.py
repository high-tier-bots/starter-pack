#(©)HighTierBots - Stats Handler

import os
import psutil
from pyrogram import Client, filters
from pyrogram.types import Message
from database.mongo import db
from utils.logger import logger
from config import OWNERS
from utils.helpers import get_readable_time, format_stats
from datetime import datetime

# Stats Command only for Owners
@Client.on_message(filters.command('ownerstats') & filters.user(OWNERS))
async def stats_command(bot: Client, message: Message):
  """Enhanced stats command showing bot metrics"""
  
  try:
    # Calculate uptime
    now = datetime.now()
    delta = now - bot.uptime
    uptime_str = get_readable_time(delta.seconds)
    
    total_users = await db.total_users_count()
    total_groups = await db.total_groups_count()
    total_approved = await db.total_approved_count()
    total_pending = await db.total_pending_count()
    
    process = psutil.Process(os.getpid())
    memory_mb = round(process.memory_info().rss / 1024 / 1024, 2)
    cpu_percent = round(process.cpu_percent(interval=1), 2)
    
    start_time_str = bot.uptime.strftime("%Y-%m-%d %H:%M:%S")
    
    stats_dict = {
      'uptime': uptime_str,
      'total_users': total_users,
      'total_groups': total_groups,
      'total_approved': total_approved,
      'total_pending': total_pending,
      'start_time': start_time_str,
      'memory_mb': memory_mb,
      'cpu_percent': cpu_percent,
    }
    
    stats_text = format_stats(stats_dict)
    await message.reply(stats_text)
    
    logger.info(f"Stats command executed for owner {message.from_user.id}")
    
  except Exception as e:
    logger.error(f"Error in stats command: {e}")
    try:
      await message.reply(f"❌ **Error retrieving stats:** `{str(e)}`")
    except:
      pass

# Stats Command only for Admins
