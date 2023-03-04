#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from core.telegram import *
from core.token import bot
from core.filter import *
from logger import Logger

Logger()


@bot.message_handler(commands=['start', 'help'])
def bot_command(message):
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


if __name__ == "__main__":
    bot.polling(non_stop=True)
