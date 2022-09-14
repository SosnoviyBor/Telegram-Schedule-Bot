import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *
from datetime import datetime

from utils.consts import *
from utils.funcs import *

async def tomorrow(message: Message):
    day = datetime.today().weekday()+1+1    # +1 cuz weekday() starts from 0 and +1 cuz tommorow
    if day in [6,7,8]:
        # if day is fri, sat or sun display info for tue
        day = 2
    week = get_week()
    if week == "week1":
        msg_text = "<code>1 неділя</code>\n"
    else:
        msg_text = "<code>2 неділя</code>\n"
    schedule = get_schedule(message)
    msg_text += f"<b>{DAYS[day]}</b>\n"
    for c in schedule[week][day]:
        msg_text += f"{c[0]}. <a href='{c[3]}'>{c[1]} ({c[2]})</a>\n"
    await message.answer(msg_text, parse_mode=ParseMode.HTML)