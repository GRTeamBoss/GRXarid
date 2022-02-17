import re
from typing import Union

from telebot.types import Message
import requests


class Xarid:


    id = False


    def __init__(self, message: Message, start: Union[str, int], end: Union[str, int]) -> None:
        self.start = int(start)
        self.end = int(end)
        self.parse()
        with open(f'./Files/{message.chat.id}_{message.date}.xlsx') as file:
            bot.send_document(message.chat.id, data=file.read(), visible_file_name=f"xt_{self.start}_{self.start+self.end}.xlsx", caption="@gr_team_xarid_bot")


    def parse(self):
        __header = {
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
        self.create_excel_file(message)
        excel_row = 2
        for num in range(self.start, self.end+self.start+1):
            self.id = num
            __params = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "get_proc",
                "params": {
                    "proc_id": self.id
                }
            }
            response = requests.post("https://api.xt-xarid.uz/urpc", headers=__header, json=__params)
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
                    value = f"ID:\r\t{data[0]}\nИмя товара:\r\t{data[1]}\nСтрана:\r\t{data[3]}\nСрок торга:\r\t{data[4]}\nЦена:\r\t{data[5]}\nКоличество:\r\t{data[6]}\nРайоны:\r\t{data[7]}\nСсылка:\r\t{data[8]}"
                    bot.send_message(message.chat.id, value) 
                    self.write_to_excel(message, __data, excel_row)
                    excel_row += 1


    def create_excel_file(self, message) -> None:
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
        wb.save(filename=f"./Files/{message.chat.id}_{message.date}.xlsx")


    def write_to_excel(self, message, data, excel_row) -> None:
        wb = openpyxl.load_workbook(f"./Files/{message.chat.id}_{message.date}.xlsx")
        sheet = wb.active
        for num in range(len(data)):
            sheet.cell(row=excel_row, column=num+1).value = data[num]
        wb.save(filename=f"./Files/{message.chat.id}_{message.date}.xlsx")

