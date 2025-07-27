import asyncio
import random
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.channels import GetParticipantsRequest, GetParticipantRequest
from telethon.tl.types import ChannelParticipantsSearch, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.tl.types import PeerChannel, PeerChat
from telethon.tl.custom import Button
import os
from dotenv import load_dotenv

load_dotenv()

active_tags = {}

support_buttons = [
    [Button.url("📥 Support", "https://t.me/PersionalSupport")],
    [Button.url("➕ Qrupuna Əlavə et", "https://t.me/PersionalMultiBot?startgroup=true")]
]

# Admin yoxlaması funksiyası
async def is_admin(chat_id, user_id):
    try:
        participant = await bot(GetParticipantRequest(chat_id, user_id))
        if isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
            return True
    except:
        pass
    return False

# Qrup üzvlərini əldə et
async def get_members(chat):
    users = []
    offset = 0
    limit = 100
    while True:
        participants = await bot(GetParticipantsRequest(
            channel=chat,
            filter=ChannelParticipantsSearch(''),
            offset=offset,
            limit=limit,
            hash=0
        ))
        if not participants.users:
            break
        for user in participants.users:
            if not user.bot:
                users.append(user)
        offset += len(participants.users)
    return users

# Tağlama funksiyası
async def tag_users(event, msg, users, tag_type="normal"):
    chat_id = event.chat_id
    user = (await event.get_sender()).first_name
    active_tags[chat_id] = True

emojis = ["🌟", "🎉", "😍", "✨", "💫", "🦄", "🍀", "🎈", "🤩", "🌈", "🍎", "🎵", "🐱", "🏆", "🌻",  
          "🐶", "🍕", "🚗", "🧩", "🎤", "📚", "🎬", "🌊", "🎮", "🥳", "🎁", "🦋", "🍩", "🎸",  
          "🌼", "🍓", "🐰", "🚴‍♂️", "🎯", "🕺", "🦊", "🍉", "🎧", "🏀", "🌙", "🐬", "🎹",  
          "🍔", "🏝️", "🐻", "🚀", "🛹", "🎂", "🐝", "🌹", "🍦", "🎺", "🐯", "🥂", "🏄‍♀️",  
          "🌺", "🐨", "🍰", "🎻", "🌞"]  
    love_msgs = [  
    "❤️ Səni sevirik", "💘 Qəlbimiz səninlə", "💋 Ən dəyərlimiz", "💕 Salam gözəl insan", "💖 Unudulmadın",  
    "💛 Sən bizim üçün", "💙 Dostluq əbədi", "💚 Hər zaman yanında", "💜 Sevgi dolu", "🧡 Gülüşün işıqdır",  
    "💝 Səninlə xoşbəxtik", "💞 Ürəyimiz birlikdə", "💓 Sonsuz məhəbbət", "💗 İnanırıq sənə", "💟 Hər zaman varsan",  
    "💌 Sevgiylə dolu", "🥰 Gözəlliyinlə parılda", "😘 Sən çox özəlsən", "😍 Həyatımızın rəngi", "🥳 Sən bizim sevincimiz",  
    "🎉 Gülümse hər zaman", "🌹 Sən baharımız", "🌸 Sevdiyimiz insan", "🌻 Sənə hər şey gözəl", "🌼 Dostluq bağımız",  
    "🌟 Ulduzumuz parlaq", "✨ Sən ən qiymətlisən", "🎈 Sevgi ilə dolu", "🎀 Sənin üçün buradayıq", "🎁 Hədiyyəmiz sənsən",  
    "🍀 Şanslıyıq səninlə", "🎶 Hər notda sən", "🐾 Yolumuz sənlə", "🕊️ Sülh və sevgi", "💫 Hər an yanında",  
    "🌈 Həyatın rəngi sən", "💐 Gözəl arzular", "🌺 Sənə sonsuz sevgi", "🐝 Hər zaman işıqlı", "🦋 Gözəl ruhlu",  
    "🍓 Sənin gülüşün", "🍉 Hər şeyin ən gözəli", "🥂 Xoşbəxtlik sənlə", "🏆 Qələbə bizimlə", "🚀 Hədəflər birlikdə",  
    "🎯 Dəqiqlik və sevgi", "🎤 Sənin səsin", "🎬 Həyatımızın filmi", "📚 Bilgi və sevgi", "🧩 Birlikdə tam",  
    "🎮 Oyun və həyat", "🍔 Dadlı anlar", "🏄‍♀️ Dalğalar kimi", "🚴‍♂️ Hərəkət dolu", "🐯 Güclü və cəsur",  
    "🐨 Yumşaq ürək", "🦊 Zərif və çevik", "🐻 Dostluq simvolu", "🐶 Sadiq yoldaş", "🐱 Sevimli dost",  
    "🎂 Xoş anlar", "🍰 Şirin xatirələr", "🎸 Musiqi və sevgi", "🎹 Hər not sevgi dolu", "🎺 Hər gün bayram",  
    "🌞 Günəş işığı", "🌙 Gecənin səması", "🌊 Dəniz kimi dərin", "🏝️ Sakit və gözəl", "🛹 Həyat sürəti",  
    "🥳 Bayram hər gün", "💃 Rəqs və sevinc", "🕺 Hər addım güclü", "🎯 Məqsədə çat", "🎉 Həyatı qeyd et."  
]  
    await event.reply(f"Tag prosesi başlandı ✅\nİcraçı 🥷 {user}", buttons=support_buttons)

    count = 0
    for i in range(0, len(users), 5):
        if not active_tags.get(chat_id, False):
            break

        mention = " ".join([f"[{u.first_name}](tg://user?id={u.id})" for u in users[i:i+5]])

        if tag_type == "emoji":
            send_text = f"{random.choice(emojis)} {msg}\n\n{mention}"
        elif tag_type == "love":
            send_text = f"{random.choice(love_msgs)} 💌\n\n{mention}"
        else:
            send_text = f"{msg}\n\n{mention}"

        await event.reply(send_text, parse_mode='markdown')
        count += len(users[i:i+5])
        await asyncio.sleep(2)

    await event.reply(f"Tag prosesi bitdi ✅\nTag edilənlər sayı🔢 {count}", buttons=support_buttons)
    active_tags[chat_id] = False

