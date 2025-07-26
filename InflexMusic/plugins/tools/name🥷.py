import aiosqlite
from pyrogram import Client, filters
from pyrogram.types import Message
from InflexMusic import app


# SQLite asinxron bazanı əvvəlcədən yarat (bir dəfə)
async def init_db():
    async with aiosqlite.connect("usernames.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS usernames (user_id INTEGER PRIMARY KEY, name TEXT)")
        await db.commit()

# Ad dəyişmə yoxlaması
@app.on_message(filters.group & ~filters.service)
async def detect_name_change(client: Client, message: Message):
    if not message.from_user:
        return

    user_id = message.from_user.id
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    full_name = f"{first_name} {last_name}".strip()

    async with aiosqlite.connect("usernames.db") as db:
        async with db.execute("SELECT name FROM usernames WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()

        if row:
            old_name = row[0]
            if old_name != full_name:
                chat_name = message.chat.title or "Bu Qrup"
                await message.reply(
                    f"📛 *Adını dəyişdi*\n"
                    f"🔙 Köhnə: `{old_name}`\n"
                    f"🔜 Yeni: `{full_name}`\n"
                    f"💬 Qrup: {chat_name}"
                )
                await db.execute("UPDATE usernames SET name = ? WHERE user_id = ?", (full_name, user_id))
        else:
            await db.execute("INSERT INTO usernames (user_id, name) VALUES (?, ?)", (user_id, full_name))

        await db.commit()
