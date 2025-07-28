from InflexMusic.core.bot import xaos as bot
import asyncio
import config
from telethon import TelegramClient, events
from telethon.tl.types import PeerUser



# 📩 Komanda işləyici
@bot.on(events.NewMessage(pattern=r'^[/|.]report(?:\s+(.+))?', incoming=True))
async def warn_handler(event):
    if event.is_private or event.is_group or event.is_channel:
        sender = await event.get_sender()
        username = sender.username or "Yoxdur"
        user_mention = f"[{sender.first_name}](tg://user?id={sender.id})"

        reason = event.pattern_match.group(1)
        if not reason:
            await event.reply(f"💁 {user_mention} Zəhmət olmasa şikayət və ya təklifinizi yazın.")
            return

        msg = f"🤵 Ad - {user_mention}\n🛑 Tag - @{username}\n👁️‍🗨️ ID - {sender.id}\n\n💬 İrad və ya təklif:\n⭕ {reason}"

        # Kanala və sahiblərə göndər
        await bot.send_message(config.C_WARN, msg)
        for owner_id in config.OWNER_IDS:
            await bot.send_message(PeerUser(owner_id), f"📬 Yeni xəbərdarlıq gəldi:\n\n{msg}")

        # Cavab mesajı
        reply = await event.reply("✅ Mesajınız kanala və sahiblərə göndərildi. Təşəkkürlər 🥰.")

        # 5 saniyə gözlə və hər iki mesajı sil
        await asyncio.sleep(5)
        await bot.delete_messages(event.chat_id, [event.id, reply.id])

