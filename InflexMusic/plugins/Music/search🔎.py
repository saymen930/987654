from InflexMusic import app
#from InflexMusic.core.bot import pls as app
from pyrogram.errors import FloodWait
from pyrogram import Client, filters
import os, youtube_dl, requests, aiohttp, wget, time, yt_dlp, logging, json
from youtube_search import YoutubeSearch
from pyrogram import Client
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@app.on_message(filters.command("search", ["/", "!", "@", "."]))
async def search(_, message: Message):
    m = await message.delete()  
    try:
        if len(message.command) < 2:
            await message.reply_text("/search **Ah Canım Sevgilim!**")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("🔎 **Axtarılır...**")
        results = YoutubeSearch(query, max_results=5).to_dict()
        i = 0
        text = ""
        while i < 5:
            text += f"🏷 **Ad:** __{results[i]['title']}__\n"
            text += f"⏱ **Müddət:** `{results[i]['duration']}`\n"
            text += f"👀 **Baxış:** `{results[i]['views']}`\n"
            text += f"📣 **Youtube Kanalı:** {results[i]['channel']}\n"
            text += f"🔗: [Görmək Üçün Toxun](https://www.youtube.com{results[i]['url_suffix']})\n\n"
            i += 1
        await m.edit(text, disable_web_page_preview=True)
    except Exception as e:
        await m.edit(str(e))
