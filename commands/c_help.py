import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *

from utils.consts import *
import acl

async def help(message: Message):
    msg_text = "/start - зареєструватися у боті. Якщо ви вже зареєстровані, то працює як наступна команда"\
             "\n/help - повідомлення із списком команд"\
             "\n/my_schedule - перегляд свого розкладу"\
             "\n/my_selecs - перегляд та вибір своїх вибіркових предметів"\
             "\n/logoff - видалити себе із боту"
    if acl.check_access_admin(message):
        msg_text += "\n\n ##### Команди адміністратора #####"\
                    "\n/reload - оновлює з'єднання боту із БД у рантаймі"   # is needed?
    await message.answer(msg_text)