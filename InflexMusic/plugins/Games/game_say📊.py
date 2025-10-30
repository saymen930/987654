from InflexMusic.core.bot import xaos as client  
from telethon import events
import os
from telethon import TelegramClient, events
import json
import config
from Jason import word  # WORDS siyahısı bu faylda saxlanılır

AZBUL = "Jason/custom_words.json"


@client.on(events.NewMessage(pattern=r"^[/!.]say(\s|$)(.*)"))
async def sual_saylari_handler(event):
    if event.sender_id not in config.OWNER_IDS:
        return  # Yalnız OWNER siyahısındakı istifadəçilər istifadə edə bilər

    cavab = ""

    # AZBUL faylı varsa, oradakı əsas sözlərin sayını göstər
    if os.path.exists(AZBUL):
        with open(AZBUL, "r", encoding="utf-8") as f:
            custom_words = json.load(f)
        cavab += f"🇦🇿 𝙰𝚉𝙱𝚄𝙻 **Sözlərin sayı:** {len(custom_words)}\n"
    else:
        cavab += "Hər hansısa fayl tapılmadı.\n"

    # WORDS siyahısındakı sözlərin sayı
    cavab += f"📚 𝚆𝙾𝚁𝙳 𝙶𝙰𝙼𝙴 **Sözlərinin sayı:** {len(word)}"

    await event.reply(cavab)
