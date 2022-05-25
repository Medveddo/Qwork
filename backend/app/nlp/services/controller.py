from loguru import logger

from app.nlp.entities.clinrec import TYPE_TO_CLINREC_MAPPING, ClinicalRecomindations
from app.nlp.services.anonymizer import Anonymizer
from app.nlp.services.finder import FINDER
from app.schemas import FeaturesResult, TextInput


class Controller:
    """
    Responsible to get all input data,
    execute needed NLP services and
    return parsed result
    """

    def __new__(cls):
        if not hasattr(cls, "instance"):
            print("Initializing Controller")
            cls.instance = super(Controller, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.finder = FINDER

    def process_text_with_related_clinrecs(self, input_: TextInput) -> FeaturesResult:
        logger.debug(f"{input_=}")
        input_.text = Anonymizer().anonimyze(input_.text)
        logger.debug(f"{input_=}")

        clinrecs = self._get_clinrec_by_type(input_.type)
        logger.debug(f"{clinrecs=}")
        result = self.finder.find_features(input_.text, clinrecs)
        return FeaturesResult(
            found_features=list(
                {found_feature_result.feature.description for found_feature_result in result.features_found}
            ),
            missing_features=[missing_feature.description for missing_feature in result.features_missing],
        )

    def _get_clinrec_by_type(self, type_: str) -> ClinicalRecomindations:
        return TYPE_TO_CLINREC_MAPPING[type_]


controller_service = Controller()
