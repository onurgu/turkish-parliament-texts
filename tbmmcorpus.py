import codecs
import logging

from gensim.corpora.textcorpus import TextCorpus
from gensim.corpora.dictionary import Dictionary

from utils import tokenize, print_err

from six import itervalues, iteritems

logger = logging.getLogger(__name__)

class TbmmCorpus(TextCorpus):

    def __init__(self, input=None, dictionary=None, metadata=False, character_filters=None,
                 tokenizer=None, token_filters=None):
        super().__init__(input, dictionary, metadata, character_filters, tokenizer, token_filters)

        self.documents = {}
        self.documents_metadata = {}

        self.dictionary.debug = True

        # self.dictionary.filter_tokens = self.filter_tokens
        #
        # self.dictionary.filter_extremes = self.filter_extremes

    def filter_extremes(dictionary_object, no_below=5, no_above=0.5, keep_n=100000, keep_tokens=None):
        """
        Filter out tokens that appear in

        1. less than `no_below` documents (absolute number) or
        2. more than `no_above` documents (fraction of total corpus size, *not*
           absolute number).
        3. if tokens are given in keep_tokens (list of strings), they will be kept regardless of
           the `no_below` and `no_above` settings
        4. after (1), (2) and (3), keep only the first `keep_n` most frequent tokens (or
           keep all if `None`).

        After the pruning, shrink resulting gaps in word ids.

        **Note**: Due to the gap shrinking, the same word may have a different
        word id before and after the call to this function!
        """
        assert isinstance(dictionary_object, Dictionary), "The object must be an instance of Dictionary"
        no_above_abs = int(
            no_above * dictionary_object.num_docs)  # convert fractional threshold to absolute threshold

        # determine which tokens to keep
        if keep_tokens:
            keep_ids = [dictionary_object.token2id[v] for v in keep_tokens if v in dictionary_object.token2id]
            good_ids = (
                v for v in itervalues(dictionary_object.token2id)
                if no_below <= dictionary_object.dfs.get(v, 0) <= no_above_abs or v in keep_ids
            )
        else:
            good_ids = (
                v for v in itervalues(dictionary_object.token2id)
                if no_below <= dictionary_object.dfs.get(v, 0) <= no_above_abs
            )
        good_ids = sorted(good_ids, key=dictionary_object.dfs.get, reverse=True)
        if keep_n is not None:
            good_ids = good_ids[:keep_n]
        bad_words = [(dictionary_object[idx], dictionary_object.dfs.get(idx, 0)) for idx in
                     set(dictionary_object).difference(good_ids)]
        logger.info("discarding %i tokens: %s...", len(dictionary_object) - len(good_ids), bad_words[:10])
        logger.info(
            "keeping %i tokens which were in no less than %i and no more than %i (=%.1f%%) documents",
            len(good_ids), no_below, no_above_abs, 100.0 * no_above
        )

        logger.info("resulting dictionary: %s", dictionary_object)
        return good_ids, (len(dictionary_object) - len(good_ids))

    def filter_tokens(dictinoary_object, bad_ids=None, good_ids=None, compact_ids=True):
        """
        Remove the selected `bad_ids` tokens from all dictionary mappings, or, keep
        selected `good_ids` in the mapping and remove the rest.

        `bad_ids` and `good_ids` are collections of word ids to be removed.
        """
        assert isinstance(dictinoary_object, Dictionary), "The object must be an instance of Dictionary"
        if bad_ids is not None:
            bad_ids = set(bad_ids)
            dictinoary_object.token2id = {token: tokenid for token, tokenid in iteritems(dictinoary_object.token2id) if
                                          tokenid not in bad_ids}
            dictinoary_object.dfs = {tokenid: freq for tokenid, freq in iteritems(dictinoary_object.dfs) if
                                     tokenid not in bad_ids}
        if good_ids is not None:
            good_ids = set(good_ids)
            dictinoary_object.token2id = {token: tokenid for token, tokenid in iteritems(dictinoary_object.token2id) if
                                          tokenid in good_ids}
            dictinoary_object.dfs = {tokenid: freq for tokenid, freq in iteritems(dictinoary_object.dfs) if
                                     tokenid in good_ids}
        if compact_ids:
            dictinoary_object.compactify()

    def add_document(self, document, filepath):
        self.dictionary.add_documents([document],
                                      prune_at=None)
        self.documents[len(self.documents)+1] = self.dictionary.doc2idx(document)

        self.documents_metadata[len(self.documents)] = {
            'filepath': filepath
        }

        if len(self.documents) % 100 == 0:
            print_err("n_documents: %d" % len(self.documents))
            good_ids, n_removed = TbmmCorpus.filter_extremes(self.dictionary, no_below=0, no_above=1, keep_n=2000000)
            # do the actual filtering, then rebuild dictionary to remove gaps in ids
            TbmmCorpus.filter_tokens(self.dictionary, good_ids=good_ids, compact_ids=False)

            if n_removed:
                logger.info("Starting to remap word ids in tbmmcorpus documents hashmap")
                n_ids = len(self.dictionary.id2token)
                for idx, (doc_id, document) in enumerate(self.documents.items()):
                    def check_and_alter(x):
                        if x >= n_ids:
                            return -1
                        else:
                            return x
                    if idx % 1000 == 0:
                        logger.info("remapping: %d documents finished" % idx)
                    self.documents[doc_id] = map(check_and_alter, document)

    def getstream(self):
        return super().getstream()

    def preprocess_text(self, text):
        return tokenize(text)

    def get_texts(self):
        if self.metadata:
            for idx, (documentno, document_text_in_ids) in enumerate(self.documents.items()):
                if idx % 1000 == 0:
                    print_err("get_texts:", documentno)
                document_text = [self.dictionary[id] for id in document_text_in_ids]
                yield self.preprocess_text(" ".join(document_text)), \
                      (documentno, self.documents_metadata[documentno])
        else:
            for idx, (documentno, document_text_in_ids) in enumerate(self.documents.items()):
                if idx % 1000 == 0:
                    print_err("get_texts:", documentno)
                document_text = [self.dictionary[id] for id in document_text_in_ids]
                yield self.preprocess_text(" ".join(document_text))

    def __len__(self):
        return len(self.documents)

    def __iter__(self):
        """The function that defines a corpus.

        Iterating over the corpus must yield sparse vectors, one for each document.
        """
        if self.metadata:
            for text, metadata in self.get_texts():
                yield self.dictionary.doc2bow(text, allow_update=False), metadata
        else:
            for text in self.get_texts():
                yield self.dictionary.doc2bow(text, allow_update=False)

    def save_tbmm_corpus(self, fname):
        # example code:
        # logger.info("converting corpus to ??? format: %s", fname)
        with codecs.open(fname, 'w', encoding='utf-8') as fout:
            for doc, (doc_id, metadata) in self.get_texts():  # iterate over the document stream
                fmt = " ".join([str(x) for x in self.dictionary.doc2idx(doc)])  # format the document appropriately...
                fout.write("%d %s %s\n" % (doc_id, metadata['filepath'], fmt))  # serialize the formatted document to disk

        self.dictionary.save(fname + ".vocabulary")
        self.dictionary.save_as_text(fname + ".vocabulary.txt")


