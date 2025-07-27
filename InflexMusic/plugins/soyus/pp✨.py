from telethon import TelegramClient, events
import random
import asyncio
from InflexMusic.core.bot import xaos as client
import config
from Jason.pp import photolist, E_M, A_A, C_S, B_A, D_S

# ==== BÜTÜN ŞƏKİL LİNKLƏRİ ====


# ==== PP ƏMRİ ====
# ==== PP ƏMRİ ====
@client.on(events.NewMessage(pattern="/pp"))
async def pp_handler(event):
    photo = random.choice(photolist)
    caption = E_M + f"\t{config.BOT_NAME}" + C_S
    buttons = [
        [Button.inline(D_S, data="change_pp"),
         Button.inline(B_A, data="close_pp")]
    ]
    # Foto göndəririk
    msg = await client.send_file(event.chat_id, photo, caption=caption, buttons=buttons)
    await event.delete()


# ==== CALLBACK HANDLER ====
@client.on(events.CallbackQuery(pattern=b"change_pp"))
async def change_pp_handler(event):
    await event.answer()

    # İlk olaraq animasiya yazısını göstəririk
    await event.edit(A_A)
    await asyncio.sleep(1)

    # Yeni şəkil və caption
    new_photo = random.choice(photolist)
    new_caption = E_M + f"\t{config.BOT_NAME}" + C_S
    new_buttons = [
        [Button.inline(D_S, data="change_pp"),
         Button.inline(B_A, data="close_pp")]
    ]

    # Media + caption + düymələri yeniləyirik
    await event.edit(file=new_photo, text=new_caption, buttons=new_buttons)
@client.on(events.CallbackQuery(pattern=b"close_pp"))
async def close_pp_handler(event):
    await event.answer()
    try:
        await event.delete()
    except:
        pass


