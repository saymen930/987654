import asyncio
from datetime import datetime, timedelta
from collections import defaultdict
from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.messages import DeleteMessagesRequest
from telethon.tl.types import ChatBannedRights
from InflexMusic.core.bot import xaos as bot

# Flood konfiqurasiya və loglar
flood_settings = defaultdict(lambda: {
    "limit": 5,
    "timer": None,
    "action": ("mute", None),
    "clear": True
})

message_log = defaultdict(lambda: defaultdict(list))  # chat_id -> user_id -> [timestamps]


async def is_admin(chat, user_id):
    try:
        participant = await bot.get_participant(chat, user_id)
        return participant.participant.__class__.__name__ in ["ChannelParticipantAdmin", "ChannelParticipantCreator"]
    except Exception:
        return False


@bot.on(events.NewMessage)
async def flood_control(event):
    if not event.is_group or event.out or not event.sender_id:
        return

    chat_id = event.chat_id
    user_id = event.sender_id
    config = flood_settings[chat_id]
    now = datetime.utcnow()

    log = message_log[chat_id][user_id]
    log.append(now)
    if len(log) > 10:
        log.pop(0)

    # Sadə flood
    if config["limit"] and len(log) >= config["limit"]:
        if all((now - t).total_seconds() < 3 for t in log[-config["limit"]:]):
            await punish_user(event, config)
            if config["clear"]:
                await delete_user_msgs(event, user_id)
            message_log[chat_id][user_id].clear()

    # Timer əsaslı flood
    if config["timer"]:
        count, duration = config["timer"]
        valid = [t for t in log if (now - t).total_seconds() <= duration]
        if len(valid) >= count:
            await punish_user(event, config)
            if config["clear"]:
                await delete_user_msgs(event, user_id)
            message_log[chat_id][user_id].clear()


async def punish_user(event, config):
    user_id = event.sender_id
    chat_id = event.chat_id
    action, duration = config["action"]

    rights = ChatBannedRights(until_date=None, send_messages=True)
    until = None

    try:
        if action == "kick":
            await bot.kick_participant(chat_id, user_id)
            await bot.invite_to_channel(chat_id, [user_id])
        elif action == "ban":
            await bot(EditBannedRequest(chat_id, user_id, rights))
        elif action == "tban":
            until = datetime.utcnow() + duration
            await bot(EditBannedRequest(chat_id, user_id, ChatBannedRights(until_date=until, send_messages=True)))
        elif action == "mute":
            await bot(EditBannedRequest(chat_id, user_id, rights))
        elif action == "tmute":
            until = datetime.utcnow() + duration
            await bot(EditBannedRequest(chat_id, user_id, ChatBannedRights(until_date=until, send_messages=True)))

        await event.reply(f"⚠️ Flood aşkarlandı və istifadəçiyə `{action}` tədbiri tətbiq olundu.")
    except Exception as e:
        await event.reply(f"🚫 Tədbir tətbiq edilə bilmədi: `{str(e)}`")


async def delete_user_msgs(event, user_id):
    msgs = []
    async for msg in bot.iter_messages(event.chat_id, limit=100):
        if msg.sender_id == user_id:
            msgs.append(msg.id)
    if msgs:
        await bot(DeleteMessagesRequest(event.chat_id, msgs))


@bot.on(events.NewMessage(pattern=r'^/setflood(?:\s+(\w+))?'))
async def set_flood(event):
    if not await is_admin(event.chat_id, event.sender_id):
        return
    arg = event.pattern_match.group(1)
    if arg in ("off", "no", "0"):
        flood_settings[event.chat_id]["limit"] = None
        await event.reply("✅ Sadə antiflood deaktiv edildi.")
    elif arg and arg.isdigit():
        flood_settings[event.chat_id]["limit"] = int(arg)
        await event.reply(f"✅ Sadə antiflood limiti `{arg}` olaraq təyin edildi.")


@bot.on(events.NewMessage(pattern=r'^/setfloodtimer\s+(\d+)\s+(\d+[smh])'))
async def set_floodtimer(event):
    if not await is_admin(event.chat_id, event.sender_id):
        return
    count = int(event.pattern_match.group(1))
    time_val = event.pattern_match.group(2)
    duration = int(time_val[:-1])
    unit = time_val[-1]
    if unit == "m":
        duration *= 60
    elif unit == "h":
        duration *= 3600
    flood_settings[event.chat_id]["timer"] = (count, duration)
    await event.reply(f"✅ Timer flood: {count} mesaj / {duration} saniyə")


@bot.on(events.NewMessage(pattern=r'^/floodmode\s+(\w+)(?:\s+(\d+[smhd]))?'))
async def set_floodmode(event):
    if not await is_admin(event.chat_id, event.sender_id):
        return
    action = event.pattern_match.group(1)
    duration_str = event.pattern_match.group(2)
    duration = None

    if duration_str:
        value = int(duration_str[:-1])
        unit = duration_str[-1]
        if unit == "s":
            duration = timedelta(seconds=value)
        elif unit == "m":
            duration = timedelta(minutes=value)
        elif unit == "h":
            duration = timedelta(hours=value)
        elif unit == "d":
            duration = timedelta(days=value)

    flood_settings[event.chat_id]["action"] = (action, duration)
    await event.reply(f"✅ Antiflood tədbiri `{action}` olaraq təyin edildi.")


@bot.on(events.NewMessage(pattern=r'^/clearflood\s+(\w+)'))
async def clearflood(event):
    if not await is_admin(event.chat_id, event.sender_id):
        return
    arg = event.pattern_match.group(1).lower()
    flood_settings[event.chat_id]["clear"] = arg in ("yes", "on")
    await event.reply(f"🧹 Flood mesajlarının silinməsi: {'aktiv' if arg in ('yes', 'on') else 'deaktiv'}")


@bot.on(events.NewMessage(pattern=r'^/flood$'))
async def show_flood(event):
    config = flood_settings[event.chat_id]
    text = (
        f"🔧 Antiflood Ayarları:\n"
        f"- Limit: {config['limit'] or 'off'}\n"
        f"- Timer: {config['timer'] or 'off'}\n"
        f"- Action: {config['action'][0]}\n"
        f"- Clear: {'yes' if config['clear'] else 'no'}"
    )
    await event.reply(text)
