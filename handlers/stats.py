"""
#(©)HighTierBots /stats command handler (Owner only).
Display bot statistics and analytics.
"""

from pyrogram import Client
from pyrogram.types import Message
from datetime import datetime, timezone

from database.mongo import MongoOperations
from utils.auth import owner_only
from utils.helpers import format_uptime, format_number


@owner_only
async def stats_command(client: Client, message: Message):
    """
    Handle /stats command.
    
    Display:
    - Total users
    - Active users (24h)
    - New users (today, this week, this month)
    - Bot uptime
    - Bot start time
    """
    # Send "calculating" message
    calculating_msg = await message.reply_text("📊 Calculating statistics... ⏳", quote=True)
    
    try:
        # Get statistics from database
        total_users = MongoOperations.get_total_users()
        active_users_24h = MongoOperations.get_active_users(hours=24)
        new_users_today = MongoOperations.get_new_users_since(days=0)
        new_users_week = MongoOperations.get_new_users_since(days=7)
        new_users_month = MongoOperations.get_new_users_since(days=30)
        
        # Get bot start time
        bot_start_time = MongoOperations.get_bot_start_time()
        
        if bot_start_time:
            uptime = format_uptime(bot_start_time)
            start_time_str = bot_start_time.strftime('%Y-%m-%d %H:%M UTC')
        else:
            uptime = "Unknown"
            start_time_str = "Unknown"
        
        # Format statistics message
        stats_message = (
            "📊 **Bot Statistics**\n\n"
            
            f"👥 Total Users: **{format_number(total_users)}**\n"
            f"✅ Active Users (24h): **{format_number(active_users_24h)}**\n"
            f"📅 New Users Today: **{format_number(new_users_today)}**\n"
            f"📈 New Users This Week: **{format_number(new_users_week)}**\n"
            f"📆 New Users This Month: **{format_number(new_users_month)}**\n\n"
            
            f"⏰ Bot Uptime: **{uptime}**\n"
            f"🚀 Bot Started: **{start_time_str}**\n\n"
            
            f"Last Updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC"
        )
        
        # Update message with statistics
        await calculating_msg.edit_text(stats_message)
        
    except Exception as e:
        await calculating_msg.edit_text(
            f"❌ Error calculating statistics: {str(e)}\n\n"
            "Please try again later."
        )
        print(f"Error in stats command: {e}")
