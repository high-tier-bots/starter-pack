#(©)HighTierBots - Utilities

def get_readable_time(seconds: int) -> str:
    """Convert seconds to readable time format (s, m, h, days)"""
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time

def format_stats(stats_dict: dict) -> str:
    """Format statistics dictionary to readable string"""
    uptime = stats_dict.get('uptime', 'N/A')
    users = stats_dict.get('total_users', 0)
    groups = stats_dict.get('total_groups', 0)
    approved = stats_dict.get('total_approved', 0)
    pending = stats_dict.get('total_pending', 0)
    start_time = stats_dict.get('start_time', 'N/A')
    memory = stats_dict.get('memory_mb', 'N/A')
    cpu = stats_dict.get('cpu_percent', 'N/A')
    
    stats_text = (
        f"<b>📊 Bot Statistics</b>\n\n"
        f"<b>⏱️ Uptime:</b> <code>{uptime}</code>\n"
        f"<b>👥 Users:</b> <code>{users}</code>\n"
        f"<b>👨‍👩‍👧 Groups:</b> <code>{groups}</code>\n"
        f"<b>✅ Approved Requests:</b> <code>{approved}</code>\n"
        f"<b>⏳ Pending Requests:</b> <code>{pending}</code>\n"
        f"<b>🚀 Started:</b> <code>{start_time}</code>\n"
    )
    
    if memory != 'N/A':
        stats_text += f"<b>💾 Memory:</b> <code>{memory} MB</code>\n"
    
    if cpu != 'N/A':
        stats_text += f"<b>🔧 CPU:</b> <code>{cpu}%</code>\n"
    
    return stats_text
  
# CREATE YOUR OWN UTILITIES HERE AS NEEDED