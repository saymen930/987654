import asyncio
import random
from telethon import events, Button
from telethon.tl.types import ChannelParticipantsAdmins, User

from InflexMusic.core.bot import xaos as client
import config
from Jason.tag import emoji, soz

# Qlobal dəyişənlər
running_tags = set()         # Hal-hazırda çalışan tag prosesləri
rxyzdev_tagTot = {}          # Hər qrup üçün tag sayını saxlayır
anlik_calisan = set()        # Aktiv çalışan proseslərin chat_id-ləri


# Qruplara əlavə düyməsi
def btn_add_to_group():
    return [[Button.url('➕ QRUPA ƏLAVƏ ET ➕', f'https://t.me/{config.BOT_USERNAME}?startgroup=a')]]


# Admin yoxlaması
async def is_admin(event):
    admins = [a.id async for a in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]
    return event.sender_id in admins


# --- /tag KOMANDASI (5-li) ---
@client.on(events.NewMessage(pattern=r"^[./!]tag(?:\s+(.+))?$"))
async def tag_handler(event: events.NewMessage.Event):
    if event.is_private:
        return await event.respond("❌ PM-də tag olmaz.", buttons=btn_add_to_group(), link_preview=False)

    if not await is_admin(event):
        return await event.respond("⛔ **Siz admin deyilsiniz!**")

    if event.chat_id in running_tags:
        return await event.respond("⚠️ Tag prosesi artıq işləyir. Dayandırmaq üçün `/cancel`.")

    text_on_cmd = event.pattern_match.group(1)
    reply_msg = await event.get_reply_message() if event.is_reply else None

    if text_on_cmd and reply_msg:
        return await event.respond("📌 **Ya mətin yazın, ya da reply edin. İkisi birlikdə olmaz.**")

    if not text_on_cmd and not reply_msg:
        return await event.respond("❌ **Tag üçün səbəb yazın!**\nMəsələn: `/tag Salam`")

    running_tags.add(event.chat_id)
    rxyzdev_tagTot[event.chat_id] = 0
    await event.respond("**✅ Tag prosesi başladı!**\nDayandırmaq üçün `/cancel`.")

    usrnum, usrtxt = 0, ""
    async for usr in client.iter_participants(event.chat_id, aggressive=False):
        if usr.bot or usr.deleted:
            continue

        if event.chat_id not in running_tags:
            break

        rxyzdev_tagTot[event.chat_id] += 1
        usrnum += 1
        usrtxt += f"\n• [{usr.first_name}](tg://user?id={usr.id})"

        if usrnum == 5:
            await client.send_message(event.chat_id, f"{text_on_cmd}\n{usrtxt}" if text_on_cmd else usrtxt,
                                      reply_to=reply_msg, link_preview=False)
            usrnum, usrtxt = 0, ""
            await asyncio.sleep(2)

    if usrtxt and event.chat_id in running_tags:
        await client.send_message(event.chat_id, f"{text_on_cmd}\n{usrtxt}" if text_on_cmd else usrtxt,
                                  reply_to=reply_msg, link_preview=False)

    if event.chat_id in running_tags:
        running_tags.remove(event.chat_id)
        starter = f"[{(await event.get_sender()).first_name}](tg://user?id={event.sender_id})"
        await event.respond(
            f"✅ **Tag prosesi tamamlandı!**\n📊 Tag edilənlər: `{rxyzdev_tagTot[event.chat_id]}`\n👤 Başladan: {starter}",
            buttons=btn_add_to_group(),
            link_preview=False
        )
        rxyzdev_tagTot.pop(event.chat_id, None)








# --- /ttag KOMANDASI (1-li) ---
@client.on(events.NewMessage(pattern=r"^[./!]ttag(?:\s+(.+))?$"))
async def ttag_handler(event: events.NewMessage.Event):
    if event.is_private:
        return await event.respond("❌ PM-də tag olmaz.", buttons=btn_add_to_group(), link_preview=False)

    if not await is_admin(event):
        return await event.respond("⛔ **Siz admin deyilsiniz!**")

    if event.chat_id in running_tags:
        return await event.respond("⚠️ Tag prosesi artıq işləyir. Dayandırmaq üçün `/cancel`.")

    text_on_cmd = event.pattern_match.group(1)
    reply_msg = await event.get_reply_message() if event.is_reply else None

    if text_on_cmd and reply_msg:
        return await event.respond("📌 **Ya mətin yazın, ya da reply edin. İkisi birlikdə olmaz.**")

    if not text_on_cmd and not reply_msg:
        return await event.respond("❌ **Tag üçün səbəb yazın!**\nMəsələn: `/ttag Salam`")

    running_tags.add(event.chat_id)
    rxyzdev_tagTot[event.chat_id] = 0
    await event.respond("**✅ Tag prosesi başladı!**")

    usrnum, usrtxt = 0, ""
    async for usr in client.iter_participants(event.chat_id, aggressive=False):
        if usr.bot or usr.deleted:
            continue

        if event.chat_id not in running_tags:
            break

        rxyzdev_tagTot[event.chat_id] += 1
        usrnum += 1
        usrtxt += f"[{usr.first_name}](tg://user?id={usr.id})"

        if usrnum == 1:
            await client.send_message(event.chat_id, f"{text_on_cmd} {usrtxt}" if text_on_cmd else usrtxt,
                                      reply_to=reply_msg, link_preview=False)
            usrnum, usrtxt = 0, ""
            await asyncio.sleep(2)

    if usrtxt and event.chat_id in running_tags:
        await client.send_message(event.chat_id, f"{text_on_cmd} {usrtxt}" if text_on_cmd else usrtxt,
                                  reply_to=reply_msg, link_preview=False)

    if event.chat_id in running_tags:
        running_tags.remove(event.chat_id)
        starter = f"[{(await event.get_sender()).first_name}](tg://user?id={event.sender_id})"
        await event.respond(
            f"✅ **Tag prosesi tamamlandı!**\n📊 Tag edilənlər: `{rxyzdev_tagTot[event.chat_id]}`\n👤 Başladan: {starter}",
            buttons=btn_add_to_group(),
            link_preview=False
        )
        rxyzdev_tagTot.pop(event.chat_id, None)


