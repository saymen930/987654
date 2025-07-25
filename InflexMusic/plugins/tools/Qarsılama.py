# @AylinRobot
# Sahib @HuseynH
# Repo Açığdısa İcazəsis Götürmə Oğlum


from AylinRobot import AylinRobot as app
from pyrogram.errors import FloodWait
import random
from random import choice
from pyrogram import Client, filters
from AylinRobot.config import Config
from pyrogram.types import Message



 
@app.on_message(filters.new_chat_members, group=1) 
async def hg(bot: Client, message: Message): 
    for new_user in message.new_chat_members: 
        if str(new_user.id) == str(Config.BOT_ID): 
            await message.reply(f' {message.from_user.mention} @{Config.BOT_USERNAME}-U {message.chat.title} Qrupuna Aldığın Üçün Təşəkürlər⚡') 
  
        elif str(new_user.id) == str(Config.OWNER_ID): 
            await message.reply( 
  f'''@{Config.OWNER_NAME}\n👋 Bax Bu Gələn Mənim Sahibimdir.\n👮‍♂️ Sahibim {message.chat.title} Qrupuna Xoş Gəldin''')
        

      
@app.on_message(filters.new_chat_members)
async def newuser(client, message):
    chat_id = message.chat.id
    await message.reply_text(f"{message.from_user.mention} {message.chat.title} QRUPUNA 𝑋𝑂Ş 𝐺Ə𝐿𝐷İ𝑁 \n\n𝐴𝐷  {message.from_user.mention}\n𝑆𝑂𝑌𝐴𝐷 - {message.from_user.last_name if message.from_user.last_name else 'None'}\n𝑇𝐴Ğ 𝐴𝐷𝐼  @{message.from_user.username}\nİ𝐷  {message.from_user.id}\n\n☠ 𝐵𝐴𝑁 𝑆Ə𝐵Ə𝐵𝐿Ə𝑅İ ☠\n\n⚠️ 𝑆Ö𝑌ÜŞ \n🔞 𝑇Ə𝐻𝑄İ𝑅 \n⚠️ 𝑅𝐸𝐾𝐿𝐴𝑀 𝐹𝐿𝑂𝑂𝐷  🔇\n⚠️ 𝑋𝐴𝑁𝐼𝑀𝐿𝐴𝑅𝐴 ŞƏ𝑋𝑆İ𝐷Ə 𝑌𝐴𝑍𝑀𝐴𝑄 📵 \n⚠️ 𝑈𝑆𝐸𝑅 𝐷𝐴Ş𝐼𝑀𝐴𝑄 ⛔\n\n𝐿İ𝑁𝐾 {message.chat.username}")
    
    
@app.on_message(filters.left_chat_member)
async def newuser(client, message):
    chat_id = message.chat.id
    await message.reply_text(f"SƏNİ TANIMAQ GÖZƏL İDİ..")
