import asyncio
from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantAdmin, ChannelParticipantCreator
from InflexMusic.core.bot import xaos as client 

warns = {}  # {(chat_id_user_id): int}

# ✅ Adminlik yoxlama funksiyası (Tam işlək)
async def is_admin(chat_id, user_id):
    try:
        participant = await client(GetParticipantRequest(channel=chat_id, user_id=user_id))
        p = participant.participant
        return isinstance(p, (ChannelParticipantAdmin, ChannelParticipantCreator))
    except Exception as e:
        print(f"[Admin Yoxlaması Xətası] {e}")
        return False

# 🔍 İstifadəçi tapma (reply, username, id ilə)
async def get_user_from_message(event):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        if reply_msg.from_id:
            return reply_msg.from_id.user_id
        return None

    args = event.raw_text.split()
    if len(args) < 2:
        return None

    identifier = args[1]
    if identifier.isdigit():
        return int(identifier)

    if identifier.startswith('@'):
        username = identifier[1:]
    else:
        username = identifier

    async for user in client.iter_participants(event.chat_id, search=username):
        if user.username and user.username.lower() == username.lower():
            return user.id
    return None

# 🚫 /mute
@client.on(events.NewMessage(pattern='/mute'))
async def mute_handler(event):
    if not await is_admin(event.chat_id, event.sender_id):
        await event.reply("Bu əmri yalnız adminlər istifadə edə bilər⛔")
        return

    user_id = await get_user_from_message(event)
    if not user_id:
        await event.reply("İstifadəçi tapılmadı. Reply edin və ya /mute @username / user_id ilə istifadə edin.")
        return

    try:
        await client(EditBannedRequest(
            channel=event.chat_id,
            participant=user_id,
            banned_rights=ChatBannedRights(
                until_date=None,
                send_messages=True,
                send_media=True,
                send_stickers=True,
                send_gifs=True,
                send_games=True,
                send_inline=True,
                embed_links=True
            )
        ))
        await event.reply("İstifadəçi səssiz edildi✅")
    except Exception as e:
        await event.reply(f"Xəta: {e}")

# 🔊 /unmute
@client.on(events.NewMessage(pattern='/unmute'))
async def unmute_handler(event):
    if not await is_admin(event.chat_id, event.sender_id):
        await event.reply("Bu əmri yalnız adminlər istifadə edə bilər⛔")
        return

    user_id = await get_user_from_message(event)
    if not user_id:
        await event.reply("İstifadəçi tapılmadı. Reply edin və ya /unmute @username / user_id ilə istifadə edin.")
        return

    try:
        await client(EditBannedRequest(
            channel=event.chat_id,
            participant=user_id,
            banned_rights=ChatBannedRights()
        ))
        await event.reply("İstifadəçinin səssizliyi açıldı✅")
    except Exception as e:
        await event.reply(f"Xəta: {e}")

# 🦶 /kick
@client.on(events.NewMessage(pattern='/kick'))
async def kick_handler(event):
    if not await is_admin(event.chat_id, event.sender_id):
        await event.reply("Bu əmri yalnız adminlər istifadə edə bilər⛔")
        return

    user_id = await get_user_from_message(event)
    if not user_id:
        await event.reply("İstifadəçi tapılmadı. Reply edin və ya /kick @username / user_id ilə istifadə edin.")
        return

    try:
        await client.kick_participant(event.chat_id, user_id)
        await client.unban_participant(event.chat_id, user_id)
        await event.reply("İstifadəçi qrupdan atıldı.")
    except Exception as e:
        await event.reply(f"Xəta: {e}")

# 🙋 /kickme
@client.on(events.NewMessage(pattern='/kickme'))
async def kickme_handler(event):
    try:
        await event.reply("Hə haqlısan! Davay bayıra 👞")
        await client.kick_participant(event.chat_id, event.sender_id)
        await client.unban_participant(event.chat_id, event.sender_id)
    except Exception as e:
        await event.reply(f"Xəta: {e}")

# ⚠️ /warn
@client.on(events.NewMessage(pattern='/warn'))
async def warn_handler(event):
    if not await is_admin(event.chat_id, event.sender_id):
        await event.reply("Bu əmri yalnız adminlər istifadə edə bilər⛔")
        return

    user_id = await get_user_from_message(event)
    if not user_id:
        await event.reply("İstifadəçi tapılmadı. Reply edin və ya /warn @username / user_id ilə istifadə edin.")
        return

    key = f"{event.chat_id}_{user_id}"
    warns[key] = warns.get(key, 0) + 1
    count = warns[key]

    markup = [Button.inline("❌ Xəbərdarlığı sil", data=f"unwarn_{event.chat_id}_{user_id}")]

    if count >= 3:
        try:
            await client.kick_participant(event.chat_id, user_id)
            warns[key] = 0
            await event.reply(f"İstifadəçi 3 dəfə xəbərdarlıq aldı və qrupdan atıldı❗", buttons=markup)
        except Exception as e:
            await event.reply(f"Xəta: {e}")
    else:
        await event.reply(f"İstifadəçi xəbərdarlıq aldı❗ Ümumi xəbərdarlıq sayı: {count}/3", buttons=markup)

# ✅ /unwarn
@client.on(events.NewMessage(pattern='/unwarn'))
async def unwarn_handler(event):
    if not await is_admin(event.chat_id, event.sender_id):
        await event.reply("Bu əmri yalnız adminlər istifadə edə bilər⛔")
        return

    user_id = await get_user_from_message(event)
    if not user_id:
        await event.reply("İstifadəçi tapılmadı. Reply edin və ya /unwarn @username / user_id ilə istifadə edin.")
        return

    key = f"{event.chat_id}_{user_id}"
    if warns.get(key, 0) > 0:
        warns[key] -= 1
        await event.reply(f"Xəbərdarlıq silindi, Cari xəbərdarlıq sayı: {warns[key]}/3")
    else:
        await event.reply("Bu istifadəçinin xəbərdarlığı yoxdur✅")

# 🔘 Inline button ilə /unwarn
@client.on(events.CallbackQuery(pattern=b'unwarn_.*'))
async def callback_unwarn_handler(event):
    data = event.data.decode('utf-8').split('_')
    if len(data) != 3:
        await event.answer("Xəta")
        return

    chat_id = int(data[1])
    user_id = int(data[2])
    caller_id = event.sender_id

    if not await is_admin(chat_id, caller_id):
        await event.answer("Yalnız adminlər istifadə edə bilər⛔")
        return

    key = f"{chat_id}_{user_id}"
    if warns.get(key, 0) > 0:
        warns[key] -= 1
        await event.answer("Xəbərdarlıq silindi✅")
        try:
            await event.edit(f"Xəbərdarlıq silindi, İstifadəçinin cari xəbərdarlıq sayı: {warns[key]}/3")
        except Exception as e:
            await event.answer(f"Mesaj redaktə olunmadı: {e}")
    else:
        await event.answer("Bu istifadəçinin xəbərdarlığı yoxdur✅")
