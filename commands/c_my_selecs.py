import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *

from utils.consts import *
from db import conn
import utils.str_utils as su

async def my_selecs(message: Message, edit_flag:bool):
    cur = conn.execute("SELECT selec_class1, selec_class2, selec_class3 "+
                      f"FROM users WHERE id = {message.from_id if not edit_flag else message.chat.id}")
    picked_classes = []
    for i in cur:
        picked_classes += i
    ikm = InlineKeyboardMarkup(row_width=3)
    ikm.add(InlineKeyboardButton(text=f"1. {su.my_selecs_b(picked_classes[0])}", callback_data="my_selecs view 1 0"),  # my_selecs view <slot> <page>
            InlineKeyboardButton(text=f"2. {su.my_selecs_b(picked_classes[1])}", callback_data="my_selecs view 2 0"),
            InlineKeyboardButton(text=f"3. {su.my_selecs_b(picked_classes[2])}", callback_data="my_selecs view 3 0"))
    msg_text = "Ваші вибіркові предмети наступні:\n\n"\
            f"1. <code>{su.my_selecs_m(picked_classes[0])}</code>\n"\
            f"2. <code>{su.my_selecs_m(picked_classes[1])}</code>\n"\
            f"3. <code>{su.my_selecs_m(picked_classes[2])}</code>\n\n"\
            "Переглянути свої предмети можна у <b><a href='https://my.kpi.ua/'>ф-каталозі</a></b>"
    if edit_flag:
        await message.edit_text(msg_text, reply_markup=ikm, parse_mode=ParseMode.HTML)
    else:
        await message.reply(msg_text, reply_markup=ikm, parse_mode=ParseMode.HTML)