from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
import numpy as np

MODEL_PATH = "app/models/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_PATH)

def extract_refined_snippets(sections, persona, job_description, top_n=3):
    query = persona.strip() + " " + job_description.strip()
    query_vec = model.encode(query)
    norm_query = np.linalg.norm(query_vec)

    refined = []

    for sec in sections[:top_n]:
        sentences = sent_tokenize(sec["content"])
        if not sentences:
            continue

        sent_vecs = model.encode(sentences)
        sent_norms = np.linalg.norm(sent_vecs, axis=1)
        sims = (sent_vecs @ query_vec) / (sent_norms * norm_query)

        best_idx = int(np.argmax(sims))
        best_sentence = sentences[best_idx].strip()

        refined.append({
            "document": sec["document"],
            "section_title": sec["section_title"],
            "refined_text": best_sentence,
            "page_number": sec["page_number"]
        })

    return refined
