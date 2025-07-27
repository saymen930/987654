import random
import asyncio
from telethon import events, Button   # <-- Button-u da import et!
from telethon.errors import MessageNotModifiedError
from InflexMusic.core.bot import xaos as client
import config
from Jason.pp import photolist, E_M, A_A, C_S, B_A, D_S  # bunlar səndə artıq var deyə götürürəm

# /pp
@client.on(events.NewMessage(pattern=r"^/pp$"))
async def pp_handler(event):
    photo = random.choice(photolist)
    caption = f"{E_M}\t{config.BOT_NAME} {C_S}"
    buttons = [
        [Button.inline(D_S, data=b"change_pp"),
         Button.inline(B_A, data=b"close_pp")]
    ]

    await client.send_file(
        event.chat_id,
        photo,
        caption=caption,
        buttons=buttons,
        reply_to=event.reply_to_msg_id or None
    )
    # əmr mesajını silmək istəyirsənsə:
    try:
        await event.delete()
    except:
        pass


# Dəyiş düyməsi
@client.on(events.CallbackQuery(pattern=b"change_pp"))
async def change_pp_handler(event):
    await event.answer()  # loading toast

    # 1) "animasiya" mətni göstər
    try:
        await event.edit(A_A)
    except MessageNotModifiedError:
        pass

    await asyncio.sleep(1)

    # 2) şəkli + mətni + düymələri dəyiş
    new_photo = random.choice(photolist)
    new_caption = f"{E_M}\t{config.BOT_NAME} {C_S}"
    new_buttons = [
        [Button.inline(D_S, data=b"change_pp"),
         Button.inline(B_A, data=b"close_pp")]
    ]

    # Telethon-un CallbackQuery-də edit media üçün event.edit istifadə olunur
    try:
        await event.edit(new_caption, file=new_photo, buttons=new_buttons)
    except Exception:
        # Bəzən edit media uğursuz ola bilər, onda yenisini göndər
        await client.send_file(event.chat_id, new_photo, caption=new_caption, buttons=new_buttons)
        try:
            await event.delete()
        except:
            pass


# Bağla düyməsi
@client.on(events.CallbackQuery(pattern=b"close_pp"))
async def close_pp_handler(event):
    await event.answer()
    try:
        await event.delete()  # şəkili və düymələri sil
    except:
        pass
