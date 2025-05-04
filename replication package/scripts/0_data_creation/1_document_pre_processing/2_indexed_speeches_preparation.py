
# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# - Text preprocessing

# NB: currently set up to work on 4 cores

###################################
#     Modules                   ###
###################################

import os
import joblib
from string import punctuation
translator = str.maketrans('', '', punctuation)
import gensim
import nltk
tagger = nltk.perceptron.PerceptronTagger()
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
from multiprocessing import Pool, freeze_support

###################################
#     Working Directory         ###
###################################

data_c = './data'

###################################
#   Parameters                  ###
###################################

DATI = ['rawspeeches_indexed1_n.pkl', 'rawspeeches_indexed2_n.pkl',
        'rawspeeches_indexed3_n.pkl', 'rawspeeches_indexed4_n.pkl']

###################################
#   Functions                   ###
###################################

def pro1(lista):
    a = [[row[0], row[1].translate(translator)] for row in lista]
    return a

# Tokenize etc
def pro2(lista):
    a = [[row[0], gensim.utils.simple_preprocess(row[1])] for row in lista]
    return a

# Eliminate digits
def pro3(lista):
    a = [[row[0], [w for w in row[1] if not w.isdigit()]] for row in lista]
    return a

# Drop words that are too short
def pro4(lista):
    a = [[row[0], [w for w in row[1] if len(w)>2]] for row in lista]
    return a

# Tag parts of speech and keep only some
def tags(lista):
    t = [[row[0], tagger.tag(row[1])] for row in lista]
    t = [[row[0], [i[0] for i in row[1] if i[1].startswith(('N', 'V', 'J'))]] for row in t]
    return t

# Stem
def pro5(lista):
    a = [[row[0], [stemmer.stem(word) for word in row[1]]] for row in lista]
    return a

# Eliminate Stopwords
os.chdir(data_c)
stopwords = joblib.load('stopwords_n.pkl')
proc = joblib.load('procedural_words.pkl')
stopwords = set(stopwords).union(proc)
del proc
def pro6(lista):
    for i in range(len(lista)):
        x = lista[i][0]
        y = lista[i][1]
        y = [w for w in y if w not in stopwords]
        lista[i] = [x, y]
    return lista

# Drop empty speeches
def dropnull(lista):
    a = [row for row in lista if len(' '.join(row[1]))>0]
    return a


###################################
#   Main                       ###
###################################


def preprocessing(data_name):
    data = joblib.load(data_name)
    data = pro1(data)
    data = pro2(data)
    data = pro3(data)
    data = pro4(data)
    data = tags(data)
    data = pro5(data)
    data = pro6(data)
    data = dropnull(data)
    lab = data_name.replace('.pkl', '') + '_temp.pkl'
    joblib.dump(data, lab)


###################################
#      Multiprocessing          ###
###################################

DATI = [[a] for a in DATI]
os.chdir(data_c)

def main():
    with Pool(4) as pool:
        pool.starmap(preprocessing, DATI)

if __name__ == "__main__":
    freeze_support()
    main()
