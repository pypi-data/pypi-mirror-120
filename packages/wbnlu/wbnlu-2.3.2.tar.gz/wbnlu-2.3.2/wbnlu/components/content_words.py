from spacy.lang.zh.stop_words import STOP_WORDS
from .text_normalizer import is_emoji

TAG_FOR_CONTENT_WORDS = {'NN', 'NR', 'VA', 'VC', 'VV', 'FW', 'JJ'}

class Content_Words(object):

    def __init__(self, doc, tokens, stop_words):
        self.doc = doc
        self.tokens = tokens
        self.stop_words = stop_words

    def __call__(self):
        tokens = self.tokens
        if self.stop_words:
            tokens['nps'] = [tokens['stopped_words'][i] for i in range (0, len(tokens['stopped_words'])) if tokens['pos'][i] in TAG_FOR_CONTENT_WORDS and not is_emoji(tokens['stopped_words'][i]) and len(tokens['stopped_words'][i])>1]
        else :
            tokens['nps'] = [tokens['words'][i] for i in range (0, len(tokens['words'])) if tokens['pos'][i] in TAG_FOR_CONTENT_WORDS and not is_emoji(tokens['words'][i]) and len(tokens['words'][i])>1]
        return tokens
    
    def nps(self, doc, custom_object, phrases, freq, topK, np_length=2):

        tokens = list(doc)

        nps_set = set(phrases)

        tokens= [token.text for token in tokens if
                 token.tag_ in TAG_FOR_CONTENT_WORDS and not is_emoji(token.text) and len(token.text) > 1 and not token._.bracket]
        tokens = [token for token in tokens if len(token) >= np_length and token not in STOP_WORDS and token not in nps_set]
        nps_set.update(self.sort_by_freq(tokens, freq))
        nps_set = [np for i, np in enumerate(nps_set) if i<topK]
        if nps_set:
            custom_object['nps'] = nps_set

        nps_set.sort(key=lambda s: len(s), reverse=True)

        # merge tokens in np
        #doc = NlpUtils.get_phrase(doc)

        return doc

    def sort_by_freq(self, tokens, freq):
        ranks = []
        for token in tokens:
            ranks.append(freq(token)[1])
        zipped = zip(tokens, ranks)

        tokens = sorted(zipped, key=lambda tup: tup[1], reverse=True)

        return [token[0] for token in tokens]