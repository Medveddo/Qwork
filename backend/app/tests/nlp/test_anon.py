from typing import Tuple

import pytest

from app.nlp.services.anonymizer import anonymizer_


@pytest.mark.parametrize(
    argnames=("text", "anonned"),
    argvalues=[
        (
            "Пациент Кондратьева Азарий Димитриевич. Дата рождения 20.12.1981. Всё хорошо. Благодарить надо Зуева Валентина Наумовна. Действие происходило в Городской Поликлинике №1 Новосибирска 28.10.1970.",  # noqa
            ("Кондратьева", "Азарий", "Димитриевич", "20", "Зуева", "Валентина", "Наумовна", "28"),
        ),
        ("Данилова Э.А. родилась 11 июля 1999. Поэтому 17 августа был устроен праздник.", ("Данилова", "11", "17")),
        ("Товарищ Иванов попросил закурить", ("Иванов",)),
    ],
    ids=["anon3", "anon1", "anon2"],
)
def test_anonymizer(text: str, anonned: Tuple[str, ...]):
    anon_text = anonymizer_.anonimyze(text)
    print(text)
    print(anon_text)
    for token in anonned:
        assert token not in anon_text
