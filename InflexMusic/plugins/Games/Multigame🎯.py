import os
import json
import time
import random
import asyncio
from dataclasses import dataclass, field
from typing import Dict, Set, List
import config
from dotenv import load_dotenv
from telethon import TelegramClient, events, Button
from telethon.tl.types import PeerChannel, PeerChat
from InflexMusic.core.bot import xaos as client  # Telethon bot instance
from Jason.word import WORDS

# ==========================
JOIN_COUNTDOWN = 20     # Oyuna qoşulma gerisayımı (saniyə)
ROUND_TIME = 50           # Hər söz üçün vaxt (saniyə)
GAME_IDLE_TIMEOUT = 40    # Heç kim oynamırsa oyunu dayandır (saniyə)


DATA_FILES = {
    "custom_words": "Jason/custom_words.json",
    "scores": "Jason/scores.json",
    "stats": "Jason/stats.json"
}



SCORE_FİLE = "/Jason/scores.json"

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


active_games: Dict[int, GameState] = {}   # chat_id -> GameState
joined_users: Dict[int, Set[int]] = {}    # chat_id -> {user_id, ...}
oyun_mesajlar: Dict[int, List[int]] = {}  # chat_id -> [message_ids...]
oyun_timer: Dict[int, float] = {}         # chat_id -> last activity ts

# Scores & stats & words
custom_words = load_json(DATA_FILES["custom_words"])
scores = load_json(DATA_FILES["scores"])
stats = load_json(DATA_FILES["stats"])



game_sessions = {}
player_scores = {}

def get_random_word():
    return random.choice(WORDS)

def scramble_word(word):
    return ''.join(random.sample(word, len(word)))
    
    
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
    if reason:
        await client.send_message(chat_id, reason)

async def send_and_collect(chat_id: int, *args, **kwargs):
    msg = await client.send_message(chat_id, *args, **kwargs)
    oyun_mesajlar.setdefault(chat_id, []).append(msg.id)
    return msg






@client.on(events.NewMessage(pattern=r"^[/!.]puan(\s|$)(.*)"))
async def ask_puan(event: events.NewMessage.Event):
    if not is_group(event):
        await event.reply("🛡️ Əmr yalnız qruplar üçün nəzərdə tutulub 🙎")
        return
    
    buttons = [
        [Button.inline("🇦🇿 𝙰𝚉𝙱𝚄𝙻", data="az_puan"),
         Button.inline("📚 𝚆𝙾𝚁𝙳 𝙶𝙰𝙼𝙴 ", data="soz_puan")],
        [Button.inline("📊 𝚂𝚃𝙰𝚃İ𝚂𝙺𝙰", data="s_puan"),
         Button.inline("🗑️ 𝙱𝙰Ğ𝙻𝙰", data="cancel_game_msg")]
    ]
    msg = await event.reply("\n💁 Puan Taboru Üçün Oyun Növünü Seçın.", buttons=buttons)
    oyun_mesajlar.setdefault(event.chat_id, []).append(msg.id)    
   
    
     

    
@client.on(events.CallbackQuery(data=b"b_b"))
async def handle_az_puan(event: events.CallbackQuery.Event):
    buttons = [
        [Button.inline("🇦🇿 𝙰𝚉𝙱𝚄𝙻", data="az_puan"),
         Button.inline("📚 𝚆𝙾𝚁𝙳 𝙶𝙰𝙼𝙴", data="soz_puan")],
        [Button.inline("📊 𝚂𝚃𝙰𝚃İ𝚂𝙺𝙰", data="s_puan"),
         Button.inline("🗑️ 𝙱𝙰Ğ𝙻𝙰", data="cancel_game_msg")]
    ]
    msg = await event.edit("\n💁 Puan Taboru Üçün Oyun Növünü Seçın.", buttons=buttons)

    if msg:
        oyun_mesajlar.setdefault(event.chat_id, []).append(msg.id)      
            
                      

@client.on(events.CallbackQuery(data=b"az_puan"))
async def handle_az_puan(event: events.CallbackQuery.Event):
    buttons = [
        [Button.inline("🌐 𝙶𝙻𝙾𝙱𝙰𝙻", data="g_p"),
         Button.inline("💁 Ö𝚉Ə𝙻", data="o_p")],
        [Button.inline("🔙 𝙶𝙴𝚁İ", data="b_b"),
        Button.inline("🗑️ 𝙱𝙰Ğ𝙻𝙰", data="cancel_game_msg")]
    ]
    msg = await event.edit("🇦🇿 𝙰𝚉𝙱𝚄𝙻 Puan Taboru Üçün Oyun Növünü Seçin", buttons=buttons)

    if msg:
        oyun_mesajlar.setdefault(event.chat_id, []).append(msg.id)    
    
       
        
