from importlib.abc import Finder
from typing import List, Optional
from app.nlp.services import NatashaProvider, LevenshteinProvider
from app.nlp.entities import Feature, FeatureFindResult, ClinicalRecomindations
from app.nlp.entities.clinrec import (
    ATRIAL_FIBRILATION_AND_FLUTTER_CLINICAL_RECOMENDATIONS,
)
from natasha import Doc
from natasha.doc import DocToken, DocSent


class FeatureFidnder:
    """
    Responsible for just finding feature in text without extracting related value
    """

    def __new__(cls):
        if not hasattr(cls, "instance"):
            print("Initializing FeatureFidnder")
            cls.instance = super(FeatureFidnder, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.nat = NatashaProvider()
        self.text: Optional[str] = None
        self.doc: Optional[Doc] = None
        self.lev_provider: LevenshteinProvider = LevenshteinProvider()

    def find_features(
        self,
        text: str,
        clinrec: ClinicalRecomindations,
    ) -> List[FeatureFindResult]:
        self.text = text  # TODO test .lower()
        self.doc = self.nat.base_pipeline(text)

        looking_features = clinrec.features
        results: List[FeatureFindResult] = []
        for sentance in self.doc.sents:
            sentance: DocSent
            for token in sentance.tokens:
                for feature in looking_features:
                    # TODO if feature.has_multiword_keywords() -> process with sentance or doc.
                    if self._feature_in_token(feature, token):
                        results.append(
                            FeatureFindResult(feature, token, sentance)
                        )

        print("Found features:")
        for result in results:
            print(result.feature.description, "-", result.sentence.text)

        print("Missing features:")
        missing_features: List[Feature] = set(looking_features) - set(
            [r.feature for r in results]
        )
        for feature in missing_features:
            print(feature.description)

    def _feature_in_token(self, feature: Feature, token: DocToken) -> bool:
        plain_keywords = [keyword.keyword for keyword in feature.keywords]
        if (token.lemma in plain_keywords) or (
            token.text.lower() in plain_keywords
        ):
            return True
        leven_keywords = [keyword for keyword in feature.keywords if keyword.levenshtein_tolerance]
        if leven_keywords is not None:
            if self.lev_provider.is_keywords_in_token(leven_keywords, token):
                return True

        return False

FINDER = FeatureFidnder()

if __name__ == "__main__":
    TEXT = "Состояние: удовлетворительное. Рост 180 см, вес 96 кг.ИМТ 29,63. В легких аускультативно везикулярное дыхание, хрипов нет. Тоны сердца умеренно приглушены, ритмичные, акцент 2 тона над аортой, ЧСС 86 в мин. АД 120/80 мм.рт.ст. Живот мягкий, печень +1 см из-под края реберной дуги. Незначительная пастозность голеней. ЭКГ: 01.08.2018 Ритм синусовый с ЧСС 74 в мин. ЭОС влево. Неполная AV блокада 1 ст. Тенденция к снижению вольтажа в стандартных отведениях. БАК сдал по месту жительства, результат в работе."  # noqa

    FINDER.find_features(
        TEXT, ATRIAL_FIBRILATION_AND_FLUTTER_CLINICAL_RECOMENDATIONS
    )
