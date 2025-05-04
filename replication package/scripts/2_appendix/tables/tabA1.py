# Emotion and Reason in Political Language: Replication Package
# Gennaro and Ash

# Description:
# Fig A21

# NB: the table cannot be exactly reproduced with
# the data in the replication package
# as this requires access to the original speeches

# This code extracts the most affective and cognitive sentences in the corpus
    # Select the top 5000 emotional and cognitive speeches
    # Extract SENTENCES
    # Select the top 1% emotional and congnitive SENTENCES
    # Randomly select 10 from those


###################################
#     Modules                   ###
###################################

from gensim.summarization.textcleaner import get_sentences
from nltk.stem.snowball import SnowballStemmer
import nltk
import gensim
import os
import joblib
import pandas as pd
import re
from gensim.models import Word2Vec
from scipy.spatial.distance import cosine
import numpy as np
import random

###################################
#     Parameters                ###
###################################

n_speeches = 5000
n_sentences = 10

###################################
#     Working Directory         ###
###################################

wd = "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

wd_data = wd + '/3 Replication Package/data/1_main_datasets'  # set the data directory
wd_results = wd + '/3 Replication Package/results/appendix'  # set the results directory
wd_aux = wd + '/3 Replication Package/data/3_auxiliary_data'  # set the auxiliary data directory
wd_model = wd + '/3 Replication Package/models'  # set the model directory


###################################
#     Upload dataset            ###
###################################

df = pd.read_csv(wd_data + '/main_dataset.csv', low_memory=False)

# Extract the titles of the most affective and cognitive speeches

df = df[['title', 'score']]

df = df.dropna()  # eliminate rows with missing values
df = df.reset_index(drop=True)
df = df.sort_values(by=['score'], ascending=[False])

t_a = df.head(n_speeches)  # extracts the top 5000 emotional speeches
t_c = df.tail(n_speeches)  # extracts the top 5000 cognition speeches

del df


###################################
#     Upload dataset            ###
###################################

# Upload speeches to match on title and extract text

data = joblib.load(wd_aux + '/synth_speeches_tabA1.pkl')
data = pd.DataFrame(data)

data.columns = ['title', 'text']

top_a = pd.merge(t_a, data, on=['title'], how='inner')
top_c = pd.merge(t_c, data, on=['title'], how='inner')

top_a = top_a['text'].values.tolist()
top_c = top_c['text'].values.tolist()


###################################
# Clean Speeches                ###
###################################

def cleaning(data):
    data = [item for item in data if len(item.split()) > 0]
    data = [item.replace('\n', ' ') for item in data]
    data = [re.sub(r'(?<=[.,])(?=[^\s])', r' ', item) for item in data] # aggiungi spazi fra punto e maiuscola
    data = [w.replace("\\\\'", "'") for w in data] # Modify to avoid fake sentences
    data = [w.replace('Mrs.', 'Mrs') for w in data] # Modify to avoid fake sentences
    data = [w.replace('Ms.', 'Ms') for w in data] # Modify to avoid fake sentences
    data = [w.replace('Mr.', 'Mr') for w in data] # Modify to avoid fake sentences
    data = [w.replace('Dr.', 'Dr') for w in data] # Modify to avoid fake sentences
    data = [w.replace('vs.', 'vs') for w in data] # Modify to avoid fake sentences
    data = [w.replace('Jr.', 'Jr') for w in data] # Modify to avoid fake sentences
    data = [re.sub("[\[].*?[\]]", "", w) for w in data] # eliminate everything in []
    data = [re.sub("[\(].*?[\)]", "", w) for w in data] # eliminate everything in ()
    #data = [re.sub("[\(\[].*?[\)\]]", "", w) for w in data] # eliminate everything in [) or (]
    data = [re.sub(r'([ \(\[][A-Z])([.] )', r"\1 ", w) for w in data]  # eliminate dot after single capital letter
    data = [re.sub(r'([0-9])([.])([0-9])', r"\1\3 ", w) for w in data]  # eliminate dot after single capital letter
    data = [re.sub(r'([N][o][ ]?)([\.])([ ]?[0-9]+[ ])', r"\1\3", w) for w in data]  # transforms cases like No. 5 into No 5
    data = [re.sub(r"-\s", "", item) for item in data]
    return data


