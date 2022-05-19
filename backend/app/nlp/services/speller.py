from pyaspeller import YandexSpeller


class Speller:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            print("Initializing Speller")
            cls.instance = super(Speller, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.speller = YandexSpeller()

    def correct_spelling(self, text: str) -> str:
        return self.speller.spelled(text)
