import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from InflexMusic.core.bot import xaos as bot
# ⚠️ Warn məlumatları
warns = {}  # {(chat_id, user_id): warn_count}

# ✅ Admin yoxlaması
def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

# 🔍 İstifadəçini tap
def extract_user_id(message):
    if message.reply_to_message:
        return message.reply_to_message.from_user.id
    parts = message.text.split()
    if len(parts) >= 2:
        try:
            return int(parts[1])
        except:
            pass
    return None

# 🚫 /mute
@bot.message_handler(commands=['mute'])
def mute_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "⛔ Yalnız adminlər istifadə edə bilər")

    user_id = extract_user_id(message)
    if not user_id:
        return bot.reply_to(message, "Reply ilə və ya user_id ilə istifadə et.")

    until_date = datetime.now() + timedelta(days=365)
    try:
        bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=telebot.types.ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        bot.reply_to(message, "✅ İstifadəçi səssiz edildi")
    except Exception as e:
        bot.reply_to(message, f"Xəta: {e}")

# 🔊 /unmute
@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "⛔ Yalnız adminlər istifadə edə bilər")

    user_id = extract_user_id(message)
    if not user_id:
        return bot.reply_to(message, "Reply ilə və ya user_id ilə istifadə et.")

    try:
        bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=telebot.types.ChatPermissions(can_send_messages=True)
        )
        bot.reply_to(message, "✅ Səssizlik ləğv edildi")
    except Exception as e:
        bot.reply_to(message, f"Xəta: {e}")

# 🦶 /kick
@bot.message_handler(commands=['kick'])
def kick_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "⛔ Yalnız adminlər istifadə edə bilər")

    user_id = extract_user_id(message)
    if not user_id:
        return bot.reply_to(message, "Reply ilə və ya user_id ilə istifadə et.")

    try:
        bot.ban_chat_member(message.chat.id, user_id)
        bot.unban_chat_member(message.chat.id, user_id)
        bot.reply_to(message, "🚪 İstifadəçi qovuldu")
    except Exception as e:
        bot.reply_to(message, f"Xəta: {e}")

# ⚠️ /warn
@bot.message_handler(commands=['warn'])
def warn_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "⛔ Yalnız adminlər istifadə edə bilər")

    user_id = extract_user_id(message)
    if not user_id:
        return bot.reply_to(message, "Reply ilə və ya user_id ilə istifadə et.")

    key = (message.chat.id, user_id)
    warns[key] = warns.get(key, 0) + 1
    count = warns[key]

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("❌ Warn sil", callback_data=f"unwarn:{user_id}"))

    if count >= 3:
        try:
            bot.ban_chat_member(message.chat.id, user_id)
            warns[key] = 0
            bot.send_message(message.chat.id, f"⚠️ 3 xəbərdarlıq aldı və qovuldu!", reply_markup=markup)
        except Exception as e:
            bot.send_message(message.chat.id, f"Xəta: {e}")
    else:
        bot.send_message(message.chat.id, f"❗ Xəbərdarlıq verildi ({count}/3)", reply_markup=markup)

# 🧹 /unwarn
@bot.message_handler(commands=['unwarn'])
def unwarn_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "⛔ Yalnız adminlər istifadə edə bilər")

    user_id = extract_user_id(message)
    if not user_id:
        return bot.reply_to(message, "Reply ilə və ya user_id ilə istifadə et.")

    key = (message.chat.id, user_id)
    if warns.get(key, 0) > 0:
        warns[key] -= 1
        bot.reply_to(message, f"✅ Warn silindi ({warns[key]}/3)")
    else:
        bot.reply_to(message, "Bu istifadəçidə xəbərdarlıq yoxdur.")

# 🔘 Button warn sil
@bot.callback_query_handler(func=lambda call: call.data.startswith("unwarn:"))
def handle_unwarn_button(call):
    user_id = int(call.data.split(":")[1])
    chat_id = call.message.chat.id
    if not is_admin(chat_id, call.from_user.id):
        return bot.answer_callback_query(call.id, "⛔ Yalnız adminlər")

    key = (chat_id, user_id)
    if warns.get(key, 0) > 0:
        warns[key] -= 1
        bot.edit_message_text(f"✅ Warn silindi ({warns[key]}/3)", chat_id, call.message.message_id)
        bot.answer_callback_query(call.id, "Warn silindi")
    else:
        bot.answer_callback_query(call.id, "Warn yoxdur")

# 🤪 /kickme
@bot.message_handler(commands=['kickme'])
def kick_me(message):
    if is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "Axı səni atmaram balam, sən bir adminsən🫂")
    try:
        bot.ban_chat_member(message.chat.id, message.from_user.id)
        bot.unban_chat_member(message.chat.id, message.from_user.id)
        bot.reply_to(message, "😅 Özünü qovdun!")
    except Exception as e:
        bot.reply_to(message, f"Xəta: {e}")
