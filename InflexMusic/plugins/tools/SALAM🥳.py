import telethon, asyncio
from telethon import TelegramClient, events
from InflexMusic.core.bot import xaos as client 
 
@client.on(events.NewMessage(pattern='salam'))
@client.on(events.NewMessage(pattern='Salam'))
async def bilgi(event):
    
    a = await event.reply("👋 Salam Aleykuma..")
    await asyncio.sleep(2)
    await a.edit("🌹 Xoş Gəldin")
    await asyncio.sleep(2)
    await a.edit("🤔 Necəsən?")
    await asyncio.sleep(2)
    await a.edit("❤️ Ümid Varam Yaxşısan...")
    await asyncio.sleep(5)
    await a.delete()
