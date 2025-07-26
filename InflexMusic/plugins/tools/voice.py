from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from InflexMusic import app
import aiohttp
import re

# Video söhbət başladıqda
@app.on_message(filters.video_chat_started)
async def vc_start(_, msg):
    await msg.reply("**😍 Video söhbət başladı! 🥳**")

# Video söhbət bitdikdə
@app.on_message(filters.video_chat_ended)
async def vc_end(_, msg):
    await msg.reply("**😕 Video söhbət bitdi... 💔**")

# Video söhbətə istifadəçi əlavə edildikdə
@app.on_message(filters.video_chat_members_invited)
async def vc_invite(app: Client, message: Message):
    text = f"➻ {message.from_user.mention}\n\n**❖ Video söhbətə dəvət olunanlar:**\n\n➻ "
    x = 0
    for user in message.video_chat_members_invited.users:
        try:
            text += f"[{user.first_name}](tg://user?id={user.id}) "
            x += 1
        except Exception:
            pass

    try:
        invite_link = await app.export_chat_invite_link(message.chat.id)
        add_link = f"https://t.me/{app.username}?startgroup=true"
        reply_text = f"{text} 🤭🤭"

        await message.reply(
            reply_text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text="🎧 Söhbətə qoşul", url=add_link)],
                ]
            ),
        )
    except Exception as e:
        print(f"Xəta: {e}")

# Riyazi ifadə hesablamaq (/math əmri)
@app.on_message(filters.command("math", prefixes="/"))
def calculate_math(client, message):
    if len(message.text.split()) < 2:
        return message.reply("Zəhmət olmasa hesablanacaq ifadəni yazın. Məsələn: `/math 2+2`")
    expression = message.text.split("/math ", 1)[1]
    try:
        result = eval(expression)
        response = f"Nəticə: `{result}`"
    except:
        response = "❌ Düzgün riyazi ifadə deyil."
    message.reply(response)

# Google axtarış funksiyası (/spg)
@app.on_message(filters.command(["spg"], ["/", "!", "."]))
async def search(event):
    if len(event.command) < 2:
        return await event.reply("🔍 Axtarış üçün söz yazın. Məsələn: `/spg Telegram bot`")

    msg = await event.reply("🔍 Axtarılır...")
    async with aiohttp.ClientSession() as session:
        start = 1
        query = event.text.split(None, 1)[1]
        async with session.get(
            f"https://content-customsearch.googleapis.com/customsearch/v1?cx=ec8db9e1f9e41e65e&q={query}&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM&start={start}",
            headers={"x-referer": "https://explorer.apis.google.com"},
        ) as r:
            response = await r.json()
            result = ""

            if not response.get("items"):
                return await msg.edit("🔍 Heç bir nəticə tapılmadı.")
            for item in response["items"]:
                title = item["title"]
                link = item["link"]
                if "/s" in item["link"]:
                    link = item["link"].replace("/s", "")
                elif re.search(r"\/\d", item["link"]):
                    link = re.sub(r"\/\d", "", item["link"])
                if "?" in link:
                    link = link.split("?")[0]
                if link in result:
                    continue
                result += f"🔹 {title}\n🔗 {link}\n\n"

            prev_and_next_btns = [
                InlineKeyboardButton("▶️ Növbəti", callback_data=f"next {start+10} {query}")
            ]
            await msg.edit(result, link_preview=False, reply_markup=InlineKeyboardMarkup([prev_and_next_btns]))
        await session.close()