#button = [[Button.inline("🔙 Geri", data="b_b")]]
          

#buttons = [[Button.inline("🔙 Geri", data="az_puan")]]
button = [
    [Button.inline("🔙 𝙶𝙴𝚁İ", data="b_b"),
     Button.inline("🗑️ 𝙱𝙰Ğ𝙻𝙰", data="cancel_game_msg")]]
    
          

buttons = [
    [Button.inline("🔙 𝙶𝙴𝚁İ", data="az_puan"),
     Button.inline("🗑️ 𝙱𝙰Ğ𝙻𝙰", data="cancel_game_msg")]]
    


#@client.on(events.NewMessage(pattern='/xallar'))
#async def show_scores(event):
    
@client.on(events.CallbackQuery(data=b"soz_puan"))
async def handle_soz_puan(event: events.CallbackQuery.Event):
    if not event.is_group:
        return

    chat_id = event.chat_id
    user_id = event.sender_id

    if chat_id not in player_scores or user_id not in player_scores[chat_id]:
        return await event.edit("🎯 Hələ heç bir xalınız yoxdur. Oyuna başlamaq üçün /game yazın!", buttons=button)

    user_score = player_scores[chat_id][user_id]
    await event.edit(
        f"📚 𝚆𝙾𝚁𝙳 𝙶𝙰𝙼𝙴 Üçün Puan\n\n📊 {event.sender.first_name}, sizin xalınız: {user_score} xal 🌟",
        buttons=button
    )    








@client.on(events.CallbackQuery(data=b"g_p"))
async def handle_g_puan(event: events.CallbackQuery.Event):
    if not scores:
        await event.edit("📊 Hələ heç kim xal qazanmayıb.",
                         buttons=[[Button.inline("🔙 Geri", data="az_puan")]])
        return

    sıralama = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:15]
    mesaj = "🌍 𝙶𝙻𝙾𝙱𝙰𝙻 Liderlər (TOP 15):\n\n"
    for i, (user_id, xal) in enumerate(sıralama, start=1):
        try:
            user = await client.get_entity(int(user_id))
            ad = user.first_name
        except:
            ad = f"ID:{user_id}"
        mesaj += f"{i}. 👤 {ad} — ⭐ {xal} xal\n"

    # Aşağıya "🔙 Geri" düyməsini əlavə edirik
    
    try:
        await event.edit(mesaj, buttons=buttons)
    except Exception as e:
        await event.edit("📛 Mesaj çox uzundur və redaktə edilə bilmir.",
                         buttons=buttons)    
    
    
    
@client.on(events.CallbackQuery(data=b"o_p"))
async def handle_o_p(event: events.CallbackQuery.Event):    
    user_id = str(event.sender_id)
    puan = scores.get(user_id, 0)
    await event.edit(f"💁 Ö𝚉Ə𝙻 Puan Taboru\n\n⭐ Xalın: {puan}", buttons=buttons)




@client.on(events.CallbackQuery(data=b"s_puan"))
async def handle_az_puan(event: events.CallbackQuery.Event):    
    user_id = str(event.sender_id)
    data = stats.get(user_id, {"oyun": 0, "tapilan": 0})
    await event.edit(
        "🇦🇿 𝙰𝚉𝙱𝚄𝙻 Oyunu Üçün Statiska:\n\n"
        f"• Oyun sayı: {data.get('oyun',0)}\n"
        f"• Tapılan söz: {data.get('tapilan',0)}", buttons=button
    )
    
# /stats
#@client.on(events.NewMessage(pattern=r"^[/!.]stats(\s|$)(.*)"))
#async def user_stats(event: events.NewMessage.Event):
    #user_id = str(event.sender_id)
    #data = stats.get(user_id, {"oyun": 0, "tapilan": 0})
    #await event.reply(
        #"📈 Statistikaların:\n"
        #f"• Oyun sayı: {data.get('oyun',0)}\n"
        #f"• Tapılan söz: {data.get('tapilan',0)}"
    #)


