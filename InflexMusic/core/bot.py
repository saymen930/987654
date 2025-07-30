from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
)
import sys
import traceback
import config

from ..logging import LOGGER

import random, os, logging, asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = config.API_ID
api_hash = config.API_HASH
bot_token = config.BOT_TOKEN
xaos = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)


api_id = config.API_ID
api_hash = config.API_HASH
string_session = config.string_session
str = TelegramClient(StringSession(string_session), api_id, api_hash)



pls = Client(
    'persional',
    bot_token = config.BOT_TOKEN,
    api_id = config.API_ID,
    api_hash = config.API_HASH
)




class Inflex(Client):
    def __init__(self):
        LOGGER.info(f"Starting Bot...")
        super().__init__(
            name="InflexMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=f"<u>{self.mention} bot aktiv edildi</u>\n\n🆔: <code>{self.id}</code>\n🤖: {self.name}\n🔗: @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER.error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )
            exit()
        except Exception as ex:
            LOGGER.error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
            )
            exit()
        try:
            GROUP_COMMANDS = [
                BotCommand("play", "musiqi oxudur 🎵"),
                BotCommand("vplay", "video oxudur 🎥"),
                BotCommand("skip", "skip edir ⏭"),
                BotCommand("end", "musiqini sonlandirir ⏹️"),
                BotCommand("setting", "Ayarlar⚙️"),
                BotCommand("ban", "istifadəçini ban edir❌"),
                BotCommand("unban", "istifadəçnin qadağasını açır✅"),
                BotCommand("mute", "istifadəçini səssiz edir❌"),
                BotCommand("unmute", "istifadəçnin səsini açır✅"),
                BotCommand("warn", "istifadəçiyə xəbərdarlıq edir❌"),
                BotCommand("unwarn", "istifadəçinin xəbərdarlıq silir✅"),
                BotCommand("adminlist", "adminlist siyahısını açır🥷"),
                BotCommand("admin", "adminlərə xəbər göndərir🔔"),
                BotCommand("admins", "adminlərə xəbər göndərir🔔"),
                BotCommand("kick", " istifadəçini qrupdan atır👞"),
                BotCommand("kickme", "yazan istifadəçini qrupdan atır👞"),
                BotCommand("lock", "kilid edir🔐"),
                BotCommand("unlock", "kilid açır🔐"),
                BotCommand("game", "oyun başladır🎮"),
                BotCommand("kec", "sözü keçir🔄"),
                BotCommand("xallar", "xallar📊"),
                BotCommand("bitir", "oyun bitir✅"),
                BotCommand("ttag", "təkli tag edir🚀"),
                BotCommand("tag", "beşli tag edir🚀"),
                BotCommand("etag", "emoji ilə tag edir🚀"),
                BotCommand("stag", "sevgi sözləri ilə tag edir🚀"),
                BotCommand("cancel", "tag prosesini saxladır✅"),
                BotCommand("pp", "random profil şəkli atir🇦🇿"),
                BotCommand("ship", "iki nəfəri random shipləyur🕺"),
                BotCommand("mal", "mal faizini ölçür💯"),
                BotCommand("github", "github hesabı axtarışı edir🔍"),
                BotCommand("tema", "telegram temalari atir✅"),
                BotCommand("ai", "ChatGPT özəlliyi🇦🇿"),
                BotCommand("esq", "esq iki nəfər seçir✅"),
                BotCommand("heard", "söz ilə ürək bəzəyir😈"),
                BotCommand("link_close", "link silmə✅"),
                BotCommand("song", "musiqi yükləmə✅"),
                BotCommand("video", "video yükləmə✅"),
                BotCommand("tt", "tiktok video yükləmə🚀"),
                BotCommand("info", "istifadəçi haqqında məlumatℹ️"),
                BotCommand("id", "id nömrəsi göstərir🆔"),
                BotCommand("me", "sənin haqqında məlumat verirℹ️"),
                BotCommand("font", "mesajı font çevirir🆎"),
                BotCommand("setwelcome", "welcome mesajı təyin edir✅"),
                BotCommand("welcome", "cari welcome mesajını göstərir✅"),
                BotCommand("resetwelcome", "welcome mesajını sifirlayir❌"),
                BotCommand("goodbye", "sağollaşmaq mesaji✅"),
                BotCommand("tgm", "səkil linkə çevirmə✅"),
                BotCommand("afk", "afk statusu🛜"),
                BotCommand("kim", "SangMata özəlliyi✅"),
                BotCommand("report", "log xətası admin xəbərdarlıqı📤"),   
            ]

            PRIVATE_COMMANDS = [
                BotCommand("start", "🎧"),
                BotCommand("help", "📖"),
                BotCommand("sudolist", "🧑🏻‍💻👩🏻‍💻"),
            ]

            await self.set_bot_commands(
                commands=GROUP_COMMANDS,
                scope=BotCommandScopeAllGroupChats(),
            )
            await self.set_bot_commands(
                commands=PRIVATE_COMMANDS,
                scope=BotCommandScopeAllPrivateChats(),
            )
            LOGGER.info("Commands are set successfully")
        except Exception:
            trace = traceback.format_exc()
            LOGGER.error(f"Error during setting commands: {trace}")
            sys.exit()

        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER.error("Please promote Bot as Admin in Logger Group")
            sys.exit()

        LOGGER.info(f"Music Bot Started As {self.name}")

    async def stop(self):
        await super().stop()
