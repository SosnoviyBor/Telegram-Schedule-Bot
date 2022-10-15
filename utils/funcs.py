import sys
sys.path.append("../Telegram-Schedule-Bot")

from aiogram.types import *
from datetime import datetime

from db import *
from utils.consts import *

# You may need to swap return values' places depending on the year
def get_week():
    if datetime.date(datetime(2010, 6, 16)).isocalendar().week % 2 == 1:
        return 1
    else:
        return 2

def get_schedule(id: int):
    """
    Returns next type of dictionary\n
    schedule {
        week : {
            day : {
                pair: [name, type, link],
                pair: ...
            }
        }
    }
    """
    classes = {
        1:{
            #1:{}}, # day starting from monday
            2:{},   # monday is ignored. uncomment if you have pairs this day
            3:{},
            4:{},
            5:{}
        },
        2:{
            #1:{},
            2:{},
            3:{},
            4:{},
            5:{}
        }
    }
    # Adding selective classes
    cur = conn.execute("SELECT group_name, selec_class1, selec_class2, selec_class3 "\
                        f"FROM users WHERE id = {id}")
    row = cur.fetchone()
    for value in row:
        if type(value) is int:
            cur = conn.execute("SELECT sc.week, sc.day, sc.pair, c.name, sc.type, sc.link "\
                                f"FROM selec_classes sc "\
                                f"INNER JOIN classes c ON sc.class_id = c.id "\
                                f"WHERE sc.class_id = {value}")
            for c in cur:
                # classes[week][day][pair] = [name, type, link]
                classes[c[0]][c[1]][c[2]] = [c[3], c[4], c[5]]
        elif type(value) is str:
            group = value.lower()
    cur = conn.execute("SELECT g.week, g.day, g.pair, c.name, g.type, g.link "\
                        f"FROM {group} g "\
                        "INNER JOIN classes c ON g.class_id = c.id")
    for row in cur:
        # classes[week][day][pair] = [name, type, link]
        classes[row[0]][row[1]][row[2]] = [row[3], row[4], row[5]]
    return classes

def pair_is_ignored(user_id, week, day, pair):
    cur = conn.execute(f"SELECT ignored FROM users WHERE id = {user_id}")
    # Result will look like "week,day,pair;week,day,pair;"
    raw = cur.fetchone()[0]
    if raw == None:
        return False
    tmp = raw.split(";")
    tmp = tmp[:len(tmp)-1:]
    for i in tmp:
        ignored = i.split(",")
        if (ignored[0] == str(week)) and (ignored[1] == str(day)) and (ignored[2] == str(pair)):
            return True
    return False