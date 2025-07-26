from pyrogram import Client, filters
from pyrogram.types import Message
from InflexMusic import app


# Admin filter yaradılır
def admin_filter():
    async def func(_, __, message: Message):
        try:
            member = await app.get_chat_member(message.chat.id, message.from_user.id)
            return member.status in ("administrator", "creator")
        except:
            return False
    return filters.create(func)


admin_only = admin_filter()  # qısayol


# /pin əmri
@app.on_message(filters.command("pin") & filters.group & admin_only)
async def pin_message(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("🔺 Zəhmət olmasa, bir mesaja cavab verin.")
    try:
        await client.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
        await message.reply_to_message.reply("📌 Mesaj sabitlənmişdir.")
    except Exception as e:
        await message.reply(f"❌ Pin edilə bilmədi. Səbəb: `{e}`")


# /unpin əmri
@app.on_message(filters.command("unpin") & filters.group & admin_only)
async def unpin_message(client: Client, message: Message):
    try:
        if message.reply_to_message:
            await client.unpin_chat_message(message.chat.id, message.reply_to_message.message_id)
            await message.reply_to_message.reply("✅ Mesaj pindən silindi.")
        else:
            await client.unpin_chat_message(message.chat.id)
            await message.reply("✅ Son pinlənmiş mesaj silindi.")
    except Exception as e:
        await message.reply(f"❌ Pin silinə bilmədi. Səbəb: `{e}`")


# /unpinall əmri
@app.on_message(filters.command("unpinall") & filters.group & admin_only)
async def unpin_all_messages(client: Client, message: Message):
    try:
        await client.unpin_all_chat_messages(message.chat.id)
        await message.reply("✅ Bütün pinlənmiş mesajlar silindi.")
    except Exception as e:
        await message.reply(f"❌ Pinlər silinə bilmədi. Səbəb: `{e}`")
