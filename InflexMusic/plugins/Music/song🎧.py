from InflexMusic import app
from pyrogram import filters
import os, requests, yt_dlp, re
from youtube_search import YoutubeSearch
import config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def time_to_seconds(time):
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(str(time).split(":"))))

# Qadağan olunmuş simvolları təmizləyən funksiya
def safe_filename(name):
    return re.sub(r'[^a-zA-Z0-9_\-() ]', '', name)



@app.on_message(filters.command("song", ["/", "!", ".", "@"]))
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
        safe_title = safe_filename(title)
        duration = result["duration"]
        views = result["views"]
        channel = result["channel"]
        thumbnail_url = result["thumbnails"][0]

        thumb_name = f'thumb_{config.BOT_USERNAME}.jpg'
        with open(thumb_name, 'wb') as f:
            f.write(requests.get(thumbnail_url).content)

        ydl_opts = {
            "format": "bestaudio[ext=m4a]",
            "outtmpl": f"{safe_title}.m4a",
            "noplaylist": True,
            "extractor_args": {'youtubetab': {'skip': 'authcheck'}},
        }

        if os.path.exists("cookies/cookies(7).txt"):
            ydl_opts["cookiefile"] = "cookies/cookies(7).txt"

        m.delete()

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            audio_file = ydl.prepare_filename(info)

        dur = time_to_seconds(duration)

        caption = f"🎧 Ad: {title}\n⏰ Vaxt: {duration}"


        buttons = {
    "markup_for_private": InlineKeyboardMarkup([
        [InlineKeyboardButton('🎧 Playlist', url=f'https://t.me/{config.PLAYLIST_NAME}')]
    ]),
    "add_to_group": InlineKeyboardMarkup([
        [InlineKeyboardButton('️✨️ Qrupa əlavə et ️✨️', url=f'https://t.me/{config.BOT_USERNAME}?startgroup=true')],
        [InlineKeyboardButton('️✨️ YouTube Linki ✨️', url=f'{link}')]
    ])
        }
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
            chat_id=config.PLAYLIST_ID,
            audio=audio_file,
            caption=caption,
            title=title,
            duration=dur,
            performer=channel,
            thumb=thumb_name,
            reply_markup=buttons["add_to_group"]
        )

    except Exception as e:
        m.edit(f"⚠️ Xəta baş verdi:\n{type(e).__name__}: {str(e)}")
        print("❌ Xəta:", type(e).__name__, e)

    finally:
        try:
            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)
            if thumb_name and os.path.exists(thumb_name):
                os.remove(thumb_name)
        except Exception as e:
            print("🧹 Təmizlik xətası", e)































