from pyrogram import Client
import config
from ..logging import LOGGER

assistants = []
assistantids = []

class Userbot:
    def __init__(self):
        self.one = Client("InflexAss1", config.API_ID, config.API_HASH, session_string=str(config.STRING1), no_updates=True)
        self.two = Client("InflexAss2", config.API_ID, config.API_HASH, session_string=str(config.STRING2), no_updates=True)
        self.three = Client("InflexAss3", config.API_ID, config.API_HASH, session_string=str(config.STRING3), no_updates=True)
        self.four = Client("InflexAss4", config.API_ID, config.API_HASH, session_string=str(config.STRING4), no_updates=True)
        self.five = Client("InflexAss5", config.API_ID, config.API_HASH, session_string=str(config.STRING5), no_updates=True)

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...")

        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("basicbots")
                await self.one.join_chat("gizliplanet")
            except:
                pass
            assistants.append(1)
            try:
                await self.one.send_message(config.LOG_GROUP_ID, "Assistent aktiv edildi")
            except:
                LOGGER(__name__).error("Assistant 1 log qrupuna çata bilmir. Admin et.")
                exit()
            me = await self.one.get_me()
            self.one.id = me.id
            self.one.name = me.mention
            self.one.username = me.username
            assistantids.append(me.id)
            LOGGER(__name__).info(f"Assistant 1: {me.first_name}")

        if config.STRING2:
            await self.two.start()
            try:
                await self.two.join_chat("basicbots")
                await self.two.join_chat("gizliplanet")
            except:
                pass
            assistants.append(2)
            try:
                await self.two.send_message(config.LOG_GROUP_ID, "Assistent aktiv edildi")
            except:
                LOGGER(__name__).error("Assistant 2 log qrupuna çata bilmir.")
                exit()
            me = await self.two.get_me()
            self.two.id = me.id
            self.two.name = me.mention
            self.two.username = me.username
            assistantids.append(me.id)
            LOGGER(__name__).info(f"Assistant 2: {me.first_name}")

        if config.STRING3:
            await self.three.start()
            try:
                await self.three.join_chat("basicbots")
                await self.three.join_chat("gizliplanet")
            except:
                pass
            assistants.append(3)
            try:
                await self.three.send_message(config.LOG_GROUP_ID, "Assistent aktiv edildi")
            except:
                LOGGER(__name__).error("Assistant 3 log qrupuna çata bilmir.")
                exit()
            me = await self.three.get_me()
            self.three.id = me.id
            self.three.name = me.mention
            self.three.username = me.username
            assistantids.append(me.id)
            LOGGER(__name__).info(f"Assistant 3: {me.first_name}")

        if config.STRING4:
            await self.four.start()
            try:
                await self.four.join_chat("basicbots")
                await self.four.join_chat("gizliplanet")
            except:
                pass
            assistants.append(4)
            try:
                await self.four.send_message(config.LOG_GROUP_ID, "Assistent aktiv edildi")
            except:
                LOGGER(__name__).error("Assistant 4 log qrupuna çata bilmir.")
                exit()
            me = await self.four.get_me()
            self.four.id = me.id
            self.four.name = me.mention
            self.four.username = me.username
            assistantids.append(me.id)
            LOGGER(__name__).info(f"Assistant 4: {me.first_name}")

        if config.STRING5:
            await self.five.start()
            try:
                await self.five.join_chat("basicbots")
                await self.five.join_chat("gizliplanet")
            except:
                pass
            assistants.append(5)
            try:
                await self.five.send_message(config.LOG_GROUP_ID, "Assistent aktiv edildi")
            except:
                LOGGER(__name__).error("Assistant 5 log qrupuna çata bilmir.")
                exit()
            me = await self.five.get_me()
            self.five.id = me.id
            self.five.name = me.mention
            self.five.username = me.username
            assistantids.append(me.id)
            LOGGER(__name__).info(f"Assistant 5: {me.first_name}")

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except:
            pass
