#(©)HighTierBots - Logging Configuration

import logging
import logging.handlers
import os
from datetime import datetime

def setup_logger():
  """Setup logging to file and console"""
  
  if not os.path.exists("logs"):
    os.makedirs("logs")
  
  logger = logging.getLogger("JoinRequestBot")
  logger.setLevel(logging.DEBUG)
  
  detailed_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
  )
  
  simple_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
  )
  
  file_handler = logging.handlers.RotatingFileHandler(
    'logs/bot.log',
    maxBytes=5*1024*1024,  # 5MB
    backupCount=5
  )
  file_handler.setLevel(logging.DEBUG)
  file_handler.setFormatter(detailed_formatter)
  
  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.INFO)
  console_handler.setFormatter(simple_formatter)
  
  logger.addHandler(file_handler)
  logger.addHandler(console_handler)
  
  return logger

logger = setup_logger()
