from pyrogram import Client, filters
from pyrogram.types import Message
from InflexMusic import app

async def is_admin(user_id: int, chat_id: int) -> bool:
    member = await app.get_chat_member(chat_id, user_id)
    return member.status in ("administrator", "creator")

@app.on_message(filters.command("pin") & filters.group)
async def pin(_, message: Message):
    if not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Admin deyilsiniz.")
    if not message.reply_to_message:
        return await message.reply("⚠️ Cavab olaraq bir mesaj seçin.")
    try:
        await app.pin_chat_message(
            chat_id=message.chat.id,
            message_id=message.reply_to_message.message_id,
            disable_notification=True
        )
        await message.reply("📌 Sabitlədim.")
    except Exception as e:
        await message.reply(f"Xəta: `{e}`")

@app.on_message(filters.command("unpin") & filters.group)
async def unpin(_, message: Message):
    if not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Admin deyilsiniz.")
    if not message.reply_to_message:
        return await message.reply("⚠️ Cavab olaraq bir mesaj seçin.")
    try:
        await app.unpin_chat_message(
            chat_id=message.chat.id,
            message_id=message.reply_to_message.message_id
        )
        await message.reply("✅ Pindən çıxartdım.")
    except Exception as e:
        await message.reply(f"Xəta: `{e}`")

@app.on_message(filters.command("unpinall") & filters.group)
async def unpin_all(_, message: Message):
    if not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Admin deyilsiniz.")
    try:
        await app.unpin_all_chat_messages(message.chat.id)
        await message.reply("✅ Bütün pinlər silindi.")
    except Exception as e:
        await message.reply(f"Xəta: `{e}`")
