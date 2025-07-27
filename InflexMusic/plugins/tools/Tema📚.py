import random
import asyncio
from Jason.tema import taim
from telethon import events, Button
from InflexMusic.core.bot import xaos as client  # Öz client importunu istifadə et

# TEMA siyahısı ("PERSİONAL ED" → "Görmək üçün toxun")


# Inline düymələr
def tema_buttons():
    return [
        [Button.inline("🔄 DƏYİŞ", data="change")],
        [Button.inline("🔐 BAĞLA", data="close")]
    ]

# Tema komandasını işlədən handler
@client.on(events.NewMessage(pattern=r"^[!./@]?tema$"))
async def tema_handler(event):
    await event.reply(random.choice(taim), buttons=tema_buttons(), link_preview=False)

# Dəyiş butonuna basıldıqda "Dəyişilir..." animasiyası
@client.on(events.CallbackQuery(data=b"change"))
async def change_callback(event):
    try:
        await event.edit("🔄 Dəyişilir...", buttons=tema_buttons(), link_preview=False)
        await asyncio.sleep(1)  # 1 saniyə gözləyir
        await event.edit(random.choice(taim), buttons=tema_buttons(), link_preview=False)
    except Exception as e:
        print("Xəta:", e)

# Callback düymə üçün close funksiyası
@client.on(events.CallbackQuery(data=b"close"))
async def close_callback(event):
    await event.delete()
