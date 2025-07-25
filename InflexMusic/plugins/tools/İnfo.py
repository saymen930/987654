from pyrogram import filters
from InflexMusic import app  # Sənin musiqi botunun Client obyekti

@app.on_message(filters.command("info") & (filters.group | filters.private))
async def info(client, message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user

    name = user.first_name or "Yoxdur"
    username = f"@{user.username}" if user.username else "Yoxdur"
    user_id = user.id
    profile_link = f"[{name}](tg://user?id={user_id})"

    text = (
        f"👾 *İstifadəçi Adı:* {name}\n"
        f"🔮 *Username:* {username}\n"
        f"🆔 *ID nömrəsi:* `{user_id}`\n"
        f"🥷 *Profil:* {profile_link}"
    )

    await message.reply(text, parse_mode="Markdown")
