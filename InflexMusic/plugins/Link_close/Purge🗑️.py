import asyncio
import time
from telethon import events, errors
from telethon.tl.types import ChannelParticipantsAdmins
from InflexMusic.core.bot import xaos as client  # Öz client importun

@client.on(events.NewMessage(pattern=r"^[!./]purge$"))
async def purge_messages(event):
    start = time.perf_counter()

    if event.is_private:
        await event.respond("💁 Bu əmri yalnız qruplarda icra edə bilərsiniz.", parse_mode='markdown')
        return

    if not await is_group_admin(event):
        await event.respond("💆 Bu əmri yalnız qrup yönəticiləri icra edə bilər.", parse_mode='markdown')
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.respond("🗑️ Silməyə başlayacağım mesaja yanıt ver.")
        return

    messages = []
    message_id = reply_msg.id
    delete_to = event.message.id
    deleted = 0

    messages.append(event.reply_to_msg_id)
    for msg_id in range(message_id, delete_to + 1):
        messages.append(msg_id)
        if len(messages) == 100:
            await event.client.delete_messages(event.chat_id, messages)
            deleted += len(messages)
            messages = []

    if messages:
        await event.client.delete_messages(event.chat_id, messages)
        deleted += len(messages)

    elapsed = time.perf_counter() - start
    result_msg = await event.respond(f"🗑️ {deleted} mesaj silindi.\n⏱ {elapsed:0.2f} saniyə.")

    # 10 saniyə sonra cavabı sil
    await asyncio.sleep(10)
    await result_msg.delete()

async def is_group_admin(event):
    """ İstifadəçi admin olub-olmadığını yoxlayır """
    try:
        user = await event.client.get_entity(event.input_chat)
        user_info = await event.client.get_participants(user, filter=ChannelParticipantsAdmins, limit=100)
        for u in user_info:
            if u.id == event.sender_id:
                return True
    except errors.rpcerrorlist.ChatAdminRequiredError:
        pass
    return False
