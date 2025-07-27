import asyncio
import csv
import os
from datetime import datetime, timedelta
import pytz
from telethon import TelegramClient, events
from InflexMusic.core.bot import xaos as client 

# ---- BOT KONFİQURASİYASI ----

qruplar = set()
aktivlik = {}
baku_tz = pytz.timezone("Asia/Baku")


@client.on(events.NewMessage)
async def handle_messages(event):
    if event.is_private:
        return
    sender = await event.get_sender()
    if sender.bot:
        return

    chat_id = event.chat_id
    user_id = sender.id
    name = sender.first_name or "Naməlum"

    qruplar.add(chat_id)
    aktivlik.setdefault(chat_id, {})
    aktivlik[chat_id].setdefault(user_id, {"name": name, "count": 0})
    aktivlik[chat_id][user_id]["count"] += 1


def init_csv():
    if not os.path.exists("aktivlik.csv"):
        with open("aktivlik.csv", "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Qrup ID", "İstifadəçi", "Mesaj sayı", "Tarix"])


async def gunluk_hesabat():
    while True:
        # Növbəti 01:00 vaxtını hesabla
        indi = datetime.now(baku_tz)
        sabah = (indi + timedelta(days=1)).replace(hour=1, minute=0, second=0, microsecond=0)
        delta = (sabah - indi).total_seconds()
        print(f"⏳ Növbəti hesabat {sabah.strftime('%Y-%m-%d %H:%M:%S')} vaxtında göndəriləcək ({int(delta)} saniyə sonra)")

        await asyncio.sleep(delta)  # Növbəti 01:00-a qədər yat

        await hesabat_ve_csv()  # Hesabatı göndər

async def hesabat_ve_csv():
    for chat_id in list(qruplar):
        if chat_id not in aktivlik:
            continue

        istifadeciler = sorted(
            aktivlik[chat_id].items(),
            key=lambda item: item[1]["count"],
            reverse=True
        )

        toplam_mesaj = sum(info["count"] for _, info in istifadeciler)
        toplam_istifadeci = sum(1 for _, info in istifadeciler if info["count"] > 0)

        if toplam_istifadeci == 0:
            report = "📊 Bu gün heç kim mesaj yazmadı."
        else:
            report = "📊 Günlük ən aktiv 15 istifadəçi:\n\n"
            for i, (user_id, info) in enumerate(istifadeciler[:15], start=1):
                report += f"{i}. {info['name']} : {info['count']}\n"
            report += f"\nToplam aktiv istifadəçi: {toplam_istifadeci}\nToplam mesaj: {toplam_mesaj}"

        try:
            await client.send_message(chat_id, report)
        except Exception as e:
            print(f"Mesaj göndərilə bilmədi: {e}")

        tarix = datetime.now(baku_tz).strftime("%Y-%m-%d %H:%M:%S")
        with open("aktivlik.csv", "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            for _, info in istifadeciler:
                writer.writerow([chat_id, info["name"], info["count"], tarix])

        # Hesabdan sonra sıfırlanır
        for user in aktivlik[chat_id].values():
            user["count"] = 0


async def main():
    init_csv()
    asyncio.create_task(gunluk_hesabat())
    
    

    
    