@client.on(events.NewMessage(pattern=r"^[/!.]game(\s|$)(.*)"))
async def ask_game_start(event: events.NewMessage.Event):
    if not is_group(event):
        await event.reply("🛡️ Əmr yalnız qruplar üçün nəzərdə tutulub 🙎")
        return

    buttons = [
        [Button.inline("🇦🇿 𝙰𝚉𝙱𝚄𝙻", data="start_real_game"),
         Button.inline("📚 𝚂Ö𝚉 ", data="soz_real_game")],
        [Button.inline("🗑️ 𝙱𝙰Ğ𝙻𝙰", data="cancel_game_msg")]
    ]
    
    msg = await event.reply("🎮 Oyun növünü seçin.", buttons=buttons)

    # Mesaj ID-ləri saxlanılır
    oyun_mesajlar.setdefault(event.chat_id, []).append(msg.id)

    # 10 saniyə sonra mesajı sil
    await asyncio.sleep(5)
    try:
        await client.delete_messages(event.chat_id, msg.id)
    except:
        pass  # silinmişsə və ya hüquq yoxdursa, xətanı burax

@client.on(events.CallbackQuery(data=b"cancel_game_msg"))
async def handle_cancel_game_msg(event: events.CallbackQuery.Event):
    try:
        await event.delete()
    except:
        pass



@client.on(events.CallbackQuery(data=b"cancel_game_msg"))
async def cancel_game_msg(event):
    try:
        await client.delete_messages(event.chat_id, event.message.id)
    except:
        pass
    await event.answer("❌ Mesaj silindi.", alert=True)


#@client.on(events.CallbackQuery(data=b"start_real_game"))
#async def handle_real_game_start(event: events.CallbackQuery.Event):
    
@client.on(events.CallbackQuery(data=b"start_real_game"))
async def handle_real_game_start(event: events.CallbackQuery.Event):
    try:
        # Seçim mesajını sil
        await client.delete_messages(event.chat_id, event.message.id)
    except:
        pass    
    
    if not is_group(event):
        await event.answer("🛡️ Əmr yalnız qruplar üçün nəzərdə tutulub 🙎", alert=True)
        return

    chat_id = event.chat_id

    if chat_id in active_games:
        msg = await event.respond("❗ Oyun artıq aktivdir.")
        await asyncio.sleep(3)
        try:
            await client.delete_messages(chat_id, [msg.id, event.message.id])
        except Exception as e:
            print("Silinmə xətası:", e)
        return

    # Buton mesajlarını sil (əgər varsa)
    for msg_id in oyun_mesajlar.get(chat_id, []):
        try:
            await client.delete_messages(chat_id, msg_id)
        except:
            pass
    oyun_mesajlar[chat_id] = []

    joined_users[chat_id] = set()

    buttons = [[Button.inline("🔗  Oyuna qoşul", data=f"join_game:{chat_id}".encode())]]
    countdown_msg = await client.send_message(chat_id, f"🎮 Oyunun başlamasına {JOIN_COUNTDOWN} saniyə qaldı...", buttons=buttons)

    oyun_mesajlar[chat_id].append(countdown_msg.id)

    async def countdown_and_start():
        checkpoints = {JOIN_COUNTDOWN, 20, 15, 11, 7, 4, 1}
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




@client.on(events.NewMessage(pattern=r"^[/!.]restart(\s|$)(.*)"))
async def restart_scores(event: events.NewMessage.Event):
    if event.sender_id not in config.OWNER_IDS:  # Siyahıda varmı yoxlanır
        await event.reply("⛔ Bu əmri yalnız bot sahib istifadə edə bilər!")
        return

    scores.clear()
    stats.clear()
    save_json(DATA_FILES["scores"], scores)
    save_json(DATA_FILES["stats"], stats)

    await event.reply("♻️ **Bütün şəxsi və qlobal puanlar sıfırlandı!")
    

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
            await client.send_message(chat_id, f"⚠️ {ana_soz} üçün cavablar tapılmadı.")
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
            await client.send_message(chat_id, f"⚠️ {ana_soz} üçün cavablar tapılmadı.")
            await stop_game(chat_id)
            return
        state.ana_soz = ana_soz
        state.cavablar = cavablar
        state.tapilan.clear()
        state.used.add(ana_soz)
        state.last_activity = now

    await client.send_message(chat_id, f"🧩 Aşağıdakı sözdən söz düzəldin:\n\n📚 <code>{state.ana_soz}</code>", parse_mode="html")

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




@client.on(events.NewMessage())
async def check_word(event: events.NewMessage.Event):

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
            f"📊 {xal} xal qazandınız.\n\n📚 {game.ana_soz}"
        )

        if len(game.tapilan) == len(game.cavablar):
            await client.send_message(chat_id, "🏆 Sözlər tapıldı. Yeni söz:")
            await start_game(chat_id)