top_a = cleaning(top_a)
top_c = cleaning(top_c)


###################################
# Split sentences               ###
###################################

# Split sentences from the top speeches
top_a_s = []
for doc in top_a:
    top_a_s += get_sentences(doc)

top_c_s = []
for doc in top_c:
    top_c_s += get_sentences(doc)


###################################
# Preprocess                    ###
###################################

# Clean sentences
stop = joblib.load(wd_aux + '/stopwords.pkl')
proc = joblib.load(wd_aux + '/procedural_words.pkl')
stop = set(stop).union(proc)

stemmer = SnowballStemmer("english")
tagger = nltk.perceptron.PerceptronTagger()
selected = set(['N', 'V', 'J'])
count = joblib.load(wd_aux + '/word_counts.pkl')


def cleaning2(data):
    data = [gensim.utils.simple_preprocess(item) for item in data]
    data = [tagger.tag(s) for s in data] # Assign part of speech
    data = [[[i[0], i[1][0]] for i in d] for d in data]
    data = [[i[0] for i in d if i[1] in selected] for d in data] # keep only nouns adj verbs
    data = [[stemmer.stem(w) for w in s] for s in data]
    data = [[w for w in item if not w in stop] for item in data]
    data = [[w for w in l if not w.isdigit()] for l in data]
    data = [[a for a in s if count[a] >= 10] for s in data]
    return data

top_a_s2 = cleaning2(top_a_s)
print('This should be True: %r' % (len(top_a_s) == len(top_a_s2)))

top_c_s2 = cleaning2(top_c_s)
print('This should be True: %r' % (len(top_c_s) == len(top_c_s2)))

del count
del tagger
del stemmer
del stop
del selected


###################################
# Calculate score for sentences
###################################

freq = joblib.load(wd_aux + '/word_freqs.pkl')
cognition = joblib.load(wd_aux + '/cog_centroid.pkl')
affect = joblib.load(wd_aux + '/affect_centroid.pkl')
w2v = Word2Vec.load(wd_model + '/w2v-vectors_8_300.pkl', mmap='r')

# find SIF weighted document vector
def documentvecweight(lista):
    out = []
    for s in lista:
        vecs = [w2v.wv[w] * freq[w] for w in s if w in w2v.wv]  # extract word vectors, weighted
        if len(vecs) == 0:
            a = np.nan
            c = np.nan
            z = np.nan
        else:
            v = np.mean(vecs, axis=0)  # take mean
            v = v.reshape(1, -1)
            v = v.tolist()
            a = cosine(v, affect)
            c = cosine(v, cognition)
            z = (1 - a + 1) / (1 - c + 1)
        out.append(z)
    return out


a = documentvecweight(top_a_s2)
print('This should be True: %r' % (len(top_a_s) == len(a)))

c = documentvecweight(top_c_s2)
print('This should be True: %r' % (len(top_c_s) == len(c)))

a = list(zip(top_a_s, a))
c = list(zip(top_c_s, c))


###############################################
# Extract top 1% emotional/congitive sentences
# and then 10 random sentences from those
###############################################

a = [i for i in a if len(i[0].split()) > 3]
a.sort(key=lambda x: x[1])
m = int(len(a) * 0.01)
top_affect = [i[0] for i in a[-m:]]

random.seed(30)
top_affect = random.sample(top_affect, n_sentences)

c = [i for i in c if len(i[0].split()) > 3]
c.sort(key=lambda x: x[1])
m = int(len(c) * 0.01)
top_cog = [i[0] for i in c[:m]]

random.seed(30)
top_cog = random.sample(top_cog, n_sentences)


os.chdir(wd_results)
with open('tabA1_affect.txt', 'w') as f:
    for item in top_affect:
        f.write("%s\n\n" % item)

with open('tabA1_logic.txt', 'w') as f:
    for item in top_cog:
        f.write("%s\n\n" % item)
