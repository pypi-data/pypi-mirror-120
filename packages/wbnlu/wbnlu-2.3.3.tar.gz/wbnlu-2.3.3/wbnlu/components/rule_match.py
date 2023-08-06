from ..utils.pattern_loader import PatternLoader
from wbnlu import logger
from spacy.matcher import Matcher
from spacy.tokens import Token, Span
from spacy.util import filter_spans
from ..constants import FeatureAcronymEnum, ExtensionKeys

import re
from collections import defaultdict
import os
import copy


logger = logger.my_logger(__name__)


class rule_match(object):

    name = 'rule_match'

    def __init__(self, spacy, disable, user_pattern,load_partial=False):

        logger.info('Initializing Rule_Match_Component...')
        self.spacy = spacy
        self.patterns = {}
        self.filters = {}
        self.normalizations = {}
        self.matcher = Matcher(spacy.vocab, validate=True)
        self.matches = None
        channels = PatternLoader.load_pattern(disable, user_pattern, load_partial=load_partial)
        self.relation_exception = ['alias_head', 'alias_tail', 'alias_trigger']

        print ('channels: ', channels)
        print ('-------------------------')
        print ('channels.items(): ', channels.items())
        print ('-------------------------')

        features_name = Token.get_extension(ExtensionKeys.features.name)
        if features_name is None:
            Token.set_extension(ExtensionKeys.features.name, default=False)

        for channel, file_type in channels.items():

            # print ('channel: ', channel)
            # print ('************************')
            # print ('file_type: ', file_type)
            # print ('************************')

            pattern_files = file_type[0]
            self.patterns[channel] = pattern_files[0]

            # print ('patterns: ', pattern_files[0])
            # print ('************************')
            
            if len(pattern_files) >= 2:
                self.filters[channel] = pattern_files[1]
            else:
                self.filters[channel] = {}
                # print ('filters: ', pattern_files[1])
                # print ('************************')
            
            if len(pattern_files) == 3:
                self.normalizations[channel] = pattern_files[2]
            else:
                self.normalizations[channel] = {}
                # print ('normalizations: ', pattern_files[2])
                # print ('************************')


            # print (len(file_type))
            # print ('************************')

            # print ('type1: ', file_type[1])
            # print ('************************')
            
            if len(file_type) == 2:
           
                for grammar_type in file_type[1]:
                    # print ('grammar_type:', grammar_type)
                    for pattern in self.patterns[channel]:
                        # print ('pattern:', pattern)
                        if grammar_type in pattern:
                            grammar = pattern[grammar_type]
                            print ('Added grammar:', grammar)
                            self.matcher.add(grammar_type, None, *grammar)
        
        # matcher = Matcher(spacy.vocab)
        # pattern = [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}]
        # self.matcher.add("HelloWorld", None, pattern)

        # doc = spacy("Hello, world! Hello world!")
        # matches = matcher(doc)
        # print ('init match:', matches)
        # for match_id, start, end in matches:
        #     string_id = spacy.vocab.strings[match_id]  # Get string representation
        #     span = doc[start:end]  # The matched span
        #     print(match_id, string_id, start, end, span.text)

    def __call__(self, doc):
        # print ('doc:', doc)
        self.matches = self.matcher(doc)
        print ('matches:', self.matches)
        spans = []
        for match_id, start, end in self.matches:
            print ('Have matches')
            # print (match_id, self.nlp.vocab.strings[match_id], start, end, doc[start:end])
            label = self.spacy.vocab.strings[match_id]
            span = Span(doc, start, end, label=label)
            print (label, span)
            spans.append(span)

        print ('Rule Match spans:', spans)
        custom_ne_dict = defaultdict(list)
        custom_ne = []
        if 'custom_ne' in doc.user_data:
            for ne in doc.user_data['custom_ne']:
                custom_ne.append(Span(doc, start=ne[0], end=ne[1], label=ne[2]))

        ml_ne = list(doc.ents)
        if ml_ne:
            ml_ne = self.filter_ml(doc, ml_ne, custom_ne)

        duplicated_entities = set(spans + ml_ne + custom_ne)
        print ('duplicated_entities:', duplicated_entities)
        deduplicated_entities = filter_spans(duplicated_entities)
        print ('deduplicated_entities:', deduplicated_entities)
        deduplicated_entities = self.recover_multi_ne(duplicated_entities, deduplicated_entities)
        print ('recovered_entities:', deduplicated_entities)
        ## TODO: Broken merged tokens. Need fixes
        #deduplicated_entities = self.merge(deduplicated_entities, doc)
        for span in deduplicated_entities:
            # A token can only be part of one entity
            # if not DictionaryFeatureComponent.is_ne(span):
            # doc.ents = list(doc.ents) + [span]
            # custom_ne.append(span)
            # if isinstance(span, list):
            #     ## TODO: Broken merged tokens. Need fixes
            #     continue
            print('deduplicated_entities:', span)
            # if span.label_ in self.relation_exception:
            #     label_class = span.label_.split('_')[0]
            #     text_span = str(span)
            #     custom_ne_dict[label_class].append(text_span)
            #     continue
            try:
                text = span.text
                if text not in custom_ne_dict[span.label_]:
                    custom_ne_dict[span.label_].append(text)
                    for token in span:
                        token._.set(ExtensionKeys.features.name, span.label_)
            except Exception:
                pass

        # merge span to tokens
        # DictionaryFeatureComponent.merge_ne(ne_exclusive_entities, doc)
        doc.user_data['custom_ne'] = custom_ne_dict

        return doc

    def recover_multi_ne(self, duplicated_entities, deduplicated_entities):
        result = deduplicated_entities.copy()
        for deduplicated_ne in deduplicated_entities:
            for duplicated_ne in duplicated_entities:
                if deduplicated_ne.start == duplicated_ne.start and duplicated_ne.label_ != deduplicated_ne.label_:
                    result.append(duplicated_ne)
                elif duplicated_ne.label_ in self.relation_exception:
                    result.append(duplicated_ne)
                    #break
        return result
