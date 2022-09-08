import sqlite3 as sql
from utils.consts import *

conn = sql.Connection("db.db")
print("Opened database successfully")

cur = conn.execute("SELECT sc.id, c.name \
                    FROM selec_classes sc\
                    INNER JOIN classes c \
                    ON sc.class_id = c.id")
for row in cur:
    ALL_SC["id"].append(row[0])
    ALL_SC["name"].append(row[1])