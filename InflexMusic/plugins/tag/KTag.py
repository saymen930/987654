import asyncio
from telethon import events, Button
from telethon.tl.types import ChannelParticipantsAdmins
import config
from InflexMusic.core.bot import xaos as client 
# Hər qrup üçün aktiv tag prosesi saxlanır
running_tags = set()
tag_count = {}

def btn_add_to_group():
    return [[Button.url('➕ QRUPA ƏLAVƏ ET ➕', f'https://t.me/{config.BOT_USERNAME}?startgroup=a')]]

async def is_admin(event):
    admins = [a.id async for a in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]
    return event.sender_id in admins

@client.on(events.NewMessage(pattern=r"^[./!]all(?:\s+(.+))?$"))
async def mention_all(event: events.NewMessage.Event):
    # PM-də blokla
    if event.is_private:
        return await event.respond(
            "**❌ PM-də tag olmaz**\n**✅ Bu əmr yalnız qruplarda/kanallarda keçərlidir!**",
            buttons=btn_add_to_group(),
            link_preview=False
        )

    # Admin yoxlaması
    if not await is_admin(event):
        return await event.respond("**⛔ Siz admin deyilsiniz!**\n✅ **Bu əmr yalnız adminlər üçün keçərlidir**")

    # Artıq çalışırsa
    if event.chat_id in running_tags:
        return await event.reply("⚠️ Bu qrupda tag prosesi artıq işləyir. Dayandırmaq üçün: `/cancel`")

    # Mesaj mənbəyini təyin et
    text_on_cmd = event.pattern_match.group(1)
    reply_msg = await event.get_reply_message() if event.is_reply else None

    if text_on_cmd and reply_msg:
        return await event.respond("**📌 Tag edə bilməyim üçün ya mətin yaz, ya da mesaja reply et. İkisi birlikdə olmaz.**")

    if not text_on_cmd and not reply_msg:
        return await event.respond("**❌ Tag etmək üçün səbəb yoxdur.\n✅ Misal: `/tag Salam`**")

    # Start
    running_tags.add(event.chat_id)
    tag_count[event.chat_id] = 0
    await event.respond("**✅ Tag prosesi başladı!**\nDayandırmaq üçün: `/cancel`")

    chunk_size = 1
    sleep_between = 2

    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id, aggressive=False):
        # Botları keç
        if usr.bot:
            continue

        if event.chat_id not in running_tags:
            break

        tag_count[event.chat_id] += 1
        usrnum += 1
        usrtxt += f"\n• - [{usr.first_name}](tg://user?id={usr.id})"

        if usrnum == chunk_size:
            if text_on_cmd:
                await client.send_message(event.chat_id, f"{text_on_cmd}\n{usrtxt}", link_preview=False)
            else:
                await client.send_message(event.chat_id, usrtxt, reply_to=reply_msg, link_preview=False)

            await asyncio.sleep(sleep_between)
            usrnum = 0
            usrtxt = ""

    # Sonuncu qalıbsa
    if event.chat_id in running_tags and usrtxt:
        if text_on_cmd:
            await client.send_message(event.chat_id, f"{text_on_cmd}\n{usrtxt}", link_preview=False)
        else:
            await client.send_message(event.chat_id, usrtxt, reply_to=reply_msg, link_preview=False)

    # Bitir
    if event.chat_id in running_tags:
        running_tags.remove(event.chat_id)
        sender = await event.get_sender()
        starter = f"[{sender.first_name}](tg://user?id={sender.id})"
        total = tag_count.get(event.chat_id, 0)
        await event.respond(
            f"**✅ Tag prosesi uğurla tamamlandı!**\n\n"
            f"📊 Tag edilənlərin sayı: `{total}`\n"
            f"👤 Prosesi başladan: {starter}",
            buttons=btn_add_to_group(),
            link_preview=False
        )
        tag_count.pop(event.chat_id, None)


@client.on(events.NewMessage(pattern=r"^[./!]cancel$"))
async def cancel_tag(event: events.NewMessage.Event):
    # PM-də işləməsin
    if event.is_private:
        return await event.respond("❌ Bu əmr yalnız qruplarda işləyir!")

    # Admin yoxlaması
    if not await is_admin(event):
        return

    if event.chat_id in running_tags:
        running_tags.remove(event.chat_id)
        await event.reply("🛑 Tag prosesi dayandırıldı.")
    else:
        await event.reply("ℹ️ Aktiv tag prosesi yoxdur.")





