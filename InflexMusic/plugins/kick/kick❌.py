from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
from InflexMusic import app

warns = {}

async def is_admin(client: Client, user_id: int, chat_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except Exception as e:
        print(f"[Admin yoxlama xətası] {e}")
        return False

async def is_self_admin(client: Client, chat_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, client.me.id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] and getattr(member.privileges, "can_restrict_members", False)
    except Exception as e:
        print(f"[Bot admin yoxlaması xətası] {e}")
        return False

# /kick
@app.on_message(filters.command("kick") & filters.group)
async def kick_user(client, message):
    if not await is_admin(client, message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")
    if not await is_self_admin(client, message.chat.id):
        return await message.reply("🔺Botun hüququ yoxdur. Admin edin və səlahiyyət verin.")

    user = message.reply_to_message.from_user if message.reply_to_message else None
    if not user:
        return await message.reply("🔺 İstifadə: /kick (reply)")

    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await client.unban_chat_member(message.chat.id, user.id)
        await message.reply(f"👢 {user.first_name} qrupdan atıldı.")
    except Exception as e:
        await message.reply(f"❌ Atıla bilmədi.\n`{e}`")

# /mute
@app.on_message(filters.command("mute") & filters.group)
async def mute_user(client, message):
    if not await is_admin(client, message.from_user.id, message.chat.id):
        return await message.reply("❌ Admin deyilsiniz.")
    if not await is_self_admin(client, message.chat.id):
        return await message.reply("🔺Botun hüququ yoxdur.")

    user = message.reply_to_message.from_user if message.reply_to_message else None
    if not user:
        return await message.reply("🔺 İstifadə: /mute (reply)")

    try:
        await client.restrict_chat_member(message.chat.id, user.id, permissions=[])
        await message.reply(f"🔇 {user.first_name} səssiz edildi.")
    except Exception as e:
        await message.reply(f"❌ Səssiz edilə bilmədi.\n`{e}`")

# /unmute
@app.on_message(filters.command("unmute") & filters.group)
async def unmute_user(client, message):
    if not await is_admin(client, message.from_user.id, message.chat.id):
        return await message.reply("❌ Admin deyilsiniz.")
    if not await is_self_admin(client, message.chat.id):
        return await message.reply("🔺Botun hüququ yoxdur.")

    user = message.reply_to_message.from_user if message.reply_to_message else None
    if not user:
        return await message.reply("🔺 İstifadə: /unmute (reply)")

    try:
        from pyrogram.types import ChatPermissions
        await client.restrict_chat_member(message.chat.id, user.id, permissions=ChatPermissions(can_send_messages=True))
        await message.reply(f"🔊 {user.first_name} danışa bilər.")
    except Exception as e:
        await message.reply(f"❌ Danışıq icazəsi verilə bilmədi.\n`{e}`")

# /warn
@app.on_message(filters.command("warn") & filters.group)
async def warn_user(client, message):
    if not await is_admin(client, message.from_user.id, message.chat.id):
        return await message.reply("❌ Admin deyilsiniz.")

    user = message.reply_to_message.from_user if message.reply_to_message else None
    if not user:
        return await message.reply("🔺 İstifadə: /warn (reply)")

    cid = message.chat.id
    uid = user.id
    warns.setdefault(cid, {})
    warns[cid][uid] = warns[cid].get(uid, 0) + 1

    if warns[cid][uid] >= 3:
        try:
            await client.ban_chat_member(cid, uid)
            await client.unban_chat_member(cid, uid)
            warns[cid][uid] = 0
            return await message.reply(f"🚫 {user.first_name} 3 xəbərdarlıqdan sonra qrupdan atıldı.")
        except Exception as e:
            return await message.reply(f"❌ Qrupdan atmaq alınmadı.\n`{e}`")

    await message.reply(f"⚠️ {user.first_name} xəbərdarlıq aldı. ({warns[cid][uid]}/3)")

# /unwarn
@app.on_message(filters.command("unwarn") & filters.group)
async def unwarn_user(client, message):
    if not await is_admin(client, message.from_user.id, message.chat.id):
        return await message.reply("❌ Admin deyilsiniz.")

    user = message.reply_to_message.from_user if message.reply_to_message else None
    if not user:
        return await message.reply("🔺 İstifadə: /unwarn (reply)")

    cid = message.chat.id
    uid = user.id
    if cid in warns and uid in warns[cid]:
        warns[cid][uid] = max(0, warns[cid][uid] - 1)
        return await message.reply(f"✅ {user.first_name} üçün xəbərdarlıq azaldıldı. ({warns[cid][uid]}/3)")
    else:
        return await message.reply("ℹ️ Bu istifadəçidə xəbərdarlıq yoxdur.")

# /kickme
@app.on_message(filters.command("kickme") & filters.group)
async def kick_me(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if await is_admin(client, user_id, chat_id):
        return await message.reply("Axı sən bir adminsən... Səni atmayacam balam🫂")

    if not await is_self_admin(client, chat_id):
        return await message.reply("🔺Botun hüququ yoxdur.")

    try:
        await client.ban_chat_member(chat_id, user_id)
        await client.unban_chat_member(chat_id, user_id)
    except Exception as e:
        await message.reply(f"❌ Atmaq mümkün olmadı.\n`{e}`")
