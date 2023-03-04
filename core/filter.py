import sqlite3


def parse_method(message) -> bool:
    __command = message.text.split()[0]
    __range = int(message.text.rstrip().split()[2])
    if __command == "/product" or __command == "/uzex":
        if __range > 10 and __range < 10000:
            return True
        else:
            return False
    else:
        return False


def is_user(message) -> bool:
    db = sqlite3.connect("bot.db")
    user_info = list(db.execute(f"select * from User where ID={message.chat.id}"))
    db.close()
    if user_info:
        return True
    else:
        return False
