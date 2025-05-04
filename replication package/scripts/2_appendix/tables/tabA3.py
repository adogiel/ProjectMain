# Emotion and Reason in Political Language: Replication Package
# Gennaro and Ash

# Description:
# Tab A3

# NB: the table cannot be exactly reproduced with
# the data in the replication package
# as this requires access to the original speeches

# This code extracts the most affective and cognitive sentences in the corpus
    # Filter speeches about social issues
    # Select the top 5000 emotional and cognitive speeches
    # Extract SENTENCES that include the topic keyword
    # Select the top 1% emotional and congnitive SENTENCES
    # Randomly select 10 from those

# For extracting sentences about other topics, change the values of:
# - topic_selected
# - keyword


###################################
#     Parameters                ###
###################################

# hyperparms
n_speeches = 5000
n_sent = 1000000
pct = 10  # With 1% not enough sentences speaking about abortion

topic_selected = 'Social Issues'
keyword = 'abortion'

###################################
#     Modules                   ###
###################################

import os
import numpy as np
import pandas as pd
import joblib
import re
import random
import gensim
from gensim.summarization.textcleaner import get_sentences
from gensim.models import Word2Vec
from scipy.spatial.distance import cosine
import nltk
from nltk.stem.snowball import SnowballStemmer
from random import shuffle
tagger = nltk.perceptron.PerceptronTagger()
stemmer = SnowballStemmer("english")


###################################
#     Working Directory         ###
###################################

wd = "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

wd_data =  wd + '/3 Replication Package/data/1_main_datasets'  # set the data directory
wd_results = wd + '/3 Replication Package/results/appendix'  # set the results directory
wd_aux =  wd + '/3 Replication Package/data/3_auxiliary_data'  # set the auxiliary data directory
wd_model = wd + '/3 Replication Package/models'  # set the model directory


###################################
#     Upload dataset            ###
###################################

dataset = pd.read_csv(wd_data + '/main_dataset.csv', low_memory=False)
dataset = dataset.dropna()
dataset = dataset.reset_index(drop=True)

# Add demeaned score and adjust come vars
dataset = dataset.rename(columns={"topic1_new": "topic_num"})
dataset['topic_num'] = pd.to_numeric(dataset['topic_num'], downcast='integer')



########################################################
#    Merge with topic label for interpretability     ###
########################################################

topic_labels = pd.read_csv(wd_aux + '/topics_numbers.csv', header=None)
topic_labels = list(topic_labels[0])
topic_labels = [[topic_labels[x], topic_labels[x + 1], topic_labels[x + 2]]
                for x in range(0, len(topic_labels) - 1, 3)]
topic_labels = pd.DataFrame(topic_labels, columns=['topic_num', 'topic', 'theme'])
topic_labels['topic_num'] = pd.to_numeric(topic_labels['topic_num'], downcast='integer')
topic_labels[['topic_broad', 'topic_detail']] = topic_labels['topic'].str.split(' - ', 1, expand=True)

dataset = pd.merge(dataset, topic_labels, on='topic_num', how='left')

dataset = dataset[['title', 'speech_year', 'score', 'topic_broad']]


###################################
#     Select the broad topic    ###
###################################

df = dataset[dataset.topic_broad == topic_selected]

# top speeches
df = df.sort_values(by=['score'], ascending=[False])
a = df.head(n_speeches)
c = df.tail(n_speeches)

t_a = a[['title']]
t_c = c[['title']]

del df
del a
del c

###################################
#     Extract the speeches      ###
###################################


data = joblib.load(wd_aux + '/synth_speeches_tabA3.pkl')

data = pd.DataFrame(data)
data.columns = ['title', 'text']

data_a = pd.merge(t_a, data, on=['title'], how='inner')
data_c = pd.merge(t_c, data, on=['title'], how='inner')

data_a = data_a['text'].values.tolist()
data_c = data_c['text'].values.tolist()


###################################
#   Extract Random Sentences    ###
###################################

