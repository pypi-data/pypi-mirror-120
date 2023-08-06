import wbnlu

TAG_FOR_CONTENT_WORDS = {'NN', 'NR', 'VA', 'VC', 'VV', 'FW', 'JJ'}

class content_words(object):

    name='content_words'

    @staticmethod
    def Content_Words(text):
        # text = wbnlu.nlp(text, enable=['text_normalizer'])
        # print ('text_normalizer')
        # swr_tagger_out = wbnlu.nlp(text, enable=['swr', 'tagger'], remove_meme=True, remove_url=True, remove_onom=True)
        swr_tagger_out = wbnlu.nlp(text, enable=['swr'], remove_meme=True, remove_url=True, remove_onom=True)
        # print ('swr_out: ', swr_tagger_out)
        De_meme_url = wbnlu.nlp(text, enable=['swr'], remove_stopwords=False, remove_meme=True, remove_url=True, remove_onom=True, remove_brand=True, remove_internet_phrase=True)
        tagger_out = wbnlu.nlp(De_meme_url, enable=['tagger'])
        # phrase_out = wbnlu.nlp(tagger_out, enable=['phrase'])
        entity_out = wbnlu.nlp(tagger_out, enable=['phrase_match'])
        # print ('phrase_match_out:', entity_out)

        phrase_res = []
        entity_res = []
        swr_res = []

        # if 'phrase' in phrase_out.keys():
        #     phrase_res = phrase_out['phrase']
        if 'udp' in entity_out.keys():
            entity_res = (list(entity_out['udp'].values())[0])
        # if 'Dewords' in swr_tagger_out:
        #     for i, word in enumerate(swr_tagger_out['Dewords']):
        #         if swr_tagger_out['pos'][i] in TAG_FOR_CONTENT_WORDS:
        #             swr_res.append(word)
        if 'Dewords' in swr_tagger_out:
            for word in swr_tagger_out['Dewords']:
                if word in De_meme_url['Dewords']:
                    index = De_meme_url['Dewords'].index(word)
                    if tagger_out['pos'][index] in TAG_FOR_CONTENT_WORDS:
                        swr_res.append(word)
        # if 'Dewords' in swr_out.keys():
        #     swr_res = swr_out['Dewords']

            # print(entity_res)
            # print(list(entity_out['udp'].values()))
        # print('Phrase_match res:', entity_res)
        # print('SWR:', swr_res)

        return set(phrase_res+entity_res+swr_res)