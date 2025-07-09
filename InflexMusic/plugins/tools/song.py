### kddan Birkelme soz silen ve ya da deyişdiren
# -*- coding: utf-8 -*-
# rahid e ata desin # bu kodu yazan



from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from InflexMusic import app

# Komutu işle
@app.on_message(filters.command(["song"]))
async def fsfsfs(client, message):
    # Yanıtlanacak mesajı oluştur
    reply_message = await message.reply_text("Mahnı yükləmək üçün aşağıdakı bota daxil olun.")
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("➡️ Bota daxil ol", url="https://t.me/MultiAzBot"),
        InlineKeyboardButton("Kanal", url="https://t.me/multiazofficiall")]] 
    )# bunu silen rahide ata desin
    await reply_message.edit_reply_markup(reply_markup=keyboard)
