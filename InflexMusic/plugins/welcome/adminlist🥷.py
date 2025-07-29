import asyncio
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins
from InflexMusic.core.bot import xaos as bot

@bot.on(events.NewMessage(pattern=r'^/(adminlist|admin|admins)(?:\s+.+)?$', incoming=True))
async def admin_commands_handler(event):
    chat = await event.get_chat()
    chat_id = event.chat_id

    if not chat or not getattr(chat, 'title', None):
        await event.reply("Bu əmrlər yalnız qruplarda işləyir.")
        return

    admins = await bot.get_participants(chat_id, filter=ChannelParticipantsAdmins)
    human_admins = [admin for admin in admins if not admin.bot]

    if not human_admins:
        await event.reply("Qrupda admin yoxdur")
        return

    command = event.pattern_match.group(1).lower()

    if command in ["admin", "admins"]:
        # İstifadəçiyə cavab veririk
        await event.reply("Aydındır! Mən bu mesajı adminlərə xəbər verirəm 🔔")

        sender = await event.get_sender()
        sender_name = sender.first_name if sender else "İstifadəçi"
        sender_username = f"@{sender.username}" if sender and sender.username else sender_name

        # Mesaj məzmunu və link
        if event.is_reply:
            reply_msg = await event.get_reply_message()
            msg_text = reply_msg.text or "[Media və ya mətn yoxdur]"
            msg_date = reply_msg.date.strftime("%Y-%m-%d %H:%M:%S")
            msg_id = reply_msg.id
        else:
            msg_text = event.message.text or "[Boş mesaj]"
            msg_date = event.message.date.strftime("%Y-%m-%d %H:%M:%S")
            msg_id = event.message.id

        # Mesaj linki
        if getattr(chat, 'username', None):
            msg_link = f"https://t.me/{chat.username}/{msg_id}"
        else:
            # chat_id telethon-da mənfi olur, link üçün 4 rəqəm atılır
            msg_link = f"https://t.me/c/{str(chat_id)[4:]}/{msg_id}"

        warning_text = (
            f"{sender_username} {chat.title} Qrupunda sizə ehtiyac duyur❗\n\n"
            f"Mesaj: {msg_text}\n"
            f"Saat: {msg_date}\n"
            f"Link: {msg_link}\n"
            f"İstifadəçi: {sender_username}"
        )

        # Adminlərə şəxsi mesaj göndəririk, tag ilə
        for admin in human_admins:
            try:
                tag = f"@{admin.username}" if admin.username else admin.first_name or "Admin"
                await bot.send_message(admin.id, f"{tag}\n\n{warning_text}")
            except Exception:
                # Mesaj göndərilə bilməyə bilər, pass edirik
                pass

    elif command == "adminlist":
        text = f"<b>{chat.title} Qrupundakı Adminlər 🥷</b>\n\n"
        for i, admin in enumerate(human_admins, start=1):
            user = admin
            display_name = f"@{user.username}" if user.username else (user.first_name or "Ad yoxdur")
            custom_title = getattr(admin, 'custom_title', None)
            rank_name = custom_title if custom_title else (user.first_name or "Ad yoxdur")
            text += f"{i}. {display_name} <{rank_name}>\n"

        await event.reply(text, parse_mode='html')