def extract_sentences(process, n_sent=n_sent):
    # Extract a Random sample of n_sent sentences
    # Output is: [id, decade, sentence]
    if process == 'affect':
        data1 = data_a
    else:
        data1 = data_c
    
    data1 = [w.replace('Jr.', 'Jr') for w in data1] # Modify to avoid fake sentences
    data1 = [w.replace('Mrs.', 'Mrs') for w in data1]  # Modify to avoid fake sentences
    data1 = [w.replace('Ms.', 'Ms') for w in data1]  # Modify to avoid fake sentences
    data1 = [w.replace('Mr.', 'Mr') for w in data1]  # Modify to avoid fake sentences
    data1 = [w.replace('Dr.', 'Dr') for w in data1]  # Modify to avoid fake sentences
    data1 = [w.replace("\\\\'", "'") for w in data1] # Modify to avoid fake sentences
    data1 = [re.sub("\[.*\]", "", w) for w in data1]  # eliminate everything in []
    data1 = [re.sub("\(.*\)", "", w) for w in data1]  # eliminate everything in ()
    data1 = [re.sub(r'([ \(\[][A-Z])([.] )', r"\1 ", w) for w in data1] # eliminate dot after single capital letter
    data1 = [re.sub(r'([0-9])([.])([0-9])', r"\1\3 ", w) for w in data1] # eliminate dot after single capital letter
    data1 = [re.sub(r'([N][o][ ]?)([\.])([ ]?[0-9]+[ ])', r"\1\3", w) for w in data1] # transforms cases like No. 5 into No 5
    data1 = [d for d in data1 if re.search(r'=""', d) is None]

    # Get list of sentences and extract random sample
    sent = [] # Container for random sentences from current dataset - decade
    for doc in data1:
        sent += get_sentences(doc)
    if len(sent) > n_sent:
        sent = random.sample(sent, n_sent)
        print(str(len(sent)) + ' sentences extracted')
    else:
        print(str(len(sent)) + ' sentences extracted')

    sent = [d for d in sent if keyword in d]
    sent = [s for s in sent if re.search("[A-Z]\w+[,][ ]+[A-Z]\w+[,][ ]+[A-Z]\w+[,][ ]+[A-Z]\w+[,][ ]", s)==None] # eliminate sentences with at least three names e.g. Smith, John, Klein, would match the pattern
    sent = [s for s in sent if re.match("^[a-z]", s) is None] # eliminate sentences that start with lower case letters
    sent = [s for s in sent if re.match("^\W[ ]", s) is None] # eliminate setences that start with special character
    sent = [s for s in sent if re.match("^[1-9]", s) is None] # eliminate setences that start with special character
    sent = [re.sub(r"[\\][\']", r"''", s) for s in sent] # eliminate \' and replace with just '
    sent = [s for s in sent if len(s.split())>2] # eliminate sentences with less that 4 words

    ids = [item for item in range(0, len(sent))]  # Create unique ids to sentences
    
    if process == 'affect':
        ids = ['a' + str(i) for i in ids]
    else:
        ids = ['c' + str(i) for i in ids]

    S = list(zip(ids, sent))  # Assign ids
    return S


sentences_a = extract_sentences(process='affect', n_sent=n_sent)
sentences_c = extract_sentences(process='cognition', n_sent=n_sent)

# SAVE CLEAN SENTENCES WITH ID FOR LATER
STORED = sentences_a + sentences_c

##########################################
#   Preprocess sentences for scoring   ###
##########################################

stop = joblib.load(wd_aux + '/stopwords.pkl')
proc = joblib.load(wd_aux + '/procedural_words.pkl')
stop = set(stop).union(proc)

count = joblib.load(wd_aux + '/word_counts.pkl')

def preprocess_sent(sentences):
    # Tokenize
    sentences = [[item[0], gensim.utils.simple_preprocess(item[1])] for item in sentences]
    sentences = [[item[0], [a for a in item[1] if len(a) > 2]] for item in sentences]
    sentences = [item for item in sentences if len(item[1]) > 0]

    # Digits
    sentences = [[item[0], [a for a in item[1] if not a.isdigit()]] for item in sentences]

    # Assign part of speech and keep only nouns adj verbs
    sentences = [[s[0], tagger.tag(s[1])] for s in sentences]
    sentences = [[s[0], [i[0] for i in s[1] if i[1].startswith(('N', 'V', 'J'))]] for s in sentences]
    sentences = [s for s in sentences if len(s[1]) > 0]  # eliminate empty rows

    # stem
    sentences = [[s[0], [stemmer.stem(i) for i in s[1]]] for s in sentences]

    # eliminate stopwords
    sentences = [[s[0], [a for a in s[1] if a not in stop]] for s in sentences]

    # eliminate unfrequent words
    sentences = [[s[0], [a for a in s[1] if count[a] >= 10]] for s in sentences]
    sentences = [s for s in sentences if len(s[1]) > 2]  # eliminate empty rows / at least 3 words in the sentence

    return sentences


