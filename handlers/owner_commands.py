#(©)HighTierBots - Owner Commands Handler

from pyrogram import Client, filters
from pyrogram.types import Message
from database.mongo import db
from services.broadcast import broadcast_to_all
from utils.logger import logger
from utils.config import OWNERS_ID 
from services.stats import build_stats_text


# Set_force Command only for Owners
@Client.on_message(filters.command('setforce') & filters.user(OWNERS_ID))
async def set_force(bot: Client, message: Message):
  """Set force mode ON or OFF - OWNER ONLY"""
  
  try:
    args = message.text.split()
    if len(args) != 2 or args[1].lower() not in ['on', 'off']:
      await message.reply("Usage: /setforce <on|off>")
      return
  
    force_value = args[1].lower() == 'on'
    result = await db.set_force_mode(force_value)
    
    if not result:
      await message.reply("❌ **Failed to set force mode. Check database connection.**")
      await db.log_error_to_debug_logs(
        command="/setforce",
        user_id=message.from_user.id,
        error="set_force_mode() returned False",
        suggested_fix="Check MongoDB settings collection accessibility"
      )
      return
    
    status = "enabled" if force_value else "disabled"
    await message.reply(f"✅ Force mode has been **{status}**.")
    
    logger.info(f"Force mode set to {status} by owner {message.from_user.id}")
      
  except Exception as e:
    logger.error(f"Error in setforce command: {e}")
    await db.log_error_to_debug_logs(
      command="/setforce",
      user_id=message.from_user.id,
      error=str(e),
      suggested_fix="Ensure set_force_mode() method exists and database is connected"
    )
    try:
      await message.reply(f"❌ **Error setting force mode:** `{str(e)}`")
    except:
      pass

    
# Addchannel Command only for Owners
@Client.on_message(filters.command('addchannel') & filters.user(OWNERS_ID))
async def add_channel(bot: Client, message: Message):
  """Add a channel or group to the database - OWNER ONLY"""
  
  try:
    args = message.text.split()
    if len(args) != 2:
      await message.reply("Usage: /addchannel <@channelname_or_id>")
      return
    
    channel_id = args[1]
    
    # Check for duplicates BEFORE adding
    existing = await db.get_channel(channel_id)
    if existing:
      await message.reply(f"⚠️ Channel/Group `{channel_id}` **already exists** in database.")
      logger.warning(f"Duplicate channel {channel_id} attempt by owner {message.from_user.id}")
      return
    
    result = await db.add_channel(channel_id)
    if not result:
      await message.reply(f"❌ **Failed to add channel {channel_id}. Check database.**")
      await db.log_error_to_debug_logs(
        command="/addchannel",
        user_id=message.from_user.id,
        error=f"add_channel() returned False for {channel_id}",
        suggested_fix="Check channels collection accessibility"
      )
      return
    
    await message.reply(f"✅ Channel/Group `{channel_id}` **added successfully**.")
    
    logger.info(f"Channel/Group {channel_id} added by owner {message.from_user.id}")
      
  except Exception as e:
    logger.error(f"Error in addchannel command: {e}")
    await db.log_error_to_debug_logs(
      command="/addchannel",
      user_id=message.from_user.id,
      error=str(e),
      suggested_fix="/addchannel @channelname or numeric_id"
    )
    try:
      await message.reply(f"❌ **Error adding channel/group:** `{str(e)}`")
    except:
      pass

# Removechannel Command only for Owners
@Client.on_message(filters.command('removechannel') & filters.user(OWNERS_ID))
async def remove_channel(bot: Client, message: Message):
  """Remove a channel or group from the database - OWNER ONLY"""
  
  try:
    args = message.text.split()
    if len(args) != 2:
      await message.reply("Usage: /removechannel <@channelname_or_id>")
      return
    
    channel_id = args[1]
    
    # Check if channel exists BEFORE deleting
    existing = await db.get_channel(channel_id)
    if not existing:
      await message.reply(f"❌ Channel/Group `{channel_id}` **does not exist** in database.")
      logger.warning(f"Channel {channel_id} not found for removal by owner {message.from_user.id}")
      return
    
    result = await db.remove_channel(channel_id)
    if not result:
      await message.reply(f"❌ **Failed to remove channel {channel_id}. Check database.**")
      await db.log_error_to_debug_logs(
        command="/removechannel",
        user_id=message.from_user.id,
        error=f"remove_channel() returned False for {channel_id}",
        suggested_fix="Check channels collection accessibility"
      )
      return
    
    await message.reply(f"✅ Channel/Group `{channel_id}` **removed successfully**.")
    
    logger.info(f"Channel/Group {channel_id} removed by owner {message.from_user.id}")
      
  except Exception as e:
    logger.error(f"Error in removechannel command: {e}")
    await db.log_error_to_debug_logs(
      command="/removechannel",
      user_id=message.from_user.id,
      error=str(e),
      suggested_fix="/removechannel @channelname or numeric_id"
    )
    try:
      await message.reply(f"❌ **Error removing channel/group:** `{str(e)}`")
    except:
      pass
    
