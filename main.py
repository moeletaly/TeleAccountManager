from pyrogram import Client, filters
from db import DB
from tools import *
import asyncio
import json

creds = json.load(open("mconfig.json", "r"))
user = Client("MainAccount", creds["api_id"], creds["api_hash"])
commands = {
    "send_message": "used to send a message to some user/bot, example: /send_message @example hello👋, how are you doing",
    "send_contact": "used to send a contact to some user/bot, example: /send_contact @example me | me = the account contact",
    #"click_button": "used to click on a button in a message from a bot\nexample1: /click_button @exampleBot 0 | this will get the last message from a bot and click the first button on the message\nexample2: /click_button @exampleBot Joined✅ | this will get the last message from the bot, and will search the entire conversation for a button with the text Joined✅ and click it",
    "join_chats": "used to join single/multiple chats\nexample: /join_chats @chat1|@chat2|https://t.me/+Sjwwq62 | this will join @chat1, @chat2 and https://t.me/+Sjwwq62 private chat",
    "ref": "emp"
}
db = DB()

@user.on_message(filters.text & filters.me)
async def main_handler(user, m):
    chat_id = m.chat.id
    text = m.text.split()
    com = text[0]
    
    if com == "/commands":
        txt = ""
        for command in commands.keys():
            txt += f"{command}: {commands[command]}\n\n"
        await m.reply(txt)
    
    elif com == "/send_message":
        try:
            num = text[1]
            username = text[2]
            txt = m.text[13+len(username)+len(num)+2:]#.replace(text[0], "").replace(text[1], "")
            asyncio.create_task(basic_animation(m))
            await refresh()
            task = asyncio.create_task(send_message(num, username, txt))
            await task
            await m.reply(f"Done {task.result()[1]}/{task.result()[2]}✅")
        except IndexError:
            await m.reply("No Enough Arguments!")
    
    elif com == "/send_contact":
        try:
            num = text[1]
            username = text[2]
            contact_info = text[3]
            asyncio.create_task(basic_animation(m))
            await refresh()
            task = asyncio.create_task(send_contact(num, username, contact_info))
            await task
            await m.reply(f"Done {task.result()[1]}/{task.result()[2]}✅")
        except IndexError:
            await m.reply("No Enough Arguments!")
    
    elif com == "/join_chats":
        try:
            num = text[1]
            chats = text[2].split("|")
            asyncio.create_task(basic_animation(m))
            await refresh()
            task = asyncio.create_task(join_chats(num, chats))
            await task
            await m.reply(f"Done ✅, Results:\njoined: {task.result()[1]}\nfailed to join: {task.result()[0]}\nAlready joined: {task.result()[3]}")
        except IndexError:
            await m.reply("No Enough Arguments!")
    
    elif com == "/ref":
        try:
            num = text[1]
            lnk = text[2]
            asyncio.create_task(basic_animation(m))
            await refresh()
            task = asyncio.create_task(send_refs(num, lnk))
            await task
            await m.reply(f"Done {task.result()[1]}/{task.result()[2]}✅")
        except IndexError:
            await m.reply("No Enough Arguments!")

user.run()