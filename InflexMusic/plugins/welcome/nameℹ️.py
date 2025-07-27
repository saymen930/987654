from telethon import TelegramClient, events
from datetime import datetime
import pytz  # pip install pytz
from InflexMusic.core.bot import xaos as client

user_names = {}  # user_id: first_name

@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    if not sender:
        return

    user_id = sender.id
    current_name = sender.first_name or ""

    old_name = user_names.get(user_id)
    if old_name and old_name != current_name:
        # Bakı vaxtı ilə saat
        baku_tz = pytz.timezone('Asia/Baku')
        now_baku = datetime.now(baku_tz)
        time_str = now_baku.strftime("%H:%M:%S")

        message = (
            f"🔄 Adı dəyişdi\n"
            f"🆔 {user_id}\n"
            f"🗓️ {time_str}\n\n"
            f"📇 Köhnə ad: {old_name}\n"
            f"🆕 Yeni ad: {current_name}"
        )
        await event.reply(message)

    user_names[user_id] = current_name
