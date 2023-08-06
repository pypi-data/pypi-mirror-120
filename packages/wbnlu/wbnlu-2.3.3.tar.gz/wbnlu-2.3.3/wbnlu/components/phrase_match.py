import os
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span, Token, Doc
from collections import OrderedDict
from collections import defaultdict
from wbnlu import logger
from spacy.util import filter_entities
from .data_statistics import Statistics
from ..constants import SENTIMENT_KEYS, FeatureAcronymEnum, ExtensionKeys, NEGATION_WORDS, FEATURE_HIERARCHY


abspath = os.path.abspath(os.path.dirname(__file__))
logger = logger.my_logger(__name__)

PRIMITIVE_FEATURES = set([fae.name for fae in FeatureAcronymEnum])


class PhraseMatchComponent(object):

    name = 'phrase_match'

    def __init__(self, spacy, disable, data_source, user_dict, char_match=True, word_tok=True):

        self.spacy = spacy
        self.matcher = PhraseMatcher(self.spacy.vocab, attr='LOWER')
        self.data_source=data_source
        self.char_match = char_match
        self.word_tok = word_tok
        self.feature_hierarchy = {}
        self.init_feature_hierarchy()
        self.prev_data_source = None
        self.statistics = Statistics()
        self.tag_as_label = False

        features_name = Token.get_extension(ExtensionKeys.features.name)
        if features_name is None:
            Token.set_extension(ExtensionKeys.features.name, default=False)
        # Load generic feature table
        attribute_word_dict = OrderedDict()

        


        if 'phrase_match' not in disable or data_source==['generic']:
            entity_feature_files = []
            entity_feature_files.append(os.path.join(abspath, '../resources/features/entity/others.txt'))
            entity_feature_files.append(os.path.join(abspath, '../resources/features/entity/time.txt'))
            entity_feature_files.append(os.path.join(abspath, '../resources/features/entity/beauty.txt'))
            entity_feature_files.append(os.path.join(abspath, '../resources/features/entity/beauty.effect.txt'))
            entity_feature_files.append(os.path.join(abspath, '../resources/features/entity/beauty.ingredient.txt'))
            entity_feature_files.append(os.path.join(abspath, '../resources/features/entity/beauty.atom.txt'))
            entity_feature_files.append(os.path.join(abspath, '../resources/features/entity/sports.txt'))
            entity_feature_files.append(os.path.join(abspath, '../resources/features/entity/game.txt'))
            # entity_feature_files.append(os.path.join(abspath, '../resources/features/generic/features.txt'))
            # entity_feature_files.append(os.path.join(abspath, '../resources/features/generic/tag_context_words.txt'))
            # entity_feature_files.append(os.path.join(abspath, '../resources/features/generic/tag_pattern.txt'))
            
            #entity_feature_files.append(os.path.join(abspath, '../resources/features/segmentation/beauty.prod.txt'))
            #entity_feature_files.append(os.path.join(abspath, '../resources/features/entity/baike.per.seg.txt'))

            PhraseMatchComponent.merge_dict(attribute_word_dict, self._load_text_dict(entity_feature_files))

        if 'sentiment' not in disable:
            sentiment_feature_files = []
            sentiment_feature_files.append(os.path.join(abspath, '../resources/features/sentiment/features.txt'))
            PhraseMatchComponent.merge_dict(attribute_word_dict, self._load_text_dict(sentiment_feature_files))

        if 'timex' not in disable:
            timex_feature_files = []
            # for ds in self.data_source:
            for ds in ['generic']:
                timex_feature_files.append(os.path.join(abspath, '../resources/features/timex/' + ds + '.txt'))
            timex_feature_files.append(os.path.join(abspath, '../resources/features/timex/generic.txt'))
            PhraseMatchComponent.merge_dict(attribute_word_dict, self._load_text_dict(timex_feature_files))
            #PhraseMatchComponent.merge_dict(attribute_word_dict, TIMEX_DICT['通用'])

        if 'wbtag' in data_source:
            logger.info('Loading tag pattern data ...')
            self.kb_pattern_dict, pattern_feature_dict = self._load_kb_pattern(os.path.join(abspath, '../resources/features/wbtag/tag_pattern.txt'))
            logger.info("Loading wbtag features ...")
            wbtag_feature_files = [os.path.join(abspath, '../resources/features/wbtag/features.txt')]
            PhraseMatchComponent.merge_dict(attribute_word_dict, self._load_text_dict(wbtag_feature_files))




        if user_dict != []:
            user_feature_files = []
            for file in user_dict:
                user_feature_files.append(file)

            self.user_dictionary = self._load_text_dict(user_feature_files)
            PhraseMatchComponent.merge_dict(attribute_word_dict, self.user_dictionary)

        self.spacy.vocab.strings.add(ExtensionKeys.features.name)
        for label in attribute_word_dict.keys():
            self.spacy.vocab.strings.add(label)

        self.id_label_dict = {}
        for label in attribute_word_dict.keys():
            self.id_label_dict[self.spacy.vocab.strings[label]] = label



        if self.char_match:
            self.spacy.turn_use_jieba(False)
        else :
            self.spacy.turn_use_jieba(True)
        logger.info('Compiling dict patterns ...')
        n = 0
        for label, terms in attribute_word_dict.items():
            n += len(terms)

            # docs = []
            # for term in terms:
            #     docs.append(self.spacy.make_doc(term, merge_ascii=False))

            self.matcher.add(label, [self.spacy.make_doc(term, merge_ascii=False) for term in terms])

        # print ('idk:', attribute_word_dict.items())

        # test = self.spacy('果酸')
        # matches = self.matcher(test)
        # print ('------Test------:', matches)

        if self.word_tok:
            self.spacy.turn_use_jieba(True)

        self.prev_data_source = data_source



        logger.info("PhraseMatch component initialization done!")


    def __call__(self, doc):

        # print ('Doc:', doc.to_json())

        char_doc = None

        # When ascii_char_merge_as_token changes the original length of doc, the indexes caculated by re_caculate_indexes() below may be wrong.
        # So only when the merge function doesn't change the original length of the doc, the re_caculate_indexes will be used.
        chardoc_len_equal_worddoc_len = True

        if 'word_doc' in doc.user_data and doc.user_data['word_doc']:
            char_doc = self.create_char_doc(doc)

        if char_doc and PhraseMatchComponent.doc_length(doc) != PhraseMatchComponent.doc_length(char_doc):
            chardoc_len_equal_worddoc_len = False
        # print ('Chardoc:', char_doc.to_json())
        # Use segmentation for dictionary initialization
        if not self.char_match:
            matches = self.matcher(doc)
        # Use segmentation, but char dictionary initialization
        elif char_doc:
            matches = self.matcher(char_doc)
        # No segmentation at all!
        else:
            char_doc = doc
            matches = self.matcher(char_doc)

        # print ('Pre-match:', matches)

        matches = PhraseMatchComponent.remove_sub_patterns(matches)
        # 对 抗 虫 咬
        # 对抗 虫咬
        char_doc_ne = defaultdict(list)
        matched_phrases = OrderedDict()
        no_further_matches = set()
        # newly tagged NE
        new_entities = []
        char_doc_other = defaultdict(list)
        tag_confidence = {}
        for match_id, start, end in matches:
            matched_phrases[char_doc[start:end].text] = (start, end)
        for match_id, start, end in matches:
            # remove disambibuation
            #s = char_doc[start:end].text
            if PhraseMatchComponent.ambiguous(start, end, doc):
                continue

            label = self.id_label_dict[match_id]


            start_copy = start
            end_copy = end
            current_match = (start_copy, end_copy)
            if current_match in no_further_matches and 'wbtag' in self.data_source:
                continue

            if self.char_match and self.word_tok:
                start, end = PhraseMatchComponent.re_caculate_indexes(start, end, doc)

            #if start != -1 and end != -1 and chardoc_len_equal_worddoc_len:
            span = char_doc[start_copy:end_copy]
            if start != -1 and end != -1 and chardoc_len_equal_worddoc_len:
                if ':' in label:
                    matched_label_tags = self.match_kb_pattern(label, doc.text, current_match, matched_phrases, no_further_matches)
                    # if matched_label_tags:
                    #    no_further_matches.add((start_copy, end_copy))
                    for matched_label_tag in matched_label_tags:
                        # print ('matched_label_tag:',matched_label_tag)
                        matched_label = matched_label_tag[0]
                        tag = matched_label_tag[1]
                        confidence = matched_label_tag[2]
                        if self.tag_as_label:
                            span = Span(doc, start, end, label=tag)
                        else:
                            span = Span(doc, start, end, label=matched_label)
                        new_entities.append(span)
                        tag_confidence[tag] = confidence
                else:

                    new_entities.append(Span(doc, start, end, label=self.spacy.vocab.strings[match_id]))
            elif label not in PRIMITIVE_FEATURES and not PhraseMatchComponent.is_atToken(span):
                if ':' in label:
                    continue
                char_doc_ne[label].append(span.text)
            elif not PhraseMatchComponent.is_atToken(span):
                char_doc_other[label].append(char_doc[start_copy:end_copy].text)


        # print ('span:', span)
        # filter atToken
        new_entities = PhraseMatchComponent.filter_atToken(new_entities)

        ne_exclusive_entities, m_entities_span = filter_entities(new_entities, PRIMITIVE_FEATURES)

        custom_ne = []
        sentiments = []
        deduplicated_entities = set(ne_exclusive_entities + m_entities_span)
        match_info = []
        # for span in ne_exclusive_entities + m_entities_span:
        for span in deduplicated_entities:
            # A token can only be part of one entity
            # if span.label_ not in PRIMITIVE_FEATURES and not PhraseMatchComponent.is_ne(span):
            label = span.label_
            if label not in PRIMITIVE_FEATURES:
                # doc.ents = list(doc.ents) + [span]
                if label in self.feature_hierarchy:
                    span = Span(doc, start=span.start, end=span.end, label=self.feature_hierarchy[label])
                custom_ne.append((span.start, span.end, span.label_))
                match_info.append(span)
            for token in span:
                if token.text in NEGATION_WORDS:
                    break
                token._.set(ExtensionKeys.features.name, label)
            #if span.label_ in SENTIMENT_KEYS and span not in sentiments:
            if span.label_ in SENTIMENT_KEYS:
                sentiments.append((span.start, span.end, span.label_))

        # merge span to tokens
        # PhraseMatchComponent.merge_ne(ne_exclusive_entities, doc)
        # PhraseMatchComponent.merge_ne(custom_ne, doc)
        doc.user_data['char_doc_ne'] = char_doc_ne
        # print ('Phrase_Match char_doc_ne:', doc.user_data['char_doc_ne'])
        doc.user_data['char_doc_other'] = char_doc_other
        # custom_ne_dict = defaultdict(list)
        # for span in custom_ne:
        #     custom_ne_dict[span.label_].append(span.text)
        doc.user_data['custom_ne'] = custom_ne
        doc.user_data['match_info'] = match_info
        # print ('Phrase_Match custom_ne:', doc.user_data['custom_ne'])
        doc.user_data['sentiment'] = sentiments
        return doc




    def init_feature_hierarchy(self):
        for parent_feature, child_features in FEATURE_HIERARCHY.items():
            for child_feature in child_features:
                self.feature_hierarchy[child_feature] = parent_feature


    def create_char_doc(self, doc):
        words = []
        spaces = []
        for char in list(doc.text):
            if char == ' ':
                spaces.append(True)
            else:
                spaces.append(False)
            words.append(char)

        return Doc(self.spacy.vocab, words=words, spaces=spaces)

    @staticmethod
    def ambiguous(start, end, doc):
        #doc_len = len(doc)
        for i, token in enumerate(doc):
            offset_start = token.idx
            offset_end = offset_start + len(token)
            # if offset_start <=start and offset_end==start:
            #     if i<doc_len-1:
            #         next_token = doc[i+1]
            #         next_offset_start = next_token.idx
            #         next_offset_end = next_offset_start + len(next_token)
            #         if next_offset_start+1 == end and next_offset_end != end:
            #             return True

            if offset_start <= start and offset_end > end:
                return True
            elif offset_end >= end and offset_start < start:
                return True
            elif offset_start < end and offset_end >end:
                return True
            elif offset_start < start and start<offset_end:
                return True

            if offset_end >end:
                return False

        return False

    @staticmethod
    def filter_atToken(spans):
        filtered_tokens = []
        for span in spans:
            is_atToken = False
            for token in span:
                if token._.atToken:
                    is_atToken = True
                    break
            if not is_atToken:
                filtered_tokens.append(span)
        return filtered_tokens

    @staticmethod
    def is_atToken(span):
        for token in span:
            if token._.atToken:
                return True
        return False

    @staticmethod
    def doc_length(doc):
        doc_len = 0
        for token in doc:
            doc_len += len(token.text)
        return doc_len

    @staticmethod
    def remove_sub_patterns(matches):
        new_matches = []
        for m in matches:
            add = True
            for o in matches:
                if not (m[1] == o[1] and m[2] == o[2]):
                    r = range(o[1], o[2] + 1)
                    if m[1] in r and m[2] in r:
                        add = False
            if add:
                new_matches.append(m)
        return new_matches

    @staticmethod
    def re_caculate_indexes(start, end, doc):
        new_start = -1
        new_end = -1

        span_length = end - start
        for token in doc:
            idx = token.idx
            index = token.i
            token_text = token.text
            token_length = len(token_text)
            if new_start != -1 and idx + token_length == end:
                new_end = index + 1
                return (new_start, new_end)
            # elif idx > start:
            #     return (-1, -1)
            elif idx == start:
                new_start = index
                if span_length == len(token):
                    return (new_start, new_start + 1)
                elif span_length < token_length:
                    # didn't find matches with tokens
                    return (-1, -1)
                continue
            if new_start != -1:
                if idx == end:
                    new_end = idx
                    break

        return (new_start, new_end)

    @staticmethod
    def is_ne(span):
        if span.ents is not None and not span.ents:
            return False
        return True

    @staticmethod
    def merge_ne(spans, doc):
        with doc.retokenize() as retokenizer:
            for span in spans:
                retokenizer.merge(span)

    def _load_text_dict(self, feature_files):
        attribute_dict = OrderedDict()
        for feature_file in feature_files:
            logger.info("Loading features from: {}.".format(feature_file))
            with open(feature_file, newline='', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    word_attribute = line.split('\t')
                    if len(word_attribute) != 2:
                        raise ValueError('Invalid line: {} from file {}'.format(line, feature_file))
                    word = word_attribute[0].strip()
                    attributes = word_attribute[1].split(',')
                    for attribute in attributes:
                        if attribute in attribute_dict:
                            attribute_dict[attribute].append(word)
                        else:
                            attribute_dict[attribute] = [word]

                logger.info('Done with loading feature dictionary ...')

        return attribute_dict

    @staticmethod
    def merge_dict(original_dict, to_merge_dict):
        for key in to_merge_dict:
            if key not in original_dict:
                original_dict[key] = to_merge_dict[key]
            else:
                original_dict[key] += to_merge_dict[key]

    @staticmethod
    def parse_tag_type(tag_and_type):
        # 1042015:festival_02eb5a8abb6051caff8ad39c2e73b1d9|吃信节
        first_pos = tag_and_type.find(':')
        second_pos = tag_and_type.find('_')

        return tag_and_type[first_pos + 1:second_pos]

    def match_kb_pattern(self, entity_tag, tokens, current_match, matched_phrases, no_further_matches):
        labels = entity_tag.split('##')
        matched = set()
        for label in labels:
            split_label = label.split('|')
            tag = split_label[0]
            # tag_name = split_label[1]
            if label in self.kb_pattern_dict:
                patterns = self.kb_pattern_dict[label]
                tag_type = patterns[0]
                tag_patterns = patterns[1]
                for tag_pattern in tag_patterns:
                    pattern_words = tag_pattern.split("^")
                    if PhraseMatchComponent.match_kb_pattern_helper(tokens, pattern_words, current_match, matched_phrases, no_further_matches):
                        confidence = self.getPatternConfidence(pattern_words)
                        matched.add((tag_type, tag, confidence))
                        #no_further_matches.update(set(matched_phrases.values()))
        return matched


    def getPatternConfidence(self, pattern_words):
        pattern_len = len(pattern_words)
        if pattern_len > 1:
            return 5

        freq = self.statistics.freq(pattern_words[0])
        if -1<freq[1] < 1000:
            return 1

        return 5


    @staticmethod
    def match_kb_pattern_helper(tokens, pattern_words, current_match, matched_phrases, no_further_matches):

        first_start = -1
        first_end = -1
        second_start = -1
        second_end = -1
        for i, word in enumerate(pattern_words):
            if word not in matched_phrases:
                return False
            else:
                if first_start == -1:
                    first_start, first_end = matched_phrases[word]
                    if (first_start, first_end) != current_match:
                        no_further_matches.add((first_start, first_end))
                else:
                    second_start, second_end = matched_phrases[word]
                    if (second_start, second_end) != current_match:
                        no_further_matches.add((second_start, second_end))

                if second_start != -1:
                    if first_start > second_start:
                        distance = abs(first_start - second_end)
                    else:
                        distance = abs(first_end - second_start)
                    if distance > 30:
                        return False
        return True



    def _load_kb_pattern(self, tag_pattern_file):
        tag_patterns = {}

        # festival_02eb5a8abb6051caff8ad39c2e73b1d9|吃信节 吃信节
        # 1042015: festival_0351e39ead257524bd712e6af988dcd4|纳西族朝山会 朝山会^纳西族|纳西族朝山会
        attribute_dict = OrderedDict()
        with open(tag_pattern_file, encoding='utf-8') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                line = line.strip()
                tag_pattern = line.split('\t')
                if len(tag_pattern) != 2:
                    raise ValueError('Invalid line: ', line)
                tag_tag_name = tag_pattern[0].strip()
                patterns = tag_pattern[1].strip().split('|')
                tag_type = PhraseMatchComponent.parse_tag_type(tag_tag_name)
                tag_patterns[tag_tag_name] = (tag_type, patterns)

                for pattern in patterns:
                    pattern_words = pattern.split('^')
                    if tag_tag_name in attribute_dict:
                        attribute_dict[tag_tag_name].extend(pattern_words)
                    else:
                        attribute_dict[tag_tag_name] = pattern_words

        logger.info('Done with loading tag pattern dictionary ...')
        return (tag_patterns, attribute_dict)
