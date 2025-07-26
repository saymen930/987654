import os
import json
import time
import random
import config
import asyncio
from dataclasses import dataclass, field
from typing import Dict, Set, List
from InflexMusic import app
from dotenv import load_dotenv
from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    Message, CallbackQuery
)

# ==========================
# KONFİQURASİYA
# ==========================
JOIN_COUNTDOWN = 15       # Oyuna qoşulma gerisayımı (saniyə)
ROUND_TIME = 50           # Hər söz üçün vaxt (saniyə)
GAME_IDLE_TIMEOUT = 40    # Heç kim oynamırsa oyunu dayandır (saniyə)



DATA_FILES = {
    "custom_words": "Jason/custom_words.json",
    "scores": "Jason/scores.json",
    "stats": "Jason/stats.json"
}

# ==========================
# YARDIMÇI FUNKSİYALAR
# ==========================
def load_json(path: str):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_group(message: Message) -> bool:
    return message.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP)

# ==========================
# STATE STRUKTURU
# ==========================
@dataclass
class GameState:
    ana_soz: str
    cavablar: List[str]
    tapilan: List[str] = field(default_factory=list)
    used: Set[str] = field(default_factory=set)  # bu qrupda istifadə olunan ana sözlər
    last_activity: float = field(default_factory=time.time)

# ==========================
# QLOBAL STATE
# ==========================
active_games: Dict[int, GameState] = {}   # chat_id -> GameState
joined_users: Dict[int, Set[int]] = {}    # chat_id -> {user_id, ...}
oyun_mesajlar: Dict[int, List[int]] = {}  # chat_id -> [message_ids...]
oyun_timer: Dict[int, float] = {}         # chat_id -> last activity ts

# Scores & stats & words
custom_words = load_json(DATA_FILES["custom_words"])
scores = load_json(DATA_FILES["scores"])
stats = load_json(DATA_FILES["stats"])




# ==========================
# KÖMƏKÇİLƏR
# ==========================
def get_joined(chat_id: int) -> Set[int]:
    return joined_users.setdefault(chat_id, set())

def add_stat_game_for_joined(chat_id: int):
    users = get_joined(chat_id)
    changed = False
    for uid in users:
        key = str(uid)
        if key not in stats:
            stats[key] = {"oyun": 0, "tapilan": 0}
        stats[key]["oyun"] += 1
        changed = True
    if changed:
        save_json(DATA_FILES["stats"], stats)

async def cleanup_messages(chat_id: int):
    msg_ids = oyun_mesajlar.get(chat_id, [])
    for mid in msg_ids:
        try:
            await app.delete_messages(chat_id, mid)
        except:
            pass
    oyun_mesajlar[chat_id] = []

async def stop_game(chat_id: int, reason: str = None):
    if chat_id in active_games:
        del active_games[chat_id]
    joined_users.pop(chat_id, None)
    oyun_timer.pop(chat_id, None)
    await cleanup_messages(chat_id)
    try:
        await app.unpin_all_chat_messages(chat_id)
    except:
        pass
    if reason:
        await app.send_message(chat_id, reason)

# ==========================
# /start (yalnız private)
# ==========================

 
@app.on_message(filters.command("g") & filters.group)
async def help_command(client, message):
    await message.reply_text(
        "👋 Salam! Bu bot vasitəsilə qruplarda söz tapma oyunu oynaya bilərsən.\n\n"
        "📚 Əmrlər:\n"
        "/games - Oyunu Başladar\n"
        "/join - Oyuna Qoşul\n"
        "/unjoin - Oyundan Ayrıl\n"
        "/joinup - Oyuna Qoşulanlara Bax\n"
        "/puan - Sənin Ümumi Puanın\n"
        "/gpuan - Qlobal Rəytinq\n"
        "/stats - Şəxsi statistika\n"
        "/soz - Söz əlavə et\n"
        "/saxla - Aktiv oyunu dayandır\n\n"
        "🧠 Sözləri tap, xal qazan və liderlikdə irəlilə!"
    )    
                   



