#(©)HighTierBots - Commands Handler

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from database.mongo import db
from utils.logger import logger
from utils.config import USER_REPLY_TEXT, OWNERS_ID
from services.bot_log import send_bot_start_log

@Client.on_message(filters.command('start'))
async def start_command(client: Client, message: Message):
  """Handle /start command"""

  try:
    user_id = message.from_user.id
    
    if not await db.is_user_exist(user_id):
      await db.add_user(user_id, message.from_user.first_name)
      await send_bot_start_log(client, message.from_user)
      logger.info(f"New user started bot: {user_id}")

    await message.reply_photo(
      "https://te.legra.ph/file/119729ea3cdce4fefb6a1.jpg",
      caption=(
        f"<b>Hello {message.from_user.mention} 👋\n\n"
        "I am a starter repo for create a new bot.\n\n"
        "Click below to contact 👇</b>"
      ),
      reply_markup=InlineKeyboardMarkup([
        [
          InlineKeyboardButton("Create Your Own Bot", url='https://github.com/hightierbots/bot-starter-repo'),
        ],
        [
          InlineKeyboardButton("❣️ Developer", url='https://t.me/justjashon'),
          InlineKeyboardButton("🤖 Updates", url='https://t.me/HighTierBots')
        ]
      ])
    )
    logger.info(f"Start command handled for user {user_id}")

  except Exception as e:
    logger.error(f"Error in start command for user {message.from_user.id}: {e}")
    await db.log_error_to_debug_logs(
      command="/start",
      user_id=message.from_user.id,
      error=str(e),
      suggested_fix="Check MongoDB connection or verify is_user_exist() method exists"
    )
    try:
      await message.reply("❌ **An error occurred. Please try again.**")
    except:
      pass


@Client.on_message(filters.command('debug') & filters.user(OWNERS_ID))
async def debug_command(client, message: Message):
    """Debug command to fetch last error from debug_logs - OWNER ONLY"""
    
    try:
        user_id = message.from_user.id
        
        # Fetch last error from debug_logs
        last_error = await db.get_last_debug_log()
        
        if not last_error:
            await message.reply("✅ **No errors logged yet. Bot is running smoothly!**")
            logger.info(f"Debug command accessed by owner {user_id} - no errors found")
            return
        
        debug_info = f"""<b>🐛 LATEST DEBUG LOG</b>

<b>Command:</b> <code>{last_error.get('command', 'N/A')}</code>
<b>User ID:</b> <code>{last_error.get('user_id', 'N/A')}</code>
<b>Error:</b> <code>{last_error.get('error', 'N/A')}</code>
<b>Suggested Fix:</b> <code>{last_error.get('suggested_fix', 'N/A')}</code>
<b>Timestamp:</b> <code>{last_error.get('timestamp', 'N/A')}</code>"""
        
        await message.reply(debug_info)
        logger.info(f"Debug command accessed by owner {user_id}")
        
    except Exception as e:
        logger.error(f"Error in debug command: {e}")
        await db.log_error_to_debug_logs(
            command="/debug",
            user_id=message.from_user.id,
            error=str(e),
            suggested_fix="Check if debug_logs collection exists and is accessible"
        )
        try:
            await message.reply("❌ **Error retrieving debug logs.**")
        except:
            pass


@Client.on_message(filters.private & filters.incoming & ~filters.command(['start', 'check' ,'broadcast', 'debug', 'stats', 'addadmin', 'removeadmin', 'setforce', 'addchannel', 'removechannel', 'ownerbroadcast', 'ownerstats']))
async def handle_private_messages(_, message: Message):
  """Handle private messages that don't match any handler"""

  try:
    if USER_REPLY_TEXT:
      await message.reply(USER_REPLY_TEXT)
      logger.debug(f"Auto-reply sent to user {message.from_user.id}")
  except Exception as e:
    logger.error(f"Error sending auto-reply to {message.from_user.id}: {e}")

