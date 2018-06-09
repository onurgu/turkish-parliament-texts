import sys

from nltk import RegexpTokenizer

CHARMAP = {
    "to_upper": {
        u"ı": u"I",
        u"i": u"İ",
    },
    "to_lower": {
        u"I": u"ı",
        u"İ": u"i",
    }
}


def turkish_lower(s):
    for key, value in CHARMAP.get("to_lower").items():
        s = s.replace(key, value)

    return s.lower()


def turkish_upper(s):
    for key, value in CHARMAP.get("to_upper").items():
        s = s.replace(key, value)

    return s.upper()

def tokenize(line):
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+')
    # tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
    return tokenizer.tokenize(line)


def print_err(*s):

    sys.stderr.write(" ".join([str(x) for x in s]) + "\n")