from enum import Enum


class Engine(Enum):
    DASHSCOPE = "dashscope"


class DataEmbedding:

    def embed(self, data: str) -> list:
        ...

    def embed_list(self, data_list: list) -> list:
        ...


class DataEmbeddingFactory:

    @staticmethod
    def create(engine: Engine = Engine.DASHSCOPE) -> DataEmbedding:
        from .dashscope_embedding import DashscopeEmbedding
        if engine == Engine.DASHSCOPE:
            return DashscopeEmbedding()
        else:
            raise NotImplementedError
