from InflexMusic import app
from pyrogram import filters
import os, requests, yt_dlp, re
from youtube_search import YoutubeSearch
import config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def time_to_seconds(time):
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(str(time).split(":"))))



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
    m = None

    try:
        # Komanda və ya sadə linkli mesaj
        is_command = message.text.startswith(("/", "!", ".", "@"))
        query = " ".join(message.command[1:]) if is_command else message.text.strip()
        link = extract_youtube_link(query)

        # Əgər link yoxdursa, axtarış et
        if not link:
            if is_command:
                if not query:
                    return await message.reply("📌 İstifadə: /video Video adı və ya linki", quote=True)
                search_result = YoutubeSearch(query, max_results=1).to_dict()
                if not search_result or not search_result[0].get("url_suffix"):
                    return await message.reply("❌ Video tapılmadı.")
                result = search_result[0]
                link = f"https://youtube.com{result['url_suffix']}"
            else:
                return  # Sadə, amma uyğun olmayan mesaj – heç nə etmə

        m = await message.reply("🔍 Videoya baxılır...")

        ydl_opts = {
            "format": "best",
            "noplaylist": True,
            "quiet": True,
            "outtmpl": "%(title)s.%(ext)s",
        }

        # Cookie varsa əlavə et
        cookie_path = "cookies/cookies(7).txt"
        if os.path.exists(cookie_path):
            ydl_opts["cookiefile"] = cookie_path

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            video_file = ydl.prepare_filename(info)
            title = info.get("title", "Video")
            duration = info.get("duration", 0)
            channel = info.get("uploader", "Bilinmir")
            views = info.get("view_count", 0)
            thumbnail_url = info.get("thumbnail")

        # Thumbnail yüklə
        if thumbnail_url:
            thumb_name = f"thumb_{config.BOT_USERNAME}.jpg"
            try:
                with open(thumb_name, "wb") as f:
                    f.write(requests.get(thumbnail_url).content)
            except Exception as e:
                print("Thumbnail yükləmə xətası:", e)
                thumb_name = None

        # Caption
        minutes, seconds = divmod(duration, 60)
        caption = f"""
🎬 Ad: {title}
⏳ Vaxt: {minutes}:{seconds:02d}
"""



        buttons = {
    "markup_for_private": InlineKeyboardMarkup([
        [InlineKeyboardButton('Playlist 🎧', url=f'https://t.me/{Config.PLAYLIST_NAME}')]
    ]),
    "add_to_group": InlineKeyboardMarkup([
        [InlineKeyboardButton('️✨️ Qrupa əlavə et ️✨️', url=f'https://t.me/{Config.BOT_USERNAME}?startgroup=true')],
        [InlineKeyboardButton('️✨️ YouTube Linki ✨️', url=f'{link}')]
    ])
        }
        # Göndər istifadəçiyə
        await message.reply_video(
            video=video_file,
            caption=caption,
            duration=duration,
            thumb=thumb_name if thumb_name and os.path.exists(thumb_name) else None,
            supports_streaming=True,
            reply_markup=buttons["markup_for_private"]
        )

        # Kanalda paylaş
        await app.send_video(
            chat_id=config.PLAYLIST_ID,
            video=video_file,
            caption=caption,
            duration=duration,
            thumb=thumb_name if thumb_name and os.path.exists(thumb_name) else None,
            supports_streaming=True,
            reply_markup=buttons["add_to_group"]
        )

        await m.delete()

    except Exception as e:
        if m:
            await m.edit(f"⚠️ Xəta baş verdi:\n`{type(e).__name__}: {str(e)}`")
        else:
            await message.reply(f"⚠️ Xəta baş verdi:\n`{type(e).__name__}: {str(e)}`")
        print("❌ Xəta:", type(e).__name__, e)

    finally:
        try:
            if video_file and os.path.exists(video_file):
                os.remove(video_file)
            if thumb_name and os.path.exists(thumb_name):
                os.remove(thumb_name)
        except Exception as e:
            print("🧹 Təmizlik xətası:", e)
