from pyrogram import filters
from pyrogram.types import Message
import re
from InflexMusic import app

# Söyüş siyahısı
söyüşlər = [
    "sikdir", "qehbe", "qəhbə", "anavı", "cındır", "blət", "blet",
    "sikim", "oğraş", "dalbayov", "osduraq", "boynu", "nın", "vı", "va",
    "s2m", "dalbek", "dalben", "qandon", "dişi", "fayşə", "faişə",
    "təpdir", "siydir", "siyim", "vz", "vzqırt", "kiwi", "oğlancıq",
    "bacını", "xirtəyini", "boşalıram", "verirəm", "real", "virtual",
    "çal", "banan", "gala", "uç", "hamilə", "donbal", "dombale", "dombal"
]
söyüş_şəkilçilər = ["nın", "vı", "vu", "sər", "m", "un", "ni", "nı"]

aktiv_qruplar = {}

# Söyüş yoxlama funksiyası
def söyüş_var(metin: str) -> bool:
    if not metin:
        return False
    metin = metin.lower()
    metin = re.sub(r"[^a-zA-Z0-9əöğıüşıçƏÖĞİÜŞİÇ]+", "", metin)
    for söz in söyüşlər:
        if söz in metin:
            return True
        for şəkilçi in söyüş_şəkilçilər:
            if f"{söz}{şəkilçi}" in metin:
                return True
    return False

# Noargo komandı – aktiv/deaktiv
@app.on_message(filters.command("noargo") & filters.group)
async def toggle_no_söyüş(_, message: Message):
    if not message.text:
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("✅ İstifadə: `/noargo yes` və ya `/noargo no`")

    seçim = parts[1].lower()
    if seçim == "yes":
        aktiv_qruplar[message.chat.id] = True
        await message.reply("🔒 **No Söyüş** funksiyası aktiv edildi.")
    elif seçim == "no":
        aktiv_qruplar.pop(message.chat.id, None)
        await message.reply("🔓 **No Söyüş** funksiyası deaktiv edildi.")
    else:
        await message.reply("❗Yanlış seçim. `/noargo yes` və ya `/noargo no` yazın.")

# Hər mesajı yoxlayır (əgər aktivdirsə)
@app.on_message(filters.group & ~filters.command("noargo"))
async def söyüş_yoxla(_, message: Message):
    if not aktiv_qruplar.get(message.chat.id):
        return

    text = message.text or message.caption
    if not text:
        return

    if söyüş_var(text):
        try:
            await message.delete()
            await message.reply(
                f"🚫 Hörmətli {message.from_user.mention}, zəhmət olmasa söyüş işlətməyin. Əks halda tədbir görülə bilər."
            )
        except Exception as e:
            print(f"[XƏTA] Mesaj silinə bilmədi: {e}")
