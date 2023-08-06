import os
from collections import defaultdict
from ..constants import FeatureEnum
# from .knowledge_extractor import KnowledgeExtractor


abspath = os.path.abspath(os.path.dirname(__file__))
NEGATION_FILTER_WORDS = ['不含', "未含"]

class Entity(object):

    def __init__(self, doc, custom_object, knowledge_extractor):
        # print ('Extracting entity...')
        self.doc = doc
        self.custom_object = custom_object
        self.knowledge_extractor = knowledge_extractor
        self.ambiguous_ne = self._load_ambiguous_ne()

    def __call__(self):
        entities = self.entities(self.doc)
        print ('udr:', entities)
        if entities:
            # TODO: this merge function needs to be improved when actual data shows up!
            if 'udr' in self.custom_object:
                self.custom_object['udr'] = {**entities, **self.custom_object['udr']}
            else:
                self.custom_object['udr'] = entities

    
    def entities(self, doc):
        entity_dict = {}
        if 'custom_ne' in doc.user_data:
            custom_ne = doc.user_data['custom_ne']
            if self._has_filter_words(doc):
                return entity_dict
            # print ('custom_ne: ', custom_ne)
            for label, tok_text_list in custom_ne.items():
                if isinstance(tok_text_list, str):
                    if label in entity_dict:
                        entity_dict[label].append(tok_text_list)
                    else:
                        entity_dict[label] = [tok_text_list]
                elif isinstance(tok_text_list, list):
                    for tok_text in tok_text_list:
                        # if not tok_text or len(tok_text) == 1:
                        #     continue
                        if hasattr(self.knowledge_extractor, 'filters') and 'PARTIAL' in self.knowledge_extractor.filters:
                            partial_filters = self.knowledge_extractor.filters['PARTIAL']
                            if label == FeatureEnum.ingredient.name or label == FeatureEnum.effect.name:
                                if tok_text in partial_filters:
                                    continue
                        if tok_text in self.ambiguous_ne:
                            continue
                        if hasattr(self.knowledge_extractor, 'filters') and 'FULL' in self.knowledge_extractor.filters:
                            full_filters = self.knowledge_extractor.filters['FULL']
                            if label == FeatureEnum.ingredient.name or label == FeatureEnum.effect.name:
                                if tok_text in full_filters:
                                    continue
                        # print ('loop word:', tok_text)
                        word = tok_text
                        if hasattr(self.knowledge_extractor, 'normalizations'):
                            word = self._normalize(tok_text, self.knowledge_extractor.normalizations)

                        if not tok_text: continue
                        if label in entity_dict:
                            entity_dict[label].append(word)
                        else:
                            entity_dict[label] = [word]
        elif doc.ents:
            ner_dict = defaultdict(list)
            for span in doc.ents:
                ner_dict[span.label_].append(span.text)
            entity_dict = self.merge_dicts(entity_dict, ner_dict)
        char_doc_ne_dict = {}
        if 'char_doc_ne' in doc.user_data:
            char_doc_ne_dict = doc.user_data['char_doc_ne']
        # print ('entity dict:', entity_dict)
        return self.merge_dicts(entity_dict, char_doc_ne_dict)

    
    def merge_dicts(self, dict1, dict2):
        """
        @param dict1: its value must a list
        @param dict2: its value must be a list
        """
        for k1, v1 in dict1.items():
            if k1 in dict2:
                dict1[k1].extend(dict2[k1])
                del dict2[k1]
        for k2, v2 in dict2.items():
            dict1[k2] = v2

        return dict1


    def _normalize(self, text, normalizations):
        for key, values in normalizations.items():
            for v in values:
                if v == text:
                    return key
        return text


    def _has_filter_words(self, doc):
        word_set = set([token.text for token in doc])
        for negation_word in NEGATION_FILTER_WORDS:
            if negation_word in word_set:
                return True
        return False

    
    def _load_ambiguous_ne(self):
        ne = set()

        with open(os.path.join(abspath, '../resources/ambiguous_ne.txt'), 'r', encoding='utf8') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                line = line.strip()
                ne.add(line)
        return ne
