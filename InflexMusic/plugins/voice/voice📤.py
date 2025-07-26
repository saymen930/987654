from InflexMusic import app
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime

pinned_messages = {}
chat_start_times = {}  # Hər qrup üçün start vaxtını yadda saxlayırıq



# Görüntülü söhbət başladıqda
@app.on_message(filters.video_chat_started & filters.group)
async def video_chat_started_handler(client: Client, message: Message):
    chat_id = message.chat.id
    text = "💁<b>Qrupda səsli söhbət başladı!</b>"

    msg = await message.reply(text)
    await client.pin_chat_message(chat_id=chat_id, message_id=msg.id)
    pinned_messages[chat_id] = msg.id

    # Başlama vaxtını yadda saxla
    chat_start_times[chat_id] = datetime.now()


# Görüntülü söhbət bitdikdə
@app.on_message(filters.video_chat_ended & filters.group)
async def video_chat_ended_handler(client: Client, message: Message):
    chat_id = message.chat.id

    # Davametmə müddətini hesabla
    if chat_id in chat_start_times:
        start_time = chat_start_times[chat_id]
        duration = datetime.now() - start_time
        seconds = int(duration.total_seconds())
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        duration_text = f"{hours} saat, {mins} dəqiqə, {secs} saniyə"
        del chat_start_times[chat_id]
    else:
        duration_text = "Naməlum"

    end_text = f"💆<b>Səsli söhbət sona çatdı</b>\n⏳<b>Davam etdi-</b> {duration_text}"

    # Pinlənmiş mesajı sil
    if chat_id in pinned_messages:
        try:
            await client.unpin_chat_message(chat_id, pinned_messages[chat_id])
            await client.delete_messages(chat_id, pinned_messages[chat_id])
            del pinned_messages[chat_id]
        except Exception as e:
            print(f"Pin silinmədi: {e}")

    await message.reply(end_text)



