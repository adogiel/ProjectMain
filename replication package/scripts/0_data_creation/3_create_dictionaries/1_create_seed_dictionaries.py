import os
import re
import string
import joblib
import pandas as pd
import numpy as np
import spacy
from glob import glob
from scipy.spatial import distance
from nltk.corpus import wordnet as wn
from nltk.tag import perceptron
from nltk.stem.snowball import SnowballStemmer
import nltk
nltk.download('wordnet')

# === Setup Paths ===
data_dir = r'C:\Users\agnin\Downloads\replication_package\data'
liwc_dir = os.path.join(data_dir, 'liwc')
output_dir = os.path.join(data_dir, 'dictionaries')
stopwords_path = os.path.join(data_dir, 'stopwords', 'stopwords.pkl')
procedural_path = os.path.join(data_dir, 'procedural language', 'procedural_words.pkl')

os.makedirs(output_dir, exist_ok=True)

# === Load Resources ===
nlp = spacy.load('en_core_web_lg')
tagger = perceptron.PerceptronTagger()
stemmer = SnowballStemmer("english")

# === Load LIWC Files ===
liwc_files = glob(os.path.join(liwc_dir, '*txt'))

labels2words = {}
for lfile in liwc_files:
    label = os.path.basename(lfile)[:-4].split('-')[-1]
    stems = open(lfile, encoding='utf-8').read().split()
    labels2words[label] = stems

# === Filter to Affect & Cogproc ===
mydict = {k: labels2words[k] for k in ['affect', 'cogproc']}

def expand_patterns(patterns):
    tokens = set()
    wildcard_re = ''
    for x in patterns:
        if '*' in x:
            x = x.replace('*','[a-z]*')
            wildcard_re += f'({x})|'
        else:
            tokens.add(x)
    wildcard_re = wildcard_re[:-1]  # remove trailing |
    
    wild_matches = []
    for syn in wn.all_synsets():
        w = syn.lemma_names()[0].lower()
        if '_' in w:
            continue
        if re.match(wildcard_re, w):
            wild_matches.append(w)
    return sorted(tokens.union(set(wild_matches)))

tokens_affect = expand_patterns(mydict['affect'])
tokens_cog = expand_patterns(mydict['cogproc'])

# === Remove punctuation and overlap ===
def clean_tokens(tokens):
    return [s for s in tokens if not set(s).intersection(set(string.punctuation))]

tokens_affect = clean_tokens(tokens_affect)
tokens_cog = clean_tokens(tokens_cog)

overlap = set(tokens_affect).intersection(tokens_cog)
tokens_affect = [w for w in tokens_affect if w not in overlap]
tokens_cog = [w for w in tokens_cog if w not in overlap]

# === Keep only tokens with vectors ===
tokens_affect = [w for w in tokens_affect if nlp.vocab[w].has_vector]
tokens_cog = [w for w in tokens_cog if nlp.vocab[w].has_vector]

# === Eliminate Unrelated Words (with safety check) ===
def find_unrelated(tokens, label=""):
    if not tokens:
        print(f"⚠️ No tokens found for {label}. Skipping.")
        return []
    doc = nlp(' '.join(tokens))
    center = doc.vector
    rows = []
    for t in doc:
        if t.has_vector:
            dist = distance.cosine(center, t.vector)
            rows.append((t.text, dist))
    if not rows:
        print(f"⚠️ No usable vectors in {label} tokens.")
        return []
    df = pd.DataFrame(rows, columns=['token', 'distance']).dropna()
    if df.empty:
        print(f"⚠️ No data for percentile calculation in {label}.")
        return []
    threshold = np.percentile(df['distance'], 75)
    return sorted(df[df['distance'] < threshold]['token'].tolist())

print(f"🔍 Filtering Affect: {len(tokens_affect)} tokens")
affect = find_unrelated(tokens_affect, label="Affect")
print(f"🔍 Filtering Cognition: {len(tokens_cog)} tokens")
cognition = find_unrelated(tokens_cog, label="Cognition")

# === Save eliminated words ===
eliminated_affect = [t for t in tokens_affect if t not in affect]
eliminated_cog = [t for t in tokens_cog if t not in cognition]

with open(os.path.join(output_dir, 'eliminated_words_affect.txt'), 'w') as f:
    f.write(','.join(eliminated_affect))
with open(os.path.join(output_dir, 'eliminated_words_cognition.txt'), 'w') as f:
    f.write(','.join(eliminated_cog))

# === POS Tagging (Nouns, Verbs, Adjectives) ===
tagged_affect = tagger.tag(affect)
tagged_cog = tagger.tag(cognition)

affect = [word for word, pos in tagged_affect if pos.startswith(('N', 'V', 'J'))]
cognition = [word for word, pos in tagged_cog if pos.startswith(('N', 'V', 'J'))]

# === Stemming ===
affect = list(set(stemmer.stem(w) for w in affect))
cognition = list(set(stemmer.stem(w) for w in cognition))

# === Remove overlaps again ===
overlap = set(affect).intersection(cognition)
affect = [w for w in affect if w not in overlap]
cognition = [w for w in cognition if w not in overlap]

# === Remove stopwords ===
if os.path.exists(stopwords_path) and os.path.exists(procedural_path):
    stop = set(joblib.load(stopwords_path)).union(joblib.load(procedural_path))
    affect = [w for w in affect if w not in stop]
    cognition = [w for w in cognition if w not in stop]
else:
    print("⚠️ Stopword or procedural .pkl files not found. Skipping stopword filtering.")

# === Save Final Dictionaries ===
joblib.dump(affect, os.path.join(output_dir, 'dictionary_affect.pkl'))
joblib.dump(cognition, os.path.join(output_dir, 'dictionary_cognition.pkl'))

with open(os.path.join(output_dir, 'dictionary_affect.txt'), 'w', encoding='utf-8') as f:
    f.write(','.join(affect))
with open(os.path.join(output_dir, 'dictionary_cognition.txt'), 'w', encoding='utf-8') as f:
    f.write(','.join(cognition))

print(f"✅ Final Affect Words: {len(affect)}")
print(f"✅ Final Cognition Words: {len(cognition)}")
