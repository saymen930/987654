from telethon import events, Button, types
from InflexMusic import xaos as Zaid
from InflexMusic.status import *
from InflexMusic.core.bot import xaos as Zaid
 

@Zaid.on(events.NewMessage(pattern="^[!/.]lock ?(.*)"))
@is_admin
async def lock(event, perm):
    if Config.MANAGEMENT_MODE == "ENABLE":
        return
    if not perm.change_info:
      await event.reply("Bu Əmri İsdifadə Edmək Üçun Lazım Olan Adminlik Haqqın Yoxdur!")
      return
    input_str = event.pattern_match.group(1)
    if not input_str:
       await event.reply("Kilidləmək Üçün Növü Müəyyən Etmədiniz..")
       return
    elif "all" in input_str:
       await Zaid.edit_permissions(event.chat_id,
          send_messages=False, 
          send_media=False,
          send_stickers=False,
          send_gifs=False,
          send_games=False,
          send_inline=False,
          send_polls=False,
          embed_link_previews=False)
       await event.reply(f"🔐 Chat Bağlandı.")

@Zaid.on(events.NewMessage(pattern="^[!./]unlock ?(.*)"))
@is_admin
async def unlock(event, perm):
    if Config.MANAGEMENT_MODE == "ENABLE":
        return
    if not perm.change_info:
      await event.reply("Bu Əmri İsdifadə Edmək Üçun Lazım Olan Adminlik Haqqın Yoxdur!")
      return
    input_str = event.pattern_match.group(1)
    if not input_str:
       await event.reply("Kilidi Açmaq Üçün Növü Müəyyən Etmədiniz.‌‌.")
       return
    elif "all" in input_str:
       await Zaid.edit_permissions(event.chat_id,
          send_messages=True, 
          send_media=True,
          send_stickers=True,
          send_gifs=True,
          send_games=True,
          send_inline=True,
          send_polls=True,
          embed_link_previews=True)
       await event.reply("🔓 Chat Açıldı.")




LOCK_TEXT = """
**Lock:**
 
‣ all
"""
 
@Zaid.on(events.NewMessage(pattern="^[!?/]locktypes"))
async def locktypes(event):
    await event.reply(LOCK_TEXT)
 
 
