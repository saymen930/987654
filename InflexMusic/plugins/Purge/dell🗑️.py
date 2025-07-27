import os
import asyncio
from telethon import TelegramClient, events, Button, functions
from telethon.tl.types import ChatAdminRights, ChatBannedRights
from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError, ChannelPrivateError
from dotenv import load_dotenv
from InflexMusic.core.bot import xaos as client  

# ------------- KONFİQURASİYA -------------
load_dotenv()


BAN_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)

# ------------- KÖMƏKÇİ FUNKSİYALAR -------------
async def is_admin(chat_id: int, user_id: int) -> bool:
    try:
        perms = await client.get_permissions(chat_id, user_id)
        return bool(getattr(perms, "is_admin", False) or getattr(perms, "is_creator", False))
    except Exception:
        return False

async def bot_can_ban(chat_id: int) -> bool:
    me = await client.get_me()
    try:
        perms = await client.get_permissions(chat_id, me.id)
    except Exception:
        return False

    if getattr(perms, "is_creator", False):
        return True

    if not getattr(perms, "is_admin", False):
        return False

    try:
        admin_rights: ChatAdminRights = perms.participant.admin_rights
        if admin_rights and getattr(admin_rights, "ban_users", False):
            return True
    except Exception:
        pass
    return False

async def list_deleted_users(chat_id: int):
    deleted = []
    try:
        async for user in client.iter_participants(chat_id):
            if getattr(user, "deleted", False):
                deleted.append(user)
    except ChannelPrivateError:
        pass
    return deleted

async def ban_deleted_users(chat_id: int, deleted_users):
    count = 0
    for user in deleted_users:
        try:
            await client(functions.channels.EditBannedRequest(
                channel=chat_id,
                participant=user.id,
                banned_rights=BAN_RIGHTS
            ))
            count += 1
        except (ChatAdminRequiredError, UserAdminInvalidError):
            try:
                await client.kick_participant(chat_id, user.id)
                count += 1
            except Exception:
                pass
        except Exception:
            pass
        await asyncio.sleep(0.2)
    return count

async def notify_admins_if_50(chat_id: int, deleted_count: int):
    """
    Əgər silinmiş hesab sayı >=50 isə admin heyətinə bildiriş göndərir.
    """
    if deleted_count >= 50:
        # Qrup adminlərini tapırıq
        admin_list = []
        async for user in client.iter_participants(chat_id, filter=functions.channels.GetParticipantsRequest(
            channel=chat_id,
            filter=None,
            offset=0,
            limit=200
        )):
            if getattr(user, "participant", None) and getattr(user.participant, "admin_rights", None):
                admin_list.append(user)
        
        # Əgər admin siyahısı boş deyilsə, qruplara xəbərdarlıq edirik
        if admin_list:
            mention_list = ", ".join(
                f"[{a.first_name}](tg://user?id={a.id})" for a in admin_list if a.first_name
            )
            await client.send_message(
                chat_id,
                f"⚠️ **Diqqət adminlər:** Qrupda silinmiş hesab sayı **{deleted_count}** ədəd oldu!\n{mention_list}",
                link_preview=False
            )

# ------------- /del ƏMRİ -------------
@client.on(events.NewMessage(pattern=r"^[!./]?dels$"))
async def del_cmd(event: events.NewMessage.Event):
    if event.is_private:
        return await event.reply("❗ Bu əmri yalnız qruplarda istifadə edə bilərsiniz.")

    chat_id = event.chat_id

    if not await is_admin(chat_id, event.sender_id):
        return await event.reply("⛔ Bu əmri yalnız adminlər istifadə edə bilər.")

    msg = await event.reply("🔎 Silinmiş hesablar yoxlanılır, gözləyin...")

    deleted_users = await list_deleted_users(chat_id)
    say = len(deleted_users)

    if say == 0:
        return await msg.edit("✅ Qrupda silinmiş hesab yoxdur.")

    # 50-dən çoxdursa xəbərdarlıq et
    await notify_admins_if_50(chat_id, say)

    lines = [f"• `{u.id}`" for u in deleted_users[:50]]
    listed = "\n".join(lines)
    if say > 50:
        listed += f"\n... və daha {say - 50} dənə"

    text = (
        f"🧹 **Silinmiş hesablar tapıldı:** `{say}` ədəd.\n\n"
        f"{listed}\n\n"
        f"Adminlər aşağıdakı düymə ilə onları qrupdan silə bilər."
    )

    buttons = [[Button.inline("🧹 Silinmiş hesabları təmizlə", data=f"purge_deleted:{chat_id}:{say}")]]
    await msg.edit(text, buttons=buttons)

# ------------- CALLBACK: Sil düyməsi -------------
@client.on(events.CallbackQuery(pattern=b"purge_deleted:"))
async def purge_deleted_cb(event: events.CallbackQuery.Event):
    data = event.data.decode().split(":")
    if len(data) != 3:
        return await event.answer("Xəta baş verdi.", alert=True)

    _, chat_id_str, _ = data
    chat_id = int(chat_id_str)

    if not await is_admin(chat_id, event.sender_id):
        return await event.answer("⛔ Bu düymə yalnız adminlər üçündür.", alert=True)

    if not await bot_can_ban(chat_id):
        return await event.answer("⚠️ Botun ban (kick) səlahiyyəti yoxdur!", alert=True)

    await event.edit("🧹 Silinmiş hesablar təmizlənir, gözləyin...")

    deleted_users = await list_deleted_users(chat_id)
    if not deleted_users:
        return await event.edit("✅ Silinmiş hesab qalmayıb.")

    count = await ban_deleted_users(chat_id, deleted_users)
    await event.edit(f"✅ {count} silinmiş hesab qrupdan çıxarıldı.")










# ------------- START -------------
