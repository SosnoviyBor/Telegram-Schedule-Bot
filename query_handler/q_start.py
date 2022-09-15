import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *

from bot import bot
from db import conn
from utils.consts import *

async def start(query: CallbackQuery, command):
    conn.execute("INSERT INTO users (id, name, group_name) "
                    f"VALUES({query.from_user.id},'{query.from_user.username}','{command[1]}')")
    conn.commit()
    msg_text = "Тепер треба обрати свої вибіркові предмети\n"\
                "Для цього використайте команду <b>/set_selecs</b>"
    await bot.send_message(query.from_user.id, parse_mode=ParseMode.HTML, text=msg_text)