from typing import List

import Levenshtein  # use as Levenshtein.distance('test', 'tesst')

from app.nlp.entities import Feature, Keyword
from natasha import Doc
from natasha.doc import DocToken


class LevenshteinProvider:
    """Responsible for helps find features using Levenshtein distance"""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            print("Initializing LevenshteinProvider")
            cls.instance = super(LevenshteinProvider, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.lev = Levenshtein

    def is_keywords_in_token(
        self, keywords: List[Keyword], token: DocToken
    ) -> bool:
        for keyword in keywords:
            if (
                self.lev.distance(token.text.lower(), keyword.keyword.lower())
                <= keyword.levenshtein_tolerance
            ):
                return True

        return False


if __name__ == "__main__":
    pass
