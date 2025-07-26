from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from InflexMusic import app

# Söyüş kökləri və şəkilçilər
söyüşlər = ["sikdir", "qehbe", "qəhbə", "anavı", "cındır", "blət","blet", "sikim", "oğraş", "dalbayov","osduraq", "boynu", "nın", "vı","va", "s2m", "Dalbek", "dalben","qandon", "dişi", "fayşə", "faişə","qehbe", "təpdir", "siydir", "siyim","qehbe", "qəhbə", "vz", "vzqırt","kiwi", "oğlancıq", "bacını", "xirtəyini","boşalıram", "verirəm", "real", "virtual","çal", "banan", "gala", "uç","hamilə", "donbal", "Dombale", "Dombal" ]
söyüş_şəkilçilər = ["nın", "vı", "vu", "sər", "m", "un", "ni", "nı"]

aktiv_qruplar = {}

def söyüş_var(metin):
    metin = metin.lower().replace(" ", "")
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
    if aktiv_qruplar.get(message.chat.id):
        if message.text and söyüş_var(message.text):
            await message.delete()
            await message.reply(f"Hörmətli {message.from_user.mention} Zəhmət olmasa Etikdadan kənar Argo kəlmələr istifadə etməyək, Əks halda ban oluna bilərsiniz😊 ")
