from pyrogram import Client, filters
from pyrogram.types import Message

from InflexMusic import app  # Bot instansiyası

@app.on_message(filters.command("adminlist") & filters.group)
async def adminlist(client: Client, message: Message):
    try:
        admins = await client.get_chat_administrators(message.chat.id)
        if not admins:
            return await message.reply("⚠️ Admin siyahısı boşdur.")

        text = "👮‍♂️ *Adminlər siyahısı:*\n\n"
        for admin in admins:
            user = admin.user
            status = "👑 Sahibi" if admin.status == "creator" else "🔧 Admin"
            mention = f"[{user.first_name}](tg://user?id={user.id})"
            username_part = f" (@{user.username})" if user.username else ""
            text += f"- {mention}{username_part} — {status}\n"

        text += "\n📌 *Qeyd:* Siyahı tam güncəldir!"
        await message.reply(text, disable_web_page_preview=True)
    except Exception:
        await message.reply("❌ Admin siyahısını əldə etmək mümkün olmadı.")
