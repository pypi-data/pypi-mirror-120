import re
import os
from itertools import zip_longest
from wbnlu.utils.fileio import read_yaml_file

from opencc import OpenCC

import emoji

cc = OpenCC('t2s')
abspath = os.path.abspath(os.path.dirname(__file__))
CONFIG = read_yaml_file(os.path.join(abspath, "../configs/other_config.yml"))

TEXT_LOWER = CONFIG['TEXT_LOWER']
REMOVE_PUNCTUALTION = CONFIG['REMOVE_PUNCTUALTION']
REMOVE_ALL_SPACES = CONFIG['REMOVE_ALL_SPACES']
REMOVE_ALL_BUT_ONE_SPACES = CONFIG['REMOVE_ALL_BUT_ONE_SPACES']
REMOVE_EMOJIS = CONFIG['REMOVE_EMOJIS']

REMOVE_HASHTAG = CONFIG['REMOVE_HASHTAG']

class Text_Normalizer(object):

    def __init__(self, text):
        self.text = text
        self.name = 'normalized_text'

    def __call__(self, remove_hash=False, text_lower=False, remove_punct=False, remove_emojis=True, remove_all_space=False, remove_all_but_one_space=True, remove_urls=True):
        """

        @param text: 原始文本
        @param remove_hash: 是否删除 hash 字符,
        @param text_lower: 是否转换文本为小写
        @param remove_punct: 是否删除标点符号
        @param remove_emojis: 是否删除情感字符
        @param remove_all_space: 是否删除所有空格字符
        @param remove_all_but_one_space: 是否删除连续的空格字符，只保留其中一个

        此外，当此函数被调用时，剩下几个函数自动调用：
        1. remove_url: 删除 URL
        2. remove_break_line: 删除行分隔符
        3. sstrip: 删除特殊空格字符 \u200b
        4. remove_junk: 删除脏数据
        5. qs2bs: 全角转半角
        6. t2s: 繁体转简体
        @return: 正规化的文本
        """
        text = self.text
        if not text:
            return " "
        if remove_urls:
            text = remove_url(text)
        text = remove_break_line(text)
        text = sstrip(text)
        text = remove_junk(text)
        text = strQ2B(text)
        text = t2s(text)
        if remove_hash:
            text = remove_hashtag(text)
        if text_lower:
            text = text.lower()
        if remove_punct:
            text = remove_punctuation(text)
        if remove_emojis:
            text = remove_emoji(text)
        if remove_all_space:
            text = remove_all_spaces(text)
        elif remove_all_but_one_space:
            text = remove_all_but_one_spaces(text)

        if not text:
            return ""
        return text.strip()


def normalize(text, remove_hash=False, text_lower=False, remove_punct=False, remove_emojis=True, remove_all_space=False, remove_all_but_one_space=True):
    if not text:
        return " "
    text = remove_url(text)
    text = remove_break_line(text)
    text = sstrip(text)
    text = remove_junk(text)
    text = qs2bs(text)
    text = t2s(text)
    if remove_hash:
        text = remove_hashtag(text)
    if text_lower:
        text = text.lower()
    if remove_punct:
        text = remove_punctuation(text)
    if remove_emojis:
        text = remove_emoji(text)
    if remove_all_space:
        text = remove_all_spaces(text)
    elif remove_all_but_one_space:
        text = remove_all_but_one_spaces(text)

    if not text:
        return ""
    return text.strip()


def t2s(text):
    return cc.convert(text)

def sstrip(text):
    text = text.replace('<U+200B>', '').strip()
    return text.replace(u'\u200b', '').strip()

def remove_emoji(text):
    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    return ''.join([str for str in list(text) if not any(i in str for i in emoji_list)])

def is_emoji(text):
    return text in emoji.UNICODE_EMOJI

def remove_junk(text):
    return re.sub(ZH_JUNK_PATTERN, "", text).strip()

def remove_hashtag(text):
    return text.replace('#', '').strip()

# 短发 中发 长发 每个长度总有一款发型适合 http://t.cn/AigOWB1q
def remove_url(text):
    return re.sub(URL_PATTERN, "", text).strip()

def remove_all_spaces(text):
    return re.sub(WS_PATTERN, "", text)

def remove_all_but_one_spaces(text):
    return re.sub(AT_LEAST_TWO_WS_PATTERN, " ", text).strip()

def remove_punctuation(text):
    return re.sub(ZH_PUNCT_PATTERN, "", text).strip()

def remove_break_line(text):
    return re.sub(BREAK_LINE_PATTERN, "", text).strip()

def is_ascii(string):
    return all(ord(c) < 128 for c in string)

def is_ascii_char(c):
    return ord(c) < 128

def has_ascii_char(string):
    for c in string:
        if is_ascii_char(c) and c != ' ':
            return True
    return False

def is_cjk(text):
    if re.search("[\u4e00-\u9FFF]", text):
        return True
    return False

def is_korean(text):
    re.search("[\uac00-\ud7a3]", text)

def is_japanese(text):
    re.search("[\u3040-\u30ff]", text)

def is_chinese(text):
    re.search("[\u4e00-\u9FFF]", text)

def is_hangul(char):
    value = ord(char)
    return value >= 4352 and value <= 4607

def are_hangul(string):
    return all(is_hangul(i) for i in string)

def has_hangul(string):
    return any(is_hangul(i) for i in string)

def is_unigram(text):
    return len(text) == 1

def qs2bs(text):
    new_text = ''
    for c in text:
        new_text += qc2bc(c)
    return new_text

