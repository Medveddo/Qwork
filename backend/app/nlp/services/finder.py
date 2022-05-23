from typing import List, Optional

from natasha import Doc
from natasha.doc import DocSent, DocToken

from app.nlp.entities import ClinicalRecomindations, Feature, FeatureFindResult
from app.nlp.entities.result import FoundMissingFeatures
from app.nlp.services import LevenshteinProvider, NatashaProvider


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
    ) -> FoundMissingFeatures:
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
                        results.append(FeatureFindResult(feature=feature, token=token, sentence=sentance))

        print("Found features:")
        for result in results:
            print(result.feature.description, "-", result.sentence.text)

        found_feature_keywords = set([result.feature.key for result in results])

        print("Missing features:")
        missing_features: List[Feature] = [
            feature for feature in clinrec.features if feature.key not in found_feature_keywords
        ]

        for feature in missing_features:
            print(feature.description)

        return FoundMissingFeatures(features_found=results, features_missing=missing_features)

    def _feature_in_token(self, feature: Feature, token: DocToken) -> bool:
        if self._token_is_in_banlist(feature, token):
            return False

        plain_keywords = [keyword.keyword for keyword in feature.keywords]
        if (token.lemma in plain_keywords) or (token.text.lower() in plain_keywords):
            return True
        leven_keywords = [keyword for keyword in feature.keywords if keyword.levenshtein_tolerance]
        if leven_keywords is not None:
            if self.lev_provider.is_keywords_in_token(leven_keywords, token):
                return True

        return False

    def _token_is_in_banlist(self, feature: Feature, token: DocToken) -> bool:
        if not feature.banlist:
            return False

        banned_keywords = [keyword.keyword for keyword in feature.banlist]
        if banned_keywords:
            if token.lemma in banned_keywords:
                return True
            if token.text in banned_keywords:
                return True


FINDER = FeatureFidnder()
