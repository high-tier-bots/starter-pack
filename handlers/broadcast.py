"""
#(©)HighTierBots /broadcast command handler (Owner only).
Send messages to all bot users.
"""

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
import asyncio
import time

from database.mongo import MongoOperations
from database.models import Broadcast
from utils.auth import owner_only
from config.config import Config


@owner_only
async def broadcast_command(client: Client, message: Message):
    """
    Handle /broadcast command.
    
    Usage: /broadcast Your message here
    
    - Only accessible by bot owner
    - Sends message to all users
    - Tracks success/failure
    - Logs to database and log group
    """
    # Get broadcast message and check for reply
    broadcast_message = None
    is_reply_broadcast = False
    
    # Check if replying to a message
    if message.reply_to_message:
        is_reply_broadcast = True
        replied_msg = message.reply_to_message
        
        # Try to get text from replied message
        if replied_msg.text:
            broadcast_message = replied_msg.text
        elif replied_msg.caption:
            broadcast_message = replied_msg.caption
        else:
            broadcast_message = "[Media broadcast]"
    
    # Check if there's text after /broadcast command
    if len(message.command) >= 2:
        # Override with explicit command text if provided
        broadcast_message = message.text.split(None, 1)[1]
        is_reply_broadcast = False
    
    # If still no message, show usage
    if not broadcast_message:
        await message.reply_text(
            "📢 **Broadcast Command**\n\n"
            "**Usage Options:**\n"
            "1. `/broadcast Your message here` - Send direct message\n"
            "2. Reply to a message and send `/broadcast` - Broadcast the replied message\n\n"
            "**Supported media:** Photos, videos, documents with captions",
            quote=True
        )
        return
    
    # Get all user IDs (excluding blocked users)
    user_ids = MongoOperations.get_all_user_ids(exclude_blocked=True)
    total_users = len(user_ids)
    
    if total_users == 0:
        await message.reply_text("❌ No users to broadcast to.", quote=True)
        return
    
    # Send progress message
    progress_msg = await message.reply_text(
        f"📢 Broadcasting to {total_users} users... ⏳\n\n"
        "This may take a few moments.",
        quote=True
    )
    
    # Broadcast counters
    successful = 0
    failed = 0
    blocked = 0
    start_time = time.time()
    
    # Check if replying to media
    is_media = False
    media = None
    media_type = None
    
    if message.reply_to_message:
        replied_msg = message.reply_to_message
        if replied_msg.photo:
            is_media = True
            media_type = "photo"
            media = replied_msg.photo.file_id
        elif replied_msg.video:
            is_media = True
            media_type = "video"
            media = replied_msg.video.file_id
        elif replied_msg.document:
            is_media = True
            media_type = "document"
            media = replied_msg.document.file_id
    
    # Broadcast to all users
    for user_id in user_ids:
        try:
            if is_media:
                # Send media with caption
                if media_type == "photo":
                    await client.send_photo(
                        chat_id=user_id,
                        photo=media,
                        caption=broadcast_message
                    )
                elif media_type == "video":
                    await client.send_video(
                        chat_id=user_id,
                        video=media,
                        caption=broadcast_message
                    )
                elif media_type == "document":
                    await client.send_document(
                        chat_id=user_id,
                        document=media,
                        caption=broadcast_message
                    )
            else:
                # Send text message
                await client.send_message(
                    chat_id=user_id,
                    text=broadcast_message
                )
            
            successful += 1
            
            # Small delay to avoid rate limiting
            await asyncio.sleep(0.05)
            
        except FloodWait as e:
            print(f"FloodWait: Sleeping for {e.value} seconds")
            await asyncio.sleep(e.value)
            # Retry
            try:
                if is_media:
                    if media_type == "photo":
                        await client.send_photo(user_id, media, caption=broadcast_message)
                    elif media_type == "video":
                        await client.send_video(user_id, media, caption=broadcast_message)
                    elif media_type == "document":
                        await client.send_document(user_id, media, caption=broadcast_message)
                else:
                    await client.send_message(user_id, broadcast_message)
                successful += 1
            except:
                failed += 1
                
        except (UserIsBlocked, InputUserDeactivated):
            failed += 1
            blocked += 1
            # Mark user as blocked
            MongoOperations.mark_user_blocked(user_id)
            
        except Exception as e:
            failed += 1
            print(f"Error broadcasting to {user_id}: {e}")
    
    # Update progress message with results
    end_time = time.time()
    duration = end_time - start_time
    
    success_rate = (successful/total_users*100) if total_users > 0 else 0
    avg_time_per_user = (duration / total_users) if total_users > 0 else 0
    
    results_message = (
        "📢 **Broadcast Complete!**\n\n"
        "📊 **Results:**\n"
        f"✅ Successful: **{successful}**\n"
        f"❌ Failed: **{failed}** (🚫 Blocked: {blocked})\n"
        f"📈 Total Recipients: **{total_users}**\n"
        f"📊 Success Rate: **{success_rate:.1f}%**\n\n"
        "⏱️ **Timing:**\n"
        f"⏳ Total Duration: **{duration:.2f}s**\n"
        f"⚡ Avg per User: **{avg_time_per_user*1000:.1f}ms**"
    )
    
    await progress_msg.edit_text(results_message)
    
    # Save broadcast to database
    broadcast_data = Broadcast(
        message=broadcast_message,
        sent_by=message.from_user.id,
        total_recipients=total_users,
        successful=successful,
        failed=failed
    ).to_dict()
    
    MongoOperations.save_broadcast(broadcast_data)
    
    # Log to log group
    if hasattr(client, '_logger'):
        try:
            # Create detailed log message with stats
            log_stats = (
                f"📊 **Broadcast Statistics:**\n"
                f"✅ Sent: {successful}\n"
                f"❌ Failed: {failed}\n"
                f"🚫 Blocked: {blocked}\n"
                f"📈 Total: {total_users}\n"
                f"📊 Rate: {success_rate:.1f}%\n\n"
                f"⏱️ **Performance:**\n"
                f"⏳ Duration: {duration:.2f}s\n"
                f"⚡ Speed: {avg_time_per_user*1000:.1f}ms/user"
            )
            
            await client._logger.log_broadcast(
                sent_by=Config.OWNER_USERNAME,
                message=broadcast_message,
                successful=successful,
                failed=failed,
                total=total_users,
                stats=log_stats
            )
        except Exception as e:
            print(f"Error logging broadcast: {e}")
