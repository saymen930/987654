import asyncio, random
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins
from InflexMusic.core.bot import xaos as client 



async def is_admin(event):
    """İstifadəçi qrup adminidirmi?"""
    if event.is_private:  # Private mesajda icazə vermə
        return False
    try:
        perms = await event.client.get_permissions(event.chat_id, event.sender_id)
        return perms.is_admin
    except:
        return False


@client.on(events.NewMessage(pattern="^[/.!]pin ?(.*)"))
async def pin(event):
    if event.is_private:  # Private-da işləməsin
        return await event.reply("⛔ Bu əmr yalnız qruplarda istifadə edilə bilər!")

    if not await is_admin(event):
        return await event.reply(f"⛔ Bu əmri yalnız adminlər icra edə bilər!")

    if not event.reply_to_msg_id:
        return await event.reply("💁 Zəhmət olmasa pinləmək üçün bir mesaja yanıt verin.")

    await event.client.pin_message(event.chat_id, event.reply_to_msg_id, notify=True)
    await event.reply("📌 Mesaj uğurla pinləndi!")


@client.on(events.NewMessage(pattern="^[/!.]unpin ?(.*)"))
async def unpin(event):
    if event.is_private:  # Private-da işləməsin
        return await event.reply("⛔ Bu əmr yalnız qruplarda istifadə edilə bilər!")

    if not await is_admin(event):
        return await event.reply(f"⛔ Bu əmri yalnız adminlər icra edə bilər!")

    await event.client.unpin_message(event.chat_id)
    await event.reply("📍 Pinlənmiş mesaj qaldırıldı.")