sentences_a = preprocess_sent(sentences_a)
sentences_c = preprocess_sent(sentences_c)

##########################################
#   Score the sentences                ###
##########################################

# Function to find SIF weighted document vector and score

# Upload all components

w2v = Word2Vec.load(wd_model + '/w2v-vectors_8_300.pkl', mmap='r')
affect = joblib.load(wd_aux + '/affect_centroid.pkl')
cognition = joblib.load(wd_aux + '/cog_centroid.pkl')
freq = joblib.load(wd_aux + '/word_freqs.pkl')


def documentvecweight(lista):
    out = []
    for s in lista:
        vecs = [w2v.wv[w] * freq[w] for w in s[1] if w in w2v.wv]  # extract word vectors, weighted
        if len(vecs) == 0:
            a = np.nan
            c = np.nan
        else:
            v = np.mean(vecs, axis=0)  # take mean
            v = v.reshape(1, -1)
            v = v.tolist()
            a = cosine(v, affect)
            c = cosine(v, cognition)
            d = (1+1-a)/(1+1-c)  # cosine similarity measure smoothed
        out.append([s[0], a, c, d])  # output is [sent id, affect, congnition, score]
    return out


# Apply the function
data_a = documentvecweight(sentences_a)
data_a = [a for a in data_a if not str(a[3]) == 'nan']  # drop if score cannot be calculated (shouldn't drop anything)

data_c = documentvecweight(sentences_c)
data_c = [a for a in data_c if not str(a[3]) == 'nan']  # drop if score cannot be calculated (shouldn't drop anything)



##############################################
#   Create sentence sets                   ###
##############################################

def create_sentence_sets(data_a, data_c, pct, n_sent_f=10):
    # Input: list of setences with scores
    # Output: pair id, sent id, decade, affect, cognition, score

    score_a = [a[3] for a in data_a]
    score_c = [a[3] for a in data_c]

    if len(data_a)< 10*n_sent_f:
        top_sent = data_a
    else:
        top_pc = np.percentile(score_a, 100 - pct)
        top_sent = [a for a in data_a if a[3] > top_pc]

    if len(data_c)< 10*n_sent_f:
        bot_sent = data_c
    else:
        bot_pc = np.percentile(score_c, 100 - pct)
        bot_sent = [a for a in data_c if a[3] > bot_pc]

    random.seed(30)
    shuffle(top_sent)

    random.seed(30)
    shuffle(bot_sent)

    if len(top_sent)<n_sent_f:
        print('The number of Available affect sentences is smaller than 10')
    else: 
        random.seed(30)
        top_sent = random.sample(top_sent, n_sent_f)


    if len(bot_sent)<n_sent_f:
        print('The number of Available cognitive sentences is smaller than 10')
    else: 
        random.seed(30)
        bot_sent = random.sample(bot_sent, n_sent_f)

    return top_sent, bot_sent


top_sent, bot_sent = create_sentence_sets(data_a=data_a, data_c=data_c, pct=pct)

##############################################
#   Match pairs back to sentences          ###
##############################################

A_sent = pd.DataFrame(top_sent)
A_sent.columns = ['sent_id', 'affect_d', 'cognition_d', 'score']
A_sent['sent_id'] = A_sent['sent_id'].astype(str)

C_sent = pd.DataFrame(bot_sent)
C_sent.columns = ['sent_id', 'affect_d', 'cognition_d', 'score']
C_sent['sent_id'] = C_sent['sent_id'].astype(str)

STORED = pd.DataFrame(STORED)
STORED.columns = ['sent_id', 'sentence']
STORED['sent_id'] = STORED['sent_id'].astype(str)

final_A = pd.merge(A_sent, STORED, how='left', on=['sent_id'])
final_C = pd.merge(C_sent, STORED, how='left', on=['sent_id'])

final_A = final_A['sentence'].values.tolist()
final_C = final_C['sentence'].values.tolist()



##############################################
#   Save                                   ###
##############################################

os.chdir(wd_results)
with open('tabA3_affect.txt', 'w') as f:
    for item in final_A:
        f.write("%s\n\n" % item)

with open('tabA3_logic.txt', 'w') as f:
    for item in final_C:
        f.write("%s\n\n" % item)
