from telethon import events, Button, types
from InflexMusic.status import *
from InflexMusic.core.bot import xaos as client
import config
from Jason.lock import LOCK_TEXT





@client.on(events.NewMessage(pattern="^[!/.]lock ?(.*)"))
@is_admin
async def lock(event, perm):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    if not perm.change_info:
        await event.reply("Bu Əmri İsdifadə Edmək Üçün Lazım Olan Adminlik Haqqın Yoxdur!")
        return

    input_str = event.pattern_match.group(1).lower()
    if not input_str:
        await event.reply("Kilidləmək Üçün Növü Müəyyən Etmədiniz..\n/locktypes")
        return
    
    if "all" in input_str:
        await client.edit_permissions(
            event.chat_id,
            send_messages=False,
            send_media=False,
            send_stickers=False,
            send_gifs=False,
            send_games=False,
            send_inline=False,
            send_polls=False,
            
            embed_link_previews=False
            
        )
        await event.reply("🔐 Chat Bağlandı.")
    elif "gif" in input_str:
        await client.edit_permissions(event.chat_id, send_gifs=False)
        await event.reply("🔐 Gif göndərmək bağlandı.")
    elif "sticker" in input_str:
        await client.edit_permissions(event.chat_id, send_stickers=False)
        await event.reply("🔐 Sticker göndərmək bağlandı.")
        
    elif "media" in input_str:
        await client.edit_permissions(event.chat_id, send_media=False)
        await event.reply("🔐 Media göndərmək bağlandı.")
    
  


@client.on(events.NewMessage(pattern="^[!/.]unlock ?(.*)"))
@is_admin
async def unlock(event, perm):
    if config.MANAGEMENT_MODE == "ENABLE":
        return
    if not perm.change_info:
        await event.reply("Bu Əmri İsdifadə Edmək Üçün Lazım Olan Adminlik Haqqın Yoxdur!")
        return

    input_str = event.pattern_match.group(1).lower()
    if not input_str:
        await event.reply("Kilidi Açmaq Üçün Növü Müəyyən Etmədiniz.‌‌.\n/locktypes")
        return
    
    if "all" in input_str:
        await client.edit_permissions(
            event.chat_id,
            send_messages=True,
            send_media=True,
            send_stickers=True,
            send_gifs=True,
            send_games=True,
            send_inline=True,
            send_polls=True,
            
            embed_link_previews=True
        )
        await event.reply("🔓 Chat Açıldı.")
    elif "gif" in input_str:
        await client.edit_permissions(event.chat_id, send_gifs=True)
        await event.reply("🔓 Gif göndərmək açıldı.")
    elif "sticker" in input_str:
        await client.edit_permissions(event.chat_id, send_stickers=True)
        await event.reply("🔓 Sticker və emoji göndərmək açıldı.")
        
    elif "media" in input_str:
        await client.edit_permissions(event.chat_id, send_media=True)
        await event.reply("🔓 Media göndərmək açıldı.")







 
@client.on(events.NewMessage(pattern="^[!?/]locktypes"))
async def locktypes(event):
    await event.reply(LOCK_TEXT)
    



 
