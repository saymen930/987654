from pyrogram import filters
from pyrogram.types import Message
from InflexMusic import app  # Öz bot modulunun adı ilə əvəz et (əgər fərqlidirsə)

@app.on_message(filters.command("me"))
async def me_command(client, message: Message):
    user = message.from_user

    text = f"**👤 İstifadəçi Məlumatı:**\n\n"
    text += f"• 🆔 ID: `{user.id}`\n"
    text += f"• 👤 Ad: `{user.first_name}`\n"
    
    if user.last_name:
        text += f"• 👤 Soyad: `{user.last_name}`\n"

    text += f"• 🌐 Dil: `{user.language_code}`\n"
    text += f"• 💎 Premium: {'✅' if user.is_premium else '❌'}\n"
    text += f"• 🤖 Bot: {'✅' if user.is_bot else '❌'}\n"

    await message.reply_text(text)
