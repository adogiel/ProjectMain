# ===============================================
# BASED ON: Emotion and Reason in Political Language Replication Package
# ADAPTED FOR MASTER'S PROJECT - GUARDIAN DATA
# Description:
# - Extract clean, POS-filtered sentences from articles
# ===============================================

import os
import joblib
import nltk
from nltk import pos_tag
from nltk.tokenize import sent_tokenize
from nltk.stem.snowball import SnowballStemmer
from random import shuffle
from nltk.tokenize import sent_tokenize
from multiprocessing import Pool, freeze_support

# Ensure NLTK models are available
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# ===============================================
# Paths
# ===============================================

script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))
data_path = os.path.join(project_root, 'data')

# Load stopwords and word frequencies
stopwords = joblib.load(os.path.join(data_path, 'stopwords.pkl'))
word_counts = joblib.load(os.path.join(data_path, 'word_frequencies', 'word_counts.pkl'))

stemmer = SnowballStemmer("english")

# ===============================================
# Sentence extraction function
# ===============================================

def extract_sentences(file_path):
    print(f"🔹 Processing: {os.path.basename(file_path)}")
    
    data = joblib.load(file_path)
    texts = [row[1] for row in data]  # Get tokenized article texts

    sentences = []
    for tokens in texts:
        # Reconstruct sentence from tokens
        text_str = ' '.join(tokens)
        doc_sentences = sent_tokenize(text_str)
        sentences.extend(doc_sentences)

    # Clean and filter
    sentences = [s for s in sentences if len(s.split()) > 1]
    sentences = [simple_preprocess(s) for s in sentences]
    sentences = [[w for w in s if not w.isdigit()] for s in sentences]
    sentences = [[w for w in s if len(w) > 2] for s in sentences]

    # POS tagging: keep nouns, verbs, adjectives
    sentences = [pos_tag(s) for s in sentences]
    sentences = [[w for w, tag in s if tag.startswith(('N', 'V', 'J'))] for s in sentences]

    # Stemming
    sentences = [[stemmer.stem(w) for w in s] for s in sentences]

    # Remove stopwords and rare words
    sentences = [[w for w in s if w not in stopwords] for s in sentences]
    sentences = [[w for w in s if word_counts.get(w, 0) >= 10] for s in sentences]

    # Drop empty sentences
    sentences = [s for s in sentences if len(s) > 1]
    shuffle(sentences)

    # Save
    output_path = file_path.replace('_clean.pkl', '_sentences.pkl')
    joblib.dump(sentences, output_path)
    print(f"✅ Saved: {os.path.basename(output_path)} ({len(sentences)} sentences)")

# ===============================================
# Run with multiprocessing
# ===============================================

if __name__ == "__main__":
    freeze_support()

    files = [
        'rawarticles_indexed1_n_clean.pkl',
        'rawarticles_indexed2_n_clean.pkl',
        'rawarticles_indexed3_n_clean.pkl',
        'rawarticles_indexed4_n_clean.pkl'
    ]

    full_paths = [[os.path.join(data_path, f)] for f in files]

    with Pool(4) as pool:
        pool.starmap(extract_sentences, full_paths)
