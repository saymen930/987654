import random
from pyrogram import Client, filters
from pyrogram.types import Message

from InflexMusic import app  # bot instance

@app.on_message(filters.left_chat_member & filters.group)
async def goodbye_member(client: Client, message: Message):
    user = message.left_chat_member
    # Bot özüdürsə, heç nə etmə
    if user.id == (await client.get_me()).id:
        return

    username = f"@{user.username}" if user.username else user.first_name

    goodbye_messages = [
        f"{username} çıxdı, canımız qurtardı 😂",
        f"{username} bezdi getdi 😒",
        f"{username} getdi... darıxmayacağıq 🫡",
        f"{username} artıq yoxdu, rahat nəfəs ala bilərik 🧘",
        f"{username} çıxdı, qapını ört get 🙃",
        f"{username} çıxıb... bəlkə də geri dönər? yox eee dönməsin 😌",
        f"{username} çıxan kimi qrup işıqlanmağa başladı 🔆",
        f"{username} sağ ol ki, getdin bro ✌️",
        f"{username} sənsiz daha sakit oldu 💤",
        f"{username} çıxdı, indi daha az drama var 🫣",
        f"{username} əfsanə getdi... yox eee, sıradan biri idi 😅",
    ]

    await message.reply(random.choice(goodbye_messages))
