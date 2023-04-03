#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import pathlib

from grteamxaridbot.core.telegram import *
from grteamxaridbot.core.token import bot
from grteamxaridbot.core.filter import *


@bot.message_handler(commands=['start', 'help'])
def bot_command(message):
    print(message.text)
    funcs = {
        "/start": start,
        "/help": usage,
    }
    funcs[message.text](message)


@bot.message_handler(func=lambda message: parse_method(message) is True)
def parse_command(message):
    if message.text.split()[0] == '/uzex':
        parse_uzex(message)
    elif message.text.split()[0] == '/product':
        parse_id(message)


def setup():
    if pathlib.Path('./Files').exists() is True:
        print('[#] Folder `./Files` is exist!')
    else:
        pathlib.Path('./Files').mkdir()
        print('[#] Folder `./Files` created!')


if __name__ == "__main__":
    setup()
    print("[*] START")
    bot.infinity_polling()
    print("[*] END")
