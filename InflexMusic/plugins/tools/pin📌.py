from pyrogram import Client, filters
from pyrogram.types import Message, ChatMember
import config  # config.py faylını import edirik

async def is_admin(client: Client, message: Message) -> bool:
    # İstifadəçi OWNER_ID siyahısındadırsa, icazə ver
    if message.from_user.id in config.OWNER_ID:
        return True

    # Əgər yoxdursa, qrupda admin statusunu yoxla
    member: ChatMember = await client.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ["administrator", "creator"]


@app.on_message(filters.command("pin") & filters.group)
async def pin_message(client, message: Message):
    if not message.reply_to_message:
        await message.reply("Bir mesajı cavablayaraq /pin yazmalısınız!")
        return

    if await is_admin(client, message):
        try:
            await message.reply_to_message.pin()
            await message.reply("📌 Bir mesajı sabitlədim...")
        except Exception as e:
            await message.reply(f"Xəta baş verdi: {e}")
    else:
        await message.reply("❌ Sizin admin olduğunuzu görmürəm.....")


@app.on_message(filters.command("unpin") & filters.group)
async def unpin_message(client, message: Message):
    if not message.reply_to_message:
        await message.reply("Bir mesajı cavablayaraq /unpin yazmalısınız!")
        return

    if await is_admin(client, message):
        try:
            await message.reply_to_message.unpin()
            await message.reply("📌 Bir mesajı sabitdən sildim.....")
        except Exception as e:
            await message.reply(f"Xəta baş verdi: {e}")
    else:
        await message.reply("❌ Sizin admin olduğunuzu görmürəm.....")
