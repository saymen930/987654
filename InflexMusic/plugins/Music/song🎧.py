from InflexMusic import app
from pyrogram import filters
import os, requests, yt_dlp, re
from youtube_search import YoutubeSearch
import config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def time_to_seconds(time):
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(str(time).split(":"))))


buttons = {
    "markup_for_private": InlineKeyboardMarkup([
        [InlineKeyboardButton('Playlist 🎧', url=f'https://t.me/{config.PLAYLIST_NAME}')]
    ]),
    "add_to_group": InlineKeyboardMarkup([
        [InlineKeyboardButton('️✨️ Qrupa əlavə et ️✨️', url=f'https://t.me/{config.BOT_USERNAME}?startgroup=true')]
    ])
}


@app.on_message(filters.command("song", ["/", "!", ".", "@"]))
async def song(client, message):
    audio_file = None
    thumb_name = None
    m = None

    try:
        if len(message.command) < 2:
            return await message.reply("📌 İstifadə: /song Mahnının adı", quote=True)

        query = " ".join(message.command[1:])
        m = await message.reply(f"🔍 Axtarılır: {query}")

        results = YoutubeSearch(query, max_results=1).to_dict()

        if not results or not isinstance(results, list) or not results[0].get("url_suffix", "").startswith("/watch"):
            return await m.edit("❌ Mahnı tapılmadı və ya düzgün məlumat alınmadı.")

        result = results[0]
        link = f"https://youtube.com{result.get('url_suffix', '')}"
        title = result.get("title", "Adsız Mahnı")[:100]
        duration = result.get("duration", "0:00")
        channel = result.get("channel", "Bilinmir")

        safe_title = re.sub(r'[\\/*?:"<>|]', "", title)

        thumbnail_url = result.get("thumbnails", [None])[0]
        if thumbnail_url:
            thumb_name = f"thumb_{config.BOT_USERNAME}.jpg"
            try:
                with open(thumb_name, 'wb') as f:
                    f.write(requests.get(thumbnail_url).content)
            except Exception as e:
                print("Thumbnail yükləmə xətası:", e)
                thumb_name = None

        ydl_opts = {
            "format": "bestaudio[ext=m4a]",
            "outtmpl": f"{safe_title}.m4a",
            "noplaylist": True,
            "extractor_args": {'youtubetab': {'skip': 'authcheck'}},
        }

        if os.path.exists("cookies/cookies(7).txt"):
            ydl_opts["cookiefile"] = "cookies/cookies(7).txt"

        await m.edit("🎧 Mahnı yüklənir...")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            audio_file = ydl.prepare_filename(info)

        dur = time_to_seconds(duration)
        caption = f"🎧 [{title}]({link})\n⏰ {duration}"

        await message.reply_audio(
            audio=audio_file,
            caption=caption,
            title=title,
            duration=dur,
            performer=channel,
            thumb=thumb_name if thumb_name else None,
            reply_markup=buttons["markup_for_private"],
            parse_mode="md"
        )

        await app.send_audio(
            chat_id=config.PLAYLIST_ID,
            audio=audio_file,
            caption=caption,
            title=title,
            duration=dur,
            performer=channel,
            thumb=thumb_name if thumb_name else None,
            reply_markup=buttons["add_to_group"],
            parse_mode="md"
        )

        await m.delete()

    except Exception as e:
        try:
            if m:
                await m.edit(f"⚠️ Xəta baş verdi:\n`{type(e).__name__}: {str(e)}`")
        except:
            pass
        print("❌ Xəta:", type(e).__name__, e)

    finally:
        try:
            if audio_file and os.path.exists(audio_file):
                os.remove(audio_file)
            if thumb_name and os.path.exists(thumb_name):
                os.remove(thumb_name)
        except Exception as e:
            print("🧹 Təmizlik xətası:", e)
