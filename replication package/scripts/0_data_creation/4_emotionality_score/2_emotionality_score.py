# Emotion and Reason in Political Language
# -- Replication Package
# Gennaro and Ash
# 2021

# Description:
# - Main Emotionality score in speeches


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
#     Working Directory         ###
###################################

wd_data = '../../../data/3_auxiliary_data'  # set the data directory
wd_results = '../../../results/appendix'  # set the results directory
wd_models = '../../../models'  # set the results directory

###################################
# Upload all elements           ###
###################################


w2v = Word2Vec.load(wd_models + '/w2v-vectors_8_300.pkl', mmap='r')

freq = joblib.load(wd_data + '/word_freqs.pkl')
affect = joblib.load(wd_data + '/affect_centroid.pkl')
cognition = joblib.load(wd_data + '/cog_centroid.pkl')


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

            a = cosine(v, affect)
            c = cosine(v, cognition)
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
    lab = dataname.replace('speeches_indexed_clean', 'temp_distances_main_')
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
#      Recompose everything     ###
###################################

DATA = glob.glob('temp_distances_main_*.pkl')

tot = []
for dataname in DATA:
    d = joblib.load(dataname)
    tot = tot + d

tot = pd.DataFrame(tot)
tot.columns = ['title', 'affect_d', 'cognition_d', 'score']
joblib.dump(tot, wd_data + '/distances_10epochs.pkl')


os.remove('distances1.pkl')
os.remove('distances2a.pkl')
os.remove('distances2b.pkl')
os.remove('distances3.pkl')
os.remove('distances4a.pkl')
os.remove('distances4b.pkl')
os.remove('distances4c.pkl')
os.remove('distances4d.pkl')
