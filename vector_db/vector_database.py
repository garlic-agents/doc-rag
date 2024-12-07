from typing import TypedDict, List

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings, Collection

from embedding.data_embedding import DataEmbedding

DEFAULT_COLLECTION_NAME = "default"


class VectorDBData(TypedDict):
    id: str
    data: str


class VectorDatabase:

    # Constructor
    def __init__(self, default_collection_name=DEFAULT_COLLECTION_NAME):
        self.collection: Collection | None = None
        self.client = chromadb.PersistentClient()
        # 检查是否启动成功
        if self.client is None or self.client.heartbeat() < 0:
            raise Exception("Failed to start Vector Database client")
        self.use_collection(default_collection_name)

    def use_collection(self, collection_name=DEFAULT_COLLECTION_NAME):
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=DocRagCustomEmbeddingFunction()
        )

    def insert_datas(self, datas: List[VectorDBData], collection_name=DEFAULT_COLLECTION_NAME):
        if self.collection is None:
            self.use_collection(collection_name)
        documents = [doc["data"] for doc in datas]
        ids = [doc["id"] for doc in datas]
        self.collection.add(documents=documents, ids=ids)


class DocRagCustomEmbeddingFunction(EmbeddingFunction[Documents]):

    def __init__(self):
        self._data_embedding = DataEmbedding()

    def __call__(self, input: Documents) -> Embeddings:
        return self._data_embedding.embed_list(input)
