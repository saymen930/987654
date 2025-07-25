from InflexMusic import app
from pyrogram import filters
import os, requests, yt_dlp
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Zamanı saniyəyə çevir
def time_to_seconds(time):
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(str(time).split(":"))))

# Parametrlər
PLAYLIST_NAME = "XAOS_PlayAudiolist"
BOT_USERNAME = "Flashtaggerbot"  # Burada @ işarəsi olmur
PLAYLIST_ID = "-1005890868081"

# Buttonlar
buttons = {
    "markup_for_private": InlineKeyboardMarkup([
        [InlineKeyboardButton('Playlist 🎧', url=f'https://t.me/{PLAYLIST_NAME}')]
    ]),
    "add_to_group": InlineKeyboardMarkup([
        [InlineKeyboardButton('️✨️ Qrupa əlavə et ️✨️', url=f'https://t.me/{BOT_USERNAME}?startgroup=true')]
    ])
}

# Komanda filter - düzgün və universal
@app.on_message(filters.command("song", prefixes=["/", "!", "."]) & (filters.private | filters.group))
def song(client, message):
    audio_file = None
    thumb_name = None

    try:
        if len(message.command) < 2:
            message.reply("📌 İstifadə: /song Mahnının adı", quote=True)
            return

        query = " ".join(message.command[1:])
        m = message.reply(f"🔍 Axtarılır: {query}")

        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            m.edit("❌ Mahnı tapılmadı.")
            return

        result = results[0]
        link = f"https://youtube.com{result['url_suffix']}"
        title = result["title"][:100]
        duration = result["duration"]
        views = result["views"]
        channel = result["channel"]
        thumbnail_url = result["thumbnails"][0]

        thumb_name = f'thumb_{BOT_USERNAME}.jpg'
        with open(thumb_name, 'wb') as f:
            f.write(requests.get(thumbnail_url).content)

        ydl_opts = {
            "format": "bestaudio[ext=m4a]",
            "outtmpl": f"{title}.m4a",
            "noplaylist": True,
            "extractor_args": {'youtubetab': {'skip': 'authcheck'}},
        }

        if os.path.exists("cookies/cookies(7).txt"):
            ydl_opts["cookiefile"] = "cookies/cookies(7).txt"

        m.edit("📥 Yüklənir...")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            audio_file = ydl.prepare_filename(info)

        dur = time_to_seconds(duration)

        caption = f"""
🎧 [{title}]({link})
⏰ {duration}
"""

        message.reply_audio(
            audio=audio_file,
            caption=caption,
            title=title,
            duration=dur,
            performer=channel,
            thumb=thumb_name,
            reply_markup=buttons["markup_for_private"]
        )

        app.send_audio(
            chat_id=PLAYLIST_ID,
            audio=audio_file,
            caption=caption,
            title=title,
            duration=dur,
            performer=channel,
            thumb=thumb_name,
            reply_markup=buttons["add_to_group"]
        )

    except Exception as e:
        if m:
            m.edit(f"⚠️ Xəta baş verdi:\n{type(e).__name__}: {str(e)}")
        print("❌ Xəta:", type(e).__name__, e)

    finally:
        try:
            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)
            if thumb_name and os.path.exists(thumb_name):
                os.remove(thumb_name)
        except Exception as e:
            print("🧹 Təmizlik xətası:", e)
