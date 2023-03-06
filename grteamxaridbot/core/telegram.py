import sqlite3

from telebot.types import *

from core.token import bot
from core.filter import *
from core.xarid_parse import Xarid
from core.xarid_uzex_parse import XaridUzex


async def start(message):
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
    await bot.send_message(message.chat.id, intro)


async def usage(message):
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
    await bot.send_message(message.chat.id, info)


async def parse_id(message):
    await Xarid(message, message.text.split()[1], message.text.split(2))


async def parse_uzex(message) -> None:
    await XaridUzex(message, message.text.split()[1], message.text.split()[2])

