import configparser
import  tbmmcorpus

DEV=False
TOPIC_DISTRIBUTIONS=False

config_parser = configparser.ConfigParser()
config_parser.read("config.ini")
config = config_parser['default']


corpus = tbmmcorpus.TbmmCorpus(metadata=True, config=config)
if DEV:
    corpus.load_tbmm_corpus("corpus-dev/tbmm_corpus")
else:
    corpus.load_tbmm_corpus("corpus-v0.1/tbmm_corpus.mm")
corpus.prepare_metadata_to_description_dictionary()
corpus.generate_word_counts()

if TOPIC_DISTRIBUTIONS:
    corpus.prepare_metadata_to_description_dictionary()

    corpus.generate_word_counts()

    from gensim.models.ldamodel import LdaModel
    lda = LdaModel.load("corpus-v0.1/tbmm_lda.model")

    topic_dist_matrix, label_vector = corpus.calculate_topic_distributions_of_all_documents(lda)

    for topic_no in range(1, 20):
        corpus.plot_topic_across_time(topic_no, topic_dist_matrix, label_vector)
