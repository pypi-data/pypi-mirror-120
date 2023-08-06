from spacy.lang.zh.stop_words import STOP_WORDS

class Parser(object):

    def __init__(self, doc, tokens, stop_words=True):
        self.doc = doc
        self.tokens = tokens
        self.stop_words = stop_words

    def __call__(self):
        deps = []
        heads = []
        children = []
        for token in self.doc:
            if self.stop_words:
                if token.text in STOP_WORDS:
                    continue
            deps.append(token.dep_)
            heads.append(token.head.text)
            childs = []
            for child in token.children:
                # childs.append(child)
                childs.append(child.text)
            children.append(childs)
        self.tokens['dep'] = {'deps': deps, 'heads': heads, 'children': children}
        return self.tokens