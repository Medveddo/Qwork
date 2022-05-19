from dataclasses import dataclass
from typing import Any, Optional, Union
from app.nlp.entities import Feature

from natasha.doc import DocToken, DocSent, DocSpan
import natasha


@dataclass
class ExtractedMatchWithSpan:
    """
    Can be used with names extraction because 
    NamesExtractor gives you Match'es with start/stop
    relative to DocSpan, not whole doc
    """
    match: natasha.extractors.Match
    span: DocSpan


class FeatureFindResult:
    def __init__(
        self,
        feature: Feature,
        token: DocToken,
        sentence: Optional[DocSent] = None,
    ) -> None:
        self.feature = feature
        self.token = token
        self.sentence = sentence
        self.found = True

    def __str__(self) -> str:
        return (
            f"FeatureFindResult(feature={self.feature.key}, "
            f"token={self.token}, "
            f"sentence={self.sentence})"
        )

    def __repr__(self) -> str:
        return (
            f"FeatureFindResult(feature={self.feature.key}, "
            f"token={self.token}, "
            f"sentence={self.sentence})"
        )


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
