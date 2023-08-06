import os
from collections import defaultdict
# from ..constants import FeatureEnum
# from .knowledge_extractor import KnowledgeExtractor


# abspath = os.path.abspath(os.path.dirname(__file__))
# NEGATION_FILTER_WORDS = ['不含', "未含"]

class Dictionary(object):

    def __init__(self, doc, custom_object):
        # print ('Extracting entity...')
        self.doc = doc
        self.custom_object = custom_object
        # self.knowledge_extractor = knowledge_extractor
        # self.ambiguous_ne = self._load_ambiguous_ne()

    def __call__(self):
        entities = self.entities(self.doc)
        # print ('UDP Entities:', entities)
        if entities:
            # TODO: this merge function needs to be improved when actual data shows up!
            if 'entities' in self.custom_object:
                self.custom_object['udp'].extend(entities)
            else:
                self.custom_object['udp'] = entities

    
    def entities(self, doc):
        udp_list = {}
        if 'match_info' in doc.user_data:
            custom_ne = doc.user_data['match_info']
            # print (custom_ne)
            for span in custom_ne:
                # if isinstance(tok_text_list, str):
                #     # print ('UDP is str:', tok_text_list)
                #     if label in udp_list:
                #         udp_list[label].append(tok_text_list)
                #     else:
                #         udp_list[label] = [tok_text_list]
                # elif isinstance(tok_text_list, list):
                #     # print ('UDP is dict:', tok_text_list)
                #     for tok_text in tok_text_list:
                        
                #         word = tok_text
                        

                #         if not tok_text: continue
                #         if label in udp_list:
                #             udp_list[label].append(word)
                #         else:
                #             udp_list[label] = [word]
                if span.label_ in udp_list:
                    udp_list[span.label_].append(span.text)
                else:
                    udp_list[span.label_] = [span.text]
        char_doc_ne_dict={}
        if 'char_doc_ne' in doc.user_data:
            char_doc_ne_dict = doc.user_data['char_doc_ne']
        # print ('entity dict:', entity_dict)
        return self.merge_dicts(udp_list, char_doc_ne_dict)


    def merge_dicts(self, dict1, dict2):
        """
        @param dict1: its value must be a list
        @param dict2: its value must be a list
        """
        for k1, v1 in dict1.items():
            if k1 in dict2:
                dict1[k1].extend(dict2[k1])
                del dict2[k1]
        for k2, v2 in dict2.items():
            dict1[k2] = v2

        return dict1


