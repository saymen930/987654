from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message, ChatPrivileges
from InflexMusic import app  # Bot instansiyası

# 👮‍♂️ İstifadəçi adminmi?
async def is_admin(client: Client, user_id: int, chat_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except:
        return False

# 👤 İstifadəçi tapmaq: reply yoxdursa komanda arqumentindən istifadə
async def extract_user(client: Client, message: Message):
    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        if len(message.command) > 1:
            try:
                user = await client.get_users(message.command[1])
            except:
                return None
    return user

# ➕ Promote əmri
@app.on_message(filters.command("promote") & filters.group)
async def promote_user(client: Client, message: Message):
    if not await is_admin(client, message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")

    user = await extract_user(client, message)
    if not user:
        return await message.reply("🔺Kimin haqqında danışdığınızı bilmirəm...")

    try:
        await client.promote_chat_member(
            message.chat.id,
            user.id,
            privileges=ChatPrivileges(
                can_manage_chat=False,
                can_delete_messages=True,
                can_restrict_members=True,
                can_promote_members=False,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=True,
                can_manage_voice_chats=False,
            )
        )
        await message.reply(f"🎉 {user.mention} admin oldu!\nİcraçı 🥷 {message.from_user.mention}")
    except Exception as e:
        await message.reply(f"❌ Admin edilə bilmədi.\n`{e}`")

# ➖ Demote əmri
@app.on_message(filters.command("demote") & filters.group)
async def demote_user(client: Client, message: Message):
    if not await is_admin(client, message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")

    user = await extract_user(client, message)
    if not user:
        return await message.reply("🔺Kimin haqqında danışdığınızı bilmirəm...")

    try:
        await client.promote_chat_member(
            message.chat.id,
            user.id,
            privileges=ChatPrivileges(
                can_manage_chat=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_promote_members=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_manage_voice_chats=False,
            )
        )
        await message.reply(f"📉 {user.mention} adminlikdən çıxarıldı!\nİcraçı 🥷 {message.from_user.mention}")
    except Exception as e:
        await message.reply(f"❌ Adminlikdən çıxarıla bilmədi.\n`{e}`")
