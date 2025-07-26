import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from InflexMusic import app
from pyrogram.enums import ChatMemberStatus


@app.on_message(filters.command('admin', [".", "!", "@", "/"]))
async def admins(client, message):
  try: 
    adminList = []
    ownerList = []
    async for admin in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
      if admin.privileges.is_anonymous == False:
        if admin.user.is_bot == True:
          pass
        elif admin.status == ChatMemberStatus.OWNER:
          ownerList.append(admin.user)
        else:  
          adminList.append(admin.user)
      else:
        pass   
    lenAdminList= len(ownerList) + len(adminList)  
    text2 = f"👮‍♂️ QRUP İDARƏÇİLƏRİ VƏ ADMİNLƏRİ\n📎 QRUP - {message.chat.title}\n\n"
    try:
      owner = ownerList[0]
      if owner.username == None:
        text2 += f"👑 Kurucu\n└ {owner.mention}\n\n👮🏻 Admin\n"
      else:
        text2 += f"👑 Kurucu\n└ @{owner.username}\n\n👮🏻 Admin\n"
    except:
      text2 += f"👑 Kurucu\n└ <i>Hidden</i>\n\n👮🏻 Admin\n"
    if len(adminList) == 0:
      text2 += "└ <i>Admins are hidden</i>"  
      await app.send_message(message.chat.id, text2)   
    else:  
      while len(adminList) > 1:
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"├ {admin.mention}\n"
        else:
          text2 += f"├ @{admin.username}\n"    
      else:    
        admin = adminList.pop(0)
        if admin.username == None:
          text2 += f"└ {admin.mention}\n\n"
        else:
          text2 += f"└ @{admin.username}\n\n"
      text2 += f"✅ | Toplam İdarəçi Sayı: {lenAdminList}\n❌ | Botlar Və Gizli Yönəticilər Iəğv Edildi"  
      await app.send_message(message.chat.id, text2)           
  except FloodWait as e:
    await asyncio.sleep(e.value)
    
    
