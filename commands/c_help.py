import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *

from utils.consts import *
import acl

async def help(message: Message):
    msg_text = "/start - зареєструватися у боті. Якщо ви вже зареєстровані, то працює як наступна команда"\
             "\n/help - повідомлення із списком команд"\
             "\n/schedule - перегляд свого розкладу"\
             "\n/today - перегляд розкладу на сьогодні"\
             "\n/tomorrow - перегляд розкладу на завтра (або наступний навчальній день, якщо завтра вихідний)"\
             "\n/set_selecs - перегляд та вибір своїх вибіркових предметів"\
             "\n/logoff - видалити себе із боту"
    if acl.is_admin(message):
        msg_text += "\n\n ##### Команди адміністратора #####"\
                    "\n/say - відправити повідомлення усім користувачам"
    await message.answer(msg_text)