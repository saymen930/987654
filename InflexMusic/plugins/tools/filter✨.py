from pyrogram import Client, filters
from pyrogram.types import Message
from typing import Dict
import asyncio
from InflexMusic import app  # sənin botun `app` ola bilər

# Filterlər yaddaşı üçün dict
filters_dict: Dict[int, Dict[str, str]] = {}


# Admin yoxlama funksiyası
async def is_admin(user_id: int, chat_id: int) -> bool:
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except:
        return False


# /filter əmri – Filter əlavə etmək
@app.on_message(filters.command("filter") & filters.group)
async def add_filter(_, message: Message):
    if not message.from_user or not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")

    chat_id = message.chat.id

    # reply ilə filter əlavə etmək
    if message.reply_to_message:
        keyword = message.reply_to_message.text or message.reply_to_message.caption
        if not keyword:
            return await message.reply("❌ Cavab verdiyiniz mesajda mətn yoxdur.")

        args = message.text.split(None, 1)
        if len(args) < 2:
            return await message.reply("İstifadə: `/filter [cavab]` ← reply ilə", quote=True)

        reply_text = args[1]
        keyword = keyword.lower()
    else:
        args = message.text.split(None, 2)
        if len(args) < 3:
            return await message.reply("İstifadə: `/filter söz cavab`", quote=True)

        keyword = args[1].lower()
        reply_text = args[2]

    # yaddaşa yaz
    if chat_id not in filters_dict:
        filters_dict[chat_id] = {}
    filters_dict[chat_id][keyword] = reply_text

    await message.reply(f"✅ Filter əlavə olundu: `{keyword}` → `{reply_text}`")


# /filters əmri – aktiv filterləri göstər
@app.on_message(filters.command("filters") & filters.group)
async def list_filters(_, message: Message):
    chat_id = message.chat.id
    if chat_id not in filters_dict or not filters_dict[chat_id]:
        return await message.reply("❌ Bu qrupda heç bir filter yoxdur.")
    
    text = "**📌 Aktiv filterlər:**\n"
    for keyword in filters_dict[chat_id]:
        text += f"• `{keyword}`\n"
    await message.reply(text)


# /stop əmri – filter silmək
@app.on_message(filters.command("stop") & filters.group)
async def remove_filter(_, message: Message):
    if not message.from_user or not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")

    args = message.text.split(None, 1)
    if len(args) < 2:
        return await message.reply("İstifadə: `/stop söz`", quote=True)

    keyword = args[1].lower()
    chat_id = message.chat.id

    if chat_id in filters_dict and keyword in filters_dict[chat_id]:
        del filters_dict[chat_id][keyword]
        return await message.reply(f"✅ Filter silindi: `{keyword}`")
    else:
        return await message.reply("❌ Bu sözə uyğun filter tapılmadı.")


# /stopall əmri – bütün filterləri sil
@app.on_message(filters.command("stopall") & filters.group)
async def remove_all_filters(_, message: Message):
    if not message.from_user or not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")

    chat_id = message.chat.id
    filters_dict[chat_id] = {}
    await message.reply("✅ Bütün filterlər silindi.")


# Auto-filter – mesajlarda avtomatik cavab
@app.on_message(filters.text & filters.group)
async def auto_reply(_, message: Message):
    chat_id = message.chat.id
    if chat_id not in filters_dict:
        return

    msg_text = message.text.lower()

    for keyword, reply_text in filters_dict[chat_id].items():
        if keyword in msg_text:
            return await message.reply(reply_text)
