import random
from telethon import events
from InflexMusic.core.bot import xaos as client  # səndə necədirsə onu istifadə et

ESQ_FAIZ = [
    "17","18","20","22","24","25","27","29","30","31","33","35","36","39","40",
    "42","43","45","47","49","50","55","56","57","58","60","62","64","65","66",
    "68","70","72","74","75","77","79","80","82","84","85","87","89","90","92",
    "93","95","97","98","99","100"
]

def mention(user):
    name = (user.first_name or "User").replace("[", "").replace("]", "")
    return f"[{name}](tg://user?id={user.id})"

# .esq / !esq @esq /eşq və s. – hamısını qəbul edir
@client.on(events.NewMessage(pattern=r"^[./!@]?(?:esq|eşq)$"))
async def esq_handler(event: events.NewMessage.Event):
    try:
        # Cavablanmış mesaja tələb var
        if not event.is_reply:
            return await event.reply("✔ Bu əmri birinin mesajına yanıt verərək istifadə edin.")

        reply = await event.get_reply_message()

        # Forward olunmuş mesaja icazə vermirik
        if getattr(reply, "fwd_from", None):
            return await event.reply("⚠️ **XƏTA**\n🚫 Bu əmri forward olunmuş mesajlara qarşı istifadə etmək olmaz.")

        u1 = await event.get_sender()
        u2 = await reply.get_sender()

        percent = random.choice(ESQ_FAIZ)
        text = (
            "Eşq Faizi Hesablandı\n\n"
            f"{mention(u2)} + {mention(u1)} = ❤\n"
            f"Eşq Faizi: **{percent}%**"
        )
        await event.reply(text, parse_mode="md")

    except Exception:
        await event.reply("⚠️ **XƏTA**")
