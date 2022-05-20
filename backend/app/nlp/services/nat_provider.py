from typing import List

from natasha import (
    PER,
    DatesExtractor,
    Doc,
    MorphVocab,
    NamesExtractor,
    NewsEmbedding,
    NewsMorphTagger,
    NewsNERTagger,
    NewsSyntaxParser,
    Segmenter,
)
from natasha.doc import DocSpan
from natasha.extractors import Match

from app.nlp.entities.result import ExtractedMatchWithSpan


class NatashaProvider:
    """
    Wrapper around natasha library
    """

    def __new__(cls):
        if not hasattr(cls, "instance"):
            print("Initializing NatashaProvider")
            cls.instance = super(NatashaProvider, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.syntax_parser = NewsSyntaxParser(self.emb)
        self.ner_tagger = NewsNERTagger(self.emb)
        self.names_extractor = NamesExtractor(self.morph_vocab)
        self.dates_extractor = DatesExtractor(self.morph_vocab)

    def base_pipeline(self, text: str) -> Doc:
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)
        doc.tag_ner(self.ner_tagger)

        for token in doc.tokens:
            token.lemmatize(self.morph_vocab)

        return doc

    def extract_names(self, doc: Doc) -> List[ExtractedMatchWithSpan]:
        result: List[ExtractedMatchWithSpan] = []
        for span in doc.spans:
            span: DocSpan
            if span.type == PER:
                match = self.names_extractor.find(span.text)
                result.append(ExtractedMatchWithSpan(match, span))
        return result

    def extract_dates(self, text: str) -> List[Match]:
        return self.dates_extractor(text)
