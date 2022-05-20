from typing import List

from pydantic import BaseModel

from .feature import (
    ATRIAL_FIBRILATION_FEATURE,
    BASIC_FEATURES_LIST,
    BLOOD_PRESSURE_FEATURE,
    ELECTROCARDIOGRAM_FEATURE,
    GENERAL_BLOOD_ANALYSIS_FEATURE,
    HEART_RATE_FEATURE,
    Feature,
)


class ClinicalRecomindations(BaseModel):
    title: str
    key: str
    codes: str
    link: str
    features: List[Feature]


ATRIAL_FIBRILATION_AND_FLUTTER_CLINICAL_RECOMENDATIONS = ClinicalRecomindations(  # noqa
    title="Фибрилляция и трепетание предсердий у взрослых",
    key="atrial_fibrilation_and_flutter",
    codes="I48.0 I48.1 I48.2 I48.3 I48.4 I48.9",
    link="https://cr.minzdrav.gov.ru/recomend/382_1",
    features=[
        ELECTROCARDIOGRAM_FEATURE,
        ATRIAL_FIBRILATION_FEATURE,
        GENERAL_BLOOD_ANALYSIS_FEATURE,
        HEART_RATE_FEATURE,
    ],
)
ACUTE_CORONARY_SYNDROME_CLINICAL_RECOMENDATIONS = ClinicalRecomindations(
    title="Острый коронарный синдром без подъема сегмента ST электрокардиограммы",
    key="acute_coronary_syndrome",
    codes="I20.0, I21.0, I21.1, I21.2, I21.3, I21.4, I21.9, I22.0, I22.1, I22.8, I22.9, I24.8, I24.9",
    link="https://cr.minzdrav.gov.ru/recomend/154_3",
    features=[
        BLOOD_PRESSURE_FEATURE,
    ],
)

ALL_CLINICAL_RECOMENDATIONS = ClinicalRecomindations(
    title="Все доступные признаки",
    key="all",
    codes="",
    link="",
    features=BASIC_FEATURES_LIST,
)

TYPE_TO_CLINREC_MAPPING = {
    "acute_coronary_syndrome": ACUTE_CORONARY_SYNDROME_CLINICAL_RECOMENDATIONS,
    "atrial_fibrilation_and_flutter": ATRIAL_FIBRILATION_AND_FLUTTER_CLINICAL_RECOMENDATIONS,
    "all": ALL_CLINICAL_RECOMENDATIONS,
}
