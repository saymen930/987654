import os, time
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message, User
from pyrogram.errors import UserNotParticipant

from InflexMusic.core.bot import pls as app  # Bot instance

# 🧠 İstifadəçini müəyyənləşdirən funksiya
def extract_user(message: Message) -> (int, str):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        return user.id, user.first_name
    elif len(message.command) > 1:
        arg = message.command[1]
        if message.entities and len(message.entities) > 1 and message.entities[1].type == "text_mention":
            entity = message.entities[1]
            return entity.user.id, entity.user.first_name
        try:
            return int(arg), arg
        except ValueError:
            return arg, arg  # username
    else:
        return message.from_user.id, message.from_user.first_name

# 🕓 Son görülmə vaxtı
def last_online(user: User) -> str:
    if user.is_bot:
        return "🤖 Bot"
    status = user.status
    if status == "recently":
        return "Yaxınlarda"
    elif status == "within_week":
        return "Son 1 həftədə"
    elif status == "within_month":
        return "Son 1 ayda"
    elif status == "long_time_ago":
        return "Çox uzun müddət əvvəl"
    elif status == "online":
        return "Hazırda onlayndır"
    elif status == "offline":
        return datetime.fromtimestamp(user.last_online_date).strftime("%d.%m.%Y • %H:%M")
    return "Bilinmir"

# 🔍 /info komandası
@app.on_message(filters.command("info", ["/", ".", "!"]) & filters.group)
async def info(client: Client, message: Message):
    status_msg = await message.reply("🔎 İstifadəçi axtarılır...")

    user_id, _ = extract_user(message)
    try:
        user = await client.get_users(user_id)
    except Exception as e:
        await status_msg.edit(f"⚠️ Xəta: `{e}`")
        return

    # Əsas məlumatlar
    text = f"<b>🛰 Telegram Məlumatları</b>\n\n"
    text += f"👤 <b>Ad:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
    text += f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
    if user.username:
        text += f"🔗 <b>İstifadəçi adı:</b> @{user.username}\n"
        text += f"🔗 <b>Link:</b> <a href='https://t.me/{user.username}'>https://t.me/{user.username}</a>\n"
    text += f"🕓 <b>Son görünmə:</b> {last_online(user)}\n"
    if user.is_deleted:
        text += "🗑 <b>Hesab silinib</b>\n"
    if user.is_verified:
        text += "✅ <b>Doğrulanmış istifadəçi</b>\n"
    if user.is_scam:
        text += "⚠️ <b>Fırıldaqçı istifadəçi</b>\n"

    # Qrupda qoşulma vaxtı
    try:
        chat_member = await message.chat.get_member(user.id)
        if chat_member.joined_date:
            join_time = datetime.fromtimestamp(chat_member.joined_date).strftime("%d.%m.%Y • %H:%M")
            text += f"👥 <b>Qrupa qoşuldu:</b> {join_time}\n"
    except UserNotParticipant:
        text += "📤 <b>İstifadəçi bu qrupda deyil</b>\n"

    # Foto varsa göstər
    if user.photo:
        photo = await client.download_media(user.photo.big_file_id)
        await message.reply_photo(photo, caption=text)
        os.remove(photo)
    else:
        await message.reply(text, disable_web_page_preview=True)

    await status_msg.delete()
