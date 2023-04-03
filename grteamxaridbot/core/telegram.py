import sqlite3

from grteamxaridbot.core.token import bot
from grteamxaridbot.core.filter import *
from grteamxaridbot.core.xarid_parse import Xarid
from grteamxaridbot.core.xarid_uzex_parse import XaridUzex

def start(message):
    intro = """
Hello, I am `GRXarid` bot!
My tasks:
---
parse `https://api.xt-xarid.uz/urpc`
---
please press to >> /help << for more info!
    """
    if is_user(message) is False:
        db = sqlite3.connect("bot.db")
        db.execute(
            f"insert into User (ID, Username, Name, Last_Name) values ({message.chat.id}, '{message.chat.username}', '{message.chat.first_name}', '{message.chat.last_name}')"
        )
        db.commit()
        db.close()
    bot.send_message(message.chat.id, intro)


def usage(message):
    info = """
_commands_:
/start
/help
/product
/uzex
_examples_:
`/product 60000 200`
---
second parameter > 200:
this should be more `10` and less `10000`
    """
    print(info)
    bot.send_message(message.chat.id, info)


def parse_id(message):
    bot.send_message(message.chat.id, "[#] Xarid")
    Xarid(message, message.text.split()[1], message.text.split(2))


def parse_uzex(message):
    bot.send_message(message.chat.id, "[#] XaridUzex")
    XaridUzex(message, message.text.split()[1], message.text.split()[2])

