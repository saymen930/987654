import os
import json
import time
import random
import asyncio
from typing import Dict, Set, List
from dataclasses import dataclass, field
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

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
    return message.chat.type in ("group", "supergroup", "channel")

# ==========================
# STATE STRUKTURU
# ==========================
@dataclass
class GameState:
    ana_soz: str
    cavablar: List[str]
    tapilan: List[str] = field(default_factory=list)
    used: Set[str] = field(default_factory=set)
    last_activity: float = field(default_factory=time.time)

# ==========================
# QLOBAL STATE
# ==========================
active_games: Dict[int, GameState] = {}
joined_users: Dict[int, Set[int]] = {}
oyun_mesajlar: Dict[int, List[int]] = {}
oyun_timer: Dict[int, float] = {}

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

async def cleanup_messages(client: Client, chat_id: int):
    msg_ids = oyun_mesajlar.get(chat_id, [])
    if not msg_ids:
        return
    try:
        await client.delete_messages(chat_id, msg_ids)
    except:
        pass
    oyun_mesajlar[chat_id] = []

async def stop_game(client: Client, chat_id: int, reason: str = None):
    if chat_id in active_games:
        del active_games[chat_id]
    joined_users.pop(chat_id, None)
    oyun_timer.pop(chat_id, None)
    await cleanup_messages(client, chat_id)
    if reason:
        await client.send_message(chat_id, reason)

async def send_and_collect(client: Client, chat_id: int, *args, **kwargs):
    msg = await client.send_message(chat_id, *args, **kwargs)
    oyun_mesajlar.setdefault(chat_id, []).append(msg.message_id)
    return msg

# ==========================
# OYUN FUNKSİYALARI
# ==========================
async def start_game(client: Client, chat_id: int):
    users = get_joined(chat_id)
    if not users:
        await client.send_message(chat_id, "Heç kim oyuna qoşulmadığı üçün oyun başlamadı.")
        await stop_game(client, chat_id)
        return

    await cleanup_messages(client, chat_id)

    now = time.time()
    oyun_timer[chat_id] = now

    asyncio.create_task(oyunu_gozle_timeout(client, chat_id))

    keys = list(custom_words.keys())
    if not keys:
        await client.send_message(chat_id, "❗ Söz bazası boşdur. Əvvəlcə /soz əmri ilə söz əlavə et.")
        await stop_game(client, chat_id)
        return

    state = active_games.get(chat_id)
    if state is None:
        ana_soz = random.choice(keys)
        cavablar = custom_words.get(ana_soz, [])
        if not cavablar:
            await client.send_message(chat_id, f"⚠️ `{ana_soz}` üçün cavablar tapılmadı.")
            await stop_game(client, chat_id)
            return
        state = GameState(ana_soz=ana_soz, cavablar=cavablar)
        state.used.add(ana_soz)
        active_games[chat_id] = state
        add_stat_game_for_joined(chat_id)
    else:
        available = [k for k in keys if k not in state.used]
        if not available:
            await client.send_message(chat_id, "🎉 Bütün səviyyələr tamamlandı!")
            await stop_game(client, chat_id)
            return
        ana_soz = random.choice(available)
        cavablar = custom_words.get(ana_soz, [])
        if not cavablar:
            await client.send_message(chat_id, f"⚠️ `{ana_soz}` üçün cavablar tapılmadı.")
            await stop_game(client, chat_id)
            return
        state.ana_soz = ana_soz
        state.cavablar = cavablar
        state.tapilan.clear()
        state.used.add(ana_soz)
        state.last_activity = now

    await client.send_message(chat_id,
        f"🧩 Aşağıdakı sözdən söz düzəldin:\n\n🌟 <code>{state.ana_soz}</code>",
        parse_mode="html"
    )

    asyncio.create_task(sual_timer(client, chat_id))

async def oyunu_gozle_timeout(client: Client, chat_id: int):
    await asyncio.sleep(GAME_IDLE_TIMEOUT)
    if chat_id in active_games:
        last = oyun_timer.get(chat_id, 0)
        if time.time() - last >= GAME_IDLE_TIMEOUT:
            await stop_game(client, chat_id, "Oyun oynanılmadığı üçün dayandırıldı.")

