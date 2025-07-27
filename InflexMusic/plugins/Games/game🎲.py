import os
import json
import time
import random
import asyncio
from dataclasses import dataclass, field
from typing import Dict, Set, List
from InflexMusic.core.bot import xaos as client 
import config 
from dotenv import load_dotenv
from telethon import TelegramClient, events, Button
from telethon.tl.types import PeerChannel, PeerChat

# ==========================
# KONFİQURASİYA
# ==========================
JOIN_COUNTDOWN = 20      # Oyuna qoşulma gerisayımı (saniyə)
ROUND_TIME = 50           # Hər söz üçün vaxt (saniyə)
GAME_IDLE_TIMEOUT = 40    # Heç kim oynamırsa oyunu dayandır (saniyə)


DATA_FILES = {
    "custom_words": "Jason/custom_words.json",
    "scores": "Jason/scores.json",
    "stats": "Jason/stats.json"
}

 # /restart üçün icazə sahibi

# ==========================
# YARDIMÇI FUNKSİYALAR
# ==========================


SCORE_FİLE = "Jason/scores.json"

def load_json(path: str):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
#####
def save_scores(scores):
    with open(SCORE_FİLE, "w", encoding="utf-8") as f:
        json.dump(filters, f, indent=2, ensure_ascii=False)

#####

def is_group(event) -> bool:
    return isinstance(event.chat_id, int) and (event.is_group or event.is_channel and event.is_group)

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
# ENV & BOT
# ==========================
load_dotenv()


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
    if not msg_ids:
        return
    try:
        await client.delete_messages(chat_id, msg_ids)
    except:
        pass
    oyun_mesajlar[chat_id] = []

async def stop_game(chat_id: int, reason: str = None):
    if chat_id in active_games:
        del active_games[chat_id]
    joined_users.pop(chat_id, None)
    oyun_timer.pop(chat_id, None)
    await cleanup_messages(chat_id)
    # Telethon-da bütün pinləri toplu açmaq yoxdur, burda sadəcə ignore edirik
    if reason:
        await client.send_message(chat_id, reason)

async def send_and_collect(chat_id: int, *args, **kwargs):
    msg = await client.send_message(chat_id, *args, **kwargs)
    oyun_mesajlar.setdefault(chat_id, []).append(msg.id)
    return msg



# /game
# ==========================
@client.on(events.NewMessage(pattern=r"^[/!.]games(\s|$)(.*)"))
async def game_start(event: events.NewMessage.Event):
    if not is_group(event):
        await event.reply("🛡️ Əmr yalnız qruplar üçün nəzərdə tutulub 🙎")
        return

    chat_id = event.chat_id

    if chat_id in active_games:
        msg = await event.reply("❗ Oyun artıq aktivdir.")
        await asyncio.sleep(3)
        try:
            await client.delete_messages(chat_id, [msg.id, event.id])
        except:
            pass
        return

    joined_users[chat_id] = set()
    oyun_mesajlar[chat_id] = []

    buttons = [[Button.inline("🔗  Oyuna qoşul", data=f"join_game:{chat_id}".encode())]]
    countdown_msg = await client.send_message(chat_id, f"🎮 Oyunun başlamasına {JOIN_COUNTDOWN} saniyə qaldı...", buttons=buttons)
    oyun_mesajlar[chat_id].extend([event.id, countdown_msg.id])

    async def countdown_and_start():
        checkpoints = {JOIN_COUNTDOWN, 20, 17, 14, 9, 4, 1}
        for sec in range(JOIN_COUNTDOWN, 0, -1):
            if sec in checkpoints:
                try:
                    await countdown_msg.edit(f"🎮 Oyunun başlamasına ⏳ {sec} saniyə qaldı...", buttons=buttons)
                except:
                    pass
            if sec == 6:
                msgx = await client.send_message(chat_id, "⏳ 5 saniyə qaldı...")
                oyun_mesajlar[chat_id].append(msgx.id)
            await asyncio.sleep(1)

        try:
            await countdown_msg.edit("🎯 Oyun başladı!")
        except:
            pass

        await asyncio.sleep(0.6)
        await start_game(chat_id)

    asyncio.create_task(countdown_and_start())

@client.on(events.CallbackQuery(pattern=b"join_game:*"))
async def handle_join_game(event: events.CallbackQuery.Event):
    data = event.data.decode()
    _, chat_id_str = data.split(":")
    chat_id = int(chat_id_str)

    if not is_group(event):
        await event.answer("❗ Bu əməliyyat yalnız qrupda mümkündür.", alert=True)
        return

    users = get_joined(chat_id)
    user_id = event.sender_id
    if user_id not in users:
        users.add(user_id)
        await event.answer("✅ Oyuna qoşuldun!")
        msg = await client.send_message(chat_id, f"👤 {(await event.get_sender()).first_name} oyuna qoşuldu.")
        oyun_mesajlar.setdefault(chat_id, []).append(msg.id)
    else:
        await event.answer("Artıq oyundasan!")

