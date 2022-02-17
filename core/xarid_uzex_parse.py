import time
from typing import Union

import requests, openpyxl
from telebot.types import Message

from core.token import bot

__header = {
'accept': 'application/json',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9',
'content-type': 'application/json; charset=utf-8',
'language': 'ru',
'origin': 'https://xarid.uzex.uz',
'referer': 'https://xarid.uzex.uz/',
'sec-ch-ua': '"(Not(A:Brand";v="8", "Chromium";v="98"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Linux"',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-site',
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
}


def parse(message: Message, start: Union[str, int], end: Union[str, int]) -> None:
    excel_row = 1
    create_excel(message)
    status = False
    for num in range(int(start), int(end)+int(start)+1):
        print("id:", num)            
        time.sleep(1)
        resp = requests.get(f"https://xarid-api-shop.uzex.uz/Common/GetLot/{num}", headers=__header)    
        if resp.status_code == 200:
            values = resp.json()
            parse_bot = parse_values(values, method='bot')
            parse_excel = parse_values(values, method='excel')
            bot.send_message(message.chat.id, parse_bot)
            write_to_excel(message, parse_excel, excel_row)
            excel_row += 1
            status = True
        else:
            values = f"id {num}: Error! May be wrong response or connection is closed"
            bot.send_message(message.chat.id, values)
    if status:
        with open(f"./Files/{message.chat.id}_uzex_{message.date}.xlsx", "rb") as file:
            bot.send_document(chat_id=message.chat.id, data=file.read(), visible_file_name=f"uzex_{start}_{int(start)+int(end)}.xlsx")
    else:
        bot.send_message(message.chat.id, "Not parsed!")



def parse_values(data, method: str) -> Union[str, list]:
    if method == "bot":
        value = ""
        value += f"[*] Категория: {data['category_name']}\n"
        value += f"[*] Название товара: {data['product_name']}\n"
        value += f"[*] Параметры: {data['condition']}\n"
        value += f"[*] Гарантийный период: {data['guarantee_period']}\n"
        value += f"[*] Гарантийный период в единицах измерения: {data['guarantee_period_name']}\n"
        value += f"[*] Лицензия: {'Имеется' if data['is_licensed'] is True else 'Не имеется'}\n"
        value += f"[*] ID лицензии: {data['license_id'] if data['is_licensed'] is True else 'Нет'}\n"
        value += f"[*] Количество: {data['lot_amount']}\n"
        value += f"[*] Начала лота: {data['lot_start_date']}\n"
        value += f"[*] Конец лота: {data['lot_end_date']}\n"
        value += f"[*] Статус лота: {data['lot_status_name']}\n"
        value += f"[*] Максимальное количество поставки: {data['max_delivery_amount']}\n"
        value += f"[*] Цена: {data['price']} UZS\n"
        value += f"[*] Код продукта: {data['product_code']}\n"
        value += f"[*] Дата производства: {data['start_date']}\n"
        value += f"[*] Статус продукта: {data['status_name']}\n"
        value += f"[*] Ссылка: https://xarid.uzex.uz/shop/lot-details/{data['lot_display_no'][-5:]}"
        return value
    elif method == "excel":
        value = []
        value.append(data['category_name'])
        value.append(data['product_name'])
        value.append(data['condition'])
        value.append(data['delivery_term'])
        value.append(data['delivery_term_period_name'])
        value.append(data['guarantee_period'])
        value.append(data['guarantee_period_name'])
        value.append('Имеется' if data['is_licensed'] is True else 'Не имеется')
        value.append(data['license_id'] if data['is_licensed'] is True else 'Нет')
        value.append(data['lot_amount'])
        value.append(data['lot_start_date'])
        value.append(data['lot_end_date'])
        value.append(data['lot_status_name'])
        value.append(data['manufacturer_name'])
        value.append(data['mark_name'])
        value.append(data['max_delivery_amount'])
        value.append(data['min_delivery_amount'])
        value.append(data['offer_display_no'])
        value.append(data['price'])
        value.append(data['producer_country_name'])
        value.append(data['product_code'])
        value.append(data['shelf_life'])
        value.append(data['shelf_life_name'])
        value.append(data['start_date'])
        value.append(data['status_name'])
        value.append("https://xarid.uzex.uz/shop/lot-details/{data['lot_display_no'][-5:]}")
        return value


def create_excel(message: Message) -> None:
    wb = openpyxl.Workbook()
    sheet = wb.active
    __values = (
        "ID",
        "Категория",
        "Имя товара",
        "Состав",
        "Время доставки",
        "Единица измерения",
        "Гарантийный период",
        "Единица измерения",
        "Лиценизия",
        "ID Лицензии",
        "Количество лота",
        "Начало лота",
        "Конец лота",
        "Статус лота",
        "Производитель",
        "Марка товара",
        "Макс. количество доставки",
        "Мин. количество доставки",
        "Оффер",
        "Цена",
        "Страна производителя",
        "Код продукта",
        "Срок годности",
        "Единица измерения",
        "Дата выпуска продукта",
        "Статус продукта"
        "Ссылка"
    )
    for num in range(0, len(__values)):
        sheet.cell(row=1, column=num+1).value = __values[num]
    wb.save(filename=f"./Files/{message.chat.id}_uzex_{message.date}.xlsx")


def write_to_excel(message, data, excel_row) -> None:
    wb = openpyxl.load_workbook(f"./Files/{message.chat.id}_uzex_{message.date}.xlsx")
    sheet = wb.active
    for num in range(len(data)):
        sheet.cell(row=excel_row, column=num+1).value = data[num]
    wb.save(filename=f"./Files/{message.chat.id}_uzex_{message.date}.xlsx")
