from InflexMusic import app
import logging
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from youtube_search import YoutubeSearch


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)



@app.on_message(filters.command("search", ["/", ".", "!", "#"]))
async def search_handler(client, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("📚 `/search Ah Canım Sevgilim`")
            return

        query = message.text.split(None, 1)[1]
        status_msg = await message.reply_text("🔎 **Axtarılır...**")

        results = YoutubeSearch(query, max_results=5).to_dict()

        text = ""
        raw_buttons = []

        for i, result in enumerate(results):
            title = result["title"]
            duration = result["duration"]
            views = result["views"]
            channel = result["channel"]
            url_suffix = result["url_suffix"]
            url = f"https://www.youtube.com{url_suffix}"

            
            text += f"🎬 {i+1}  __{title}__\n"
            text += f"⏱ Müddət: `{duration}`\n"
            text += f"👁 Baxış: `{views}`\n"
            text += f"📺 Kanal: {channel}\n\n"

            raw_buttons.append(InlineKeyboardButton(f"🎬 Video {i+1}", url=url))

        buttons = []
        for i in range(0, len(raw_buttons) - 1, 2):
            buttons.append([raw_buttons[i], raw_buttons[i + 1]])
        if len(raw_buttons) % 2 != 0:
            buttons.append([raw_buttons[-1]])

        reply_markup = InlineKeyboardMarkup(buttons)

        await status_msg.edit_text(text, disable_web_page_preview=True, reply_markup=reply_markup)

    except Exception as e:
        logger.error(f"Xəta baş verdi: {e}")
        await message.reply(f"❌ Xəta:\n`{e}`")


