import re
import requests
from telethon import events
from InflexMusic.core.bot import xaos as client  # səndə necə adlanırsa onu istifadə et

# ----- Helpers -----
def is_tiktok_link(text: str) -> bool:
    return bool(re.search(r"(https?://)?(www\.)?(vm\.tiktok\.com|tiktok\.com)", text))

def get_tiktok_video(url: str):
    try:
        api = "https://tikwm.com/api/"
        r = requests.get(api, params={"url": url}, timeout=15).json()
        if r.get("data") and r["data"].get("play"):
            return r["data"]["play"]
        return None
    except Exception as e:
        print(f"Error while downloading: {e}")
        return None

# ----- Command -----
@client.on(events.NewMessage(pattern=r"^/tt(?:\s+(.+))?$"))
async def tiktok_dl(event: events.NewMessage.Event):
    try:
        url = event.pattern_match.group(1)
        if not url:
            return await event.reply("ℹ️ İstifadə: `/tt <tiktok linki>`", parse_mode="md")

        if not is_tiktok_link(url):
            return await event.reply("❌ Etibarlı TikTok linki daxil edin.")

        msg = await event.reply("🔄 Video yüklənir...")
        video_url = get_tiktok_video(url)

        if video_url:
            try:
                await msg.delete()
            except:
                pass
            await event.client.send_file(
                event.chat_id,
                video_url,
                caption="✅ Buyur.",
                supports_streaming=True
            )
        else:
            await msg.edit("❌ Videonu yükləmək mümkün olmadı.")
    except Exception as e:
        await event.reply(f"⚠️ Xəta baş verdi:\n`{e}`", parse_mode="md")
