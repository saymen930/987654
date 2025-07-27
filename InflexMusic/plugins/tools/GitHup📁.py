import aiohttp
from telethon import events
from InflexMusic.core.bot import xaos as client  # səndə necədirsə onu istifadə et

def _nz(v, default="-"):
    return v if v not in (None, "", "null") else default

# /github, .github, !github, @github və s. üçün
@client.on(events.NewMessage(pattern=r"^[./!@]?github(?:\s+(\S+))?$"))
async def github_lookup(event: events.NewMessage.Event):
    username = (event.pattern_match.group(1) or "").strip()

    if not username:
        return await event.reply("/github <istifadəçi_adı> yazmadınız 😐")

    url = f"https://api.github.com/users/{username}"

    await event.reply("⏳ Məlumat yüklənir...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 404:
                    return await event.reply("❌ İstifadəçi tapılmadı (404).")
                if resp.status != 200:
                    return await event.reply(f"❌ GitHub API xəta qaytardı: {resp.status}")
                data = await resp.json()

        profile_url = data.get("html_url")
        name        = _nz(data.get("name"), username)
        company     = _nz(data.get("company"))
        bio         = _nz(data.get("bio"))
        created_at  = _nz(data.get("created_at"))
        avatar_url  = data.get("avatar_url")
        blog        = _nz(data.get("blog"))
        location    = _nz(data.get("location"))
        repos       = data.get("public_repos", 0)
        followers   = data.get("followers", 0)
        following   = data.get("following", 0)

        caption = (
            f"**Info Of {name}**\n"
            f"👨🏻‍💻İstifadəçi adı: `{username}`\n"
            f"🗣️Bio: {bio}\n"
            f"🔗Profil linki: [Here]({profile_url})\n"
            f"👤Şirkət: {company}\n"
            f"📅Yaradılma tarixi: {created_at}\n"
            f"📔Depolar: {repos}\n"
            f"🛄Blog: {blog}\n"
            f"🌐Məkan: {location}\n"
            f"👁️‍🗨️İzləyicilər: {followers}\n"
            f"👁️‍🗨️İzlədikləri: `{following}`"
        )

        if avatar_url:
            await client.send_file(
                event.chat_id,
                avatar_url,
                caption=caption,
                parse_mode="md"
            )
        else:
            await event.reply(caption, parse_mode="md")

    except Exception as e:
        await event.reply(f"⚠️ Xəta baş verdi:\n`{e}`", parse_mode="md")
