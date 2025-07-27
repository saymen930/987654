import asyncio
import json
import os
from telethon import TelegramClient, events, types

FILTERS_FILE = "Jason/filters.json"

def load_filters():
    if os.path.exists(FILTERS_FILE):
        with open(FILTERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_filters(filters):
    with open(FILTERS_FILE, "w", encoding="utf-8") as f:
        json.dump(filters, f, indent=2, ensure_ascii=False)

filters_data = load_filters()

async def is_admin(event):
    try:
        chat = await event.get_chat()
        user = await event.get_sender()
        admins = await event.client.get_participants(chat, filter=types.ChannelParticipantsAdmins)
        return user.id in [admin.id for admin in admins]
    except Exception:
        return False

@bot.on(events.NewMessage(pattern=r'^/filter', func=lambda e: e.is_group))
async def add_filter(event):
    if not await is_admin(event):
        # Admin olmayan istifadəçi mesajı silmir, sadəcə xəbərdarlıq edir
        return await event.reply("⚠️ Bu əmri yalnız adminlər istifadə edə bilər!", reply_to=event.message.id)

    text = event.raw_text.split(None, 2)
    if len(text) < 2:
        await event.delete()
        return await event.reply("❗ Format: `/filter söz [cavab]`", reply_to=event.message.id)

    word = text[1].lower()
    chat_id = str(event.chat_id)
    if chat_id not in filters_data:
        filters_data[chat_id] = {}

    if event.is_reply:
        reply_msg = await event.get_reply_message()
        if reply_msg and reply_msg.media:
            media_info = {
                "type": "media",
                "chat_id": reply_msg.chat_id,
                "message_id": reply_msg.id
            }
            filters_data[chat_id][word] = media_info
            save_filters(filters_data)
            await event.delete()
            return await event.reply(f"✅ `{word}` üçün media filter əlavə olundu!", reply_to=event.message.id)

    if len(text) >= 3:
        reply_text = text[2]
        filters_data[chat_id][word] = {"type":"text", "data":reply_text}
        save_filters(filters_data)
        await event.delete()
        return await event.reply(f"✅ `{word}` üçün mətn filter əlavə olundu!", reply_to=event.message.id)

    await event.delete()
    await event.reply("❗ Ya media ilə reply et, ya da `/filter söz cavab` formatında yaz.", reply_to=event.message.id)

@bot.on(events.NewMessage(pattern=r'^/(stop|!stop)', func=lambda e: e.is_group))
async def remove_filter(event):
    if not await is_admin(event):
        # Admin olmayan istifadəçi mesajı silmir, sadəcə xəbərdarlıq edir
        return await event.reply("⚠️ Bu əmri yalnız adminlər istifadə edə bilər!", reply_to=event.message.id)

    text = event.raw_text.split(None, 1)
    if len(text) < 2 or not text[1].strip():
        await event.delete()
        return await event.reply("❗ Format: `/stop söz`", reply_to=event.message.id)

    word = text[1].strip().lower()
    chat_id = str(event.chat_id)

    if chat_id in filters_data and word in filters_data[chat_id]:
        del filters_data[chat_id][word]
        save_filters(filters_data)
        await event.delete()
        return await event.reply(f"❌ `{word}` filteri silindi.", reply_to=event.message.id)
    else:
        await event.delete()
        return await event.reply("🚫 Belə bir filter tapılmadı.", reply_to=event.message.id)

@bot.on(events.NewMessage(pattern=r'^/filters$', func=lambda e: e.is_group))
async def list_filters(event):
    if not await is_admin(event):
        # Admin olmayan istifadəçi mesajı silmir, sadəcə xəbərdarlıq edir
        return await event.reply("⚠️ Bu əmri yalnız adminlər istifadə edə bilər!", reply_to=event.message.id)

    chat_id = str(event.chat_id)
    if chat_id not in filters_data or not filters_data[chat_id]:
        await event.delete()
        return await event.reply("ℹ️ Bu qrupda heç bir filter yoxdur.", reply_to=event.message.id)
    
    filters_list = '\n'.join(f"• `{key}`" for key in filters_data[chat_id].keys())
    await event.delete()
    await event.reply(f"📃 Filter siyahısı:\n{filters_list}", reply_to=event.message.id)

@bot.on(events.NewMessage(func=lambda e: e.is_group))
async def auto_reply(event):
    if not event.message:
        return

    if event.out:
        return  # Botun öz mesajına cavab vermə

    text = event.message.message
    if not text:
        return

    text_lower = text.lower()
    command_prefixes = ['/filter', '/filters', '/stop', '!stop']
    first_word = text_lower.strip().split()[0] if text_lower.strip().split() else ""
    if first_word in command_prefixes:
        return

    chat_id = str(event.chat_id)
    if chat_id not in filters_data:
        return

    for word, data in filters_data[chat_id].items():
        if word in text_lower:
            if isinstance(data, dict) and data.get("type") == "media":
                try:
                    msg = await bot.get_messages(entity=data["chat_id"], ids=data["message_id"])
                    if msg and msg.media:
                        await event.reply(file=msg.media)
                    else:
                        await event.reply("⚠️ Media faylını göndərmək mümkün olmadı.")
                except Exception as e:
                    await event.reply(f"⚠️ Xəta baş verdi: {e}")
            elif isinstance(data, dict) and data.get("type") == "text":
                await event.reply(data["data"])
            else:
                await event.reply(str(data))
            break