# /join
@client.on(events.NewMessage(pattern=r"^[/!.]join(\s|$)(.*)"))
async def join_cmd(event: events.NewMessage.Event):
    if not is_group(event):
        await event.reply("🛡️ Əmr yalnız qruplar üçün nəzərdə tutulub 🙎")
        return

    chat_id = event.chat_id
    if chat_id not in active_games:
        await event.reply("❗ Hal-hazırda aktiv oyun yoxdur. Yeni oyun başlatmaq üçün /game yazın.")
        return

    users = get_joined(chat_id)
    user_id = event.sender_id
    if user_id in users:
        await event.reply("🔁 Artıq oyundasan.")
        return

    users.add(user_id)
    await client.send_message(chat_id, f"📥 {(await event.get_sender()).first_name} oyuna qoşuldu.")

# /unjoin
@client.on(events.NewMessage(pattern=r"^[/!.]unjoin(\s|$)(.*)"))
async def unjoin_cmd(event: events.NewMessage.Event):
    if not is_group(event):
        await event.reply("🛡️ Əmr yalnız qruplar üçün nəzərdə tutulub 🙎")
        return

    chat_id = event.chat_id
    if chat_id not in active_games:
        await event.reply("❗ Hal-hazırda aktiv oyun yoxdur, ayrılmaq üçün oyun başlamalıdır.")
        return

    users = get_joined(chat_id)
    user_id = event.sender_id
    if user_id in users:
        users.remove(user_id)
        await client.send_message(chat_id, f"📤 {(await event.get_sender()).first_name} Oyundan ayrıldı.")
    else:
        await event.reply("ℹ️ Sən artıq oyunda deyilsən.")

# /stop
@client.on(events.NewMessage(pattern=r"^[/!.]saxla(\s|$)(.*)"))
async def stop_cmd(event: events.NewMessage.Event):
    if not is_group(event):
        await event.reply("🛡️ Əmr yalnız qruplar üçün nəzərdə tutulub 🙎")
        return

    chat_id = event.chat_id
    if chat_id in active_games:
        await stop_game(chat_id, f"🛑 Oyun {(await event.get_sender()).first_name} tərəfindən sonlandırıldı.")
    else:
        msg = await event.reply(f"ℹ️ Hörmətli {(await event.get_sender()).first_name}, hal-hazırda aktiv oyun yoxdur.")
        await asyncio.sleep(4)
        try:
            await client.delete_messages(chat_id, [msg.id, event.id])
        except:
            pass

# /joinup
@client.on(events.NewMessage(pattern=r"^[/!.]joinup(\s|$)(.*)"))
async def joinup_cmd(event: events.NewMessage.Event):
    if not is_group(event):
        await event.reply("🛡️ Əmr yalnız qruplar üçün nəzərdə tutulub 🙎")
        return

    chat_id = event.chat_id
    if chat_id not in active_games:
        msg = await event.reply("❗ Oyun aktiv deyil.")
        await asyncio.sleep(3)
        try:
            await client.delete_messages(chat_id, [msg.id, event.id])
        except:
            pass
        return

    users = get_joined(chat_id)
    if not users:
        msg = await event.reply("🧍‍♂️ Heç kim oyuna qoşulmayıb.")
    else:
        adlar = []
        for uid in users:
            try:
                user = await client.get_entity(uid)
                adlar.append(f"👤 {user.first_name}")
            except:
                adlar.append(f"👤 {uid}")
        msg = await client.send_message(chat_id, "🎮 Oyuna qoşulanlar:\n\n" + "\n".join(adlar))

    await asyncio.sleep(5)
    try:
        await client.delete_messages(chat_id, [msg.id, event.id])
    except:
        pass

# /gpuan
@client.on(events.NewMessage(pattern=r"^[/!.]gpuan(\s|$)(.*)"))
async def global_puan(event: events.NewMessage.Event):
    if not scores:
        await event.reply("📊 Hələ heç kim xal qazanmayıb.")
        return

    sıralama = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:15]
    mesaj = "🌍 Global Liderlər (TOP 15):\n\n"
    for i, (user_id, xal) in enumerate(sıralama, start=1):
        ad = f"ID:{user_id}"
        try:
            user = await client.get_entity(int(user_id))
            ad = user.first_name
        except:
            pass
        mesaj += f"{i}. 👤 {ad} — ⭐ {xal} xal\n"

    await client.send_message(event.chat_id, mesaj)

# /puan
@client.on(events.NewMessage(pattern=r"^[/!.]puan(\s|$)(.*)"))
async def show_puan(event: events.NewMessage.Event):
    user_id = str(event.sender_id)
    puan = scores.get(user_id, 0)
    await event.reply(f"⭐ Xalın: {puan}")

# /stats
@client.on(events.NewMessage(pattern=r"^[/!.]stats(\s|$)(.*)"))
async def user_stats(event: events.NewMessage.Event):
    user_id = str(event.sender_id)
    data = stats.get(user_id, {"oyun": 0, "tapilan": 0})
    await event.reply(
        "📈 Statistikaların:\n"
        f"• Oyun sayı: {data.get('oyun',0)}\n"
        f"• Tapılan söz: {data.get('tapilan',0)}"
    )

