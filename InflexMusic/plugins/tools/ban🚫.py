from pyrogram import Client, filters
from pyrogram.types import Message
from InflexMusic import app  # Sənin bot instansın

# Admin yoxlama funksiyası
async def is_admin(client: Client, user_id: int, chat_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in ("administrator", "creator")
    except:
        return False

# 🚫 Ban əmri
@app.on_message(filters.command("ban") & filters.group)
async def ban_user(client: Client, message: Message):
    if not await is_admin(client, message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")

    user = message.reply_to_message.from_user if message.reply_to_message else None

    if not user and len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            return await message.reply("❌ İstifadəçi tapılmadı.")

    if not user:
        return await message.reply("🔺 İstifadə: /ban (reply) və ya /ban <ID/@username>")

    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await message.reply(f"🚫 {user.mention} qrupdan banlandı.")
    except Exception as e:
        await message.reply(f"❌ Ban edilə bilmədi.\n`{e}`")

# ✅ Unban əmri
@app.on_message(filters.command("unban") & filters.group)
async def unban_user(client: Client, message: Message):
    if not await is_admin(client, message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")

    user = message.reply_to_message.from_user if message.reply_to_message else None

    if not user and len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            return await message.reply("❌ İstifadəçi tapılmadı.")

    if not user:
        return await message.reply("🔺 İstifadə: /unban (reply) və ya /unban <ID/@username>")

    try:
        await client.unban_chat_member(message.chat.id, user.id)
        await message.reply(f"✅ {user.mention} üçün qadağa ləğv edildi.")
    except Exception as e:
        await message.reply(f"❌ Qadağa silinə bilmədi.\n`{e}`")
