from aiogram.types import *
try:
    import config_local as config
except:
    import config

# check if it is direct chat (not a group chat)
def check_access_direct(message: Message):
    if message.from_user.id == message.chat.id:
        return True
    return False

# check if it is message from admin
def check_access_admin(message: Message):
    if message.from_user.id in config.admins:
        return True
    return False