# /soz
@client.on(events.NewMessage(pattern=r"^[/!.]soz(\s|$)(.*)"))
async def add_word(event: events.NewMessage.Event):
    if len(event.raw_text.split(" ", 2)) < 3:
        await event.reply("❌ Format: /soz alma {alma,mal,lam,al}")
        return
    try:
        _, soz, cavablar = event.raw_text.split(" ", 2)
        cavablar = cavablar.strip("{} ").split(",")
        custom_words[soz.lower()] = [c.strip().lower() for c in cavablar if c.strip()]
        save_json(DATA_FILES["custom_words"], custom_words)
        await event.reply(f"✅ '{soz}' sözü və cavablar əlavə olundu.")
    except Exception as e:
        await event.reply("❌ Format: /soz alma {alma,mal,lam,al}")

# /restart (admin)
# /restart (admin)
@client.on(events.NewMessage(pattern=r"^[/!.]restart(\s|$)(.*)"))
async def restart_scores(event: events.NewMessage.Event):
    if event.sender_id not in config.OWNER_IDS:  # Siyahıda varmı yoxlanır
        await event.reply("⛔ Bu əmri yalnız bot sahib istifadə edə bilər!")
        return

    scores.clear()
    stats.clear()
    save_json(DATA_FILES["scores"], scores)
    save_json(DATA_FILES["stats"], stats)

    await event.reply("♻️ **Bütün şəxsi və qlobal puanlar sıfırlandı!**")
    
#@client.on(events.NewMessage(pattern=r"^/(game|join|unjoin|joinup|stop)$"))
#async def tag_commands_private(event: events.NewMessage.Event):
    #if event.is_private:
        #await event.reply("🛡️ Əmr yalnız qruplar üçün nəzərdə tutulub 🙎")

# ==========================
# OYUN FUNKSİYALARI
# ==========================
async def start_game(chat_id: int):
    users = get_joined(chat_id)
    if not users:
        await client.send_message(chat_id, "Heç kim oyuna qoşulmadığı üçün oyun başlamadı.")
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
        await client.send_message(chat_id, "❗ Söz bazası boşdur. Əvvəlcə /soz əmri ilə söz əlavə et.")
        await stop_game(chat_id)
        return

    state = active_games.get(chat_id)
    if state is None:
        # ilk dəfə başlayır
        ana_soz = random.choice(keys)
        cavablar = custom_words.get(ana_soz, [])
        if not cavablar:
            await client.send_message(chat_id, f"⚠️ `{ana_soz}` üçün cavablar tapılmadı.")
            await stop_game(chat_id)
            return
        state = GameState(ana_soz=ana_soz, cavablar=cavablar)
        state.used.add(ana_soz)
        active_games[chat_id] = state
        add_stat_game_for_joined(chat_id)
    else:
        # növbəti sözə keçid
        available = [k for k in keys if k not in state.used]
        if not available:
            await client.send_message(chat_id, "🎉 Bütün səviyyələr tamamlandı!")
            await stop_game(chat_id)
            return
        ana_soz = random.choice(available)
        cavablar = custom_words.get(ana_soz, [])
        if not cavablar:
            await client.send_message(chat_id, f"⚠️ `{ana_soz}` üçün cavablar tapılmadı.")
            await stop_game(chat_id)
            return
        state.ana_soz = ana_soz
        state.cavablar = cavablar
        state.tapilan.clear()
        state.used.add(ana_soz)
        state.last_activity = now

    await client.send_message(chat_id, f"🧩 Aşağıdakı sözdən söz düzəldin:\n\n🌟 <code>{state.ana_soz}</code>", parse_mode="html")

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
            await client.send_message(chat_id, "⏰ Növbəti sözə keçid edildi...")
            await start_game(chat_id)
            break

# ==========================
# Sözləri yoxlayan handler
# ==========================
@client.on(events.NewMessage())
async def check_word(event: events.NewMessage.Event):
    """
    Bütün mesajları tutur. Aşağıdakı şərtləri keçməyənləri return edirik.
    """
    if not is_group(event):
        return

    text = (event.raw_text or "").strip()
    if not text:
        return

    # Komandaları burda ignore et
    if text.startswith("/"):
        return

    chat_id = event.chat_id
    user_id = event.sender_id

    if chat_id not in active_games:
        return

    if user_id not in get_joined(chat_id):
        return

    game = active_games[chat_id]
    user_input = text.lower()

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

        sender = await event.get_sender()
        await event.reply(
            f"✅ {sender.first_name} Cavab Doğrudur!\n"
            f"📊 {xal} xal qazandınız.\n\n⭐ '{game.ana_soz}'"
        )

        if len(game.tapilan) == len(game.cavablar):
            await client.send_message(chat_id, "🏆 Sözlər tapıldı. Yeni söz:")
            await start_game(chat_id)

# ==========================
# START
# ==========================
