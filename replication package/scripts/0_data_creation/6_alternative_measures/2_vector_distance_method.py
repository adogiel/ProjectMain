# Emotion and Reason in Political Language
# -- Replication Package
# Gennaro and Ash
# 2021

# Description:
# - This code creates the alternative emotionality measure
# based on the AC vector


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


###################################
#     Working Directory         ###
###################################

wd_data = './data/3_auxiliary_data'
wd_models = './models'

###################################
# Upload word vectors           ###
###################################

w2v = Word2Vec.load(wd_models + '/w2v-vectors_8_300.pkl', mmap='r')


###################################
#     AC VECTOR                 ###
###################################

os.chdir(wd_data)
freq = joblib.load('word_freqs.pkl')
affect = joblib.load('affect_centroid.pkl')
cognition = joblib.load('cog_centroid.pkl')

# create the AC vector
ac = affect - cognition


############################################
# find SIF weighted document vector      ###
############################################

def documentvecweight(lista):
    out = []
    for s in lista:
        vecs = [w2v.wv[w] * freq[w] for w in s[1] if w in w2v.wv]  # extract word vectors, weighted
        if len(vecs) == 0:
            d = np.nan
        else:
            v = np.mean(vecs, axis=0)  # take mean
            v = v.reshape(1, -1)
            v = v.tolist()
            d = cosine(v, ac)
        out.append([s[0], d])
    return out


# Upload pre-processed speeches
DATA = glob.glob("speeches_indexed_clean1*.pkl") + \
    glob.glob("speeches_indexed_clean2*.pkl") + \
    glob.glob("speeches_indexed_clean3*.pkl") + \
    glob.glob("speeches_indexed_clean4*.pkl")


tot = []
for d in DATA:
    testi = joblib.load(d)
    vec = documentvecweight(testi)
    tot = tot + vec


# dump
tot = pd.DataFrame(tot)
tot.columns = ['title', 'vec_score']
joblib.dump(tot, 'vector_distance.pkl')
