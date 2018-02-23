import configparser
import tbmmcorpus

DEV=False
TOPIC_DISTRIBUTIONS=False

if DEV:
    corpus_filepath = "corpus-dev/tbmm_corpus"
else:
    corpus_filepath = "corpus-v0.2/tbmm_corpus.mm"

config_parser = configparser.ConfigParser()
config_parser.read("config.ini")
config = config_parser['default']


corpus = tbmmcorpus.TbmmCorpus(metadata=True, config=config)
if DEV:
    corpus.load_tbmm_corpus(corpus_filepath)
else:
    corpus.load_tbmm_corpus(corpus_filepath)

corpus.prepare_metadata_to_description_dictionary()
corpus.generate_word_counts()

if TOPIC_DISTRIBUTIONS:

    if DEV:
        lda_model_path = "corpus-dev/tbmm_corpus.tbmm_lda.model"
    else:
        lda_model_path = "corpus-v0.2/tbmm_lda.model.passes_100"

    corpus.prepare_metadata_to_description_dictionary()

    corpus.generate_word_counts()

    from gensim.models.ldamodel import LdaModel
    # lda = LdaModel.load("corpus-v0.1/tbmm_lda.model")
    if DEV:
        lda = LdaModel.load(lda_model_path)
    else:
        lda = LdaModel.load(lda_model_path)

    topic_dist_matrix, label_vector = corpus.calculate_topic_distributions_of_all_documents(lda)

    # for topic_no in range(1, 20):
    #     corpus.plot_topic_across_time(topic_no, topic_dist_matrix, label_vector)
