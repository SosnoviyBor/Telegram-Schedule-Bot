import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *
from datetime import datetime

from utils.consts import *
from utils.funcs import *

async def today(message: Message):
    day = datetime.today().weekday()+1    # +1 cuz weekday() starts from 0
    if day in [1,6,7]:
        await message.answer("Нащастя, вьогодні ви можете відпочити 😉\n"\
            "Але якщо ви хочете подивитися розклад на вівторок, клацніть <b>/tomorrow</b>", parse_mode=ParseMode.HTML)
        return
    week = get_week()
    if week == "week1":
        msg_text = "<code>1 неділя</code>\n"
    else:
        msg_text = "<code>2 неділя</code>\n"
    schedule = get_schedule(message.from_user.id)
    msg_text += f"<b>{DAYS[day]}</b>\n"
    for c in schedule[week][day]:
        msg_text += f"{c[0]}. <a href='{c[3]}'>{c[1]} ({c[2]})</a>\n"
    await message.answer(msg_text, parse_mode=ParseMode.HTML)