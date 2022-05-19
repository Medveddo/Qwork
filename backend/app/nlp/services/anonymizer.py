import datetime
from typing import Optional

from faker import Faker
from app.nlp.services import NatashaProvider

from natasha import Doc
import natasha

from random import SystemRandom

from app.nlp.entities.result import ExtractedMatchWithSpan


class Anonymizer:
    """Responsible for removing any personal data from text"""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            print("Initializing Anonymizer")
            cls.instance = super(Anonymizer, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.nat = NatashaProvider()
        self.text: Optional[str] = None
        self.faker = Faker("ru_RU")
        self.doc: Optional[Doc] = None
        self.rnd = SystemRandom()
        self.text_shift = 0

    def anonimyze_names(self) -> None:
        names_with_spans = self.nat.extract_names(self.doc)
        for match in names_with_spans:
            self.text = self.replace_name(self.text, match, self.random_name())

    def anonimyze_dates(self) -> None:
        dates = self.nat.extract_dates(self.text)
        for date in dates:
            self.text = self.replace_date(self.text, date, self.random_date())

    def anonimyze_location(self) -> None:
        raise NotImplementedError()

    def anonymize_organiztaion(self) -> None:
        raise NotImplementedError()

    def anonimyze(self, text: str) -> str:
        self.text = text
        self.doc = self.nat.base_pipeline(text)

        self.anonimyze_names()
        self._reset_text_shift()
        self.anonimyze_dates()
        text = self.text
        self._reset_state()
        return text

    def random_name(self) -> natasha.extractors.obj.Name:
        if self.rnd.randint(0, 1):
            return natasha.extractors.obj.Name(
                first=self.faker.first_name(),
                last=self.faker.last_name(),
                middle=self.faker.middle_name(),
            )

        return natasha.extractors.obj.Name(
            first=self.faker.first_name_female(),
            last=self.faker.last_name_female(),
            middle=self.faker.middle_name_female(),
        )

    def random_date(self) -> str:
        date: datetime.date = self.faker.date_between(start_date="-60y")
        return date

    def replace_name(
        self,
        text: str,
        match: ExtractedMatchWithSpan,
        new_name: natasha.extractors.obj.Name,
    ) -> str:
        old_name = match.match.fact
        new_name_str = ""

        if old_name.last:
            if len(old_name.last) == 1:
                new_name_str += new_name.last[0] + ". "
            else:
                new_name_str += new_name.last + " "

        if old_name.first:
            if len(old_name.first) == 1:
                new_name_str += new_name.first[0] + ". "
            else:
                new_name_str += new_name.first + " "

        if old_name.middle:
            if len(old_name.middle) == 1:
                new_name_str += new_name.middle[0] + ". "
            else:
                new_name_str += new_name.middle + " "

        new_name_str = new_name_str.strip()

        match_start = match.span.start + match.match.start
        match_stop = match_start + match.match.stop

        replaced_text = (
            f"{text[:match_start + self.text_shift]}"
            f"{new_name_str}"
            f"{text[match_stop + self.text_shift:]}"
        )

        self.text_shift += len(new_name_str) - (match_stop - match_start)

        return replaced_text

    def replace_date(
        self,
        text: str,
        date: natasha.extractors.Match,
        new_date: datetime.date,
    ):
        date_str = new_date.strftime("%d.%m.%Y")

        replaced_text = (
            f"{text[:date.start + self.text_shift]}"
            f"{date_str}"
            f"{text[date.stop + self.text_shift:]}"
        )
        self.text_shift += len(date_str) - (date.stop - date.start)
        return replaced_text

    def _reset_state(self) -> None:
        self.text_shift = 0
        self.text = None
        self.doc = None

    def _reset_text_shift(self) -> None:
        self.text_shift = 0


if __name__ == "__main__":
    text1 = "Пациент Кондратьева Азарий Димитриевич. Дата рождения 20.12.1981. Всё хорошо. Благодарить надо Зуева Валентина Наумовна. Действие происходило в Городской Поликлинике №1 Новосибирска 28.10.1970."
    text2 = "Данилова Э.А. родилась 11 июля 1999. Поэтому 17 августа был устроен праздник."
    text3 = "Товарищ Иванов попросил закурить"

    anon = Anonymizer()

    print(
        anon.anonimyze(text1)
    )  # Пациент Ширяева Жанна Юльевна. Дата рождения 25.07.2005. Всё хорошо. Благодарить надо Журавлева Хохлов Виктория. Действие происходило в Городской Поликлинике №1 Новосибирска 30.09.1991.
    print(
        anon.anonimyze(text2)
    )  # Цветкова Е. Ф. родилась 13.02.2007. Поэтому 16.07.1989 был устроен праздник.
    print(anon.anonimyze(text3))  # Товарищ Иван попросил закурить
