import configparser
from tbmmcorpus import TbmmCorpus

config_parser = configparser.ConfigParser()
config_parser.read("config.ini")
config = config_parser['default']



corpus = TbmmCorpus(metadata=True, config=config)
corpus.load_tbmm_corpus("corpus-v0.1/tbmm_corpus.mm")
corpus.prepare_metadata_to_description_dictionary()
corpus.generate_word_counts()
