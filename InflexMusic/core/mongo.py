from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_DB_URI

from ..logging import LOGGER

LOGGER(name).info("Connecting to your Mongo Database...")

try:
mongo_async = AsyncIOMotorClient(MONGO_DB_URI)
mongodb = mongo_async.ByMidoffMusicBot
LOGGER(name).info("Connected to your Mongo Database.")
except:
LOGGER(name).error("Failed to connect to your Mongo Database.")
exit()
