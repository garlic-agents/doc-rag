import os

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from vector_db import VectorDatabase


class ChatAI:

    def __init__(self, vector_db: VectorDatabase, model: str = "qwen-plus", stream: bool = True):
        self.vector_db = vector_db
        self.model = model
        self.stream = stream
        self.client: OpenAI = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        if not self.client:
            raise Exception("dashscope client 问答接口初始化失败")
        self.messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": "你好"
            }
        ]

    def clean_messages(self):
        self.messages = [
            {
                "role": "system",
                "content": "你好"
            }
        ]

    def ask(self, question: str):
        self.messages.append({
            "role": "user",
            "content": question
        })
        # 从向量化数据库初始化提示词
        self._init_prompt(question)
        # 发送请求
        self._send_request()
        pass

    def _init_prompt(self, question: str):
        # 优化问题内容，方便向量化数据库查询（待定）
        # TODO 查询向量化数据库
        self.vector_db.query(question)
        pass

    def _send_request(self):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=self.stream,
            stream_options={"include_usage": True}
        )
        for chunk in completion:
            print(chunk.model_dump_json())
