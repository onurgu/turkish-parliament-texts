import codecs

from gensim.corpora.textcorpus import TextCorpus

from utils import tokenize, print_err


class TbmmCorpus(TextCorpus):

    def __init__(self, input=None, dictionary=None, metadata=False, character_filters=None,
                 tokenizer=None, token_filters=None):
        super().__init__(input, dictionary, metadata, character_filters, tokenizer, token_filters)

        self.documents = {}
        self.documents_metadata = {}

    def add_document(self, document, filepath):
        self.dictionary.add_documents([document], prune_at=None)
        self.documents[len(self.documents)+1] = document

        self.documents_metadata[len(self.documents)] = {
            'filepath': filepath
        }

        if len(self.documents) % 100 == 0:
            print_err("n_documents: %d" % len(self.documents))


    def getstream(self):
        return super().getstream()

    def preprocess_text(self, text):
        return tokenize(text)

    def get_texts(self):
        if self.metadata:
            for idx, (documentno, document_text) in enumerate(self.documents.items()):
                if idx % 1000 == 0:
                    print_err("get_texts:", documentno, document_text)
                yield self.preprocess_text(" ".join(document_text)), \
                      (documentno, self.documents_metadata[documentno])
        else:
            for idx, (documentno, document_text) in enumerate(self.documents.items()):
                if idx % 1000 == 0:
                    print_err("get_texts:", documentno, document_text)
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


