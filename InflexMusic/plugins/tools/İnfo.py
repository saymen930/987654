from pyrogram import filters
from InflexMusic import app  # Sənin musiqi botunun Client obyekti

@app.on_message(filters.command("info") & (filters.group | filters.private))
async def info(client, message):
    if message.chat.type != "private" and not message.reply_to_message:
        return await message.reply(
            "📌 Qrupda bu əmri işlətmək üçün bir mesaja cavab ver!\n"
            "Məs: Mesajı reply edib /info yaz."
        )

    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user

    name = user.first_name or "Yoxdur"
    username = f"@{user.username}" if user.username else "Yoxdur"
    user_id = user.id

    text = (
        f"👾 İstifadəçi Adı: {name}\n"
        f"🔮 Username: {username}\n"
        f"🆔 ID nömrəsi: {user_id}\n"
        f"🥷 Profil: tg://user?id={user_id}"
    )

    await message.reply(text)