# ==========================
# /game
# ==========================
@app.on_message(filters.command("games") & filters.group)
async def game_start(_, message: Message):
    chat_id = message.chat.id

    if chat_id in active_games:
        msg = await message.reply_text("❗ Oyun artıq aktivdir.")
        await asyncio.sleep(3)
        try:
            await app.delete_messages(chat_id, [msg.id, message.id])
        except:
            pass
        return

    # per-chat joined set
    joined_users[chat_id] = set()
    oyun_mesajlar[chat_id] = []

    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔗  Oyuna qoşul", callback_data=f"join_game:{chat_id}")]]
    )
    countdown_msg = await app.send_message(chat_id, f"🎮 Oyunun başlamasına {JOIN_COUNTDOWN} saniyə qaldı...", reply_markup=markup)
    oyun_mesajlar[chat_id].extend([message.id, countdown_msg.id])

    try:
        await app.pin_chat_message(chat_id, countdown_msg.id)
    except:
        pass

    async def countdown_and_start():
        checkpoints = {JOIN_COUNTDOWN, 12, 9, 6, 4, 1}
        for sec in range(JOIN_COUNTDOWN, 0, -1):
            if sec in checkpoints:
                try:
                    await countdown_msg.edit_text(f"🎮 Oyunun başlamasına ⏳ {sec} saniyə qaldı...", reply_markup=markup)
                except:
                    pass
            if sec == 6:
                msgx = await app.send_message(chat_id, "⏳ 5 saniyə qaldı...")
                oyun_mesajlar[chat_id].append(msgx.id)
            await asyncio.sleep(1)

        try:
            await countdown_msg.edit_text("🎯 Oyun başladı!")
        except:
            pass

        try:
            await app.delete_messages(chat_id, countdown_msg.id)
        except:
            pass

        await asyncio.sleep(0.6)
        await start_game(chat_id)

    asyncio.create_task(countdown_and_start())

@app.on_callback_query(filters.regex(r"^join_game:(-?\d+)$"))
async def handle_join_game(_, cq: CallbackQuery):
    chat_id = int(cq.data.split(":")[1])
    if cq.message.chat.type not in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
        await cq.answer("❗ Bu əməliyyat yalnız qrupda mümkündür.", show_alert=True)
        return

    users = get_joined(chat_id)
    user_id = cq.from_user.id
    if user_id not in users:
        users.add(user_id)
        await cq.answer("✅ Oyuna qoşuldun!")
        msg = await app.send_message(chat_id, f"👤 {cq.from_user.first_name} oyuna qoşuldu.")
        oyun_mesajlar.setdefault(chat_id, []).append(msg.id)
    else:
        await cq.answer("Artıq oyundasan!")
# /join
@app.on_message(filters.command("join") & filters.group)
async def join_cmd(_, message: Message):
    chat_id = message.chat.id

    # 🔴 Əgər aktiv oyun yoxdursa, xəbərdarlıq mesajı ver
    if chat_id not in active_games:
        await message.reply_text("❗ Hal-hazırda aktiv oyun yoxdur. Yeni oyun başlatmaq üçün /game yazın.")
        return

    users = get_joined(chat_id)
    user_id = message.from_user.id
    if user_id in users:
        await message.reply_text("🔁 Artıq oyundasan.")
        return

    users.add(user_id)
    await app.send_message(chat_id, f"📥 {message.from_user.first_name} oyuna qoşuldu.")

# /unjoin
@app.on_message(filters.command("unjoin") & filters.group)
async def unjoin_cmd(_, message: Message):
    chat_id = message.chat.id

    # 🔴 Aktiv oyun yoxdursa, əmri blokla
    if chat_id not in active_games:
        await message.reply_text("❗ Hal-hazırda aktiv oyun yoxdur, ayrılmaq üçün oyun başlamalıdır.")
        return

    users = get_joined(chat_id)
    user_id = message.from_user.id
    if user_id in users:
        users.remove(user_id)
        await app.send_message(chat_id, f"📤 {message.from_user.first_name} Oyundan ayrıldı.")
    else:
        await message.reply_text("ℹ️ Sən artıq oyunda deyilsən.")

# /stop
@app.on_message(filters.command("saxla") & filters.group)
async def stop_cmd(_, message: Message):
    chat_id = message.chat.id
    if chat_id in active_games:
        await stop_game(chat_id, f"🛑 Oyun {message.from_user.first_name} tərəfindən sonlandırıldı.")
    else:
        msg = await message.reply_text(f"ℹ️ Hörmətli {message.from_user.first_name}, hal-hazırda aktiv oyun yoxdur.")
        await asyncio.sleep(4)
        try:
            await app.delete_messages(chat_id, [msg.id, message.id])
        except:
            pass

