from pyrogram import Client, filters
from pyrogram.types import Message
from InflexMusic.owner import OWNER_ID  # owner.py-dən gəlir

from InflexMusic import app


@bot.message_handler(commands=['pin'])
def pin(message):
    if not is_admin(message.from_user.id, message.chat.id):
        return bot.reply_to(message, "❌ Bu əmri istifadə etmək üçün admin olmalısınız.")
    if not message.reply_to_message:
        return bot.reply_to(message, "🔺 Zəhmət olmasa, hər hansısa mesaja cavab verin ✅")
    try:
        bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
        bot.reply_to(message.reply_to_message, "📌 Bir mesajı sabitlədim")
    except Exception as e:
        bot.reply_to(message, "❌ Pin edilə bilmədi. Yetkiniz olmaya bilər.")

@bot.message_handler(commands=['unpin'])
def unpin(message):
    if not is_admin(message.from_user.id, message.chat.id):
        return bot.reply_to(message, "❌ Bu əmri istifadə etmək üçün admin olmalısınız.")
    if not message.reply_to_message:
        return bot.reply_to(message, "🔺 Zəhmət olmasa, hər hansısa mesaja cavab verin ✅")
    try:
        bot.unpin_chat_message(message.chat.id, message.reply_to_message.message_id)
        bot.reply_to(message.reply_to_message, "✅ Bir mesajı pindən sildim")
    except Exception as e:
        bot.reply_to(message, "❌ Pin silinə bilmədi. Yetkiniz olmaya bilər.")

@bot.message_handler(commands=['unpinall'])
def unpinall(message):
    if not is_admin(message.from_user.id, message.chat.id):
        return bot.reply_to(message, "❌ Bu əmri istifadə etmək üçün admin olmalısınız.")
    try:
        bot.unpin_all_chat_messages(message.chat.id)
        bot.reply_to(message, "✅ Bütün sabitləmələr silindi")
    except Exception as e:
        bot.reply_to(message, "❌ Bütün pinlər silinə bilmədi. Yetkiniz olmaya bilər.")
