#(©)HighTierBots - Broadcast Handler

from pyrogram.errors import (
    InputUserDeactivated,
    FloodWait,
    UserIsBlocked,
    PeerIdInvalid
)
from pyrogram import Client, filters
from database.mongo import db
from config import OWNERS_ID
import asyncio
import datetime
import time
from utils.logger import logger


async def broadcast_message(user_id, message):
  """Send message to user with error handling"""
  
  try:
    await message.copy(chat_id=user_id)
    return True, "Success"
  
  except FloodWait as e:
    logger.warning(f"FloodWait {e.value}s, waiting...")
    await asyncio.sleep(e.value)
    return await broadcast_message(user_id, message)
  
  except InputUserDeactivated:
    await db.delete_user(int(user_id))
    logger.info(f"User {user_id} - Deleted account, removed from database")
    return False, "Deleted"

  except UserIsBlocked:
    await db.delete_user(int(user_id))
    logger.info(f"User {user_id} - Blocked bot, removed from database")
    return False, "Blocked"

  except PeerIdInvalid:
    await db.delete_user(int(user_id))
    logger.warning(f"User {user_id} - Invalid peer ID, removed from database")
    return False, "Error"
  
  except Exception as e:
    try:
      await message.forward(chat_id=user_id)
      return True, "Success"
    except Exception as e2:
      logger.error(f"Broadcast error for user {user_id}: {e} | Fallback failed: {e2}")
      return False, "Error"


# Broadcast Command only for Owners
@Client.on_message(filters.command("ownerbroadcast") & filters.user(OWNERS_ID) & filters.reply)
async def broadcast_command(bot: Client, message):
  """Broadcast message to all users"""
  
  users = await db.get_all_users()
  broadcast_msg = message.reply_to_message
  
  status_msg = await message.reply_text("📢 **Broadcast started...**")
  
  start_time = time.time()
  total_users = await db.total_users_count()
  
  stats = {
    'done': 0,
    'success': 0,
    'blocked': 0,
    'deleted': 0,
    'failed': 0,
  }
  
  logger.info(f"Broadcast started by owner {message.from_user.id} to {total_users} users")
  
  try:
    async for user in users:
      if 'id' not in user:
        stats['failed'] += 1
        stats['done'] += 1
        continue
    
      success, status = await broadcast_message(int(user['id']), broadcast_msg)
      
      if success:
        stats['success'] += 1
      else:
        if status == "Blocked":
          stats['blocked'] += 1
        elif status == "Deleted":
          stats['deleted'] += 1
        else:
          stats['failed'] += 1
      
      stats['done'] += 1
      
      if stats['done'] % 20 == 0:
        progress_text = (
          f"📢 **Broadcast in progress**\n\n"
          f"Total Users: {total_users}\n"
          f"Processed: {stats['done']} / {total_users}\n"
          f"✅ Success: {stats['success']}\n"
          f"❌ Blocked: {stats['blocked']}\n"
          f"🗑️ Deleted: {stats['deleted']}\n"
          f"⚠️ Failed: {stats['failed']}"
        )
        await status_msg.edit(progress_text)

  except Exception as e:
    logger.error(f"Error during broadcast: {e}")
    await status_msg.edit(f"❌ **Broadcast error:** `{str(e)}`")
    return
  
  # Final summary
  time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
  
  final_text = (
    f"✅ **Broadcast completed!**\n\n"
    f"⏱️ Time: {time_taken}\n"
    f"👥 Total Users: {total_users}\n"
    f"✅ Success: {stats['success']}\n"
    f"❌ Blocked: {stats['blocked']}\n"
    f"🗑️ Deleted: {stats['deleted']}\n"
    f"⚠️ Failed: {stats['failed']}"
  )
  
  await status_msg.edit(final_text)
  logger.info(f"Broadcast completed - Success: {stats['success']}, Blocked: {stats['blocked']}, Deleted: {stats['deleted']}")
