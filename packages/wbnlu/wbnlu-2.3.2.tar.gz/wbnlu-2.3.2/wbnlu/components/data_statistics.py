import os

abspath = os.path.abspath(os.path.dirname(__file__))


class Statistics(object):

    def __init__(self):
        self.word_freq_dict = {}
        self._load_freq(os.path.join(abspath, '../resources/statistics/freq_8_days_ngram.txt'),
                                         os.path.join(abspath, '../resources/statistics/freq_unigram.txt'),
                        os.path.join(abspath, '../resources/statistics/freq_en_unigram.txt'),)

    def freq(self, word):
        if word in self.word_freq_dict:
            return self.word_freq_dict[word]
        return (0, -1)

    def _load_freq(self, ngram_file, unigram_file, unigram_en_file):

        ngram_rank = 1
        unigram_rank = 1
        en_unigram_rank = 1
        with open(ngram_file, 'r', encoding='utf8') as f1, \
                open(unigram_file, 'r', encoding='utf8') as f2, \
                open(unigram_en_file, 'r', encoding='utf8') as f3:
            for line in f1:
                if not line:
                    continue
                word, freq = line.split('\t')
                word = word.strip()
                freq = int(freq.strip())
                self.word_freq_dict[word] = (freq, ngram_rank)
                ngram_rank += 1

            for line in f2:
                if not f2:
                    continue
                word, freq = line.split('\t')
                word = word.strip()
                freq = freq.strip()
                self.word_freq_dict[word] = (freq, unigram_rank)
                unigram_rank += 1

            for line in f3:
                if not f3:
                    continue
                word, freq = line.split('\t')
                word = word.strip()
                freq = freq.strip()
                self.word_freq_dict[word] = (freq, en_unigram_rank)
                en_unigram_rank += 1
