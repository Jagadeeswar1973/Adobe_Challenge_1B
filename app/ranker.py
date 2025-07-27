from sentence_transformers import SentenceTransformer
import numpy as np
import os

# Load model once and reuse
MODEL_PATH = "app/models/all-MiniLM-L6-v2"  # Path inside Docker image
model = SentenceTransformer(MODEL_PATH)

def rank_sections(sections, persona, job_description, top_k=10):
    query = persona.strip() + " " + job_description.strip()
    query_vec = model.encode(query)
    norm_query = np.linalg.norm(query_vec)

    section_texts = [
        sec["section_title"] + " " + sec["content"][:500]
        for sec in sections
    ]
    section_vecs = model.encode(section_texts)
    section_norms = np.linalg.norm(section_vecs, axis=1)

    sims = (section_vecs @ query_vec) / (section_norms * norm_query)

    for sec, sim in zip(sections, sims):
        sec["score"] = float(sim)

    ranked = sorted(sections, key=lambda x: x["score"], reverse=True)
    for i, sec in enumerate(ranked, start=1):
        sec["importance_rank"] = i

    return ranked[:top_k]
