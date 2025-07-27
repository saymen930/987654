from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime
from InflexMusic import app
# Mesaj saylarını yadda saxlamaq üçün
user_message_count = {}
user_message_day = {}

@app.on_message(filters.group & filters.text)
async def message_tracker(client: Client, message: Message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    key = f"{chat_id}:{user_id}"
    today = datetime.utcnow().date()

    # Günü dəyişibsə, sıfırla
    if user_message_day.get(key) != today:
        user_message_count[key] = 0
        user_message_day[key] = today

    # Sayı artır
    user_message_count[key] = user_message_count.get(key, 0) + 1
    count = user_message_count[key]

    # Xüsusi mərhələlərə uyğun cavablar
    if count == 10:
        await message.reply(f"{user_name} sən bu gün 201 mesaj yazmısan 🤩\nKurucu tərəfindən 1 cüt corab qazandınız 😅")
    elif count == 500:
        await message.reply(f"{user_name} gözümüz qamaşdı......😮\nSən bu gün 500 mesaj yazmısan 🫢")
    elif count == 1000:
        await message.reply(f"{user_name} axirət zamanı gəldiii 😲\nBu gün sən 1000 mesaj yazmağı bacardın 😳")
    elif count == 1500:
        await message.reply(f"Yox dahaaaaa {user_name}\nSən bu gün 1500 mesaj yazmağla qrupu dağıdırsan 🐮")
