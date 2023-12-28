import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
from llm_feats import get_embedding


class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for doc in input:
            embeddings.append(get_embedding(doc))
            print("produced am embedding!")
        return embeddings


client = chromadb.PersistentClient(path="chroma_data")

client.heartbeat()

emb_fn = MyEmbeddingFunction()

collection = client.get_or_create_collection(
    name="my_collection",
    metadata={"hnsw:space": "cosine"},
    embedding_function=emb_fn,
)
