from time import sleep
from pyrogram import Client
import logging
from dotenv import load_dotenv, set_key, unset_key
from os import getenv
import config
from telethon import TelegramClient

load_dotenv('config.env')

# THE LOGGING

  
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)
 
 # AylinRobot 
ps = Client(
    'persional',
    bot_token = config.BOT_TOKEN,
    api_id = config.API_ID,
    api_hash = config.API_HASH
)

# Telethon
api_id = config.API_ID
api_hash = config.API_HASH
bot_token = config.BOT_TOKEN
 
xaos = TelegramClient('Xaos', api_id, api_hash).start(bot_token=bot_token)

