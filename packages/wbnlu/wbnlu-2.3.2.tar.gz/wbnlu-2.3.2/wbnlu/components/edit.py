import re
from spacy.lang.zh.stop_words import STOP_WORDS, ONOMATOPOEIA, BRAND, INTERNET_PHRASE


class EDIT(object):

    def __init__(self, doc, output, remove_stopwords=True,remove_meme=False, remove_url=False, remove_all_spaces=True, remove_onom=False,
        remove_brand=False, remove_internet_phrase=True):
        self.doc = doc
        self.output = output
        self.remove_stopwords=remove_stopwords
        self.meme = remove_meme
        self.url = remove_url
        self.onom = remove_onom
        self.brand = remove_brand
        self.internet_phrase = remove_internet_phrase
        self.remove_all_spaces = remove_all_spaces

    def __call__(self):
        # if self.stop_words:
        #     self.tokens['stop_words'] = [token.text for token in self.doc if token.text and token.text not in STOP_WORDS]
        # else:
        #     self.tokens['pos'] = [token.tag_ for token in self.doc if token.text]
        stopwords_list = [token.text for token in self.doc if token.text]
        self.output['words'] = [token.text for token in self.doc if token.text]
        if self.remove_stopwords:
            stopwords_list = [token.text for token in self.doc if token.text and token.text not in STOP_WORDS]
            self.output['Dewords'] = stopwords_list
        
        if self.meme:
            #TODO: load emoji dictionary
            
            stopwords_list = [word for word in stopwords_list if word and word[0]!='[' and word[-1]!=']']
            self.output['Dewords'] = stopwords_list

        if self.url:
            stopwords_list = [word for word in stopwords_list if word and 'http://' not in word]
            self.output['Dewords'] = stopwords_list
        # self.output['swr'] = tokens
        
        if self.remove_all_spaces:
            # WS_PATTERN = re.compile(r"\s+")
            stopwords_list = [word for word in stopwords_list if word and word[0]!=' ' and word[-1]!=' ' ]
            self.output['Dewords'] = stopwords_list

        if self.onom:
            stopwords_list = [word for word in stopwords_list if word and word[0] not in ONOMATOPOEIA and word[-1] not in ONOMATOPOEIA ]
            self.output['Dewords'] = stopwords_list

        if self.brand:
            stopwords_list = [word for word in stopwords_list if word and word not in BRAND ]
            self.output['Dewords'] = stopwords_list

        if self.internet_phrase:
            stopwords_list = [word for word in stopwords_list if word and word not in INTERNET_PHRASE]
            self.output['Dewords'] = stopwords_list

        return self.output