import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID", "22920799"))
api_hash = os.environ.get("API_HASH", "e6226116f74ba8dc1ceae2d572a39d80")
bot_token = os.environ.get("TOKEN", "8103483580:AAFbwuHz1pUQsfDPrNm6lAeHpqm6O16u-_U")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/tagstart$"))
async def start(event):
  await event.reply(
    "__**I'm MentionAll Bot**, I can mention almost all members in group or channel 👻\nClick **/help** for more information__\n\n Follow [@AnjanaMadu](https://github.com/AnjanaMadu) on Github",
    link_preview=False,
    buttons=(
      [
        Button.url('📣 Channel', 'https://t.me/JasaSiArab'),
        Button.url('📦 Source', 'https://t.me/Dhilnihnge')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/taghelp$"))
async def help(event):
  helptext = "**Help Menu of MentionAllBot**\n\nCommand: /mentionall\n__You can use this command with text what you want to mention others.__\n`Example: /mentionall Good Morning!`\n__You can you this command as a reply to any message. Bot will tag users to that replied messsage__.\n\nFollow [@AnjanaMadu](https://github.com/AnjanaMadu) on Github"
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('📣 Channel', 'https://t.me/JasaSiArab'),
        Button.url('📦 Source', 'https://t.me/Dhilnihnge')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/tagall ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("<b>ᴘᴇʀɪɴᴛᴀʜ ɪɴɪ ᴅᴀᴘᴀᴛ ᴅɪɢᴜɴᴀᴋᴀɴ ᴅᴀʟᴀᴍ ɢʀᴜᴘ ᴅᴀɴ ᴄʜᴀɴɴᴇʟ!!</b>")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("ʜᴀɴʏᴀ ᴀᴅᴍɪɴ ʏᴀɴɢ ʙɪꜱᴀ ɴɢᴇᴛᴀɢᴀʟʟ!")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("ᴋᴀꜱɪʜ ꜱᴀʏᴀ ᴘᴇʀɪɴᴛᴀʜ ʏᴀɴɢ ᴊᴇʟᴀꜱ!")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("ɢᴜᴀ ɢᴀ ʙɪꜱᴀ ɴɢᴇᴛᴀɢᴀʟʟ ᴘᴇꜱᴀɴ ʏᴀɴɢ ᴜᴅᴀʜ ʟᴀᴍᴀ ʙʟᴏᴋ")
  else:
    return await event.respond("ᴋᴀꜱɪʜ ᴘᴇꜱᴀɴ ᴀᴛᴀᴜ ʀᴇᴘʟʏ ᴋᴇ ᴘᴇꜱᴀɴ ᴋᴀʟᴏ ᴍᴀᴜ ᴛᴀɢᴀʟʟ ʙᴏᴅᴏʜ!!")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"🗿[{usr.first_name}](tg://user?id={usr.id}) \n"
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/stop$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('ᴜᴅᴀʜ ɢᴀ ᴀᴅᴀ ᴛᴀɢᴀʟʟ ʙᴏᴅᴏʜ...')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('ᴛᴀɢᴀʟʟ-ɴʏᴀ ᴜᴅᴀʜ ʙᴇʀᴇɴᴛɪ ᴍᴇᴋ')

print(">> BOT STARTED <<")
client.run_until_disconnected()