###########
#######
######

#@client.on(events.NewMessage(pattern='/oyun'))
#async def start_game(event):
@client.on(events.CallbackQuery(data=b"soz_real_game"))
async def handle_soz_real_game_start(event: events.CallbackQuery.Event):    
    if not event.is_group:
        return await event.reply("<b>❗ Bu əmr yalnız qruplarda işləyir</b>")

    chat_id = event.chat_id

    # Əgər oyun aktivdirsə — yeni oyun başladılmasın
    if chat_id in game_sessions and game_sessions[chat_id].get('active') == True:
        return await event.answer("⚠️ Bu qrupda artıq aktiv oyun var!\n/bitir  əmri ilə dayandıra bilərsiniz.", alert=True)

    # Yeni söz seç və qarışdır
    word = get_random_word()
    scrambled = scramble_word(word)

    # Oyun sessiyasını yadda saxla
    game_sessions[chat_id] = {
        'word': word,
        'scrambled': scrambled,
        'active': True
    }

    # Qrup üçün xal siyahısı yoxdursa, yarat
    if chat_id not in player_scores:
        player_scores[chat_id] = {}

    # Butonlar
    buttons = [[Button.inline("🔃 Sözü dəyişmək", b'kec')]]

    await event.reply(
        f" 📚 𝚆𝙾𝚁𝙳 𝙶𝙰𝙼𝙴 Oyunu Başladı!\n\n"
        f"🔤 Qarışdırılmış söz: {scrambled}\n\n"
        f"Bu hərflərdən düzgün sözü tapın!\n"
        f"✅ Düzgün cavab: +5 xal\n"
        f"🛑 Bitirmək: /bitir\n"
        f"📊 Xallar: /puan\n",
        buttons=buttons
    )

# ==== /bitir və /dayan əmrləri ====

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
        player_scores[chat_id][user_id] += 5

        new_word = get_random_word()
        scrambled = scramble_word(new_word)
        game_sessions[chat_id]['word'] = new_word
        game_sessions[chat_id]['scrambled'] = scrambled

        buttons = [[Button.inline("🔃 Sözü dəyişmək", b'kec')]]

        await event.reply(
            f"🎉 Təbriklər, {event.sender.first_name}!\n"
            f"✅ Düzgün cavab verdiniz və 5 xal qazandınız!\n\n"
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









@client.on(events.NewMessage(pattern=r"^[/!.](saxla|bitir|dayan)(\s|$)"))
async def stop_any_game(event: events.NewMessage.Event):
    if not is_group(event):
        await event.reply("🛡️ Bu əmr yalnız qruplarda işləyir.")
        return

    chat_id = event.chat_id
    sender = await event.get_sender()
    sender_name = sender.first_name

    oyun_dayandirildi = False

    # 1-ci Oyun (Məsələn: join_game ilə başlanan oyun)
    if chat_id in active_games:
        await stop_game(chat_id, f"🛑 Oyun {sender_name} tərəfindən sonlandırıldı.")
        oyun_dayandirildi = True

    # 2-ci Oyun (Məsələn: söz oyunu)
    elif chat_id in game_sessions and game_sessions[chat_id].get('active'):
        game_sessions[chat_id]['active'] = False
        oyun_dayandirildi = True

        if chat_id in player_scores and player_scores[chat_id]:
            top_player = max(player_scores[chat_id], key=player_scores[chat_id].get)
            top_score = player_scores[chat_id][top_player]
            try:
                top_user = await client.get_entity(top_player)
                top_name = top_user.first_name
            except:
                top_name = "Naməlum"

            await event.reply(
                f"📚 𝚆𝙾𝚁𝙳 𝙶𝙰𝙼𝙴 Oyunu Bitdi!\n\n"
                f"🏆 Ən yüksək xal: {top_name} - {top_score} xal\n\n"
                f"Yeni oyun üçün /oyun yazın! 🎮"
            )
        else:
            await event.reply("📚 𝚆𝙾𝚁𝙳 𝙶𝙰𝙼𝙴 oyunu Bitdi! Yeni oyun üçün /game yazın! 🎮")

    # Heç bir aktiv oyun yoxdursa
    if not oyun_dayandirildi:
        msg = await event.reply(f"ℹ️ Hörmətli {sender_name}, hal-hazırda aktiv oyun yoxdur.")
        await asyncio.sleep(4)
        try:
            await client.delete_messages(chat_id, [msg.id, event.id])
        except:
            pass
























  
                
