
import os, asyncio, time, shlex, requests, pyrogram

from datetime import datetime
#from InflexMusic import app
from InflexMusic.core.bot import pls as app
from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.types import User




def extract_user(message: Message) -> (int, str):
    user_id = None
    user_first_name = None

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_first_name = message.reply_to_message.from_user.first_name

    elif len(message.command) > 1:
        if (
            len(message.entities) > 1 and
            message.entities[1].type == "text_mention"
        ):
            # 0: is the command used
            # 1: should be the user specified
            required_entity = message.entities[1]
            user_id = required_entity.user.id
            user_first_name = required_entity.user.first_name
        else:
            user_id = message.command[1]
            # don't want to make a request -_-
            user_first_name = user_id

        try:
            user_id = int(user_id)
        except ValueError:
            print("Scam ")

    else:
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name

    return (user_id, user_first_name)


def last_online(from_user: User) -> str:
    time = ""
    if from_user.is_bot:
        time += "🤖 Bot :("
    elif from_user.status == 'recently':
        time += "Recently"
    elif from_user.status == 'within_week':
        time += "Within the last week"
    elif from_user.status == 'within_month':
        time += "Within the last month"
    elif from_user.status == 'long_time_ago':
        time += "A long time ago :("
    elif from_user.status == 'online':
        time += "Currently Online"
    elif from_user.status == 'offline':
        time += datetime.fromtimestamp(from_user.last_online_date).strftime("%a, %d %b %Y, %H:%M:%S")
    return time







@app.on_message(filters.command("info", [".", "/", "!"]))
async def info(client, message):
    """ℹ  **İstifadəçi Məlumatını Çıxarın** """
    status_message = await message.reply_text(
        "🔎"
    )
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        await status_message.edit("⛔ Etibarlı İstifadəçi **ID** göstərilməyib")
        return
    
    first_name = from_user.first_name or ""
    last_name = from_user.last_name or ""
    username = from_user.username or ""
    
    message_out_str = (
        "<b>🛰 Telegram verilənlər bazasından</b>\n\n"
        f"<b>• Ad : <a href='tg://user?id={from_user.id}'>{first_name}</a></b>\n"
        f"<b>• ID :</b> <code>{from_user.id}</code>\n"
        f"<b>• İstifadəçi Adı :</b> @{username}\n"
        f"<b>• Link :</b> {from_user.mention}\n" if from_user.username else ""
        f"<b>Silindi:</b>Doğrudur\n" if from_user.is_deleted else ""
        f"<b>Doğrulanıb:</b>Doğrudur" if from_user.is_verified else ""
        f"<b>Fırıldaqdır:</b>Doğrudur" if from_user.is_scam else ""
        # f"<b>Is Fake:</b> True" if from_user.is_fake else ""
        f"<b>Son görünmə:</b> <code>{last_online(from_user)}</code>\n\n"
    )

    if message.chat.type in ["supergroup", "channel"]:
        try:
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = datetime.fromtimestamp(
                chat_member_p.joined_date or time.time()
            ).strftime("%Y.%m.%d %H:%M:%S")
            message_out_str += (
                "<b>• Lastseen :</b> <code>"
                f"{joined_date}"
                "</code>\n"
                "▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
            )
        except UserNotParticipant:
            pass
    chat_photo = from_user.photo
    if chat_photo:
        local_user_photo = await client.download_media(
            message=chat_photo.big_file_id
        )
        await message.reply_photo(
            photo=local_user_photo,
            quote=True,
            caption=message_out_str,
            disable_notification=True
        )
        os.remove(local_user_photo)
    else:
        await message.reply_text(
            text=message_out_str,
            quote=True,
            disable_notification=True
        )
    await status_message.delete()
