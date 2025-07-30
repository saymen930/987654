import json
import os
from datetime import datetime
from telethon import TelegramClient, events, Button
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from InflexMusic.core.bot import xaos as client

# Fayl yolları
WELCOME_FILE = 'Jason/welcome.json'
STATUS_FILE = 'Jason/status.json'

# Default mesaj
default_welcome = "Salam {username} 🫂 {chatname} qrupuna xoş gəldin! Necəsən?❤️‍🔥"

# JSON yükləmə və saxlama funksiyaları
def load_json(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)

# Yaddaşdan dataları yüklə
welcome_data = load_json(WELCOME_FILE)
welcome_status = load_json(STATUS_FILE)

# ✅ Qarşılama mesajı (təkrar göndərməni əngəlləyir)
sent_users = set()

@client.on(events.ChatAction)
async def on_user_join(event):
    if not (event.user_joined or event.user_added):
        return

    chat_id = str(event.chat_id)
    if welcome_status.get(chat_id, True) is False:
        return

    for user in event.users:
        if user.id in sent_users:
            continue
        sent_users.add(user.id)

        sender = await client.get_entity(user.id)
        chat = await event.get_chat()

        username = f"@{sender.username}" if sender.username else sender.first_name
        first_name = sender.first_name or ""
        last_name = sender.last_name or ""
        fullname = f"{first_name} {last_name}".strip()
        user_id = sender.id
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chatname = chat.title or "Qrup"

        msg_template = welcome_data.get(chat_id, default_welcome)

        msg = msg_template.format(
            username=username,
            id=user_id,
            fullname=fullname,
            name=first_name,
            time=now,
            chatname=chatname
        )

        await client.send_message(event.chat_id, msg)

# ✅ /setwelcome — mesaj təyin etmək
@client.on(events.NewMessage(pattern=r'^/setwelcome'))
async def set_welcome(event):
    sender = await event.get_sender()
    chat_id = str(event.chat_id)

    try:
        p = await client(GetParticipantRequest(int(chat_id), sender.id))
        if not isinstance(p.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            return await event.reply("⛔ Bu əmri yalnız adminlər istifadə edə bilər.")
    except:
        return

    if event.is_reply:
        reply_msg = await event.get_reply_message()
        new_msg = reply_msg.text
    else:
        parts = event.raw_text.split('\n', 1)
        if len(parts) < 2:
            return await event.reply("Welcome mesajını təyin etmək üçün\n\n/setwelcome <mesaj> və ya hər hansı mesaja reply atın✅")
        new_msg = parts[1]

    welcome_data[chat_id] = new_msg
    save_json(WELCOME_FILE, welcome_data)
    await event.reply("✅ Qarşılama mesajı yeniləndi!")

# ✅ /resetwelcome — default mesaj geri qaytar
@client.on(events.NewMessage(pattern=r'^/resetwelcome$'))
async def reset_welcome(event):
    sender = await event.get_sender()
    chat_id = str(event.chat_id)

    try:
        p = await client(GetParticipantRequest(int(chat_id), sender.id))
        if not isinstance(p.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            return await event.reply("⛔ Bu əmri yalnız adminlər istifadə edə bilər.")
    except:
        return

    welcome_data.pop(chat_id, None)
    save_json(WELCOME_FILE, welcome_data)
    await event.reply("♻️ Qarşılama mesajı sıfırlandı. Default mesaj istifadə olunacaq.")

# ✅ /welcome — cari mesajı göstər və buttonlar
@client.on(events.NewMessage(pattern=r'^/welcome$'))
async def show_welcome(event):
    chat_id = str(event.chat_id)
    msg_template = welcome_data.get(chat_id, default_welcome)
    status = welcome_status.get(chat_id, True)
    status_text = "✅ Aktivdir" if status else "❌ Deaktivdir"

    await event.reply(
        f"📩 {event.chat.title} Qrupunun Welcome Mesajı 🌟\n\n{msg_template}\n\nStatus: {status_text}",
        buttons=[
            [Button.inline("✅ Aktiv et", f"enable:{chat_id}"),
             Button.inline("❌ Deaktiv et", f"disable:{chat_id}")],
            [Button.inline("🔄 Bağla", "close")]
        ]
    )

# ✅ Inline düymələrin idarəsi (admin yoxlamalı)
@client.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode('utf-8')
    sender = await event.get_sender()
    message = await event.get_message()

    # enable:disable:<chat_id>
    if data.startswith("enable:") or data.startswith("disable:"):
        action, cid = data.split(":")

        # Admin yoxlaması
        try:
            p = await client(GetParticipantRequest(int(cid), sender.id))
            is_admin = isinstance(p.participant, (ChannelParticipantAdmin, ChannelParticipantCreator))
            if not is_admin:
                return await event.answer("⛔ Bu əmri yalnız adminlər istifadə edə bilər.", alert=True)
        except:
            return await event.answer("❗ Admin yoxlaması mümkün olmadı.", alert=True)

        # Status dəyiş və yaz
        if action == "enable":
            welcome_status[cid] = True
            await event.edit("✅ Qarşılama mesajı **aktiv** edildi.")
        elif action == "disable":
            welcome_status[cid] = False
            await event.edit("❌ Qarşılama mesajı **deaktiv** edildi.")

        save_json(STATUS_FILE, welcome_status)

    elif data == "close":
        await event.delete()
