import re

import requests


class Xarid:


    def __init__(self, id) -> None:
        self.id = str(id)


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
                return __data
            else:
                return "Nope"
        else:
            return False