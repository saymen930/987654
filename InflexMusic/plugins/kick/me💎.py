from pyrogram import filters
from pyrogram.types import Message
from InflexMusic import app  # Öz bot modulunun adı ilə əvəz et (əgər fərqlidirsə)

@app.on_message(filters.command("me"))
async def me_command(client, message: Message):
    user = message.from_user

    text = f"<b>👤 İstifadəçi Məlumatı:</b>\n\n"
    text += f"<b>• 🆔 ID: {user.id}</b>\n"
    text += f"<b>• 👤 Ad: {user.first_name}</b>\n"
    
    if user.last_name:
        text += f"<b>• 👤 Soyad: {user.last_name}</b>\n"

    text += f"<b>• 🌐 Dil: {user.language_code}</b>\n"
    text += f"• 💎 Premium: {'✅' if user.is_premium else '❌'}\n"
    text += f"• 🤖 Bot: {'✅' if user.is_bot else '❌'}\n"

    await message.reply_text(text)