# /joinup
@app.on_message(filters.command("joinup") & filters.group)
async def joinup_cmd(_, message: Message):
    chat_id = message.chat.id
    if chat_id not in active_games:
        msg = await message.reply_text("❗ Oyun aktiv deyil.")
        await asyncio.sleep(3)
        try:
            await app.delete_messages(chat_id, [msg.id, message.id])
        except:
            pass
        return

    users = get_joined(chat_id)
    if not users:
        msg = await message.reply_text("🧍‍♂️ Heç kim oyuna qoşulmayıb.")
    else:
        adlar = []
        for uid in users:
            try:
                member = await app.get_chat_member(chat_id, uid)
                adlar.append(f"👤 {member.user.first_name}")
            except:
                adlar.append(f"👤 {uid}")
        msg = await app.send_message(chat_id, "🎮 Oyuna qoşulanlar:\n\n" + "\n".join(adlar))

    await asyncio.sleep(5)
    try:
        await app.delete_messages(chat_id, [msg.id, message.id])
    except:
        pass

# /gpuan
@app.on_message(filters.command("gpuan"))
async def global_puan(_, message: Message):
    if not scores:
        await message.reply_text("📊 Hələ heç kim xal qazanmayıb.")
        return

    sıralama = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:15]
    mesaj = "🌍 Global Liderlər (TOP 15):\n\n"
    for i, (user_id, xal) in enumerate(sıralama, start=1):
        ad = f"ID:{user_id}"
        try:
            user = await app.get_users(int(user_id))
            ad = user.first_name
        except:
            pass
        mesaj += f"{i}. 👤 {ad} — ⭐ {xal} xal\n"

    await app.send_message(message.chat.id, mesaj)

# /puan
@app.on_message(filters.command("puan"))
async def show_puan(_, message: Message):
    user_id = str(message.from_user.id)
    puan = scores.get(user_id, 0)
    await message.reply_text(f"⭐ Xalın: {puan}")

# /stats
@app.on_message(filters.command("stats"))
async def user_stats(_, message: Message):
    user_id = str(message.from_user.id)
    data = stats.get(user_id, {"oyun": 0, "tapilan": 0})
    await message.reply_text(
        "📈 Statistikaların:\n"
        f"• Oyun sayı: {data.get('oyun',0)}\n"
        f"• Tapılan söz: {data.get('tapilan',0)}"
    )

# /soz
@app.on_message(filters.command("soz") & filters.group)
async def add_word(_, message: Message):
    try:
        _, soz, cavablar = message.text.split(" ", 2)
        cavablar = cavablar.strip("{} ").split(",")
        custom_words[soz.lower()] = [c.strip().lower() for c in cavablar if c.strip()]
        save_json(DATA_FILES["custom_words"], custom_words)
        await message.reply_text(f"✅ '{soz}' sözü və cavablar əlavə olundu.")
    except:
        await message.reply_text("❌ Format: /soz alma {alma,mal,lam,al}")

