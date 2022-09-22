import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *

from bot import bot
from db import conn
from utils.consts import *

async def logoff(query: CallbackQuery, command: list):
    if command[1] == "true":
        conn.execute(f"DELETE FROM users WHERE id = {query.from_user.id}")
        conn.commit()
        await bot.send_message(query.from_user.id, text="Ви успішно від'єдналися від боту")
    else:
        await bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id, text="Фух, це добре 😉")