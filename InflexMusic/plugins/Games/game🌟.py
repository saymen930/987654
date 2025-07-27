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
        f"🎮 Söz Oyunu Başladı!\n\n"
        f"🔤 Qarışdırılmış söz: {scrambled}\n\n"
        f"Bu hərflərdən düzgün sözü tapın!\n"
        f"✅ Düzgün cavab: +25 xal\n"
        f"🛑 Oyunu bitirmək: /bitir və ya /dayan\n"
        f"📊 Xallarınızı görmək: /xallar\n"
        f"⏭️ Keçmək: /kec",
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
        return await event.reply("🎯 Hələ heç bir xalınız yoxdur. Oyuna başlamaq üçün /oyun yazın!")

    user_score = player_scores[chat_id][user_id]
    await event.reply(f"📊 {event.sender.first_name}, sizin xalınız: {user_score} xal 🌟")

# ==== /bitir və /dayan əmrləri ====
@client.on(events.NewMessage(pattern=r'/(dayan|bitir)'))
async def stop_game(event):
    if not event.is_group:
        return

    chat_id = event.chat_id

    if chat_id not in game_sessions or not game_sessions[chat_id]['active']:
        return await event.reply("🚫 Aktiv oyun yoxdur")

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
            f"🏁 Söz Oyunu Bitdi!\n\n"
            f"🏆 Ən yüksək xal: {top_name} - {top_score} xal\n\n"
            f"Yeni oyun üçün /oyun yazın! 🎮"
        )
    else:
        await event.reply("🏁 Söz Oyunu Bitdi! Yeni oyun üçün /oyun yazın! 🎮")

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
            f"🎉 Təbriklər, {event.sender.first_name}!\n"
            f"✅ Düzgün cavab verdiniz və 25 xal qazandınız!\n\n"
            f"🔤 Yeni söz: {scrambled}",
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
        return await message_event.reply("🚫 Aktiv oyun yoxdur. /oyun ilə başlayın!")

    word = get_random_word()
    scrambled = scramble_word(word)
    game_sessions[chat_id]['word'] = word
    game_sessions[chat_id]['scrambled'] = scrambled

    buttons = [[Button.inline("🔃 Sözü dəyişmək", b'kec')]]

    await message_event.reply(
        f"⏭️ Söz keçildi!\n\n"
        f"🔤 Yeni qarışdırılmış söz: {scrambled}\n\n"
        f"Bu hərflərdən düzgün sözü tapın!",
        buttons=buttons
    )