# ==========================
# OYUN FUNKSİYALARI
# ==========================
async def start_game(chat_id: int):
    users = get_joined(chat_id)
    if not users:
        await app.send_message(chat_id, "Heç kim oyuna qoşulmadığı üçün oyun başlamadı.")
        await stop_game(chat_id)
        return

    # təmizlə
    await cleanup_messages(chat_id)

    now = time.time()
    oyun_timer[chat_id] = now

    # oyun hərəkətsiz qalırsa dayandırma thread-i
    asyncio.create_task(oyunu_gözlə_timeout(chat_id))

    keys = list(custom_words.keys())
    if not keys:
        await app.send_message(chat_id, "❗ Söz bazası boşdur. Əvvəlcə /soz əmri ilə söz əlavə et.")
        await stop_game(chat_id)
        return

    state = active_games.get(chat_id)
    if state is None:
        # ilk dəfə başlayır
        ana_soz = random.choice(keys)
        cavablar = custom_words.get(ana_soz, [])
        if not cavablar:
            await app.send_message(chat_id, f"⚠️ `{ana_soz}` üçün cavablar tapılmadı.")
            await stop_game(chat_id)
            return
        state = GameState(ana_soz=ana_soz, cavablar=cavablar)
        state.used.add(ana_soz)
        active_games[chat_id] = state
        add_stat_game_for_joined(chat_id)
    else:
        # növbəti sözə keçidi burada da çağıracağıq
        available = [k for k in keys if k not in state.used]
        if not available:
            await app.send_message(chat_id, "🎉 Bütün səviyyələr tamamlandı!")
            await stop_game(chat_id)
            return
        ana_soz = random.choice(available)
        cavablar = custom_words.get(ana_soz, [])
        if not cavablar:
            await app.send_message(chat_id, f"⚠️ `{ana_soz}` üçün cavablar tapılmadı.")
            await stop_game(chat_id)
            return
        state.ana_soz = ana_soz
        state.cavablar = cavablar
        state.tapilan.clear()
        state.used.add(ana_soz)
        state.last_activity = now

    await app.send_message(chat_id, f"🧩 Aşağıdakı sözdən söz düzəldin:\n\n🌟 <code>{state.ana_soz}</code>", parse_mode=enums.ParseMode.HTML)

    # hər söz üçün timer
    asyncio.create_task(sual_timer(chat_id))

async def oyunu_gözlə_timeout(chat_id: int):
    await asyncio.sleep(GAME_IDLE_TIMEOUT)
    if chat_id in active_games:
        last = oyun_timer.get(chat_id, 0)
        if time.time() - last >= GAME_IDLE_TIMEOUT:
            await stop_game(chat_id, "Oyun oynanılmadığı üçün dayandırıldı.")

async def sual_timer(chat_id: int):
    start_time = time.time()
    while True:
        await asyncio.sleep(1)
        if chat_id not in active_games:
            break
        elapsed = time.time() - oyun_timer.get(chat_id, start_time)
        if elapsed >= ROUND_TIME:
            await app.send_message(chat_id, "⏰ Növbəti sözə keçid edildi...")
            await start_game(chat_id)
            break

# ==========================
# Sözləri yoxlayan message handler
# ==========================
@app.on_message(filters.text & filters.group & ~filters.command(["game","join","unjoin","joinup","puan","gpuan","stop","soz","stats"]))
async def check_word(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if chat_id not in active_games:
        return

    if user_id not in get_joined(chat_id):
        return

    game = active_games[chat_id]
    user_input = message.text.strip().lower()

    if user_input in game.tapilan:
        return

    if user_input in game.cavablar:
        game.tapilan.append(user_input)

        # sayğacı yalnız düzgün cavabda yenilə
        oyun_timer[chat_id] = time.time()

        uid = str(user_id)
        xal = len(user_input)
        scores[uid] = scores.get(uid, 0) + xal
        st = stats.setdefault(uid, {"oyun": 0, "tapilan": 0})
        st["tapilan"] += 1
        save_json(DATA_FILES["scores"], scores)
        save_json(DATA_FILES["stats"], stats)

        await message.reply_text(
            f"✅ {message.from_user.first_name} Cavab Doğrudur!\n"
            f"📊 {xal} xal qazandınız.\n\n⭐ '{game.ana_soz}'"
        )

        if len(game.tapilan) == len(game.cavablar):
            await app.send_message(chat_id, "🏆 Sözlər tapıldı. Yeni söz:")
            await start_game(chat_id)



@app.on_message(filters.command("restart") & (filters.private | filters.group))
async def restart_scores(client, message):
    user_id = message.from_user.id

    if user_id not in config.OWNER_IDS:
        await message.reply_text("⛔ Bu əmri yalnız bot sahib(lər)i istifadə edə bilər!")
        return

    # Faylları sıfırla
    scores.clear()
    stats.clear()
    save_json(DATA_FILES["scores"], scores)
    save_json(DATA_FILES["stats"], stats)

    await message.reply_text("♻️ **Bütün şəxsi və qlobal puanlar sıfırlandı!**")




@app.on_message(filters.command(["game", "join", "unjoin", "joinup", "stop"]) & filters.private)
async def tag_commands_private(client, message):
    await message.reply(
        "🛡️ Əmrir yalnız qruplar üçün nəzərdə tutub 🙎"
    )

# ==========================
# START
# ==========================