def qc2bc(zh_char):
    assert len(zh_char) == 1
    inside_code = ord(zh_char)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:
        return zh_char
    return chr(inside_code)


def strQ2B(ustring):
    ss = []
    for s in ustring:
        rstring = ""
        prev_code = -1
        next_code = -1
        for i, uchar in enumerate(s):
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                flag1 = False
                flag2 = False
                if i < len(s)-1:
                    next_code = ord(s[i+1])
                else:
                    next_code = -1
                if (prev_code >= 0 and prev_code <= 127) or prev_code == -1:
                    flag1 = True
                if (next_code >= 0 and next_code <= 127) or next_code == -1:
                    flag2 = True
                if flag1 and flag2:
                    inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)

def strB2Q(ustring):
    ss = []
    for s in ustring:
        rstring = ""
        prev_code = -1
        next_code = -1
        for i, uchar in enumerate(s):
            inside_code = ord(uchar)
            if inside_code == 32:
                inside_code = 12288
            elif (inside_code >= 33 and inside_code <= 126):
                flag1 = False
                flag2 = False
                if i < len(s)-1:
                    next_code = ord(s[i+1])
                else:
                    next_code = -1
                if (prev_code >= 19968 and prev_code <= 40959) or prev_code == -1:
                    flag1 = True
                if (next_code >= 19968 and next_code <= 40959) or next_code == -1:
                    flag2 = True
                if flag1 and flag2:
                    inside_code += 65248
                    if inside_code == 65294:
                        inside_code = 12290
                prev_code = inside_code
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)

def has_zh_words(word_list, text):
    for word in word_list:
        if word in text:
            return True
    return False

def split_keep_delimiter(line):
    sentences = []
    lines = re.split(ZH_SEG_PUNCT_CHARS_PATTERN, line)
    for a,b in zip_longest(lines[::2],lines[1::2]):
        r = a+(b if b else '')
        sentences.append(r)
    new_sentences = []
    for sentence in sentences:
        sentence = sentence.replace('\\n','\n')
        new_sentences.append(sentence)

    return new_sentences

def unit_exchange(text):
    if text.find('cm'):
        index = text.find('cm')
        if not is_chinese(text[index-1]):
            text = text[:index]+'厘米'+text[index+2:]
    return text


WS_PATTERN = re.compile(r"\s+")
BREAK_LINE_PATTERN = re.compile(r"[\t\r\n]")
AT_LEAST_TWO_WS_PATTERN = re.compile(r"\s{2,}")

# context = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "",context)
# context = re.sub("[【】╮╯▽╰╭★→「」]+".decode("utf8"),"",context)
# context = re.sub("！，❤。～《》：（）【】「」？”“；：、".decode("utf8"),"",context)

URL_PATTERN = re.compile(r"https?:[^\s]+[a-zA-Z0-9]")
ZH_SEG_PUNCT_CHARS = ["。", "！", "？", "；", "!", "?"]
ZH_SEG_PUNCT_CHARS_PATTERN = re.compile(r"([。！？,；!?\n])")
ZH_PUNCT_PATTERN = re.compile(r"[。，！？；,!?.【】~“”@·╮╯▽╰╭★→「」/~…&*+—^❤～《》：（）\]\[\u200b]")
ZH_JUNK_PATTERN = re.compile(r"[●~〜·╮╯▽╰╭★→…&*^❤～\u200b\xa0]")
TFIDF_TERM_PATTERN = re.compile('([^\s]+)\s+(\d+)\s+\d+\s+(\d+\.\d+)')
# 眼影                    467798    16536                     0.000181422351233672      		面膜                    634692
TF_TERM_PATTERN = re.compile('[^\s]+\s+\d+\s+\d+\s+\d+\.\d+\s+([^\s]+)+\s+(\d+)')

if __name__ == "__main__":
    # str = "Fish Market𓆝𓆟𓆜𓆞𓆡𓆝𓆟𓆜𓆞𓆡 "
    # print(str)
    # print(remove_emoji(str))

    # text = "短发 中发 长发 每个长度总有一款发型适合 http://t.cn/AigOWB1q"
    # print(remove_url(text))

    # text = "短发  中发 长发"
    # print(remove_all_but_one_spaces(text))

    text = "姐妹们，怎么把假 睫 毛贴 成太 阳花呢？"
    print(remove_all_spaces(text))

    # text = "唇膏.."
    # print(remove_punctuation(text))

    # text = '红'
    # print(is_ascii_char(text))

    # s = '种草 ​'
    # print(len(s))
    # s = remove_punctuation(s)
    # print(len(s))

    # text = '长发 每个长度.【”@“”@·╮╯▽╰╭★→「」/$~#￥%…&*+—^❤～《》：（）\u200b'

    # print(remove_punctuation(text))

    # print(remove_break_line('头要变得越低。 \n\n被称为'))

    # str = "Fish Market𓆝𓆟𓆜𓆞𓆡𓆝𓆟𓆜𓆞𓆡 "
    # print(str)
    # print(remove_emoji(str))

    # str = '。 ； ，'
    # str2 = qs2bs(str)
    # print(len(str2), len(str))

    str = '椒卡末节0分，里弗斯再次被3：1翻船。'
    print ('Quan 2 ban: ', str, ' -> ',strQ2B(str))

    str = '我来了,我来了.'
    print ('Ban 2 quan: ', str, ' -> ', strB2Q(str))

    str = '博班的手掌（27.3cm）'
    print ('Unit: ', str, ' -> ', unit_exchange(str))
