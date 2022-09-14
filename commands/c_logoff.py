import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *

from db import conn

async def logoff(message: Message):
    cur = conn.execute("SELECT id FROM users")
    for user in cur:
        if message.from_user.id not in user:
            await message.answer("Ви ще навіть не зареєструвалися у боті. Спочатку зареєструйтесь, а лише потім виходьте з нього")
        else:
            ikm = InlineKeyboardMarkup(row_width=2)
            ikm.add(InlineKeyboardButton(text="✅ Так, видаліть мене", callback_data="logoff true"))
            ikm.add(InlineKeyboardButton(text="❌ Ні, я міссклікнув", callback_data="logoff false"))
            await message.answer("Ви впенені, що хочете видалити себе із боту?", reply_markup=ikm)