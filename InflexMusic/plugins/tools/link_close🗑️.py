import random
import os
import logging
import asyncio
from telethon import Button
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins
from telethon import TelegramClient, events

import config


 
 
# LİNK_CLOSE


CLOSE = f"🗑️**Qrupa Göndərilən Linki Sildim**\n---------------------------------------------------------\n❌** Bu Qrupa Hər Hansısa Link Göndərməyə  İcazə Yoxdu**"

NUMBER = f"🗑️**Qrupa Göndərilən Mobil Nömrəni Sildim**\n---------------------------------------------------------\n❌** Bu Qrupa Hər Hansısa Link Və Ya Mobil Nömrə Göndərməyə  İcazə Yoxdu**"

isleyen = []
rxyzdev_tagTot = {}
 
@xaos.on(events.NewMessage(pattern="^[/.!]link_close ?(.*)"))
async def chatbot(event):
    global isleyen
    rxyzdev_tagTot[event.chat_id] = 0
    if event.is_private:
      return await event.respond("❌ /link_close **Əmri PM Də Qadağandır**\n**✅ Bu Əmr Sadəcə Qruplarda Və Kanallarda Keçərlidi!**", buttons=(
			                                 [
                                    Button.url('➕ QRUPA ƏLAVƏ ET ➕', f'https://t.me/{config.BOT_USERNAME}?startgroup=a')
                                    ],
                                  ),
                                  link_preview=False)
 
    admins = []
    async for admin in xaos.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
      admins.append(admin.id)
    if not event.sender_id in admins:
      return await event.reply("**⛔ Siz Admin Deyilsiz!**\n✅ **Bu Əmir Sadəcə Adminlər Üçün Keçərlidi**")
  

 
    emr = event.pattern_match.group(1)
    qrup = event.chat_id
    if emr == "ON" or emr == "on" or emr == "On":
        if qrup not in isleyen:
            isleyen.append(qrup)
            aktiv_olundu = f"✅ **Tamamdır Paşam.!**\n🗑️ Artıq Qrupa Atılan Hər Bir Linki Siləcəm\n⛔ __YouTube, Whatsapp, Telegram, İnstagram, Facebook, Google, Mobil-Nömrə, Və S__.\n"
            await event.reply(aktiv_olundu)
            return
        await event.reply("⚠️ **LİNK_CLOSE Hal-Hazırda Qrupda Aktivdir !**")
        return
    elif emr == "OFF" or emr == "off" or emr == "Off":
        if qrup in isleyen:
            isleyen.remove(qrup)
            await event.reply("⛔️ **Tamamdır Paşam**\n🗑️ Artiq Qrupa Göndərilən Linkləri Silməyəcəm !**")
            return # aykhan026 | aykhan_s
        await event.reply("⚠️ **LİNK_CLOSE Hal-Hazırda Qrupda Deaktivdir !**")
        return
    
    else:
        await event.reply("✅ **LİNK_CLOSE ni Aktivləşdirmək Üçün link_close on Yazın**\n❌ **Söndürmək Üçün link_close off yazın**")
 
 
 
        
        
@xaos.on(events.NewMessage)
async def chatbot(event):
    global isleyen
    mesaj = str(event.raw_text)
    qrup = event.chat_id
    if qrup not in isleyen:
        return
      
    if "https://instagram.com/" in mesaj or "https://www.instagram.com/" in mesaj: #instagram
        await event.delete()
        await event.reply(f"{CLOSE}")
    if "https://chat.whatsapp.com/" in mesaj or "https://whatsapp.com/" in mesaj:# Whatsapp
        await event.delete()
        await event.reply(f"{CLOSE}")
    if "https://www.youtube.com/" in mesaj:# YouTube
        await event.delete()
        await event.reply(f"{CLOSE}")
    if "https://t.me/" in mesaj: # Telegram
        await event.delete()
        await event.reply(f"{CLOSE}")
    if "https://www.google.com/" in mesaj or "https://google.com/" in mesaj: # Google
        await event.delete()
        await event.reply(f"{CLOSE}")
    if "https://vt.tiktok.com/" in mesaj or "https://www.tiktok.com/" in mesaj or "https://tiktok.com/" in mesaj: # TikTok
        await event.delete()
        await event.reply(f"{CLOSE}")
    if "https://www.facebook.com/" in mesaj or "https://facebook.com/" in mesaj: # Facebook
        await event.delete()
        await event.reply(f"{CLOSE}")
    if "+99450" in mesaj or "+99451" in mesaj or "+99455" in mesaj or "+99470" in mesaj or "+99477" in mesaj: # Mobil nömrə
        await event.delete()
        await event.reply(f"{NUMBER}")
    if "051" in mesaj or "050" in mesaj or "055" in mesaj or "070" in mesaj or "077" in mesaj or "010" in mesaj: # Mobil nömrə
        await event.delete()
        await event.reply(f"{NUMBER}")






