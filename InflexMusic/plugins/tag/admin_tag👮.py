import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.enums import ChatMemberStatus
from strings.langs.en import A_Tag_I, A_Tag_SAY, A_Tag_ADMIN, A_Tag_KURUCU, A_Tag_LEGV, A_Tag_Q_A



@app.on_message(filters.command('admins', [".", "!", "@", "/"]))
async def admins(client, message):
    try: 
        adminList = []
        ownerList = []
        async for admin in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if not admin.privileges.is_anonymous:
                if not admin.user.is_bot:
                    if admin.status == ChatMemberStatus.OWNER:
                        ownerList.append(admin.user)
                    else:  
                        adminList.append(admin.user)
        
        lenAdminList = len(ownerList) + len(adminList)  
        text2 = f"{A_Tag_I}\n{A_Tag_Q_A} - {message.chat.title}\n\n"

        try:
            owner = ownerList[0]
            if owner.username is None:
                text2 += f"{A_Tag_KURUCU}\n└ {owner.mention}\n\n{A_Tag_ADMIN}\n"
            else:
                text2 += f"{A_Tag_KURUCU}\n└ @{owner.username}\n\n{A_Tag_ADMIN}\n"
        except:
            text2 += f"{A_Tag_KURUCU}\n└ <i>Hidden</i>\n\n{A_Tag_ADMIN}\n"
        
        if len(adminList) == 0:
            text2 += "└ <i>Admins are hidden</i>"  
            await app.send_message(message.chat.id, text2)   
        else:  
            while len(adminList) > 1:
                admin = adminList.pop(0)
                text2 += f"├ @{admin.username if admin.username else admin.mention}\n"
            else:    
                admin = adminList.pop(0)
                text2 += f"└ @{admin.username if admin.username else admin.mention}\n\n"
            
            text2 += f"{A_Tag_SAY}  {lenAdminList}\n{A_Tag_LEGV}"  
            await app.send_message(message.chat.id, text2)           
    except FloodWait as e:
        await asyncio.sleep(e.value)
