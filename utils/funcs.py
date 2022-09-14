from aiogram.types import *
from datetime import datetime

from db import *
from utils.consts import *

# You may need to swap return values' places depending on the year
def get_week():
    if datetime.date(datetime(2010, 6, 16)).isocalendar().week % 2 == 1:
        return "week1"
    else:
        return "week2"

def get_schedule(message: Message):
    """
    Returns next type of dictionary\n
    schedule {
        week : {
            day : [pair, name, type, link]
        }
    }
    """
    classes = {
        "week1":{
            1:[], # day starting from monday
            2:[],
            3:[],
            4:[],
            5:[]
        }, "week2":{
            1:[],
            2:[],
            3:[],
            4:[],
            5:[]
        }
    }
    # Adding selective classes
    cur = conn.execute("SELECT group_name, selec_class1, selec_class2, selec_class3 "\
                        f"FROM users WHERE id = {message.from_user.id}")
    row = cur.fetchone()
    for value in row:
        if type(value) is int:
            cur = conn.execute("SELECT 'week'||sc.week, sc.day, sc.pair, c.name, sc.type, sc.link "\
                                f"FROM selec_classes sc "\
                                f"INNER JOIN classes c ON sc.class_id = c.id "\
                                f"WHERE sc.class_id = {value}")
            c = cur.fetchone()
            classes[c[0]][c[1]].append([c[2], c[3], c[4], c[5]])
        elif type(value) is str:
            group = value.lower()
    cur = conn.execute("SELECT 'week'||g.week, g.day, g.pair, c.name, g.type, g.link "\
                        f"FROM {group} g "\
                        "INNER JOIN classes c ON g.class_id = c.id")
    for row in cur:
        classes[row[0]][row[1]].append([row[2], row[3], row[4], row[5]])
    # Sorting classes in each day by order
    for week in classes.keys():
        for day in classes[week].keys():
            classes[week][day].sort(key=lambda x: x[0])
    return classes