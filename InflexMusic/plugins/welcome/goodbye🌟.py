import json
import os
import random
from telethon import TelegramClient, events, Button
from InflexMusic.core.bot import xaos as client  # Sənin bot instance

GOODBYE_FILE = "Jason/goodbye_data.json"

if not os.path.exists(GOODBYE_FILE):
    with open(GOODBYE_FILE, "w") as f:
        json.dump({}, f)

def load_goodbye_data():
    with open(GOODBYE_FILE, "r") as f:
        return json.load(f)

def save_goodbye_data(data):
    with open(GOODBYE_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Son unban edilmiş istifadəçiləri saxlayan set
recently_unbanned_users = set()

@client.on(events.NewMessage(pattern=r"/goodbye(?:\s+(\w+))?", chats=None))
async def goodbye_command(event):
    if not event.is_group:
        await event.reply("Bu əmri yalnız qruplarda istifadə edə bilərsiniz.")
        return

    data = load_goodbye_data()
    chat_id = str(event.chat_id)

    sender = await event.get_sender()
    member = await client.get_permissions(event.chat_id, sender.id)
    if not (member.is_admin or member.is_creator):
        await event.reply("❗ Bu əmri yalnız qrup adminləri istifadə edə bilər.")
        return

    arg = event.pattern_match.group(1)

    if not arg:
        buttons = [
            [Button.inline("Aktif Etmək ✅", b"goodbye_on"), Button.inline("Deaktiv Etmək ❌", b"goodbye_off")],
            [Button.inline("Bağla 🔄", b"goodbye_close")],
        ]
        await event.reply("GoodBye funksiyasının bağlanması üçün düymələrdən istifadə edin 🕺", buttons=buttons)
        return

    arg = arg.lower()
    if arg == "on":
        data[chat_id] = True
        save_goodbye_data(data)
        await event.reply("✅ Goodbye mesajı **aktiv** edildi.", parse_mode="md")
    elif arg == "off":
        data[chat_id] = False
        save_goodbye_data(data)
        await event.reply("❌ Goodbye mesajı **deaktiv** edildi.", parse_mode="md")
    else:
        await event.reply("❗Yanlış seçim. `on` və ya `off` yaz.", parse_mode="md")

@client.on(events.CallbackQuery(pattern=b"goodbye_.*"))
async def callback_handler(event):
    data = load_goodbye_data()
    chat_id = str(event.chat_id)
    user_id = event.sender_id

    member = await client.get_permissions(event.chat_id, user_id)
    if not (member.is_admin or member.is_creator):
        await event.answer("❗Bu əmri yalnız adminlər istifadə edə bilər.", alert=True)
        return

    data_code = event.data.decode("utf-8")

    if data_code == "goodbye_on":
        data[chat_id] = True
        save_goodbye_data(data)
        await event.edit("✅ Goodbye mesajı **aktiv** edildi.")
        await event.answer("Aktiv edildi!")
    elif data_code == "goodbye_off":
        data[chat_id] = False
        save_goodbye_data(data)
        await event.edit("❌ Goodbye mesajı **deaktiv** edildi.")
        await event.answer("Deaktiv edildi!")
    elif data_code == "goodbye_close":
        await event.delete()
        await event.answer("Mesaj bağlandı.")

# Unban əmri (sadə nümunə)
@client.on(events.NewMessage(pattern=r"/unban(?:\s+(\S+))?"))
async def unban_command(event):
    if not event.is_group:
        await event.reply("Bu əmri yalnız qruplarda istifadə edə bilərsiniz.")
        return

    sender = await event.get_sender()
    member = await client.get_permissions(event.chat_id, sender.id)
    if not (member.is_admin or member.is_creator):
        await event.reply("❗ Bu əmri yalnız qrup adminləri istifadə edə bilər.")
        return

    args = event.message.text.split()
    if len(args) < 2:
        await event.reply("❗ İstifadəçi ID və ya username daxil edin.")
        return

    target = args[1]

    try:
        if target.startswith("@"):
            target_entity = await client.get_entity(target)
        else:
            target_entity = await client.get_entity(int(target))
    except Exception:
        await event.reply("❗ İstifadəçi tapılmadı.")
        return

    try:
        await client.edit_permissions(event.chat_id, target_entity.id, view_messages=True)
        # Unban olunan istifadəçini yadda saxla
        recently_unbanned_users.add((event.chat_id, target_entity.id))
        await event.reply(f"✅ {target} qadağa götürüldü.")
    except Exception as e:
        await event.reply(f"❗ Xəta baş verdi: {e}")

@client.on(events.ChatAction())
async def member_left_handler(event):
    if event.user_left or event.user_kicked:
        data = load_goodbye_data()
        chat_id = event.chat_id
        user_id = event.user_id

        if not data.get(str(chat_id), False):
            return

        bot_self = await client.get_me()
        if user_id == bot_self.id:
            return

        # Əgər istifadəçi unban olunmuş istifadəçilər siyahısındadırsa goodbye mesajı göndərmə
        if (chat_id, user_id) in recently_unbanned_users:
            recently_unbanned_users.remove((chat_id, user_id))
            return

        left_user = await event.get_user()
        name = left_user.first_name or "İstifadəçi"

        goodbye_messages = [
            f"{name} çıxdı, canımız qurtardı 😂",
            f"{name} bezdi getdi 😒",
            f"{name} getdi... darıxmayacağıq 🫡",
            f"{name} artıq yoxdu, rahat nəfəs ala bilərik 🧘",
            f"{name} çıxdı, qapını ört get 🙃",
            f"{name} çıxıb... bəlkə də geri dönər? yox eee dönməsin 😌",
            f"{name} çıxan kimi qrup işıqlanmağa başladı 🔆",
            f"{name} sağ ol ki, getdin bro ✌️",
            f"{name} sənsiz daha sakit oldu 💤",
            f"{name} çıxdı, indi daha az drama var 🫣",
            f"{name} əfsanə getdi... yox eee, sıradan biri idi 😅",
        ]

        await client.send_message(event.chat_id, random.choice(goodbye_messages))
