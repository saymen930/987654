import json
import requests
from telethon import events
from InflexMusic.core.bot import xaos as client  # səndə necədirsə onu istifadə et

API_URL = "https://aicodegenerator.ifscswiftcodeapp.in/api.php"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# /ai, .ai, !ai, @ai ...
@client.on(events.NewMessage(pattern=r"^[!/\.@]ai(?:\s+(.+))?$"))
async def ai_command(event: events.NewMessage.Event):
    user_input = (event.pattern_match.group(1) or "").strip()

    if not user_input:
        return await event.reply(
            "✍️ Zəhmət olmasa /ai əmri ilə sualınızı yazın.\n"
            "Məsələn: `/ai Python nədir?`",
            parse_mode="md"
        )

    # Pyrogram-da etdiyin kimi /ai -> /gemini string dəyişimi (əslində lazım deyil,
    # amma eyni davranışı saxlamaq üçün qoyuram)
    user_input = user_input.replace("/ai", "/gemini", 1)

    try:
        resp = requests.post(
            API_URL,
            headers=HEADERS,
            json={
                "message": [{"type": "text", "text": user_input}],
                "chatId": str(event.chat_id),
                "generatorType": "CodeGenerator"
            },
            timeout=10
        )

        if resp.status_code == 200:
            try:
                data = resp.json()
                reply_text = data.get("response", "⚠️ Cavab tapılmadı.")
            except json.JSONDecodeError:
                reply_text = "⚠️ JSON cavabı alınmadı."
        else:
            reply_text = f"⚠️ Server xətası: {resp.status_code}"

    except requests.exceptions.RequestException as e:
        reply_text = f"❌ Sorğu zamanı xəta baş verdi:\n{e}"

    await event.reply(reply_text)
