from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio
from InflexMusic.core.bot import xaos as client
goodbye_status = {}
recent_goodbye = set()

@client.on(events.ChatAction)
async def auto_activate_goodbye(event):
    if event.user_joined or event.user_added:
        if event.user_id == (await client.get_me()).id:
            chat = event.chat_id
            if chat not in goodbye_status:
                goodbye_status[chat] = True
                await client.send_message(chat, "Salam! Goodbye mesajı avtomatik olaraq aktiv edildi ✅")

@client.on(events.NewMessage(pattern=r'/goodbye(?:\s+(on|off))?'))
async def goodbye_toggle(event):
    chat = event.chat_id
    sender = await event.get_sender()
    sender_id = sender.id

    if event.is_private:
        await event.reply("Bu əmrlər yalnız qruplarda işləyir.")
        return

    admins = []
    async for admin in client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        admins.append(admin.id)
    if sender_id not in admins:
        await event.reply("Bu əmri yalnız adminlər istifadə edə bilər.")
        return

    arg = event.pattern_match.group(1)

    if arg == "on":
        goodbye_status[chat] = True
        await event.reply("Goodbye mesajı aktiv edildi ✅")
    elif arg == "off":
        goodbye_status[chat] = False
        await event.reply("Goodbye mesajı deaktiv edildi ❌")
    else:
        status = goodbye_status.get(chat, False)
        status_text = "aktivdir ✅" if status else "deaktivdir ❌"
        await event.reply(
            f"Goodbye mesajı {status_text}\n\n"
            "Goodbye mesajını aktiv və deaktiv etmək üçün 🔄\n"
            "/goodbye on\n"
            "/goodbye off  yazın ✅"
        )

@client.on(events.ChatAction)
async def goodbye_handler(event):
    chat = event.chat_id
    user_id = event.user_id

    if event.user_left or event.user_kicked:
        if goodbye_status.get(chat, False):
            if (chat, user_id) in recent_goodbye:
                return
            recent_goodbye.add((chat, user_id))
            user = await event.get_user()
            username = f"@{user.username}" if user.username else user.first_name
            text = f"{username} səni itirmək üzücüdür 😑 Uğurlar!! 💔"
            await client.send_message(chat, text)

            async def remove_after_delay():
                await asyncio.sleep(30)
                recent_goodbye.discard((chat, user_id))

            asyncio.create_task(remove_after_delay())
