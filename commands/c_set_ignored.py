import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *
from utils.consts import *

async def set_ignored(message: Message, edit_flag=False):
    msg_text = "Пару якої неділі ви хочете ігнорувати?"
    ikm = InlineKeyboardMarkup(row_width=2)
    ikm.add(InlineKeyboardButton(text=INT2EMOJI[1], callback_data="set_ignored 1"),
            InlineKeyboardButton(text=INT2EMOJI[2], callback_data="set_ignored 2"))
    if edit_flag:
        await message.edit_text(text=msg_text, reply_markup=ikm)
    else:
        await message.answer(text=msg_text, reply_markup=ikm)