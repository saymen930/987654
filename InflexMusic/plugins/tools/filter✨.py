from pyrogram import Client, filters
from pyrogram.types import Message
from typing import Dict
import asyncio
from InflexMusic import app  # sənin botun app ola bilə

@app.on_message(filters.command("filter") & filters.group)
async def add_filter(_, message: Message):
    if not message.from_user:
        return

    print(f"Yoxlanır: {message.from_user.id} / {message.chat.id}")
    adminmi = await is_admin(message.from_user.id, message.chat.id)
    print(f"Admin status: {adminmi}")
    
    if not adminmi:
        return await message.reply("❌ Bu əmri istifadə etmək üçün admin olmalısınız.")
