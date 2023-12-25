import chromadb
from chromadb import EmbeddingFunction
from llm_feats import get_embedding


class MyEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: str) -> list:
        embedding = get_embedding(input)
        return [embedding]


client = chromadb.PersistentClient(path="chroma_data")

client.heartbeat()

emb_fn = MyEmbeddingFunction()

collection = client.get_collection(
    name="my_collection", embedding_function=emb_fn
)
