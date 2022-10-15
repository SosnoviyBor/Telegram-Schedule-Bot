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
        if pair_is_ignored(message.from_user.id, week, day, id):
            msg_text += f"{id}. <span class='tg-spoiler'><a href='{link}'>{name} ({type})</span></s>\n"
        else:
            msg_text += f"{id}. <a href='{link}'>{name} ({type})</a>\n"

    await message.answer(msg_text, parse_mode=ParseMode.HTML)