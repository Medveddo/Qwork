from typing import List, Optional

from pydantic import BaseModel


class Keyword(BaseModel):
    keyword: str
    levenshtein_tolerance: Optional[int] = None


class Feature(BaseModel):
    description: str
    key: str
    keywords: List[Keyword]
    banlist: List[Keyword] = []

    def __hash__(self) -> int:
        return hash(self.key)


HEART_RATE_FEATURE = Feature(
    description="Частота сердечных сокращений",
    key="heart_rate",
    keywords=[
        Keyword(keyword="чсс", levenshtein_tolerance=1),
    ],
    banlist=[Keyword(keyword="чжс")],
)

BLOOD_PRESSURE_FEATURE = Feature(
    description="Артериальное давление",
    key="blood_pressure",
    keywords=[
        Keyword(keyword="давление"),
        Keyword(keyword=r"а\д"),
        Keyword(keyword="ад", levenshtein_tolerance=1),
        Keyword(keyword="артериальный"),
        Keyword(keyword="давл"),
        Keyword(keyword="артериальный давление"),
    ],
    banlist=[Keyword(keyword="уд")],
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
    # banlist=[Keyword(keyword="бак")]
)

WEIGHT_FEATURE = Feature(description="Вес", key="weight", keywords=[Keyword(keyword="вес")])

HEIGHT_FEATURE = Feature(description="Рост", key="height", keywords=[Keyword(keyword="рост")])

BODY_MASS_INDEX_FEATURE = Feature(
    description="Индекс массы тела",
    key="body_mass_index",
    keywords=[Keyword(keyword="имт", levenshtein_tolerance=1)],
)

CARDIAC_TROPONIN_FEATURE = Feature(
    description="Уровень сердечных тропонинов",
    key="cardiac_troponin",
    keywords=[
        Keyword(keyword="тропонин"),
        Keyword(keyword="тропонины"),
    ],
)

CHOLESTEROL_FEATURE = Feature(
    description="Уровень холестерина",
    key="cholesterol",
    keywords=[
        Keyword(keyword="холестерин"),
    ],
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
    CARDIAC_TROPONIN_FEATURE,
    CHOLESTEROL_FEATURE,
]
