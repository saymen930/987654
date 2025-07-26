from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
from InflexMusic import app  # Bot instansiyası

# 👮‍♂️ İstifadəçi adminmi?
async def is_admin(client: Client, user_id: int, chat_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception as e:
        print(f"[Admin yoxlama xətası] {e}")
        return False

# 🤖 Bot adminmi və hüququ varmı?
async def is_self_admin(client: Client, chat_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, client.me.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return False
        # Ban səlahiyyəti varsa: can_restrict_members = True
        return getattr(member.privileges, "can_restrict_members", False)
    except Exception as e:
        print(f"[Bot admin yoxlaması xətası] {e}")
        return False

# 🚫 Ban əmri
@app.on_message(filters.command("ban") & filters.group)
async def ban_user(client: Client, message: Message):
    if not await is_admin(client, message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")

    if not await is_self_admin(client, message.chat.id):
        return await message.reply("🔺Botun ban etmək hüququ yoxdur. Admin edin və səlahiyyət verin.")

    user = message.reply_to_message.from_user if message.reply_to_message else None

    if not user and len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            return await message.reply("❌ İstifadəçi tapılmadı.")

    if not user:
        return await message.reply("🔺 İstifadə: <b>/ban</b> (cavabla) və ya <b>/ban</b> <ID/@username>", quote=True)

    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await message.reply(f"🚫 {user.first_name} qrupdan banlandı.")
    except Exception as e:
        await message.reply(f"❌ Ban edilə bilmədi.\n`{e}`")

# ✅ Unban əmri
@app.on_message(filters.command("unban") & filters.group)
async def unban_user(client: Client, message: Message):
    if not await is_admin(client, message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")

    if not await is_self_admin(client, message.chat.id):
        return await message.reply("🔺Botun unban etmək hüququ yoxdur. Admin edin və səlahiyyət verin.")

    user = message.reply_to_message.from_user if message.reply_to_message else None

    if not user and len(message.command) > 1:
        try:
            user = await client.get_users(message.command[1])
        except:
            return await message.reply("❌ İstifadəçi tapılmadı.")

    if not user:
        return await message.reply("🔺 İstifadə: <b>/unban</b> (cavabla) və ya <b>/unban</b> <ID/@username>", quote=True)

    try:
        await client.unban_chat_member(message.chat.id, user.id)
        await message.reply(f"✅ `{user.first_name}` üçün qadağa ləğv edildi.")
    except Exception as e:
        await message.reply(f"❌ Qadağa silinə bilmədi.\n`{e}`")
