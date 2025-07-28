from InflexMusic.core.bot import xaos as client  
import os
import requests
import asyncio
from telethon import TelegramClient, events, Button
from telethon.tl.types import MessageMediaPhoto
from PIL import Image, ImageDraw, ImageFont
import textwrap



# 📤 Faylı catbox.moe saytına yükləmək funksiyası
def upload_file(file_path):
    url = "https://catbox.moe/user/api.php"
    data = {"reqtype": "fileupload", "json": "true"}
    with open(file_path, "rb") as f:
        files = {"fileToUpload": f}
        response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        try:
            json_data = response.json()
            return True, json_data["url"]
        except Exception:
            return True, response.text.strip()
    else:
        return False, f"Xəta baş verdi: {response.status_code} - {response.text}"

# 📥 Əmr işləyicisi
@client.on(events.NewMessage(pattern=r'^/(tgm|tgt|telegraph|tl)$'))
async def handler(event):
    if not event.is_group:
        await event.reply("📌 Bu əmrdən yalnız qruplarda istifadə edilə bilər.")
        return

    if not event.reply_to_msg_id:
        await event.reply("📌 Zəhmət olmasa, bu əmrdən istifadə etmək üçün bir media faylına cavab verin.")
        return

    replied = await event.get_reply_message()
    media = replied.media

    if not media:
        await event.reply("⚠️ Yalnız şəkil, video və sənədlər dəstəklənir.")
        return

    file_size = 0

    try:
        if isinstance(media, MessageMediaPhoto):
            if replied.photo and replied.photo.sizes:
                file_size = max([s.size for s in replied.photo.sizes if hasattr(s, 'size')])
        elif hasattr(replied, 'document') and replied.document:
            file_size = replied.document.size
        else:
            await event.reply("⚠️ Bu media tipi dəstəklənmir.")
            return
    except Exception:
        await event.reply("⚠️ Media ölçüsünü təyin etmək mümkün olmadı.")
        return

    if file_size and file_size > 200 * 1024 * 1024:
        await event.reply("⚠️ Zəhmət olmasa, 200MB-dan kiçik bir media faylı istifadə edin.")
        return

    status = await event.reply("⏳ Yüklənir...")

    try:
        file_path = await replied.download_media(progress_callback=lambda d, t: asyncio.create_task(
            status.edit(f"📥 Endirilir... {d * 100 / t:.1f}%")
        ))

        await status.edit("📤 Fayl Telegraph'a yüklənir...")

        success, result = upload_file(file_path)

        if success:
            await status.edit(
                "✅ Fayl uğurla yükləndi!",
                buttons=[[Button.url("📥 Toxun və Bax", result)]]
            )
        else:
            await status.edit(f"❌ Yükləmə zamanı xəta baş verdi:\n\n{result}")

        try:
            os.remove(file_path)
        except Exception:
            pass

    except Exception as e:
        await status.edit(f"❌ Gözlənilməz xəta: `{e}`")



def make_simple_image(code: str, output_file="carbon.png"):
    font_path = "/system/fonts/DroidSansMono.ttf"  # Pydroid3-də ola biləcək font
    try:
        font = ImageFont.truetype(font_path, 20)
    except:
        font = ImageFont.load_default()

    lines = textwrap.wrap(code, width=60)
    width = 800
    height = 20 * len(lines) + 20

    image = Image.new("RGB", (width, height), color=(40, 44, 52))  # Tünd fon (Monokai tərzi)
    draw = ImageDraw.Draw(image)
    y_text = 10

    for line in lines:
        draw.text((10, y_text), line, font=font, fill=(248, 248, 242))  # Açıq mətn rəngi
        y_text += 20

    image.save(output_file)
    return output_file

@client.on(events.NewMessage(pattern="/carbon(?:\s+(.+))?"))
async def carbon_handler(event):
    code = event.pattern_match.group(1)
    if not code:
        reply = await event.get_reply_message()
        if reply and reply.text:
            code = reply.text
        else:
            await event.reply("❌ Zəhmət olmasa kod göndərin və ya mesaja reply edin.")
            return

    await event.reply("🖼️ Carbon hazırlanır...")

    try:
        img_path = make_simple_image(code)
        await client.send_file(event.chat_id, img_path, caption="✅ Hazırdır!")
        os.remove(img_path)
    except Exception as e:
        await event.reply(f"❌ Xəta baş verdi:\n{e}")
        
# 🔄 Botu işə sal
#client.start()
#print("🤖 Bot işə düşdü!")
#client.run_until_disconnected()







