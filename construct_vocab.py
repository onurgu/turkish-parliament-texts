import argparse

import glob
import logging
import sys

import configparser
config_parser = configparser.ConfigParser()
config_parser.read("config.ini")
config = config_parser['default']

from utils import tokenize, print_err, turkish_lower

from six import itervalues, iteritems

from gensim import corpora

logger = logging.getLogger(__name__)

def check_if_pdf_directory(filepath):

    if sum(map(lambda x: x == "/", filepath)) == 3:
        return True
    else:
        return False


def combine_files_in_the_pdf_directory(filepath):

    sorted_pagefilepaths = sorted(glob.glob(filepath+"*.processed"))

    document = []
    for page_filepath in sorted_pagefilepaths:
        with open(page_filepath, "r") as f:
            document += [turkish_lower(x) for x in tokenize(" ".join(f.readlines()))]

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

    parser.add_argument("--log_filepath",
                        default="construct_vocab.log")

    parser.add_argument("--max_documents",
                        type=int,
                        default=0)

    args = parser.parse_args()

    logging.basicConfig(filename=args.log_filepath,
                        format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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

        corpus = TbmmCorpus(metadata=True, config=config)

        for idx, filepath in enumerate(glob.iglob(config["data_dir"] + '/**/', recursive=True)):
            # print(idx)
            if args.max_documents != 0 and idx == args.max_documents:
                print_err("Stopping as we hit the max documents limit: %d" % args.max_documents)
                break
            if check_if_pdf_directory(filepath.replace(config["data_dir"], "")):
                document = combine_files_in_the_pdf_directory(filepath)
                metadata_filepath = filepath.replace(config["data_dir"], "")
                corpus.add_document(document, metadata_filepath)
            else:
                continue

        # corpus.dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=2000000, keep_tokens=None)
        good_ids, n_removed = TbmmCorpus.filter_extremes(corpus.dictionary,
                                                         no_below=5, no_above=0.5, keep_n=2000000,
                                                         keep_tokens=None)

        # do the actual filtering, then rebuild dictionary to remove gaps in ids
        TbmmCorpus.filter_tokens(corpus.dictionary, good_ids=good_ids, compact_ids=False)

        logger.info("construct_vocab: rebuilding dictionary, shrinking gaps")

        # build mapping from old id -> new id
        idmap = dict(zip(sorted(itervalues(corpus.dictionary.token2id)), range(len(corpus.dictionary.token2id))))

        # reassign mappings to new ids
        corpus.dictionary.token2id = {token: idmap[tokenid] for token, tokenid in iteritems(corpus.dictionary.token2id)}
        corpus.dictionary.id2token = {}
        corpus.dictionary.dfs = {idmap[tokenid]: freq for tokenid, freq in iteritems(corpus.dictionary.dfs)}

        if n_removed:
            logger.info("Starting to remap word ids in tbmmcorpus documents hashmap")
            # def check_and_replace(x):
            #     if x in idmap:
            #         return x
            #     else:
            #         return -1
            for idx, (doc_id, document) in enumerate(corpus.documents.items()):
                if idx % 1000 == 0:
                    logger.info("remapping: %d documents finished" % idx)
                # corpus.documents[doc_id] = [check_and_replace(oldid) for oldid in document]
                corpus.documents[doc_id] = [idmap[oldid] for oldid in document if oldid in idmap]

        corpus.save_tbmm_corpus(args.corpus_filename)

        # from gensim.models.ldamodel import LdaModel
        from gensim.models.ldamulticore import LdaMulticore

        # setting metadata to False is required because of the way logperplexity code requires the
        # output of get_texts to be.
        corpus.metadata = False
        lda = LdaMulticore(workers=19, corpus=corpus, id2word=corpus.dictionary,
                           num_topics=20,
                           eval_every=100,
                           chunksize=100, passes=10)

        lda.print_topics(20)

        lda.save("tbmm_lda.model")



