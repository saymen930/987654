from telethon import events
from InflexMusic.core.bot import xaos as Zaid
import functools

# Yalnız adminlər üçün dekorator
def is_admin(func):
    @functools.wraps(func)
    async def a_c(event):
        try:
            if event.is_private:
                await event.reply("❌ Bu əmri yalnız qruplarda istifadə edə bilərsiniz.")
                return

            perm = await event.client.get_permissions(event.chat_id, event.sender_id)
            if perm.is_admin:
                await func(event, perm)
            else:
                await event.reply("❌ Bu əmri yalnız adminlər istifadə edə bilər.")
        except Exception:
            await event.reply("❌ Səlahiyyət yoxlanarkən xəta baş verdi.")
    return a_c


@Zaid.on(events.NewMessage(pattern=r"^[!/.]lock ?(.*)"))
@is_admin
async def lock(event, perm):
    if getattr(Config, "MANAGEMENT_MODE", "DISABLE") == "ENABLE":
        return

    if not perm.change_info:
        await event.reply("❌ Bu əmri istifadə etmək üçün `change_info` icazən yoxdur.")
        return

    input_str = event.pattern_match.group(1).lower()
    if not input_str:
        await event.reply("Kilidləmək üçün növü müəyyən etmədiniz.")
        return

    if "all" in input_str:
        await Zaid.edit_permissions(
            event.chat_id,
            send_messages=False,
            send_media=False,
            send_stickers=False,
            send_gifs=False,
            send_games=False,
            send_inline=False,
            send_polls=False,
            embed_link_previews=False,
        )
        await event.reply("🔐 Chat bağlandı.")


@Zaid.on(events.NewMessage(pattern=r"^[!/.]unlock ?(.*)"))
@is_admin
async def unlock(event, perm):
    if getattr(Config, "MANAGEMENT_MODE", "DISABLE") == "ENABLE":
        return

    if not perm.change_info:
        await event.reply("❌ Bu əmri istifadə etmək üçün `change_info` icazən yoxdur.")
        return

    input_str = event.pattern_match.group(1).lower()
    if not input_str:
        await event.reply("Kilidi açmaq üçün növü müəyyən etmədiniz.")
        return

    if "all" in input_str:
        await Zaid.edit_permissions(
            event.chat_id,
            send_messages=True,
            send_media=True,
            send_stickers=True,
            send_gifs=True,
            send_games=True,
            send_inline=True,
            send_polls=True,
            embed_link_previews=True,
        )
        await event.reply("🔓 Chat açıldı.")


LOCK_TEXT = """
**Lock Növləri:**

‣ all
"""

@Zaid.on(events.NewMessage(pattern=r"^[!/.]locktypes"))
async def locktypes(event):
    await event.reply(LOCK_TEXT)
