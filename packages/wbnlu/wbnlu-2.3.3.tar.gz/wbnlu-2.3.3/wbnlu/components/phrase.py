

class Phrase(object):

    def __init__(self, doc, custom_object):
        self.doc = doc
        self.custom_object = custom_object

    def __call__(self,  np_length=2):
        # print (self.doc.noun_chunks)
        
        phrases = [chunk.text for chunk in self.doc.noun_chunks if len(chunk.text) >= np_length]
        # print (phrases)
        # print ('Phrase: ', phrases)
        if phrases:
            self.custom_object['phrase'] = phrases
        return phrases, self.doc

