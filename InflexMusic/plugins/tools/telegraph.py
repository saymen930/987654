import os
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from InflexMusic import app

# Faylı catbox.moe saytına yükləmək funksiyası
def upload_file(file_path):
    url = "https://catbox.moe/user/api.php"
    data = {"reqtype": "fileupload", "json": "true"}
    files = {"fileToUpload": open(file_path, "rb")}
    response = requests.post(url, data=data, files=files)

    if response.status_code == 200 and "url" in response.text:
        # JSON cavab varsa, linki düzəldək
        try:
            json_data = response.json()
            return True, json_data["url"]
        except Exception:
            return True, response.text.strip()
    else:
        return False, f"Xəta baş verdi: {response.status_code} - {response.text}"

# Əmr işləyicisi - Qruplarda işləməsi üçün
@app.on_message(filters.command(["tgm", "tgt", "telegraph", "tl"]) & filters.group)
async def get_link_group(client, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "📌 Zəhmət olmasa, bu əmrdən istifadə etmək üçün bir media faylına cavab verin✅"
        )

    media = message.reply_to_message
    file_size = 0

    try:
        if media.photo:
            file_size = media.photo.file_size
        elif media.video:
            file_size = media.video.file_size
        elif media.document:
            file_size = media.document.file_size
        else:
            return await message.reply_text("⚠️ Yalnız şəkil, video və sənədlər dəstəklənir.")
    except Exception:
        return await message.reply_text("❌ Media məlumatı oxunmadı.")

    if file_size > 200 * 1024 * 1024:
        return await message.reply_text("⚠️ Zəhmət olmasa, 200MB-dan kiçik bir media faylı istifadə edin.")

    try:
        status = await message.reply("⏳ Yüklənir...")

        async def progress(current, total):
            try:
                faiz = current * 100 / total
                await status.edit_text(f"📥 Endirilir... {faiz:.1f}%")
            except Exception:
                pass

        try:
            local_path = await media.download(progress=progress)
            await status.edit_text("📤 Fayl Telegraph'a yüklənir...")

            success, result = upload_file(local_path)

            if success:
                await status.edit_text(
                    f"✅ Fayl uğurla yükləndi: [Bağlantı]({result})",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("📁 Faylı aç", url=result)]]
                    ),
                    disable_web_page_preview=True
                )
            else:
                await status.edit_text(f"❌ Yükləmə zamanı xəta baş verdi:\n\n{result}")

            try:
                os.remove(local_path)
            except Exception:
                pass

        except Exception as e:
            await status.edit_text(f"❌ Fayl yükləmə alınmadı\n\n<i>Səbəb: {e}</i>")
            try:
                os.remove(local_path)
            except Exception:
                pass
    except Exception as e:
        await message.reply_text(f"❌ Gözlənilməz xəta: {e}")
