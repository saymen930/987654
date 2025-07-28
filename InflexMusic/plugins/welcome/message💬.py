import json
import os
import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from telethon.sessions import StringSession


# 📁 Mesaj sayını saxlamaq üçün fayl
MESSAGE_COUNT_FILE = "Jason/message_counts.json"

# 📌 Mərhələlər
milestones = {
    200: "{username} gəlməyinlə qrupu qızışdırdı bravooo🫂",
    500: "Partlayışın ən böyük səbəbiii😲\n{username} tam olaraq 500 mesaj yazıb 🤩",
    1000: "Axirət dönəmi baş vurur🫢 {username} 1000 mesaj ilə qrupu dağıdır 😍",
    1300: "Ola bilməzzz😮 Qrupunun legendi 1300 mesaj yazdı🥴",
    1500: "Göründüyü kimi dağıdıcı qüvvə gəlir 🚀 {username} qrupu partladır 🫨",
    2000: "Kilometr fərqinə baxmayaraq amperajdan kəllə vuran {username} 2000 mesaj yazmağı bacardı😱"
}

# 🔄 Fayl idarəsi
def load_message_counts():
    if os.path.exists(MESSAGE_COUNT_FILE):
        try:
            with open(MESSAGE_COUNT_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("[WARNING] message_counts.json faylı pozulub, sıfırdan başlayırıq.")
            return {}
    return {}

def save_message_counts(data):
    with open(MESSAGE_COUNT_FILE, "w") as f:
        json.dump(data, f)

# 🕐 Gündəlik sıfırlama funksiyası
async def daily_reset():
    while True:
        now = datetime.utcnow() + timedelta(hours=4)  # Bakı vaxtı
        next_reset = (now + timedelta(days=1)).replace(hour=1, minute=0, second=0, microsecond=0)
        wait_seconds = (next_reset - now).total_seconds()
        print(f"[RESET TIMER] Növbəti sıfırlama: {next_reset} (Bakı vaxtı)")
        await asyncio.sleep(wait_seconds)

        save_message_counts({})
        print("[RESET] Mesaj sayları sıfırlandı (01:00 Bakı vaxtı)")

# 📊 Mesaj izləmə
@client.on(events.NewMessage)
async def handler(event):
    if not event.is_group:
        return

    sender = await event.get_sender()
    if sender.bot:
        return  # Bot öz mesajlarını saymasın

    chat_id = str(event.chat_id)
    user_id = str(sender.id)
    username = sender.first_name

    data = load_message_counts()

    if chat_id not in data:
        data[chat_id] = {}

    if user_id not in data[chat_id]:
        data[chat_id][user_id] = 0

    data[chat_id][user_id] += 1
    user_count = data[chat_id][user_id]

    if user_count in milestones:
        text = milestones[user_count].format(username=username)
        await event.reply(text)

    save_message_counts(data)
