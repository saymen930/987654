from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from datetime import datetime, timedelta
import asyncio
import os
from InflexMusic.core.bot import xaos as bot
# ⚠️ Warn məlumatları
warns = {}  # {(chat_id, user_id): warn_count}

# ✅ Admin yoxlaması
async def is_admin(chat_id, user_id):
    try:
        participant = await bot(GetParticipantRequest(chat_id, user_id))
        return isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator))
    except:
        return False

# 🔍 İstifadəçini tap
def extract_user_id(event):
    if event.is_reply:
        reply = event.message.reply_to_msg_id
        # Get the sender of the replied message:
        if reply:
            return event.message.reply_to_msg.from_id.user_id if event.message.reply_to_msg.from_id else None
    parts = event.raw_text.split()
    if len(parts) >= 2:
        try:
            return int(parts[1])
        except:
            pass
    return None

# 🚫 /mute
@bot.on(events.NewMessage(pattern="/mute"))
async def mute_user(event):
    if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("⛔ Yalnız adminlər istifadə edə bilər")

    user = None
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        user = reply_msg.sender_id
    else:
        parts = event.raw_text.split()
        if len(parts) >= 2:
            try:
                user = int(parts[1])
            except:
                pass

    if not user:
        return await event.reply("Reply ilə və ya user_id ilə istifadə et.")

    until = datetime.utcnow() + timedelta(days=365)
    banned_rights = ChatBannedRights(
        until_date=until,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    try:
        await bot(EditBannedRequest(event.chat_id, user, banned_rights))
        await event.reply("✅ İstifadəçi səssiz edildi")
    except Exception as e:
        await event.reply(f"Xəta: {e}")

# 🔊 /unmute
@bot.on(events.NewMessage(pattern="/unmute"))
async def unmute_user(event):
    if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("⛔ Yalnız adminlər istifadə edə bilər")

    user = None
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        user = reply_msg.sender_id
    else:
        parts = event.raw_text.split()
        if len(parts) >= 2:
            try:
                user = int(parts[1])
            except:
                pass

    if not user:
        return await event.reply("Reply ilə və ya user_id ilə istifadə et.")

    unbanned_rights = ChatBannedRights(
        until_date=None,
        send_messages=False,
        send_media=False,
        send_stickers=False,
        send_gifs=False,
        send_games=False,
        send_inline=False,
        embed_links=False,
    )
    try:
        await bot(EditBannedRequest(event.chat_id, user, unbanned_rights))
        await event.reply("✅ Səssizlik ləğv edildi")
    except Exception as e:
        await event.reply(f"Xəta: {e}")

# 🦶 /kick
@bot.on(events.NewMessage(pattern="/kick"))
async def kick_user(event):
    if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("⛔ Yalnız adminlər istifadə edə bilər")

    user = None
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        user = reply_msg.sender_id
    else:
        parts = event.raw_text.split()
        if len(parts) >= 2:
            try:
                user = int(parts[1])
            except:
                pass

    if not user:
        return await event.reply("Reply ilə və ya user_id ilə istifadə et.")

    try:
        # Kick (ban)
        await bot.kick_participant(event.chat_id, user)
        await asyncio.sleep(1)
        # Unban (allow user to rejoin)
        unbanned_rights = ChatBannedRights(
            until_date=None,
            send_messages=False,
            send_media=False,
            send_stickers=False,
            send_gifs=False,
            send_games=False,
            send_inline=False,
            embed_links=False,
        )
        await bot(EditBannedRequest(event.chat_id, user, unbanned_rights))
        await event.reply("👞 İstifadəçi qovuldu")
    except Exception as e:
        await event.reply(f"Xəta: {e}")

# ⚠️ /warn
@bot.on(events.NewMessage(pattern="/warn"))
async def warn_user(event):
    if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("⛔ Yalnız adminlər istifadə edə bilər")

    user = None
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        user = reply_msg.sender_id
    else:
        parts = event.raw_text.split()
        if len(parts) >= 2:
            try:
                user = int(parts[1])
            except:
                pass

    if not user:
        return await event.reply("Reply ilə və ya user_id ilə istifadə et.")

    key = (event.chat_id, user)
    warns[key] = warns.get(key, 0) + 1
    count = warns[key]

    if count >= 3:
        try:
            await bot.kick_participant(event.chat_id, user)
            warns[key] = 0
            await event.respond(
                f"⚠️ 3 xəbərdarlıq aldı və qovuldu!",
                buttons=[Button.inline("❌ Warn sil", data=f"unwarn:{user}")]
            )
        except Exception as e:
            await event.reply(f"Xəta: {e}")
    else:
        await event.respond(
            f"❗ Xəbərdarlıq verildi ({count}/3)",
            buttons=[Button.inline("❌ Warn sil", data=f"unwarn:{user}")]
        )

# 🧹 /unwarn
@bot.on(events.NewMessage(pattern="/unwarn"))
async def unwarn_user(event):
    if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("⛔ Yalnız adminlər istifadə edə bilər")

    user = None
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        user = reply_msg.sender_id
    else:
        parts = event.raw_text.split()
        if len(parts) >= 2:
            try:
                user = int(parts[1])
            except:
                pass

    if not user:
        return await event.reply("Reply ilə və ya user_id ilə istifadə et.")

    key = (event.chat_id, user)
    if warns.get(key, 0) > 0:
        warns[key] -= 1
        await event.reply(f"✅ Warn silindi ({warns[key]}/3)")
    else:
        await event.reply("Bu istifadəçidə xəbərdarlıq yoxdur.")

# 🔘 Warn sil button
@bot.on(events.CallbackQuery(pattern="unwarn:(\d+)"))
async def handle_unwarn_button(event):
    user_id = int(event.pattern_match.group(1))
    chat_id = event.chat_id

    if not await is_admin(chat_id, event.sender_id):
        return await event.answer("⛔ Yalnız adminlər")

    key = (chat_id, user_id)
    if warns.get(key, 0) > 0:
        warns[key] -= 1
        await event.edit(f"✅ Warn silindi ({warns[key]}/3)")
        await event.answer("Warn silindi")
    else:
        await event.answer("Warn yoxdur")

# 🤪 /kickme
@bot.on(events.NewMessage(pattern="/kickme"))
async def kick_me(event):
    if await is_admin(event.chat_id, event.sender_id):
        return await event.reply("Axı səni atmaram balam, sən bir adminsən🫂")
    try:
        await bot.kick_participant(event.chat_id, event.sender_id)
        await asyncio.sleep(1)
        unbanned_rights = ChatBannedRights(
            until_date=None,
            send_messages=False,
            send_media=False,
            send_stickers=False,
            send_gifs=False,
            send_games=False,
            send_inline=False,
            embed_links=False,
        )
        await bot(EditBannedRequest(event.chat_id, event.sender_id, unbanned_rights))
        await event.reply("Haklısan bəli!! Bayıra davay 🫂")
    except Exception as e:
        await event.reply(f"Xəta: {e}")
