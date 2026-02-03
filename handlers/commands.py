#(©)HighTierBots - Commands Handler

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from database.mongo import db
from utils.logger import logger
from utils.config import USER_REPLY_TEXT
from services.bot_log import send_bot_start_log

@Client.on_message(filters.command('start'))
async def start_command(client: Client, message: Message):
  """Handle /start command"""

  try:
    if not await db.is_user_exist(message.from_user.id):
      await db.add_user(message.from_user.id, message.from_user.first_name)
      await send_bot_start_log(client, message.from_user)
      logger.info(f"New user started bot: {message.from_user.id}")

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
    logger.info(f"Start command handled for user {message.from_user.id}")

  except Exception as e:
    logger.error(f"Error in start command for user {message.from_user.id}: {e}")
    try:
      await message.reply("❌ **An error occurred. Please try again.**")
    except:
      pass


@Client.on_message(filters.command('debug'))
async def debug_command(client, message: Message):
    """Debug command to check bot status"""

    user_id = message.from_user.id
    session = await db.get_session(user_id)

    debug_info = f"""
    **=== BOT DEBUG INFO ===**

    👤 User ID: `{user_id}`
    📝 Has Session: {'Yes' if session else 'No'}
    {"🔐 Session Length: " + str(len(session)) if session else ""}

    **Status:** ✅ Bot Running
    """

    await message.reply(debug_info)
    logger.info(f"Debug command accessed by user {user_id}")


@Client.on_message(filters.private & filters.incoming & ~filters.command(['start', 'broadcast', 'debug', 'stats', 'addadmin', 'removeadmin', 'setforce', 'addchannel', 'removechannel']))
async def handle_private_messages(_, message: Message):
  """Handle private messages that don't match any handler"""

  try:
    if USER_REPLY_TEXT:
      await message.reply(USER_REPLY_TEXT)
      logger.debug(f"Auto-reply sent to user {message.from_user.id}")
  except Exception as e:
    logger.error(f"Error sending auto-reply to {message.from_user.id}: {e}")
