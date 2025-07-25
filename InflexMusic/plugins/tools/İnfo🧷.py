import os
import time
from datetime import datetime

from pyrogram import filters
from pyrogram.errors import UserNotParticipant, PeerIdInvalid
from InflexMusic import app
from cookies.extract_user import extract_user, last_online


@app.on_message(filters.command("info", [".", "@", "/", "!"]))
async def info(client, message):
    """ℹ️ İstifadəçi haqqında məlumat çıxarır"""
    status_message = await message.reply_text("🔎 Məlumat yığılır...")

    # İstifadəçi ID-sini çıxart
    from_user_id, _ = extract_user(message)
    if not from_user_id:
        await status_message.edit("⛔ Etibarlı istifadəçi ID-si tapılmadı.")
        return

    # İstifadəçini götür
    try:
        from_user = await client.get_users(from_user_id)
    except PeerIdInvalid:
        await status_message.edit("❌ İstifadəçi tapılmadı! ID etibarsızdır.")
        return
    except Exception as error:
        await status_message.edit(f"❌ Xəta: `{error}`")
        return

    if from_user is None:
        await status_message.edit("⛔ Etibarlı istifadəçi tapılmadı.")
        return

    # İstifadəçi məlumatları
    first_name = from_user.first_name or ""
    last_name = from_user.last_name or ""
    username = f"@{from_user.username}" if from_user.username else "Yoxdur"

    message_out_str = (
        "<b>🛰 Telegram Verilənlər Bazası</b>\n\n"
        f"• 👤 Ad: <a href='tg://user?id={from_user.id}'>{first_name}</a>\n"
        f"• 🆔 ID: <code>{from_user.id}</code>\n"
        f"• 🏷 İstifadəçi adı: {username}\n"
        f"• 📎 Link: {from_user.mention}\n"
    )

    if from_user.is_deleted:
        message_out_str += "• 🚫 Silinib: Bəli\n"
    if from_user.is_verified:
        message_out_str += "• ✅ Doğrulanıb: Bəli\n"
    if from_user.is_scam:
        message_out_str += "• ⚠️ Fırıldaq: Bəli\n"

    message_out_str += f"• ⏱ Son görünmə: <code>{last_online(from_user)}</code>\n\n"

    # Qrup üçün əlavə məlumat
    if message.chat.type in ["supergroup", "channel"]:
        try:
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = datetime.fromtimestamp(
                chat_member_p.joined_date or time.time()
            ).strftime("%Y-%m-%d %H:%M:%S")
            message_out_str += f"• 👥 Qrupa qoşulma: <code>{joined_date}</code>\n"
        except UserNotParticipant:
            message_out_str += "• ❌ Bu qrupda deyil.\n"

    # Şəkil varsa
    if from_user.photo and getattr(from_user.photo, "big_file_id", None):
        local_user_photo = await client.download_media(from_user.photo.big_file_id)
        await message.reply_photo(
            photo=local_user_photo,
            caption=message_out_str,
            quote=True
        )
        os.remove(local_user_photo)
    else:
        await message.reply_text(
            text=message_out_str,
            quote=True
        )

    await status_message.delete()
