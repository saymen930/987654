from pykeyboard import InlineKeyboard
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, Message, CallbackQuery

from InflexMusic import app
from InflexMusic.utils.database import get_lang, set_lang
from InflexMusic.utils.decorators import ActualAdminCB, language, languageCB
from config import BANNED_USERS
from strings import get_string, languages_present


def lanuages_keyboard(_):
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(
        *[
            (
                InlineKeyboardButton(
                    text=languages_present[i],
                    callback_data=f"languages:{i}",
                )
            )
            for i in languages_present
        ]
    )
    keyboard.row(
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data=f"settingsback_helper",
        ),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
    )
    return keyboard


def dil_xguliyev(_):
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(
        *[
            (
                InlineKeyboardButton(
                    text=languages_present[i],
                    callback_data=f"languages:{i}",
                )
            )
            for i in languages_present
        ]
    )
    keyboard.row(
        InlineKeyboardButton(
            text=_["CLOSE_BUTTON"],
            callback_data=f"settingsback_helper",
        ),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
    )
    return keyboard


@app.on_message(filters.command(["lang", "setlang", "language"]) & ~BANNED_USERS)
@language
async def langs_command(client, message: Message, _):
    keyboard = lanuages_keyboard(_)
    await message.reply_text(
        _["lang_1"],
        reply_markup=keyboard,
    )


"""
@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def lanuagecb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)
"""

# xguliyev
# @app.on_callback_query(filters.regex("DIL") & ~BANNED_USERS & filters.private)
# @languageCB
# async def lanuagecb(client, CallbackQuery, _):
#    try:
#        pass
#    except:
#        pass
#    keyboard = dil_xguliyev(_)
#    return await callback_query.edit_message_text(_["lang_1"])


# @app.on_callback_query(filters.regex("DL") & ~BANNED_USERS & filters.private)
@app.on_callback_query(filters.regex(r"kapat") & ~BANNED_USERS & filters.private)
@languageCB
async def callback_handler(client, callback_query):
    chat_id = callback_query.message.chat.id  # Sohbetin ID'sini alın
    chat_type = await client.get_chat_member(
        chat_id, "me"
    )  # Botun bu sohbetteki üye bilgisini alın
    await callback_query.answer("Düğmeye basıldı!")
    await callback_query.edit_message_text("Düğmeye basıldı!")


@app.on_callback_query(filters.regex("BASICBOTS") & ~BANNED_USERS)
@languageCB
async def callback_handler(client: Client, cb: CallbackQuery, _):
    keyboard = lanuages_keyboard(_)
    await cb.message.edit(
        _["lang_1"],
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
@ActualAdminCB
async def language_markup(client, CallbackQuery, _):
    langauge = (CallbackQuery.data).split(":")[1]
    old = await get_lang(CallbackQuery.message.chat.id)
    if str(old) == str(langauge):
        return await CallbackQuery.answer(_["lang_4"], show_alert=True)
    try:
        _ = get_string(langauge)
        await CallbackQuery.answer(_["lang_2"], show_alert=True)
    except:
        _ = get_string(old)
        return await CallbackQuery.answer(
            _["lang_3"],
            show_alert=True,
        )
    await set_lang(CallbackQuery.message.chat.id, langauge)
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)
