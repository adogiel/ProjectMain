# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# - Replicates Figure 1: Word Cloud


###################################
#     Modules                   ###
###################################

import matplotlib
matplotlib.use('Agg')
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import joblib
from gensim.models import Word2Vec

###################################
#     Working Directory         ###
###################################

# indicate here the path to the replication package
wd = "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

wd_data = wd + '/3 Replication Package/data/1_main_datasets'  # set the data directory
wd_results = wd + '/3 Replication Package/results/main_paper'  # set the results directory
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
#     Save                      ###
###################################

wc_affect = nuvolasep(affect_centroid, affect, 100, 'purple')
wc_cog = nuvolasep(cog_centroid, cognition, 100, 'darkgreen')

os.chdir(wd_results)
wc_affect.to_file('fig1a.png')
wc_cog.to_file('fig1b.png')
