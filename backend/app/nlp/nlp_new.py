# # python -m app.nlp.nlp_new
# from typing import List, Optional

# from natasha import (
#     Doc,
#     MorphVocab,
#     NamesExtractor,
#     NewsEmbedding,
#     NewsMorphTagger,
#     NewsNERTagger,
#     NewsSyntaxParser,
#     Segmenter,
# )


# from app.nlp.entities import (
#     Feature,
#     ClinicalRecomindations,
# )

# from app.nlp.entities.clinrec import (
#     ATRIAL_FIBRILATION_AND_FLUTTER_CLINICAL_RECOMENDATIONS,
# )

# from app.nlp.leven import Distanter
# from app.nlp.services import NatashaProvider


# class ClinRecFinder:
#     def __init__(self) -> None:
#         self.nat = NatashaProvider()
#         self.text: Optional[str] = None
#         self.doc: Optional[Doc] = None
#         self.distanter: Distanter = Distanter()

#     def find_features(
#         self, text: str, clin_rec: ClinicalRecomindations
#     ) -> List[Feature]:
#         self.text = text
#         self.doc = self.nat.base_pipeline(text)

#         looking_features = clin_rec.features
#         found_features = []

#         for token in self.doc.tokens:
#             for feature in looking_features:
#                 if (token.lemma in feature.keywords) or (
#                     token.text in feature.keywords
#                 ):
#                     found_features.append(feature)
#                     # continue  # ?
#                 if feature.levenshtein_tolerance is not None:
#                     if self.distanter.check_feaute_in_text_with_leven(
#                         token.text, feature
#                     ) or self.distanter.check_feaute_in_text_with_leven(
#                         token.lemma, feature
#                     ):
#                         # TODO check if found text
#                         # not in other features keywords - ok
#                         # otherwise - skip
#                         found_features.append(feature)

#         print(self.text)
#         print(" --- ")
#         print(" ".join([token.lemma for token in self.doc.tokens]))

#         print("Found features:")
#         found_features: List[Feature] = set(found_features)
#         for feature in found_features:
#             print(feature.description)

#         print("Missing features:")
#         missing_features: List[Feature] = set(looking_features) - set(
#             found_features
#         )
#         for feature in missing_features:
#             print(feature.description)

#         print(
#             f"Accordance value: {len(found_features) / len(looking_features) * 100 :.2f}%"
#         )
#         # TODO: post processing after pyaspeller


# if __name__ == "__main__":

#     TEXT = "Состояние: удовлетворительное. Рост 180 см, вес 96 кг.ИМТ 29,63. В легких аускультативно везикулярное дыхание, хрипов нет. Тоны сердца умеренно приглушены, ритмичные, акцент 2 тона над аортой, ЧСС 86 в мин. АД 120/80 мм.рт.ст. Живот мягкий, печень +1 см из-под края реберной дуги. Незначительная пастозность голеней. ЭКГ: 01.08.2018 Ритм синусовый с ЧСС 74 в мин. ЭОС влево. Неполная AV блокада 1 ст. Тенденция к снижению вольтажа в стандартных отведениях. БАК сдал по месту жительства, результат в работе."  # noqa

#     crf = ClinRecFinder()
#     crf.find_features(TEXT, ATRIAL_FIBRILATION_AND_FLUTTER_CLINICAL_RECOMENDATIONS)
