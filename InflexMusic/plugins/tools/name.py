from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
from InflexMusic import app  # Sənin layihə modulu

usernames = {}

@app.on_message(filters.group & filters.text)
async def detect_name_change(client: Client, message: Message):
    user = message.from_user
    user_id = user.id
    current_name = user.first_name
    if user.last_name:
        current_name += " " + user.last_name

    old_name = usernames.get(user_id)
    if old_name is None:
        usernames[user_id] = current_name
    else:
        if old_name != current_name:
            usernames[user_id] = current_name
            chat_title = message.chat.title or "Qrup"
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            alert_text = (
                "Ad dəyişdirildi 🔃\n"
                f"🆕 Yeni Adı  {current_name}\n"
                f"🔄 Köhnə adı  {old_name}\n"
                f"🆔 ID  {user_id}\n"
                f"⏳ Tarix {now}\n"
                f"💬 Chat {chat_title}"
            )
            await message.reply_text(alert_text)
