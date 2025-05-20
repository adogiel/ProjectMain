# ===============================================
# BASED ON: Emotion and Reason in Political Language Replication Package
# ADAPTED FOR MASTER'S PROJECT - GUARDIAN DATA
# Description:
# - Train Word2Vec model on sentence-level Guardian data
# ===============================================

import os
import joblib
from gensim.models import Word2Vec

# ===============================================
# Paths
# ===============================================

# Locate script and define paths
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, '..', '..', '..'))
data_dir = os.path.join(project_root, 'data')
model_dir = os.path.join(project_root, 'models')
os.makedirs(model_dir, exist_ok=True)

# Sentence files (Guardian-based)
sentence_files = [
    'rawarticles_indexed1_n_sentences.pkl',
    'rawarticles_indexed2_n_sentences.pkl',
    'rawarticles_indexed3_n_sentences.pkl',
    'rawarticles_indexed4_n_sentences.pkl'
]

# Full paths
sentence_paths = [os.path.join(data_dir, fname) for fname in sentence_files]

# ===============================================
# Load sentence data
# ===============================================

all_sentences = []

for path in sentence_paths:
    print(f"Loading: {os.path.basename(path)}")
    data = joblib.load(path)
    all_sentences.extend(data)  # Flatten to single list of sentences

print(f"✅ Total sentences loaded: {len(all_sentences)}")

# ===============================================
# Train Word2Vec model
# ===============================================

print("🚀 Training Word2Vec model...")
w2v_model = Word2Vec(
    sentences=all_sentences,
    vector_size=300,     # Size of word vectors
    window=8,            # Context window size
    min_count=10,        # Ignore words with freq < 10
    workers=4,           # Parallelism
    sample=1e-3,         # Subsampling frequent words
    epochs=10            # Training epochs
)

# ===============================================
# Save model
# ===============================================

model_path = os.path.join(model_dir, 'guardian_w2v_8_300.model')
w2v_model.save(model_path)
print(f"✅ Word2Vec model saved at: {model_path}")
