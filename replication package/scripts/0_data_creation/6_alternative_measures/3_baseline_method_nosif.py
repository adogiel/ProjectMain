# Emotion and Reason in Political Language
# -- Replication Package
# Gennaro and Ash
# 2021

# Description:
# - Find the document vectors for the cognition and affcet dictionaries
# - These centroids are simple averages, non SIF weighted
# - Calculate emotionality scores for all speeches


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
from multiprocessing import Pool, freeze_support


###################################
#   Working directory           ###
###################################

wd_data = './data/3_auxiliary_data'
wd_models = './models'

###################################
# Upload all elements           ###
###################################

w2v = Word2Vec.load(wd_models + '/w2v-vectors_8_300.pkl', mmap='r')
freq = joblib.load(wd_data + '/word_freqs.pkl')

cognition = joblib.load(wd_data + '/dictionary_cognition.pkl')
affect = joblib.load(wd_data + '/dictionary_affect.pkl')


###################################
# Find the centroid             ###
###################################


def findcentroid(text, model):
    vecs = [model.wv[w] for w in text if w in model.wv]
    vecs = [v for v in vecs if len(v) > 0]
    centroid = np.mean(vecs, axis=0)
    centroid = centroid.reshape(1, -1)
    return centroid


c_affect = findcentroid(affect, w2v)
c_cognition = findcentroid(cognition, w2v)


###################################
# Define Functions              ###
###################################


def documentvecweight(lista):
    out = []
    lista = [i for i in lista if len(i[1]) > 0]
    for s in lista:
        vecs = [w2v.wv[w] * freq[w] for w in s[1] if w in w2v.wv]
        if len(vecs) == 0:
            a = np.nan
            c = np.nan
        else:
            v = np.mean(vecs, axis=0)  # take mean
            v = v.reshape(1, -1)
            v = v.tolist()

            a = cosine(v, c_affect)
            c = cosine(v, c_cognition)
            score = (1 + 1 - a) / (1 + 1 - c)
        out.append([s[0], a, c, score])
    return out


DATA = glob.glob("speeches_indexed_clean1*.pkl") + \
    glob.glob("speeches_indexed_clean2*.pkl") + \
    glob.glob("speeches_indexed_clean3*.pkl") + \
    glob.glob("speeches_indexed_clean4*.pkl")


def main_function(dataname):
    data = joblib.load(dataname)
    data = documentvecweight(data)
    lab = dataname.replace('speeches_indexed_clean', 'temp_distances_nosif_')
    joblib.dump(data, lab)


###################################
#      Multiprocessing          ###
###################################

DATA = [[a] for a in DATA]
pools = len(DATA)
os.chdir(data_c)


def main():
    with Pool(pools) as pool:
        pool.starmap(main_function, DATA)


if __name__ == "__main__":
    freeze_support()
    main()


###################################
#      Single dataset           ###
###################################

DATA = glob.glob('temp_distances_nosif_*.pkl')

tot = []
for dataname in DATA:
    d = joblib.load(dataname)
    tot = tot + d


tot = pd.DataFrame(tot)
tot.columns = ['title', 'affect_d_no_sif', 'cognition_d_no_sif', 'score_no_sif']
joblib.dump(tot, 'distances_nosif_new.pkl')
