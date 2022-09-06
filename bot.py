import sqlite3 as sql
from aiogram import Bot, Dispatcher, executor
from aiogram.types import *
import asyncio
import aioschedule
import logging

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
                    ON sc.class_id = c.id\
                    WHERE sc.type = 'lec'")
tmp_ids = []
tmp_names = []
for row in cur:
    tmp_ids.append(row[0])
    tmp_names.append(row[1])
ALL_SELECTIVE_CLASSES = {"ids": tmp_ids,
               "names": tmp_names}
ALL_GROUPS = ["IT01", "IT02", "IT03", "IT04"]

@dp.message_handler(commands=['start', 'help'])
async def start(message: Message):
    if message.from_id not in []:
        ikm = InlineKeyboardMarkup(row_width=4)
        for group in ALL_GROUPS:
            ikm.add(InlineKeyboardButton(text=group, callback_data=group))
        await message.reply("З якої ти групи?", reply_markup=ikm)
    else:
        await message.reply(
            "/help - повідомлення із списком команд"
        )

@dp.message_handler()
async def plain_text(message: Message):
    return

@dp.callback_query_handler()
async def callback(query: CallbackQuery):
    # Register user in bot
    if query.data in ALL_GROUPS:
        # TODO. Add user to DB
        await bot.send_message(query.from_user.id, parse_mode="markdown", text=
            "Тепер треба обрати свої вибіркові предмети\n"
            "Передивитися свої предмети можна у [ф-каталозі](https://my.kpi.ua/)"
        )
        msg_text = ""
        ikm = InlineKeyboardMarkup(row_width=5)
        for i in range(len(ALL_SELECTIVE_CLASSES["ids"])):
            msg_text += f"{ALL_SELECTIVE_CLASSES['ids'][i]}. {ALL_SELECTIVE_CLASSES['names'][i]}\n"
            ikm.add(InlineKeyboardButton(text=ALL_SELECTIVE_CLASSES['ids'][i], callback_data="a"))
            pass
        await bot.send_message(query.from_user.id, text=msg_text, reply_markup=ikm)
    return


# Saved for future
async def on_startup(_):
    asyncio.create_task(scheduler())

async def scheduler():
    aioschedule.every().day.at("8:00").do()
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)