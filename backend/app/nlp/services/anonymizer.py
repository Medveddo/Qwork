import datetime
from random import SystemRandom
from typing import Optional

import natasha
from faker import Faker
from natasha import Doc

from app.nlp.entities.result import ExtractedMatchWithSpan
from app.nlp.services import NatashaProvider


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

    def _anonimyze_names(self) -> None:
        names_with_spans = self.nat.extract_names(self.doc)
        for match in names_with_spans:
            self.text = self._replace_name(self.text, match, self._random_name())

        self._reset_text_shift()

    def _anonimyze_dates(self) -> None:
        dates = self.nat.extract_dates(self.text)
        for date in dates:
            self.text = self._replace_date(self.text, date, self._random_date())

        self._reset_text_shift()

    def _anonimyze_location(self) -> None:
        raise NotImplementedError()

    def _anonymize_organiztaion(self) -> None:
        raise NotImplementedError()

    def anonimyze(self, text: str) -> str:
        self.text = text
        self.doc = self.nat.base_pipeline(text)

        self._anonimyze_names()
        self._anonimyze_dates()
        anoned_text = self.text
        self._reset_state()
        return anoned_text

    def _random_name(self) -> natasha.extractors.obj.Name:
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

    def _random_date(self) -> str:
        date: datetime.date = self.faker.date_between(start_date="-100y")
        return date

    def _replace_name(
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
            f"{text[:match_start + self.text_shift]}" f"{new_name_str}" f"{text[match_stop + self.text_shift:]}"
        )

        self.text_shift += len(new_name_str) - (match_stop - match_start)

        return replaced_text

    def _replace_date(
        self,
        text: str,
        date: natasha.extractors.Match,
        new_date: datetime.date,
    ):
        date_str = new_date.strftime("%d.%m.%Y")

        replaced_text = f"{text[:date.start + self.text_shift]}" f"{date_str}" f"{text[date.stop + self.text_shift:]}"
        self.text_shift += len(date_str) - (date.stop - date.start)
        return replaced_text

    def _reset_state(self) -> None:
        self.text_shift = 0
        self.text = None
        self.doc = None

    def _reset_text_shift(self) -> None:
        self.text_shift = 0


anonymizer_ = Anonymizer()
