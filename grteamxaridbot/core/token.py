import os, pathlib

from telebot import TeleBot


class Token:


    def __init__(self) -> None:
        self.__TOKEN = "5083456307:AAENuIpz_8N5RG3UqPdHtf6B37ANjIUJkUs"
        self.__bot = TeleBot(self.__TOKEN, parse_mode='MARKDOWN')


    def parse_environment(self, key: str) -> str:
        content = str(pathlib.Path('./.env').read_text()).splitlines()
        for item in content:
            k, v = item.split("=", 1)
            if key == k:
                return v
        return ""

    def activate(self):
        if pathlib.Path('./.env').exists():
            self.__TOKEN = self.parse_environment('TOKEN')
        else:
            self.__TOKEN = os.environ.get('TOKEN', "")
        if self.__TOKEN == "":
            print("[#] You might set environment with TOKEN from telegram bot or write key pair TOKEN in '.env' file in same directory where placed 'main.py'")
            exit(1)

    @property
    def get(self) -> TeleBot:
        return self.__bot



bot = Token().get
