import time
import json
import aiohttp
import random
import string
import asyncio
from .устройство import Устройство
from .заголовки import Заголовки
from .данные import КлиентскиеДанные
from .исключения import *
from .объекты import *
class Клиент:
    """
    Главный класс, отвечающий за авторизацию и глобальные действия
    """
    def __init__(self):
        self.заголовки = Заголовки().заголовки
        self.мобильные_заголовки = Заголовки().мобильные_заголовки
        self.устройство = Устройство().создать_устройство()
        self.интерфейс = "https://aminoapps.com/api"
        self.мобильный_интерфейс = "https://service.narvii.com/api/v1"
    def получить_проверку(self):
        проверка = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + "_-", k=462)).replace("--", "-")
        return проверка
    async def войти(self, почта, пароль):
        информация = {
            "auth_type": 0,
            "email": почта,
            "recaptcha_challenge": self.получить_проверку(),
            "recaptcha_version": "v3",
            "secret": пароль
            }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.интерфейс}/auth", json = информация) as результат:
                ответ = await результат.text()
                ответ = json.loads(ответ)
                try:
                    self.имя = ответ["result"]["nickname"]
                    self.печенье = результат.headers["set-cookie"]
                    self.печенье = self.печенье[0: self.печенье.index(";")]
                    self.уникальный_идентификатор = ответ["result"]["uid"]
                    self.заголовки["cookie"] = self.печенье
                    self.заголовки["cookie"] = self.печенье
                    self.мобильные_заголовки["NDCAUTH"] = self.печенье
                    КлиентскиеДанные()["сессия"] = self.печенье
                    КлиентскиеДанные()["имя"] = self.имя
                    self.loggedin = True
                except:
                    try:
                        if ответ["result"]["api:message"] == "Account or password is incorrect! If you forget your password, please reset it.":
                            raise НеверныйПароль(ответ["result"]["api:message"])
                        elif ответ["result"]["api:message"] == "Invalid email address.":
                            raise НевернаяПочта(ответ["result"]["api:message"])
                    except:
                        raise Исключение(ответ)
    async def войти_в_сообщество(self, идентификатор):
        информация = {
            "ndcId": идентификатор
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.интерфейс}/join", json = информация, headers = self.заголовки) as результат:
                ответ = await результат.text()
                ответ = json.loads(ответ)
                try:
                    if ответ["code"] == 200:
                        return ответ["code"]
                    else:
                        raise Исключение(ответ)
                except:
                    raise Исключение(ответ)
    async def получить_мои_сообщества(self, начало_диапазона = 0, конец_диапазона = 10):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.мобильный_интерфейс}/g/s/community/joined?v=1&start={начало_диапазона}&size={конец_диапазона}", headers = self.мобильные_заголовки) as результат:
                ответ = await результат.json()
                try:
                    ответ = ответ["communityList"]
                    сообщество = Сообщество(ответ)
                    return сообщество
                except:
                    raise Исключение(ответ)