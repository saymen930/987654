from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
from InflexMusic import app  # Bot instansiyası

# 👮‍♂️ İstifadəçi adminmi?
async def is_admin(client: Client, user_id: int, chat_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    except:
        return False

# 🤖 Botun qovmaq icazəsi varmı?
async def is_self_admin(client: Client, chat_id: int) -> bool:
    try:
        member = await client.get_chat_member(chat_id, client.me.id)
        return (
            member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
            and getattr(member.privileges, "can_restrict_members", False)
        )
    except:
        return False

# 👞 Kick əmri (ban + unban)
@app.on_message(filters.command("kick") & filters.group)
async def kick_user(client: Client, message: Message):
    if not await is_admin(client, message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")
    
    if not await is_self_admin(client, message.chat.id):
        return await message.reply("🔺Botun istifadəçini qovmaq icazəsi yoxdur.")

    user = message.reply_to_message.from_user if message.reply_to_message else None

    if not user:
        return await message.reply("🔺 Kimi qovacağımı bilmirəm. /kick (reply) istifadə edin.")

    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await client.unban_chat_member(message.chat.id, user.id)
        await message.reply(
            f"👞 {user.mention} qrupdan qovuldu.\n🥷 İcraçı: {message.from_user.mention}"
        )
    except Exception as e:
        await message.reply(f"❌ Qovula bilmədi.\n`{e}`")

# ⚠️ Warn əmri
@app.on_message(filters.command("warn") & filters.group)
async def warn_user(client: Client, message: Message):
    if not await is_admin(client, message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")

    args = message.text.split(maxsplit=2)
    user = message.reply_to_message.from_user if message.reply_to_message else None
    reason = "Səbəb göstərilməyib"

    # Reply yoxdursa və ID/username verilmişsə
    if not user and len(args) > 1:
        try:
            user = await client.get_users(args[1])
            if len(args) > 2:
                reason = args[2]
        except:
            return await message.reply("❌ İstifadəçi tapılmadı. /warn @istifadəçi [səbəb] yazın.")
    elif user and len(args) > 1:
        reason = args[1:]

    if not user:
        return await message.reply("🔺 İstifadə: /warn (reply) [səbəb] və ya /warn <ID/@username> [səbəb]")

    username_display = f"@{user.username}" if user.username else "yoxdur"
    await message.reply(
        f"⚠️ {user.mention} xəbərdarlıq aldı!\n"
        f"👤 Username: {username_display}\n"
        f"🆔 ID: `{user.id}`\n"
        f"📝 Səbəb: {reason}\n"
        f"🥷 İcraçı: {message.from_user.mention}"
                         )
