import logging, asyncio, random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins
from AylinRobot.config import Config
from telethon import events, errors
from InflexMusic.core.bot import xaos as client 
import time
from telethon.tl.functions.channels import GetParticipantsRequest


import asyncio
import random
from telethon import events
 
faiz = ['10%','11%','12%','13%','14%','15%','16%','17%','18%','19%','20%','21%','22%','23%','24%','25%','26%','27%','28%','29%','30%','31%','32%','33%','34%','35%','36%','37%','38%','39%','40%','41%','42%','43%','44%','45%','46%','47%','48%','49%','50%','51%','52%','53%','54%','55%','56%','57%','58%','59%','60%','61%','62%','63%','64%','65%','66%','67%','68%','69%','70%','71%','72%','73%','74%','75%','76%','77%','78%','79%','80%','81%','82%','83%','84%','85%','86%','87%','88%','89%','90%','91%','92%','93%','94%','95%','96%','97%','98%','99%','100%']
urek = ['❤️','🧡','💛','💚','💙','💜','🖤','🤍','🤎','❤️‍🔥','❤️‍🩹','❣️','💕','💞','💓','💗','💖','💘','💝']
 
 
@client.on(events.NewMessage(pattern="^[.!/@]eros ?(.*)|^[.!/@]ship ?(.*)"))
async def eros(event):
     if event.is_private:
          return await event.respond("**ℹ️ Bu əmr qruplar üçün nəzərdə tutulub**")
     qrup = await event.get_chat() 
     istifadeciler = await client.get_participants(qrup)
     sev1, sev2 = random.sample(istifadeciler, 2)
     secirem = await event.reply(f"{random.choice(urek)} **Cütlük seçilir...**")
     await asyncio.sleep(2)
     await secirem.delete()
     await event.reply(f"{random.choice(urek)} **Cütlüklər:**\n"
                       f"[{sev1.first_name}](tg://user?id={sev1.id})" + f" 🔐 [{sev2.first_name}](tg://user?id={sev2.id})\n"
                       f"**Eşq Faizi:** {random.choice(faiz)}")
 
