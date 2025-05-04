# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# - Replicates Figure A1: Word Cloud
 

###################################
#     Modules                   ###
###################################

import matplotlib
matplotlib.use('Agg')
import numpy as np
from scipy.spatial.distance import cosine
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import joblib
from gensim.models import Word2Vec
import random


###################################
#     Working Directory         ###
###################################

# indicate here the path to the replication package
wd = "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

wd_data = wd + '/3 Replication Package/data/1_main_datasets'  # set the data directory
wd_results = wd + '/3 Replication Package/results/appendix'  # set the results directory
wd_aux = wd + '/3 Replication Package/data/3_auxiliary_data'
wd_model = wd + '/3 Replication Package/models'


###################################
#     Upload dataset            ###
###################################


# Upload word frequencies
freqs = joblib.load(wd_aux + '/word_freqs.pkl')

# Upload model
w2v = Word2Vec.load(wd_model + '/w2v-vectors_8_300.pkl', mmap='r')

# Upload dictionaries
cognition = joblib.load(wd_aux + '/dictionary_cognition.pkl')
affect = joblib.load(wd_aux + '/dictionary_affect.pkl')

# Upload centroids
affect_centroid = joblib.load(wd_aux + '/affect_centroid.pkl')
cog_centroid = joblib.load(wd_aux + '/cog_centroid.pkl')


###################################
#     Set-Up                    ###
###################################

# color function
class SimpleGroupedColorFunc(object):
    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


def nuvolasep(cen, lista, num, col):
    l1 = w2v.wv.most_similar(cen, topn=1000)
    l1 = [a for a in l1 if a not in lista]  # keep only lexicon / non-dictionary word
    l1 = l1[:num]
    max_num = l1[0][1]
    l1 = [(i[0], i[1] / max_num) for i in l1]
    l1w = [i[0] for i in l1]
    color_to_words = {col: l1w}
    l = dict(l1)
    wc = WordCloud(background_color="white", max_words=num, max_font_size=60, random_state=10).generate_from_frequencies(l)
    grouped_color_func = SimpleGroupedColorFunc(color_to_words, 'grey')
    wc.recolor(color_func=grouped_color_func)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    return wc



###################################
#     Sentiment                 ###
###################################

neg = 'hatr, hate, griev, grief'#, wrong'
neg = neg.split(', ')
neg = list(set([stemmer.stem(i) for i in neg])) #145

neg2 = []
for i in neg:
    neg2 += [a[0] for a in w2v.wv.most_similar(i, topn=10)]


pos = 'donat, heart'#, thought'#, strength' #solidar love bless
pos = pos.split(', ')
pos = list(set([stemmer.stem(i) for i in pos])) #145

pos2 = []
for i in pos:
    pos2 += [a[0] for a in w2v.wv.most_similar(i, topn=10)]

pos3 = list(set(pos2) - set(pos2).intersection(set(neg2)))
neg3 = list(set(neg2) - set(pos2).intersection(set(neg2)))

pos3 = [a for a in pos3 if a not in affect+cognition]
neg3 = [a for a in neg3 if a not in affect+cognition]


def findcentroid(text, model):
    vecs=[model.wv[w]*freqs[w] for w in text if w in model.wv]
    vecs=[v for v in vecs if len(v)>0]
    centroid = np.mean(vecs, axis=0)
    centroid = centroid.reshape(1,-1)
    return centroid;


neg_centroid = findcentroid(neg3, w2v)
pos_centroid = findcentroid(pos3, w2v)




###################################
#     Plots                     ###
###################################

d = list(set([stemmer.stem(x) for x in affect]))
a = [(i, cosine(w2v.wv[i], pos_centroid)/cosine(w2v.wv[i], neg_centroid)) for i in d if i in w2v.wv.vocab]
a_pos = [i[0] for i in a if i[1]<1]
a_neg = [i[0] for i in a if i[1]>=1]

a_pos_cent = findcentroid(a_pos, w2v)
a_neg_cent = findcentroid(a_neg, w2v)

wc_pos = nuvolasep(a_pos_cent, a_pos, 100, 'fuchsia')
wc_neg = nuvolasep(a_neg_cent, a_neg, 100, 'purple')

wc_pos.to_file(wd_results + '/figA1b.png')
wc_neg.to_file(wd_results + '/figA1d.png')



d = list(set([stemmer.stem(x) for x in cognition]))
c = [(i, cosine(w2v.wv[i], pos_centroid)/cosine(w2v.wv[i], neg_centroid)) for i in d if i in w2v.wv.vocab]
c_pos = [i[0] for i in c if i[1]<1]
c_neg = [i[0] for i in c if i[1]>=1]

c_pos_cent = findcentroid(c_pos, w2v)
c_neg_cent = findcentroid(c_neg, w2v)

wc_pos = nuvolasep(c_pos_cent, c_pos, 100, 'limegreen')
wc_neg = nuvolasep(c_neg_cent, c_neg, 100, 'darkgreen')

wc_pos.to_file(wd_results + '/figA1a.png')
wc_neg.to_file(wd_results + '/figA1c.png')
