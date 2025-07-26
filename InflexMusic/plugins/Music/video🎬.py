
from InflexMusic import app
#from InflexMusic.core.bot import pls as app
from pyrogram import filters
import os, requests, yt_dlp, re
from youtube_search import YoutubeSearch
import config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def time_to_seconds(time):
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(str(time).split(":"))))

buttons = {
    "markup_for_private": InlineKeyboardMarkup([
        [InlineKeyboardButton('Videolist 🎬', url=f'https://t.me/{config.PLAYLIST_NAME}')]
    ]),
    "add_to_group": InlineKeyboardMarkup([
        [InlineKeyboardButton('️✨️ Qrupa əlavə et ️✨️', url=f'https://t.me/{config.BOT_USERNAME}?startgroup=true')]
    ])
}

def extract_youtube_link(text):
    yt_pattern = r"(https?://)?(www\.)?(youtube\.com/watch\?v=[\w\-]+|youtu\.be/[\w\-]+)"
    match = re.search(yt_pattern, text)
    if match:
        return "https://" + match.group(3)
    return None

@app.on_message(filters.command("video", ["/", "!", ".", "@"]) | filters.regex(r"(youtu\.be/|youtube\.com/watch\?v=)"))
async def video_handler(client, message):
    video_file = None
    thumb_name = None
    try:
        query = " ".join(message.command[1:]) if message.text.startswith(("/", "!", ".", "@")) else message.text
        link = extract_youtube_link(query)

        if not link and message.text.startswith(("/", "!", ".", "@")):
            if not query:
                await message.reply("📌 İstifadə: /video Video adı və ya linki", quote=True)
                return
            search_result = YoutubeSearch(query, max_results=1).to_dict()
            if not search_result:
                await message.reply("❌ Video tapılmadı.")
                return
            result = search_result[0]
            link = f"https://youtube.com{result['url_suffix']}"
        elif not link:
            return  # Sadə mesajdır, heç nə etmə

        m = await message.reply("🔍 Videoya baxılır...")

        ydl_opts = {
            "format": "best",
            "noplaylist": True,
            "quiet": True,
            "outtmpl": "%(title)s.%(ext)s",
            "cookiefile": "cookies/cookies.txt" if os.path.exists("cookies/cookies(7).txt") else None,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            video_file = ydl.prepare_filename(info)
            title = info.get("title", "Video")
            duration = info.get("duration")
            channel = info.get("uploader")
            views = info.get("view_count", 0)
            thumbnail_url = info.get("thumbnail")

        if thumbnail_url:
            thumb_name = f"thumb_{config.BOT_USERNAME}.jpg"
            with open(thumb_name, "wb") as f:
                f.write(requests.get(thumbnail_url).content)

        caption = f"""
🎬 [{title}]({link})
⏳ Müddət: {duration//60}:{duration%60:02d}
👁 Baxış: {views}
👤 İstəyən: {message.from_user.mention}
📡 Kanal: {channel}
"""

        await message.reply_video(
            video=video_file,
            caption=caption,
            duration=duration,
            thumb=thumb_name if os.path.exists(thumb_name) else None,
            supports_streaming=True,
            reply_markup=buttons["markup_for_private"]
        )

        await app.send_video(
            chat_id=config.PLAYLIST_ID,
            video=video_file,
            caption=caption,
            duration=duration,
            thumb=thumb_name if os.path.exists(thumb_name) else None,
            supports_streaming=True,
            reply_markup=buttons["add_to_group"]
        )

        await m.delete()

    except Exception as e:
        await message.reply(f"⚠️ Xəta baş verdi:\n{type(e).__name__}: {str(e)}")
        print("❌ Xəta:", type(e).__name__, e)

    finally:
        try:
            if video_file and os.path.exists(video_file):
                os.remove(video_file)
            if thumb_name and os.path.exists(thumb_name):
                os.remove(thumb_name)
        except Exception as e:
            print("🧹 Təmizlik xətası:", e)
