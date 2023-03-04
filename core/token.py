import os

from telebot import TeleBot


bot = TeleBot(os.environ.get("TOKEN", None), parse_mode="MARKDOWN")