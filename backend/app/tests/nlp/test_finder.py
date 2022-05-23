from typing import List

import pytest
from pydantic import BaseModel

from app.nlp.entities.clinrec import ALL_CLINICAL_RECOMENDATIONS
from app.nlp.entities.feature import (  # noqa
    ATRIAL_FIBRILATION_FEATURE,
    BLOOD_PRESSURE_FEATURE,
    BODY_MASS_INDEX_FEATURE,
    ELECTROCARDIOGRAM_FEATURE,
    GENERAL_BLOOD_ANALYSIS_FEATURE,
    HEART_RATE_FEATURE,
    HEIGHT_FEATURE,
    TEMPERATURE_FEATURE,
    WEIGHT_FEATURE,
    Feature,
)
from app.nlp.services import FeatureFidnder


class FinderTestCase(BaseModel):
    text: str
    expected_features: List[Feature]


finder_test_cases = [
    FinderTestCase(
        text="Состояние удовлетворительное.  РОСТ= 174см,   ВЕС=100 кг,  ИМТ=33,03.  Ожирение 1  ст.  Тоны сердца  приглушены  аритмичные, мерцательная аритмия  с  ЧСС=86   уд/мин.  АД= 127/103  мм.рт.ст.  В легких дыхание везикулярное,хрипов нет.  Живот   увеличен в обьеме  за счет п/к жирового слоя.  Отеков нет.  По ЭКГ фибрилляция предсердий с ЧСС=62-74уд. мин. Диффузные изменения миокарда.  Хс=   нет данных.  ХМ ЭКГ и заключение их НИИПК прилагаются.",  # noqa
        expected_features=[
            HEIGHT_FEATURE,
            WEIGHT_FEATURE,
            BODY_MASS_INDEX_FEATURE,
            HEART_RATE_FEATURE,
            BLOOD_PRESSURE_FEATURE,
            ELECTROCARDIOGRAM_FEATURE,
            ATRIAL_FIBRILATION_FEATURE,
        ],
    ),
    FinderTestCase(
        text="Состояние: удовлетворительное. Рост 180 см, вес 96 кг.ИМТ 29,63. В легких аускультативно везикулярное дыхание, хрипов нет. Тоны сердца умеренно приглушены, ритмичные, акцент 2 тона над аортой, ЧСС 86 в мин. АД 120/80 мм.рт.ст. Живот мягкий, печень +1 см из-под края реберной дуги. Незначительная пастозность голеней. ЭКГ: 01.08.2018 Ритм синусовый с ЧСС 74 в мин. ЭОС влево. Неполная AV блокада 1 ст. Тенденция к снижению вольтажа в стандартных отведениях. БАК сдал по месту жительства, результат в работе.",  # noqa
        expected_features=[
            HEIGHT_FEATURE,
            WEIGHT_FEATURE,
            BODY_MASS_INDEX_FEATURE,
            HEART_RATE_FEATURE,
            BLOOD_PRESSURE_FEATURE,
            ELECTROCARDIOGRAM_FEATURE,
            GENERAL_BLOOD_ANALYSIS_FEATURE,
        ],
    ),
]


@pytest.mark.parametrize(
    argnames="test_case",
    argvalues=finder_test_cases,
    ids=[
        "finder_0",
        "finder_1",
    ],
)
def test_nlp_finder(test_case: FinderTestCase):
    finder = FeatureFidnder()
    result = finder.find_features(test_case.text, ALL_CLINICAL_RECOMENDATIONS)
    found_features = [found_result.feature for found_result in result.features_found]
    for expected_feature in test_case.expected_features:
        assert expected_feature in found_features
