#(©)HighTierBots - Broadcast Handler

from pyrogram import Client, filters

from utils.config import OWNERS_ID
from services.broadcast import broadcast_to_all


# Broadcast Command only for Owners
@Client.on_message(filters.command("ownerbroadcast") & filters.user(OWNERS_ID) & filters.reply)
async def broadcast_command(bot: Client, message):
  """Broadcast message to all users"""
  await broadcast_to_all(message)
