from wbnlu import logger

from ..constants import SegmentationGrammar, PatternTypeEnum
from ..utils.pattern_loader import PatternLoader
from spacy.util import filter_spans
from spacy.matcher import Matcher
from spacy.tokens import Span
# from .extractors.constants import PatternTypeEnum
from ..utils.fileio import read_yaml_file
from ..components.text_normalizer import has_hangul
import os

abspath = os.path.abspath(os.path.dirname(__file__))

SPACY_CONFIG = read_yaml_file(os.path.join(abspath, "../configs/spacy_config.yml"))

logger = logger.my_logger(__name__)


class RuleSegmenter(object):
    name = "rule_segmenter"

    def __init__(self, nlp, disable):
        self.patterns = PatternLoader.load_nlp_pattern(PatternTypeEnum.segmentation, disable)
        self.nlp = nlp
        self.matcher = Matcher(nlp.vocab, validate=True)
        self.segmentation_definition = {}

        logger.info('Compiling segmentation patterns starts ...')

        for segmentation_type, label_list in SegmentationGrammar.items():
            for label in label_list:
                self.segmentation_definition[label] = segmentation_type
                if label == '(c1c1_pub)' and 'timex' not in disable:
                    continue
                for pattern in self.patterns:
                    if label in pattern:
                        grammar = pattern[label]
                        self.matcher.add(label, None, *grammar)
                        break
        logger.info('Compiling segmentation patterns ends ...')

    def __call__(self, doc):

        matches = self.matcher(doc)
        #spans = list(doc.ents)
        to_be_merged = []
        to_be_split = []
        for match_id, start, end in matches:

            label = self.nlp.vocab.strings[match_id]
            if label == '(c1c1)' or label == '(c1c1_pub)':
                start = start+1
                end = end -1
            elif label == 'c2c1_punct':
                end = end - 1
            elif label == 'punct_c1c2_punct':
                start = start + 1
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
        RuleSegmenter.merge_span(filter_spans(to_be_merged), doc)
        return doc

    @staticmethod
    def merge_span(spans, doc):
        with doc.retokenize() as retokenizer:
            for span in spans:
                if span.label_ == '(c1c1_pub)':
                    retokenizer.merge(span, attrs={"TAG": "NR"})
                else:
                    retokenizer.merge(span)
                    #merged_indexes.add(span[0].idx)
                    #doc.user_data['pub'] = (span.start, span.end, span.label_)
                    #doc.user_data['pub'] = span
        # for token in doc:
        #     if merged_indexes and token.idx in merged_indexes:
        #         merged_indexes.remove(token.idx)
        #         token._.features = 'pub'
        #     if not merged_indexes:
        #         break



    def to_be_skipped(self, start, end, doc, label):

        if end <len(doc)-1:
            current_text = doc[start:end].text
            if has_hangul(current_text):
                return False
            left_token = doc[end-1:end][0]
            # if left_token.is_ascii:
            #     next_span = doc[end:end+1]
            #     if next_span.text == ':':
            #         return True
        return False

    @staticmethod
    def split_tokens(spans, doc):
        with doc.retokenize() as retokenizer:
            heads = [(doc[3], 0), (doc[3], 1), (doc[3], 2)]
            retokenizer.split(doc[3], ["New", "York", "City"], heads=heads)
