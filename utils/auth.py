"""
#(©)HighTierBots
Authorization utilities for bot commands.
"""

from pyrogram import Client
from pyrogram.types import Message
from config.config import Config
from functools import wraps


def is_owner(user_id: int) -> bool:
    """
    Check if the user is the bot owner.
    
    Args:
        user_id: Telegram user ID
        
    Returns:
        True if user is owner, False otherwise
    """
    return user_id == Config.OWNER_ID


def owner_only(func):
    """
    Decorator to restrict command to owner only.
    
    Usage:
        @owner_only
        async def my_command(client, message):
            ...
    """
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        if not is_owner(message.from_user.id):
            await message.reply_text(
                "⛔ **Unauthorized Access**\n\n"
                "This command is restricted to the bot owner only.",
                quote=True
            )
            return
        return await func(client, message)
    return wrapper


def get_user_info(message: Message) -> dict:
    """
    Extract user information from message.
    
    Args:
        message: Pyrogram message object
        
    Returns:
        Dictionary with user information
    """
    user = message.from_user
    if not user:
        return {}
    
    return {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "language_code": user.language_code,
        "is_bot": user.is_bot
    }
