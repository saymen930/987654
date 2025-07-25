
import os

class Config:

   API_ID = int(os.getenv("API_ID", "27804609"))
   API_HASH = os.getenv("API_HASH", "e27685923fc24e08591caff39e764bbd")
   BOT_TOKEN = os.getenv("BOT_TOKEN", "7539501739:AAHhwIlR87EkMlC5h3D_wVN01Y8Uz3D5Aro")
   BOT_USERNAME = os.environ.get("BOT_USERNAME", "Ahaahaah7bot")
   BOT_NAME = os.environ.get("BOT_NAME", "Ahahha")   
   OWNER_ID = int(os.environ.get("OWNER_ID","7926847490"))
   OWNER_NAME = os.environ.get("OWNER_NAME", "X7Miro") 
   GONDERME_TURU = bool(os.environ.get("GONDERME_TURU", "False"))
   MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb+srv://TEAMBABY01:UTTAMRATHORE09@cluster0.vmjl9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
   LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002606202136"))
   PLAYLIST_NAME = os.environ.get("PLAYLIST_NAME", "Oa")
   PLAYLIST_ID = int(os.environ.get("PLAYLIST_ID", "-1002606202136"))
   BAN_GROUP = int(os.environ.get("BAN_GROUP", "-1002606202136"))
   HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", "HRKU-AAwNu2aaHv0TKXSUaUJ6gxk_XODl79TyKs0giLl-RsFQ_wx11gGHU63r")
   ALIVE_NAME = os.environ.get("ALIVE_NAME", "Miro")
   CHANNEL = os.environ.get("CHANNEL", "MiroBotlar")
   SUPPORT = os.environ.get("SUPPORT", "MiroBotlar")
   ALIVE_IMG = os.environ.get("ALIVE_IMG", "https://files.catbox.moe/0s1wpb.jpg") 
   START_IMG = os.environ.get("START_IMG", "https://files.catbox.moe/eahk6i.jpg")
   COMMAND_PREFIXES = list(os.environ.get("COMMAND_PREFIXES", "/ ! .").split())
