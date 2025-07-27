import asyncio
import random
from telethon import events
from telethon.tl.types import User
import config  # Məsələn: OWNER_IDS = [123456789, 987654321]
  # Öz client obyektinizi import edin
from InflexMusic import xaos as client


@client.on(events.NewMessage(pattern=r'^[!/\.]mal$'))
async def mal_varligi_olcme(event: events.NewMessage.Event):
    if not event.is_reply:
        return await event.reply("💁 Bu komutu istifadə etmək üçün bir mesaja yanıt verməlisiniz.")

    replied = await event.get_reply_message()
    if not replied or not isinstance(replied.sender, User):
        return await event.reply("🙅 İstifadəçini tapa bilmədim.")

    target = replied.sender
    me = await client.get_me()

    def mention(u: User) -> str:
        ad = (u.first_name or "İstifadəçi").replace("[", "\").replace("]", "\")
        return f"[{ad}](tg://user?id={u.id})"

    # 2 OWNER_ID üçün yoxlama
    if target.id in config.OWNER_IDS:
        return await event.reply(f"🙂‍↕️ {mention(target)} mənim sahibimdir, mal sənsən!")

    if target.id == me.id:
        return await event.reply("🕺 Məni də mal deyə çağıra bilməzsən!")

    initial = await event.reply(f"{mention(target)}-ın mallığı ölçülür... 📊")
    await asyncio.sleep(1)
    
    percentage = random.randint(0, 100)
    await initial.edit(f"{mention(target)} sən\n{percentage}% malsan 😅")
