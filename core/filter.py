import sqlite3

from core.token import bot


def user_command(message) -> bool:
    _commands = (
        "/start",
        "/help",
    )
    if message.text.split(" ")[0] in _commands:
        return True
    else:
        return False


def parse(message) -> bool:
    if message.text.split(" ")[0] == "/product":
        if int(message.text.split()[2]) > 10 and int(message.text.split()[2]) < 10000:
            return True
        else:
            bot.send_message(message.chat.id, f"this > `{message.text.split()[2]}` should more `10` and less `10000`!")
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
