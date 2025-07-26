import os
from pyrogram import Client, filters
from InflexMusic import app
 
 
DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/")
 

DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/rizad/")
 
 

 
@app.on_message(filters.video & filters.private)
async def mp3(bot, message):
    
    # download video
    file_path = DOWNLOAD_LOCATION + f"xaos.mp3"
    txt = await message.reply_text("`📡 Əsas Serverə Yüklənir...`")
    await message.download(file_path)
    await txt.edit_text("`Uğurla Yükləndi ✅`")
    
    # convert to audio
    await txt.edit_text("**♻️ AUDİİYO Gətrilir**\n**💿 Gözləyin**")
    await message.reply_audio(audio=file_path, caption="**❤️ Uğurla Yükləndi**", quote=True)
    
    # remove file
    try:
        os.remove(file_path)
    except:
        pass
    
    await txt.delete()
 
