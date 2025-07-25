from pyrogram import Client, filters
from InflexMusic import app  # Səndə `app` necədirsə, eyni saxla

@app.on_message(filters.command("info") & (filters.group | filters.private))
async def info(client: Client, message):
    # Qrupda başqasının məlumatını almaq üçün cavab yoxla
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = message.from_user

    name = user.first_name or "Yoxdur"
    username = f"@{user.username}" if user.username else "Yoxdur"
    user_id = user.id
    profile_link = f'<a href="tg://user?id={user_id}">{name}</a>'

    text = (
        f"👾 <b>İstifadəçi Adı:</b> {name}\n"
        f"🔮 <b>Username:</b> {username}\n"
        f"🆔 <b>ID nömrəsi:</b> <code>{user_id}</code>\n"
        f"🥷 <b>Profil:</b> {profile_link}"
    )

await message.reply(
    text,
    parse_mode="HTML"
)
