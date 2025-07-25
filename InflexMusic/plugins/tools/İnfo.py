from pyrogram import Client, filters
from pyrogram.types import Message

from InflexMusic import app  # səndə app Client obyekti belə adlanırsa

@app.on_message(filters.command("info") & filters.private)
async def info(client: Client, message: Message):
    user = message.from_user

    # İstifadəçi məlumatları
    name = user.first_name or "Yoxdur"
    username = f"@{user.username}" if user.username else "Yoxdur"
    user_id = user.id
    profile_link = f'<a href="tg://user?id={user_id}">{name}</a>'

    # Profil şəkli varsa götür
    photos = await client.get_profile_photos(user.id)
    if photos.total_count > 0:
        photo_id = photos.photos[0].file_id
    else:
        photo_id = None

    text = (
        f"👾 <b>İstifadəçi Adı:</b> {name}\n"
        f"🔮 <b>Username:</b> {username}\n"
        f"🆔 <b>ID nömrəsi:</b> <code>{user_id}</code>\n"
        f"🥷 <b>Profil:</b> {profile_link}"
    )

    if photo_id:
        await message.reply_photo(
            photo_id,
            caption=text,
            parse_mode="html"
        )
    else:
        await message.reply(
            text,
            parse_mode="html"
        )
