import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *

from bot import bot
from utils.consts import *
from utils.funcs import *

async def set_ignored(query: CallbackQuery, command: list):
    # Only week was set
    if len(command) == 2:
        week = command[1]
        msg_text = f"Неділя: {week}\n"\
                    "\n"\
                    "Пару якого дня ви хочете ігнорувати?\n"
        buttons = []
        for i in range(2,6):
            msg_text += f"\n{i}. {DAYS[i]}"
            buttons.append(InlineKeyboardButton(text=INT2EMOJI[i], callback_data=f"set_ignored {command[1]} {i}"))
        ikm = InlineKeyboardMarkup(row_width=4)
        ikm.add(*buttons)
        ikm.add(InlineKeyboardButton(text="❌ Закрити", callback_data="func set_ignored True"))
        await bot.edit_message_text(chat_id=query.from_user.id,
            message_id=query.message.message_id, text=msg_text, reply_markup=ikm)

    # Week and day was set
    elif len(command) == 3:
        week = int(command[1])
        day = int(command[2])
        msg_text = f"Неділя: {week}\n"\
                    f"День: {day}\n"\
                    "\n"\
                    "Яку пару ви хочете ігнорувати? Номер відповідає розкладу\n"\
                    "\n"\
                    "Перечіркнута пара - вже ігнорована. Якщо ще раз її вибрати, вам знову почнуть приходити повідомлення про неї\n"
        buttons = []
        sched = get_schedule(query.from_user.id)
        for pair in sorted(sched[week][day].keys()):
            name = sched[week][day][pair][0]
            type = sched[week][day][pair][1]
            if pair_is_ignored(query.from_user.id, week, day, pair):
                msg_text += f"\n{pair}. <s>{name} ({type})</s>"
                callback_data=f"set_ignored rm {week} {day} {pair}"
            else:
                msg_text += f"\n{pair}. {name} ({type})"
                callback_data=f"set_ignored add {week} {day} {pair}"
            buttons.append(InlineKeyboardButton(text=INT2EMOJI[pair], callback_data=callback_data))
        ikm = InlineKeyboardMarkup(row_width=6)
        ikm.add(*buttons)
        ikm.add(InlineKeyboardButton(text="❌ Закрити", callback_data=query.data[:-2:]))
        await bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
            text=msg_text, reply_markup=ikm, parse_mode=ParseMode.HTML)

    # set_ignored <add/rm> <week> <day> <pair>
    elif command[1] in ["add", "rm"]:
        week = int(command[2])
        day = int(command[3])
        pair = int(command[4])
        cur = conn.execute(f"SELECT ignored FROM users WHERE id = {query.from_user.id}")
        curr_ignored = str(cur.fetchall()[0][0])
        sched = get_schedule(query.from_user.id)
        if command[1] == "add":
            curr_ignored += f"{week},{day},{pair};"
        else:
            curr_ignored = curr_ignored.replace(f"{week},{day},{pair};", "")
        conn.execute("UPDATE users "\
                    f"SET ignored = '{curr_ignored}' "\
                    f"WHERE id = {query.from_user.id}")
        conn.commit()

        sched = get_schedule(query.from_user.id)
        if command[1] == "add":
            msg_text = "Тепер ви <b>ігноруєте</b> наступний предмет:\n\n"
        else:
            msg_text = "Для наступного предмету були знову <b>вімкнуті</b> повідомлення:\n\n"
        name = sched[week][day][pair][0]
        type = sched[week][day][pair][1]
        msg_text += f"Назва: {name} ({type})\n"\
                    f"Тиждень: {week}\n"\
                    f"День: {day}\n"\
                    f"Номер пари: {pair}\n"\
                    "\n"\
                    "Хочете вимкнути/вімкнути ще якісь пари? Ось <b>/set_ignored</b>"
        await bot.edit_message_text(text=msg_text, parse_mode=ParseMode.HTML,
                                    chat_id=query.from_user.id, message_id=query.message.message_id)