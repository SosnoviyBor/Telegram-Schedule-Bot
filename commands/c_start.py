import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *

from utils.consts import *
from db import conn

from c_help import help

async def start(message):
    cur = conn.execute(f"SELECT id FROM users")
    reg_users = []
    for i in cur:
        reg_users += i
    # If the user is new or admin
    if message.from_id not in reg_users:
        ikm = InlineKeyboardMarkup(row_width=4)
        for group in ALL_GROUPS:
            ikm.add(InlineKeyboardButton(text=group, callback_data=f"start {group}"))
        await message.reply("З якої ти групи?", reply_markup=ikm)
    # If the user is already in system
    else:
        await message.answer("Ви вже зареєстровані, тому перенаправляю вас на повідомлення із командами 😉")
        await help(message)