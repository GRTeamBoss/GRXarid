import os, pathlib

from telebot.async_telebot import AsyncTeleBot

__TOKEN = None

def parse_environment(key: str) -> str:
    content = str(pathlib.Path('./../.env').read_text()).splitlines()
    for item in content:
        k, v = item.split("=", 1)
        if key == k:
            return v
    return None


if pathlib.Path('./../.env').exists():
    __TOKEN = parse_environment('TOKEN')
else:
    __TOKEN = os.environ.get('TOKEN')

if __TOKEN is None:
    print("[#] You might set environment with TOKEN from telegram bot or write key pair TOKEN in '.env' file in same directory where placed 'main.py'")
    exit(1)
else:
    bot = AsyncTeleBot(__TOKEN, parse_mode="MARKDOWN")