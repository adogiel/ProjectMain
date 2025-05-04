# Emotion and Reason in Political Language
# -- Replication Package
# Gennaro and Ash
# 2021

# Description:
# - This codes creates calculates the emotionality score
# - On google unigrams, for all years in corpus

###################################
#     Modules                   ###
###################################

from google_ngram_downloader import readline_google_store
import itertools
import os
import joblib
from gensim.models import Word2Vec
import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
from multiprocessing import Pool, freeze_support
import glob


###################################
#     Working Directory         ###
###################################

# Set working directory
wd_data = './data/3_auxiliary_data'
wd_models = './models'

###############################
#    Auxiliary Functions    ###
###############################


# 1/ Extract unigrams and frequency from google ngrams

def extract(letter, year):
    # Input: letter, year
    # Ourtput: list of words and their frequencies
    fname, url, records = next(readline_google_store(ngram_len=1,
                                                     indices=letter))
    a = [list(next(records))]

    for _ in itertools.repeat(None, 8000000):
        x = list(next(records))
        if (x[0] == a[0][0]) & (x[1] == a[0][1]):  # stop when you start again
            break
        if str(x[1]) == year:  # keep only the year you want
            a.append(x)
        else:
            continue
    for p in "! ( ) - [ ] { } ; : ' \ , < > . / ? @ # $ % ^ & * ~".split(sep=' '):
        a = [i for i in a if p not in i[0]]

    a = [[i[0].split(sep='_')[0], i[2]] for i in a if '_' in i[0]]
    return a


# 2/ Extract document vectors for google ngrams

def yearvec(lista):
    tot = sum(x[1] for x in lista)
    sif = 0.001
    s = [str.lower(i[0]) for i in lista]
    s = [stemmer.stem(w) for w in s]
    f = [sif / (sif + (i[1] / tot)) for i in lista]
    freq = dict(zip(s, f))
    vecs = [w2v.wv[w] * freq[w] for w in s if w in w2v.wv]
    if len(vecs) == 0:
        a = np.nan
        c = np.nan
    else:
        v = np.mean(vecs, axis=0)  # take mean
        v = v.reshape(1, -1)
        v = v.tolist()

        a = cosine(v, affect_centroid)
        c = cosine(v, cog_centroid)
    return (1 + 1 - a) / (1 + 1 - c)

def tutto(year):
    lista = []
    for i in alpha:
        try:
            a = extract(i, year)
            lista = lista + a
            print('letter {} for {} extracted'.format(i, year))
        except:
            pass
    print('words for {} extracted'.format(year))
    res = yearvec(lista)
    print('score for {} calculated'.format(year))
    return res


###############################
#    Letters and Years      ###
###############################

alpha = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split(sep=' ')

###############################
#    Upload Everything      ###
###############################

w2v = Word2Vec.load(wd_models + '/w2v-vectors_8_300.pkl', mmap='r')
word_vectors = w2v.wv

affect_centroid = joblib.load(wd_data + '/affect_centroid.pkl')
cog_centroid = joblib.load(wd_data + '/cog_centroid.pkl')


###############################
#    Main function          ###
###############################


years_list = [str(y) for y in range(1858, 2016)]
years_list = [[years_list[x:x + 20]] for x in range(0, len(years_list), 20)]

def main_function(years_list):
    google_out = []
    for year in years_list:
        score = tutto(year)
        google_out.append([year, score])
        print('Year {} completed, length should be 2: {}'.format(year, len(google_out)))
    lab = 'google_' + str(years_list[0]) + '.pkl'
    joblib.dump(google_out, lab)


def main():
    with Pool(len(years_list)) as pool:
        pool.starmap(main_function, years_list)

if __name__ == "__main__":
    freeze_support()
    main()




###############################
#    All toghether          ###
###############################

os.chdir(wd_data)
DATA = glob.glob("google_1*.pkl")

final = []
for doc in DATA:
    data = joblib.load(doc)
    final = final + data

final = pd.DataFrame(final, columns=['speech_year', 'google'])


# ###############################
# #   Save                    ###
# ###############################

final.to_csv('google_score_year.csv', index=False)
