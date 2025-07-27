from sentence_transformers import SentenceTransformer
import nltk

print("Downloading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
model.save("app/models/all-MiniLM-L6-v2")

print("Downloading NLTK punkt tokenizer...")
nltk.download("punkt")
