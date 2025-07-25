from pyrogram import Client, filters
from pyrogram.types import Message
from InflexMusic.owner import OWNER_ID  # owner.py-dən gəlir

from InflexMusic import app


async def is_admin(client: Client, message: Message) -> bool:
    if message.from_user.id in OWNER_ID:
        return True

    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ["administrator", "creator"]


@app.on_message(filters.command("pin") & filters.group)
async def pin_message(client, message: Message):
    if not message.reply_to_message:
        await message.reply("Bir mesajı cavablayaraq /pin yazmalısınız 🔮")
        return

    if await is_admin(client, message):
        await client.pin_chat_message(
            chat_id=message.chat.id,
            message_id=message.reply_to_message.id
        )
        await message.reply("📌 Bir mesajı sabitlədim...")
    else:
        await message.reply("❌ Sizin admin olduğunuzu görmürəm.....")


@app.on_message(filters.command("unpin") & filters.group)
async def unpin_message(client, message: Message):
    if not message.reply_to_message:
        await message.reply("Bir mesajı cavablayaraq /unpin yazmalısınız 🔮")
        return

    if await is_admin(client, message):
        await client.unpin_chat_message(
            chat_id=message.chat.id,
            message_id=message.reply_to_message.id
        )
        await message.reply("📌 Bir mesajı sabitdən sildim.....")
    else:
        await message.reply("❌ Sizin admin olduğunuzu görmürəm.....")
