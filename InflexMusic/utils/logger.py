from pyrogram.enums import ParseMode

from InflexMusic import app
from InflexMusic.utils.database import is_on_off
from config import LOG_GROUP_ID


async def play_logs(message, streamtype):
    if await is_on_off(2):
        logger_text = f"""
<b>{app.mention} PLAY LOG</b>

<b>Qrup ID:</b> <code>{message.chat.id}</code>
<b>Qrup Adı:</b> {message.chat.title}
<b>Qrup linki:</b> @{message.chat.username}

<b>🆔:</b> <code>{message.from_user.id}</code>
<b>👤:</b> {message.from_user.mention}
<b>🔗:</b> @{message.from_user.username}

<b>Tələbi:</b> {message.text.split(None, 1)[1]}
<b>Platform:</b> {streamtype}"""
        if message.chat.id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    chat_id=LOG_GROUP_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                pass
        return
