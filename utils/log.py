"""
#(©)HighTierBots - Bot Log Service
Send message in log group, add more as needed.
"""

from datetime import datetime

from pyrogram import Client
from pyrogram.errors import FloodWait

from utils.config import LOG_GROUP_ID
from utils.logger import logger


async def send_bot_start_log(client: Client, user) -> bool:
  """
  Send bot start notification to LOG_GROUP_ID

  Args:
    client: Pyrogram Client instance
    user: User object from message

  Returns:
    bool: True if successful, False otherwise
  """
  try:
    if not LOG_GROUP_ID or LOG_GROUP_ID == 0:
      logger.warning("LOG_GROUP_ID not configured")
      return False

    username = user.username if user.username else "Not Available"
    user_id = user.id if user.id else "Unknown"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    notification_text = (
      f"🚀 <b>New User Start Bot</b>\n\n"
      f"👤 User ID: <code>{user_id}</code>\n"
      f"👤 Username: @{username}\n"
      f"🕒 Time: <code>{timestamp}</code>"
    )

    await client.send_message(LOG_GROUP_ID, notification_text)
    logger.info(f"Bot start notification sent for user {user_id}")
    return True

  except FloodWait as e:
    logger.warning(f"FloodWait error while sending start log: {e.value}s")
    return False
  except Exception as e:
    logger.error(f"Error sending bot start notification: {e}")
    return False


async def send_bot_added_log(client: Client, chat, added_by_user) -> bool:
  """
  Send bot added to group/channel notification to LOG_GROUP_ID

  Args:
    client: Pyrogram Client instance
    chat: Chat object
    added_by_user: User object who added the bot

  Returns:
    bool: True if successful, False otherwise
  """
  try:
    if not LOG_GROUP_ID or LOG_GROUP_ID == 0:
      logger.warning("LOG_GROUP_ID not configured")
      return False

    chat_id = chat.id if chat.id else "Unknown"
    chat_name = chat.title if chat.title else "Unknown"
    chat_username = chat.username if chat.username else "Not Available"

    chat_type = "Group"
    if hasattr(chat, 'type'):
      if chat.type == "channel":
        chat_type = "Channel"
      elif chat.type in ["group", "supergroup"]:
        chat_type = "Group"

    added_by_id = added_by_user.id if added_by_user.id else "Unknown"
    added_by_username = added_by_user.username if added_by_user.username else "Not Available"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    notification_text = (
      f"🤖 <b>Bot Added Notification</b>\n\n"
      f"📌 Chat Type: <code>{chat_type}</code>\n"
      f"📌 Chat ID: <code>{chat_id}</code>\n"
      f"📌 Chat Name: <code>{chat_name}</code>\n"
      f"📌 Chat Username: @{chat_username}\n\n"
      f"👤 Added By User ID: <code>{added_by_id}</code>\n"
      f"👤 Added By Username: @{added_by_username}\n\n"
      f"🕒 Time: <code>{timestamp}</code>"
    )

    await client.send_message(LOG_GROUP_ID, notification_text)
    logger.info(f"Bot added notification sent for chat {chat_id}")

    return True

  except FloodWait as e:
    logger.warning(f"FloodWait error while sending bot added log: {e.value}s")
    return False
  except Exception as e:
    logger.error(f"Error sending bot added notification: {e}")
    return False
