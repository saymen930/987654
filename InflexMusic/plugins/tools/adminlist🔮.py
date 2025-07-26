from pyrogram import filters
from pyrogram.types import Message
from InflexMusic import app  # app = Inflex()

@app.on_message(filters.command("adminlist") & filters.group)
async def adminlist(_, message: Message):
    chat_id = message.chat.id
    try:
        admins = await app.get_chat_administrators(chat_id)
    except Exception as e:
        return await message.reply(
            f"❌ Admin siyahısını əldə etmək mümkün olmadı.\n\n**Xəta:** `{str(e)}`"
        )

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
