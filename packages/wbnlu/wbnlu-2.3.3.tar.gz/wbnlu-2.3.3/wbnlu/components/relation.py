from ..extractors.constants import FeatureEnum, RelationEnum
from .text_normalizer import is_ascii

class Relation(object):

    def __init__(self, doc, custom_object, knowledge_extractor, freq):
        self.doc = doc
        self.custom_object = custom_object
        self.knowledge_extractor = knowledge_extractor
        self.freq = freq

    def __call__(self):
        relations = self.relations(self.doc, self.knowledge_extractor, self.freq)
        # print ('relation: ', relations)
        if relations:
            if 'relations' in self.custom_object:
                self.custom_object['relations'] = {**relations, **self.custom_object['relations']}
            else:
                self.custom_object['relations'] = relations

    
    def relations(self, doc, knowledge_extractor, freq):
        relations = []
        head, tail = None, None
        if 'relation' in doc.user_data:
            for ent in doc.user_data['relation']:
                label = ent.label_
                text = ent.text

                if len(text) == 1 or text in knowledge_extractor.relation_filters:
                    continue

                if label == FeatureEnum.alias_head.name:
                    head = text
                elif label == FeatureEnum.alias_tail.name:
                    tail = text

                # print ('rel1 and rel2: ', head, tail)

                if head and tail and head != tail:
                    if is_ascii(head) and is_ascii(tail):
                        continue
                    tail_rank = freq(tail)[1]
                    head_rank = freq(head)[1]
                    if (tail_rank < 4000 and tail_rank > 0) or (head_rank < 4000 and head_rank > 0) or (
                            head in knowledge_extractor.triggers or tail in knowledge_extractor.triggers):
                        continue
                    relations.append((head, RelationEnum.alias.name, tail))
                    head, tail = None, None

        return relations
