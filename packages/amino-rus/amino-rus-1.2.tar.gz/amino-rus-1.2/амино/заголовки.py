from .устройство import Устройство
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