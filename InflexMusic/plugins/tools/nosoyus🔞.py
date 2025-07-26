from pyrogram import Client, filters
from pyrogram.types import Message

qadağan_sözlər = [
    "sik", "sikdir", "peyser", "peysər", "oğras", "qəhbə", "qehbe", "anavi",
    "Bacivi", "nin", "sikim", "dalbayov", "blət", "blet", "qələt",
    "Pox", "heyvan", "varyox", "doğduğu", "bicbala", "bicok", "ble", "blə", "pesi", "cındır", "cindir", "ogras", "nənəvi"
]
@app.on_message(filters.text & filters.group)
async def check_and_delete(client: Client, message: Message):
    lower_text = message.text.lower()
    for soz in qadağan_sözlər:
        if soz in lower_text:
            try:
                await message.delete()
                print(f"Silindi: {message.text}")
                username = message.from_user.username
                if username:
                    name = f"@{username}"
                else:
                    name = message.from_user.first_name or "İstifadəçi"
                
                warning_text = f"{name} qrupumuzda argo verici kəlmə işlətmək qadağandır ⛔"
                await message.reply(warning_text)
            except Exception as e:
                print(f"Silmək mümkün olmadı: {e}")
            break
