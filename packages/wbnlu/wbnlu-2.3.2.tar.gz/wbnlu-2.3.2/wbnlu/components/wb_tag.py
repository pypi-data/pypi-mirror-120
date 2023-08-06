

class Wb_Tag(object):

    def __init__(self, doc, custom_object, knowledge_extractor):
        self.doc = doc
        self.custom_object = custom_object
        self.knowledge_extractor = knowledge_extractor

    def __call__(self):
        wb_tags = self.wbtags(self.doc, self.knowledge_extractor)
        if wb_tags:
            if 'tag_confidence' in self.doc.user_data:
                self.add_confidence(wb_tags, self.doc.user_data['tag_confidence'])
            # TODO: this merge function needs to be improved when actual data shows up!
            if 'wb_tag' in self.custom_object:
                self.custom_object['wb_tags'] = {**wb_tags, **self.custom_object['wb_tags']}
            else:
                self.custom_object['wb_tags'] = wb_tags
            

    
    def wbtags(self, doc, knowledge_extractor):
        tag_dict = {}
        if 'wb_tag' in doc.user_data:
            wb_tags = doc.user_data['wb_tag']
            for label, tok_text_list in wb_tags.items():
                for tok_text in tok_text_list:
                    if not tok_text: continue
                    word = tok_text
                    if label in tag_dict:
                        tag_dict[label].append(word)
                    else:
                        tag_dict[label] = [word]
        char_doc_wbtag_dict = {}
        if 'char_doc_wb_tag' in doc.user_data:
            char_doc_wbtag_dict = doc.user_data['char_doc_wb_tag']
        return knowledge_extractor.merge_dicts(tag_dict, char_doc_wbtag_dict)

    def add_confidence(self, entity_dict, tag_confidence_dict):
        for key, value in tag_confidence_dict.items():
            # some entities may have been filtered!
            if key in entity_dict:
                entity_dict[key] = (entity_dict[key], value)
