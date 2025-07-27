import asyncio
import json
import os
from telethon import TelegramClient, events, Button
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantsAdmins

API_ID = 23470912
API_HASH = "33ac02b7891c5396e6b305802d56cf4f"
BOT_TOKEN = "8234671504:AAFUi0nvY5pmcUvCVRlzKCgp--j5XsOCXo8"

bot = TelegramClient('welcomeBot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Faylları oxu və ya boş obyektlər yarat
if os.path.exists("welcome.json"):
    with open("welcome.json", "r", encoding="utf-8") as f:
        welcome_data = json.load(f)
else:
    welcome_data = {}

if os.path.exists("welstatus.json"):
    with open("welstatus.json", "r", encoding="utf-8") as f:
        welcome_status = json.load(f)
else:
    welcome_status = {}

# Format funksiyası
def parse_welcome(text, user, chat):
    username = f"@{user.username}" if user.username else user.first_name
    firstname = user.first_name or ""
    chatname = chat.title or "Qrup"
    return (
        text.replace("{username}", username)
            .replace("{firstname}", firstname)
            .replace("{chatname}", chatname)
            .replace("{chatname}", id)
    )

# /setwelcome
@bot.on(events.NewMessage(pattern="/setwelcome"))
async def set_welcome(event):
    if not event.is_group:
        return
    chat_id = str(event.chat_id)
    parts = event.raw_text.split("\n", 1)
    if len(parts) < 2 or not parts[1].strip():
        await event.reply("❗️ Zəhmət olmasa /setwelcome əmrindən sonra mesaj yazın.\n\nNümunə:\n`/setwelcome\nSalam {username}, xoş gəldin {chatname}`", parse_mode="md")
        return
    welcome_text = parts[1].strip()
    welcome_data[chat_id] = {"text": welcome_text}
    welcome_status[chat_id] = True

    with open("welcome.json", "w", encoding="utf-8") as f:
        json.dump(welcome_data, f, ensure_ascii=False, indent=4)
    with open("welstatus.json", "w", encoding="utf-8") as f:
        json.dump(welcome_status, f, ensure_ascii=False, indent=4)

    await event.reply("✅ Xoş gəldin mesajı uğurla yadda saxlanıldı.")

# /resetwelcome
@bot.on(events.NewMessage(pattern="/resetwelcome"))
async def reset_welcome(event):
    if not event.is_group:
        return
    chat_id = str(event.chat_id)
    welcome_data.pop(chat_id, None)
    welcome_status[chat_id] = False

    with open("welcome.json", "w", encoding="utf-8") as f:
        json.dump(welcome_data, f, ensure_ascii=False, indent=4)
    with open("welstatus.json", "w", encoding="utf-8") as f:
        json.dump(welcome_status, f, ensure_ascii=False, indent=4)

    await event.reply("♻️ Xoş gəldin mesajı silindi və deaktiv edildi.")

# /welcome (mövcud mesajı göstər və idarə et buttonları ilə)
@bot.on(events.NewMessage(pattern="/welcome"))
async def show_welcome(event):
    if not event.is_group:
        return
    chat_id = str(event.chat_id)
    text = welcome_data.get(chat_id, {}).get("text")
    if not text:
        await event.reply("❌ Qrup üçün heç bir xoş gəldin mesajı təyin olunmayıb.")
        return

    status = welcome_status.get(chat_id, False)
    status_text = "✅ Aktivdir" if status else "❌ Deaktivdir"
    await event.reply(
        f"📨 Hazırda olan Xoş Gəldin Mesajı:\n\n{text}\n\nStatus: {status_text}",
        buttons=[
            [
                Button.inline("✅ Aktiv et", data=f"welon:{chat_id}"),
                Button.inline("❌ Deaktiv et", data=f"weloff:{chat_id}")
            ],
            [Button.inline("🔄 Bağla", data="close")]
        ]
    )

# Inline Button Handler
@bot.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode("utf-8")

    if data.startswith("welon:"):
        chat_id = data.split(":")[1]
        welcome_status[chat_id] = True
        with open("welstatus.json", "w", encoding="utf-8") as f:
            json.dump(welcome_status, f, ensure_ascii=False, indent=4)
        await event.edit("✅ Xoş gəldin mesajı aktiv edildi.")

    elif data.startswith("weloff:"):
        chat_id = data.split(":")[1]
        welcome_status[chat_id] = False
        with open("welstatus.json", "w", encoding="utf-8") as f:
            json.dump(welcome_status, f, ensure_ascii=False, indent=4)
        await event.edit("❌ Xoş gəldin mesajı deaktiv edildi.")

    elif data == "close":
        await event.delete()

# Yeni üzv üçün mesaj
@bot.on(events.ChatAction())
async def welcome_user(event):
    if not event.user_joined and not event.user_added:
        return
    chat_id = str(event.chat_id)
    if not welcome_status.get(chat_id) or chat_id not in welcome_data:
        return

    try:
        user = await bot(GetFullUserRequest(event.user_id))
        user_info = user.user
    except Exception:
        user_info = event.user

    text = parse_welcome(welcome_data[chat_id].get("text", ""), user_info, event.chat)
    await event.reply(text)

print("🤖 Bot işə düşdü!")
bot.run_until_disconnected()
