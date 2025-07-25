from pyrogram import Client, filters
from pyrogram.types import Message
from InflexMusic import app


async def is_admin(user_id: int, chat_id: int) -> bool:
    member = await app.get_chat_member(chat_id, user_id)
    return member.status in ("administrator", "creator")


@app.on_message(filters.command("pin") & filters.group)
async def pin(client: Client, message: Message):
    if not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Sizin admin olduğunuzu görmürəm...")
    if not message.reply_to_message:
        return await message.reply("🔺 Zəhmət olmasa, bir mesaja cavab verin ✅")

    try:
        await client.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
        await message.reply("📌 Bir mesajı sabitlədim...")
    except Exception as e:
        await message.reply(f"❌ Pin edilə bilmədi: {e}")

@app.on_message(filters.command("unpin") & filters.group)
async def unpin(client: Client, message: Message):
    if not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Sizin admin olduğunuzu görmürəm...")
    if not message.reply_to_message:
        return await message.reply("🔺 Zəhmət olmasa, bir mesaja cavab verin ✅")

    try:
        await client.unpin_chat_message(message.chat.id, message.reply_to_message.message_id)
        await message.reply("✅ Bir mesajı pindən sildim")
    except Exception as e:
        await message.reply(f"❌ Pin silinə bilmədi: {e}")

@app.on_message(filters.command("unpinall") & filters.group)
async def unpin_all(client: Client, message: Message):
    if not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Sizin admin olduğunuzu görmürəm...")

    try:
        await client.unpin_all_chat_messages(message.chat.id)
        await message.reply("✅ Bütün sabitləmələr silindi")
    except Exception as e:
        await message.reply(f"❌ Bütün pinlər silinə bilmədi: {e}")
