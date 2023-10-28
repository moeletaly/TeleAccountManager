from pyrogram import Client
from tools import r,g,w, binput
import asyncio


async def add():
    while True:
        print("Choose:\n(1) - Add Account\n(2/exit/q) - EXIT")
        choice = await binput(g)
        if choice.strip() == "1":
            await add_account()
        elif choice.strip().lower() in ["exit","2", "q"]:
            exit()

asyncio.run(add())