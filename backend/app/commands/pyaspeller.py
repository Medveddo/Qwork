from pyaspeller import YandexSpeller

speller = YandexSpeller()

input = "Уравень эритрацитов в крови"

print(speller.spelled(input))
