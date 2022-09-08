from ast import parse
from email import message
import sqlite3 as sql
from subprocess import call
from aiogram import Bot, Dispatcher, executor
from aiogram.types import *
import asyncio
import aioschedule
import logging

import utils as u

try:
    import config_local as config
    conn = sql.Connection("db.db")
except:
    import config
    # your data src
print("Opened database successfully")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token)
dp = Dispatcher(bot)

cur = conn.execute("SELECT sc.id, c.name \
                    FROM selec_classes sc\
                    INNER JOIN classes c \
                    ON sc.class_id = c.id")
ALL_SC = {
    "id": [],
    "name": []
}
for row in cur:
    ALL_SC["id"].append(row[0])
    ALL_SC["name"].append(row[1])
ALL_GROUPS = ["IT01", "IT02", "IT03", "IT04"]

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
    ikm.add(InlineKeyboardButton(text=f"1. {'❌' if picked_classes[0] is None else '✅'}", callback_data="my_selecs view 1 0"),  # my_selecs view <slot> <page>
            InlineKeyboardButton(text=f"2. {'❌' if picked_classes[1] is None else '✅'}", callback_data="my_selecs view 2 0"),
            InlineKeyboardButton(text=f"3. {'❌' if picked_classes[2] is None else '✅'}", callback_data="my_selecs view 3 0"))
    msg_text = "Ваші вибіркові предмети наступні:\n\n"\
            f"1. <code>{ALL_SC['name'][picked_classes[0]] if picked_classes[0] is not None else 'Відсутній'}</code>\n"\
            f"2. <code>{ALL_SC['name'][picked_classes[0]] if picked_classes[1] is not None else 'Відсутній'}</code>\n"\
            f"3. <code>{ALL_SC['name'][picked_classes[0]] if picked_classes[2] is not None else 'Відсутній'}</code>\n\n"\
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

""" ########################################## Plain text handler ########################################## """

@dp.message_handler()
async def plain_text(message: Message):
    return

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
        conn.execute("INSERT INTO users (id, name, 'group') "
                    f"VALUES({query.from_user.id},'{query.from_user.username}','{command[1]}')")
        conn.commit()
        msg_text = "Тепер треба обрати свої вибіркові предмети\n"\
                   "Для цього використайте команду <b>/my_selecs</b>"
        await bot.send_message(query.from_user.id, parse_mode=ParseMode.HTML, text=msg_text)
    # /logoff helper
    # Remove user from bot's DB
    elif command[0] == "logoff":
        if command[1] == "true":
            conn.execute(f"DELETE FROM users WHERE id = {query.from_user.id}")
            conn.commit()
            await bot.send_message(query.from_user.id, text="Ви успішно від'єдналися від боту")
        else:
            await bot.send_message(query.from_user.id, text="Фух, це добре 😉")
    # /my_selecs helper
    # Set selective classes for yourself
    elif command[0] == "my_selecs":
        # my_selecs view <slot> <page>
        if command[1] == "view":
            command[2] = int(command[2])    # slot
            command[3] = int(command[3])    # page
            cur = conn.execute("SELECT selec_class1, selec_class2, selec_class3 "+
                            f"FROM users WHERE id = {query.from_user.id}")
            picked_classes = []
            for i in cur:
                picked_classes += i

            ikm = InlineKeyboardMarkup(row_width=5)
            button_row1, button_row2 = [], []
            picked_class_curr = 'Ще не вибрано' if picked_classes[command[2]-1] == None else ALL_SC['name'][int(picked_classes[command[2]-1])]
            msg_text = f"Предмет №{command[2]}:  <code>{picked_class_curr}</code>\n\n"
            for rel_id in range(10):           # sc id on page
                abs_id = rel_id+1*command[3]   # sc id in ALL_SC
                if abs_id > len(ALL_SC['id'])-1:
                    break
                if ALL_SC['id'][abs_id]-1 in picked_classes:
                    msg_text += f"<s><b>{rel_id+1}.</b> {ALL_SC['name'][abs_id]}</s>\n"
                    button = InlineKeyboardButton(text="*️⃣", callback_data="a")
                else:
                    msg_text += f"<b>{rel_id+1}.</b> {ALL_SC['name'][abs_id]}\n"
                    button = InlineKeyboardButton(text=u.int2emoji[rel_id+1],
                                                callback_data=f"my_selecs set {command[2]} {ALL_SC['id'][abs_id]}")  # my_selecs set <slot> <sc_id>
                if rel_id < 5:
                    button_row1.append(button)
                else:
                    button_row2.append(button)
            ikm.add(*button_row1)
            ikm.add(*button_row2)

            button_row3 = []
            prev_page = command[3] if command[3]-1 >= 0 else 0
            go_back = "func my_selecs True"
            next_page = command[3] if command[3]+1 >= len(ALL_SC['id'])//10 else len(ALL_SC['id'])//10
            button_row3.append(InlineKeyboardButton(text="⬅️", callback_data=f"my_selecs view {command[2]} {prev_page}"))
            button_row3.append(InlineKeyboardButton(text="❌", callback_data=go_back))
            button_row3.append(InlineKeyboardButton(text="➡️", callback_data=f"my_selecs view {command[2]} {next_page}"))
            ikm.add(*button_row3)

            await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                        text=msg_text, parse_mode=ParseMode.HTML, reply_markup=ikm)
        # my_selecs set <slot> <sc_id>
        elif command[1] == "set":
            conn.execute(f"UPDATE users\
                           SET selec_class{command[2]} = {int(command[3])-1}\
                           WHERE id = {query.from_user.id}")
            conn.commit()
            query.data = "func my_selecs True"
            await callback(query)



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