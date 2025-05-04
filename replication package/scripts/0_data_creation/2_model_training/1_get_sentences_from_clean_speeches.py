# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# - Extract sentences from the corpus

###################################
#     Modules                   ###
###################################


import os
import gensim
from gensim.summarization.textcleaner import get_sentences
from random import shuffle
import nltk
tagger = nltk.perceptron.PerceptronTagger()
import joblib
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")


###################################
#     Working Directory         ###
###################################

data_c = './data'


# Upload ressources
os.chdir(data_c)
stopwords = joblib.load('stopwords.pkl')
count = joblib.load('word_counts.pkl')


###################################
#     Extract senmtences        ###
###################################

def extract_sentences(dataname):
    data = joblib.load(dataname)
    data = [a[1] for a in data]  # keep only text, no title

    sentences = []
    for doc in data:
        sentences += get_sentences(doc)

    sentences = [item for item in sentences if len(item.split()) > 1]  # drop empty
    sentences = [gensim.utils.simple_preprocess(item) for item in sentences]

    sentences = [[a for a in s if not a.isdigit()] for s in sentences]  # drop digits
    sentences = [[a for a in s if len(a) > 2] for s in sentences]  # drop too short
    
    sentences = [tagger.tag(s) for s in sentences]
    sentences = [[i[0] for i in s if i[1].startswith(('N', 'V', 'J'))] for s in sentences]
    
    sentences = [[stemmer.stem(i) for i in s] for s in sentences]
    sentences = [[a for a in b if a not in stopwords] for b in sentences]
    sentences = [[a for a in b if count[a] >= 10] for b in sentences]

    sentences = [a for a in data if len(a)>1]  # eliminate empty ones
    shuffle(sentences)

    lab = dataname.replace('rawspeeches_', 'sentences_')
    print('{} processed'.format(dataname))
    joblib.dump(sentences, lab)
    print('{} saved'.format(lab))



###################################
#      Multiprocessing          ###
###################################

# Upload speeches
DATI = ['rawspeeches_indexed1.pkl', 'rawspeeches_indexed2.pkl',
        'rawspeeches_indexed3.pkl', 'rawspeeches_indexed4.pkl']

DATI = [[a] for a in DATI]
os.chdir(data_c)

def main():
    with Pool(4) as pool:
        pool.starmap(extract_sentences, DATI)

if __name__ == "__main__":
    freeze_support()
    main()

