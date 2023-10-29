from pyrogram import Client, errors
from pyrogram.errors import BadRequest, Unauthorized, FloodWait, SessionPasswordNeeded
from db import DB
from datetime import datetime
import asyncio
import json

r,g,w = "\033[1;31;40m", "\033[1;32;40m>> ", "\033[0;40m"
db = DB()

def log(error):
    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    err = {"error": str(error), "time": time}
    with open("errors.txt", "a+") as file:
        file.write(json.dumps(err, indent=4) + "\n")
        file.close()


async def binput(text):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, text)


async def create_account():
    creds = json.load(open("config.json", "r"))
    password=""
    print(f"{r}Type phone number with +\nExample: +2018421981{w}")
    phone_number = await binput(g)
    if not db.check_exist(phone_number):
        app = Client(phone_number, creds["api_id"], creds["api_hash"], device_model="AccountManager")
        try:
            await app.connect()
            sent_code = await app.send_code(phone_number)
            print(f"{r}Type the code that has been sent to you✉️{w}")
            code = await binput(g)
            do_it = True
            try:
    	        await app.sign_in(phone_number=phone_number, phone_code_hash=sent_code.phone_code_hash, phone_code=code)
            except BadRequest:
    	        print("\033[1;31;40mCode Invalid!!, type it again\033[0;40m")
    	        code = await binput(g)
    	        while True:
    	            try:
    	                print("\033[1;31;40mChecking Code💬\033[0;40m")
    	                await app.sign_in(phone_number=phone_number, phone_code_hash=sent_code.phone_code_hash, phone_code=code)
    	                print('\033[1;31;40mCorrect Code✅\033[0;40m')
    	                break
    	            except BadRequest:
    	                print("\033[1;31;40mCode Invalid!!, type it again")
    	                code = await binput(g)
    	            except SessionPasswordNeeded:
    	                break
    	            except Exception as e:
    	                log(e)
    	                do_it=False
    	                break
    	            
            except SessionPasswordNeeded:
    	        while True:
        	       try:
        	           print('\033[1;31;40mChecking Password🔑\033[0;40m')
        	           await app.check_password(password)
        	           break
        	       except BadRequest as e:
        	            if e.ID == "PASSWORD_HASH_INVALID":
        	                print(f"{r}Password Invalid🔑❌ Send Password:{w}")
        	                password = await binput(g) 
        	            else:
        	                log(e.ID)
        	                do_it=False
        	                break
        	       except Exception as e:
        	            do_it=False
        	            break

            if do_it:
                 session_string = ""
                 if not db.check_exist(phone_number):
                     session_string = await app.export_session_string()
                 try:
                     await app.disconnect()
                 except:
                     pass
                
                 db.add_account(phone_number, session_string, password)
                 print(f"\033[1;32;40mSigned in to {phone_number} Successfully✅\033[0;40m")
            else:
                 print("\033[1;31;40mFailed to login❗\033[0;40m")
        except Exception as e:
            log(e)
            print(f"{r}Phone number Invalid{w}")
    else:
    	print(f"{r}Account Already In DB!{w}")

async def refresh():
    accs = db.get_accounts()
    n=0
    m=0
    for acc in accs.keys():
        app = Client("user", session_string=accs[acc])
        try:
            await app.connect()
            await app.send_message("me", "Ping")
            await app.disconnect()
        except errors.AuthKeyUnregeisterd:
            db.delete_account(acc)
            n+=1
        except errors.SessionRevoked:
            db.delete_account(acc)
            n+=1
        except errors.UserDeactivated:
            db.delete_account(acc)
            m+=1
        except errors.UserDeactivatedBan:
            db.delete_account(acc)
            m+=1
    if m+n > 0:
        print(f"{r}Deleted {n+m} ACCOUNTS🛑{w}")
        print(f"{r}SignOut: {n}\nBanned: {m}{w}")

async def basic_animation(message):
    new_message = await message.reply("Refreshing")
    n = 0
    for i in range(12):
        n+=1
        if n == 4:
            n = 1
        await new_message.edit_text(f"Refreshing{n*'.'}")

async def send_message(max, username, text):
    accs = db.get_accounts()
    s = 0
    f = 0
    n = 0
    if max == "max":
        max = float("inf")
    else:
        max = int(max)
    for acc in accs.keys():
        if n <= max:
            app = Client("user", session_string=accs[acc])
            await app.connect()
            try:
                await app.send_message(username, text)
                s+=1
            except:
                f += 1
                pass
            await app.disconnect()
            n+=1
        else:
            break
    return [f, s, n]

async def send_contact(max, username, contact):
    accs = db.get_accounts()
    s = 0
    f = 0
    n = 0
    if max == "max":
        max = float("inf")
    else:
        max = int(max)
    for acc in accs.keys():
        if n <= max:
            app = Client("user", session_string=accs[acc])
            await app.connect()
            try:
                l = []
                if contact.lower().strip() == "me":
                    app.me = await app.get_me()
                    l = [app.me.phone_number, app.me.first_name]
                else:
                    l = contact.split("-")
                await app.send_contact(username, phone_number=l[0], first_name=l[1])
                    
            except:
                f +=1
            await app.disconnect()
            n+=1
        else:
            break
    return [f, s, n]

def process_chat_links(chats):
    result = []
    for chat in chats:
        if chat.startswith("@"):
            result.append(chat[1:])
        elif chat.startswith("https://t.me/"):
            user = chat[13:]
            if user.startswith("+"):
                result.append(chat)
            else:
                result.append(user)
        else:
            result.append(chat)
    return result

async def join_chats(max, chats):
    links = process_chat_links(chats)
    accs = db.get_accounts()
    s = 0
    f = 0
    ftg = 0
    n = 0
    if max == "max":
        max = float("inf")
    else:
        max = int(max)
    for acc in accs.keys():
        if n < max:
            app = Client("user", session_string=accs[acc])
            await app.connect()
            try:
                for chat in links:
                    await app.join_chat(chat)
                s+=1
            except errors.UserAlreadyParticipant:
                ftg += 1
            except:
                f += 1
            await app.disconnect()
            n+=1
    return [f, s, n, ftg]

def process_invite_link(link):
    link = link.replace("https://t.me/", "")
    bot_user = link[:link.index("?")]
    command, ref_code = link[link.index("?")+1:].split("=")
    return [bot_user,f"/{command} {ref_code}"]

async def send_refs(max, invite_link):
    accs = db.get_accounts()
    s = 0
    f = 0
    n = 0
    ref = process_invite_link(invite_link)
    if max == "max":
        max = float("inf")
    else:
        max = int(max)
    for acc in accs.keys():
        if n <= max:
            app = Client("user", session_string=accs[acc])
            await app.connect()        
            try:
                await app.send_message(ref[0], ref[1])
                s+=1
            except:
                f+=1
            await app.disconnect()
            n+=1
        else:
            break
    return [f, s, n]
            