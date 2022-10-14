from aiogram import Bot, Dispatcher, executor
from aiogram.types import *
import asyncio
import aioschedule
import logging
from datetime import datetime

try:
    import config_local as config
except:
    import config
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token)
dp = Dispatcher(bot)

import commands.master as c
import query_handler.master as qh
import acl
from db import *
from utils.consts import *
from utils.funcs import *

""" ########################################## Command handlers ########################################## """

@dp.message_handler(commands=['start'])
async def start(message: Message):
    await c.start(message)

@dp.message_handler(commands=['help'])
async def help(message: Message):
    await c.help(message)

@dp.message_handler(acl.is_registered, acl.is_dm, commands=['set_selecs'])
async def set_selecs(message: Message, edit_flag=False):
    await c.set_selecs(message, edit_flag)

@dp.message_handler(commands=['logoff'])
async def logoff(message: Message):
    await c.logoff(message)

@dp.message_handler(acl.is_registered, commands=['schedule'])
async def schedule(message: Message):
    await c.schedule(message)

@dp.message_handler(acl.is_registered, commands=['today'])
async def today(message: Message):
    await c.today(message)

@dp.message_handler(acl.is_registered, commands=['tomorrow'])
async def tomorrow(message: Message):
    await c.tomorrow(message)

@dp.message_handler(acl.is_registered, acl.is_dm, commands=['set_ignored'])
async def set_ignored(message: Message):
    await c.set_ignored(message)

say_params = {
    "flag": False,  # Should bot read next message?
    "msg_id": -1,
    "admin_id": -1
}
@dp.message_handler(acl.is_admin, commands=['say'])
async def say(message: Message):
    sent_message = await c.say(message)
    say_params["flag"] = True
    say_params["msg_id"] = sent_message.message_id
    say_params["admin_id"] = message.chat.id

@dp.message_handler(lambda _: say_params["flag"],
                    lambda message: message.chat.id == say_params["admin_id"])
async def say_helper(message: Message):
    await c.say_helper(message, bot, say_params)
    say_params["flag"] = False
    say_params["id"] = -1
    say_params["admin_id"] = -1

""" ########################################## Callback query handler ########################################## """

@dp.callback_query_handler()
async def callback(query: CallbackQuery):
    command = query.data.split()
    # general helper
    # Used in case if I need to call any function after pressing inline button
    if command[0] == "func":
        # <func_name> <args>
        if command[1] == "set_selecs":
            await c.set_selecs(query.message, bool(command[2]))
        if command[1] == "set_ignored":
            await c.set_ignored(query.message, bool(command[2]))
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
    elif command[0] == "set_selecs":
        await qh.set_selecs(query, command)
    # /set_ignored helper
    # Set ignored classes for yourself
    elif command[0] == "set_ignored":
        await qh.set_ignored(query, command)
    #/say helper
    # Display message for all users
    elif command[0] == "say":
        if command[1] == "exit":
            say_params["flag"] = False
            say_params["id"] = -1
            say_params["admin_id"] = -1
            await query.message.delete()

""" ########################################## Initialization things ########################################## """

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
    if day in [1,6,7]:
        return
    pair = PAIRS[datetime.now().hour]
    cur = conn.execute("SELECT id FROM users")
    for user_id in cur.fetchall():
        # cuz fetschall() returns typle instead of single value
        user_id = user_id[0]
        sched = get_schedule(user_id)
        name = sched[week][day][pair][0]
        type = sched[week][day][pair][1]
        link = sched[week][day][pair][2]
        if not pair_is_ignored(user_id, week, day, pair):
            msg_text = "Через 5 хвилин почнеться пара\n"\
                    f"{pair}. <a href='{link}'>{name} ({type})</a>"
            await bot.send_message(chat_id=user_id, text=msg_text, parse_mode=ParseMode.HTML)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)