# Əmr funksiyaları
@bot.on(events.NewMessage(pattern="/tag"))
async def handler_tag(event):
    if not event.is_group:
        return await event.reply("Bu əmr yalnız qruplarda işləyir.", buttons=support_buttons)

    if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("❌ Bu əmrdən yalnız adminlər istifadə edə bilər.", buttons=support_buttons)

    args = event.raw_text.split(" ", 1)
    if len(args) < 2:
        return await event.reply("❗İstifadə: /tag mesaj")
    users = await get_members(event.chat_id)
    await tag_users(event, args[1], users)

@bot.on(events.NewMessage(pattern="/tektag"))
async def handler_tektag(event):
    if not event.is_group:
        return await event.reply("Bu əmr yalnız qruplarda işləyir.", buttons=support_buttons)

    if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("❌ Bu əmrdən yalnız adminlər istifadə edə bilər.", buttons=support_buttons)

    args = event.raw_text.split(" ", 1)
    if len(args) < 2:
        return await event.reply("❗İstifadə: /tektag mesaj")
    users = await get_members(event.chat_id)
    chat_id = event.chat_id
    sender = await event.get_sender()
    active_tags[chat_id] = True

    await event.reply(f"Təkli tag prosesi başlandı ✅\n🥷 İcraçı {sender.first_name}", buttons=support_buttons)

    count = 0
    for u in users:
        if not active_tags.get(chat_id, False):
            break
        await event.reply(f"{args[1]}\n\n[{u.first_name}](tg://user?id={u.id})", parse_mode="markdown")
        count += 1
        await asyncio.sleep(1.5)

    await event.reply(f"Təkli tag prosesi bitdi ✅\nTag edilənlər sayı🔢 {count}", buttons=support_buttons)
    active_tags[chat_id] = False

@bot.on(events.NewMessage(pattern="/etag"))
async def handler_etag(event):
    if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("❌ Bu əmrdən yalnız adminlər istifadə edə bilər.", buttons=support_buttons)
    users = await get_members(event.chat_id)
    await tag_users(event, "Buradasızmı?", users, tag_type="emoji")

@bot.on(events.NewMessage(pattern="/stag"))
async def handler_stag(event):
    if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("❌ Bu əmrdən yalnız adminlər istifadə edə bilər.", buttons=support_buttons)
    users = await get_members(event.chat_id)
    await tag_users(event, "Sevgilərimizlə ❤️", users, tag_type="love")

@bot.on(events.NewMessage(pattern="/atag"))
async def handler_atag(event):
    if not await is_admin(event.chat_id, event.sender_id):
        return await event.reply("❌ Bu əmrdən yalnız adminlər istifadə edə bilər.", buttons=support_buttons)
    # yalnız adminləri topla
    all_users = await get_members(event.chat_id)
    admins = []
    for u in all_users:
        if await is_admin(event.chat_id, u.id):
            admins.append(u)
    await tag_users(event, "🔔 Admin tag!", admins)

@bot.on(events.NewMessage(pattern="/dayan|/cancel"))
async def stop_tagging(event):
    active_tags[event.chat_id] = False
    await event.reply("Tag Prosesi dayandırıldı 🛑", buttons=support_buttons)
