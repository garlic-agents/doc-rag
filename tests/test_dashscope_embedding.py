from embedding.dashscope_embedding import DashscopeEmbedding


def test_dashscope_embedding():
    embedding = DashscopeEmbedding()
    data = "data"
    embeddings = embedding.embed(data)
    print(f"\nEmbed Data: {embeddings}\n")
    assert embeddings not in [None, []]
