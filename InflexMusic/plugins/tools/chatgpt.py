import requests
from InflexMusic import app
from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import json
import logging



@app.on_message(filters.command("ai"))
async def ai_command(client: Client, message: Message):
    user_input = message.text.replace("/ai", "/gemini", 1).strip()

    if not user_input:
        await message.reply("✍️ Zəhmət olmasa /ai və ya /gemini əmri ilə sualınızı yazın.\nMəsələn: `/ai Python nədir?`")
        return

    try:
        response = requests.post(
            "https://aicodegenerator.ifscswiftcodeapp.in/api.php",
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            },
            json={
                "message": [{"type": "text", "text": user_input}],
                "chatId": str(message.chat.id),
                "generatorType": "CodeGenerator"
            },
            timeout=10
        )

        if response.status_code == 200:
            try:
                data = response.json()
                reply_text = data.get("response", "⚠️ Cavab tapılmadı.")
            except json.JSONDecodeError:
                reply_text = "⚠️ JSON cavabı alınmadı."
        else:
            reply_text = f"⚠️ Server xətası: {response.status_code}"

    except requests.exceptions.RequestException as e:
        reply_text = f"❌ Sorğu zamanı xəta baş verdi:\n{e}"

    await message.reply(reply_text)

# ▶️ Botu işə salırıq
