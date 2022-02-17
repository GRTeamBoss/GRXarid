import sqlite3

from core.token import bot


def user_command(message) -> bool:
    _commands = (
        "/start",
        "/help",
    )
    if message.text.split()[0] in _commands:
        return True
    else:
        return False


def parse(message) -> bool:
    __command = message.text.split()[0]
    __range = int(message.text.rstrip().split()[2])
    if __command == "/product" or __command == "/uzex":
        if __range > 10 and __range < 10000:
            return True
        else:
            return False
    else:
        return False


def user(message) -> bool:
    db = sqlite3.connect("bot.db")
    user_info = list(db.cursor().execute(
        f"select * from User where ID={message.chat.id}"
    ))
    db.close()
    if user_info:
        return True
    else:
        return False
