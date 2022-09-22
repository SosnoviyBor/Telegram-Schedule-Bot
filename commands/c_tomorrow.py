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
    if week == 1:
        msg_text = "<code>1 тиждень</code>\n"
    else:
        msg_text = "<code>2 тиждень</code>\n"

    sched = get_schedule(message.from_user.id)
    msg_text += f"<b>{DAYS[day]}</b>\n"
    for id in sched[week][day].keys():
        name = sched[week][day][id][0]
        type = sched[week][day][id][1]
        link = sched[week][day][id][2]
        msg_text += f"{id}. <a href='{link}'>{name} ({type})</a>\n"

    await message.answer(msg_text, parse_mode=ParseMode.HTML)