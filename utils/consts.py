from db import *

# All selective classes
# Filled on startup
ALL_SC = {
    "id": [],
    "name": []
}
__cur = conn.execute("SELECT sc.class_id, c.name \
                    FROM selec_classes sc\
                    INNER JOIN classes c \
                    ON sc.class_id = c.id")
for row in __cur:
    ALL_SC["id"].append(row[0])
    ALL_SC["name"].append(row[1])

# All groups
# For increased user scope it should be moved to db (probbly)
ALL_GROUPS = ["IT03"]

DAYS = {
    1:"Понеділок",
    2:"Вівторок",
    3:"Середа",
    4:"Четвер",
    5:"П'ятниця"
}

PAIRS = {
    8: 1,
    10: 2,
    12: 3,
    14: 4,
    16: 5
}

INT2EMOJI = [
    '0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'
]