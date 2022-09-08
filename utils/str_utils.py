from utils.consts import *

int2emoji = [
    '0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'
]

def my_selecs_b(sc):
    return '❌' if sc is None else '✅'

def my_selecs_m(sc):
    return ALL_SC['name'][sc] if sc is not None else 'Відсутній'