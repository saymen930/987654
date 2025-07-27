import random
from telethon import TelegramClient, events, Button
from InflexMusic.core.bot import xaos as client  # Telethon bot instance
from Jason.word import WORDS

# ==== OYUN PARAMETRLƏRİ ====
game_sessions = {}
player_scores = {}

def get_random_word():
    return random.choice(WORDS)

def scramble_word(word):
    return ''.join(random.sample(word, len(word)))

# ==== /oyun əmri ====
@client.on(events.NewMessage(pattern='/oyun'))
async def start_game(event):
    if not event.is_group:
        return await event.reply("<b>❗ Bu əmr yalnız qruplarda işləyir</b>")
    
    chat_id = event.chat_id
    word = get_random_word()
    scrambled = scramble_word(word)

    game_sessions[chat_id] = {'word': word, 'scrambled': scrambled, 'active': True}
    if chat_id not in player_scores:
        player_scores[chat_id] = {}

    buttons = [[Button.inline("🔃 Sözü dəyişmək", b'kec')]]

    await event.reply(
        f"<b>🎮 Söz Oyunu Başladı!</b>\n\n"
        f"<b>🔤 Qarışdırılmış söz: {scrambled}</b>\n\n"
        f"<b>Bu hərflərdən düzgün sözü tapın!</b>\n"
        f"<b>✅ Düzgün cavab: +25 xal</b>\n"
        f"<b>🛑 Oyunu bitirmək: /bitir və ya /dayan</b>\n"
        f"<b>📊 Xallarınızı görmək: /xallar</b>\n"
        f"<b>⏭️ Keçmək: /kec</b>",
        buttons=buttons
    )

# ==== /xallar əmri ====
@client.on(events.NewMessage(pattern='/xallar'))
async def show_scores(event):
    if not event.is_group:
        return

    chat_id = event.chat_id
    user_id = event.sender_id

    if chat_id not in player_scores or user_id not in player_scores[chat_id]:
        return await event.reply("<b>🎯 Hələ heç bir xalınız yoxdur. Oyuna başlamaq üçün /oyun yazın!</b>")

    user_score = player_scores[chat_id][user_id]
    await event.reply(f"<b>📊 {event.sender.first_name}, sizin xalınız: {user_score} xal 🌟</b>")

# ==== /bitir və /dayan əmrləri ====
@client.on(events.NewMessage(pattern=r'/(dayan|bitir)'))
async def stop_game(event):
    if not event.is_group:
        return

    chat_id = event.chat_id

    if chat_id not in game_sessions or not game_sessions[chat_id]['active']:
        return await event.reply("<b>🚫 Aktiv oyun yoxdur.</b>")

    game_sessions[chat_id]['active'] = False

    if chat_id in player_scores and player_scores[chat_id]:
        top_player = max(player_scores[chat_id], key=player_scores[chat_id].get)
        top_score = player_scores[chat_id][top_player]
        try:
            top_user = await client.get_entity(top_player)
            top_name = top_user.first_name
        except:
            top_name = "Naməlum"

        await event.reply(
            f"<b>🏁 Söz Oyunu Bitdi!</b>\n\n"
            f"<b>🏆 Ən yüksək xal: {top_name} - {top_score} xal</b>\n\n"
            f"<b>Yeni oyun üçün /oyun yazın! 🎮</b>"
        )
    else:
        await event.reply("<b>🏁 Söz Oyunu Bitdi! Yeni oyun üçün /oyun yazın! 🎮</b>")

# ==== Cavab yoxlama ====
@client.on(events.NewMessage)
async def check_answer(event):
    if not event.is_group or event.text.startswith('/'):
        return

    chat_id = event.chat_id
    user_id = event.sender_id
    text = event.text.strip().lower()

    if chat_id not in game_sessions or not game_sessions[chat_id]['active']:
        return

    correct_word = game_sessions[chat_id]['word'].lower()
    if text == correct_word:
        if user_id not in player_scores[chat_id]:
            player_scores[chat_id][user_id] = 0
        player_scores[chat_id][user_id] += 25

        new_word = get_random_word()
        scrambled = scramble_word(new_word)
        game_sessions[chat_id]['word'] = new_word
        game_sessions[chat_id]['scrambled'] = scrambled

        buttons = [[Button.inline("🔃 Sözü dəyişmək", b'kec')]]

        await event.reply(
            f"<b>🎉 Təbriklər, {event.sender.first_name}!</b>\n"
            f"<b>✅ Düzgün cavab verdiniz və 25 xal qazandınız!</b>\n\n"
            f"<b>🔤 Yeni söz: {scrambled}</b>",
            buttons=buttons
        )

# ==== /kec əmri ====
@client.on(events.NewMessage(pattern='/kec'))
async def skip_word(event):
    await change_word(event.chat_id, event)

# ==== Buttonla dəyişmək ====
@client.on(events.CallbackQuery(data=b'kec'))
async def change_word_button(event):
    chat_id = event.chat_id
    message = await event.get_message()
    await change_word(chat_id, message)
    await event.answer("Yeni söz göndərildi!")

# ==== Söz dəyişdirmə funksiyası ====
async def change_word(chat_id, message_event):
    if chat_id not in game_sessions or not game_sessions[chat_id]['active']:
        return await message_event.reply("<b>🚫 Aktiv oyun yoxdur. /oyun ilə başlayın!</b>")

    word = get_random_word()
    scrambled = scramble_word(word)
    game_sessions[chat_id]['word'] = word
    game_sessions[chat_id]['scrambled'] = scrambled

    buttons = [[Button.inline("🔃 Sözü dəyişmək", b'kec')]]

    await message_event.reply(
        f"<b>⏭️ Söz keçildi!</b>\n\n"
        f"<b>🔤 Yeni qarışdırılmış söz: {scrambled}</b>\n\n"
        f"<b>Bu hərflərdən düzgün sözü tapın!</b>",
        buttons=buttons
    )