# --- /etag KOMANDASI (emoji ilə) ---
@client.on(events.NewMessage(pattern=r"^[./!]etag$"))
async def etag_handler(event):
    if event.is_private:
        return await event.respond("❌ PM-də tag olmaz.", buttons=btn_add_to_group(), link_preview=False)

    if not await is_admin(event):
        return await event.respond("⛔ **Siz admin deyilsiniz!**")

    chat_id = event.chat_id
    rxyzdev_tagTot[chat_id] = 0
    anlik_calisan.add(chat_id)
    await event.respond("**✅ Emoji tag prosesi başladı!**")

    usrnum, usrtxt = 0, ""
    async for usr in client.iter_participants(chat_id, aggressive=False):
        if usr.bot or usr.deleted:
            continue
        if chat_id not in anlik_calisan:
            break

        rxyzdev_tagTot[chat_id] += 1
        usrnum += 1
        usrtxt += f"[{random.choice(emoji)}](tg://user?id={usr.id}) "

        if usrnum == 5:
            await client.send_message(chat_id, usrtxt)
            usrnum, usrtxt = 0, ""
            await asyncio.sleep(2)

    if usrtxt:
        await client.send_message(chat_id, usrtxt)

    if chat_id in anlik_calisan:
        anlik_calisan.remove(chat_id)
        starter = f"[{(await event.get_sender()).first_name}](tg://user?id={event.sender_id})"
        await event.respond(
            f"✅ **Emoji tag tamamlandı!**\n📊 Tag edilənlər: `{rxyzdev_tagTot[chat_id]}`\n👤 Başladan: {starter}",
            buttons=btn_add_to_group()
        )
        rxyzdev_tagTot.pop(chat_id, None)



# --- /cancel KOMANDASI --


# --- /stag KOMANDASI (sözlə) ---
@client.on(events.NewMessage(pattern=r"^[./!]stag$"))
async def stag_handler(event):
    if event.is_private:
        return await event.respond("❌ PM-də tag olmaz.", buttons=btn_add_to_group(), link_preview=False)

    if not await is_admin(event):
        return await event.respond("⛔ **Siz admin deyilsiniz!**")

    chat_id = event.chat_id
    rxyzdev_tagTot[chat_id] = 0
    anlik_calisan.add(chat_id)
    await event.respond("**✅ Sözlə tag prosesi başladı!**")

    usrnum, usrtxt = 0, ""
    async for usr in client.iter_participants(chat_id, aggressive=False):
        if usr.bot or usr.deleted:
            continue
        if chat_id not in anlik_calisan:
            break

        rxyzdev_tagTot[chat_id] += 1
        usrnum += 1
        usrtxt += f"[{random.choice(soz)}](tg://user?id={usr.id}) "

        if usrnum == 1:
            await client.send_message(chat_id, usrtxt)
            usrnum, usrtxt = 0, ""
            await asyncio.sleep(2)

    if usrtxt:
        await client.send_message(chat_id, usrtxt)

    if chat_id in anlik_calisan:
        anlik_calisan.remove(chat_id)
        starter = f"[{(await event.get_sender()).first_name}](tg://user?id={event.sender_id})"
        await event.respond(
            f"✅ **Sözlə tag tamamlandı!**\n📊 Tag edilənlər: `{rxyzdev_tagTot[chat_id]}`\n👤 Başladan: {starter}",
            buttons=btn_add_to_group()
        )
        rxyzdev_tagTot.pop(chat_id, None)


# --- /cancel KOMANDASI ---
@client.on(events.NewMessage(pattern=r"^[./!]cancel$"))
async def cancel_handler(event):
    chat_id = event.chat_id
    if chat_id in running_tags:
        running_tags.remove(chat_id)
    if chat_id in anlik_calisan:
        anlik_calisan.remove(chat_id)
    count = rxyzdev_tagTot.get(chat_id, 0)
    await event.respond(
        f"🛑 **Tag prosesi dayandırıldı!**\n📊 Tag edilənlər: `{count}`",
        buttons=btn_add_to_group()
    )
