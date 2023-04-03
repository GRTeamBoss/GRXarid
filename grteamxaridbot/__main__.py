#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import asyncio

from grteamxaridbot.core.telegram import *
from grteamxaridbot.core.token import bot
from grteamxaridbot.core.filter import *


@bot.message_handler(commands=['start', 'help'])
async def bot_command(message):
    print(message.text)
    funcs = {
        "/start": start,
        "/help": usage,
    }
    funcs[message.text](message)


@bot.message_handler(func=lambda message: parse_method(message) is True)
async def parse_command(message):
    if message.text.split()[0] == '/uzex':
        parse_uzex(message)
    elif message.text.split()[0] == '/product':
        parse_id(message)


if __name__ == "__main__":
    print("[*] START")
    asyncio.run(bot.polling(non_stop=True, interval=0))
    print("[*] END")
