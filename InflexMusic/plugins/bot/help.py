from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

from InflexMusic import app
from InflexMusic.utils import help_pannel
from InflexMusic.utils.database import get_lang
from InflexMusic.utils.decorators.language import LanguageStart, languageCB
from InflexMusic.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_GROUP
from strings import get_string, helpers


@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_GROUP), reply_markup=keyboard
        )
    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_)
        await update.reply(
            text=_["help_1"].format(SUPPORT_GROUP),
            reply_markup=keyboard,
        )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = help_back_markup(_)
    if cb == "hb1":
        await CallbackQuery.edit_message_text(_["musiqis"], reply_markup=keyboard)
    elif cb == "hb2":
        await CallbackQuery.edit_message_text(_["nezarets"], reply_markup=keyboard)
    elif cb == "hb3":
        await CallbackQuery.edit_message_text(_["nosoyus"], reply_markup=keyboard)
    elif cb == "hb4":
        await CallbackQuery.edit_message_text(_["oyuns"], reply_markup=keyboard)
    elif cb == "hb5":
        await CallbackQuery.edit_message_text(_["taggers"], reply_markup=keyboard)
    elif cb == "hb6":
        await CallbackQuery.edit_message_text(_["eylences"], reply_markup=keyboard)
    elif cb == "hb7":
        await CallbackQuery.edit_message_text(_["nolinks"], reply_markup=keyboard)
    elif cb == "hb8":
        await CallbackQuery.edit_message_text(_["antispams"], reply_markup=keyboard)
    elif cb == "hb9":
        await CallbackQuery.edit_message_text(_["songs"], reply_markup=keyboard)
    elif cb == "hb10":
        await CallbackQuery.edit_message_text(_["infos"], reply_markup=keyboard)   
    elif cb == "hb11":
        await CallbackQuery.edit_message_text(_["fonts"], reply_markup=keyboard) 
    elif cb == "hb12":
        await CallbackQuery.edit_message_text(_["welcomes"], reply_markup=keyboard) 
    elif cb == "hb13":
        await CallbackQuery.edit_message_text(_["telegraphs"], reply_markup=keyboard) 
    elif cb == "hb14":
        await CallbackQuery.edit_message_text(_["afks"], reply_markup=keyboard)
    elif cb == "hb15":
        await CallbackQuery.edit_message_text(_["songmatas"], reply_markup=keyboard) 
    elif cb == "hb16":
        await CallbackQuery.edit_message_text(_["downloads"], reply_markup=keyboard) 
