# Emotion and Reason in Political Language
# -- Replication Package
# Gennaro and Ash
# 2021

# Description:
# - Find positve and negative sentiment in speeches
# - Based on our method

###################################
#     Modules                   ###
###################################

import os
import joblib
from gensim.models import Word2Vec
import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine
import glob
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")


###################################
#     Working Directory         ###
###################################

# Set working directory
wd_data = './data/3_auxiliary_data'
wd_models = './models'

###################################
#     Upload                    ###
###################################

w2v = Word2Vec.load(wd_models + '/w2v-vectors_8_300.pkl', mmap='r')
freq = joblib.load(wd_data + '/word_freqs.pkl')

cognition = joblib.load(wd_data + '/dictionary_cognition.pkl')
affect = joblib.load(wd_data + '/dictionary_affect.pkl')


# function to find the SIF weighted centroid
def findcentroid(text, model):
    vecs = [model.wv[w] * freq[w] for w in text if w in model.wv]
    vecs = [v for v in vecs if len(v) > 0]
    centroid = np.mean(vecs, axis=0)
    centroid = centroid.reshape(1, -1)
    return centroid


###############################################
#  Find the positve and negative centroids   ##
###############################################

neg = 'hatr, hate, griev, grief, wrong'
neg = neg.split(', ')
neg = list(set([stemmer.stem(i) for i in neg]))  # 145

neg2 = []
for i in neg:
    neg2 += [a[0] for a in w2v.wv.most_similar(i, topn=10)]


pos = 'strength, heart, donat, thought'  # solidar love bless eliminated from original list
pos = pos.split(', ')
pos = list(set([stemmer.stem(i) for i in pos]))  # 145

pos2 = []
for i in pos:
    pos2 += [a[0] for a in w2v.wv.most_similar(i, topn=10)]


neg3 = list(set(neg2) - set(pos2).intersection(set(neg2)))
pos3 = list(set(pos2) - set(pos2).intersection(set(neg2)))

pos3 = [a for a in pos3 if a not in affect + cognition]
neg3 = [a for a in neg3 if a not in affect + cognition]

pos_centroid = findcentroid(pos3, w2v)
neg_centroid = findcentroid(neg3, w2v)

', '.join(sorted(neg3))
', '.join(sorted(pos3))


del neg
del neg2
del pos
del pos2
del cognition
del affect


############################
#  Doc vectors and score  ##
############################

# find final measure
def documentvecweight(lista):
    out = []
    lista = [i for i in lista if len(i) > 0]
    for s in lista:
        vecs = [w2v.wv[w] * freq[w] for w in s[1] if w in w2v.wv]
        if len(vecs) == 0:
            p = np.nan
            n = np.nan
        else:
            v = np.mean(vecs, axis=0)  # take mean
            v = v.reshape(1, -1)
            v = v.tolist()

            p = cosine(v, pos_centroid)
            n = cosine(v, neg_centroid)
            score = (1 + 1 - p) / (1 + 1 - n)

        out.append([s[0], p, n, score])
    return out


DATA = glob.glob("speeches_indexed_clean1*.pkl") + \
    glob.glob("speeches_indexed_clean2*.pkl") + \
    glob.glob("speeches_indexed_clean3*.pkl") + \
    glob.glob("speeches_indexed_clean4*.pkl")


tot = []
for i in DATA:
    testi = joblib.load(i)
    vec = documentvecweight(testi)
    tot = tot + vec


tot = pd.DataFrame(tot)
tot.columns = ['title', 'positive_d', 'negative_d', 'sentiment']
joblib.dump(tot, 'sentiment.pkl')
