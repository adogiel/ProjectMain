import os
import glob
import joblib
import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from scipy.spatial.distance import cosine
from multiprocessing import Pool, freeze_support

# === Paths ===
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, "../../../"))
data_dir = os.path.join(project_root, "data")
aux_dir = os.path.join(data_dir, "3_auxiliary_data")
freqs_file = os.path.join(data_dir, "word_frequencies", "word_freqs.pkl")  # <-- fixed path here
model_path = os.path.join(project_root, "models", "guardian_w2v_8_300.model")
results_dir = os.path.join(project_root, "results", "appendix")
os.makedirs(results_dir, exist_ok=True)

# === Load resources ===
print("🔹 Loading models and centroids...")
w2v = Word2Vec.load(model_path)
freqs = joblib.load(freqs_file)
affect_centroid = joblib.load(os.path.join(aux_dir, "affect_centroid.pkl"))
cognition_centroid = joblib.load(os.path.join(aux_dir, "cog_centroid.pkl"))

# === Scoring function ===
def document_vec_score(documents):
    results = []
    for doc in documents:
        title = doc[0]
        words = doc[1]
        vectors = [w2v.wv[w] * freqs.get(w, 1.0) for w in words if w in w2v.wv]
        if not vectors:
            results.append([title, np.nan, np.nan, np.nan])
            continue
        doc_vec = np.mean(vectors, axis=0)
        d_affect = cosine(doc_vec, affect_centroid.flatten())
        d_cognition = cosine(doc_vec, cognition_centroid.flatten())
        score = (1 + 1 - d_affect) / (1 + 1 - d_cognition)
        results.append([title, d_affect, d_cognition, score])
    return results

# === Process individual file ===
def process_file(file_path):
    print(f"🔹 Processing {os.path.basename(file_path)}")
    data = joblib.load(file_path)
    scored = document_vec_score(data)
    temp_file = os.path.join(results_dir, f"scored_{os.path.basename(file_path)}")
    joblib.dump(scored, temp_file)
    return temp_file

# === Main execution ===
def main():
    input_files = sorted(glob.glob(os.path.join(data_dir, "rawarticles_indexed*_n_clean.pkl")))
    with Pool(len(input_files)) as pool:
        temp_files = pool.map(process_file, input_files)

    print("📦 Combining all emotionality scores...")
    all_data = []
    for f in temp_files:
        all_data.extend(joblib.load(f))

    df = pd.DataFrame(all_data, columns=["title", "affect_dist", "cognition_dist", "emotionality_score"])
    joblib.dump(df, os.path.join(aux_dir, "distances_10epochs.pkl"))
    print("✅ All emotionality scores saved.")

if __name__ == "__main__":
    freeze_support()
    main()
