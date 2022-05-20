from typing import List, Optional

from pydantic import BaseModel


class Keyword(BaseModel):
    # class Type(Enum):
    #     SINGLE = 0
    #     MULTIWORD = 1

    keyword: str
    levenshtein_tolerance: Optional[int] = None
    # type: Optional[Type] = None

    # def __init__(
    #     self,
    #     keyword: str,
    # ) -> None:
    #     self.type: self.Type = (
    #         self.Type.SINGLE
    #         if len(keyword.strip().split()) == 1
    #         else self.Type.MULTIWORD
    #     )


class Feature(BaseModel):
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
    # TODO banlist, e.g. "уд" для Артериального давления АД

    def __hash__(self) -> int:
        return hash(self.key)


HEART_RATE_FEATURE = Feature(
    description="Частота сердечных сокращений",
    key="heart_rate",
    keywords=[
        Keyword(keyword="чсс", levenshtein_tolerance=1),
    ],
)

BLOOD_PRESSURE_FEATURE = Feature(
    description="Артериальное давление",
    key="blood_pressure",
    keywords=[
        Keyword(keyword="давление"),
        Keyword(keyword="ад", levenshtein_tolerance=1),
        Keyword(keyword="артериальный"),
        Keyword(keyword="давл"),
        Keyword(keyword="артериальный давление"),
    ],
)

TEMPERATURE_FEATURE = Feature(
    description="Температура",
    key="temperature",
    keywords=[
        Keyword(keyword="температура"),
        Keyword(keyword="темп"),
    ],
)

ELECTROCARDIOGRAM_FEATURE = Feature(
    description="Электрокардиограмма (ЭКГ)",
    key="electrocardiogram",
    keywords=[Keyword(keyword="экг")],
)

ATRIAL_FIBRILATION_FEATURE = Feature(
    description="Фибрилляция пердсердий",
    key="atrial_fibrillation",
    keywords=[
        Keyword(keyword="фп"),
        Keyword(keyword="фибриляция"),
        Keyword(keyword="предсердие"),
    ],
)

GENERAL_BLOOD_ANALYSIS_FEATURE = Feature(
    description="Общий анализ крови",
    key="general_blood_analysis",
    keywords=[Keyword(keyword="оак", levenshtein_tolerance=1)],
)

WEIGHT_FEATURE = Feature(description="Вес", key="weight", keywords=[Keyword(keyword="вес")])

HEIGHT_FEATURE = Feature(description="Рост", key="height", keywords=[Keyword(keyword="рост")])

BODY_MASS_INDEX_FEATURE = Feature(
    description="Индекс массы тела",
    key="body_mass_index",
    keywords=[Keyword(keyword="имт", levenshtein_tolerance=1)],
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
