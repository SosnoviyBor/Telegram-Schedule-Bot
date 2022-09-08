from aiogram import Bot, Dispatcher, executor
from aiogram.types import *
import asyncio
import aioschedule
import logging

import query_handler.master as qh
import commands.master as c
import utils.str_utils as su
from utils.consts import *
from db import conn

try:
    import config_local as config
except:
    import config
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token)
dp = Dispatcher(bot)

""" ########################################## Command handlers ########################################## """

@dp.message_handler(commands=['register'])
async def register(message: Message):
    cur = conn.execute(f"SELECT id FROM users")
    reg_users = []
    for i in cur:
        reg_users += i
    # If the user is new or admin
    if message.from_id not in reg_users or message.from_id in config.admins:
        ikm = InlineKeyboardMarkup(row_width=4)
        for group in ALL_GROUPS:
            ikm.add(InlineKeyboardButton(text=group, callback_data=f"register {group}"))
        await message.reply("З якої ти групи?", reply_markup=ikm)
    # If the user is already in system
    else:
        await message.answer("Ви вже зареєстровані, тому перенаправляю вас на повідомлення із командами 😉")
        await help(message)

@dp.message_handler(commands=['help'])
async def help(message: Message):
    await message.reply(
        "/register - зареєструватися у боті. Якщо ви вже зареєстровані, то працює як наступна команда"
      "\n/help - повідомлення із списком команд"
      "\n/my_selecs - перегляд та вибір своїх вибіркових предметів"
      "\n/logoff - видалити себе із боту"   # Можна буде ще подумати над назвою команди
    )

@dp.message_handler(commands=['my_selecs'])
async def my_selecs(message: Message, edit_flag=False):
    cur = conn.execute("SELECT selec_class1, selec_class2, selec_class3 "+
                      f"FROM users WHERE id = {message.from_id if not edit_flag else message.chat.id}")
    picked_classes = []
    for i in cur:
        picked_classes += i
    ikm = InlineKeyboardMarkup(row_width=3)
    ikm.add(InlineKeyboardButton(text=f"1. {su.my_selecs_b(picked_classes[0])}", callback_data="my_selecs view 1 0"),  # my_selecs view <slot> <page>
            InlineKeyboardButton(text=f"2. {su.my_selecs_b(picked_classes[1])}", callback_data="my_selecs view 2 0"),
            InlineKeyboardButton(text=f"3. {su.my_selecs_b(picked_classes[2])}", callback_data="my_selecs view 3 0"))
    msg_text = "Ваші вибіркові предмети наступні:\n\n"\
            f"1. <code>{su.my_selecs_m(picked_classes[0])}</code>\n"\
            f"2. <code>{su.my_selecs_m(picked_classes[1])}</code>\n"\
            f"3. <code>{su.my_selecs_m(picked_classes[2])}</code>\n\n"\
            "Переглянути свої предмети можна у <b><a href='https://my.kpi.ua/'>ф-каталозі</a></b>"
    if edit_flag:
        await message.edit_text(msg_text, reply_markup=ikm, parse_mode=ParseMode.HTML)
    else:
        await message.reply(msg_text, reply_markup=ikm, parse_mode=ParseMode.HTML)

@dp.message_handler(commands=['logoff'])
async def logoff(message: Message):
    # TODO add check if user is not yet registered
    ikm = InlineKeyboardMarkup(row_width=2)
    ikm.add(InlineKeyboardButton(text="✅ Так, видаліть мене", callback_data="logoff true"))
    ikm.add(InlineKeyboardButton(text="❌ Ні, я міссклікнув", callback_data="logoff false"))
    await message.answer("Ви впенені, що хочете видалити себе із боту?", reply_markup=ikm)

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
    # /register helper
    # Register user in bot
    elif command[0] == "register":
        await qh.register(query, command)
    # /logoff helper
    # Remove user from bot's DB
    elif command[0] == "logoff":
        await qh.logoff(query, command)
    # /my_selecs helper
    # Set selective classes for yourself
    elif command[0] == "my_selecs":
        await qh.my_selecs(query, command)



# Saved for future
async def on_startup(_):
    return
    asyncio.create_task(scheduler())

async def scheduler():
    aioschedule.every().day.at("8:00").do()
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)