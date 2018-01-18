# turkish-parliament-texts

## Install

    wget http://voltran.cmpe.boun.edu.tr/temporary_download/datasets/tbmm/tbmm-corpus-v0.1.tar.gz
    tar -zxvf tbmm-corpus-v0.1.tar.gz
    
    pip3 install pipenv
    pipenv install --python 3
    
## Run
     
Example code to save a figure:
   
    pipenv shell
    ipython
    import corpus_loader
    corpus_loader.corpus.plot_word_freqs_given_a_regexp(r"^mebus", keyword="mebus")
   
    
## Preprocessing

Run below command to test the new clean text suit.

    python3 cleaning_text_files.py
