import random
from pyrogram import Client, filters
from pyrogram.types import Message

from InflexMusic import app  # bot instance

@app.on_message(filters.left_chat_member & filters.group)
async def goodbye_member(client: Client, message: Message):
    user = message.left_chat_member

    # Əgər botun özü çıxıbsa, heç nə etmə
    if user.id == (await client.get_me()).id:
        return

    name = user.first_name  # Təkcə ad göstəriləcək

    goodbye_messages = [
        f"{name} çıxdı, canımız qurtardı 😂",
        f"{name} bezdi getdi 😒",
        f"{name} getdi... darıxmayacağıq 🫡",
        f"{name} artıq yoxdu, rahat nəfəs ala bilərik 🧘",
        f"{name} çıxdı, qapını ört get 🙃",
        f"{name} çıxıb... bəlkə də geri dönər? yox eee dönməsin 😌",
        f"{name} çıxan kimi qrup işıqlanmağa başladı 🔆",
        f"{name} sağ ol ki, getdin bro ✌️",
        f"{name} sənsiz daha sakit oldu 💤",
        f"{name} çıxdı, indi daha az drama var 🫣",
        f"{name} əfsanə getdi... yox eee, sıradan biri idi 😅",
    ]

    await message.reply(random.choice(goodbye_messages))
