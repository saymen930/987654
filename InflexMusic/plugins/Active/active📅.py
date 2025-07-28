import asyncio
from telethon import TelegramClient, events, Button
from datetime import datetime
from collections import defaultdict
import pytz
from InflexMusic.core.bot import xaos as client  # Telethon bot instance
import config

# 🧠 Qrup statistikası
group_stats = defaultdict(lambda: defaultdict(lambda: {'name': '', 'count': 0}))

# 🕓 Bakı saat qurşağı
baku_tz = pytz.timezone("Asia/Baku")

# 📨 Mesaj izləmə
@client.on(events.NewMessage)
async def handler(event):
    if event.is_group:
        if event.sender_id and not event.sender.bot:
            group_id = event.chat_id
            sender = await event.get_sender()
            full_name = sender.first_name or ""
            if sender.last_name:
                full_name += f" {sender.last_name}"
            user_id = sender.id
            group_stats[group_id][user_id]['name'] = full_name
            group_stats[group_id][user_id]['count'] += 1

# 🕔 Gündəlik aktive saati üçün yoxlayıcı funksiya
async def daily_stats_sender():
    while True:
        now = datetime.now(baku_tz)
        if now.hour == 19 and now.minute == 14:
            for group_id, user_data in group_stats.items():
                if not user_data:
                    continue

                total_messages = sum(info['count'] for info in user_data.values())
                active_users = len(user_data)
                top_users = sorted(user_data.items(), key=lambda x: x[1]['count'], reverse=True)[:15]

                # 📆 Tarix və Qrup Adı
                date_str = now.strftime("%d/%m/%Y")
                try:
                    chat = await client.get_entity(group_id)
                    group_name = chat.title or "Qrup"
                except:
                    group_name = "Qrup"

                msg = f"📊 <b>{group_name} üçün ən aktiv 15 istifadəçi:</b>\n\nİstifadəçi --> Mesaj\n"
                for idx, (user_id, info) in enumerate(top_users, start=1):
                    name = info['name']
                    count = info['count']
                    profile_link = f'<a href="tg://user?id={user_id}">{name}</a>'
                    msg += f"{idx}. {profile_link} : {count}\n"

                msg += (
                    f"\n📊 <i>Bu sıralama {date_str} tarixi üçündür.</i>\n"
                    f"├ Toplam aktiv istifadəçi: {active_users}\n"
                    f"└ Toplam mesaj: {total_messages}"
                )

                buttons = [
                    [Button.url("🔮 Yeniliklər", f"{config.SPORT_K}"),
                     Button.url("🔗 Qrupa Əlavə Et", f"https://t.me/{config.BOT_USERNAME}?startgroup=new")]
                ]

                try:
                    await client.send_message(group_id, msg, parse_mode='html', buttons=buttons)
                except Exception as e:
                    print(f"Mesaj göndərilə bilmədi ({group_id}): {e}")

            group_stats.clear()
            await asyncio.sleep(60)
        await asyncio.sleep(5)

# 🚀 Botu başladın
async def main():
    print("✅ Bot Bakı vaxtı ilə 17:05 üçün hazırdır.")
    await daily_stats_sender()

with client:
    client.loop.create_task(main())
    client.run_until_disconnected()
