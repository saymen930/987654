from pyrogram import Client, filters
from pyrogram.types import Message
from InflexMusic import app  # Bot instansiyası

# Sadə yaddaşda filterləri saxlayan dəyişən
filters_dict = {}

# Admin yoxlama funksiyası
async def is_admin(user_id: int, chat_id: int) -> bool:
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False

# /filter komandasını əlavə et
@app.on_message(filters.command("filter") & filters.group)
async def add_filter(client: Client, message: Message):
    if not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")
    
    chat_id = message.chat.id

    # Reply varsa
    if message.reply_to_message:
        replied_text = message.reply_to_message.text or message.reply_to_message.caption
        if not replied_text:
            return await message.reply("❌ Cavab verdiyiniz mesajda mətn yoxdur.")
        
        args = message.text.split(None, 1)
        if len(args) < 2:
            return await message.reply("İstifadə: /filter [cavab metni] (mesaja reply ilə)")
        
        reply_text = args[1]
        word = replied_text.lower()
    else:
        args = message.text.split(None, 2)
        if len(args) < 3:
            return await message.reply("İstifadə: /filter söz cavab və ya mesaja reply ilə /filter cavab")
        word, reply_text = args[1].lower(), args[2]

    if chat_id not in filters_dict:
        filters_dict[chat_id] = {}
    filters_dict[chat_id][word] = reply_text

    await message.reply(f"✅ Filter əlavə olundu: `{word}` → `{reply_text}`")

# /stop filter silmək üçün
@app.on_message(filters.command("stop") & filters.group)
async def stop_filter(client: Client, message: Message):
    if not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")
    
    args = message.text.split(None, 1)
    if len(args) < 2:
        return await message.reply("İstifadə: /stop söz")
    
    word = args[1].lower()
    chat_id = message.chat.id

    if chat_id in filters_dict and word in filters_dict[chat_id]:
        del filters_dict[chat_id][word]
        await message.reply(f"✅ Filter silindi: `{word}`")
    else:
        await message.reply("❌ Belə filter tapılmadı.")

# /stopall - bütün filterləri silmək
@app.on_message(filters.command("stopall") & filters.group)
async def stop_all_filters(client: Client, message: Message):
    if not await is_admin(message.from_user.id, message.chat.id):
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")
    
    chat_id = message.chat.id
    if chat_id in filters_dict:
        filters_dict[chat_id].clear()
        await message.reply("✅ Bütün filterlər silindi.")
    else:
        await message.reply("❌ Filterlər mövcud deyil.")

# /filters - mövcud filterləri göstər
@app.on_message(filters.command("filters") & filters.group)
async def list_filters(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in filters_dict and filters_dict[chat_id]:
        text = "📋 Mövcud filterlər:\n\n"
        for word, reply in filters_dict[chat_id].items():
            text += f"• `{word}` → `{reply}`\n"
        await message.reply(text)
    else:
        await message.reply("❌ Heç bir filter mövcud deyil.")

# Filter trigger - adi mesajlarda cavab verir
@app.on_message(filters.text & filters.group)
async def trigger_filter(client: Client, message: Message):
    chat_id = message.chat.id
    msg_text = message.text.lower()

    if chat_id in filters_dict:
        for word, reply_text in filters_dict[chat_id].items():
            if word in msg_text:
                await message.reply(reply_text)
                break
