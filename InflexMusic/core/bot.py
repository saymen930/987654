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


class Inflex(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
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
                text=f"<u>{self.mention} bot aktiv edildi</b><u>\n\n🆔: <code>{self.id}</code>\n🤖: {self.name}\n🔗: @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
            )
            exit()
        try:
            GROUP_COMMANDS = [
                # BotCommand("start", "🎧 Botu başlatır"),
                BotCommand("play", "🎶"),
                BotCommand("vplay", "🎥"),
                BotCommand("skip", "⏭"),
                BotCommand("end", "⏹"),
                BotCommand("setting", "⚙️"),
                BotCommand("lang", "🇦🇿🇹🇷🇷🇺"),
                ]

            PRIVATE_COMMANDS = [
            BotCommand("start", "🎧"), 
            BotCommand("help", "📖"),
            BotCommand("sudolist", "🧑🏻‍💻👩🏻‍💻"),
            ]
            await self.set_bot_commands(  # * Group Commands
                commands=GROUP_COMMANDS,
                scope=BotCommandScopeAllGroupChats(),
            )
            await self.set_bot_commands(  # * Private Commands
                commands=PRIVATE_COMMANDS,
                scope=BotCommandScopeAllPrivateChats(),
            )
            LOGGER(__name__).info("Commands are set successfully")
        except Exception as e:
            trace = traceback.format_exc()
            LOGGER(__name__).error(f"Error during setting commands: {trace}")
            sys.exit()
        else:
            pass

            a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("Please promote Bot as Admin in Logger Group")
                sys.exit()        
        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote your bot as an admin in your log group/channel."
            )
            exit()
        LOGGER(__name__).info(f"Music Bot Started As {self.name}")

    async def stop(self):
        await super().stop()
