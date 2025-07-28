import asyncio, random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

import config
from InflexMusic.core.bot import xaos as client

# Bir nəfər yerinə bir neçə ID:

def is_owner(user_id: int) -> bool:
    return user_id in config.OWNER_IDS

@client.on(events.NewMessage(pattern=r"^[/!.]pins(\s|$)(.*)"))
async def pin(event):
    if not is_owner(event.sender_id):
        return await event.reply(f"Sən {config.BOT_NAME} bota sahib deyilsən!\n⛔ Pinləməyə çalışma.")

    if not event.reply_to_msg_id:
        return await event.reply("🗨 Zəhmət olmasa bir mesaja yanıt verin.")

    await event.client.pin_message(event.chat_id, event.reply_to_msg_id, notify=True)
    await event.reply("📌 Mesaj pinləndi!")

@client.on(events.NewMessage(pattern=r"^[/!.]unpins(\s|$)(.*)"))
async def unpin(event):
    if not is_owner(event.sender_id):
        return await event.reply(f"Sən {config.BOT_NAME} bota sahib deyilsən!\n⛔ Unpinləməyə çalışmayın.")

    if not event.reply_to_msg_id:
        return await event.reply("🗨 Zəhmət olmasa pinlənmiş mesaja yanıt verin.")

    await event.client.unpin_message(event.chat_id)
    await event.reply("📍 Pin qaldırıldı.")