# Addadmin Command only for Owners
@Client.on_message(filters.command('addadmin') & filters.user(OWNERS_ID))
async def add_admin(bot: Client, message: Message):
  """Add a new admin user - OWNER ONLY"""
  
  try:
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
      await message.reply("Usage: /addadmin <user_id>")
      return
    
    user_id = int(args[1])
    
    # Check if user exists
    if not await db.is_user_exist(user_id):
      await message.reply(f"❌ User `{user_id}` **does not exist** in database. Add /start first.")
      logger.warning(f"Non-existent user {user_id} admin attempt by owner {message.from_user.id}")
      return
    
    # Check for duplicate admin
    if await db.is_admin(user_id):
      await message.reply(f"⚠️ User `{user_id}` **is already an admin**.")
      logger.warning(f"Duplicate admin {user_id} attempt by owner {message.from_user.id}")
      return
    
    result = await db.add_admin(user_id)
    if not result:
      await message.reply(f"❌ **Failed to add admin {user_id}. Check database.**")
      await db.log_error_to_debug_logs(
        command="/addadmin",
        user_id=message.from_user.id,
        error=f"add_admin() returned False for {user_id}",
        suggested_fix="Check admins collection accessibility"
      )
      return
    
    await message.reply(f"✅ User `{user_id}` **added as admin successfully**.")
    
    logger.info(f"User {user_id} added as admin by owner {message.from_user.id}")
      
  except Exception as e:
    logger.error(f"Error in addadmin command: {e}")
    await db.log_error_to_debug_logs(
      command="/addadmin",
      user_id=message.from_user.id,
      error=str(e),
      suggested_fix="/addadmin <numeric_user_id>"
    )
    try:
      await message.reply(f"❌ **Error adding admin:** `{str(e)}`")
    except:
      pass
    
# Removeadmin Command only for Owners
@Client.on_message(filters.command('removeadmin') & filters.user(OWNERS_ID))
async def remove_admin(bot: Client, message: Message):
  """Remove an admin user - OWNER ONLY"""
  
  try:
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
      await message.reply("Usage: /removeadmin <user_id>")
      return
    
    user_id = int(args[1])
    
    # Check if admin exists BEFORE deleting
    if not await db.is_admin(user_id):
      await message.reply(f"❌ User `{user_id}` **is not an admin**.")
      logger.warning(f"Non-admin {user_id} removal attempt by owner {message.from_user.id}")
      return
    
    # Check total admins (prevent removing last admin)
    total_admins = await db.total_admins_count()
    if total_admins <= 1:
      await message.reply("❌ **Cannot remove the last admin!**")
      logger.warning(f"Last admin removal attempt by owner {message.from_user.id}")
      return
    
    result = await db.remove_admin(user_id)
    if not result:
      await message.reply(f"❌ **Failed to remove admin {user_id}. Check database.**")
      await db.log_error_to_debug_logs(
        command="/removeadmin",
        user_id=message.from_user.id,
        error=f"remove_admin() returned False for {user_id}",
        suggested_fix="Check admins collection accessibility"
      )
      return
    
    await message.reply(f"✅ User `{user_id}` **removed from admins successfully**.")
    
    logger.info(f"User {user_id} removed from admins by owner {message.from_user.id}")
      
  except Exception as e:
    logger.error(f"Error in removeadmin command: {e}")
    await db.log_error_to_debug_logs(
      command="/removeadmin",
      user_id=message.from_user.id,
      error=str(e),
      suggested_fix="/removeadmin <numeric_user_id>"
    )
    try:
      await message.reply(f"❌ **Error removing admin:** `{str(e)}`")
    except:
      pass
    
# Broadcast Command only for Owners
@Client.on_message(filters.command("ownerbroadcast") & filters.user(OWNERS_ID) & filters.reply)
async def broadcast_command(bot: Client, message):
  """Broadcast message to all users - OWNER ONLY"""
  
  try:
    await broadcast_to_all(message)
    logger.info(f"Broadcast completed by owner {message.from_user.id}")
  except Exception as e:
    logger.error(f"Broadcast error: {e}")
    await db.log_error_to_debug_logs(
      command="/ownerbroadcast",
      user_id=message.from_user.id,
      error=str(e),
      suggested_fix="Check if users collection is accessible and reply message exists"
    )
    try:
      await message.reply(f"❌ **Broadcast error:** `{str(e)}`")
    except:
      pass


# Stats Command only for Owners
@Client.on_message(filters.command('ownerstats') & filters.user(OWNERS_ID))
async def stats_command(bot: Client, message: Message):
  """Enhanced stats command showing bot metrics - OWNER ONLY"""
  
  try:
    stats_text = await build_stats_text(bot)
    await message.reply(stats_text)
    
    logger.info(f"Stats command executed for owner {message.from_user.id}")
    
  except Exception as e:
    logger.error(f"Error in stats command: {e}")
    await db.log_error_to_debug_logs(
      command="/ownerstats",
      user_id=message.from_user.id,
      error=str(e),
      suggested_fix="Verify all database count methods exist: total_users_count(), total_groups_count(), etc."
    )
    try:
      await message.reply(f"❌ **Error retrieving stats:** `{str(e)}`")
    except:
      pass