async def sual_timer(client: Client, chat_id: int):
    start_time = time.time()
    while True:
        await asyncio.sleep(1)
        if chat_id not in active_games:
            break
        elapsed = time.time() - oyun_timer.get(chat_id, start_time)
        if elapsed >= ROUND_TIME:
            await client.send_message(chat_id, "⏰ Növbəti sözə keçid edildi...")
            await start_game(client, chat_id)
            break

# ==========================
# BOT İNSTANSIN İLƏ ƏMRLƏR
# ==========================

def register_game_handlers(client: Client):

    @client.on_message(filters.command("games") & filters.group)
    async def game_start(client: Client, message: Message):
        chat_id = message.chat.id
        if chat_id in active_games:
            msg = await message.reply_text("❗ Oyun artıq aktivdir.")
            await asyncio.sleep(3)
            try:
                await client.delete_messages(chat_id, [msg.message_id, message.message_id])
            except:
                pass
            return

        joined_users[chat_id] = set()
        oyun_mesajlar[chat_id] = []

        buttons = [[InlineKeyboardButton("🔗 Oyuna qoşul", callback_data=f"join_game:{chat_id}")]]
        countdown_msg = await client.send_message(
            chat_id,
            f"🎮 Oyunun başlamasına {JOIN_COUNTDOWN} saniyə qaldı...",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        oyun_mesajlar[chat_id].extend([message.message_id, countdown_msg.message_id])

        async def countdown_and_start():
            checkpoints = {JOIN_COUNTDOWN, 12, 9, 6, 4, 1}
            for sec in range(JOIN_COUNTDOWN, 0, -1):
                if sec in checkpoints:
                    try:
                        await countdown_msg.edit(
                            f"🎮 Oyunun başlamasına ⏳ {sec} saniyə qaldı...",
                            reply_markup=InlineKeyboardMarkup(buttons)
                        )
                    except:
                        pass
                if sec == 6:
                    msgx = await client.send_message(chat_id, "⏳ 5 saniyə qaldı...")
                    oyun_mesajlar[chat_id].append(msgx.message_id)
                await asyncio.sleep(1)

            try:
                await countdown_msg.edit("🎯 Oyun başladı!", reply_markup=None)
            except:
                pass

            await asyncio.sleep(0.6)
            await start_game(client, chat_id)

        asyncio.create_task(countdown_and_start())

    @client.on_callback_query(filters.regex(r"join_game:\d+"))
    async def handle_join_game(client: Client, callback_query: CallbackQuery):
        data = callback_query.data
        chat_id = int(data.split(":")[1])

        users = get_joined(chat_id)
        user_id = callback_query.from_user.id

        if user_id not in users:
            users.add(user_id)
            await callback_query.answer("✅ Oyuna qoşuldun!")
            await client.send_message(chat_id, f"👤 {callback_query.from_user.first_name} oyuna qoşuldu.")
        else:
            await callback_query.answer("Artıq oyundasan!")

    @client.on_message(filters.command("join") & filters.group)
    async def join_cmd(client: Client, message: Message):
        chat_id = message.chat.id
        if chat_id not in active_games:
            await message.reply_text("❗ Hal-hazırda aktiv oyun yoxdur. Yeni oyun başlatmaq üçün /games yazın.")
            return

        users = get_joined(chat_id)
        user_id = message.from_user.id
        if user_id in users:
            await message.reply_text("🔁 Artıq oyundasan.")
            return

        users.add(user_id)
        await client.send_message(chat_id, f"📥 {message.from_user.first_name} oyuna qoşuldu.")

    @client.on_message(filters.command("unjoin") & filters.group)
    async def unjoin_cmd(client: Client, message: Message):
        chat_id = message.chat.id
        if chat_id not in active_games:
            await message.reply_text("❗ Hal-hazırda aktiv oyun yoxdur, ayrılmaq üçün oyun başlamalıdır.")
            return

        users = get_joined(chat_id)
        user_id = message.from_user.id
        if user_id in users:
            users.remove(user_id)
            await client.send_message(chat_id, f"📤 {message.from_user.first_name} oyundan ayrıldı.")
        else:
            await message.reply_text("ℹ️ Sən artıq oyunda deyilsən.")

    @client.on_message(filters.command("saxla") & filters.group)
    async def stop_cmd(client: Client, message: Message):
        chat_id = message.chat.id
        if chat_id in active_games:
            await stop_game(client, chat_id, f"🛑 Oyun {message.from_user.first_name} tərəfindən sonlandırıldı.")
        else:
            msg = await message.reply_text(f"ℹ️ Hörmətli {message.from_user.first_name}, hal-hazırda aktiv oyun yoxdur.")
            await asyncio.sleep(4)
            try:
                await client.delete_messages(chat_id, [msg.message_id, message.message_id])
            except:
                pass

    @client.on_message(filters.command("joinup") & filters.group)
    async def joinup_cmd(client: Client, message: Message):
        chat_id = message.chat.id
        if chat_id not in active_games:
            msg = await message.reply_text("❗ Oyun aktiv deyil.")
            await asyncio.sleep(3)
            try:
                await client.delete_messages(chat_id, [msg.message_id, message.message_id])
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
                    user = await client.get_users(uid)
                    adlar.append(f"👤 {user.first_name}")
                except:
                    adlar.append(f"👤 {uid}")
            msg = await client.send_message(chat_id, "🎮 Oyuna qoşulanlar:\n\n" + "\n".join(adlar))

        await asyncio.sleep(5)
        try:
            await client.delete_messages(chat_id, [msg.message_id, message.message_id])
        except:
            pass

    @client.on_message(filters.command("gpuan") & filters.group)
    async def global_puan(client: Client, message: Message):
        if not scores:
            await message.reply_text("📊 Hələ heç kim xal qazanmayıb.")
            return

        sıralama = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:15]
        mesaj = "🌍 Global Liderlər (TOP 15):\n\n"
        for i, (user_id, xal) in enumerate(sıralama, start=1):
            ad = f"ID:{user_id}"
            try:
                user = await client.get_users(int(user_id))
                ad = user.first_name
            except:
                pass
            mesaj += f"{i}. 👤 {ad} — ⭐ {xal} xal\n"

        await client.send_message(message.chat.id, mesaj)

    @client.on_message(filters.command("puan") & filters.group)
    async def show_puan(client: Client, message: Message):
        user_id = str(message.from_user.id)
        puan = scores.get(user_id, 0)
        await message.reply_text(f"⭐ Xalın: {puan}")

    @client.on_message(filters.command("stats") & filters.group)
    async def user_stats(client: Client, message: Message):
        user_id = str(message.from_user.id)
        data = stats.get(user_id, {"oyun": 0, "tapilan": 0})
        await message.reply_text(
            "📈 Statistikaların:\n"
            f"• Oyun sayı: {data.get('oyun',0)}\n"
            f"• Tapılan söz: {data.get('tapilan',0)}"
        )

    @client.on_message(filters.command("soz") & filters.group)
    async def add_word(client: Client, message: Message):
        # /soz alma {alma,mal,lam,al}
        parts = message.text.split(" ", 2)
        if len(parts) < 3:
            await message.reply_text("❌ Format: /soz alma {alma,mal,lam,al}")
            return
        try:
            _, soz, cavablar = parts
            cavablar = cavablar.strip("{} ").split(",")
            custom_words[soz.lower()] = [c.strip().lower() for c in cavablar if c.strip()]
            save_json(DATA_FILES["custom_words"], custom_words)
            await message.reply_text(f"✅ '{soz}' sözü və cavablar əlavə olundu.")
        except Exception:
            await message.reply_text("❌ Format: /soz alma {alma,mal,lam,al}")

    @client.on_message(filters.text & filters.group)
    async def check_word(client: Client, message: Message):
        if not is_group(message):
            return

        text = (message.text or "").strip()
        if not text:
            return

        if text.startswith("/"):
            return

        chat_id = message.chat.id
        user_id = message.from_user.id

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
                await client.send_message(chat_id, "🏆 Sözlər tapıldı. Yeni söz:")
                await start_game(client, chat_id)

# ==========================
# BU FUNKSİYANI SƏNİN BOTUNDA İMPORT EDİB ÇAĞIRACAQSAN
# ==========================
def setup_game_plugin(client: Client):
    register_game_handlers(client)
