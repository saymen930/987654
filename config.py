import re
import random
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID", "23470912"))
API_HASH = getenv("API_HASH", "33ac02b7891c5396e6b305802d56cf4f")

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN", "7646934610:AAGu9KswDL8qbe1H8Rpkjgblz0bxo_Iuu3w")

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://TEAMBABY01:UTTAMRATHORE09@cluster0.vmjl9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 180))

# Chat id of a group for logging bot's activities
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1002894584465"))

# Get this value from @MissRose_Bot on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", "8085531180"))
OWNER_NAME = getenv("OWNER_NAME", "t.me/XpertMaster")


# Fill Queue Limit . Example - 15
QUEUE_LIMIT = int(getenv("QUEUE_LIMIT", "20"))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", None)
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY", None)

UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/ZumaBotlar")
SUPPORT_GROUP = getenv("SUPPORT_GROUP", "https://t.me/ZumaBotlar")

# Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", None))


# Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None)


# Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))


# Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 104857600))
# Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes


# Get your pyrogram v2 session from Replit
STRING1 = getenv("STRING_SESSION", "AgFmI0AAUML9CRSy3xO76Znk5j0_jqvfL3DhZxklFtWEq-j1-ELKTi1Db1UGLHrYOAQIArtF24VxD7Gdts88ekVn5dPZBpMpQNtJUM18vRAQNUy3B-Kxl1m6h7Ioj9rXzY1Ba3uwBnXlLR781AUa6UD0aiEYRJrGu3p9SFO1kqRQnBo7MJ4rB75v6RTkOl1eeV-gOI0zMIjohw8APEjBVa75GKPxAR1vnpzNLoRJ42kDauxQ9oURvxJHTE5jsdWNaZvbK_hO26zkL0Y5vcb0E5N9vv9i7XmBkAc9-eFktiqG7msKpwEC1rpiwzTMcjL1sY3N7sqF7Tzd9t7FIQFPuoTFbeFPmAAAAAF3bZQuAA")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}


START_IMG_URL = ["https://files.catbox.moe/vnpuan.jpg"]

PING_IMG_URL = "https://files.catbox.moe/vnpuan.jpg"
STATS_IMG_URL = "https://files.catbox.moe/vnpuan.jpg"
PLAYLIST_IMG_URL = getenv(
    "PLAYLIST_IMG_URL", "https://files.catbox.moe/vnpuan.jpg"
)
TELEGRAM_AUDIO_URL = getenv(
    "TELEGRAM_AUDIO_URL", "https://files.catbox.moe/vnpuan.jpg"
)
TELEGRAM_VIDEO_URL = getenv(
    "TELEGRAM_VIDEO_URL", "https://files.catbox.moe/vnpuan.jpg"
)
STREAM_IMG_URL = getenv(
    "STREAM_IMG_URL", "https://files.catbox.moe/vnpuan.jpg"
)
SOUNCLOUD_IMG_URL = getenv(
    "SOUNCLOUD_IMG_URL", "https://files.catbox.moe/vnpuan.jpg"
)
YOUTUBE_IMG_URL = getenv(
    "YOUTUBE_IMG_URL", "https://files.catbox.moe/vnpuan.jpg"
)
SPOTIFY_ARTIST_IMG_URL = getenv(
    "SPOTIFY_ARTIST_IMG_URL", "https://files.catbox.moe/vnpuan.jpg"
)
SPOTIFY_ALBUM_IMG_URL = getenv(
    "SPOTIFY_ALBUM_IMG_URL", "https://files.catbox.moe/vnpuan.jpg"
)
SPOTIFY_PLAYLIST_IMG_URL = getenv(
    "SPOTIFY_PLAYLIST_IMG_URL", "https://files.catbox.moe/vnpuan.jpg"
)


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_GROUP:
    if not re.match("(?:http|https)://", SUPPORT_GROUP):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_GROUP url is wrong. Please ensure that it starts with https://"
        )
