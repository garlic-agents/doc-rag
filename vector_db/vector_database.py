from typing import TypedDict

import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings, Collection
from typing_extensions import Optional

from embedding.data_embedding import DataEmbeddingFactory

DEFAULT_COLLECTION_NAME = "default"


class VectorDBData(TypedDict):
    id: str
    data: str
    metadata: dict | None


class VectorDatabase:

    # Constructor
    def __init__(self, default_collection_name=DEFAULT_COLLECTION_NAME):
        self.collection_name = default_collection_name
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

    def delete_collection_data(self):
        if self.collection is None:
            return
        # 删除集合
        self.client.delete_collection(name=self.collection_name)
        # 重新创建集合
        self.use_collection(collection_name=self.collection_name)

    def insert_datas(self, datas: list[VectorDBData], collection_name=DEFAULT_COLLECTION_NAME):
        if self.collection is None:
            self.use_collection(collection_name)
        documents = [doc["data"] for doc in datas]
        ids = [doc["id"] for doc in datas]
        self.collection.upsert(documents=documents, ids=ids)

    def query(self, query: str) -> list[str]:
        if self.collection is None:
            raise Exception("Collection is not initialized")
        if query is None or query == "":
            raise Exception("Query is empty")
        query_result = self.collection.query(query_texts=[query], n_results=5)
        return query_result.get("documents", [[]])[0]


class DocRagCustomEmbeddingFunction(EmbeddingFunction[Documents]):

    def __init__(self):
        self._data_embedding = DataEmbeddingFactory.create()

    def __call__(self, input: Documents) -> Embeddings:
        print(f"Embedding {len(input)} documents")
        return self._data_embedding.embed_list(input)
