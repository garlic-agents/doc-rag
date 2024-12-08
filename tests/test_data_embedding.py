from embedding.dashscope_embedding import DashscopeEmbedding
from embedding.data_embedding import DataEmbeddingFactory


def test_dashscope_embedding():
    embedding = DashscopeEmbedding()
    data = "data"
    embeddings = embedding.embed(data)
    print(f"\nEmbed Data: {embeddings}\n")
    assert embeddings not in [None, []]


def test_data_embedding():
    embedding = DataEmbeddingFactory.create()
    embed_list = embedding.embed_list(["data1", "data2"])
    print(f"\nEmbed List: {embed_list}\n")
    assert embed_list not in [None, []]
