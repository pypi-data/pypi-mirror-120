from spacy.lang.zh.stop_words import STOP_WORDS

class Tagger(object):

    def __init__(self, doc, tokens, stop_words):
        self.doc = doc
        self.tokens = tokens
        self.stop_words = stop_words

    def __call__(self):
        if self.stop_words:
            self.tokens['pos'] = [token.tag_ for token in self.doc if token.text and token.text not in STOP_WORDS]
        else:
            self.tokens['pos'] = [token.tag_ for token in self.doc if token.text]
        return self.tokens