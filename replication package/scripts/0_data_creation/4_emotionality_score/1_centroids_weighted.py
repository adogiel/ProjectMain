# ===============================================
# BASED ON: Emotion and Reason in Political Language Replication Package
# ADAPTED FOR MASTER'S PROJECT - GUARDIAN DATA
# Description:
# - Compute SIF-weighted centroids for affect and cognition dictionaries
# ===============================================

import os
import joblib
import numpy as np
from gensim.models import Word2Vec

# === Setup Paths ===
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, "../../../"))

data_dir = os.path.join(project_root, "data")
model_path = os.path.join(project_root, "models", "guardian_w2v_8_300.model")
word_freq_file = os.path.join(data_dir, "word_frequencies", "word_freqs.pkl")
dict_dir = os.path.join(data_dir, "dictionaries")
output_dir = os.path.join(data_dir, "3_auxiliary_data")
os.makedirs(output_dir, exist_ok=True)

# === Load Data ===
affect_words = joblib.load(os.path.join(dict_dir, "dictionary_affect.pkl"))
cognition_words = joblib.load(os.path.join(dict_dir, "dictionary_cognition.pkl"))

w2v_model = Word2Vec.load(model_path)
word_vectors = w2v_model.wv

freqs = joblib.load(word_freq_file)

# === Compute Centroids ===
def compute_centroid(words, model, sif_weights):
    vectors = [model.wv[w] * sif_weights[w] for w in words if w in model.wv and w in sif_weights]
    if not vectors:
        return np.zeros((1, model.vector_size))
    return np.mean(vectors, axis=0).reshape(1, -1)

affect_centroid = compute_centroid(affect_words, w2v_model, freqs)
cognition_centroid = compute_centroid(cognition_words, w2v_model, freqs)

# === Save Centroids ===
joblib.dump(affect_centroid, os.path.join(output_dir, "affect_centroid.pkl"))
joblib.dump(cognition_centroid, os.path.join(output_dir, "cog_centroid.pkl"))

print("✅ Affect and cognition centroids computed and saved.")
