import asyncio

from pyrogram import Client as c

API_ID = "24357907"
API_HASH = "e8bbafbec8541225f8e2c5a94af3d040"

print("\n\n Enter Phone number when asked.\n\n")

i = c("vipstring", in_memory=True, api_id=API_ID, api_hash=API_HASH)


async def main():
    await i.start()
    ss = await i.export_session_string()
    xx = f"HERE IS YOUR STRING SESSION, COPY IT, DON'T SHARE!!\n\n`{ss}`\n\n STRING GENERATED"
    ok = await i.send_message("me", xx)
    print("\nHERE IS YOUR STRING SESSION, COPY IT, DON'T SHARE!!\n")
    print(f"\n{ss}\n")
    print("\n STRING GENERATED\n")


asyncio.run(main())
