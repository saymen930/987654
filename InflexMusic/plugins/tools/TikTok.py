from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import re
from InflexMusic import app


def is_tiktok_link(text):
    return re.search(r"(https?://)?(www\.)?(vm\.tiktok\.com|tiktok\.com)", text)

def get_tiktok_video(url):
    try:
        api = "https://tikwm.com/api/"
        params = {"url": url}
        r = requests.get(api, params=params).json()
        if r.get("data") and r["data"].get("play"):
            return r["data"]["play"]
        return None
    except Exception as e:
        print(f"Error while downloading: {e}")
        return None



# Qruplarda /tt komandası ilə video yükləmə
@app.on_message(filters.command("tt"))
async def tiktok_group(client, message: Message):
    try:
        if len(message.command) < 2:
            return await message.reply("ℹ️ İstifadə: /tt  • tiktok linki •")

        url = message.text.split(" ", 1)[1]
        if not is_tiktok_link(url):
            return await message.reply("❌ Etibarlı TikTok linki daxil edin.")

        msg = await message.reply("🔄 Video yüklənir...")
        video_url = get_tiktok_video(url)
        if video_url:
            await msg.delete()
            await message.reply_video(video_url, caption="✅ Logosuz TikTok videosu")
        else:
            await msg.edit("❌ Videonu yükləmək mümkün olmadı.")
    except Exception as e:
        await message.reply(f"⚠️ Xəta baş verdi:\n`{str(e)}`")
