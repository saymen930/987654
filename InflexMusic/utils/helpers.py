# InflexMusic/utils/helpers.py

HELP_1 = """<b><u>ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs :</b></u>

ᴊᴜsᴛ ᴀᴅᴅ <b>ᴄ</b> ɪɴ ᴛʜᴇ sᴛᴀʀᴛɪɴɢ ᴏғ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴜsᴇ ᴛʜᴇᴍ ғᴏʀ ᴄʜᴀɴɴᴇʟ.

...

"""

HELP_2 = """sağol"""
HELP_3 = """öl"""
HELP_4 = """Qac"""
HELP_5 = """..."""
HELP_6 = """..."""
HELP_7 = """..."""
HELP_8 = """..."""
HELP_9 = """..."""
HELP_10 = """..."""
HELP_11 = """..."""
HELP_12 = """..."""
HELP_13 = """..."""
HELP_14 = """..."""
HELP_15 = """..."""

# Əgər istəsən buraya bütün HELP_x dəyişənlərini tam yerləşdir!

def get_string(key: str) -> str:
    """
    Açarın adını HELP_x dəyişənlərindən qaytarır.
    Tapmasa açarı olduğu kimi verir.
    """
    return globals().get(key, key)
