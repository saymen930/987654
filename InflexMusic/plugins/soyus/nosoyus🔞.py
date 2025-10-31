from pyrogram import Client, filters
from pyrogram.types import Message
from InflexMusic import app
import re

# 🔒 Söyüş siyahısı
qadağan_sözlər = [
    "sik", "sikdir", "peyser", "peysər", "oğras", "qəhbə", "qehbe", "anavi",
    "bacivi", "sikim", "dalbayov", "blət", "blet", "qələt",
    "pox", "heyvan", "varyox", "doğduğu", "bicbala", "bicok", "ble", "blə", "pesi",
    "cındır", "cindir", "ogras", "nənəvi", "seks", "sikis"
]

# 🔧 Qrup üçün filtr vəziyyəti (True = aktiv, False = deaktiv)
nosoyus_state = {}

# ✅ Komanda: /nosoyus
@app.on_message(filters.command("nosoyus", prefixes="/") & filters.group)
async def nosoyus_command(client: Client, message: Message):
    chat_id = message.chat.id
    args = message.command

    # Əgər komanda yalnız "/nosoyus" yazılıbsa
    if len(args) == 1:
        await message.reply_text(
            "⚠️ Zəhmət olmasa düzgün komandalardan istifadə et\n\n"
            "↪️ /nosoyus on  • funksiyasını açmaq\n"
            "↪️ /nosoyus off • funksiyanı bağlamaq ⚠️",
            quote=True
        )
        return

    arg = args[1].lower()

    if arg == "on":
        nosoyus_state[chat_id] = True
        await message.reply_text("✅ Söyüş filtri aktiv edildi!")
    elif arg == "off":
        nosoyus_state[chat_id] = False
        await message.reply_text("🚫 Söyüş filtri deaktiv edildi!")
    else:
        await message.reply_text(
            "⚠️ Zəhmət olmasa düzgün komandalardan istifadə et\n\n"
            "↪️ /nosoyus on  • funksiyasını açmaq\n"
            "↪️ /nosoyus off • funksiyanı bağlamaq ⚠️",
            quote=True
        )

# 🔍 Mesaj yoxlama funksiyası
@app.on_message(filters.text & filters.group)
async def check_and_delete(client: Client, message: Message):
    chat_id = message.chat.id

    # Əgər bu qrupda filtr aktiv deyilsə, heç nə etmə
    if not nosoyus_state.get(chat_id, False):
        return

    lower_text = message.text.lower()
    sözlər = re.findall(r"\b\w+\b", lower_text)

    for soz in qadağan_sözlər:
        if soz in sözlər:
            try:
                await message.delete()
                print(f"Silindi: {message.text}")

                username = message.from_user.username
                if username:
                    name = f"@{username}"
                else:
                    name = message.from_user.first_name or "İstifadəçi"

                warning_text = f"{name}, qrupumuzda argo ifadə işlətmək qadağandır ⛔"
                await message.reply(warning_text)
            except Exception as e:
                print(f"Silmək mümkün olmadı: {e}")
            break
