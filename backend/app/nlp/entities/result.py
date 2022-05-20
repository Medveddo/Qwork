from dataclasses import dataclass
from typing import Any, List, Optional, Union

import natasha
from natasha.doc import DocSent, DocSpan, DocToken
from pydantic import BaseModel

from app.nlp.entities import Feature


@dataclass
class ExtractedMatchWithSpan:
    """
    Can be used with names extraction because
    NamesExtractor gives you Match'es with start/stop
    relative to DocSpan, not whole doc
    """

    match: natasha.extractors.Match
    span: DocSpan


class FeatureFindResult(BaseModel):
    feature: Feature
    token: DocToken
    sentence: Optional[DocSent] = None
    # def __init__(
    #     self,
    # ) -> None:
    #     self.feature = feature
    #     self.token = token
    #     self.sentence = sentence
    #     self.found = True

    class Config:
        arbitrary_types_allowed = True

    def __str__(self) -> str:
        return f"FeatureFindResult(feature={self.feature.key}, " f"token={self.token}, " f"sentence={self.sentence})"

    def __repr__(self) -> str:
        return f"FeatureFindResult(feature={self.feature.key}, " f"token={self.token}, " f"sentence={self.sentence})"


class FeatureExtractionResult:
    def __init__(
        self,
        feature: Feature,
        value: Union[int, float, str, Any],
        units: Optional[str] = None,
    ) -> None:
        self.feature = feature
        self.value = value
        self.units = units


class FoundMissingFeatures(BaseModel):
    features_found: List[FeatureFindResult]
    features_missing: List[Feature]
