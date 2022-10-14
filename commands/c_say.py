import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *
from aiogram import Bot

from utils.funcs import *

async def say(message: Message):
    msg_text = "Для того, щоб трансювати ваше повідомлення усім користувачам, відправте його відповіддю на це\n"\
                "\n"\
                "Якщо ви передумали його відправляти, натисніть ❌"
    ikm = InlineKeyboardMarkup(row_width=1)
    ikm.add(InlineKeyboardButton("❌", callback_data="say exit"))
    return await message.answer(msg_text, reply_markup=ikm)

async def say_helper(message: Message, bot:Bot, say_params: dict):
    if message.reply_to_message != None:
        if message.reply_to_message.message_id == say_params["msg_id"]:
            cur = conn.execute("SELECT id FROM users")
            for id in cur:
                id = id[0]
                try:
                    msg_text = "<b>Повідомлення від адміністратора:</b>\n\n" + message.html_text
                    await bot.send_message(chat_id=id, text=msg_text, parse_mode=ParseMode.HTML)
                except:
                    conn.execute(f"DELETE FROM users WHERE id={id}")
            conn.commit()
        else:
            msg_text = "Здається, ви відповіли не на те повідомлення...\n"\
                        "\n"\
                        "Якщо ви все ще хочете щось відправити, натисніть /say"
            await message.answer(msg_text)
    else:
        msg_text = "Повідомлення не було розіслано, бо ви відправили його не відповіддю. Зпишемо це на міссклік\n"\
                    "\n"\
                    "Якщо ви все ще хочете щось відправити, натисніть /say"
        await message.answer(msg_text)