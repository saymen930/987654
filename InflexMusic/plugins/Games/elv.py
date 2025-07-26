
from pyrogram import filters
from InflexMusic.core.bot import pls as app
import config

DATA_FILES = {
    "custom_words": "Jason/custom_words.json",
    "scores": "Jason/scores.json",
    "stats": "Jason/stats.json"
}


custom_words = load_json(DATA_FILES["custom_words"])
scores = load_json(DATA_FILES["scores"])
stats = load_json(DATA_FILES["stats"])





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
      



@app.on_message(filters.command(["game", "join", "unjoin", "joinup", "stop"]) & filters.private)
async def tag_commands_private(client, message):
    await message.reply(
        "🛡️ Əmrir yalnız qruplar üçün nəzərdə tutub 🙎"
    )
  
