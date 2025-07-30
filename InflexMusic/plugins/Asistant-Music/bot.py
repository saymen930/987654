from InflexMusic.core.bot import xaos as client  # Telethon bot instance


# bot.py
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import GetFullChatRequest, GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, PeerUser, PeerChat, PeerChannel, ChannelParticipantsSearch
import asyncio
from telethon.tl.custom import Button  # Əlavə et

from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantBanned, ChatBannedRights
from telethon.tl.functions.channels import GetParticipantRequest
import config
from Jason.assistant import buttons, P_MSG, P_BAN, O_MSG




@client.on(events.NewMessage(pattern='[.!/]music'))
async def bot_as_command(event):
    if event.is_private:
        await event.reply(O_MSG, buttons=buttons)
        return

    try:
        chat = await event.get_chat()
        chat_id = event.chat_id

        try:
            participant = await client(GetParticipantRequest(chat_id, config.userbot_username))
            part = participant.participant

            # BAN olub olmadığını yoxla
            if hasattr(part, 'banned_rights') and part.banned_rights:
                await event.reply(P_BAN, buttons=buttons)
                return

            # SƏSİZƏ alınıbsa
            if hasattr(part, 'restrictions') and part.restrictions:
                await event.reply(P_BAN, buttons=buttons)
                return

        except UserNotParticipantError:
            await event.reply(P_MSG, buttons=buttons)
            return

        # Əgər hər şey qaydasındadırsa, userbota mesaj göndər
        await client.send_message(config.userbot_username, f"[.!/]music {chat_id}")
        
    except Exception as e:
        await event.reply(f"⚠️ Xəta baş verdi: {e}")
  
client.run_until_disconnected()  
