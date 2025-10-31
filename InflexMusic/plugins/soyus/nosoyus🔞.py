from pyrogram import Client, filters
from pyrogram.types import Message
from InflexMusic import app

qadağan_sözlər = [
    "sik", "sikdir", "peyser", "peysər", "oğras", "qəhbə", "qehbe", "anavi",
    "bacivi", "sikim", "dalbayov", "blət", "blet", "qələt",
    "pox", "heyvan", "varyox", "doğduğu", "bicbala", "bicok", "ble", "blə", "pesi",
    "cındır", "cindir", "ogras", "nənəvi", "seks", "sikis"
]

@app.on_message(filters.text & filters.group)
async def check_and_delete(client: Client, message: Message):
    lower_text = message.text.lower()

    # Mesajı sözlərə bölürük (nöqtə, vergül və s. nəzərə alınmasın deyə)
    import re
    sözlər = re.findall(r"\b\w+\b", lower_text)

    for soz in qadağan_sözlər:
        if soz in sözlər:  # Yalnız tam uyğun gələn söz varsa
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
