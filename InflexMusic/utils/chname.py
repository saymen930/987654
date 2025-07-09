from InflexMusic import app
from InflexMusic.utils.database import get_active_chats
from config import LOG_GROUP_ID


async def play_logs(message, streamtype):
    chat_id = message.chat.id
    aktifseslisayısı = len(await get_active_chats())
    if message.chat.id != LOG_GROUP_ID:
        try:
            await app.set_chat_title(LOG_GROUP_ID, f"Rahid_Music_Bot - {aktifseslisayısı}")
        except:
            pass
    return
