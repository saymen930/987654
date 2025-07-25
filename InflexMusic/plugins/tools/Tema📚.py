import random
from random import choice
from pyrogram.errors import FloodWait
from InflexMusic import app
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


taim = [" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/sf158WSw7LWOtpvV) ",
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/bpcrFtP4qYu0DdnJ) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/aUFKCX7AQ3aQpDjp) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/L7HVQjC4UUyOfL9y) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/Qd4eBWTIOH4Ai3Zv) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/NightWolf) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/GreenBlack) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/TvldPzYmpG8LqkY3) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/Q4GuvNPpMvG59G6V) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/kGQaW0HHsjc7oFOv) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/z3E6vkceX0pfmo5P) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/poMW3amfnwUwOefI) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/l1felAbEVNQCN3NW) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/y6xMaSuBOmuGekHj) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/Fp6h6JpzXrWnjF9y) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/Purple_Grapes) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/xQNP1Jp2aklmldNx) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/ry0AgHsISs439fxi) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/ZHl93FYO9ja7hN81) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/gc2MlPyKHMBjw5WS) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/ciNZt5N6QCFjsrQI) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/bEKOF0v8XuLAFZ6P) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/IOSTelegramThemes2020_11july) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/DarkPink_1) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/Halloween_04) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/BlackBlue_ByYamila) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/NewYorkNyVK) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/blackcircles_ByYamila) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/KINGByVK) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/MRPERFECTBYVK) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/ChanchiNeonByVK) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/SamurayByVK) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/NeonRocks_ByYamila) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/StichOhanaByVK) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/SkullDarkByVK) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/RedGirlByVK) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/SpidermanByVK) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/CuteMelodyByVK) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/YouAreBeautifulStichByVK) " ,
" [𝕏𝔸𝕆𝕊](https://t.me/addtheme/ManchesterUnitedByVK) "]
 

@app.on_callback_query(filters.regex("close"))
async def close_reply(msg, CallbackQuery):
    await CallbackQuery.message.delete()
 

@app.on_message(filters.command("tema", ["/", "!", "@", "."]))
async def tema(app: Client, msg: Message):
    await msg.reply(random.choice(taim), reply_markup=temas)
  

temas = InlineKeyboardMarkup(

              [[InlineKeyboardButton(
                        "🔐 BAĞLA", callback_data= "close")]    
            ])
  
  
