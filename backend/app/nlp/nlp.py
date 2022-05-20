# from dataclasses import dataclass
# from typing import List, Optional, Tuple

# from loguru import logger
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
# from natasha.doc import DocSent, DocToken
# from pyaspeller import YandexSpeller

# segmenter = Segmenter()
# morph_vocab = MorphVocab()

# emb = NewsEmbedding()
# morph_tagger = NewsMorphTagger(emb)
# syntax_parser = NewsSyntaxParser(emb)
# ner_tagger = NewsNERTagger(emb)

# names_extractor = NamesExtractor(morph_vocab)

# separators = ("/", "-", "|", "\\")
# cconjes = ("на", "и")


# @dataclass
# class TempBloodPressRecomendations:
#     temperature: Optional[int] = None
#     blood_pressure: Optional[Tuple[int, int]] = None

#     def is_fully_correspond(self) -> bool:
#         if self.temperature and self.blood_pressure and self.blood_pressure[0] and self.blood_pressure[1]:
#             return True

#         return False

#     def show_info(self) -> None:
#         if self.temperature:
#             logger.info(f"Temperature: {self.temperature}")
#         else:
#             logger.info("Temperature is not found in text.")

#         if self.blood_pressure and self.blood_pressure[0] and self.blood_pressure[1]:
#             logger.info(f"Blood pressure: {self.blood_pressure}")
#         else:
#             logger.info("Blood pressure is not found in text.")


# RECOMENDATIONS_KEYWORDS = {
#     "temperature": ("температура", "темп"),
#     "blood_pressure": ("давление", "артериальный", "давл", "ад"),
# }


# def isfloat(value: str):
#     try:
#         float(value)
#         return True
#     except ValueError:
#         return False


# def exclude_punct_and_adp(tokens: List[DocToken]) -> List[DocToken]:
#     return [token for token in tokens if token.pos not in ("ADP", "PUNCT")]


# def extract_temperature(tokens: List[DocToken]) -> Optional[float]:
#     temp_tokens = [token for token in tokens if token.lemma in RECOMENDATIONS_KEYWORDS["temperature"]]
#     if not temp_tokens:
#         return 0

#     logger.debug(f"Found temperature keyword:\n{temp_tokens}")

#     numerics = [token for token in tokens if token.pos == "NUM" or isfloat(token.text)]
#     if not numerics:
#         return 0

#     for token in numerics:
#         if "," in token.text:
#             token.text = token.text.strip(",").replace(",", ".")

#     numerics = [
#         token
#         for token in numerics
#         if not any(separator in token.text for separator in separators) and 33.0 <= float(token.text) <= 45.0
#     ]

#     if not numerics:
#         return None
#     logger.debug(f"Numerics in temerature sentence:\n{numerics}")
#     if len(numerics) == 1:
#         return float(numerics[0].text)

#     logger.warning("(temperature) More than one numerics in sentence")
#     logger.warning("ERROR MAY OCCUR")
#     return float(numerics[0].text)


# def get_numeric_tokens_with_separator(tokens: List[DocToken]) -> List[DocToken]:
#     return [token for token in tokens if any(separator in token.text for separator in separators)]


# def numerics_with_cconj_between(
#     tokens: List[DocToken],
# ) -> List[Tuple[DocToken, DocToken, DocToken]]:
#     result = []
#     for i, token in enumerate(tokens):
#         if (
#             token.lemma in cconjes
#             and i > 0
#             and i < len(tokens) - 1
#             and tokens[i - 1].pos == "NUM"
#             and tokens[i + 1].pos == "NUM"
#         ):
#             result.append((tokens[i - 1], token, tokens[i + 1]))

#     logger.success(f"NUMERICS WITH CCONJ BETWEEN: {result}")
#     return result  # [(120, на, 80)]


# def extract_blood_pressure(
#     tokens: List[DocToken],
# ) -> Tuple[Optional[int], Optional[int]]:
#     blood_pressure_tokens = [token for token in tokens if token.lemma in RECOMENDATIONS_KEYWORDS["blood_pressure"]]
#     if not blood_pressure_tokens:
#         return (None, None)

#     logger.debug(f"Found blood pressure keyword:\n{blood_pressure_tokens}")

#     numerics = [token for token in tokens if token.pos == "NUM" or isfloat(token.text) or has_digits(token.text)]

#     with_separator = get_numeric_tokens_with_separator(numerics)

#     if not numerics:
#         return (None, None)

#     if with_separator:
#         if len(with_separator) == 1:
#             sep = ""
#             for separator in separators:
#                 if separator in with_separator[0].text:
#                     sep = separator
#                     break
#             pressures = with_separator[0].text.split(sep)
#             return int(pressures[0]), int(pressures[1])
#         else:
#             logger.warning(f"MORE THAN ONE NUMERICS WITH SEPARATOR: {with_separator}")

