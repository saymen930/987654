import asyncio
from telethon import events, Button
from telethon.tl.types import ChannelParticipantsAdmins
import config
from InflexMusic.core.bot import xaos as client 
from Jason.tag import emoji, sevgi
# Hər qrup üçün aktiv tag prosesi saxlanır
running_tags = set()
tag_count = {}

def btn_add_to_group():
    return [[Button.url('➕ QRUPA ƏLAVƏ ET ➕', f'https://t.me/{config.BOT_USERNAME}?startgroup=a')]]

async def is_admin(event):
    admins = [a.id async for a in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]
    return event.sender_id in admins

@client.on(events.NewMessage(pattern=r"^[./!]tag(?:\s+(.+))?$"))
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
        return await event.respond("**❌ 5-li tag etmək üçün səbəb yoxdur.\n✅ Misal: `/tag Salam`**")

    # Start
    running_tags.add(event.chat_id)
    tag_count[event.chat_id] = 0
    await event.respond("**✅ Tag prosesi başladı!**\nDayandırmaq üçün: `/cancel`")

    chunk_size = 5
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











def btn_add_to_group():
    return [[Button.url('➕ QRUPA ƏLAVƏ ET ➕', f'https://t.me/{config.BOT_USERNAME}?startgroup=a')]]

async def is_admin(event):
    admins = [a.id async for a in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]
    return event.sender_id in admins

@client.on(events.NewMessage(pattern=r"^[./!]ttag(?:\s+(.+))?$"))
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
        return await event.respond("**❌ T2kli tağ etmək üçün səbəb yoxdur.\n✅ Misal: `/ttag Salam`**")

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












running_tags = set()
tag_count = {}

# ETAG KOMANDASI
@client.on(events.NewMessage(pattern=r"^[./!]etag$"))
async def etag_handler(event):
    chat_id = event.chat_id
    rxyzdev_tagTot[chat_id] = 0

    if event.is_private:
        return await event.respond(
            "❌ PM-də tağ olmaz.\n✅ Bu əmr yalnız qruplar və kanallar üçündür.",
            buttons=[[Button.url("➕ QRUPA ƏLAVƏ ET ➕", f"https://t.me/{config.BOT_USERNAME}?startgroup=a")]],
            link_preview=False
        )

    # Admin yoxlaması
    admins = [admin.id async for admin in client.iter_participants(chat_id, filter=ChannelParticipantsAdmins)]
    if event.sender_id not in admins:
        return await event.respond("⛔ **Siz admin deyilsiniz!**\n✅ **Bu əmri yalnız adminlər istifadə edə bilər.**")

    anlik_calisan.add(chat_id)
    usrnum = 0
    usrtxt = ""
    await event.respond("**✅ Tağ prosesi başladı!**")

    async for usr in client.iter_participants(chat_id, aggressive=False):
        if usr.bot or usr.deleted:
            continue  # Bot və silinmiş userləri keçirik

        rxyzdev_tagTot[chat_id] += 1
        usrnum += 1
        usrtxt += f"[{random.choice(emoji)}](tg://user?id={usr.id}) • "

        if chat_id not in anlik_calisan:
            return
        if usrnum == 5:  # 5 nəfərdən bir mesaj göndərilir
            await client.send_message(chat_id, usrtxt)
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ""

    # Qalan userlər üçün mesaj
    if usrnum > 0:
        await client.send_message(chat_id, usrtxt)

    sender = await event.get_sender()
    starter = f"[{sender.first_name}](tg://user?id={sender.id}) "
    await event.respond(f"**✅ Tağ prosesi uğurla tamamlandı!**\n\n📊 **Tağ edilənlərin sayı:** `{rxyzdev_tagTot[chat_id]}`\n👤 **Başladan:** {starter}")
    anlik_calisan.remove(chat_id)


# CANCEL KOMANDASI
@client.on(events.NewMessage(pattern=r"^[./!]cancel$"))
async def cancel_handler(event):
    chat_id = event.chat_id
    if chat_id in anlik_calisan:
        anlik_calisan.remove(chat_id)
        count = rxyzdev_tagTot.get(chat_id, 0)
        await event.respond(
            f"✅ **Tağ prosesi dayandırıldı.**\n\n📋 **Tağ edilənlərin sayı:** `{count}`",
            buttons=[[Button.url("➕ QRUPA ƏLAVƏ ET ➕", f"https://t.me/{config.BOT_USERNAME}?startgroup=a")]],
            link_preview=False
        )
    else:
        await event.respond("❌ Hal-hazırda heç bir tağ prosesi işləmir.")










running_tags = set()
tag_count = {}



# STAGKOMANDASI
@client.on(events.NewMessage(pattern=r"^[./!]stag$"))
async def etag_handler(event):
    chat_id = event.chat_id
    rxyzdev_tagTot[chat_id] = 0

    if event.is_private:
        return await event.respond(
            "❌ PM-də tağ olmaz.\n✅ Bu əmr yalnız qruplar və kanallar üçündür.",
            buttons=[[Button.url("➕ QRUPA ƏLAVƏ ET ➕", f"https://t.me/{config.BOT_USERNAME}?startgroup=a")]],
            link_preview=False
        )

    # Admin yoxlaması
    admins = [admin.id async for admin in client.iter_participants(chat_id, filter=ChannelParticipantsAdmins)]
    if event.sender_id not in admins:
        return await event.respond("⛔ **Siz admin deyilsiniz!**\n✅ **Bu əmri yalnız adminlər istifadə edə bilər.**")

    anlik_calisan.add(chat_id)
    usrnum = 0
    usrtxt = ""
    await event.respond("**✅ Tağ prosesi başladı!**")

    async for usr in client.iter_participants(chat_id, aggressive=False):
        if usr.bot or usr.deleted:
            continue  # Bot və silinmiş userləri keçirik

        rxyzdev_tagTot[chat_id] += 1
        usrnum += 1
        usrtxt += f"[{random.choice(sevgi)}](tg://user?id={usr.id}) • "

        if chat_id not in anlik_calisan:
            return
        if usrnum == 5:  # 5 nəfərdən bir mesaj göndərilir
            await client.send_message(chat_id, usrtxt)
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ""

    # Qalan userlər üçün mesaj
    if usrnum > 0:
        await client.send_message(chat_id, usrtxt)

    sender = await event.get_sender()
    starter = f"[{sender.first_name}](tg://user?id={sender.id}) "
    await event.respond(f"**✅ Tağ prosesi uğurla tamamlandı!**\n\n📊 **Tağ edilənlərin sayı:** `{rxyzdev_tagTot[chat_id]}`\n👤 **Başladan:** {starter}")
    anlik_calisan.remove(chat_id)


# CANCEL KOMANDASI
@client.on(events.NewMessage(pattern=r"^[./!]cancel$"))
async def cancel_handler(event):
    chat_id = event.chat_id
    if chat_id in anlik_calisan:
        anlik_calisan.remove(chat_id)
        count = rxyzdev_tagTot.get(chat_id, 0)
        await event.respond(
            f"✅ **Tağ prosesi dayandırıldı.**\n\n📋 **Tağ edilənlərin sayı:** `{count}`",
            buttons=[[Button.url("➕ QRUPA ƏLAVƏ ET ➕", f"https://t.me/{config.BOT_USERNAME}?startgroup=a")]],
            link_preview=False
        )
    else:
        await event.respond("❌ Hal-hazırda heç bir tağ prosesi işləmir.")












