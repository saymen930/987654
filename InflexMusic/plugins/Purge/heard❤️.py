import asyncio
from telethon import events
from Jason.heard import FRAMES
from InflexMusic.core.bot import xaos as client 

@client.on(events.NewMessage(pattern=r'^/ure(?:\s+(.*))?$'))
async def hearts_anim(event):
    text = event.pattern_match.group(1)

    if not text or text.strip() == "":
        await event.reply("⚠️ Zəhmət olmasa `/ure` yazdıqdan sonra bir mətin yazın.")
        return

    # İlk mesaj
    msg = await event.reply(FRAMES[0].format(text=text))

    # Animasiya ilə dəyiş
    for frame in FRAMES[1:]:
        await asyncio.sleep(0.5)
        await msg.edit(frame.format(text=text))

    # Sonda silmək istəyirsənsə
    await msg.delete()
