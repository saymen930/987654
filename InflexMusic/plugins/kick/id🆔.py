from InflexMusic import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@app.on_message(filters.command("id"))
async def ids(_, message):
    reply = message.reply_to_message
    button = InlineKeyboardButton("✯ Bağla ✯", callback_data="close")
    markup = InlineKeyboardMarkup([[button]])

    if reply and reply.from_user:
        await message.reply_text(
            f"👤 İstifadəçi: {reply.from_user.first_name}\n🆔 ID: {reply.from_user.id}",
            reply_markup=markup,
            quote=True
        )
    else:
        await message.reply_text(
           f"<b>💬 Bu qrupun ID-si: {message.chat.id}</b>",
           reply_markup=markup,
           quote=True
        )

# Callback query handler - "close" düyməsinə cavab
@app.on_callback_query(filters.regex("close"))
async def close_callback(client, callback_query):
    await callback_query.message.delete()
    await callback_query.answer()  # Hər zaman cavab vermək lazımdır
