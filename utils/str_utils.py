from utils.consts import *
from datetime import datetime

int2emoji = [
    '0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'
]

def my_selecs_b(sc):
    return '❌' if sc is None else '✅'

def my_selecs_m(sc):
    return ALL_SC['name'][sc] if sc is not None else 'Відсутній'

# You may need to swap return values' places depending on year
def get_week():
    if datetime.date(datetime(2010, 6, 16)).isocalendar().week % 2 == 1:
        return "week1"
    else:
        return "week2"