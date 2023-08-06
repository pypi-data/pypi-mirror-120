import os
import enum
from ..utils.fileio import read_yaml_file
from spacy.lang.zh.stop_words import STOP_WORDS
from wbnlu import logger
abspath = os.path.abspath(os.path.dirname(__file__))
from ..extractors.constants import FeatureEnum, RelationEnum
from .text_normalizer import is_ascii, is_emoji
from collections import defaultdict
from .phrase import Phrase
from .content_words import Content_Words
from .entity import Entity
from .parser import Parser
from .relation import Relation
from .stop_words import Stop_Words
from .tagger import Tagger
from .wb_tag import Wb_Tag
import wbjieba.analyse as tfidf_extractor


logger = logger.my_logger(__name__)

OTHER_CONFIG = read_yaml_file(os.path.join(abspath, "../configs/other_config.yml"))
TEXT_LENTH_LIMIT = OTHER_CONFIG['MAX_TEXT_LENGTH']
REMOVE_UNIGRAMS = OTHER_CONFIG['REMOVE_UNIGRAMS']
NOTMALIZE_TEXT = OTHER_CONFIG['NOTMALIZE_TEXT']

SPACY_CONFIG = read_yaml_file(os.path.join(abspath, "../configs/spacy_config.yml"))


TAG_FOR_CONTENT_WORDS = {'NN', 'NR', 'VA', 'VC', 'VV', 'FW', 'JJ'}

class NlpToolEnum(enum.Enum):
    #sentencizer = 1
    #np_chunker = 4
    segmenter = 1
    seg_corrector = 2
    tagger = 3
    ner = 4
    stopwords = 5
    text_normalizer = 6
    parser = 7
    dictionary = 8
    entity = 9
    relation = 10
    content_words = 11
    phrase = 12
    wb_tag = 13
    wordpiece = 14
    phrase_match = 15
    rule_match = 16

    @staticmethod
    def as_list():
        return set([e.name for e in NlpToolEnum])

class NlpUtils(object):

    @staticmethod
    def segment(doc, disable, remove_meme, remove_url):
        #tokens = []
        tokens = {}
        tokens['words'] = [token.text for token in doc if token.text]
        # tokens['words'] = [word for token in tokens['words'] for word in token.split(' ')]
        if 'stopwords' not in disable:
            # tokens['stopped_words'] = [token.text for token in doc if token.text and token.text not in STOP_WORDS]
            stop_words = Stop_Words(doc, tokens, True, remove_meme, remove_url)
            tokens = stop_words()
            if 'tagger' not in disable:
                tagger = Tagger(doc, tokens, True)
                tokens = tagger()
                if 'parser' not in disable:
                    # NlpUtils.get_deps(doc, tokens, stopwords=True)
                    parser = Parser(doc, tokens, True)
                    parser()
        else:
            if 'tagger' not in disable:
                tagger = Tagger(doc, tokens, False)
                tokens = tagger()
                if 'parser' not in disable:
                    parser = Parser(doc, tokens, False)
                    parser()

        #return NlpUtils.get_content_words(disable, tokens)
        return tokens


    @staticmethod
    def extract_nlp(custom_object, doc, disable, knowledge_extractor, freq, topK, remove_meme, remove_url):
        # 6. Get tokens
        # 6.1 Get chunks first, then get tokens! You can't switch the order unless you don't want to get the phrases
        # phrases = []
        # if 'phrase' not in disable:
        #     phrases, doc = NlpUtils.get_phrases(doc, custom_object)
        # if 'content_words' not in disable:
        #     doc = NlpUtils.nps(doc, custom_object, phrases, freq, topK)
        # # 6.2 Get tokens
        # else:
        #     tokens = NlpUtils.segment(doc, disable)
        #     if 'stopped_words' in tokens.keys():
        #         custom_object['stopped_words'] = tokens.pop('stopped_words')
        #     custom_object['tokens'] = tokens

        if 'phrase' not in disable or 'rule_match' not in disable:
            phrase = Phrase(doc, custom_object)
            phrases, doc = phrase()
        if 'content_words' not in disable:
            content_words = Content_Words(doc, [], False)
            doc = content_words.nps(doc, custom_object, phrases, freq, topK)
        else:
            tokens = NlpUtils.segment(doc, disable, remove_meme, remove_url)
            if 'stopped_words' in tokens.keys():
                custom_object['stopped_words'] = tokens.pop('stopped_words')
            custom_object['tokens'] = tokens

        # if 'dictionary' not in disable or 'entity' not in disable or 'ner' not in disable:
        if 'dictionary' not in disable or 'entity' not in disable or 'ner' not in disable or 'phrase_match' not in disable or 'rule_match' not in disable:
            # 7. Get entities, if any
            # entities = NlpUtils.entities(doc, knowledge_extractor)
            
            #logger.info(doc.text)
            # if entities:
            #     # TODO: this merge function needs to be improved when actual data shows up!
            #     if 'entities' in custom_object:
            #         custom_object['entities'] = {**entities, **custom_object['entities']}
            #     else:
            #         custom_object['entities'] = entities
            entity = Entity(doc, custom_object, knowledge_extractor)
            entity()

        if 'wb_tag' not in disable:
            # 8. Get wb_tags, if any
            # wb_tags = NlpUtils.wbtags(doc, knowledge_extractor)
            # #logger.info(doc.text)
            # if wb_tags:
            #     if 'tag_confidence' in doc.user_data:
            #         NlpUtils.add_confidence(wb_tags, doc.user_data['tag_confidence'])
            #     # TODO: this merge function needs to be improved when actual data shows up!
            #     if 'wb_tag' in custom_object:
            #         custom_object['wb_tags'] = {**wb_tags, **custom_object['wb_tags']}
            #     else:
            #         custom_object['wb_tags'] = wb_tags
            wb_tag = Wb_Tag(doc, custom_object, knowledge_extractor)
            wb_tag()

        if 'relation' not in disable or 'rule_match' not in disable:
            # 9. Get relations, if any
            # relations = NlpUtils.relations(doc, knowledge_extractor, freq)
            # if relations:
            #     if 'relations' in custom_object:
            #         custom_object['relations'] = {**relations, **custom_object['relations']}
            #     else:
            #         custom_object['relations'] = relations
            relation = Relation(doc, custom_object, knowledge_extractor, freq)
            relation()

