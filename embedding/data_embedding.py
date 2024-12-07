from enum import Enum
from .dashscope_embedding import DashscopeEmbedding


class Engine(Enum):
    DASHSCOPE = "dashscope"


class DataEmbedding:

    def __init__(self, engine: Engine = Engine.DASHSCOPE):
        self.engine = engine
        if self.engine == Engine.DASHSCOPE:
            self._embedding_factory = DashscopeEmbedding()
        else:
            raise NotImplementedError

    def embed(self, data) -> list:
        if self.engine == Engine.DASHSCOPE:
            return self._embedding_factory.embed(data)
        else:
            raise NotImplementedError

    def embed_list(self, data_list: list) -> list:
        return [self.embed(data) for data in data_list]
