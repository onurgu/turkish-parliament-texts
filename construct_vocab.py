import argparse
import glob
import sys

from utils import tokenize, print_err

config = {}

config["data_dir"] = "data/TXTs/"

from gensim import corpora


def check_if_pdf_directory(filepath):

    if sum(map(lambda x: x == "/", filepath)) == 3:
        return True
    else:
        return False


def combine_files_in_the_pdf_directory(filepath):

    import os
    sorted_pagefilepaths = sorted(glob.glob(filepath+"*.processed"))

    document = []
    for page_filepath in sorted_pagefilepaths:
        with open(page_filepath, "r") as f:
            document += tokenize(" ".join(f.readlines()))

    return document


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument("--command",
                        choices=["construct_vocab", "construct_corpus"],
                        default="")

    parser.add_argument("--vocabulary_filename",
                        default="vocabulary.dict")

    parser.add_argument("--corpus_filename",
                        default="tbmm_corpus.mm")

    args = parser.parse_args()

    if args.command == "construct_vocab":

        dictionary = corpora.Dictionary()

        count = 0

        line = sys.stdin.readline()
        while line:

            tokens = tokenize(line)

            dictionary.add_documents([tokens], prune_at=None)
            count += 1

            if count % 100000 == 0:
                print_err("line %d %d" % (count, len(dictionary)))

            line = sys.stdin.readline()

        dictionary.save(args.vocabulary_filename)
        dictionary.save_as_text(args.vocabulary_filename + ".txt")

    elif args.command == "construct_corpus":
        # use glob to recurse under data/TXTs directory

        # every directory in the first level is the type of the content (cs, kapali-oturum, etc.)

        # in the second level, eeach directory is like ko-d01 (separated by -).

        # in the third level, the directories are actually matched with pdf files.
        # our get_texts code could treat the files inside them as pages and combine them and then add to
        # dictionary and the corpus (maybe just adding to the corpus is sufficient)
        # 1) does adding to the corpus require preprocessing? I think so. TextCorpus is suitable for these
        # operations

        from tbmmcorpus import TbmmCorpus

        from gensim.corpora.mmcorpus import MmCorpus

        corpus = TbmmCorpus(metadata=True)

        for filepath in glob.iglob(config["data_dir"] + '/**/', recursive=True):

            if check_if_pdf_directory(filepath.replace(config["data_dir"], "")):
                document = combine_files_in_the_pdf_directory(filepath)
                metadata_filepath = filepath.replace(config["data_dir"], "")
                corpus.add_document(document, metadata_filepath)
            else:
                continue

        corpus.save_tbmm_corpus(args.corpus_filename)

        from gensim.models.ldamodel import LdaModel

        lda = LdaModel(corpus=corpus, id2word=corpus.dictionary.id2token, num_topics=20,
                                              update_every=1, chunksize=100, passes=1)

        lda.print_topics(20)

        lda.save("tbmm_lda.model")



