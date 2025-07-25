import asyncio
import random
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from InflexMusic import app  # Sənin layihə modulu

load_dotenv()

active_tags = {}

support_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("📥 Support", url="https://t.me/PersionalSupport")],
    [InlineKeyboardButton("➕ Qrupuna Əlavə et", url="https://t.me/PersionalMultiBot?startgroup=true")]
])


async def get_members(client, chat_id, admins_only=False):
    members = []
    async for member in client.get_chat_members(chat_id):
        if member.user.is_bot:
            continue
        if admins_only and member.status not in ("administrator", "creator"):
            continue
        members.append(member.user)
    return members


async def tag_users(client, message, msg, users, tag_type="normal"):
    chat_id = message.chat.id
    user = message.from_user.first_name
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

    await message.reply(f"Tag prosesi başlandı ✅\nİcraçı 🥷 {user}", reply_markup=support_keyboard)

    count = 0
    for i in range(0, len(users), 5):
        if not active_tags.get(chat_id, False):
            break

        mention = " ".join([f"[{u.first_name}](tg://user?id={u.id})" for u in users[i:i + 5]])

        if tag_type == "emoji":
            send_text = f"{random.choice(emojis)} {msg}\n\n{mention}"
        elif tag_type == "love":
            send_text = f"{random.choice(love_msgs)} 💌\n\n{mention}"
        else:
            send_text = f"{msg}\n\n{mention}"

        await message.reply(send_text, parse_mode=ParseMode.MARKDOWN)
        count += len(users[i:i + 5])
        await asyncio.sleep(2)

    await message.reply(f"Tag prosesi bitdi ✅\nTag edilənlər sayı🔢 {count}", reply_markup=support_keyboard)
    active_tags[chat_id] = False


@app.on_message(filters.command("tag") & filters.group)
async def tag_command(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        return await message.reply("❗İstifadə: /tag mesaj")
    users = await get_members(client, message.chat.id)
    await tag_users(client, message, args[1], users)


@app.on_message(filters.command("tektag") & filters.group)
async def tektag_command(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        return await message.reply("❗İstifadə: /tektag mesaj")
    users = await get_members(client, message.chat.id)
    chat_id = message.chat.id
    user = message.from_user.first_name
    active_tags[chat_id] = True
    await message.reply(f"Təkli tag prosesi başlandı ✅\n🥷 İcraçı {user}", reply_markup=support_keyboard)

    count = 0
    for u in users:
        if not active_tags.get(chat_id, False):
            break
        await message.reply(f"{args[1]}\n\n[{u.first_name}](tg://user?id={u.id})", parse_mode=ParseMode.MARKDOWN)
        count += 1
        await asyncio.sleep(1.5)

    await message.reply(f"Təkli tag prosesi bitdi ✅\nTag edilənlər sayı🔢 {count}", reply_markup=support_keyboard)
    active_tags[chat_id] = False


@app.on_message(filters.command("atag") & filters.group)
async def atag_command(client, message):
    users = await get_members(client, message.chat.id, admins_only=True)
    if not users:
        return await message.reply("Bu qrupda admin tapılmadı!")
    await tag_users(client, message, "🔔 Admin tag!", users)


@app.on_message(filters.command("etag") & filters.group)
async def etag_command(client, message):
    users = await get_members(client, message.chat.id)
    await tag_users(client, message, "Buradasızmı?", users, tag_type="emoji")


@app.on_message(filters.command("stag") & filters.group)
async def stag_command(client, message):
    users = await get_members(client, message.chat.id)
    await tag_users(client, message, "Sevgilərimizlə ❤️", users, tag_type="love")


@app.on_message(filters.command(["stop", "cancel"]) & filters.group)
async def stop_command(client, message):
    chat_id = message.chat.id
    active_tags[chat_id] = False
    await message.reply("Tag Prosesi dayandırıldı 🛑", reply_markup=support_keyboard)


# ------- PRIVATE YOXLAMASI -------

@app.on_message(filters.command(["tag", "tektag", "atag", "etag", "stag"]) & filters.private)
async def tag_commands_private(client, message):
    await message.reply(
        "🛡️ Sahibim tağ əmrini yalnız qruplar üçün nəzərdə tutub 🙎",
        reply_markup=support_keyboard
    )


@app.on_message(filters.command(["stop", "cancel"]) & filters.private)
async def stop_command_private(client, message):
    await message.reply(
        "🛡️ Sahibim tağ əmrini yalnız qruplar üçün nəzərdə tutub 🙎",
        reply_markup=support_keyboard
    )
