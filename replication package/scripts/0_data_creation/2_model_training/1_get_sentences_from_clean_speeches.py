# ===============================================
# Sentence Extraction Script — Guardian Adaptation
# Works with NLTK 3.7 and Python 3.11
# ===============================================

import os
import joblib
import nltk
from nltk import pos_tag
from nltk.tokenize import sent_tokenize
from nltk.stem.snowball import SnowballStemmer
from gensim.utils import simple_preprocess
from random import shuffle

# Download punkt if not already
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# === Paths ===
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))
data_path = os.path.join(project_root, 'data')
word_freqs = joblib.load(os.path.join(data_path, 'word_frequencies', 'word_counts.pkl'))
stopwords = joblib.load(os.path.join(data_path, 'stopwords.pkl'))

# === Stemmer ===
stemmer = SnowballStemmer("english")

# === Sentence extraction and cleaning function ===
def extract_sentences(file_path):
    print(f"🔹 Processing: {os.path.basename(file_path)}")
    data = joblib.load(file_path)
    texts = [row[1] for row in data]

    sentences = []
    for tokens in texts:
        text_str = ' '.join(tokens)
        doc_sents = sent_tokenize(text_str)
        sentences.extend(doc_sents)

    # Cleaning pipeline
    sentences = [s for s in sentences if len(s.split()) > 1]
    sentences = [simple_preprocess(s) for s in sentences]
    sentences = [[w for w in s if not w.isdigit() and len(w) > 2] for s in sentences]
    sentences = [pos_tag(s) for s in sentences]
    sentences = [[w for w, tag in s if tag.startswith(('N', 'V', 'J'))] for s in sentences]
    sentences = [[stemmer.stem(w) for w in s] for s in sentences]
    sentences = [[w for w in s if w not in stopwords and word_freqs.get(w, 0) >= 10] for s in sentences]
    sentences = [s for s in sentences if len(s) > 1]
    shuffle(sentences)

    # Save processed output
    output_path = file_path.replace('_clean.pkl', '_sentences.pkl')
    joblib.dump(sentences, output_path)
    print(f"✅ Saved {len(sentences)} sentences → {os.path.basename(output_path)}")

# === Run on all cleaned Guardian article batches ===
if __name__ == "__main__":
    files = [
        'rawarticles_indexed1_n_clean.pkl',
        'rawarticles_indexed2_n_clean.pkl',
        'rawarticles_indexed3_n_clean.pkl',
        'rawarticles_indexed4_n_clean.pkl'
    ]
    for f in files:
        extract_sentences(os.path.join(data_path, f))
