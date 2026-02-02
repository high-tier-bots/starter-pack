#(©)HighTierBots - Owner Commands Handler

from pyrogram import Client, filters
from pyrogram.types import Message
from database.mongo import db
from logger import logger
from config import OWNERS_ID 

# Set_force Command only for Owners
@Client.on_message(filters.command('setforce') & filters.user(OWNERS_ID))
async def set_force(bot: Client, message: Message):
  """Set force mode ON or OFF"""
  
  try:
    args = message.text.split()
    if len(args) != 2 or args[1].lower() not in ['on', 'off']:
      await message.reply("Usage: /setforce <on|off>")
      return
  
    force_value = args[1].lower() == 'on'
    await db.set_force_mode(force_value)
    
    status = "enabled" if force_value else "disabled"
    await message.reply(f"✅ Force mode has been {status}.")
    
    logger.info(f"Force mode set to {status} by owner {message.from_user.id}")
      
  except Exception as e:
    logger.error(f"Error in setforce command: {e}")
    try:
      await message.reply(f"❌ **Error setting force mode:** `{str(e)}`")
    except:
      pass
    
# Addchannel Command only for Owners
@Client.on_message(filters.command('addchannel') & filters.user(OWNERS_ID))
async def add_channel(bot: Client, message: Message):
  """Add a channel or group to the database"""
  
  try:
    args = message.text.split()
    if len(args) != 2:
      await message.reply("Usage: /addchannel <channel_or_group_id>")
      return
    
    channel_id = args[1]
    await db.add_channel(channel_id)
    
    await message.reply(f"✅ Channel/Group `{channel_id}` added successfully.")
    
    logger.info(f"Channel/Group {channel_id} added by owner {message.from_user.id}")
      
  except Exception as e:
    logger.error(f"Error in addchannel command: {e}")
    try:
      await message.reply(f"❌ **Error adding channel/group:** `{str(e)}`")
    except:
      pass  

# Removechannel Command only for Owners
@Client.on_message(filters.command('removechannel') & filters.user(OWNERS))
async def remove_channel(bot: Client, message: Message):
  """Remove a channel or group from the database"""
  
  try:
    args = message.text.split()
    if len(args) != 2:
      await message.reply("Usage: /removechannel <channel_or_group_id>")
      return
    
    channel_id = args[1]
    await db.remove_channel(channel_id)
    
    await message.reply(f"✅ Channel/Group `{channel_id}` removed successfully.")
    
    logger.info(f"Channel/Group {channel_id} removed by owner {message.from_user.id}")
      
  except Exception as e:
    logger.error(f"Error in removechannel command: {e}")
    try:
      await message.reply(f"❌ **Error removing channel/group:** `{str(e)}`")
    except:
      pass
    
# Admin Command only for Owners
@Client.on_message(filters.command('addadmin') & filters.user(OWNERS))
async def add_admin(bot: Client, message: Message):
  """Add a new admin user"""
  
  try:
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
      await message.reply("Usage: /addadmin <user_id>")
      return
    
    user_id = int(args[1])
    await db.add_admin(user_id)
    
    await message.reply(f"✅ User `{user_id}` added as admin successfully.")
    
    logger.info(f"User {user_id} added as admin by owner {message.from_user.id}")
      
  except Exception as e:
    logger.error(f"Error in addadmin command: {e}")
    try:
      await message.reply(f"❌ **Error adding admin:** `{str(e)}`")
    except:
      pass
    
# Removeadmin Command only for Owners
@Client.on_message(filters.command('removeadmin') & filters.user(OWNERS))
async def remove_admin(bot: Client, message: Message):
  """Remove an admin user"""
  
  try:
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
      await message.reply("Usage: /removeadmin <user_id>")
      return
    
    user_id = int(args[1])
    await db.remove_admin(user_id)
    
    await message.reply(f"✅ User `{user_id}` removed from admins successfully.")
    
    logger.info(f"User {user_id} removed from admins by owner {message.from_user.id}")
      
  except Exception as e:
    logger.error(f"Error in removeadmin command: {e}")
    try:
      await message.reply(f"❌ **Error removing admin:** `{str(e)}`")
    except:
      pass
    
