from pyrogram import Client, filters
from pyrogram.types import Message

from InflexMusic import app  # Bot instansiyası

# Admin olub-olmadığını yoxlayan funksiya
async def is_admin(user_id: int, chat_id: int) -> bool:
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False

# /pin əmri
@app.on_message(filters.command("pin") & filters.group)
async def pin_message(client: Client, message: Message):
    if not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")
    
    if not message.reply_to_message:
        return await message.reply("🔺 Zəhmət olmasa, hər hansısa mesaja cavab verin ✅")
    
    try:
        await client.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
        await message.reply_to_message.reply("📌 Mesaj sabitlənmişdir")
    except Exception:
        await message.reply("❌ Pin edilə bilmədi. Yetkiniz olmaya bilər.")

# /unpin əmri
@app.on_message(filters.command("unpin") & filters.group)
async def unpin_message(client: Client, message: Message):
    if not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")
    
    if not message.reply_to_message:
        return await message.reply("🔺 Zəhmət olmasa, hər hansısa mesaja cavab verin ✅")
    
    try:
        await client.unpin_chat_message(message.chat.id, message.reply_to_message.message_id)
        await message.reply_to_message.reply("✅ Mesaj pindən silindi")
    except Exception:
        await message.reply("❌ Pin silinə bilmədi. Yetkiniz olmaya bilər.")

# /unpinall əmri
@app.on_message(filters.command("unpinall") & filters.group)
async def unpin_all_messages(client: Client, message: Message):
    if not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")
    
    try:
        await client.unpin_all_chat_messages(message.chat.id)
        await message.reply("✅ Bütün pinlənmiş mesajlar silindi")
    except Exception:
        await message.reply("❌ Pinlər silinə bilmədi. Yetkiniz olmaya bilər.")
