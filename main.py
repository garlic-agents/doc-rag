import os
import argparse

from dotenv import load_dotenv

from llm import ChatAI
from utils import input_util
from documents import DocumentParser
from vector_db import VectorDatabase

# 加载 .env 文件
load_dotenv(".env.local")
load_dotenv(".env")


## 初始化
def init(vector_db: VectorDatabase):
    parser = argparse.ArgumentParser(description="文档RAG对话原型程序")
    parser.add_argument('-f', '--file', type=str, default="./.data/test.docx", help='需要解析的文件路径')
    args = parser.parse_args()
    # 检查参数信息
    if args.file is None or args.file == "":
        raise Exception("文件路径不能为空")
    print(f"文件路径: {args.file}")
    if not os.path.exists(args.file):
        raise Exception("文件不存在")
    # 解析文档
    document_parser = DocumentParser(args.file)
    parsed_documents = document_parser.parse()
    # 是否向量化
    if input_util.check_user_intention("是否向量化此文档？"):
        vector_db.delete_collection_data()
        vector_db.insert_datas(datas=parsed_documents)
        print("文档向量化完成")


## 开始聊天
def start_chat(vector_db: VectorDatabase):
    chat_ai = ChatAI(vector_db=vector_db)
    while True:
        question = input_util.get_input("#请输入问题")
        if question.startswith("/"):
            if question in ["/h", "/help"]:
                # 帮助
                print("指令说明：")
                print("/h, /help\t\t\t显示帮助信息")
                print("/q, /quit, /exit\t\t退出程序")
                print("/r, /reset\t\t\t重置对话")
                continue
            elif question in ["/q", "/quit", "/exit"]:
                # 退出
                break
            elif question in ["/r", "/reset"]:
                # 重置
                chat_ai.clean_messages()
                print("对话已重置")
                continue
            else:
                print("未知指令，请重新输入")
                continue
        chat_ai.ask(question)


if __name__ == '__main__':
    vdb = VectorDatabase()
    init(vdb)
    start_chat(vdb)
