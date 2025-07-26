import random
from pyrogram import Client, filters
from pyrogram.types import Message

from InflexMusic import app  # bot instance

@app.on_message(filters.new_chat_members & filters.group)
async def welcome_new_members(client: Client, message: Message):
    for new_member in message.new_chat_members:
        # Bot özüdürsə, heç nə etmə
        if new_member.id == (await client.get_me()).id:
            continue

        username = f"@{new_member.username}" if new_member.username else new_member.first_name
        
        welcome_messages = [
            f"{username} xoş gəldin⚡ nə gətirmisən mənə🥱",
            f"{username} xoş gəldin necəsən?❤️‍🔥",
            f"{username} xoş gəldin çıxacaqsansa indidən vzzz🥳",
            f"{username} xoş gəldin necəsən brat 🌸",
            f"{username} xoş gəlmisən əəəə🤭",
            f"{username} başıma xeyir yenə gəldi",
            f"{username} səni görməy mənə xoş oldu 🤩",
            f"{username} Sən döyərsən mən?🙎"
        ]
        
        await message.reply(random.choice(welcome_messages))
