"""
Log group notification utilities.
"""

from datetime import datetime, timezone
from pyrogram import Client
from pyrogram.errors import FloodWait, PeerIdInvalid
import asyncio
from config.config import Config


class Logger:
    """Log group notification handler."""
    
    def __init__(self, client: Client):
        self.client = client
        self.log_group_id = Config.LOG_GROUP_ID
        self._disabled = False
    
    async def log_new_user(self, user_info: dict, total_users: int):
        """
        Log new user to the log group.
        
        Args:
            user_info: Dictionary containing user information
            total_users: Total number of users in the database
        """
        if self._disabled:
            return
        try:
            username = f"@{user_info['username']}" if user_info.get('username') else "N/A"
            full_name = user_info.get('first_name', 'Unknown')
            if user_info.get('last_name'):
                full_name += f" {user_info['last_name']}"
            
            message = (
                "🆕 **New User Started Bot**\n\n"
                "👤 **User Info:**\n"
                f"• Name: {full_name}\n"
                f"• Username: {username}\n"
                f"• User ID: `{user_info['user_id']}`\n"
                f"• Language: {user_info.get('language_code', 'N/A')}\n\n"
                f"📅 Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n"
                f"📊 Total Users: **{total_users:,}**"
            )
            
            await self.client.send_message(
                chat_id=self.log_group_id,
                text=message
            )
        except PeerIdInvalid:
            self._disabled = True
            print("Log group disabled: invalid LOG_GROUP_ID or bot not in group.")
        except FloodWait as e:
            print(f"FloodWait: Sleeping for {e.value} seconds")
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"Error logging new user to group: {e}")
    
    async def log_broadcast(self, sent_by: str, message: str, successful: int, failed: int, total: int, stats: str = ""):
        """
        Log broadcast activity to the log group.
        
        Args:
            sent_by: Username of the sender
            message: Broadcast message content
            successful: Number of successful sends
            failed: Number of failed sends
            total: Total recipients
            stats: Additional statistics string (optional)
        """
        if self._disabled:
            return
        try:
            # Truncate message if too long
            display_message = message[:100] + "..." if len(message) > 100 else message
            
            log_message = (
                "📢 **Broadcast Message Sent**\n\n"
                f"👨‍💻 Sent by: @{sent_by}\n"
                f"📝 Message: \"{display_message}\"\n\n"
                "📊 **Results:**\n"
                f"✅ Successful: {successful}\n"
                f"❌ Failed: {failed}\n"
                f"📈 Total Recipients: {total}\n"
            )
            
            if stats:
                log_message += f"\n{stats}\n"
            
            log_message += f"\n⏰ Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC"
            
            await self.client.send_message(
                chat_id=self.log_group_id,
                text=log_message
            )
        except PeerIdInvalid:
            self._disabled = True
            print("Log group disabled: invalid LOG_GROUP_ID or bot not in group.")
        except Exception as e:
            print(f"Error logging broadcast to group: {e}")
    
    async def log_bot_started(self, total_users: int):
        """
        Log bot start/restart to the log group.
        
        Args:
            total_users: Total number of users in database
        """
        if self._disabled:
            return
        try:
            message = (
                "🚀 **Bot Started Successfully**\n\n"
                f"⏰ Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
                f"📊 Total Users in DB: **{total_users:,}**\n"
                "✅ Status: **Online**"
            )
            
            await self.client.send_message(
                chat_id=self.log_group_id,
                text=message
            )
        except PeerIdInvalid:
            self._disabled = True
            print("Log group disabled: invalid LOG_GROUP_ID or bot not in group.")
        except Exception as e:
            print(f"Error logging bot start to group: {e}")
    
    async def log_error(self, error: str, module: str):
        """
        Log error to the log group.
        
        Args:
            error: Error message
            module: Module where error occurred
        """
        if self._disabled:
            return
        try:
            message = (
                "⚠️ **Error Occurred**\n\n"
                f"📝 Error: {error}\n"
                f"📂 Module: {module}\n"
                f"⏰ Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC"
            )
            
            await self.client.send_message(
                chat_id=self.log_group_id,
                text=message
            )
        except PeerIdInvalid:
            self._disabled = True
            print("Log group disabled: invalid LOG_GROUP_ID or bot not in group.")
        except Exception as e:
            print(f"Error logging error to group: {e}")
