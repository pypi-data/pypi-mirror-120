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
class МестныйКлиент:
    """
    Класс, содержащий фукнции для осуществления действий внутри определённого сообщества, ndcId которого указывается в аргументах конструктора
    """
    def __init__(self, область = None):
        self.заголовки = Заголовки().заголовки
        self.мобильные_заголовки = Заголовки().мобильные_заголовки
        self.устройство = Устройство().создать_устройство()
        self.интерфейс = "https://aminoapps.com/api"
        self.мобильный_интерфейс = "https://service.narvii.com/api/v1"
        self.область = область
        self.заголовки["cookie"] = КлиентскиеДанные().данные["сессия"]
        self.мобильные_заголовки["NDCAUTH"] = КлиентскиеДанные().данные["сессия"]
        self.печенье = КлиентскиеДанные().данные["сессия"]
    async def войти_в_чат(self, идентификатор):
        информация = {
            "ndcId": f"x{self.область}",
            "threadId": идентификатор
            }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.интерфейс}/join-thread", json = информация, headers = self.заголовки) as результат:
                ответ = await результат.text()
                ответ = json.loads(ответ)
                try:
                    if ответ["code"] == 200:
                        return ответ["code"]
                    else:
                        raise Исключение(ответ)
                except:
                    raise Исключение(ответ)
    async def отправить_сообщение(self, идентификатор_комнаты_общения, текст, разновидность = 0):
        информация = {
            "ndcId": f"x{self.область}",
            "threadId": идентификатор_комнаты_общения,
            "message": {
                "content": текст,
                "mediaType": 0,
                "type": разновидность,
                "sendFailed": False,
                "clientRefId": 0
                }
            }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.интерфейс}/add-chat-message", json = информация, headers = self.заголовки) as результат:
                ответ = await результат.text()
                ответ = json.loads(ответ)
                try:
                    if ответ["code"] == 200:
                        print(200)
                        return ответ["code"]
                    else:
                        raise Исключение(ответ)
                except:
                    raise Исключение(ответ)
    async def получить_мои_комнаты(self, начало_диапазона = 0, конец_диапазона = 10):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.мобильный_интерфейс}/x{self.область}/s/chat/thread?type=joined-me&start={начало_диапазона}&size={конец_диапазона}", headers = self.мобильные_заголовки) as результат:
                ответ = await результат.json()
                try:
                    ответ = ответ["threadList"]
                    комната = Комната(ответ)
                    return комната
                except:
                    raise Исключение(ответ)
    async def получить_пользователей_в_сети(self, начало_диапазона = 0, конец_диапазона = 10):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.мобильный_интерфейс}/x{self.область}/s/live-layer?topic=ndtopic:x{self.область}:online-members&start={начало_диапазона}&size={конец_диапазона}", headers = self.мобильные_заголовки) as результат:
                ответ = await результат.json()
                try:
                    ответ = ответ["userProfileList"]
                    пользователи = Пользователь(ответ)
                    return пользователи
                except:
                    raise Исключение(ответ)
    async def начать_разговор(self, цели, сообщение):
        информация = {
                "ndcId": self.область,
                "inviteeUids": цели,
                "initialMessageContent": сообщение,
                "type": 0
            }
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.интерфейс}/create-chat-thread", json = информация, headers = self.заголовки) as результат:
                ответ = await результат.text()
                ответ = json.loads(ответ)
                try:
                    if ответ["code"] == 200:
                        return ответ["code"]
                    else:
                        raise Исключение(ответ)
                except:
                    raise Исключение(ответ)