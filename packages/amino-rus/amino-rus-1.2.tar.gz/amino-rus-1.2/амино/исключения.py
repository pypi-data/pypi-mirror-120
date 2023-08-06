class Исключение(Exception):
    def __init__(self, сообщение):
        super().__init__(сообщение)
        try:
            self.url = сообщение["url"]
        except:
            pass
class НеверныйПароль(Exception):
    def __init__(self, сообщение):
        super().__init__(сообщение)
class НевернаяПочта(Exception):
    def __init__(self, сообщение):
        super().__init__(сообщение)
class ЗапрошеноПодтверждение(Exception):
    def __init__(self, сообщение):
        super().__init__(сообщение)
        self.url = сообщение["url"]
class ВасЗаблокировали(Exception):
    def __init__(self, сообщение):
        super().__init__(сообщение)
class ПриглашенияОтключены(Exception):
    def __init__(self, сообщение):
        super().__init__(self, сообщение)