#(©)HighTierBots - Stats Service

import os
from datetime import datetime

import psutil

from database.mongo import db
from utils.helpers import get_readable_time, format_stats


async def build_stats_text(bot) -> str:
  """Build formatted stats text for the bot."""

  now = datetime.now()
  delta = now - bot.uptime
  uptime_str = get_readable_time(delta.seconds)

  total_users = await db.total_users_count()
  total_groups = await db.total_groups_count()
  total_approved = await db.total_approved_count()
  total_pending = await db.total_pending_count()

  process = psutil.Process(os.getpid())
  memory_mb = round(process.memory_info().rss / 1024 / 1024, 2)
  cpu_percent = round(process.cpu_percent(interval=1), 2)

  start_time_str = bot.uptime.strftime("%Y-%m-%d %H:%M:%S")

  stats_dict = {
    'uptime': uptime_str,
    'total_users': total_users,
    'total_groups': total_groups,
    'total_approved': total_approved,
    'total_pending': total_pending,
    'start_time': start_time_str,
    'memory_mb': memory_mb,
    'cpu_percent': cpu_percent,
  }

  return format_stats(stats_dict)
