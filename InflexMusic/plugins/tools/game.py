from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from InflexMusic import app
import random

WORDS = ["alma", "kitab", "telefon", "qələm", "komputer", "oyun", "məktəb"]
game_sessions = {}
player_scores = {}

def get_random_word():
    return random.choice(WORDS)

def scramble_word(word):
    return ''.join(random.sample(word, len(word)))

# 🎮 Oyun başlat
@app.on_message(filters.command("game") & filters.group)
async def start_game_command(client: Client, message: Message):
    chat_id = message.chat.id
    word = get_random_word()
    scrambled = scramble_word(word)

    game_sessions[chat_id] = {'word': word, 'scrambled': scrambled, 'active': True}

    if chat_id not in player_scores:
        player_scores[chat_id] = {}

    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔃 Sözü dəyişmək", callback_data="kec")]]
    )

    await message.reply(
        f"🎮 Söz Oyunu Başladı!\n\n"
        f"🔤 Qarışdırılmış söz: {scrambled}\n\n"
        f"Bu hərflərdən düzgün sözü tapın!\n"
        f"✅ Düzgün cavab: +25 xal\n"
        f"🛑 Oyunu bitirmək: /bitir və ya /stop\n"
        f"📊 Xallarınızı görmək: /xallar\n"
        f"⏭️ Keçmək: /kec",
        reply_markup=markup
    )

# 📊 Xallar
@app.on_message(filters.command("xallar") & filters.group)
async def show_scores_command(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if chat_id not in player_scores or user_id not in player_scores[chat_id]:
        await message.reply("🎯 Hələ heç bir xalınız yoxdur. Oyuna başlamaq üçün /game yazın!")
        return

    user_score = player_scores[chat_id][user_id]
    await message.reply(f"📊 {message.from_user.first_name}, sizin xalınız: {user_score} xal 🌟")

# ⏭️ Söz keçmək (/kec və ya button)
@app.on_message(filters.command("kec") & filters.group)
async def skip_word_command(client: Client, message: Message):
    await change_word(client, message)

# 🛑 Bitir
@app.on_message(filters.command(["bitir", "stop"]) & filters.group)
async def stop_game_command(client: Client, message: Message):
    chat_id = message.chat.id

    if chat_id not in game_sessions or not game_sessions[chat_id]['active']:
        await message.reply("🚫 Aktiv oyun yoxdur.")
        return

    game_sessions[chat_id]['active'] = False

    if chat_id in player_scores and player_scores[chat_id]:
        top_player = max(player_scores[chat_id], key=player_scores[chat_id].get)
        top_score = player_scores[chat_id][top_player]
        try:
            top_user = await app.get_chat_member(chat_id, top_player)
            top_name = top_user.user.first_name
        except:
            top_name = "Naməlum"

        await message.reply(
            f"🏁 Söz Oyunu Bitdi!\n\n"
            f"🏆 Ən yüksək xal: {top_name} - {top_score} xal\n\n"
            f"Yeni oyun üçün /game yazın! 🎮"
        )
    else:
        await message.reply("🏁 Söz Oyunu Bitdi! Yeni oyun üçün /game yazın! 🎮")

# ✅ Cavab yoxlama
@app.on_message(filters.text & filters.group)
async def check_answer(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.strip().lower()

    if chat_id not in game_sessions or not game_sessions[chat_id]['active']:
        return

    correct_word = game_sessions[chat_id]['word'].lower()
    if text == correct_word:
        # Xal artır
        if user_id not in player_scores[chat_id]:
            player_scores[chat_id][user_id] = 0
        player_scores[chat_id][user_id] += 25

        # Yeni söz
        new_word = get_random_word()
        scrambled = scramble_word(new_word)
        game_sessions[chat_id]['word'] = new_word
        game_sessions[chat_id]['scrambled'] = scrambled

        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔃 Sözü dəyişmək", callback_data="kec")]]
        )

        await message.reply(
            f"🎉 Təbriklər, {message.from_user.first_name}!\n"
            f"✅ Düzgün cavab verdiniz və 25 xal qazandınız!\n\n"
            f"🔤 Yeni söz: {scrambled}",
            reply_markup=markup
        )

# 🔃 Buttonla söz dəyişmək (callback)
@app.on_callback_query(filters.regex(r"^kec$"))
async def change_word_callback(client: Client, callback_query: CallbackQuery):
    message = callback_query.message
    await change_word(client, message)
    await callback_query.answer("Yeni söz göndərildi!")

# 💡 Funksiya: Söz dəyişdirmə
async def change_word(client, message):
    chat_id = message.chat.id

    if chat_id not in game_sessions or not game_sessions[chat_id]['active']:
        await message.reply("🚫 Aktiv oyun yoxdur. /game ilə başlayın!")
        return

    word = get_random_word()
    scrambled = scramble_word(word)
    game_sessions[chat_id]['word'] = word
    game_sessions[chat_id]['scrambled'] = scrambled

    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔃 Sözü dəyişmək", callback_data="kec")]]
    )

    await message.reply(
        f"⏭️ Söz keçildi!\n\n"
        f"🔤 Yeni qarışdırılmış söz: {scrambled}\n\n"
        f"Bu hərflərdən düzgün sözü tapın!",
        reply_markup=markup
  )
