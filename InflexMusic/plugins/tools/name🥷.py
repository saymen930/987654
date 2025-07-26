import sqlite3
from pyrogram import Client, filters
from pyrogram.types import Message
from InflexMusic import app

# DB bağlantısı və cədvəl
conn = sqlite3.connect("usernames.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS usernames (user_id INTEGER PRIMARY KEY, name TEXT)")
conn.commit()


@app.on_message(filters.group & ~filters.service)
async def detect_name_change(client: Client, message: Message):
    if not message.from_user:
        return

    user_id = message.from_user.id
    current_name = message.from_user.first_name

    cursor.execute("SELECT name FROM usernames WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    if row:
        old_name = row[0]
        if old_name != current_name:
            chat_name = message.chat.title or "Bu Qrup"
            await message.reply(
                f"📛 *Adını dəyişdi*\n"
                f"🔙 Köhnə: `{old_name}`\n"
                f"🔜 Yeni: `{current_name}`\n"
                f"💬 Qrup: {chat_name}"
            )
            cursor.execute("UPDATE usernames SET name = ? WHERE user_id = ?", (current_name, user_id))
    else:
        cursor.execute("INSERT INTO usernames (user_id, name) VALUES (?, ?)", (user_id, current_name))

    conn.commit()
