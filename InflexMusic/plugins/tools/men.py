from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime

from InflexMusic import app  # bot instance
from InflexMusic.utils.decorators.language import language  # varsa istifadə et, yoxdursa sil

def format_time():
    return datetime.now().strftime("%d.%m.%Y • %H:%M")

@app.on_message(filters.command("men") & filters.group)
async def men_command(client: Client, message: Message):
    user = message.from_user
    chat = await client.get_chat(message.chat.id)
    owner = "Tapılmadı"
    try:
        admins = await client.get_chat_administrators(message.chat.id)
        for admin in admins:
            if admin.status == "creator":
                owner = admin.user.first_name
                break
    except:
        pass

    text = (
        f"▻ | • Ad: {user.first_name}\n"
        f"▻ | • ID: {user.id}\n"
        f"▻ | • Saat: {format_time()}\n"
        f"▻ | • Qrup: {chat.title}\n"
        f"▻ | • Sahibi: {owner}"
    )
    await message.reply(text)

@app.on_message(filters.command(["il", "in", "ki"]) & filters.group)
async def info_commands(client: Client, message: Message):
    user = None
    chat = message.chat
    args = message.text.split()

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(args) > 1:
        try:
            user_id = int(args[1])
            member = await client.get_chat_member(chat.id, user_id)
            user = member.user
        except:
            try:
                username = args[1]
                member = await client.get_chat_member(chat.id, username)
                user = member.user
            except:
                pass
    else:
        user = message.from_user

    if not user:
        return await message.reply("🔺 Zəhmət olmasa, istifadəçini təyin edin ✅")

    if message.text.startswith("/il"):
        return await message.reply(f"Sənin 🆔: {user.id}")

    text = (
        f"▻ | • Ad: {user.first_name}\n"
        f"▻ | • ID: {user.id}\n"
        f"▻ | • Saat: {format_time()}\n"
        f"▻ | • Qrup: {chat.title}"
    )

    if message.text.startswith("/in"):
        try:
            member = await client.get_chat_member(chat.id, user.id)
            if member.status in ["kicked", "left"]:
                text += "\n▻ | • Qadağan: Qadağan olunub 🚫"
            else:
                text += "\n▻ | • Qadağan: Yoxdur ✅"
        except:
            text += "\n▻ | • Qadağan: Məlumat tapılmadı ❔"

    await message.reply(text)
