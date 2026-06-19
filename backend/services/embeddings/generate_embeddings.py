from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def _load_model():
    try:
        return SentenceTransformer(MODEL_NAME, local_files_only=True)
    except Exception:
        return SentenceTransformer(MODEL_NAME)


model = _load_model()


def embed(text):
    return model.encode(text or "")


def embed_many(texts):
    return model.encode([text or "" for text in texts])
