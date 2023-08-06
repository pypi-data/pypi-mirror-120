import time
import json
import aiohttp
import random
import string
import asyncio

from aiohttp.helpers import HeadersMixin
class КлиентскаяИнформация:
    """
    Класс, хранящий информацию о пользователе
    """
    инфо = {}
class Сообщество:
    """
    Объект списка сообществ, возвращаемый функцией получить_мои_сообщества(...)
    """
    def __init__(self, объект):
        self.объект = объект
        self.название = []
        self.идентификатор = []
        for элемент in объект:
            self.название.append(элемент['name'])
            self.идентификатор.append(элемент['ndcId'])
class Комната:
    """
    Объект списка чатов, возвращаемый функцией получить_мои_комнаты(...)
    """
    def __init__(self, объект):
        self.объект = объект
        self.название = []
        self.идентификатор = []
        for элемент in объект:
            self.название.append(элемент['title'])
            self.идентификатор.append(элемент['threadId'])
class Пользователь:
    """
    Объект списка пользователей, возвращаемый функцией получить_пользователей_в_сети(...)
    """
    def __init__(self, объект):
        self.объект = объект
        self.идентификатор = []
        self.имя = []
        self.профильное_изображение = []
        for элемент in объект:
            self.идентификатор.append(элемент['uid'])
            self.имя.append(элемент['nickname'])
            self.профильное_изображение.append(элемент['icon'])
class Устройство:
    """
    Класс, отвечающий за генерацию DeviceID.
    """
    def создать_устройство(self):
        строка = random.randint(0, 500)
        with open("варианты", mode='r') as в:
            список = в.read().splitlines()
        результат = random.choice(список)
        return результат
class Исключение(Exception):
    def __init__(self, сообщение):
        super().__init__(сообщение)
class НеверныйПароль(Exception):
    def __init__(self, сообщение):
        super().__init__(сообщение)
class НевернаяПочта(Exception):
    def __init__(self, сообщение):
        super().__init__(сообщение)
class Заголовки:
    """
    Класс, хранящий заголовки запросов к API Amino
    """
    def __init__(self):
        self.заголовки = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
            "x-requested-with": "xmlhttprequest",
            "Accept-Language": "ru-UA"
        }
        self.мобильные_заголовки = {
            "NDCDEVICEID": Устройство().создать_устройство(),
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; Redmi Note 8 Build/PKQ1.190616.001; com.narvii.amino.master/3.4.33578)",
            "Host": "service.narvii.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Accept-Language": "ru-UA"
        }
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
                print(ответ)
                try:
                    self.имя = ответ["result"]["nickname"]
                    self.печенье = результат.headers["set-cookie"]
                    self.печенье = self.печенье[0: self.печенье.index(";")]
                    self.уникальный_идентификатор = ответ["result"]["uid"]
                    self.заголовки["cookie"] = self.печенье
                    self.заголовки["cookie"] = self.печенье
                    self.мобильные_заголовки["NDCAUTH"] = self.печенье
                    КлиентскаяИнформация().инфо["сессия"] = self.печенье
                    КлиентскаяИнформация().инфо["имя"] = self.имя
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
class МестныйКлиент(Клиент):
    """
    Класс, содержащий фукнции для осуществления действий внутри определённого сообщества, ndcId которого указывается в аргументах конструктора
    """
    def __init__(self, область = None):
        super().__init__()
        self.область = область
        self.заголовки["cookie"] = КлиентскаяИнформация().инфо["сессия"]
        self.мобильные_заголовки["NDCAUTH"] = КлиентскаяИнформация().инфо["сессия"]
        self.печенье = КлиентскаяИнформация().инфо["сессия"]
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
                        print(200)
                        return ответ["code"]
                    else:
                        raise Исключение(ответ)
                except:
                    raise Исключение(ответ)