#     if list_of_matches := numerics_with_cconj_between(tokens):
#         if len(list_of_matches) == 1:
#             # ist_of_matches[0] = (120, "на", 80)
#             first = int(list_of_matches[0][0].text)
#             second = int(list_of_matches[0][2].text)
#             if first > second and first > 42 and second > 42:
#                 return (first, second)
#         else:
#             logger.warning((f"MORE THAN ONE GROUP OF NUMERICS WITH" f"CCONJ BETWEEN: {list_of_matches}"))

#     numerics = [token for token in numerics if float(token.text) > 42]

#     # Вместо этого трая надо отсеивать всё чо float и оставлять всё чо инт
#     try:
#         logger.debug(f"Numerics in blood pressure sentence:\n{numerics}")
#         if len(numerics) == 1:
#             return (int(numerics[0].text), None)

#         logger.warning("(blood_pressure) More than one numerics in sentence")
#         logger.warning("ERROR MAY OCCUR")
#         return (int(numerics[0].text), None)
#     except ValueError as ex:
#         logger.error(ex)
#         return (None, None)


# @dataclass
# class Result:
#     is_correspond: bool = False
#     temperature: Optional[float] = None
#     systole_pressure: Optional[int] = None
#     diastole_pressure: Optional[int] = None


# def has_digits(text: str) -> bool:
#     return any(ch.isdigit() for ch in text)


# def verify_temp_and_blood_pressure(text: str) -> Result:
#     speller = YandexSpeller()
#     text = speller.spelled(text)

#     # Natasha text actions
#     doc = Doc(text)
#     doc.segment(segmenter)
#     doc.tag_morph(morph_tagger)
#     doc.parse_syntax(syntax_parser)
#     doc.tag_ner(ner_tagger)

#     for token in doc.tokens:
#         token.lemmatize(morph_vocab)

#     recomendations_correspondence = TempBloodPressRecomendations()
#     result = Result()
#     # Processing
#     sentence: DocSent
#     for i, sentence in enumerate(doc.sents):
#         print(f"SENTENCE #{i+1}\n  TEXT: {sentence.text}")
#         # sent_tokens = exclude_punct_and_adp(sentence.tokens)
#         sent_tokens = sentence.tokens
#         temperature = extract_temperature(sent_tokens)
#         blood_pressure = extract_blood_pressure(sent_tokens)
#         if temperature:
#             logger.success(f"Found temperature: {temperature}")
#             recomendations_correspondence.temperature = temperature
#             result.temperature = temperature
#         if blood_pressure and all(blood_pressure):
#             logger.success(f"Found blood pressure: {blood_pressure}")
#             recomendations_correspondence.blood_pressure = blood_pressure
#             result.systole_pressure = blood_pressure[0]
#             result.diastole_pressure = blood_pressure[1]

#     recomendations_correspondence.show_info()
#     result.is_correspond = recomendations_correspondence.is_fully_correspond()

#     return result


# if __name__ == "__main__":
#     texts = [
#         # "Мама мыла раму",  # ❌
#         # "Температура давление",  # ❌
#         "Пациент приехал с температурой 38.6 градусов. Артериальное давление высокое - 160/120",  # ✅
#         "Температура 37 Давление 100/80.",  # ✅
#         "Температура градусов 37. Давление 100 и 80.",  # ✅
#         "Температура градусов 37. Давление 120 на 100.",  # ✅
#         "Температура градусов 37. Давление 100",  # ✅
#         "температура 36 давление 120 и 80",  # ✅
#         "Температура в норме, давление окей",  # ✅
#         "Температура 38. Давление низкое",  # ✅
#         "37 температура 120/80 давление",  # ✅
#         "Повышенная температура. Давление 90",  # ✅
#         "Повышенная температура. давление 90",  # ✅
#         "давление 140/100, температура 38.4",  # ✅
#         "температура с давлением были высоки - 39.1 и 160/110",  # ✅
#         "Температура и давление пациента: 37 и 120/80",  # ✅
#         "Температура и давление 37 и 100 соответственно",  # ✅
#         "Температура и давление 37 и 100/70 соответственно",  # ✅
#         "Температура и давление были 39.1, 190",  # ✅
#         "Температура и давление были 39.1, 190 на 120",  # ✅
#         # "Темп 37 гц, давл 190/120, прекол",
#         "Состояние: удовлетворительное. АД  130/80  мм. рт.ст. Тоны сердца: аритмичные, приглушены. Дыхание: везикулярное, хрипов нет. Живот б/о. На ЭКГ - фибрилляция предсердий, ЧСС 80.", # noqa
#     ]
#     results = []
#     for text in texts:
#         result = verify_temp_and_blood_pressure(text)
#         results.append(
#             (
#                 text,
#                 "✅" if result.is_correspond else "❌",
#                 result.temperature,
#                 result.systole_pressure,
#                 result.diastole_pressure,
#             )
#         )
#     print("RESULTS:")
#     print("| text | соответствует ли рекомендациям | температура | систолическое давление | диастолическое давление |") # noqa
#     for result in results:
#         print(result)
