from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class Keyword:
    class Type(Enum):
        SINGLE = 0
        MULTIWORD = 1

    def __init__(
        self, keyword: str, levenshtein_tolerance: Optional[int] = None
    ) -> None:
        self.keyword = keyword
        self.levenshtein_tolerance = levenshtein_tolerance
        self.type: self.Type = (
            self.Type.SINGLE if len(keyword.strip().split()) == 1 else self.Type.MULTIWORD
        )


@dataclass
class Feature:
    """
    Feature that need to be extracted from text

    :keywords should be lowercase

    Examples
    --------
    f = Feature(["чсс"], 1)

    Means that "чжс", also must return True when finding
    this feature in text using levenshtein distance
    """

    description: str
    key: str
    keywords: List[Keyword]

    def __hash__(self) -> int:
        return hash(self.key)


HEART_RATE_FEATURE = Feature(
    description="Частота сердечных сокращений",
    key="heart_rate",
    keywords=[
        Keyword("чсс", 1),
    ],
)

BLOOD_PRESSURE_FEATURE = Feature(
    description="Артериальное давление",
    key="blood_pressure",
    keywords=[
        Keyword("давление"),
        Keyword("ад", 1),
        Keyword("артериальный"),
        Keyword("давл"),
        Keyword("артериальный давление"),
    ],
)

TEMPERATURE_FEATURE = Feature(
    description="Температура",
    key="temperature",
    keywords=[
        Keyword("температура"),
        Keyword("темп"),
    ],
)

ELECTROCARDIOGRAM_FEATURE = Feature(
    description="Электрокардиограмма (ЭКГ)",
    key="electrocardiogram",
    keywords=[Keyword("экг")],
)

ATRIAL_FIBRILATION_FEATURE = Feature(
    description="Фибрилляция пердсердий",
    key="atrial_fibrillation",
    keywords=[Keyword("фп")],
)

GENERAL_BLOOD_ANALYSIS_FEATURE = Feature(
    description="Общий анализ крови",
    key="general_blood_analysis",
    keywords=[Keyword("оак", 1)],
)

WEIGHT_FEATURE = Feature(
    description="Вес", key="weight", keywords=[Keyword("вес")]
)

HEIGHT_FEATURE = Feature(
    description="Рост", key="height", keywords=[Keyword("рост")]
)

BODY_MASS_INDEX_FEATURE = Feature(
    description="Индекс массы тела",
    key="body_mass_index",
    keywords=[Keyword("имт", 1)],
)

BASIC_FEATURES_LIST = [
    HEART_RATE_FEATURE,
    BLOOD_PRESSURE_FEATURE,
    TEMPERATURE_FEATURE,
    ELECTROCARDIOGRAM_FEATURE,
    ATRIAL_FIBRILATION_FEATURE,
    GENERAL_BLOOD_ANALYSIS_FEATURE,
    WEIGHT_FEATURE,
    HEIGHT_FEATURE,
    BODY_MASS_INDEX_FEATURE,
]
