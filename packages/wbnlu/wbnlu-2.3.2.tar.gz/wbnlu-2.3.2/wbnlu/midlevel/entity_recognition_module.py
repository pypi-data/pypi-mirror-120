from wbnlu import logger
from spacy.tokens import Token
from spacy.util import filter_spans
from spacy.tokens import Span
from ..constants import FeatureAcronymEnum, ExtensionKeys
from ..utils.fileio import read_yaml_file
import dateutil.parser as dparser
import re
from collections import defaultdict
import os

abspath = os.path.abspath(os.path.dirname(__file__))

SPACY_CONFIG = read_yaml_file(os.path.join(abspath, "../configs/spacy_config.yml"))

logger = logger.my_logger(__name__)

NE_EXCLUSION_TYPES = set([fae.name for fae in FeatureAcronymEnum])



class entity_recognition(object):

    name = 'entity_recognition'

    def __init__(self, spacy, rule_match):
        logger.info('Initializing Entity Recognition')
        self.spacy = spacy
        self.patterns = rule_match.patterns['entity']
        self.filters = rule_match.filters['entity']
        self.normalizations = rule_match.normalizations['entity']
        self.rule = rule_match
        self.filter_re_patterns = {}
        # self.timex_re_2 = None
        # self.init_re_patterns()
        self.filter_re_patterns['timex'] = r'\d{1,2}(\.\d{1,2})?分$|\d{1,2}(\.\d{1,2})?分\d{1,2}(\.\d{1,2})?[^秒]|\d:\d$|.*时代'
        self.timex_re_2 = r'^\d{1,3}:\d{1,3}$'
        self.timex_re_3 = r'(今日|昨日|今天|昨天)'
        self.time_filter_suffixes = {'出生','生','生于','出生于','月生','起任','参加工作', '加入中国共产党'}
        self.time_filter_prefixes = {'出生于','生于','月生','每天','每天','每晚','每月','每周','每星期','每礼拜','每季度','每年','经常','常常'}
        self.time_filter_inside_triggers = {'当日', '当天'}
        self.time_types = {'DATE', 'TIME'}
        logger.info('Done with initializing Entity Recognition')


    def __call__(self, doc):

        matches = self.rule.matches
        spans = []
        for match_id, start, end in matches:
            # print (match_id, self.nlp.vocab.strings[match_id], start, end, doc[start:end])
            label = self.spacy.vocab.strings[match_id]
            span = Span(doc, start, end, label=label)
            spans.append(span)

        #ne_exclusive_entities, m_entities_span = filter_entities(spans, [])

        custom_ne_dict = defaultdict(list)
        custom_ne = []
        if 'custom_ne' in doc.user_data:
            for ne in doc.user_data['custom_ne']:
                custom_ne.append(Span(doc, start=ne[0], end=ne[1], label=ne[2]))

        ml_ne = list(doc.ents)
        if ml_ne:
            ml_ne = self.filter_ml(doc, ml_ne, custom_ne)

        #deduplicated_entities = set(ne_exclusive_entities + m_entities_span + ml_ne)
        duplicated_entities = set(spans + ml_ne + custom_ne)
        deduplicated_entities = filter_spans(duplicated_entities)
        deduplicated_entities = self.merge(deduplicated_entities, doc)
        for span in deduplicated_entities:
            # A token can only be part of one entity
            # if not DictionaryFeatureComponent.is_ne(span):
            # doc.ents = list(doc.ents) + [span]
            # custom_ne.append(span)
            if span.label_ in self.time_types:
                if self.trouble_maker_time(doc, span):
                    continue
            text = span.text
            if text not in custom_ne_dict[span.label_]:
                custom_ne_dict[span.label_].append(text)
                for token in span:
                    token._.set(ExtensionKeys.features.name, span.label_)
        # merge span to tokens
        #DictionaryFeatureComponent.merge_ne(ne_exclusive_entities, doc)
        doc.user_data['custom_ne'] = custom_ne_dict
        #doc.user_data['tag_confidence'] = 1.0
        return doc


    def filter_ml(self, doc, ml_ents, dict_ents):
        filtered_ents = []

        # Trust more from rule/dict
        ml_ents_copy = ml_ents.copy()
        for ent in ml_ents_copy:
            for dict_ent in dict_ents:
                if dict_ent.text == ent.text:
                    ml_ents.remove(ent)
                    break

        for ent in ml_ents:
            ne_type = ent.label_
            if ne_type in self.time_types:
                if re.match(self.filter_re_patterns['timex'], ent.text):
                    continue
                if '.' in ent.text or '%' in ent.text:
                    continue
                if ":" in ent.text and not self.is_time(ent.text):
                    continue
                if self.has_filter(ent):
                    filtered_ents.append(ent)
            elif self.wrong_ne(ent):
                continue
            elif ne_type != 'WORK_OF_ART':
                filtered_ents.append(ent)

        return filtered_ents

    def merge(self, ents, doc):

        spans = []
        date_found = None
        new_spans = []
        for ent in ents:
            ne_type = ent.label_
            new_spans.append(ent)
            if ne_type == 'DATE':
                date_found = ent
                continue

            if date_found and ne_type == 'TIME' :
                if date_found.end == ent.start:
                    spans.append(date_found)
                    spans.append(ent)
                    merged_span = entity_recognition.merge_multi_ne(spans, doc)
                    new_spans.remove(date_found)
                    new_spans.remove(ent)
                    new_spans.append(merged_span)
                    date_found = None
                    #return doc.ents
        return new_spans

    @staticmethod
    def merge_multi_ne(spans, doc):
        if spans:
            start = spans[0][0].i
            last_span = spans[len(spans)-1]
            last_token = last_span[len(last_span)-1]
            end = last_token.i+1
            merged_span = Span(doc, start, end, label=last_span.label_)
            #doc.ents = list(doc.ents) + [merged_span]

            with doc.retokenize() as retokenizer:
                retokenizer.merge(merged_span)
            return merged_span
        return spans

    def has_filter(self, ent):
        for filter in self.filters['time']:
            if filter in ent.text:
                return True
        return False

    def _no_overlap(self, span, ents):
        if span in ents:
            return False
        for ent in ents:
            if ent.end < span.start or span.end < ent.start:
                return True
        return False

    def is_time(self, time_str):
        if re.match(self.timex_re_2, time_str):
            return False
        try:
            dparser.parse(time_str, fuzzy=True)
            return True
        except Exception:
            return False

    def trouble_maker_time(self, doc, time_ent):
        last_token = time_ent[len(time_ent)-1]
        tok_id = last_token.i
        doc_len = len(doc)
        # 1987年5月出生
        if doc_len-1 >tok_id:
            if doc[tok_id+1].text in self.time_filter_suffixes:
                return True
            if doc_len-2>tok_id:
                if doc[tok_id+1:tok_id+3].text in self.time_filter_suffixes:
                    return True

        # 出生于 1987年5月
        first_token = time_ent[0]
        if first_token.text in self.time_filter_inside_triggers:
            return True
        tok_id = first_token.i
        if tok_id >0:
            if doc[tok_id-1].text in self.time_filter_prefixes:
                return True
            elif tok_id>1 and doc[tok_id-2].text in self.time_filter_prefixes:
                return True

        return False

    def wrong_ne(self, time_ent):
        if re.match(self.timex_re_3, time_ent.text):
            return True

        return False


