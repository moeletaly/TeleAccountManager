from pyrogram import Client
from tools import r,g,w, binput, create_account
import asyncio
import subprocess



async def add():
    subprocess.run("clear")
    while True:
        print(f"{r}Choose:\n(1) - Add Account\n(2/exit/q) - EXIT{w}")
        choice = await binput(g)
        if choice.strip() == "1":
            await create_account()
        elif choice.strip().lower() in ["exit","2", "q"]:
            exit()

asyncio.run(add())