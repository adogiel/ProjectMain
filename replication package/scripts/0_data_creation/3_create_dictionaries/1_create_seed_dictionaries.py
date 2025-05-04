# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# - Extract lwic dictionaries
# - Matches them to nlp vocabulary
# - Eliminate words that are too far
# Output is the final affect and cognition dictionaries

###################################
#     Modules                   ###
###################################

import string
import os
from glob import glob
import spacy
from scipy.spatial import distance
import pandas as pd
import numpy as np
import nltk
nltk.download('wordnet')
nlp = spacy.load('en_core_web_lg')  # make sure to use larger model
from nltk.corpus import wordnet as wn
import re
from nltk.tag import perceptron
tagger = perceptron.PerceptronTagger()
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
import joblib

###################################
#     Working directories       ###
###################################

wd_data = './data'
wd_results = './results'

# Set working directory
os.chdir(wd_data)


###################################
#     Match stems               ###
###################################

# Find list and direction of liwc lists
liwc_files = glob('liwc/*txt')

# Create a dictionnary where the key is the liwc label 
# and each entry is the list of tokens from liwc
# Selecting only affect and cognition

labels2words = {}
for lfile in liwc_files:
    label = lfile[:-4].split('-')[-1] # this extracts the label from the title of liwc
    stems = open(lfile).read().split() # creates tokens from each liwc list
    labels2words[label] = stems # I give the liwc label as key to the dict and add the words

del lfile
del label
del liwc_files
del stems

# I extract only the two keys affect and cogproc and create separate lists for affect and cogproc / wildcards and tokens
mydict = dict([ (k, labels2words.get(k, None)) for k in ['affect', 'cogproc']])


# Separate wildcards from clean tokens for affect
tokens_affect = set()
wildcards_affect = ''

for x in mydict['affect']:
    if '*' in x:
        x = x.replace('*','[a-z]*') # this replaces * with [a-z]* and puts all the liwc stems in wildcards
        wildcards_affect += '(' + x + ')|'
    else:
        tokens_affect.add(x) # only "clean" tokens get into the tokens set
wildcards_affect = wildcards_affect[:-1]
del x


# Separate wildcards from clean tokens for cognition
tokens_cog = set()
wildcards_cog = ''

for x in mydict['cogproc']:
    if '*' in x:
        x = x.replace('*','[a-z]*') # this replaces * with [a-z]* and puts all the liwc stems in wildcards
        wildcards_cog += '(' + x + ')|'
    else:
        tokens_cog.add(x) # only "clean" tokens get into the tokens set
wildcards_cog = wildcards_cog[:-1]
del x


# Find the wildcards (after pattern match)
# AFFECT : complete wildcards
wild_affect_matches = []
for i, word in enumerate(wn.all_synsets()):
    w = word.lemma_names()[0].lower()
    if '_' in w:
        continue
    if re.match(wildcards_affect, w): # keeps a word if it matches with the pattern of wildcard above
        wild_affect_matches.append(w)
 #       print(i,w)
wild_affect_matches = set(wild_affect_matches)
del w
del i

tokens_affect = list(tokens_affect.union(wild_affect_matches))
tokens_affect = [s for s in tokens_affect if set.intersection(set(string.punctuation),set(list(s)))==set()]


# CONGITION : complete wildcards
wild_cog_matches = []

for i, word in enumerate(wn.all_synsets()):
    w = word.lemma_names()[0].lower()
    if '_' in w:
        continue
    if re.match(wildcards_cog, w): # keeps a word if it matches with the pattern of wildcard above
        wild_cog_matches.append(w)
 #       print(i,w)
wild_cog_matches = set(wild_cog_matches)
del i
del w


tokens_cog = list(tokens_cog.union(wild_cog_matches))
tokens_cog = [s for s in tokens_cog if set.intersection(set(string.punctuation),set(list(s)))==set()]


# eliminate common words between the two lists
intersection = sorted(list(set.intersection(set(tokens_cog),set(tokens_affect))))
tokens_cog = [s for s in tokens_cog if s not in intersection]
tokens_affect = [s for s in tokens_affect if s not in intersection]
del intersection

# eliminate words not in nlp vocabulary as these are not assigned any vector
tokens_cog = [s for s in tokens_cog if s in nlp.vocab]
tokens_affect = [s for s in tokens_affect if s in nlp.vocab]


###################################
# Eliminate words that are unrelated
###################################

def findunrelatedwords(tokens):
    s = ' '.join(tokens) # put initial words in a string
    s = nlp(s) # find word vectors with pre-trained vectors
    center = s.vector
    l= [] # list of tuples (word, cosine distance from the centroid)
    for t in range(len(tokens)):
        if s[t].has_vector:
            d = (s[t].text, distance.cosine(center, s[t].vector))
            l.append(d)
        else:
            continue
    l = sorted(l, key=lambda x: x[1])
    df = pd.DataFrame(l)
    df.columns = ['token', 'distance']
    df = df.dropna()
    df = df.loc[df['distance']<np.percentile(df['distance'], 75)] # eliminate the 25% most dissimilar words
    final = sorted(list(df['token']))
    return final;

affect = findunrelatedwords(tokens_affect)
cognition = findunrelatedwords(tokens_cog)


# List of eliminated words here - for the paper
c = [a for a in tokens_cog if a not in cognition]
a = [b for b in tokens_affect if b not in affect]
os.chdir(results)
with open ('eliminated_words_affect.txt', 'w') as fo:
     fo.write(','.join(str(i) for i in a))
with open ('eliminated_words_cognition.txt', 'w') as fo:
     fo.write(','.join(str(i) for i in c))

print(len(c)) # Number of cognitive words eliminated with findunrelatedwords
print(len(a)) # Number of affect words eliminated with findunrelatedwords


###################################
# Keep only adjectives and verbs
###################################

tagged_affect = tagger.tag(affect)
tagged_cog = tagger.tag(cognition)
affect = [i[0] for i in tagged_affect if i[1].startswith(('N', 'V', 'J'))]
cognition = [i[0] for i in tagged_cog if i[1].startswith(('N', 'V', 'J'))]

del tagged_affect
del tagged_cog

# Stem lwic and eliminate doubles
cognition = list(set([stemmer.stem(item) for item in cognition]))
affect = list(set([stemmer.stem(item) for item in affect]))

# eliminate commons
intersection = sorted(list(set.intersection(set(cognition),set(affect))))
cognition = [s for s in cognition if s not in intersection]
affect = [s for s in affect if s not in intersection]
del intersection


# THIS IS THE NEW STEP WRT THE PREVIOUS VERSION
# eliminate stopwords
os.chdir(wd_data)

stop = joblib.load('stopwords/stopwords.pkl')
proc = joblib.load('procedural language/procedural_words.pkl')
stop = set(stop).union(proc)

affect = [b for b in affect if b not in stop]
cognition = [b for b in cognition if b not in stop]


# Save dictionaries for later use
joblib.dump(cognition, 'dictionaries/dictionary_cognition.pkl')
joblib.dump(affect,'dictionaries/dictionary_affect.pkl') # save final list

# Save of affect and cog words into txt file
os.chdir(wd_results)
with open ('dictionaries/dictionary_affect.txt', 'w') as fo:
     fo.write(','.join(str(i) for i in affect))
with open ('dictionaries/dictionary_cognition.txt', 'w') as fo:
     fo.write(','.join(str(i) for i in cognition))
