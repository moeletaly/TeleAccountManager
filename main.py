from pyrogram import Client, filters
from db import DB
import json

creds = json.load(open("config.json", "r"))
user = Client("MainAccount", creds["api_id"], creds["api_hash"])
commands = {
    "send_message": "used to send a message to some user/bot, example: /send_message @example hello👋, how are you doing",
    "send_contact": "used to send a contact to some user/bot, example: /send_contact @example me | me = the account contact",
    "click_button": "used to click on a button in a message from a bot\nexample1: /click_button @exampleBot 0 | this will get the last message from a bot and click the first button on the message\nexample2: /click_button @exampleBot Joined✅ | this will get the last message from the bot, and will search the entire conversation for a button with the text Joined✅ and click it",
    "join_chats": "used to join single/multiple chats\nexample: /join_chats @chat1,@chat2,https://t.me/+Sjwwq62 | this will join @chat1, @chat2 and https://t.me/+Sjwwq62 private chat"
}
db = DB()

@user.on_message(filters.me)
async def main_handler(user, m):
    chat_id = m.chat.id
    text = m.text.split()
    com = text[0]
    
    if com == "/commands":
        txt = ""
        for command in commands.keys():
            txt += f"{command}: {commands[command]}\n\n"
        await m.reply(txt)


user.run()