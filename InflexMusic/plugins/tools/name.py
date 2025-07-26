from pyrogram import Client, filters
from pyrogram.types import Message

from InflexMusic import app  # sənin bot instansın

# Global dictionary istifadəçi adlarını yadda saxlamaq üçün
user_names = {}

@app.on_message(filters.group & ~filters.service)  # yalnız qrup mesajları, system mesajlar deyil
async def handle_all_messages(client: Client, message: Message):
    if not message.from_user:
        return  # anonymous admin və ya sistem mesajları

    user_id = message.from_user.id
    current_name = message.from_user.first_name

    if user_id in user_names and user_names[user_id] != current_name:
        chat_name = message.chat.title or "Bu Qrup"
        await message.reply(
            f"📛 *Adını dəyişdi*\n"
            f"🔙 Köhnə: `{user_names[user_id]}`\n"
            f"🔜 Yeni: `{current_name}`\n"
            f"💬 Qrup: {chat_name}"
        )

    # Cari adı yadda saxla
    user_names[user_id] = current_name
