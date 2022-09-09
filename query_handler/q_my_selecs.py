import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *

from bot import bot, callback
from db import conn
from utils.consts import *
import utils.str_utils as su

async def my_selecs(query: CallbackQuery, command):
    # my_selecs view <slot> <page>
    if command[1] == "view":
        command[2] = int(command[2])    # slot
        command[3] = int(command[3])    # page
        cur = conn.execute("SELECT selec_class1, selec_class2, selec_class3 "+
                        f"FROM users WHERE id = {query.from_user.id}")
        picked_classes = []
        for i in cur:
            picked_classes += i

        ikm = InlineKeyboardMarkup(row_width=5)
        button_row1, button_row2 = [], []
        if picked_classes[command[2]-1] == None:
            picked_class_curr = 'Ще не вибрано ❌'
        else:
            picked_class_curr = f"<u>{ALL_SC['name'][int(picked_classes[command[2]-1])]}</u> ✅"
        msg_text = f"Предмет №{command[2]}:  {picked_class_curr}\n\n"
        for rel_id in range(10):           # sc id on page
            abs_id = rel_id+1*command[3]   # sc id in ALL_SC
            if abs_id > len(ALL_SC['id'])-1:
                break
            if ALL_SC['id'][abs_id]-1 in picked_classes:
                msg_text += f"<s><b>{rel_id+1}.</b> {ALL_SC['name'][abs_id]}</s>\n"
                button = InlineKeyboardButton(text="*️⃣", callback_data="a")
            else:
                msg_text += f"<b>{rel_id+1}.</b> {ALL_SC['name'][abs_id]}\n"
                button = InlineKeyboardButton(text=su.int2emoji[rel_id+1],
                                            callback_data=f"my_selecs set {command[2]} {ALL_SC['id'][abs_id]}")  # my_selecs set <slot> <sc_id>
            if rel_id < 5:
                button_row1.append(button)
            else:
                button_row2.append(button)
        ikm.add(*button_row1)
        ikm.add(*button_row2)

        button_row3 = []
        prev_page = command[3] if command[3]-1 >= 0 else 0
        go_back = "func my_selecs True"
        next_page = command[3] if command[3]+1 >= len(ALL_SC['id'])//10 else len(ALL_SC['id'])//10
        button_row3.append(InlineKeyboardButton(text="⬅️", callback_data=f"my_selecs view {command[2]} {prev_page}"))
        button_row3.append(InlineKeyboardButton(text="❌", callback_data=go_back))
        button_row3.append(InlineKeyboardButton(text="➡️", callback_data=f"my_selecs view {command[2]} {next_page}"))
        ikm.add(*button_row3)

        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    text=msg_text, parse_mode=ParseMode.HTML, reply_markup=ikm)
    # my_selecs set <slot> <sc_id>
    elif command[1] == "set":
        conn.execute(f"UPDATE users\
                        SET selec_class{command[2]} = {int(command[3])-1}\
                        WHERE id = {query.from_user.id}")
        conn.commit()
        query.data = "func my_selecs True"
        await callback(query)