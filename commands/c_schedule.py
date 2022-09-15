import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *
from utils.consts import *
from utils.funcs import *

async def schedule(message: Message):
    classes = get_schedule(message.from_user.id)
    msg_text = ""
    for week in classes.keys():
        if week == "week1":
            msg_text += "<code>1 неділя</code>\n"
        else:
            msg_text += "\n<code>2 неділя</code>\n"
        for day in classes[week].keys():
            msg_text += "-----------------------\n"
            msg_text += f"<b>{DAYS[day]}</b>\n"
            for i in classes[week][day]:
                msg_text += f"{i[0]}. <a href='{i[3]}'>{i[1]} ({i[2]})</a>\n"
    await message.answer(text=msg_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)