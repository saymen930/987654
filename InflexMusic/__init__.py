from InflexMusic.core.bot import Inflex
from InflexMusic.core.dir import dirr
from InflexMusic.core.userbot import Userbot
from InflexMusic.misc import dbb, heroku

from .logging import LOGGER

# Lazım olsa main.py-də çağır
dirr()
dbb()
heroku()

app = Inflex()
userbot = Userbot()

from .platforms import (
    AppleAPI,
    SoundAPI,
    SpotifyAPI,
    RessoAPI,
    TeleAPI,
    YouTubeAPI
)

from .owner import OWNER_ID

Apple = AppleAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
