import re, requests, openpyxl, pathlib, typing, telebot, core

from ..logger import Logger
from typing import Union
from telebot.types import Message
from core.token import bot


class Xarid:

    """
    :private: id
    :param: message, start, end
    :method: parse, create_excel_file, write_to_excel
    :description: API for parse log with ID.
    """

    __ID = False
    __HEADER = {
        "Host": "api.xt-xarid.uz",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://xt-xarid.uz/",
        "X-DBRPC-Language": "ru",
        "Content-Type": "application/json;charset=utf-8",
        "Origin": "https://xt-xarid.uz",
        "Content-Length": "73",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TE": "trailers",
    }

    def __init__(self, message: Message, start: Union[str, int], end: Union[str, int]):
        self.message = message
        self.start = int(start)
        self.end = int(end)
        self.logger = Logger().logger
        self.__parse()
        data = pathlib.Path(f'./Files/{self.message.chat.id}_{self.message.date}.xlsx').read_bytes()
        bot.send_document(message.chat.id, data=data, visible_file_name=f"xt_{self.start}_{self.start+self.end}.xlsx", caption="@gr_team_xarid_bot")

    def __parse(self):
        self.__create_excel_file()
        excel_row = 2
        __params = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "get_proc",
            "params": {
                "proc_id": self.__ID
            }
        }
        for num in range(self.start, self.end+self.start+1):
            self.__ID = num   
            response = requests.post("https://api.xt-xarid.uz/urpc", headers=self.__HEADER, json=__params)
            if response.status_code == 200:
                print(f"[*] {self.id} parsed!")
                json = response.json()
                if json["result"]["status"] == "open" and json["result"]["type"] == "request":
                    __data = []
                    __regions = json["result"]["fields"]["regions"]["value"]
                    __regions_value = ""
                    for item in __regions:
                        __regions_value += re.findall(r">{1}[\w\W]+<{1}", item)[0].strip("<>") + ";"
                    __data.append(str(json["result"]["proc_id"]))
                    __data.append(json["result"]["fields"]["brand"]["value"])
                    __data.append(json["result"]["fields"]["desc"]["value"])
                    __data.append(json["result"]["fields"]["country"]["value"])
                    __data.append(json["result"]["fields"]["close_at"]["value"])
                    __data.append(json["result"]["fields"]["price"]["value"])
                    __data.append(json["result"]["fields"]["amount"]["value"])
                    __data.append(__regions_value)
                    __data.append(f"https://xt-xarid.uz/procedure/{json['result']['proc_id']}/core")
                    value = f"ID:\r\t{__data[0]}\nИмя товара:\r\t{__data[1]}\nСтрана:\r\t{__data[3]}\nСрок торга:\r\t{__data[4]}\nЦена:\r\t{__data[5]}\nКоличество:\r\t{__data[6]}\nРайоны:\r\t{__data[7]}\nСсылка:\r\t{__data[8]}"
                    bot.send_message(self.message.chat.id, value) 
                    self.__write_to_excel(self.message, __data, excel_row)
                    excel_row += 1
                else:
                    self.logger.info(f"[ID = {self.__ID}] [status = {json['result']['status']}]")
            else:
                self.logger.info(f"[ID = {self.__ID}] [status = {response.status_code}]")

    def __create_excel_file(self):
        wb = openpyxl.Workbook()
        sheet = wb.active
        __values = (
            "ID",
            "Имя товара",
            "Описание",
            "Страна производства",
            "Срок торга",
            "Цена",
            "Количество",
            "Районы",
            "Ссылка"
        )
        for num in range(0, len(__values)):
            sheet.cell(row=1, column=num+1).value = __values[num]
        wb.save(filename=f"./Files/{self.message.chat.id}_{self.message.date}.xlsx")

    def __write_to_excel(self, data, excel_row):
        wb = openpyxl.load_workbook(f"./Files/{self.message.chat.id}_{self.message.date}.xlsx")
        sheet = wb.active
        for num in range(len(data)):
            sheet.cell(row=excel_row, column=num+1).value = data[num]
        wb.save(filename=f"./Files/{self.message.chat.id}_{self.message.date}.xlsx")

