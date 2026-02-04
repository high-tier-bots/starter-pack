"""
#(©)HighTierBots /start command handler.
Bot command to handle /start bot.
"""

from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import os

from database.mongo import MongoOperations
from utils.auth import get_user_info
from utils.helpers import check_banner_exists


async def start_command(client: Client, message: Message):
    """
    Handle /start command.
    
    - Display banner image
    - Show services directory message
    - Add interactive buttons
    - Log new user to database and log group
    """
    user = message.from_user
    
    if not user:
        return
    
    user_info = get_user_info(message)
    
    is_new_user = MongoOperations.is_user_new(user_info['user_id'])
    
    MongoOperations.add_or_update_user(user_info)
    
    total_users = MongoOperations.get_total_users()
    
    if is_new_user and hasattr(client, '_logger'):
        try:
            await client._logger.log_new_user(user_info, total_users)
        except Exception as e:
            print(f"Error logging new user: {e}")
    
    text = (
        "🪧 **HighTierBots Starter Package**\n\n"
        "Click below button to get starter package details.\n"
    )
    
    keyboard = InlineKeyboardMarkup([
        [
          InlineKeyboardButton("Developer", url="https://t.me/sahilkumardev"),
          InlineKeyboardButton("Support", url="https://t.me/+t5OggMuHRJ5iODc1")  
        ],
        [InlineKeyboardButton("💼 Get Your Starter Package", url="https://github.com/HighTierBots/starter-package")],
    ])
    
    banner_exists, banner_path = check_banner_exists()
    
    try:
        if banner_exists and os.path.exists(banner_path):
            await message.reply_photo(
                photo=banner_path,
                caption=text,
                reply_markup=keyboard
            )
        else:
            await message.reply_text(
                text,
                reply_markup=keyboard
            )
            
            if is_new_user:
                print("⚠️ Warning: Banner image not found in assets/ folder")
                print("   Please add 'directory_banner.jpg' or 'directory_banner.png'")
    
    except Exception as e:
        print(f"Error sending start message: {e}")
        await message.reply_text(
            "🪧 HighTierBots Starter Package\n\n"
            "Contact @justjashon for Package."
        )
