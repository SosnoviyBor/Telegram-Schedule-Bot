from aiogram import Bot, Dispatcher, executor
from aiogram.types import *
import asyncio
import aioschedule
import logging

import commands.master as c
import query_handler.master as qh
import acl
from db import *
from utils.consts import *
try:
    import config_local as config
except:
    import config

# TODO. Delete on release
from utils.funcs import *
from datetime import datetime

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token)
dp = Dispatcher(bot)

""" ########################################## Command handlers ########################################## """

@dp.message_handler(commands=['start'])
async def start(message: Message):
    await c.start(message)

@dp.message_handler(commands=['help'])
async def help(message: Message):
    await c.help(message)

@dp.message_handler(commands=['my_selecs'])
async def my_selecs(message: Message, edit_flag=False):
    await c.my_selecs(message, edit_flag)

@dp.message_handler(commands=['logoff'])
async def logoff(message: Message):
    await c.logoff(message)

@dp.message_handler(commands=['my_schedule'])
async def my_schedule(message: Message):
    await c.my_schedule(message)

@dp.message_handler(commands=['today'])
async def today(message: Message):
    await c.today(message)

@dp.message_handler(commands=['tomorrow'])
async def tomorrow(message: Message):
    await c.tomorrow(message)

""" ########################################## Callback query handler ########################################## """

@dp.callback_query_handler()
async def callback(query: CallbackQuery):
    command = query.data.split()
    # general helper
    # Used in case if I need to call any function after pressing inline button
    if command[0] == "func":
        # <func_name> <args>
        if command[1] == "my_selecs":
            await my_selecs(query.message, bool(command[2]))
    # /start helper
    # Register user in bot
    elif command[0] == "start":
        await qh.start(query, command)
    # /logoff helper
    # Remove user from bot's DB
    elif command[0] == "logoff":
        await qh.logoff(query, command)
    # /my_selecs helper
    # Set selective classes for yourself
    elif command[0] == "my_selecs":
        await qh.my_selecs(query, command)



async def on_startup(_):
    asyncio.create_task(scheduler())

async def scheduler():
    aioschedule.every().day.at("8:25").do(remind)
    aioschedule.every().day.at("10:20").do(remind)
    aioschedule.every().day.at("12:15").do(remind)
    aioschedule.every().day.at("14:10").do(remind)
    aioschedule.every().day.at("16:05").do(remind)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def remind():
    week = get_week()
    day = datetime.today().weekday()+1
    pair = PAIRS[datetime.now().hour]
    cur = conn.execute("SELECT id FROM users")
    for id in cur.fetchall()[0]:
        sched = get_schedule(id)
        for c in sched[week][day]:
            if c[0] == pair:
                msg_text = "Через 5 хвилин почнеться пара\n"\
                        f"{pair}. <a href='{c[3]}'>{c[1]} ({c[2]})</a>"
                await bot.send_message(chat_id=id, text=msg_text, parse_mode=ParseMode.HTML)
                break

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)