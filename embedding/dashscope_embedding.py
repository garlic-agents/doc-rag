import dashscope
from dashscope import TextEmbedding
from http import HTTPStatus


class DashscopeEmbedding:

    def __init__(self, model=TextEmbedding.Models.text_embedding_v1):
        self.model = model

    def embed(self, source_str) -> list:
        resp = dashscope.TextEmbedding.call(model=self.model, input=source_str)
        if (resp.status_code == HTTPStatus.OK
                and resp.output is not None
                and resp.output.get("embeddings") is not None
                and len(resp.output.get("embeddings")) > 0
                and resp.output.get("embeddings")[0] is not None
                and resp.output.get("embeddings")[0].get("embedding") is not None
        ):
            return resp.output.get("embeddings")[0].get("embedding")
        else:
            raise Exception(f"Failed to embed data: {resp.message}")
