from backend.services.embeddings.generate_embeddings import embed_many


def batch_embed(texts):
    safe_texts = [
        text if text and text.strip() else "No resume evidence provided."
        for text in texts
    ]
    return embed_many(safe_texts)
