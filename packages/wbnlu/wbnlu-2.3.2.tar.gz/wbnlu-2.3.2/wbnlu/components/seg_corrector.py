from wbnlu import logger
from .extractors.dictionary_feature_component import DictionaryFeatureComponent

from .extractors.constants import SegmentationGrammar
from .extractors.pattern_loader import PatternLoader
from spacy.util import filter_spans
from spacy.matcher import Matcher
from spacy.tokens import Span
from .extractors.constants import PatternTypeEnum
from .utils.fileio import read_yaml_file
from .components.text_normalizer import has_hangul
import os

abspath = os.path.abspath(os.path.dirname(__file__))

SPACY_CONFIG = read_yaml_file(os.path.join(abspath, "./configs/spacy_config.yml"))

logger = logger.my_logger(__name__)

class Seg_Corrector(object):

    def __init__(self, nlp):
        self.patterns = PatternLoader.load_nlp_pattern(PatternTypeEnum.segmentation)
        self.nlp = nlp
        self.matcher = Matcher(nlp.vocab, validate=True)
        self.segmentation_definition = {}

        logger.info('Compiling segmentation patterns starts ...')

        for segmentation_type, label_list in SegmentationGrammar.items():
            for label in label_list:
                self.segmentation_definition[label] = segmentation_type
                for pattern in self.patterns:
                    if label in pattern:
                        grammar = pattern[label]
                        self.matcher.add(label, None, *grammar)
                        break

    def __call__(self, doc):
        matches = self.matcher(doc)
        #spans = list(doc.ents)
        to_be_merged = []
        to_be_split = []
        for match_id, start, end in matches:

            label = self.nlp.vocab.strings[match_id]
            if label == '(c1c1)':
                start = start+1
                end = end -1
            elif label == 'c2c1_punct':
                end = end - 1
            if not self.to_be_skipped(start, end, doc, label):
                span = Span(doc, start, end, label=label)
                if self.segmentation_definition[label] == 'merge':
                    to_be_merged.append(span)
                elif self.segmentation_definition[label] == 'split':
                    to_be_split.append(span)
                else:
                    raise ValueError("Invalid rule label: ", label)

        # merge span to tokens
        DictionaryFeatureComponent.merge_ne(filter_spans(to_be_merged), doc)
        for token in doc:
            if previous_token and previous_token.text == '[':
                token._.set('bracket', True)
            elif previous_token and token.text == ']':
                previous_token._.set('bracket', True)
            previous_token = token
        return doc


    def to_be_skipped(self, start, end, doc, label):

        if end <len(doc)-1:
            current_text = doc[start:end].text
            if has_hangul(current_text):
                return False
            left_token = doc[end-1:end][0]
            if left_token.is_ascii:
                next_span = doc[end:end+1]
                if next_span.text == ':':
                    return True
        return False

    @staticmethod
    def split_tokens(spans, doc):
        with doc.retokenize() as retokenizer:
            heads = [(doc[3], 0), (doc[3], 1), (doc[3], 2)]
            retokenizer.split(doc[3], ["New", "York", "City"], heads=heads)
