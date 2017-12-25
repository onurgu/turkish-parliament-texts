import sys

from nltk import RegexpTokenizer

def tokenize(line):
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
    return tokenizer.tokenize(line)


def print_err(*s):

    sys.stderr.write(" ".join(s) + "\n")