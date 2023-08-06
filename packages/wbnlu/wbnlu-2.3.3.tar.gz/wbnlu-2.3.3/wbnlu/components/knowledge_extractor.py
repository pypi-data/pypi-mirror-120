import csv
from wbnlu import logger
from ..utils.text_normalizer import normalize, is_ascii
from .dictionary_feature_component import DictionaryFeatureComponent
from .relation_extractor import BaseRelationExtractor, RelationExtraction
from .sentiment_extractor import SentimentExtraction
from .entity_extractor import EntityExtraction
from .wb_tagger_component import WBTaggerComponent
from ..utils.my_utils import read_batch_from_csv
from .constants import FeatureEnum, RelationEnum
import pandas as pd

from .constants import FeatureAcronymEnum
from ..utils.fileio import read_yaml_file
import os

import wbnlu

abspath = os.path.abspath(os.path.dirname(__file__))

SPACY_CONFIG = read_yaml_file(os.path.join(abspath, "../configs/spacy_config.yml"))

logger = logger.my_logger(__name__)

NE_EXCLUSION_TYPES = set([fae.name for fae in FeatureAcronymEnum])

NEGATION_FILTER_WORDS = ['不含', "未含"]

class KnowledgeExtractor(BaseRelationExtractor):
    name = "knowledge_extractor"

    def __init__(self, nlp, data_source, disable):
        logger.info('Initializaing knowledge extractor ...')
        BaseRelationExtractor.__init__(self, disable)
        self.nlp = nlp
        self.dictionary_intialized = False
        self.wb_tag_intialized = False
        self.entity_initialized = False
        self.relation_initialized = False
        self.sentiment_initialized = False
        self.init_knowledge_extractor(data_source, disable)
        logger.info("KnowledgeExtractor initialized ...")

    def __call__(self, doc):
        # do nothing further here. Tasks are dispatched
        return doc

    def init_knowledge_extractor(self, data_source, disable):
        if 'dictionary' not in disable and not self.dictionary_intialized:
            self.init_dictionary_extractor(data_source, disable, SPACY_CONFIG['char_match'], SPACY_CONFIG['word_tok'])
            self.dictionary_intialized = True
        else:
            SPACY_CONFIG['word_tok'] = True
        # elif ('entity' not in disable or 'relation' not in disable) and not self.dictionary_intialized:
        #     raise ValueError(
        #         'Entity Recognizer and Relation Extractor depend on Dictionary recognizer. Please DO NOT disable dictionary when using entity or relation!')

        if 'wb_tag' not in disable and not self.wb_tag_intialized:
            self.init_wbtag_extractor(SPACY_CONFIG['tag_as_label'], SPACY_CONFIG['char_match'],
                                           SPACY_CONFIG['word_tok'])
            self.wb_tag_intialized = True
        else:
            SPACY_CONFIG['word_tok'] = True

        if 'entity' not in disable and not self.entity_initialized:
            self.init_entity_extractor(SPACY_CONFIG['word_tok'])
            self.entity_initialized = True

        if 'relation' not in disable and not self.relation_initialized:
            self.init_relation_extractor()
            self.relation_initialized = True

        if 'sentiment' not in disable and not self.sentiment_initialized:
            self.init_sentiment_extractor()
            self.sentiment_initialized = True


    def init_dictionary_extractor(self, data_source, disable, char_match, word_tok):
        logger.info("Initializaing dictionary extractor ...")
        if char_match:
            self.nlp.turn_use_jieba(False)
        else:
            self.nlp.turn_use_jieba(True)
        generic_dict_component = DictionaryFeatureComponent(self.nlp, data_source, disable, char_match, word_tok)
        if 'dictionary' not in self.nlp.pipe_names:
            self.nlp.add_pipe(generic_dict_component)

        # if 'timex' not in disable:
        #     timex_dict_component = TimexDictionaryComponent(self.nlp, data_source, char_match, word_tok)
        #     self.nlp.add_pipe(timex_dict_component)

        if word_tok:
            self.nlp.turn_use_jieba(True)
        # self.nlp.add_pipe(remove_unserializable_results, last=True)

    def init_wbtag_extractor(self, tag_as_label, char_match, word_tok):
        logger.info("Initializaing wb tag extractor ...")
        if char_match:
            self.nlp.turn_use_jieba(False)
        else:
            self.nlp.turn_use_jieba(True)
        wb_tag_component = WBTaggerComponent(self.nlp, tag_as_label, char_match, word_tok)
        self.nlp.add_pipe(wb_tag_component)
        if word_tok:
            self.nlp.turn_use_jieba(True)

    def init_entity_extractor(self, word_tok):
        logger.info("Initializaing entity extractor ...")
        if word_tok:
            self.nlp.turn_use_jieba(True)
        else:
            self.nlp.turn_use_jieba(False)
        entity_companent = EntityExtraction(self.nlp, self.domain_patterns)

        self.entity_filters = entity_companent.filters
        self.normalizations = entity_companent.normalizations
        if 'entity' not in self.nlp.pipe_names:
            self.nlp.add_pipe(entity_companent)

    def init_relation_extractor(self):
        logger.info("Initializaing relation extractor ...")
        relation_component = RelationExtraction(self.nlp, self.domain_patterns)
        self.relation_filters = relation_component.alias_filters
        self.triggers = relation_component.alias_triggers
        if 'relation' not in self.nlp.pipe_names:
            self.nlp.add_pipe(relation_component)

    def init_sentiment_extractor(self):
        logger.info("Initializaing sentiment extractor ...")
        sentiment_component = SentimentExtraction(self.nlp, self.domain_patterns)
        # self.sentiment_filters = sentiment_component.alias_filters
        # self.triggers = sentiment_component.alias_triggers
        if 'sentiment' not in self.nlp.pipe_names:
            self.nlp.add_pipe(sentiment_component)

    def _batch_nlp_process(self, textlines):
        log_every_n = 10000
        i = 1
        for doc in self.nlp.pipe(textlines, n_process=-1):
            if (i % log_every_n) == 0:
                logger.info('Doc: {}'.format(str(i)))
            i += 1
            yield doc

    def _has_filter_words(self, doc):
        word_set = set([token.text for token in doc])
        for negation_word in NEGATION_FILTER_WORDS:
            if negation_word in word_set:
                return True
        return False

    def extract_entity(self, text):
        return self._entities_from_doc(self.nlp(text))

    def _entities_from_doc(self, doc):
        entity_dict = {}
        if 'custom_ne' in doc.user_data:
            custom_ne = doc.user_data['custom_ne']
            if self._has_filter_words(doc):
                return entity_dict
            for label, tok_text in custom_ne.items():
                if len(tok_text) == 1:
                    continue
                if hasattr(self, 'entity_filters') and 'PARTIAL' in self.entity_filters:
                    partial_filters = self.entity_filters['PARTIAL']
                    if label == FeatureEnum.ingredient.name or label == FeatureEnum.effect.name:
                        if tok_text in partial_filters:
                            continue
                if not tok_text:
                    continue
                if tok_text in self.ambiguous_ne:
                    continue
                if hasattr(self, 'entity_filters') and 'FULL' in self.entity_filters:
                    full_filters = self.entity_filters['FULL']
                    if label == FeatureEnum.ingredient.name or label == FeatureEnum.effect.name:
                        if tok_text in full_filters:
                            continue
                word = KnowledgeExtractor._normalize(tok_text, self.normalizations)
                if not tok_text: continue
                if label in entity_dict:
                    entity_dict[label].append(word)
                else:
                    entity_dict[label] = [word]

            return self.merge_dicts(entity_dict, doc.user_data['char_doc_ne'])

        # return entity_dict

    @staticmethod
    def merge_dicts(dict1, dict2):
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

        # Given '深圳' and '深圳市', remove '深圳'
        # for key, value in dict1.items():
        #     value.sort(key=len)
        #     new_value = value[:]
        #     length = len(value)
        #     for i, v in enumerate(value[:length - 1]):
        #         for v2 in value[i + 1:]:
        #             if v in v2:
        #                 new_value.remove(v)
        #                 break
        #     dict1[key] = new_value
        return dict1

    def extract_entities_csv(self, inputfile, outputfile, batch_size, delimiter, text_field):
        with open(inputfile, 'r', encoding='utf8') as f1, open(
                outputfile, 'w', newline='', encoding='utf8') as f2:
            csv_reader = csv.DictReader(f1, delimiter=delimiter, quoting=csv.QUOTE_NONE)
            headers = csv_reader.fieldnames
            headers.append('ne')

            if text_field not in headers:
                raise ValueError('Invalid csv file format. It must contain the column {}'.format(text_field))

            csv_writer = csv.DictWriter(f2, fieldnames=headers, delimiter=delimiter)
            csv_writer.writeheader()
            for i, batch in enumerate(read_batch_from_csv(f1, batch_size, delimiter, csv_reader, text_field)):
                logger.info("Batch {}".format(str(i)))
                docs = self._batch_nlp_process(batch[0])
                csv_rows = batch[1]
                for i, doc in enumerate(docs):
                    entity_dict = self._entities_from_doc(doc)
                    #NlpUtils.extract_nlp(custom_object, doc, disable, stopwords, self.knowledge_extractor, self.freq)
                    csv_row = csv_rows[i]
                    if not entity_dict:
                        entity_dict = ''
                    csv_row['ne'] = entity_dict
                    # csv_row.move_to_end('ne', last=False)
                    csv_writer.writerow(csv_row)

    @staticmethod
    def _remove_sub_string(element_set):
        string_list = list(element_set)
        string_list.sort(key=len, reverse=True)
        result = []
        for s in string_list:
            if not any([s in o for o in result]):
                result.append(s)
        return result

    @staticmethod
    def _normalize(text, normalizations):
        for key, values in normalizations.items():
            for v in values:
                if v == text:
                    return key
        return text

    def extract_relations(self, text):
        doc = self.nlp(text)
        return self._relations_from_doc(doc)

    def _relations_from_doc(self, doc):
        relations = []
        head, tail = None, None
        for ent in doc.user_data['relation']:
            label = ent.label_
            text = ent.text

            if len(text) == 1 or text in self.relation_filters:
                continue

            if label == FeatureEnum.alias_head.name:
                head = text
            elif label == FeatureEnum.alias_tail.name:
                tail = text

            if head and tail and head != tail:
                if is_ascii(head) and is_ascii(tail):
                    continue
                tail_rank = wbnlu.freq(tail)[1]
                head_rank = wbnlu.freq(head)[1]
                if (tail_rank < 4000 and tail_rank > 0) or (head_rank < 4000 and head_rank > 0) or (
                        head in self.triggers or tail in self.triggers):
                    continue
                relations.append((head, RelationEnum.alias.name, tail))
                head, tail = None, None

        return relations

    def extract_relations_csv(self, inputfile, outputfile, batch_size, delimiter, text_field):
        with open(os.path.join(abspath, inputfile), 'r', encoding='utf8') as f1, open(
                os.path.join(abspath, outputfile), 'w', newline='', encoding='utf8') as f2:
            csv_reader = csv.DictReader(f1, delimiter=delimiter, quoting=csv.QUOTE_NONE)
            headers = csv_reader.fieldnames
            headers.append('relation')

            csv_writer = csv.DictWriter(f2, fieldnames=headers)
            csv_writer.writeheader()
            for i, batch in enumerate(read_batch_from_csv(f1, batch_size, delimiter, csv_reader, text_field)):
                logger.info("Batch {}".format(str(i)))
                docs = self._batch_nlp_process(batch[0])
                csv_rows = batch[1]
                for i, doc in enumerate(docs):
                    relation_list = self._relations_from_doc(doc)
                    csv_row = csv_rows[i]
                    if not relation_list:
                        relation_list = ''
                    csv_row['relation'] = relation_list
                    csv_row.move_to_end('relation', last=False)
                    csv_writer.writerow(csv_row)

    def extract_relations_custom(self, inputfile, outputfile):

        textlines = []
        with open(os.path.join(abspath, inputfile), 'r', encoding='utf8') as f:
            for line in f:
                if line:
                    line = normalize(line)
                    textlines.append(line)

        all_alias = []
        docs = self._batch_nlp_process(textlines)
        log_every_n = 1000
        for i, doc in enumerate(docs):
            # print(i)
            if (i % log_every_n) == 0:
                logger.info("Line: {}".format(str(i)))

            relation_list = self._relations_from_doc(doc)
            for relation in relation_list:
                all_alias.append((relation[0], relation[2], doc.text))

        output_dict = {}
        alias_length = len(all_alias)
        output_dict[FeatureEnum.alias_head.name] = [None] * alias_length
        output_dict[FeatureEnum.alias_tail.name] = [None] * alias_length
        output_dict['kg_head'] = [None] * alias_length
        output_dict['kg_tail'] = [None] * alias_length
        output_dict['text'] = [None] * alias_length

        logger.info("Computing similarities ...")
        for i, alias in enumerate(all_alias):
            head = alias[0]
            tail = alias[1]
            output_dict[FeatureEnum.alias_head.name][i] = head
            kg_head = KnowledgeExtractor._found_kg_item(wbnlu.kg_similarity(head, similarity_threhold=0.2))
            output_dict['kg_head'][i] = kg_head
            kg_tail = KnowledgeExtractor._found_kg_item(wbnlu.kg_similarity(tail, similarity_threhold=0.2))
            output_dict['kg_tail'][i] = kg_tail
            output_dict[FeatureEnum.alias_tail.name][i] = tail
            output_dict['text'][i] = alias[2]

        # print("All tags:{} effect:{} ingredients: {}".format(str(all_tags), str(effect_count), str(ingredient_count)))
        print("Percentage: alias:{:.3f} ".format(len(all_alias) / len(textlines))),
        #                                                              ingredient_count / all_tags))
        print("All: {}  Extracted: {}".format(str(len(textlines)), str(len(all_alias))))

        headers = ['alias_head', 'kg_head', 'alias_tail', 'kg_tail', 'text']
        df = pd.concat([pd.Series(output_dict[k], name=k) for k in headers], 1)
        df.to_csv(os.path.join(abspath, outputfile), sep='\t', index=False)

    @staticmethod
    def _found_kg_item(similarity_dict):
        for item, score in similarity_dict.items():
            if score >= 0.95:
                return {item, score}
        return similarity_dict
