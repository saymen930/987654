# userbot.py əsasss
import random
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaDocument
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.sessions import StringSession
from telethon.errors import ChatWriteForbiddenError
from telethon.tl.custom import Button  # Əlavə et
import config
from telethon import Button
from InflexMusic.core.bot import str as client  # Telethon bot instance




buttons = [[Button.url("🎧 Asistant Hesabı »", f"https://t.me/sesizKOLGE")]]

T_T = "Tesrttttttt"




buttos = [
    [Button.url("🎧 Asistant Hesabı »", "https://t.me/your_bot_username")]
]

buttons=[
                [Button.url("🎧 Asistant Hesabı »", "https://t.me/sesizKOLGE")]
            ]


@client.on(events.NewMessage(pattern='[.!/]music'))
async def send_random_song(event):
    try:
        channel_entity = await client.get_entity(config.music_channel)
        history = await client(GetHistoryRequest(
            peer=channel_entity,
            limit=100,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        audio_messages = [
            msg for msg in history.messages 
            if msg.media and isinstance(msg.media, MessageMediaDocument) 
            and msg.file and msg.file.mime_type and msg.file.mime_type.startswith("audio")
        ]

        if not audio_messages:
            await event.reply("🎵 Kanaldan mahnı tapılmadı.")
            return

        random_song = random.choice(audio_messages)
        
        # 1. Mahnını at
        await client.send_file(event.chat_id, random_song)
        
        
    
   
    except Exception as e:
        await event.reply(f"⚠️ Xəta baş verdi: {e}")
        
        
async def send_random_song(target, reply_event=None):
    try:
        random_song = random.choice(song_list, buttons=buttons)
        await client.send_file(target, random_song)
    except ChatWriteForbiddenError:
        if reply_event:
            await reply_event.reply("❌ Söhbətə yazmaq icazəm yoxdur.")
        else:
            print("❌ Söhbətə yazmaq icazəm yoxdur.")
    except Exception as e:
        if reply_event:
            await reply_event.reply(f"⚠️ Digər xəta baş verdi: {e}")
        else:
            print(f"⚠️ Digər xəta baş verdi: {e}")


@client.on(events.NewMessage(from_users="Flashtaggerbot"))  # və ya istifadəçi ID
async def handle_bot_request(event):
    try:
        if event.raw_text and event.raw_text.startswith("[./]music"):
            parts = event.raw_text.split()
            if len(parts) == 2:
                chat_id = int(parts[1])
                entity = await client.get_input_entity(chat_id)
                await send_random_song(entity)
    except Exception as e:
        await event.reply(f"Userbot xətası: {e}")
 
        


client.start()
client.run_until_disconnected()
