
from pyrogram import filters
from pyrogram.types import Message
import re
from InflexMusic import app  # Sənin bot instance-ın

# Söyüş kökləri və şəkilçilər
söyüşlər = [
    "sikdir", "qehbe", "qəhbə", "anavı", "cındır", "blət", "blet",
    "sikim", "oğraş", "dalbayov", "osduraq", "boynu", "nın", "vı", "va",
    "s2m", "Dalbek", "dalben", "qandon", "dişi", "fayşə", "faişə", "qehbe",
    "təpdir", "siydir", "siyim", "qehbe", "qəhbə", "vz", "vzqırt", "kiwi",
    "oğlancıq", "bacını", "xirtəyini", "boşalıram", "verirəm", "real",
    "virtual", "çal", "banan", "gala", "uç", "hamilə", "donbal", "Dombale", "Dombal"
]
söyüş_şəkilçilər = ["nın", "vı", "vu", "sər", "m", "un", "ni", "nı"]

# Aktiv qrupların chat_id-lərini saxlayır
aktiv_qruplar = {}

def söyüş_var(metin: str) -> bool:
    if not metin:
        return False
    metin = metin.lower()
    # Mətnin içindən hərf və rəqəmlərdən başqa simvolları silirik
    metin = re.sub(r"[^a-zA-Z0-9əöğıüşıçƏÖĞİÜŞİÇ]+", "", metin)

    for söz in söyüşlər:
        if söz in metin:
            return True
        for şəkilçi in söyüş_şəkilçilər:
            if f"{söz}{şəkilçi}" in metin:
                return True
    return False

@app.on_message(filters.command("noargo") & filters.group)
async def toggle_no_söyüş(_, message: Message):
    if len(message.command) < 2:
        await message.reply("İstifadə: /noargo yes və ya /noargo no")
        return

    cmd = message.command[1].lower()
    if cmd == "yes":
        aktiv_qruplar[message.chat.id] = True
        await message.reply("No söyüş funksiyası artıq **aktiv edildi**.")
    elif cmd == "no":
        aktiv_qruplar.pop(message.chat.id, None)
        await message.reply("No söyüş funksiyası artıq **deaktiv edildi**.")
    else:
        await message.reply("Yanlış seçim, /noargo yes və ya /noargo no yaz.")

@app.on_message(filters.group & ~filters.command("noargo"))
async def söyüş_yoxla(_, message: Message):
    if not aktiv_qruplar.get(message.chat.id):
        return  # Funksiya yalnız aktiv qruplarda işləyir

    text = message.text or message.caption
    if not text:
        return  # Mətn yoxdursa yoxla

    if söyüş_var(text):
        try:
            await message.delete()
            await message.reply(
                f"Hörmətli {message.from_user.mention}, zəhmət olmasa etikdan kənar argo kəlmələr istifadə etməyək, "
                "əks halda ban oluna bilərsiniz 😊"
            )
        except Exception as e:
            print(f"[NoArgo] Mesajı silmək mümkün olmadı: {e}")

