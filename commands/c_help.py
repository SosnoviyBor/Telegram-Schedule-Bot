import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *

from utils.consts import *

async def help(message):
    await message.reply(
        "/start - зареєструватися у боті. Якщо ви вже зареєстровані, то працює як наступна команда"
      "\n/help - повідомлення із списком команд"
      "\n/my_selecs - перегляд та вибір своїх вибіркових предметів"
      "\n/logoff - видалити себе із боту"   # Можна буде ще подумати над назвою команди
    )