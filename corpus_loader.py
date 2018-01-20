import configparser
import  tbmmcorpus

config_parser = configparser.ConfigParser()
config_parser.read("config.ini")
config = config_parser['default']


corpus = tbmmcorpus.TbmmCorpus(metadata=True, config=config)
corpus.load_tbmm_corpus("corpus-dev/tbmm_corpus")
corpus.load_tbmm_corpus("corpus-v0.1/tbmm_corpus")
corpus.prepare_metadata_to_description_dictionary()
corpus.generate_word_counts()
