from InflexMusic import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@app.on_message(filters.command("id"))
def ids(_, message):
    reply = message.reply_to_message
    button = InlineKeyboardButton("✯ Bağla ✯", callback_data="close")
    markup = InlineKeyboardMarkup([[button]])

    if reply:
        message.reply_text(
            f"👤 İstifadəçi: {reply.from_user.first_name}\n🆔 ID: `{reply.from_user.id}`",
            reply_markup=markup
        )
    else:
        message.reply(
           f"💬 Bu qrupun ID-si: `{message.chat.id}`",
           reply_markup=markup
        )
