import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *
from utils.consts import *
from utils.funcs import *

async def schedule(message: Message):
    sched = get_schedule(message.from_user.id)
    msg_text = ""
    for week in sched.keys():
        if week == 1:
            msg_text += "<code>1 тиждень</code>\n"
        else:
            msg_text += "\n<code>2 тиждень</code>\n"

        for day in sched[week].keys():
            msg_text += "-----------------------\n"
            msg_text += f"<b>{DAYS[day]}</b>\n"
            for id in sched[week][day].keys():
                name = sched[week][day][id][0]
                type = sched[week][day][id][1]
                link = sched[week][day][id][2]
                msg_text += f"{id}. <a href='{link}'>{name} ({type})</a>\n"

    await message.answer(text=msg_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)