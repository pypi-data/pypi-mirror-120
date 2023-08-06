class Исключение(Exception):
    def __init__(self, сообщение):
        super().__init__(сообщение)
class НеверныйПароль(Exception):
    def __init__(self, сообщение):
        super().__init__(сообщение)
class НевернаяПочта(Exception):
    def __init__(self, сообщение):
        super().__init__(сообщение)