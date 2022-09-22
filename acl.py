from aiogram.types import *
try:
    import config_local as config
except:
    import config

# check if it is direct chat (not a group chat)
def is_dm(message: Message):
    if message.from_user.id == message.chat.id:
        return True
    return False

# check if it is message from admin
def is_admin(message: Message):
    if message.from_user.id in config.admins:
        return True
    return False

def is_registered(message: Message):
    users = conn.execute("SELECT id FROM users").fetchall()
    id = (message.from_user.id,)
    if id in users:
        return True
    return False