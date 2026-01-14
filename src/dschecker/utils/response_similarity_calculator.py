import openai
import numpy as np


def get_embedding(texts: list[str]) -> list:
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )
    embeddings = [d.embedding for d in response.data]
    return embeddings


def get_cosine_similarity(list_json_strings):
    embedding_array = np.array(get_embedding(list_json_strings))
    sims = np.dot(embedding_array, embedding_array.T)/np.dot(np.abs(embedding_array), np.abs(embedding_array.T))
    i, j = np.triu_indices(sims.shape[0], 1)
    return sims[i, j]
