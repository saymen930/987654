import telethon, asyncio
import random
from random import choice
from telethon import TelegramClient, events
from InflexMusic.core.bot import xaos as client 
 
Y_D = ["Yalan Danışır 🎃", "Doğru danışır 👻", "Balamın canı onun başın buraq. O nə danışır heç özüdə bilmir 🤐 Yuxuludu o"]

@client.on(events.NewMessage(pattern='[/!.]yd'))
async def bilgi(event):
    
    a = await event.reply("Araşıdıraq görək yalandı ya doğru 🔬")
    await asyncio.sleep(2)
    await a.edit("Araşdırılır 🔬")
    await asyncio.sleep(0.1)
    await a.edit("////////25%///////")
    await asyncio.sleep(0.1)
    await a.edit("////////55%///////")
    await asyncio.sleep(0.1)
    await a.edit("////////82%///////")
    await asyncio.sleep(0.1)
    await a.edit("Ay səni Dəcəll 😂")
    await asyncio.sleep(1)
    await a.edit(f"{random.choice(Y_D)}")
    await asyncio.sleep(5)
    await a.delete()
