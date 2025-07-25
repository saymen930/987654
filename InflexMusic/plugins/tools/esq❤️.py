from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from InflexMusic import app
 

ESQ_FAIZ = ["17","18","20","22","24","25","27","29","30","31","33","35","36","39","40","42","43","45","47","49","50","55","56","57","58","60","62","64","65","66","68","70","72","74","75","77","79","80","82","84","85","87","89","90","92","93","95","97","98","99","100"]



@app.on_message(filters.command(["esq", "eşq"], [".", "!", "@", "/"]))
async def get_id(client, message):
    try:
 
        if (not message.reply_to_message) and (message.chat):
            await message.reply(f"✔ Bu Əmri Hər Hansı Bir Nəfərin Mesajına Yanıt Verərək İsdifadə Edin.")
          
        elif not message.reply_to_message:
            await message.reply(f"⚠️ **__XƏTA__**") 
 
        elif message.reply_to_message.forward_from_chat:
            await message.reply(f"**__⚠️XƏTA__**\n🚫 Bu Əmr Kanal Üzrə Keçərli Deyil")
 
        elif message.reply_to_message.forward_from:
            await message.reply(f"⚠️ **__XƏTA__**")
 
        elif message.reply_to_message.forward_sender_name:
            await message.reply("**__⚠️ XƏTA__**")
 
        else:
            await message.reply(f"Eşq Faizi Hesablandı\n\n{message.reply_to_message.from_user.mention} + {message.from_user.mention} = ❤\nEşq Faizi:-  {random.choice(ESQ_FAIZ)}")
 
    except Exception:
            await message.reply("⚠️  **__XƏTA__**")
 
